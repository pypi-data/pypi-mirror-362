#
# SPDX-FileCopyrightText: Copyright (c) 1993-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
from polygraphy import mod
from polygraphy.json import Decoder, add_json_methods
from polygraphy.logger.logger import G_LOGGER
from polygraphy.tools.args.backend.onnx.loader import OnnxInferShapesArgs, OnnxLoadArgs
from polygraphy.tools.base import Tool
from polygraphy.tools.args import ModelArgs
from polygraphy.tools.args import OnnxSaveArgs
from polygraphy.tools.plugin.subtool.replace import default_replace_with_plugin
from polygraphy.tools.surgeon.subtool.base import BaseSurgeonSubtool

onnx = mod.lazy_import("onnx")
gs = mod.lazy_import("onnx_graphsurgeon")
onnx_backend = mod.lazy_import("polygraphy.backend.onnx")


class AttentionLayerHint:
    def __init__(self, q, gather_kv, gather_q, replace=None):
        self.q = q
        self.gather_kv = gather_kv
        self.gather_q = gather_q
        self.replace = replace

    @staticmethod
    def from_dict(dct):
        return AttentionLayerHint(
            q=dct["q"],
            gather_kv=dct["gather_kv"],
            gather_q=dct["gather_q"],
            replace=dct.get("replace"),
        )

@add_json_methods("shard hints")
class ShardHints:
    def __init__(self, parallelism, n_gpus, root, groups, attention_layers):
        self.parallelism = parallelism
        self.n_gpus = n_gpus
        self.root = root
        self.groups = groups
        self.attention_layers = attention_layers

@Decoder.register(ShardHints)
def decode(dct):
    return ShardHints(
        parallelism=dct["parallelism"],
        n_gpus=dct["n_gpus"],
        root=dct["root"],
        groups=dct["groups"],
        attention_layers=[AttentionLayerHint.from_dict(al) for al in dct["attention_layers"]],
    )

class GraphTraverser():
    def __init__(self, graph):
        self.inputs = {input.name : input for input in graph.inputs}
        self.outputs = {output.name : output for output in graph.outputs}
        self.nodes = {node.name :  node for node in graph.nodes}

        # Tensors are the output of only one node
        self.node_outputs = {output.name: {node.name} for node in graph.nodes for output in node.outputs}

        # Have to handle this slightly differently
        self.node_inputs = {input.name : set() for node in graph.nodes for input in node.inputs}
        for node in graph.nodes:
            for input in node.inputs:
                self.node_inputs[input.name].add(node.name)


    def _traverse(self, node, edges, terminal, relative, dependent, visited):
        visited.add(node.name)
        for name in edges(node):
            if name in terminal:
                dependent.add(name)
            elif name in relative:
                for r in relative[name]:
                    if r not in visited:
                        self._traverse(self.nodes[r], edges, terminal, relative, dependent, visited)

    def get_dep_inputs(self, node):
        inputs = set()
        visited = set()
        self._traverse(
            node,
            lambda n: [input.name for input in n.inputs],
            self.inputs,
            self.node_outputs,
            inputs,
            visited
        )
        return [self.inputs[input_name] for input_name in inputs]

    def get_dep_outputs(self, node):
        outputs = set()
        visited = set()
        self._traverse(
            node,
            lambda n: [output.name for output in n.outputs],
            self.outputs,
            self.node_inputs,
            outputs,
            visited
        )
        return [self.outputs[output_name] for output_name in outputs]

class Shard(Tool):
    """
    Convert a SD model to a MD model using a sharding hints file.
    """

    def __init__(self):
        super().__init__("shard")

    def _make_dist_node(self, graph, tensor, attrs, inputs, outputs, tensors):

        # Prevent tensors from getting sharded multiple times if inputs are the same
        if tensor.name in self.sharded:
            return None

        name = tensor.name + "_md"

        # Make new tensor and node needed
        tensor_md = gs.Variable(name = name, shape = tensor.shape, dtype = tensor.dtype)

        if inputs is None:
            inputs = [tensor_md]
        if outputs is None:
            outputs = [tensor_md]

        node_md = gs.Node(op = "DistCollective", name = "DistCollective_" + str(self.dist_count), inputs = inputs, outputs = outputs, attrs = attrs)
        
        # Update nodes affected by tensor
        for node in [n for n in graph.nodes if tensor in tensors(n)]:
            for i, t in enumerate(tensors(node)):
                if tensor == t:
                    tensors(node)[i] = tensor_md

        # Change layers that have scattered input as tensor          
        for layer in self.hints.attention_layers: 
                if layer.q == tensor.name:
                        layer.q = tensor_md.name
                    
        self.dist_count += 1
        self.sharded.add(tensor.name)
        graph.nodes.insert(0, node_md)
        graph.toposort()

        return tensor_md

    def _make_attrs(self, collective_operation):
        return {
            "collective_operation": collective_operation,
            "reduce_op": "sum",
            "root": self.hints.root,
            "group_size": self.hints.n_gpus,
        }

    def _update_traverser(self, tensor, traverser_dict):
        if tensor is not None:
            traverser_dict.update({tensor.name : tensor})

    def _make_all_gather(self, graph, tensor, traverser):
        """
        Insert an all gather operation to tensor
        T -> T'--AG--T
        """

        G_LOGGER.info(f"Inserting all-gather for tensor: {tensor.name}")
        attrs = self._make_attrs("all_gather")
        tensor_md = self._make_dist_node(graph, tensor, attrs, None, [tensor], lambda n : n.outputs)
        self._update_traverser(tensor_md, traverser.node_inputs)

    def _make_reduce_scatter(self, graph, tensor, traverser):
        """
        Insert a reduce scatter operation to tensor
        T -> T--RS--T'
        """

        G_LOGGER.info(f"Inserting reduce-scatter for tensor: {tensor.name}")
        attrs = self._make_attrs("reduce_scatter")
        tensor_md = self._make_dist_node(graph, tensor, attrs, [tensor], None, lambda n : n.inputs)
        self._update_traverser(tensor_md, traverser.node_outputs)

    def _get_attention_pattern():
        """
        Returns the pattern for canonical attention layers.

        Attention layers follow the pattern:

        Q    K
        |    |
        MatMul
          |
        SoftMax
          |
          |  V
          |  |
        MatMul
          |
        Output
        """
        
        pattern = gs.GraphPattern()
        q = pattern.variable()
        k = pattern.variable()
        v = pattern.variable()

        matmul_1 = pattern.add("MatMul1", "MatMul", inputs=[q, k])
        softmax = pattern.add("Softmax", "Softmax", inputs=[matmul_1])
        matmul_2 = pattern.add("MatMul2", "MatMul", inputs=[softmax, v])
        pattern.set_output_tensors([matmul_2])
        return pattern

    def get_subscriptions_impl(self):
        return [
            ModelArgs(
                model_opt_required=True,
                input_shapes_opt_name=False,
                required_model_type="onnx",
            ),
            OnnxInferShapesArgs(),
            OnnxLoadArgs(outputs_opt_prefix=False),
            OnnxSaveArgs(allow_shape_inference=True, output_opt_required=True),
        ]

    def add_parser_args_impl(self, parser):
        parser.add_argument(
            "-s",
            "--hint",
            help = "Hints file to describe shardable layers.",
            type = argparse.FileType("r"),
            dest = "hint_file",
            required = True
        )

    def run_impl(self, args):
        # Reset state for each run to avoid interference between tests
        self.dist_count = 0
        self.gather_output = False
        self.sharded = set()
        
        surgeon = BaseSurgeonSubtool("shard")
        surgeon.arg_groups = self.arg_groups
        graph = onnx_backend.gs_from_onnx(surgeon.load_model())

        traverser = GraphTraverser(graph)

        G_LOGGER.info(f"Loading sharding hints from: {args.hint_file.name if hasattr(args.hint_file, 'name') else args.hint_file}")
        self.hints = ShardHints.load(args.hint_file)
        G_LOGGER.info(f"Loaded hints: parallelism={self.hints.parallelism}, n_gpus={self.hints.n_gpus}, root={self.hints.root}, groups={self.hints.groups}")
    
        # Get all attention layers that match supported pattern(s)
        pattern = Shard._get_attention_pattern()
        matches = pattern.match_all(graph)
        G_LOGGER.info(f"Found {len(matches)} attention pattern matches in the graph.")

        for layer in self.hints.attention_layers:
            G_LOGGER.info(f"Processing attention layer: q={layer.q}, gather_q={layer.gather_q}, gather_kv={layer.gather_kv}, replace={layer.replace}")
            # Find configuration for matching attenion layer (inputs and outputs match)
            match = next((match for match in matches if match.inputs[0].name == layer.q), None)
            if match is not None:
                gather_q = layer.gather_q
                gather_kv = layer.gather_kv

                # Scatter inputs that q depends on
                for input in traverser.get_dep_inputs(match["MatMul2"].onnx_node):
                    self._make_reduce_scatter(graph, input, traverser)

                # Gather outputs that depend on the output of this attention head
                if not layer.gather_q:
                    for output in traverser.get_dep_outputs(match["MatMul2"].onnx_node):
                        self._make_all_gather(graph, output, traverser)

                # Get tensors directly
                q = match["MatMul1"].onnx_node.inputs[0]
                k = match["MatMul1"].onnx_node.inputs[1]
                v = match["MatMul2"].onnx_node.inputs[1]
                o = list(match["MatMul2"].onnx_node.outputs)
    
                # Determine if attention layer should be replaced with plugin or dist collectives spliced in
                if layer.replace:
                    G_LOGGER.info(f"Replacing attention layer with plugin: {layer.replace}")
                    default_replace_with_plugin(graph, [q, k, v], o, op=layer.replace)

                # Insert collective ops as specified
                for i, tensor in enumerate([q, k, v]): 
                    if [gather_q, gather_kv, gather_kv][i]:
                        self._make_all_gather(graph, tensor, traverser)
                            
            else:
                G_LOGGER.warning(f"No matching attention pattern found for layer with q={layer.q}")

        # Cleanup and save
        graph.cleanup()

        # Manually add in groups attribute since graph surgeon doesn't support
        # type inference for an empty list, which is necessary for a group configuration of '[]'
        model = surgeon.export_graph(graph)
        for node in model.graph.node:
            if node.op_type == "DistCollective":
                node.attribute.append(onnx.helper.make_attribute("groups", self.hints.groups, attr_type = onnx.AttributeProto.INTS))
        
        surgeon.save_model(model)

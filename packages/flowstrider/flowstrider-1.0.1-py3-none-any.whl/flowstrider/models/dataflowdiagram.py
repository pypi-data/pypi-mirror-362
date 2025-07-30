# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import typing
from dataclasses import dataclass, field

from flowstrider.models import common_models


@dataclass
class DataflowDiagram:
    """
    Represents a data flow diagram.

    Attributes:
        id (str): A unique identifier for the diagram.
        nodes (Dict[str, Node]): The nodes in the diagram.
            These can represent processes, external entities, or data stores.
        edges (Dict[str, Edge]): The edges in the diagram.
            These represent data flows between nodes.
        clusters (Dict[str, Cluster]): The clusters in the diagram.
            These contain nodes and represent trust boundaries.
        name (str): The name of the diagram.
        tags (Set[str]): A set of tags specifying the rule set to use
             ['stride', 'bsi_rules'].
        attributes (Dict[str, Any]): Contextual information about the data flow
            diagram. This information is not used in the current version.
    """

    id: str
    nodes: typing.Dict[str, common_models.Node]
    edges: typing.Dict[str, common_models.Edge]
    clusters: typing.Dict[str, common_models.Cluster]
    name: str = ""  # TODO name not used once, id being used instead. Could be removed?
    tags: typing.Set[str] = field(default_factory=set)
    attributes: typing.Dict[str, typing.Any] = field(default_factory=dict)

    def get_node_by_id(self, node_id: str) -> common_models.Node:
        for node in self.nodes.values():
            if node.id == node_id:
                return node
        return None

    def get_clusters_for_node_id(
        self, node_id: int
    ) -> typing.List[common_models.Cluster]:
        # TODO .dot doesn't suppport one node being in more than one subgraph; should
        # ...this function return only one cluster?
        clusters_with_node = []
        for key in self.clusters:
            if node_id in self.clusters[key].node_ids:
                clusters_with_node.append(self.clusters[key])
        return clusters_with_node

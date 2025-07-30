# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import abc
import typing

import networkx as nx

from flowstrider import settings
from flowstrider.models import common_models, dataflowdiagram, threat
from flowstrider.rules import attributes_dict


# Helper method to unify strings for matching
def string_unify(input: str) -> str:
    string = input.casefold()
    string = string.replace(" ", "")
    string = string.replace("-", "")
    string = string.replace("_", "")
    return string


# Helper method
def meet_any_requirement(attribute_in, requirements: list) -> bool:
    if requirements is None or len(requirements) == 0:
        return True
    if attribute_in is None:
        return False

    # Convert
    if isinstance(attribute_in, str):
        attribute = string_unify(attribute_in)
        if attribute == "true":
            attribute = True
        elif attribute == "false":
            attribute = False
    else:
        attribute = attribute_in

    # Check boolean
    if isinstance(attribute, bool) and isinstance(requirements[0], bool):
        return any(attribute == req for req in requirements)
    elif isinstance(attribute, bool) or isinstance(requirements[0], bool):
        return False

    # Check string
    for req in requirements:
        req = string_unify(req)
        if req in attribute:
            return True

    return False


# Helper method
def meet_all_requirement(attributes: list, requirements: list) -> bool:
    if not isinstance(attributes, list) or len(attributes) < len(requirements):
        return False

    for req in requirements:
        req = string_unify(req)
        req_fulfilled = False
        for att in attributes:
            att = string_unify(att)
            if req in att:
                req_fulfilled = True
        if not req_fulfilled:
            return False

    return True


# Helper method
def attributes_to_string(current_attributes):
    if current_attributes is None:
        return ""
    if isinstance(current_attributes, bool) or isinstance(current_attributes, int):
        return str(current_attributes)
    if isinstance(current_attributes, list):
        return ", ".join(current_attributes)
    return current_attributes


Entity: typing.TypeAlias = typing.Union[
    common_models.Node,
    common_models.Edge,
]


class Rule:
    display_name: typing.Optional[str] = None
    short_description: str
    long_description: str = "No long description given."
    attribute_names: typing.List[str] = []
    mitigation_options: typing.List[str] = []
    requirement: str = ""
    req_status: str = "Status missing"

    @classmethod
    def _generate_threat(cls, location: threat.Location) -> typing.List[threat.Threat]:
        return [
            threat.Threat(
                source=(
                    cls.display_name if cls.display_name is not None else cls.__name__
                ),
                source_internal=cls.__name__,
                location=location,
                short_description=cls.short_description,
                long_description=cls.long_description,
                mitigation_options=cls.mitigation_options,
                requirement=cls.requirement,
                req_status=cls.req_status,
            )
        ]

    @classmethod
    def set_status(cls, entity: Entity):
        global _
        _ = settings.lang_out.gettext
        status_list = []
        for attribute_name in cls.attribute_names:
            if attribute_name not in entity.attributes:
                status_list.append(
                    _("Attribute missing: {name}").format(
                        name=attributes_dict.attributes[attribute_name][0]
                    )
                )
            else:
                status_list.append(
                    ("{name} = {curr}").format(
                        name=attributes_dict.attributes[attribute_name][0],
                        curr=attributes_to_string(entity.attributes[attribute_name]),
                    )
                )

        cls.req_status = "\n".join(status_list)

    @classmethod
    @abc.abstractmethod
    def init_texts(cls):
        raise NotImplementedError


class NodeRule(Rule):
    @classmethod
    @abc.abstractmethod
    def _test(
        cls, node: common_models.Node, dfd: dataflowdiagram.DataflowDiagram
    ) -> bool:
        raise NotImplementedError

    @classmethod
    def evaluate(
        cls, node: common_models.Node, dfd: dataflowdiagram.DataflowDiagram
    ) -> typing.List[threat.Threat]:
        if cls._test(node, dfd):
            cls.set_status(node)
            return cls._generate_threat(node)
        else:
            return []


class NodeTagRule(NodeRule):
    node_tags_all = {}
    node_tags_any = {}

    @classmethod
    def _test(
        cls, node: common_models.Node, dfd: dataflowdiagram.DataflowDiagram
    ) -> bool:
        for tag in cls.node_tags_all:
            if tag not in node.tags:
                return False
        else:
            for tag in cls.node_tags_any:
                if tag in node.tags:
                    return True
            return False


class EdgeRule(Rule):
    @classmethod
    @abc.abstractmethod
    def _test(
        cls, edge: common_models.Edge, dfd: dataflowdiagram.DataflowDiagram
    ) -> bool:
        raise NotImplementedError

    @classmethod
    def evaluate(
        cls, edge: common_models.Edge, dfd: dataflowdiagram.DataflowDiagram
    ) -> typing.List[threat.Threat]:
        if cls._test(edge, dfd):
            cls.set_status(edge)
            return cls._generate_threat(edge)
        else:
            return []


class EdgeTagRule(EdgeRule):
    edge_tags_all = {}
    edge_tags_any = {}

    @classmethod
    def _test(
        cls, edge: common_models.Edge, dfd: dataflowdiagram.DataflowDiagram
    ) -> bool:
        for tag in cls.edge_tags_all:
            if tag not in edge.tags:
                return False
        else:
            for tag in cls.edge_tags_any:
                if tag in edge.tags:
                    return True
            return False


class DataflowDiagramRule(Rule):
    @classmethod
    @abc.abstractmethod
    def _test(cls, dfd: dataflowdiagram.DataflowDiagram) -> bool:
        raise NotImplementedError

    @classmethod
    def evaluate(
        cls, dfd: dataflowdiagram.DataflowDiagram
    ) -> typing.List[threat.Threat]:
        if cls._test(dfd):
            raise NotImplementedError  # Status has to be set
            cls.set_status()
            return cls._generate_threat(dfd)
        else:
            return []


class GraphRule(Rule):
    @classmethod
    @abc.abstractmethod
    def _test(cls, graph: nx.DiGraph, dfd: dataflowdiagram.DataflowDiagram) -> bool:
        raise NotImplementedError

    @classmethod
    def evaluate(
        cls, graph: nx.DiGraph, dfd: dataflowdiagram.DataflowDiagram
    ) -> typing.List[threat.Threat]:
        if cls._test(graph, dfd):
            raise NotImplementedError  # Status has to be set
            cls.set_status()
            return cls._generate_threat(dfd)
        else:
            return []


RuleType = typing.TypeVar("RuleType", bound=Rule)
NodeRuleType = typing.TypeVar("NodeRuleType", bound=NodeRule)
EdgeRuleType = typing.TypeVar("EdgeRuleType", bound=EdgeRule)
DataflowDiagramRuleType = typing.TypeVar(
    "DataflowDiagramRuleType", bound=DataflowDiagramRule
)
GraphRuleType = typing.TypeVar("GraphRuleType", bound=GraphRule)


class DataflowDiagramRuleCollection(abc.ABC):
    tags: typing.Set[str] = {}
    name: str = "Rule collection"
    node_rules: typing.List[NodeRuleType] = []
    edge_rules: typing.List[EdgeRuleType] = []
    dfd_rules: typing.List[DataflowDiagramRuleType] = []
    graph_rules: typing.List[GraphRule] = []

    @classmethod
    def evaluate(
        cls, dfd: dataflowdiagram.DataflowDiagram
    ) -> typing.List[threat.Threat]:
        results: typing.List[threat.Threat] = []

        for tag in cls.tags:
            if tag not in dfd.tags:
                return results

        # Evaluate node rules
        for node_rule in cls.node_rules:
            for _, node in dfd.nodes.items():
                rule_results = node_rule.evaluate(node, dfd)
                results += rule_results

        # Evaluate edge rules
        for edge_rule in cls.edge_rules:
            for _, edge in dfd.edges.items():
                rule_results = edge_rule.evaluate(edge, dfd)
                results += rule_results

        # Evaluate dfd rules
        for dfd_rule in cls.dfd_rules:
            rule_results = dfd_rule.evaluate(dfd)
            results += rule_results

        # Evaluate graph rules
        if len(cls.graph_rules) > 0:
            graph = nx.DiGraph()

            for node_id, node in dfd.nodes.items():
                graph.add_node(node_id, node_data=node)

            for _, edge in dfd.edges.items():
                graph.add_edge(edge.source_id, edge.sink_id, edge_data=edge)

            for graph_rule in cls.graph_rules:
                rule_results = graph_rule.evaluate(graph, dfd)
                results += rule_results

        return results


__all__ = [
    "NodeRule",
    "NodeTagRule",
    "EdgeRule",
    "EdgeTagRule",
    "DataflowDiagramRule",
    "GraphRule",
    "DataflowDiagramRuleCollection",
]

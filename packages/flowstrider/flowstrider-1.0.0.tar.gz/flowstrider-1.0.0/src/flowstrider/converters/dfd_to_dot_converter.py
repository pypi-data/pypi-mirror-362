# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import sys
from datetime import datetime

from graphviz import Source

from flowstrider import settings
from flowstrider.models import common_models, dataflowdiagram


def wrap_text(
    text_to_wrap: str, max_line_char_length: int = settings.CMD_MAX_CHAR_WIDTH
) -> str:
    """Inserts line breaks in the given string to fit the given maximum character
    length per line

    Args:
        text_to_wrap: the text that is being wrapped
        max_line_char_length: number of characters that will be allowed in one line
    Returns:
        wrapped version of the input text up to the maximum char length per line as a
         string with line breaks (\n)
    """
    if len(text_to_wrap) == 0:
        return ""
    text_words = text_to_wrap.split(" ")
    text_wrapped = ""

    while len(text_words) > 0:
        # Wrap single words that are too long
        if len(text_words[0]) > max_line_char_length:
            text_wrapped += text_words[0][: max_line_char_length - 1] + "-\n"
            text_words[0] = text_words[0][max_line_char_length - 1 :]
            continue
        # Wrap words that are not too long
        else:
            curr_line_char_length = len(text_words[0])
            text_wrapped += text_words.pop(0)
            # Terminate if whole text is wrapped
            if len(text_words) == 0:
                break

        # Prepare for more words (extra '1' is for the space char between words)
        curr_line_char_length += 1 + len(text_words[0])

        # Add more words too current line until max is reached or no words are left
        while curr_line_char_length <= max_line_char_length:
            text_wrapped += " " + text_words.pop(0)
            if len(text_words) == 0:
                break
            curr_line_char_length += 1 + len(text_words[0])

        text_wrapped += "\n"

    # Remove last \n and return
    if text_wrapped[-1] == "\n":
        return text_wrapped[:-1]
    else:
        return text_wrapped


def render_dfd(dfd: dataflowdiagram.DataflowDiagram):
    """Renders a given dataflow diagram as a PNG file (or SVG)

    Args:
        dfd: the dataflowdiagram to be rendered

    """
    dot_format = deserialized_dfd_to_dot(dfd)

    output_file = "output/visualization/visualization"

    source = Source(dot_format)
    source.save(output_file + ".dot")

    os.makedirs("output/visualization", exist_ok=True)

    with open("output/warnings_log.txt", "w") as log_file:
        log_file.write(
            "Log for {id} from {time}.\n\n".format(id=dfd.id, time=datetime.now())
        )
        log_file.write("Graphviz warnings:\n")

        temp_stderr = sys.stderr
        sys.stderr = log_file

        source.render(
            output_file, format="png", cleanup=True
        )  # PNG can be added to pdf report (does not include metadata)
        source.render(
            output_file, format="svg", cleanup=True
        )  # SVG can be opened in browser to view metadata tooltips

        sys.stderr = temp_stderr


def deserialized_dfd_to_dot(dfd: dataflowdiagram.DataflowDiagram) -> str:
    """takes dfd object as input and creates a dot representation (as string)
        which can be rendered as PNG file

    Args:
        dfd: the dataflow diagram to be converted to dot format
    Returns:
        the dot representation of the dfd as a string

    """
    dfd_as_dot = 'digraph "' + dfd.id.replace(" ", "_") + '" {\n'

    # represent relationships between (nested) clusters (parent: list of children)
    # this is necessary because graphviz does not automatically show nested structures
    # adding a node twice as part of two different clusters does not work. it would be
    # ignored by the second cluster
    relationships = {cluster.id: [] for cluster in dfd.clusters.values()}

    for parent_key, parent_cluster in dfd.clusters.items():
        for child_key, child_cluster in dfd.clusters.items():
            if parent_key != child_key and set(child_cluster.node_ids).issubset(
                parent_cluster.node_ids
            ):
                relationships[parent_key].append(child_key)

    # Find the root clusters (not child of any other cluster)
    all_subclusters = {sub_id for subs in relationships.values() for sub_id in subs}
    root_clusters = [
        cluster_id for cluster_id in relationships if cluster_id not in all_subclusters
    ]

    # track all nodes that have been added already as part of a cluster
    nodes_in_clusters = set()

    # add root clusters to dot representation
    # cluster_to_dot recursively add child clusters
    for root_cluster_id in root_clusters:
        cluster = dfd.clusters[root_cluster_id]
        dfd_as_dot += cluster_to_dot(cluster, dfd, relationships)
        nodes_in_clusters.update(cluster.node_ids)

    # in case of nodes that do not belong to any cluster
    for node_key in dfd.nodes:
        node = dfd.nodes[node_key]
        if node.id not in nodes_in_clusters:
            dfd_as_dot += node_to_dot(node) + "\n"

    # add edges to dot representation
    for edge_key in dfd.edges:
        edge = dfd.edges[edge_key]
        dfd_as_dot += dataflow_to_dot(edge) + "\n"

    dfd_as_dot += "}"

    return dfd_as_dot


def cluster_to_dot(
    cluster: common_models.Cluster,
    dfd: dataflowdiagram.DataflowDiagram,
    relationships: dict,
) -> str:
    """takes a cluster object and generates dot string. recursively includes
        nested clusters

    Args:
        cluster: the cluster to be converted to dot
        dfd: the dataflow diagram to which the cluster belongs
            (needed to get node and child cluster objects)
        relationships: possible child clusters to be added recursively
    Returns:
        the dot representation of the cluster(s) as a string

    """

    cluster_id_underscores = cluster.id.replace(" ", "_").replace("-", "_")
    cluster_as_dot = f"    subgraph cluster_{cluster_id_underscores} {{\n"
    cluster_label = cluster.name if cluster.name != "" else cluster.id
    cluster_as_dot += f"        label=< <B>{cluster_label}</B> >;\n"
    # tooltip only relevant if rendered as svg file
    cluster_as_dot += f'        tooltip="{format_attributes(cluster.attributes)}";\n'
    cluster_as_dot += "        style=dashed;\n"

    # add nodes in cluster
    node_ids_sorted = sorted(cluster.node_ids)
    for node_id in node_ids_sorted:
        node = dfd.get_node_by_id(node_id)
        cluster_as_dot += node_to_dot(node) + "\n"

    # Recursively add subclusters
    for subcluster_id in relationships[cluster.id]:
        subcluster = dfd.clusters[subcluster_id]
        cluster_as_dot += cluster_to_dot(subcluster, dfd, relationships)

    cluster_as_dot += "    }\n"
    return cluster_as_dot


def node_to_dot(node: common_models.Node) -> str:
    """takes a node object and generates dot string

    Args:
        node: the node to be converted to dot
    Returns:
        the dot representation of the node as a string

    """
    label = node.name if node.name != "" else node.id
    label_formatted = wrap_text(label, 20)

    node_as_dot = f'        "{node.id}" [label="{label_formatted}"'
    # Tooltip only relevant if rendered as svg file
    node_as_dot += f', tooltip="{format_attributes(node.attributes)}"'
    node_as_dot += ", fixedsize=true"
    node_as_dot += ", width=2.5"
    node_as_dot += ", height=1.0"

    node_as_dot += ", shape="
    if "STRIDE:Interactor" in node.tags:
        node_as_dot += "box, style=filled"
    elif "STRIDE:DataStore" in node.tags:
        node_as_dot += "cylinder"
    elif "STRIDE:Process" in node.tags:
        node_as_dot += "circle"

    node_as_dot += "]"

    return node_as_dot


def dataflow_to_dot(edge: common_models.Edge) -> str:
    """takes an edge object and generates dot string

    Args:
        edge: the edge to be converted to dot
    Returns:
        the dot representation of the edge as a string

    """
    label = edge.name if edge.name != "" else edge.id
    label_formatted = wrap_text(label, 15)

    edge_as_dot = f'    "{edge.source_id}" -> "{edge.sink_id}" '
    edge_as_dot += f'[label="{label_formatted}"'
    # tooltip only relevant if rendered as svg file
    edge_as_dot += f', tooltip="{format_attributes(edge.attributes)}"];'
    return edge_as_dot


def format_attributes(attributes: dict) -> str:
    """takes metadata of an entity and formats it in a more human-readable format
        (helpful for the SVG representation where a metadata tooltip can be added)

    Args:
        attributes: the metadata dictionary of an entity (node, edge, cluster)
    Returns:
        the formatted attributes to be added to the dot string of the entity

    """
    if not attributes:
        return "No metadata listed"

    attributes_as_string = ""

    for key, value in attributes.items():
        attributes_as_string += f"{key}: {value} \n"

    return attributes_as_string

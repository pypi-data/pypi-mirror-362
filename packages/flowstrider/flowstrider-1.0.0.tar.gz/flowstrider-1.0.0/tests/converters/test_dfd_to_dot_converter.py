# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

from unittest.mock import MagicMock, patch

from flowstrider.converters import dfd_to_dot_converter
from flowstrider.models.common_models import Cluster, Edge, Node
from flowstrider.models.dataflowdiagram import DataflowDiagram

__author__ = "Sara Brianna Lehmann"


def test_deserialized_dfd_to_dot():
    cluster1 = Cluster(id="cluster1", name="Cluster 1", node_ids=["node1", "node2"])
    cluster2 = Cluster(id="cluster2", name="Cluster 2", node_ids=["node3"])

    node1 = Node(id="node1", name="Node 1", attributes={}, tags=["STRIDE:Interactor"])
    node2 = Node(id="node2", name="Node 2", attributes={}, tags=["STRIDE:Process"])
    node3 = Node(id="node3", name="Node 3", attributes={}, tags=["STRIDE:DataStore"])

    edge = Edge(
        id="edge1", source_id="node1", sink_id="node2", name="Edge 1", attributes={}
    )

    dfd = DataflowDiagram(
        id="test_dfd",
        clusters={"cluster1": cluster1, "cluster2": cluster2},
        nodes={"node1": node1, "node2": node2, "node3": node3},
        edges={"edge1": edge},
    )

    result = dfd_to_dot_converter.deserialized_dfd_to_dot(dfd)
    expected_substring = (
        'digraph "test_dfd" {\n'
        "    subgraph cluster_cluster1 {\n"
        "        label=< <B>Cluster 1</B> >;\n"
        '        tooltip="No metadata listed";\n'
        "        style=dashed;\n"
        '        "node1" [label="Node 1", tooltip="No metadata listed", '
        "fixedsize=true, width=2.5, height=1.0, shape=box, style=filled]\n"
        '        "node2" [label="Node 2", tooltip="No metadata listed", '
        "fixedsize=true, width=2.5, height=1.0, shape=circle]\n"
        "    }\n"
        "    subgraph cluster_cluster2 {\n"
        "        label=< <B>Cluster 2</B> >;\n"
        '        tooltip="No metadata listed";\n'
        "        style=dashed;\n"
        '        "node3" [label="Node 3", tooltip="No metadata listed", '
        "fixedsize=true, width=2.5, height=1.0, shape=cylinder]\n"
        "    }\n"
        '    "node1" -> "node2" [label="Edge 1", tooltip="No metadata listed"];\n'
        "}"
    )
    assert expected_substring in result


def test_deserialized_dfd_to_dot_special_chars():
    # Test with special characters in names and ids
    cluster1 = Cluster(id="cluster 1", name="Cluster 1", node_ids=["node 1", "node_2"])
    cluster2 = Cluster(id="cluster-2", name="Cluster-2", node_ids=['node"3"'])

    node1 = Node(id="node 1", name="Node 1", attributes={}, tags=["STRIDE:Interactor"])
    node2 = Node(id="node_2", name="Node_2", attributes={}, tags=["STRIDE:Process"])
    node3 = Node(
        id='node"3"', name='Node "3"', attributes={}, tags=["STRIDE:DataStore"]
    )

    edge = Edge(
        id="edge 1", source_id="node 1", sink_id="node_2", name="Edge 1", attributes={}
    )

    dfd = DataflowDiagram(
        id="test_dfd",
        clusters={"cluster 1": cluster1, "cluster-2": cluster2},
        nodes={"node 1": node1, "node_2": node2, 'node"3"': node3},
        edges={"edge 1": edge},
    )

    result = dfd_to_dot_converter.deserialized_dfd_to_dot(dfd)
    expected_substring = (
        'digraph "test_dfd" {\n'
        "    subgraph cluster_cluster_1 {\n"
        "        label=< <B>Cluster 1</B> >;\n"
        '        tooltip="No metadata listed";\n'
        "        style=dashed;\n"
        '        "node 1" [label="Node 1", tooltip="No metadata listed", '
        "fixedsize=true, width=2.5, height=1.0, shape=box, style=filled]\n"
        '        "node_2" [label="Node_2", tooltip="No metadata listed", '
        "fixedsize=true, width=2.5, height=1.0, shape=circle]\n"
        "    }\n"
        "    subgraph cluster_cluster_2 {\n"
        "        label=< <B>Cluster-2</B> >;\n"
        '        tooltip="No metadata listed";\n'
        "        style=dashed;\n"
        '        "node"3"" [label="Node "3"", tooltip="No metadata listed", '
        "fixedsize=true, width=2.5, height=1.0, shape=cylinder]\n"
        "    }\n"
        '    "node 1" -> "node_2" [label="Edge 1", tooltip="No metadata listed"];\n'
        "}"
    )
    assert expected_substring in result


@patch("flowstrider.converters.dfd_to_dot_converter.Source")
def test_render_dfd(mock_source):
    mock_dfd = MagicMock()
    mock_dfd.id = "test_dfd"

    with patch(
        "flowstrider.converters.dfd_to_dot_converter.deserialized_dfd_to_dot",
        return_value="digraph test_dfd { }",
    ) as mock_to_dot:
        dfd_to_dot_converter.render_dfd(mock_dfd)

        # Assert deserialized_dfd_to_dot was called
        mock_to_dot.assert_called_once_with(mock_dfd)

        # Assert Source was instantiated with the expected DOT string
        mock_source.assert_called_once_with("digraph test_dfd { }")

        # Assert render was called with correct arguments
        mock_source.return_value.render.assert_any_call(
            "output/visualization/visualization", format="png", cleanup=True
        )
        mock_source.return_value.render.assert_any_call(
            "output/visualization/visualization", format="svg", cleanup=True
        )


def test_wrap_text():
    assert dfd_to_dot_converter.wrap_text("Test string", 20) == "Test string"

    assert (
        dfd_to_dot_converter.wrap_text("This is a fabulous test string", 20)
        == "This is a fabulous\ntest string"
    )

    assert (
        dfd_to_dot_converter.wrap_text(
            "This is an extremely fabulous and very exquisit test string", 20
        )
        == "This is an extremely\nfabulous and very\nexquisit test string"
    )

    assert (
        dfd_to_dot_converter.wrap_text(
            "This is an extremely fabulous and very exquisit test string", 30
        )
        == "This is an extremely fabulous\nand very exquisit test string"
    )

    assert (
        dfd_to_dot_converter.wrap_text(
            "This is an extremely fabulous and very exquisit test string", 10
        )
        == "This is an\nextremely\nfabulous\nand very\nexquisit\ntest\nstring"
    )

    assert (
        dfd_to_dot_converter.wrap_text(
            "Thisteststringhasnospacesbutshouldstillbewrapped", 20
        )
        == "Thisteststringhasno-\nspacesbutshouldstil-\nlbewrapped"
    )

    assert (
        dfd_to_dot_converter.wrap_text(
            "Thisteststringhaspartiallynospaces but should stillbewrappedloremipsumdol"
            + "or",
            20,
        )
        == "Thisteststringhaspa-\nrtiallynospaces but\nshould\nstillbewrappedlorem-\ni"
        + "psumdolor"
    )

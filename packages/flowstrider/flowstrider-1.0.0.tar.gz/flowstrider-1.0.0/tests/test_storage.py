# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import pytest

from flowstrider.converters.dfd_to_dot_converter import wrap_text as wrap
from flowstrider.storage import deserialize_dfd


@pytest.fixture
def dfd_blueprint():
    serialized_dfd_plain = """
    {
    "dfd": {
        "id": "{id_1}",
        "nodes": {
        "node1": {
            "id": "{id_2}",
            "name": "User",
            "tags": [
            "STRIDE:Interactor"
            ],
            "attributes": {}
        },
        "node2": {
            "id": "{id_3}",
            "name": "Application",
            "tags": [
            "STRIDE:Process"
            ],
            "attributes": {}
        }
        },
        "edges": {
        "edge1": {
            "id": "{id_4}",
            "source_id": "{id_ref_2}",
            "sink_id": "{id_ref_3}",
            "name": "Connection",
            "tags": [
            "STRIDE:Dataflow"
            ],
            "attributes": {}
        }
        },
        "clusters": {
        "cluster1":{
            "id": "{id_5}",
            "node_ids": [
                "{id_ref2_3}"
            ],
            "name": "Internet",
            "tags": [
            "STRIDE:TrustBoundary"
            ],
            "attributes": {}
        }
        },
        "name": "",
        "tags": [
        "bsi_rules"
        ],
        "attributes": {}
    }
    }
    """
    return serialized_dfd_plain[serialized_dfd_plain.find("\n") + 1 :]


@pytest.fixture
def dfd_blueprint_2():
    serialized_dfd_plain = """
    {
    "dfd": {
        "id": "diagram",
        "nodes": {
            "{name_2}": {
                "id": "{id_2}",
                "name": "User",
                "tags": [
                "STRIDE:Interactor"
                ],
                "attributes": {}
            },
            "{name_3}": {
                "id": "{id_3}",
                "name": "Application",
                "tags": [
                "STRIDE:Process"
                ],
                "attributes": {}
            }
            },
        "edges": {
            "{name_4}": {
                "id": "{id_4}",
                "source_id": "{id_2}",
                "sink_id": "{id_3}",
                "name": "Connection",
                "tags": [
                "STRIDE:Dataflow"
                ],
                "attributes": {}
            }
        },
        "clusters": {
            "{name_5}":{
                "id": "{id_5}",
                "node_ids": [
                    "{id_3}"
                ],
                "name": "Internet",
                "tags": [
                "STRIDE:TrustBoundary"
                ],
                "attributes": {}
            }
        },
        "name": "",
        "tags": [
        "bsi_rules"
        ],
        "attributes": {}
    }
    }
    """
    return serialized_dfd_plain[serialized_dfd_plain.find("\n") + 1 :]


@pytest.fixture
def dfd_blueprint_3():
    serialized_dfd_plain = """
    {
    "dfd": {
        "id": "diagram",
        "nodes": {
            "id_2": {
                "id": "id_2",
                "name": "User",
                "tags": ["{tag_1}"],
                "attributes": {}
            },
            "id_3": {
                "id": "id_3",
                "name": "Application",
                "tags": [
                "{tag_2}",
                "{tag_2_2}"
                ],
                "attributes": {}
            }
            },
        "edges": {
            "id_4": {
                "id": "id_4",
                "source_id": "id_2",
                "sink_id": "id_3",
                "name": "Connection",
                "tags": ["{tag_3}"],
                "attributes": {}
            }
        },
        "clusters": {
            "id_5":{
                "id": "id_5",
                "node_ids": ["id_3"],
                "name": "Internet",
                "tags": ["{tag_4}"],
                "attributes": {}
            }
        },
        "name": "",
        "tags": ["{tag_5}"],
        "attributes": {}
    }
    }
    """
    return serialized_dfd_plain[serialized_dfd_plain.find("\n") + 1 :]


@pytest.fixture
def dfd_blueprint_4():
    serialized_dfd_plain = """
    {
    "dfd": {
        "id": "id_1",
        "nodes": {
        "node1": {
            "id": "node1",
            "name": "User",
            "tags": [
            "STRIDE:Interactor"
            ],
            "attributes": {att_node_1}
        },
        "node2": {
            "id": "node2",
            "name": "Application",
            "tags": [
            "STRIDE:Process"
            ],
            "attributes": {att_node_2}
        }
        },
        "edges": {
        "edge1": {
            "id": "edge1",
            "source_id": "node1",
            "sink_id": "node2",
            "name": "Connection",
            "tags": [
            "STRIDE:Dataflow"
            ],
            "attributes": {att_edge_1}
        }
        },
        "clusters": {
        "cluster1":{
            "id": "cluster1",
            "node_ids": [
                "node2"
            ],
            "name": "Internet",
            "tags": [
            "STRIDE:TrustBoundary"
            ],
            "attributes": {}
        }
        },
        "name": "",
        "tags": [
        "bsi_rules"
        ],
        "attributes": {}
    }
    }
    """
    return serialized_dfd_plain[serialized_dfd_plain.find("\n") + 1 :]


def test_deserialize_dfd_correct(
    capsys, dfd_blueprint, dfd_blueprint_2, dfd_blueprint_3
):
    # str.format() didn't work so I had to use str.replace()
    serialized_dfd_correct = (
        dfd_blueprint.replace("{id_1}", "diagram")
        .replace("{id_2}", "node1")
        .replace("{id_ref_2}", "node1")
        .replace("{id_3}", "node2")
        .replace("{id_ref_3}", "node2")
        .replace("{id_ref2_3}", "node2")
        .replace("{id_4}", "edge1")
        .replace("{id_5}", "cluster1")
    )
    dfd = deserialize_dfd(serialized_dfd_correct)
    assert dfd.id == "diagram"
    assert len(dfd.nodes) == 2
    assert len(dfd.edges) == 1
    assert len(dfd.clusters) == 1
    captured = capsys.readouterr()
    assert "Warning: " not in captured.out
    assert "Error: " not in captured.out

    serialized_dfd_correct_2 = (
        dfd_blueprint_2.replace("{name_2}", "node1")
        .replace("{id_2}", "node1")
        .replace("{name_3}", "node2")
        .replace("{id_3}", "node2")
        .replace("{name_4}", "edge1")
        .replace("{id_4}", "edge1")
        .replace("{name_5}", "cluster1")
        .replace("{id_5}", "cluster1")
    )
    dfd = deserialize_dfd(serialized_dfd_correct_2)
    assert len(dfd.nodes) == 2
    assert len(dfd.edges) == 1
    assert len(dfd.clusters) == 1
    captured = capsys.readouterr()
    assert "Warning: " not in captured.out
    assert "Error: " not in captured.out

    # Modify dfd_correct_2 so that node ids are in one line and not beneath each other
    serialized_dfd_correct_2_2 = serialized_dfd_correct_2
    node_ids_index = serialized_dfd_correct_2_2.find('"node_ids":')
    start_index = node_ids_index + serialized_dfd_correct_2_2[node_ids_index:].find("[")
    end_index = node_ids_index + serialized_dfd_correct_2_2[node_ids_index:].find("]")
    serialized_dfd_correct_2_2 = (
        serialized_dfd_correct_2_2[:start_index]
        + '["node1", "node2"]'
        + serialized_dfd_correct_2_2[end_index + 1 :]
    )
    dfd = deserialize_dfd(serialized_dfd_correct_2_2)
    assert len(dfd.nodes) == 2
    assert len(dfd.edges) == 1
    assert len(dfd.clusters) == 1
    captured = capsys.readouterr()
    assert "Warning: " not in captured.out
    assert "Error: " not in captured.out

    serialized_dfd_correct_3 = (
        dfd_blueprint_3.replace("{tag_1}", "STRIDE:Interactor")
        .replace("{tag_2}", "STRIDE:Interactor")
        .replace("{tag_2_2}", "STRIDE:Process")
        .replace("{tag_3}", "STRIDE:Dataflow")
        .replace("{tag_4}", "STRIDE:TrustBoundary")
        .replace("{tag_5}", "bsi_rules")
    )
    dfd = deserialize_dfd(serialized_dfd_correct_3)
    assert len(dfd.nodes) == 2
    assert len(dfd.edges) == 1
    assert len(dfd.clusters) == 1
    captured = capsys.readouterr()
    assert "Warning: " not in captured.out
    assert "Error: " not in captured.out


def test_deserialize_dfd_id_reuse(capsys, dfd_blueprint):
    serialized_dfd_fail_1 = (
        dfd_blueprint.replace("{id_1}", "diagram")
        .replace("{id_2}", "diagram")
        .replace("{id_ref_2}", "diagram")
        .replace("{id_3}", "node2")
        .replace("{id_ref_3}", "node2")
        .replace("{id_ref2_3}", "node2")
        .replace("{id_4}", "edge1")
        .replace("{id_5}", "cluster1")
    )
    deserialize_dfd(serialized_dfd_fail_1)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: id "diagram" was used for more than one object in the dfd. '
            + "(JSON line 6)"
        )
        in captured.out
    )

    serialized_dfd_fail_2 = (
        dfd_blueprint.replace("{id_1}", "diagram")
        .replace("{id_2}", "node1")
        .replace("{id_ref_2}", "node1")
        .replace("{id_3}", "node1")
        .replace("{id_ref_3}", "node1")
        .replace("{id_ref2_3}", "node1")
        .replace("{id_4}", "edge1")
        .replace("{id_5}", "cluster1")
    )
    deserialize_dfd(serialized_dfd_fail_2)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: id "node1" was used for more than one object in the dfd.'
            + " (JSON line 14)"
        )
        in captured.out
    )

    serialized_dfd_fail_3 = (
        dfd_blueprint.replace("{id_1}", "diagram")
        .replace("{id_2}", "node1")
        .replace("{id_ref_2}", "node1")
        .replace("{id_3}", "node2")
        .replace("{id_ref_3}", "node2")
        .replace("{id_ref2_3}", "node2")
        .replace("{id_4}", "node1")
        .replace("{id_5}", "cluster1")
    )
    deserialize_dfd(serialized_dfd_fail_3)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: id "node1" was used for more than one object in the dfd.'
            + " (JSON line 24)"
        )
        in captured.out
    )

    serialized_dfd_fail_4 = (
        dfd_blueprint.replace("{id_1}", "diagram")
        .replace("{id_2}", "node1")
        .replace("{id_ref_2}", "node1")
        .replace("{id_3}", "node2")
        .replace("{id_ref_3}", "node2")
        .replace("{id_ref2_3}", "node2")
        .replace("{id_4}", "edge1")
        .replace("{id_5}", "edge1")
    )
    deserialize_dfd(serialized_dfd_fail_4)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: id "edge1" was used for more than one object in the dfd.'
            + " (JSON line 36)"
        )
        in captured.out
    )

    serialized_dfd_fail_4 = (
        dfd_blueprint.replace("{id_1}", "diagram")
        .replace("{id_2}", "AEIOU")
        .replace("{id_ref_2}", "AEIOU")
        .replace("{id_3}", "AEIOU")
        .replace("{id_ref_3}", "AEIOU")
        .replace("{id_ref2_3}", "AEIOU")
        .replace("{id_4}", "edge1")
        .replace("{id_5}", "AEIOU")
    )
    deserialize_dfd(serialized_dfd_fail_4)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: id "AEIOU" was used for more than one object in the dfd.'
            + " (JSON line 14)"
        )
        in captured.out
    )
    assert (
        wrap(
            'Warning: id "AEIOU" was used for more than one object in the dfd.'
            + " (JSON line 36)"
        )
        in captured.out
    )


def test_deserialize_dfd_id_missing(capsys, dfd_blueprint):
    serialized_dfd_fail_1 = (
        dfd_blueprint.replace("{id_1}", "diagram")
        .replace("{id_2}", "node1")
        .replace("{id_ref_2}", "node3")
        .replace("{id_3}", "node2")
        .replace("{id_ref_3}", "node2")
        .replace("{id_ref2_3}", "node2")
        .replace("{id_4}", "edge1")
        .replace("{id_5}", "cluster")
    )
    deserialize_dfd(serialized_dfd_fail_1)
    captured = capsys.readouterr()
    assert (
        wrap('Warning: id "node3" was referenced but not found. (JSON line 25)')
        in captured.out
    )

    serialized_dfd_fail_2 = (
        dfd_blueprint.replace("{id_1}", "diagram")
        .replace("{id_2}", "node1")
        .replace("{id_ref_2}", "node1")
        .replace("{id_3}", "node2")
        .replace("{id_ref_3}", "node2")
        .replace("{id_ref2_3}", "node3")
        .replace("{id_4}", "edge1")
        .replace("{id_5}", "cluster")
    )
    deserialize_dfd(serialized_dfd_fail_2)
    captured = capsys.readouterr()
    assert (
        wrap('Warning: id "node3" was referenced but not found. (JSON line 38)')
        in captured.out
    )


def test_deserialize_dfd_id_name_missmatch(capsys, dfd_blueprint_2):
    serialized_dfd_fail_1 = (
        dfd_blueprint_2.replace("{name_2}", "node1")
        .replace("{id_2}", "node_1")
        .replace("{name_3}", "node2")
        .replace("{id_3}", "node2")
        .replace("{name_4}", "edge1")
        .replace("{id_4}", "edge1")
        .replace("{name_5}", "cluster")
        .replace("{id_5}", "cluster")
    )
    deserialize_dfd(serialized_dfd_fail_1)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: element name "node1" does not correspond with its id "node_1".'
            + " (JSON line 5)"
        )
        in captured.out
    )

    serialized_dfd_fail_2 = (
        dfd_blueprint_2.replace("{name_2}", "node1")
        .replace("{id_2}", "node1")
        .replace("{name_3}", "node2abc")
        .replace("{id_3}", "node2")
        .replace("{name_4}", "edge1")
        .replace("{id_4}", "edge1")
        .replace("{name_5}", "cluster")
        .replace("{id_5}", "cluster")
    )
    deserialize_dfd(serialized_dfd_fail_2)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: element name "node2abc" does not correspond with its id "node2".'
            + " (JSON line 13)"
        )
        in captured.out
    )

    serialized_dfd_fail_3 = (
        dfd_blueprint_2.replace("{name_2}", "node1")
        .replace("{id_2}", "node1")
        .replace("{name_3}", "node2")
        .replace("{id_3}", "node2")
        .replace("{name_4}", "edgeNr1")
        .replace("{id_4}", "edge1")
        .replace("{name_5}", "cluster")
        .replace("{id_5}", "cluster")
    )
    deserialize_dfd(serialized_dfd_fail_3)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: element name "edgeNr1" does not correspond with its id "edge1".'
            + " (JSON line 23)"
        )
        in captured.out
    )

    serialized_dfd_fail_4 = (
        dfd_blueprint_2.replace("{name_2}", "node1")
        .replace("{id_2}", "node1")
        .replace("{name_3}", "node2")
        .replace("{id_3}", "node2")
        .replace("{name_4}", "edge1")
        .replace("{id_4}", "edge1")
        .replace("{name_5}", "cluster")
        .replace("{id_5}", "cluuuster")
    )
    deserialize_dfd(serialized_dfd_fail_4)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: element name "cluster" does not correspond with its id '
            + '"cluuuster". (JSON line 35)'
        )
        in captured.out
    )


def test_deserialize_dfd_false_tags(capsys, dfd_blueprint_3):
    serialized_dfd_fail_1 = (
        dfd_blueprint_3.replace("{tag_1}", "STRIDE:Interactor")
        .replace("{tag_2}", "STRIDE:Interactor")
        .replace("{tag_2_2}", "STRIDE:Processs")
        .replace("{tag_3}", "STRIDE:Dataflow")
        .replace("{tag_4}", "STRIDE:TrustBoundary")
        .replace("{tag_5}", "bsi_rules")
    )
    deserialize_dfd(serialized_dfd_fail_1)
    captured = capsys.readouterr()
    assert (
        wrap('Warning: tag "STRIDE:Processs" is not a valid tag. (JSON line 16)')
        in captured.out
    )

    serialized_dfd_fail_2 = (
        dfd_blueprint_3.replace("{tag_1}", "STRIDE:Interactor")
        .replace("{tag_2}", "STRIDE:Interactor")
        .replace("{tag_2_2}", "STRIDE:Process")
        .replace("{tag_3}", "STRIDE:Dataflow")
        .replace("{tag_4}", "STRIDE:TrustBoundary")
        .replace("{tag_5}", "no_rules_embrace_anarchy")
    )
    deserialize_dfd(serialized_dfd_fail_2)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: tag "no_rules_embrace_anarchy" is not a valid tag. (JSON line 41)'
        )
        in captured.out
    )

    serialized_dfd_fail_3 = (
        dfd_blueprint_3.replace("{tag_1}", "STRIDE:Interactor")
        .replace("{tag_2}", "STRIDE:Interactor")
        .replace("{tag_2_2}", "STRIDE:Process")
        .replace("{tag_3}", "STRIDE:Dataflow")
        .replace("{tag_4}", "TrustBoundary")
        .replace("{tag_5}", "stride")
    )
    deserialize_dfd(serialized_dfd_fail_3)
    captured = capsys.readouterr()
    assert (
        wrap('Warning: tag "TrustBoundary" is not a valid tag. (JSON line 36)')
        in captured.out
    )


def test_deserialize_dfd_false_attributes(capsys, dfd_blueprint_4):
    serialized_dfd_fail_1 = (
        dfd_blueprint_4.replace("{att_node_1}", '{"given_permissions": "Read"}')
        .replace("{att_node_2}", '{"auth_factors": "Chip Card", "auth_req": false}')
        .replace(
            "{att_edge_1}",
            '{"handles_confidential_data": true, "integrity_check": "ECDSA"}',
        )
    )
    deserialize_dfd(serialized_dfd_fail_1)
    captured = capsys.readouterr()
    assert "Warning: " not in captured.out
    assert "Error: " not in captured.out

    serialized_dfd_fail_4 = (
        dfd_blueprint_4.replace("{att_node_1}", '{"handles_confidential_data": true}')
        .replace("{att_node_2}", "{}")
        .replace("{att_edge_1}", "{}")
    )
    deserialize_dfd(serialized_dfd_fail_4)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: attribute "handles_confidential_data" is not applicable for an '
            + "element of type STRIDE:Interactor. (JSON line 11)"
        )
        in captured.out
    )

    serialized_dfd_fail_5 = (
        dfd_blueprint_4.replace("{att_node_1}", '{"kauderwelsch": "irgendwas"}')
        .replace("{att_node_2}", "{}")
        .replace("{att_edge_1}", "{}")
    )
    deserialize_dfd(serialized_dfd_fail_5)
    captured = capsys.readouterr()
    assert (
        wrap(
            'Warning: attribute "kauderwelsch" is not a valid attribute. (JSON line 11)'
        )
        in captured.out
    )

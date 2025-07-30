# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

from flowstrider.rules import attributes_dict

accepted_types = [
    "Node: Interactor",
    "Node: DataStore",
    "Node: Process",
    "Edge: Dataflow",
    "Trust Boundary",
]


def test_attributes_correct_types():
    for key, value in attributes_dict.attributes.items():
        for type in value[2]:
            assert type in accepted_types

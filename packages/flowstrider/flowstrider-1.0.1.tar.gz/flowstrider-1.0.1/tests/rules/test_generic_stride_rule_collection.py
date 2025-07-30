# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import unittest

from flowstrider import settings
from flowstrider.models.common_models import Edge, Node
from flowstrider.models.dataflowdiagram import DataflowDiagram
from flowstrider.rules import elicit


class TestHelpers(unittest.TestCase):
    def setUp(self):
        pass

    # Initialize Localization
    settings.init_localization("en", "sys")
    settings.init_localization("en", "out")


class TestStrideRules(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(id="n1", name="ProcessA", tags=["STRIDE:Interactor"])
        self.node2 = Node(id="n2", name="ProcessB", tags=["STRIDE:DataStore"])
        self.node3 = Node(id="n3", name="ProcessC", tags=["STRIDE:Process"])

        # Edge that crosses boundary without TLS (should trigger rule)
        self.edge1 = Edge(
            id="e1",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            tags=["STRIDE:Dataflow"],
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={"n1": self.node1, "n2": self.node2, "n3": self.node3},
            edges={"edge1": self.edge1},
            clusters={},
            tags="stride",
        )

    def test_stride_rules(self):
        has_spoofing_node_threat = False
        has_tampering_node_threat = False
        has_tampering_data_flow_threat = False
        has_repudiation_node_threat = False
        has_information_disclosure_node_threat = False
        has_information_disclosure_data_flow_threat = False
        has_denial_of_service_node_threat = False
        has_denial_of_service_data_flow_threat = False
        has_elevation_of_privilege_node_threat = False

        threats = elicit(self.dfd)
        for threat in threats:
            print(threat.source)
            match threat.source:
                case "Generic Spoofing Node Rule":
                    if threat.location_str(self.dfd) == "ProcessA":
                        has_spoofing_node_threat = True

                case "Generic Tampering Node Rule":
                    if threat.location_str(self.dfd) == "ProcessB":
                        has_tampering_node_threat = True

                case "Generic Tampering Dataflow Rule":
                    print("Yes: " + threat.location_str(self.dfd))
                    if threat.location_str(self.dfd) == "e1: ProcessA -> ProcessB":
                        has_tampering_data_flow_threat = True

                case "Generic Repudiation Node Rule":
                    if threat.location_str(self.dfd) == "ProcessC":
                        has_repudiation_node_threat = True

                case "Generic Information Disclosure Node Rule":
                    if threat.location_str(self.dfd) == "ProcessB":
                        has_information_disclosure_node_threat = True

                case "Generic Information Disclosure Dataflow Rule":
                    if threat.location_str(self.dfd) == "e1: ProcessA -> ProcessB":
                        has_information_disclosure_data_flow_threat = True

                case "Generic Denial of Service Node Rule":
                    if threat.location_str(self.dfd) == "ProcessC":
                        has_denial_of_service_node_threat = True

                case "Generic Denial of Service Dataflow Rule":
                    if threat.location_str(self.dfd) == "e1: ProcessA -> ProcessB":
                        has_denial_of_service_data_flow_threat = True

                case "Generic Elevation of Privilege Node Rule":
                    if threat.location_str(self.dfd) == "ProcessC":
                        has_elevation_of_privilege_node_threat = True

        assert has_spoofing_node_threat
        assert has_tampering_node_threat
        assert has_tampering_data_flow_threat
        assert has_repudiation_node_threat
        assert has_information_disclosure_node_threat
        assert has_information_disclosure_data_flow_threat
        assert has_denial_of_service_node_threat
        assert has_denial_of_service_data_flow_threat
        assert has_elevation_of_privilege_node_threat

# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from unittest.mock import Mock, patch

from flowstrider import settings
from flowstrider.models.common_models import Edge, Node
from flowstrider.models.dataflowdiagram import DataflowDiagram
from flowstrider.rules.builtin.bsi_rules.bsi_rule_collection import (
    AuthenticationProtocolNodeRule,
    ConfidentialDataflowEdgeRule,
    EncryptionOfConfidentialDataNodeRule,
    HashedPasswordsNodeRule,
    InputValidationNodeRule,
    IntegrityOfExternalEntitiesEdgeRule,
    LoggingDataNodeRule,
    MFAHighSecurityNodeRule,
    MFANodeRule,
    PermissionNodeRule,
    SecureHTTPConfigEdgeRule,
    UntrustworthyDataflowEdgeRule,
    UseOfProxiesEdgeRule,
    does_edge_cross_cluster_boundary,
    does_edge_have_external_source,
    get_smallest_cluster,
)

MODULE_PATH = "flowstrider.rules.builtin.bsi_rules.bsi_rule_collection"


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.dfd = Mock()
        self.edge = Mock()
        self.cluster1 = Mock(node_ids={1, 2, 3})
        self.cluster2 = Mock(node_ids={4, 5})

    def test_get_smallest_cluster_just_sink(self):
        self.edge.sink_id = 2
        self.dfd.get_clusters_for_node_id.return_value = [self.cluster1]
        result = get_smallest_cluster(self.edge, self.dfd, just_sink=True)
        self.assertEqual(result, self.cluster1)

    def test_get_smallest_cluster_includes_source(self):
        self.edge.sink_id = 2
        self.edge.source_id = 5
        self.dfd.get_clusters_for_node_id.side_effect = lambda node_id: [
            self.cluster1 if node_id == 2 else self.cluster2
        ]
        result = get_smallest_cluster(self.edge, self.dfd, just_sink=False)
        self.assertEqual(result, self.cluster2)  # Smaller cluster should be returned

    def test_get_smallest_cluster_no_clusters(self):
        self.dfd.get_clusters_for_node_id.return_value = []
        result = get_smallest_cluster(self.edge, self.dfd, just_sink=True)
        self.assertIsNone(result)

    def test_does_edge_cross_cluster_boundary_false(self):
        self.edge.sink_id = 2
        self.edge.source_id = 3
        self.dfd.get_clusters_for_node_id.return_value = [self.cluster1]
        self.assertFalse(does_edge_cross_cluster_boundary(self.edge, self.dfd))

    def test_does_edge_cross_cluster_boundary_true(self):
        self.edge.sink_id = 2
        self.edge.source_id = 5
        self.dfd.get_clusters_for_node_id.side_effect = lambda node_id: [
            self.cluster1 if node_id == 2 else self.cluster2
        ]
        self.assertTrue(does_edge_cross_cluster_boundary(self.edge, self.dfd))

    def test_does_edge_have_external_source_false(self):
        self.edge.sink_id = 2
        self.edge.source_id = 3
        self.dfd.get_clusters_for_node_id.return_value = [self.cluster1]
        self.assertFalse(does_edge_have_external_source(self.edge, self.dfd))

    def test_does_edge_have_external_source_true(self):
        self.edge.sink_id = 2
        self.edge.source_id = 6
        self.dfd.get_clusters_for_node_id.return_value = [self.cluster1]
        self.assertTrue(does_edge_have_external_source(self.edge, self.dfd))

    # Initialize Localization
    settings.init_localization("en", "sys")
    settings.init_localization("en", "out")


class TestUntrustWorthyDataflowEdgeRule(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(id="n1", name="ProcessA")
        self.node2 = Node(id="n2", name="ProcessB")
        self.node3 = Node(id="n3", name="ProcessC")

        # Edge that crosses boundary without TLS (should trigger rule)
        self.edge1 = Edge(
            id="e1",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={"transport_protocol": "HTTP"},  # Not secure
        )

        # Edge that crosses boundary but uses TLS (should NOT trigger rule)
        self.edge2 = Edge(
            id="e2",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={"transport_protocol": "TLS 1.2"},  # Secure
        )

        # Edge that does not cross a boundary (should NOT trigger rule)
        self.edge3 = Edge(
            id="e3",
            source_id=self.node1.id,
            sink_id=self.node3.id,
            attributes={"transport_protocol": "HTTP"},  # No TLS but safe
        )

        # Edge that crosses boundary but uses TLS (should NOT trigger rule)
        self.edge4 = Edge(
            id="e4",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={"transport_protocol": "https"},  # Secure
        )

        # Edge that crosses boundary but uses TLS (should NOT trigger rule)
        self.edge5 = Edge(
            id="e5",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={"transport_protocol": "TLs 1.3"},  # Secure
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={"node1": self.node1, "node2": self.node2},
            edges={
                "edge1": self.edge1,
                "edge2": self.edge2,
                "edge3": self.edge3,
                "edge4": self.edge4,
                "edge5": self.edge5,
            },
            clusters={},
        )

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    def test_rule_applies_when_no_tls_and_crosses_boundary(self, mock_crosses_boundary):
        mock_crosses_boundary.side_effect = (
            lambda edge, dfd: edge == self.edge1
        )  # Only edge1 crosses

        result = UntrustworthyDataflowEdgeRule._test(self.edge1, self.dfd)
        self.assertTrue(result)
        UntrustworthyDataflowEdgeRule.set_status(self.edge1)
        self.assertTrue(
            UntrustworthyDataflowEdgeRule.req_status == "Transport protocol = HTTP"
        )

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    def test_rule_does_not_apply_if_tls_is_used(self, mock_crosses_boundary):
        mock_crosses_boundary.return_value = True

        result = UntrustworthyDataflowEdgeRule._test(self.edge2, self.dfd)
        self.assertFalse(result)
        result = UntrustworthyDataflowEdgeRule._test(self.edge4, self.dfd)
        self.assertFalse(result)
        result = UntrustworthyDataflowEdgeRule._test(self.edge5, self.dfd)
        self.assertFalse(result)

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    def test_rule_does_not_apply_if_edge_does_not_cross_boundary(
        self, mock_crosses_boundary
    ):
        mock_crosses_boundary.side_effect = (
            lambda edge, dfd: edge != self.edge3
        )  # Only edge3 is safe

        result = UntrustworthyDataflowEdgeRule._test(self.edge3, self.dfd)
        self.assertFalse(result)

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    def test_rule_handles_missing_transport_protocol(self, mock_crosses_boundary):
        self.edge1.attributes.pop(
            "transport_protocol", None
        )  # Remove transport_protocol key
        mock_crosses_boundary.return_value = True  # Assume it crosses boundary

        result = UntrustworthyDataflowEdgeRule._test(self.edge1, self.dfd)
        self.assertTrue(result)  # Should still trigger as it is considered non-TLS
        UntrustworthyDataflowEdgeRule.set_status(self.edge1)
        self.assertTrue(
            UntrustworthyDataflowEdgeRule.req_status
            == "Attribute missing: Transport protocol"
        )


class TestConfidentialDataflowEdgeRule(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(id="n1", name="ProcessA")
        self.node2 = Node(id="n1", name="ProcessB")
        self.node3 = Node(id="n3", name="ProcessC")

        # Edge that crosses boundary should not trigger
        self.edge1 = Edge(
            id="e1",
            source_id=self.node1.id,
            sink_id=self.node3.id,
            attributes={"transport_protocol": "HTTP"},
        )

        # Edge that doesn't handle confidential data should not trigger
        self.edge2 = Edge(
            id="e2",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={"handles_confidential_data": False},
        )

        # Edge that uses TLS should not trigger
        self.edge3 = Edge(
            id="e3",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "transport_protocol": "TLS1.3",
                "handles_confidential_data": True,
            },
        )

        # Edge that handles confidential data and does not use TLS should trigger
        self.edge4 = Edge(
            id="e4",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "transport_protocol": "HTTP",
                "handles_confidential_data": True,
            },
        )

        # Edge that does not define transport protocol should trigger
        self.edge6 = Edge(
            id="e6",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "handles_confidential_data": True,
            },
        )

        # Edge that does not define if it handles confidential data should trigger
        self.edge7 = Edge(
            id="e7",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={},
        )

        # Edge that uses old TLS should trigger
        self.edge8 = Edge(
            id="e8",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "handles_confidential_data": True,
                "transport_protocol": "TLS 1.1",
            },
        )

        # Edge that uses TLS should not trigger
        self.edge5 = Edge(
            id="e5",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "transport_protocol": " https ",
                "handles_confidential_data": True,
            },
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={"node1": self.node1, "node2": self.node2, "node3": self.node3},
            edges={
                "edge1": self.edge1,
                "edge2": self.edge2,
                "edge3": self.edge3,
                "edge4": self.edge4,
                "edge5": self.edge5,
                "edge6": self.edge6,
                "edge7": self.edge7,
                "edge8": self.edge8,
            },
            clusters={},
        )

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    @patch(MODULE_PATH + ".does_edge_have_external_source")
    def test_rule_does_not_apply_if_edge_crosses_boundary(
        self, mock_external_source, mock_crosses_boundary
    ):
        mock_crosses_boundary.return_value = True  # Edge does cross boundary
        mock_external_source.return_value = True  # Edge does have external source

        result = ConfidentialDataflowEdgeRule._test(self.edge1, self.dfd)
        self.assertFalse(
            result
        )  # should not trigger because only interested in inside boundary

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    @patch(MODULE_PATH + ".does_edge_have_external_source")
    def test_rule_does_not_apply_if_not_confidential(
        self, mock_external_source, mock_crosses_boundary
    ):
        mock_crosses_boundary.return_value = False  # Edge does not cross boundary
        mock_external_source.return_value = False  # Edge does not have external source

        result = ConfidentialDataflowEdgeRule._test(self.edge2, self.dfd)
        self.assertFalse(result)  # should not trigger because data not confidential

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    @patch(MODULE_PATH + ".does_edge_have_external_source")
    def test_rule_does_not_apply_if_secure_protocol(
        self, mock_external_source, mock_crosses_boundary
    ):
        mock_crosses_boundary.return_value = False  # Edge does not cross boundary
        mock_external_source.return_value = False  # Edge does not have external source

        result = ConfidentialDataflowEdgeRule._test(self.edge3, self.dfd)
        self.assertFalse(result)  # should not trigger because TLS used
        result = ConfidentialDataflowEdgeRule._test(self.edge5, self.dfd)
        self.assertFalse(result)

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    @patch(MODULE_PATH + ".does_edge_have_external_source")
    def test_rule_does_apply_if_not_secure_protocol(
        self, mock_external_source, mock_crosses_boundary
    ):
        mock_crosses_boundary.return_value = False  # Edge does not cross boundary
        mock_external_source.return_value = False  # Edge does not have external source

        result = ConfidentialDataflowEdgeRule._test(self.edge4, self.dfd)
        self.assertTrue(result)  # should trigger because not TLS used and confidential
        ConfidentialDataflowEdgeRule.set_status(self.edge4)
        self.assertTrue(
            ConfidentialDataflowEdgeRule.req_status
            == "Handles confidential data = True\nTransport protocol = HTTP"
        )
        result = ConfidentialDataflowEdgeRule._test(self.edge6, self.dfd)
        self.assertTrue(result)  # should trigger because not TLS used and confidential
        ConfidentialDataflowEdgeRule.set_status(self.edge6)
        self.assertTrue(
            ConfidentialDataflowEdgeRule.req_status
            == "Handles confidential data = True\nAttribute missing: Transport protocol"
        )
        result = ConfidentialDataflowEdgeRule._test(self.edge7, self.dfd)
        self.assertTrue(
            result
        )  # should trigger because not TLS used and confidential not defined
        ConfidentialDataflowEdgeRule.set_status(self.edge7)
        self.assertTrue(
            ConfidentialDataflowEdgeRule.req_status
            == "Attribute missing: Handles confidential data\nAttribute missing:"
            + " Transport protocol"
        )
        result = ConfidentialDataflowEdgeRule._test(self.edge8, self.dfd)
        self.assertTrue(result)  # should trigger because depricated TLS version used
        ConfidentialDataflowEdgeRule.set_status(self.edge8)
        self.assertTrue(
            ConfidentialDataflowEdgeRule.req_status
            == "Handles confidential data = True\nTransport protocol = TLS 1.1"
        )


class TestSecureHTTPConfigEdgeRule(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(id="n1", name="ProcessA")
        self.node2 = Node(id="n1", name="ProcessB")
        self.node3 = Node(id="n3", name="ProcessC")

        # Edge that doesn't use HTTPS does not trigger
        self.edge1 = Edge(
            id="e1",
            source_id=self.node1.id,
            sink_id=self.node3.id,
            attributes={"transport_protocol": "something"},
        )

        # Edge that sets all required headers does not trigger
        self.edge2 = Edge(
            id="e2",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "transport_protocol": "https",
                "http_header": [
                    "Content Security Policy",
                    "Strict Transport Security",
                    "Content Type",
                    "X Content Options",
                    "Cache Control",
                ],
            },
        )

        # Edge that uses HTTPs but doesn't set all required headers should trigger
        self.edge3 = Edge(
            id="e3",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "transport_protocol": "https",
                "http_header": [
                    "Strict Transport Security",
                    "Content Type",
                    "X Content Options",
                    "Cache Control",
                ],
            },
        )

        # Edge that sets all required headers does not trigger
        self.edge4 = Edge(
            id="e4",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "transport_protocol": "HTTPS",
                "http_header": [
                    "Content security policy ",
                    "strict transport security",
                    "CONTENT TYPE",
                    " X Content Options",
                    "CacheControl",
                ],
            },
        )

        # Edge that uses HTTPs but doesn't set required headers should trigger
        self.edge5 = Edge(
            id="e5",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "transport_protocol": "https",
                "http_header": "Strict Transport Security",
            },
        )

        # Edge that doesn't define transport protocol but has all headers
        # ...should not trigger
        self.edge6 = Edge(
            id="e6",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "http_header": [
                    "Content security policy ",
                    "strict transport security",
                    "CONTENT TYPE",
                    " X Content Options",
                    "CacheControl",
                ],
            },
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={"node1": self.node1, "node2": self.node2, "node3": self.node3},
            edges={
                "edge1": self.edge1,
                "edge2": self.edge2,
                "edge3": self.edge3,
                "edge4": self.edge4,
                "edge5": self.edge5,
                "edge6": self.edge6,
            },
            clusters={},
        )

    def test_does_not_apply_if_not_https(self):
        result = SecureHTTPConfigEdgeRule._test(self.edge1, self.dfd)
        self.assertFalse(result)

    def test_does_not_apply_if_sets_req_headers(self):
        result = SecureHTTPConfigEdgeRule._test(self.edge2, self.dfd)
        self.assertFalse(result)
        result = SecureHTTPConfigEdgeRule._test(self.edge4, self.dfd)
        self.assertFalse(result)
        result = SecureHTTPConfigEdgeRule._test(self.edge6, self.dfd)
        self.assertFalse(result)

    def test_does_apply_if_https_and_not_req_headers(self):
        result = SecureHTTPConfigEdgeRule._test(self.edge3, self.dfd)
        self.assertTrue(result)
        SecureHTTPConfigEdgeRule.set_status(self.edge3)
        self.assertTrue(
            SecureHTTPConfigEdgeRule.req_status
            == "Transport protocol = https\nHTTP header = Strict Transport Security, "
            + "Content Type, X Content Options, Cache Control"
        )
        result = SecureHTTPConfigEdgeRule._test(self.edge5, self.dfd)
        self.assertTrue(result)
        SecureHTTPConfigEdgeRule.set_status(self.edge5)
        self.assertTrue(
            SecureHTTPConfigEdgeRule.req_status
            == "Transport protocol = https\nHTTP header = Strict Transport Security"
        )


class TestLoggingDataNodeRule(unittest.TestCase):
    def setUp(self):
        # Node that isn't a data store (DS) does not trigger
        self.node1 = Node(id="n1", name="ProcessA")

        # DS that doesn't specify if it handles logs should trigger
        self.node2 = Node(id="n2", name="ProcessB", tags=["STRIDE:DataStore"])

        # DS that doesn't handle Logs does not trigger
        self.node3 = Node(
            id="n3",
            name="ProcessC",
            tags=["STRIDE:DataStore"],
            attributes={"handles_logs": False},
        )

        # DS that handles Logs but doesn't specify signature scheme should trigger
        self.node4 = Node(
            id="n4",
            name="ProcessD",
            tags=["STRIDE:DataStore"],
            attributes={"handles_logs": True},
        )

        # DS that handles Logs but doesn't use allowed signature scheme should trigger
        self.node5 = Node(
            id="n5",
            name="ProcessE",
            tags=["STRIDE:DataStore"],
            attributes={"handles_logs": True, "signature_scheme": "ECSA"},
        )

        # DS that handles Logs and uses allowed signature scheme should not trigger
        self.node6 = Node(
            id="n6",
            name="ProcessF",
            tags=["STRIDE:DataStore"],
            attributes={"handles_logs": True, "signature_scheme": "DSA"},
        )

        # DS that handles Logs and uses allowed signature scheme should not trigger
        self.node7 = Node(
            id="n7",
            name="ProcessG",
            tags=["STRIDE:DataStore"],
            attributes={"handles_logs": True, "signature_scheme": "RSA-4096"},
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={
                "node1": self.node1,
                "node2": self.node2,
                "node3": self.node3,
                "node4": self.node4,
                "node5": self.node5,
                "node6": self.node6,
                "node7": self.node7,
            },
            edges={},
            clusters={},
        )

    def test_does_not_apply_if_component_not_datastore(self):
        result = LoggingDataNodeRule._test(self.node1, self.dfd)
        self.assertFalse(result)

    def test_does_apply_if_unclear_handles_logs(self):
        result = LoggingDataNodeRule._test(self.node2, self.dfd)
        self.assertTrue(result)
        LoggingDataNodeRule.set_status(self.node2)
        self.assertTrue(
            LoggingDataNodeRule.req_status
            == "Attribute missing: Handles logs\nAttribute missing: Signature scheme"
        )

    def test_does_not_apply_if_not_handles_logs(self):
        result = LoggingDataNodeRule._test(self.node3, self.dfd)
        self.assertFalse(result)

    def test_does_apply_if_logs_unclear_scheme(self):
        result = LoggingDataNodeRule._test(self.node4, self.dfd)
        self.assertTrue(result)
        LoggingDataNodeRule.set_status(self.node4)
        self.assertTrue(
            LoggingDataNodeRule.req_status
            == "Handles logs = True\nAttribute missing: Signature scheme"
        )

    def test_does_apply_if_logs_wrong_scheme(self):
        result = LoggingDataNodeRule._test(self.node5, self.dfd)
        self.assertTrue(result)
        LoggingDataNodeRule.set_status(self.node5)
        self.assertTrue(
            LoggingDataNodeRule.req_status
            == "Handles logs = True\nSignature scheme = ECSA"
        )

    def test_does_not_apply_if_logs_allowed_scheme(self):
        result = LoggingDataNodeRule._test(self.node6, self.dfd)
        self.assertFalse(result)
        result = LoggingDataNodeRule._test(self.node7, self.dfd)
        self.assertFalse(result)


class TestIntegrityofExternalEntitiesEdgeRule(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(id="n1", name="ProcessA")
        self.node2 = Node(id="n1", name="ProcessB")
        self.node3 = Node(id="n3", name="ProcessC")

        # Edge that doesn't have external source does not trigger
        self.edge1 = Edge(
            id="e1",
            source_id=self.node1.id,
            sink_id=self.node3.id,
        )

        # Edge that uses allowed check does not trigger
        self.edge2 = Edge(
            id="e2",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={"integrity_check": "check sum"},
        )

        # Edge that has external source but not allowed check should trigger
        self.edge3 = Edge(
            id="e3",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={"integrity_check": "Signature"},
        )

        # Edge that uses allowed check does not trigger
        self.edge4 = Edge(
            id="e4",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={"integrity_check": "ecdsa"},
        )

        # Edge that doesn't define check should trigger
        self.edge5 = Edge(
            id="e5",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={},
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={"node1": self.node1, "node2": self.node2, "node3": self.node3},
            edges={
                "edge1": self.edge1,
                "edge2": self.edge2,
                "edge3": self.edge3,
                "edge4": self.edge4,
                "edge5:": self.edge5,
            },
            clusters={},
        )

    @patch(MODULE_PATH + ".does_edge_have_external_source")
    def test_does_not_apply_if_internal_source(self, mock_external_source):
        mock_external_source.return_value = False

        result = IntegrityOfExternalEntitiesEdgeRule._test(self.edge1, self.dfd)
        self.assertFalse(result)

    @patch(MODULE_PATH + ".does_edge_have_external_source")
    def test_does_not_apply_if_allowed_check(self, mock_external_source):
        mock_external_source.return_value = True

        result = IntegrityOfExternalEntitiesEdgeRule._test(self.edge2, self.dfd)
        self.assertFalse(result)
        result = IntegrityOfExternalEntitiesEdgeRule._test(self.edge4, self.dfd)
        self.assertFalse(result)

    @patch(MODULE_PATH + ".does_edge_have_external_source")
    def test_does_apply_if_external_source_and_not_allowed_check(
        self, mock_external_source
    ):
        mock_external_source.return_value = True

        result = IntegrityOfExternalEntitiesEdgeRule._test(self.edge3, self.dfd)
        self.assertTrue(result)
        IntegrityOfExternalEntitiesEdgeRule.set_status(self.edge3)
        self.assertTrue(
            IntegrityOfExternalEntitiesEdgeRule.req_status
            == "Integrity check = Signature"
        )
        result = IntegrityOfExternalEntitiesEdgeRule._test(self.edge5, self.dfd)
        self.assertTrue(result)
        IntegrityOfExternalEntitiesEdgeRule.set_status(self.edge5)
        self.assertTrue(
            IntegrityOfExternalEntitiesEdgeRule.req_status
            == "Attribute missing: Integrity check"
        )


class TestUseOfProxiesEdgeRule(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(id="n1", name="ProcessA")
        self.node2 = Node(id="n1", name="ProcessB")
        self.node3 = Node(id="n3", name="ProcessC")

        # Edge that doesn't cross boundary does not trigger
        self.edge1 = Edge(
            id="e1", source_id=self.node1.id, sink_id=self.node3.id, attributes={}
        )

        # Edge that uses proxy does not trigger
        self.edge2 = Edge(
            id="e2",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={"proxy": True},
        )

        # Edge that has external source but not allowed check should trigger
        self.edge3 = Edge(
            id="e3",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={
                "proxy": False,
            },
        )

        # Edge that doesn't define if it uses proxy should trigger
        self.edge4 = Edge(
            id="e4",
            source_id=self.node1.id,
            sink_id=self.node2.id,
            attributes={},
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={"node1": self.node1, "node2": self.node2, "node3": self.node3},
            edges={"edge1": self.edge1, "edge2": self.edge2, "edge3": self.edge3},
            clusters={},
        )

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    def test_does_not_apply_if_not_crosses_boundary(self, mock_crosses_boundary):
        mock_crosses_boundary.return_value = False

        result = UseOfProxiesEdgeRule._test(self.edge1, self.dfd)
        self.assertFalse(result)

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    def test_does_not_apply_if_uses_proxy(self, mock_crosses_boundary):
        mock_crosses_boundary.return_value = True

        result = UseOfProxiesEdgeRule._test(self.edge2, self.dfd)
        self.assertFalse(result)

    @patch(MODULE_PATH + ".does_edge_cross_cluster_boundary")
    def test_does_apply_if_crosses_boundary_no_proxy(self, mock_crosses_boundary):
        mock_crosses_boundary.return_value = True

        result = UseOfProxiesEdgeRule._test(self.edge3, self.dfd)
        self.assertTrue(result)
        UseOfProxiesEdgeRule.set_status(self.edge3)
        self.assertTrue(UseOfProxiesEdgeRule.req_status == "Uses proxy = False")

        result = UseOfProxiesEdgeRule._test(self.edge4, self.dfd)
        self.assertTrue(result)
        UseOfProxiesEdgeRule.set_status(self.edge4)
        self.assertTrue(
            UseOfProxiesEdgeRule.req_status == "Attribute missing: Uses proxy"
        )


class TestHashedPasswordsNodeRule(unittest.TestCase):
    def setUp(self):
        # Node that is not a datastore does not trigger
        self.node1 = Node(
            id="n1",
            tags=["STRIDE:Process"],
        )
        # Node that does not store Credentials does not trigger
        self.node2 = Node(
            id="n2", tags=["STRIDE:DataStore"], attributes={"stores_credentials": False}
        )
        # node that uses allowed hash function does not trigger
        self.node3 = Node(
            id="n3",
            tags=["STRIDE:DataStore"],
            attributes={"stores_credentials": True, "hash_function": "SHA_256"},
        )
        # Node that stores credentials and does not use allowed function should trigger
        self.node4 = Node(
            id="n4",
            tags=["STRIDE:DataStore"],
            attributes={"stores_credentials": True, "hash_function": "SHA_128"},
        )
        # Node that stores credentials and does not use allowed function should trigger
        self.node5 = Node(
            id="n5",
            tags=["STRIDE:DataStore"],
            attributes={"stores_credentials": True, "hash_function": "SHA"},
        )
        # node that uses allowed hash function does not trigger
        self.node6 = Node(
            id="n6",
            tags=["STRIDE:DataStore"],
            attributes={"stores_credentials": True, "hash_function": "sha-512"},
        )
        # node that uses allowed hash function does not trigger
        self.node7 = Node(
            id="n7",
            tags=["STRIDE:DataStore"],
            attributes={"stores_credentials": True, "hash_function": "Sha 384"},
        )
        # Node that stores credentials and does not define function should trigger
        self.node8 = Node(
            id="n8", tags=["STRIDE:DataStore"], attributes={"stores_credentials": True}
        )
        # Node that does not define if it stores credentials should trigger
        self.node9 = Node(id="n9", tags=["STRIDE:DataStore"], attributes={})

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={
                "node1": self.node1,
                "node2": self.node2,
                "node3": self.node3,
                "node4": self.node4,
                "node5": self.node5,
                "node6": self.node6,
                "node7": self.node7,
                "node8": self.node8,
                "node9": self.node9,
            },
            edges={},
            clusters={},
        )

    def test_does_not_apply_if_not_datastore(self):
        result = HashedPasswordsNodeRule._test(self.node1, self.dfd)
        self.assertFalse(result)

    def test_does_not_apply_if_not_credentials(self):
        self.assertFalse(HashedPasswordsNodeRule._test(self.node2, self.dfd))

    def test_does_not_apply_if_allowed_hash_function(self):
        self.assertFalse(HashedPasswordsNodeRule._test(self.node3, self.dfd))
        self.assertFalse(HashedPasswordsNodeRule._test(self.node6, self.dfd))
        self.assertFalse(HashedPasswordsNodeRule._test(self.node7, self.dfd))

    def test_does_apply_if_stores_credentials_not_allowed_hash_function(self):
        self.assertTrue(HashedPasswordsNodeRule._test(self.node4, self.dfd))
        HashedPasswordsNodeRule.set_status(self.node4)
        self.assertTrue(
            HashedPasswordsNodeRule.req_status
            == "Stores credentials = True\nHash function = SHA_128"
        )
        self.assertTrue(HashedPasswordsNodeRule._test(self.node5, self.dfd))
        HashedPasswordsNodeRule.set_status(self.node5)
        self.assertTrue(
            HashedPasswordsNodeRule.req_status
            == "Stores credentials = True\nHash function = SHA"
        )
        self.assertTrue(HashedPasswordsNodeRule._test(self.node8, self.dfd))
        HashedPasswordsNodeRule.set_status(self.node8)
        self.assertTrue(
            HashedPasswordsNodeRule.req_status
            == "Stores credentials = True\nAttribute missing: Hash function"
        )
        self.assertTrue(HashedPasswordsNodeRule._test(self.node9, self.dfd))
        HashedPasswordsNodeRule.set_status(self.node9)
        self.assertTrue(
            HashedPasswordsNodeRule.req_status
            == "Attribute missing: Stores credentials\nAttribute missing: Hash function"
        )


class TestEncryptionOfConfidentialDataNodeRule(unittest.TestCase):
    def setUp(self):
        # Node that is not a datastore does not trigger
        self.node1 = Node(
            id="n1",
            tags=["STRIDE:Process"],
        )
        # Node that does not handle Confidential Data does not trigger
        self.node2 = Node(
            id="n2",
            tags=["STRIDE:DataStore"],
            attributes={"handles_confidential_data": False},
        )
        # Node that does not specify confidentialty should trigger
        self.node3 = Node(id="n3", tags=["STRIDE:DataStore"], attributes={})
        # Node that handles confidential data but not allowed encryption should trigger
        self.node4 = Node(
            id="n4",
            tags=["STRIDE:DataStore"],
            attributes={
                "handles_confidential_data": True,
                "encryption_method": "SHA_256",
            },
        )
        # Node that handles confidential data and
        # ...uses allowed encryption does not trigger
        self.node5 = Node(
            id="n5",
            tags=["STRIDE:DataStore"],
            attributes={
                "handles_confidential_data": True,
                "encryption_method": "AES_128",
            },
        )
        # Node that handles confidential data and
        # ...uses allowed encryption does not trigger
        self.node6 = Node(
            id="n6",
            tags=["STRIDE:DataStore"],
            attributes={
                "handles_confidential_data": True,
                "encryption_method": "AES 192",
            },
        )
        # Node that handles confidential data but doesn't define allowed encryption
        # ...should trigger
        self.node7 = Node(
            id="n7",
            tags=["STRIDE:DataStore"],
            attributes={"handles_confidential_data": True},
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={
                "node1": self.node1,
                "node2": self.node2,
                "node3": self.node3,
                "node4": self.node4,
                "node5": self.node5,
                "node6": self.node6,
                "node7": self.node7,
            },
            edges={},
            clusters={},
        )

    def test_does_not_apply_if_not_datastore(self):
        result = EncryptionOfConfidentialDataNodeRule._test(self.node1, self.dfd)
        self.assertFalse(result)

    def test_does_not_apply_if_not_confidential(self):
        self.assertFalse(
            EncryptionOfConfidentialDataNodeRule._test(self.node2, self.dfd)
        )

    def test_does_apply_if_confidentiality_unclear(self):
        self.assertTrue(
            EncryptionOfConfidentialDataNodeRule._test(self.node3, self.dfd)
        )
        EncryptionOfConfidentialDataNodeRule.set_status(self.node3)
        self.assertTrue(
            EncryptionOfConfidentialDataNodeRule.req_status
            == "Attribute missing: Handles confidential data\nAttribute missing: "
            + "Encryption method"
        )

    def test_does_apply_if_confidential_not_allowed_encryption(self):
        self.assertTrue(
            EncryptionOfConfidentialDataNodeRule._test(self.node4, self.dfd)
        )
        EncryptionOfConfidentialDataNodeRule.set_status(self.node4)
        self.assertTrue(
            EncryptionOfConfidentialDataNodeRule.req_status
            == "Handles confidential data = True\nEncryption method = SHA_256"
        )
        self.assertTrue(
            EncryptionOfConfidentialDataNodeRule._test(self.node7, self.dfd)
        )
        EncryptionOfConfidentialDataNodeRule.set_status(self.node7)
        self.assertTrue(
            EncryptionOfConfidentialDataNodeRule.req_status
            == "Handles confidential data = True\nAttribute missing: Encryption method"
        )

    def test_does_not_apply_if_allowed_encryption(self):
        self.assertFalse(
            EncryptionOfConfidentialDataNodeRule._test(self.node5, self.dfd)
        )
        self.assertFalse(
            EncryptionOfConfidentialDataNodeRule._test(self.node6, self.dfd)
        )


class TestAuthenticationProtocolNodeRule(unittest.TestCase):
    def setUp(self):
        # Node that is not a datastore does not trigger
        self.node1 = Node(
            id="n1",
            tags=["STRIDE:Process"],
        )
        # Node that uses allowed protocol does not trigger
        self.node2 = Node(
            id="n2",
            tags=["STRIDE:DataStore"],
            attributes={"is_san_fabric": True, "auth_protocol": "DH-CHAP"},
        )
        # node that does not specify protocol should trigger
        self.node3 = Node(
            id="n3", tags=["STRIDE:DataStore"], attributes={"is_san_fabric": True}
        )
        # Node that uses wrong protocol should trigger
        self.node4 = Node(
            id="n4",
            tags=["STRIDE:DataStore"],
            attributes={"is_san_fabric": True, "auth_protocol": "DCAP"},
        )
        # Node that uses allowed protocol does not trigger
        self.node5 = Node(
            id="n5",
            tags=["STRIDE:DataStore"],
            attributes={"auth_protocol": "FCPAP"},
        )
        # Node that is not SAN fabric does not trigger
        self.node6 = Node(
            id="n6",
            tags=["STRIDE:DataStore"],
            attributes={"is_san_fabric": False, "auth_protocol": "x"},
        )
        # Node doesn't specify SAN fabric but uses allowed protocol should not trigger
        self.node7 = Node(
            id="n7",
            tags=["STRIDE:DataStore"],
            attributes={"auth_protocol": "FCPAP"},
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={
                "node1": self.node1,
                "node2": self.node2,
                "node3": self.node3,
                "node4": self.node4,
                "node5": self.node5,
                "node6": self.node6,
                "node7": self.node7,
            },
            edges={},
            clusters={},
        )

    def test_does_not_apply_if_not_datastore(self):
        result = AuthenticationProtocolNodeRule._test(self.node1, self.dfd)
        self.assertFalse(result)

    def test_does_not_apply_if_not_san_fabric(self):
        result = AuthenticationProtocolNodeRule._test(self.node6, self.dfd)
        self.assertFalse(result)

    def test_does_not_apply_if_uses_allowed_protocol(self):
        self.assertFalse(AuthenticationProtocolNodeRule._test(self.node2, self.dfd))
        self.assertFalse(AuthenticationProtocolNodeRule._test(self.node5, self.dfd))
        self.assertFalse(AuthenticationProtocolNodeRule._test(self.node7, self.dfd))

    def test_does_apply_if_protocol_unclear(self):
        self.assertTrue(AuthenticationProtocolNodeRule._test(self.node3, self.dfd))
        AuthenticationProtocolNodeRule.set_status(self.node3)
        self.assertTrue(
            AuthenticationProtocolNodeRule.req_status
            == "Is SAN fabric = True\nAttribute missing: Authentication protocol"
        )

    def test_does_apply_if_uses_not_allowed_protocol(self):
        self.assertTrue(AuthenticationProtocolNodeRule._test(self.node4, self.dfd))
        AuthenticationProtocolNodeRule.set_status(self.node4)
        self.assertTrue(
            AuthenticationProtocolNodeRule.req_status
            == "Is SAN fabric = True\nAuthentication protocol = DCAP"
        )


class TestMFANodeRule(unittest.TestCase):
    def setUp(self):
        # Node that is not a datastore or process does not trigger
        self.node1 = Node(
            id="n1",
            tags=["STRIDE:Interactor"],
        )
        # Node that does not require authentication does not trigger
        self.node2 = Node(
            id="n2", tags=["STRIDE:DataStore"], attributes={"auth_req": False}
        )
        # Node that does not specify if authentication required should trigger
        self.node3 = Node(id="n3", tags=["STRIDE:Process"], attributes={})
        # Node that requires authentication but doesnt specify factors should trigger
        self.node4 = Node(
            id="n4", tags=["STRIDE:DataStore"], attributes={"auth_req": True}
        )
        # Node that requires authentication and uses less than 2 factors should trigger
        self.node5 = Node(
            id="n5",
            tags=["STRIDE:DataStore"],
            attributes={"auth_req": True, "auth_factors": ["OTP"]},
        )
        # Node that requires authentication and uses 2 factors does not trigger
        self.node6 = Node(
            id="n6",
            tags=["STRIDE:Process"],
            attributes={"auth_req": True, "auth_factors": ["OTP", "Biometrics"]},
        )
        # Node that requires authentication and uses less than 2 factors should trigger
        self.node7 = Node(
            id="n7",
            tags=["STRIDE:DataStore"],
            attributes={"auth_req": True, "auth_factors": "Custom factor 1"},
        )
        # Node that requires authentication and uses 2 factors does not trigger
        self.node8 = Node(
            id="n8",
            tags=["STRIDE:Process"],
            attributes={"auth_req": True, "auth_factors": "Custom factor 1, Custom 2"},
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={
                "node1": self.node1,
                "node2": self.node2,
                "node3": self.node3,
                "node4": self.node4,
                "node5": self.node5,
                "node6": self.node6,
                "node7": self.node7,
                "node8": self.node8,
            },
            edges={},
            clusters={},
        )

    def test_does_not_apply_if_not_datastore_or_process(self):
        result = MFANodeRule._test(self.node1, self.dfd)
        self.assertFalse(result)

    def test_does_not_apply_if_authentication_not_required(self):
        self.assertFalse(MFANodeRule._test(self.node2, self.dfd))

    def test_does_apply_if_authentication_requirement_unclear(self):
        self.assertTrue(MFANodeRule._test(self.node3, self.dfd))
        MFANodeRule.set_status(self.node3)
        self.assertTrue(
            MFANodeRule.req_status
            == "Attribute missing: Requires authentication\nAttribute missing: "
            + "Authentication factors"
        )

    def test_does_apply_if_auth_req_factors_unclear(self):
        self.assertTrue(MFANodeRule._test(self.node4, self.dfd))
        MFANodeRule.set_status(self.node4)
        self.assertTrue(
            MFANodeRule.req_status
            == "Requires authentication = True\nAttribute missing: Authentication "
            + "factors"
        )

    def test_does_apply_if_auth_req_just_one_factor(self):
        self.assertTrue(MFANodeRule._test(self.node5, self.dfd))
        MFANodeRule.set_status(self.node5)
        self.assertTrue(
            MFANodeRule.req_status
            == "Requires authentication = True\nAuthentication factors = OTP"
        )
        self.assertTrue(MFANodeRule._test(self.node7, self.dfd))
        MFANodeRule.set_status(self.node7)
        self.assertTrue(
            MFANodeRule.req_status == "Requires authentication = True\nAuthentication"
            " factors = Custom factor 1"
        )

    def test_does_not_apply_if_auth_req_factors_enough(self):
        self.assertFalse(MFANodeRule._test(self.node6, self.dfd))
        self.assertFalse(MFANodeRule._test(self.node8, self.dfd))


class TestMFAHighSecurityNodeRule(unittest.TestCase):
    def setUp(self):
        # Node that is not a datastore or process does not trigger
        self.node1 = Node(
            id="n1",
            tags=["STRIDE:Interactor"],
        )
        # Node that does not require authentication does not trigger
        self.node2 = Node(
            id="n2", tags=["STRIDE:DataStore"], attributes={"auth_req": False}
        )
        # Node that does not handle confidential data does not trigger
        self.node3 = Node(
            id="n3",
            tags=["STRIDE:Process"],
            attributes={"auth_req": True, "handles_confidential_data": False},
        )
        # Node that requires authentication, handles confidential data
        # but does not use secure factor should trigger
        self.node4 = Node(
            id="n4",
            tags=["STRIDE:DataStore"],
            attributes={"auth_req": True, "handles_confidential_data": True},
        )
        # Node that requires authentication, handles confidential data
        # and uses secure factor does not trigger
        self.node5 = Node(
            id="n5",
            tags=["STRIDE:DataStore"],
            attributes={
                "auth_req": True,
                "handles_confidential_data": True,
                "auth_factors": ["Chip Card"],
            },
        )
        # Node that requires authentication, handles confidential data
        # and uses secure factor does not trigger
        self.node6 = Node(
            id="n6",
            tags=["STRIDE:DataStore"],
            attributes={
                "auth_req": True,
                "handles_confidential_data": True,
                "auth_factors": ["security-token"],
            },
        )
        # Node that doesn't define if authentication is required and has wrong
        # ...authentication should trigger
        self.node7 = Node(
            id="n7",
            tags=["STRIDE:DataStore"],
            attributes={
                "handles_confidential_data": True,
                "auth_factors": ["x"],
            },
        )
        # Node that doesn't define if it handles confidential data and has wrong
        # ...authentication should trigger
        self.node8 = Node(
            id="n8",
            tags=["STRIDE:DataStore"],
            attributes={
                "auth_req": True,
                "auth_factors": ["x"],
            },
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={
                "node1": self.node1,
                "node2": self.node2,
                "node3": self.node3,
                "node4": self.node4,
                "node5": self.node5,
                "node6": self.node6,
                "node7": self.node7,
                "node8": self.node8,
            },
            edges={},
            clusters={},
        )

    def test_does_not_apply_if_not_datastore_or_process(self):
        result = MFAHighSecurityNodeRule._test(self.node1, self.dfd)
        self.assertFalse(result)

    def test_does_not_apply_if_authentication_not_required(self):
        self.assertFalse(MFAHighSecurityNodeRule._test(self.node2, self.dfd))

    def test_does_not_apply_if_not_confidential(self):
        self.assertFalse(MFAHighSecurityNodeRule._test(self.node3, self.dfd))

    def test_does_apply_if_auth_req_confidential_but_not_secure(self):
        self.assertTrue(MFAHighSecurityNodeRule._test(self.node4, self.dfd))
        MFAHighSecurityNodeRule.set_status(self.node4)
        self.assertTrue(
            MFAHighSecurityNodeRule.req_status
            == "Handles confidential data = True\nAttribute missing: Authentication "
            + "factors\nRequires authentication = True"
        )
        self.assertTrue(MFAHighSecurityNodeRule._test(self.node7, self.dfd))
        MFAHighSecurityNodeRule.set_status(self.node7)
        self.assertTrue(
            MFAHighSecurityNodeRule.req_status
            == "Handles confidential data = True\nAuthentication factors = x\n"
            + "Attribute missing: Requires authentication"
        )
        self.assertTrue(MFAHighSecurityNodeRule._test(self.node8, self.dfd))
        MFAHighSecurityNodeRule.set_status(self.node8)
        self.assertTrue(
            MFAHighSecurityNodeRule.req_status
            == "Attribute missing: Handles confidential data\nAuthentication "
            + "factors = x\nRequires authentication = True"
        )

    def test_does_not_apply_if_secure_factor(self):
        self.assertFalse(MFAHighSecurityNodeRule._test(self.node5, self.dfd))
        self.assertFalse(MFAHighSecurityNodeRule._test(self.node6, self.dfd))


class TestPermissionNodeRule(unittest.TestCase):
    def setUp(self):
        # Node that is not a interactor or process does not trigger
        self.node1 = Node(
            id="n1",
            tags=["STRIDE:DataStore"],
        )
        # Node that specifies required but not given permissions should trigger
        self.node3 = Node(
            id="n3",
            tags=["STRIDE:Process"],
            attributes={"req_permissions": ["read", "write"]},
        )
        # Node with more given than required permissions should trigger
        self.node4 = Node(
            id="n4",
            tags=["STRIDE:Interactor"],
            attributes={
                "req_permissions": ["read"],
                "given_permissions": ["read", "write"],
            },
        )
        # Node with matching or less given permission than required does not trigger
        self.node5 = Node(
            id="n5",
            tags=["STRIDE:Interactor"],
            attributes={"req_permissions": ["read"], "given_permissions": ["read"]},
        )
        # Node with matching or less given permission than required does not trigger
        self.node6 = Node(
            id="n6",
            tags=["STRIDE:Interactor"],
            attributes={
                "req_permissions": ["read", "write", "delete"],
                "given_permissions": ["Write", "Read"],
            },
        )
        # Node that doesn't define either should trigger
        self.node7 = Node(
            id="n7",
            tags=["STRIDE:Interactor"],
            attributes={},
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={
                "node1": self.node1,
                "node3": self.node3,
                "node4": self.node4,
                "node5": self.node5,
                "node6": self.node6,
                "node7": self.node7,
            },
            edges={},
            clusters={},
        )

    def test_does_not_apply_if_not_interactor_or_process(self):
        result = PermissionNodeRule._test(self.node1, self.dfd)
        self.assertFalse(result)

    def test_does_apply_if_given_permissions_unclear(self):
        self.assertTrue(PermissionNodeRule._test(self.node3, self.dfd))
        PermissionNodeRule.set_status(self.node3)
        self.assertTrue(
            PermissionNodeRule.req_status
            == "Required permissions = read, write\nAttribute missing: "
            + "Given permissions"
        )
        self.assertTrue(PermissionNodeRule._test(self.node7, self.dfd))
        PermissionNodeRule.set_status(self.node7)
        self.assertTrue(
            PermissionNodeRule.req_status
            == "Attribute missing: Required permissions\nAttribute missing: "
            + "Given permissions"
        )

    def test_does_apply_if_too_many_given_permissions(self):
        self.assertTrue(PermissionNodeRule._test(self.node4, self.dfd))
        PermissionNodeRule.set_status(self.node4)
        self.assertTrue(
            PermissionNodeRule.req_status
            == "Required permissions = read\nGiven permissions = read, write"
        )

    def test_does_not_apply_if_given_match_required_permissions(self):
        self.assertFalse(PermissionNodeRule._test(self.node5, self.dfd))
        self.assertFalse(PermissionNodeRule._test(self.node6, self.dfd))


class TestInputValidationNodeRule(unittest.TestCase):
    def setUp(self):
        # Node that is not a process does not trigger
        self.node1 = Node(
            id="n1",
            tags=["STRIDE:DataStore"],
        )

        # Node where input is not validated should trigger
        self.node3 = Node(
            id="n3",
            tags=["STRIDE:Process"],
            attributes={
                "input_data": ["User Query"],
                "input_validation": False,
            },
        )

        # Node with enough validation and no sanitization does not trigger
        self.node2 = Node(
            id="n2",
            tags=["STRIDE:Process"],
            attributes={
                "input_data": ["User Query"],
                "input_validation": ["XSS Scanning", "Client-side validation"],
            },
        )

        # Node where input is not specified should trigger
        self.node4 = Node(
            id="n4",
            tags=["STRIDE:Process"],
            attributes={
                "input_validation": ["XSS Scanning", "Client-side validation"],
            },
        )

        # Node where validation is not specified should trigger
        self.node5 = Node(
            id="n5",
            tags=["STRIDE:Process"],
            attributes={"input_data": ["User Query"]},
        )

        # Diagram setup
        self.dfd = DataflowDiagram(
            name="Test DFD",
            id="d1",
            nodes={
                "node1": self.node1,
                "node3": self.node3,
                "node2": self.node2,
                "node4": self.node4,
                "node5": self.node5,
            },
            edges={},
            clusters={},
        )

    def test_does_not_apply_if_not_process(self):
        result = InputValidationNodeRule._test(self.node1, self.dfd)
        self.assertFalse(result)

    def test_does_apply_if_not_enough_validation(self):
        self.assertTrue(InputValidationNodeRule._test(self.node3, self.dfd))
        InputValidationNodeRule.set_status(self.node3)
        self.assertTrue(
            InputValidationNodeRule.req_status
            == "Input data = User Query\nInput validation = False"
        )
        self.assertTrue(InputValidationNodeRule._test(self.node5, self.dfd))
        InputValidationNodeRule.set_status(self.node5)
        self.assertTrue(
            InputValidationNodeRule.req_status
            == "Input data = User Query\nAttribute missing: Input validation"
        )

    def test_does_apply_if_input_not_specified(self):
        self.assertTrue(InputValidationNodeRule._test(self.node4, self.dfd))
        InputValidationNodeRule.set_status(self.node4)
        self.assertTrue(
            InputValidationNodeRule.req_status
            == "Attribute missing: Input data\nInput validation = XSS Scanning, "
            + "Client-side validation"
        )

    def test_does_not_apply_if_no_sanitization_and_validated(self):
        self.assertFalse(InputValidationNodeRule._test(self.node2, self.dfd))

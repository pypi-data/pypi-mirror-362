# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import re

from flowstrider import settings
from flowstrider.models import dataflowdiagram
from flowstrider.models.common_models import Cluster, Edge, Node
from flowstrider.rules import attributes_dict
from flowstrider.rules.common_rules import (
    DataflowDiagramRuleCollection,
    EdgeRule,
    NodeRule,
    meet_all_requirement,
    meet_any_requirement,
)

# Rules derived from the basis of the BSI checklists
# ...'Checklisten zum IT-Grundschutz-Kompendium (Edition 2023)'
# ...https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium/checklisten_2023.html


# Helper method
def get_smallest_cluster(
    edge: Edge, dfd: dataflowdiagram.DataflowDiagram, just_sink: bool
) -> Cluster:
    clusters = dfd.get_clusters_for_node_id(edge.sink_id)
    if not just_sink:
        clusters += dfd.get_clusters_for_node_id(edge.source_id)

    if not clusters:
        return None

    return min(clusters, key=lambda cluster: len(cluster.node_ids))


# Helper method
def does_edge_cross_cluster_boundary(edge: Edge, dfd: dataflowdiagram.DataflowDiagram):
    smallest_involved_cluster = get_smallest_cluster(edge, dfd, False)

    if not smallest_involved_cluster:
        return True

    if (
        edge.sink_id in smallest_involved_cluster.node_ids
        and edge.source_id in smallest_involved_cluster.node_ids
    ):
        return False

    return True


# Helper method
def does_edge_have_external_source(edge: Edge, dfd: dataflowdiagram.DataflowDiagram):
    smallest_sink_cluster = get_smallest_cluster(edge, dfd, True)

    if not smallest_sink_cluster:
        return True

    if edge.source_id in smallest_sink_cluster.node_ids:
        return False

    return True


class UntrustworthyDataflowEdgeRule(EdgeRule):
    allowed_protocols = ""

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Untrustworthy Data Flow")
        cls.short_description = _(
            "Transportprotokoll für Verbindungen außerhalb der Vertrauensgrenze"
        )
        cls.long_description = _(
            "Datenflüsse, die Vertrauensgrenzen überschreiten, MÜSSEN "
            "gemäß Richtlinien APP.3.2.A11 und NET.1.1.A7 des "
            "IT-Grundschutzkompendium des BSI, "
            "ein sicheres Transportprotokoll, wie TLS, einsetzen, "
            "um die Vertraulichkeit der Daten zu bewahren."
        )
        cls.attribute_names = ["transport_protocol"]
        cls.allowed_protocols = attributes_dict.attributes[cls.attribute_names[0]][3]

        cls.mitigation_options = [_("TLS einsetzen")]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[0]][0]
            + _(": one of {")
            + ", ".join(cls.allowed_protocols)
            + "}"
        )

    @classmethod
    def _test(cls, edge: Edge, dfd: dataflowdiagram.DataflowDiagram) -> bool:
        crosses_boundary = does_edge_cross_cluster_boundary(edge, dfd)

        uses_TLS = cls.attribute_names[0] in edge.attributes and meet_any_requirement(
            edge.attributes[cls.attribute_names[0]], cls.allowed_protocols
        )

        return crosses_boundary and not uses_TLS


class ConfidentialDataflowEdgeRule(EdgeRule):
    allowed_protocols = ""

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Confidential Data Flow")
        cls.short_description = _("Transportprotokoll für vertrauliche Daten")
        cls.long_description = _(
            "Gemäß u.a. Richtlinie APP.2.1.A13 des IT-Grundschutzkompendiums des BSI "
            "SOLLTEN Datenflüsse, die innerhalb der Vertrauensgrenzen vertrauliche "
            "Daten übertragen, ein sicheres Transportprotokoll, wie TLS, einsetzen."
        )
        cls.attribute_names = ["handles_confidential_data", "transport_protocol"]
        cls.allowed_protocols = attributes_dict.attributes[cls.attribute_names[1]][3]

        cls.mitigation_options = [_("TLS einsetzen")]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[1]][0]
            + _(": one of {")
            + ", ".join(cls.allowed_protocols)
            + "}"
        )

    @classmethod
    def _test(cls, edge: Edge, dfd: dataflowdiagram.DataflowDiagram):
        is_inside_boundary = not does_edge_cross_cluster_boundary(
            edge, dfd
        ) and not does_edge_have_external_source(edge, dfd)

        handles_confidential_data = (
            cls.attribute_names[0] in edge.attributes
            and edge.attributes[cls.attribute_names[0]]
        ) or cls.attribute_names[0] not in edge.attributes

        uses_TLS = cls.attribute_names[1] in edge.attributes and meet_any_requirement(
            edge.attributes[cls.attribute_names[1]], cls.allowed_protocols
        )

        return is_inside_boundary and handles_confidential_data and not uses_TLS


class SecureHTTPConfigEdgeRule(EdgeRule):
    checked_protocols = ""
    required_headers = ""

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Secure HTTP Configuration")
        cls.short_description = _("Sichere HTTP-Konfiguration bei Webanwendungen")
        cls.long_description = _(
            "Gemäß Richtlinien CON.10.A14, APP.3.1.A21 des IT-Grundschutzkompendium "
            "des BSI SOLLTEN zum Schutz vor Clickjacking, Cross-Site-Scripting und "
            "anderen Angriffen geeignete HTTP-Response-Header verwendet werden. "
            "Mindestens Content-Security-Policy, Strict-Transport-Security, "
            "Content-Type, X-Content-Options und Cache-Control. Die HTTP-Header "
            "SOLLTEN auf die Webanwendung abgestimmt werden und SOLLTEN so restriktiv "
            "wie möglilch sein."
        )
        cls.attribute_names = ["transport_protocol", "http_header"]
        cls.checked_protocols = attributes_dict.attributes[cls.attribute_names[0]][3]
        cls.required_headers = attributes_dict.attributes[cls.attribute_names[1]][3]

        cls.mitigation_options = [
            _("Prüfen, dass alle erforderlichen HTTP-Response-Header gesetzt sind")
        ]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[1]][0]
            + _(": all of {")
            + ", ".join(cls.required_headers)
            + "}"
        )

    @classmethod
    def _test(cls, edge: Edge, dfd: dataflowdiagram.DataflowDiagram):
        is_https_request = (
            cls.attribute_names[0] in edge.attributes
            and meet_any_requirement(
                edge.attributes[cls.attribute_names[0]], cls.checked_protocols
            )
            or cls.attribute_names[0] not in edge.attributes
        )

        sets_required_headers = cls.attribute_names[
            1
        ] in edge.attributes and meet_all_requirement(
            edge.attributes[cls.attribute_names[1]], cls.required_headers
        )

        return is_https_request and not sets_required_headers


class IntegrityOfExternalEntitiesEdgeRule(EdgeRule):
    allowed_checks = ""

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Integrity of External Entities")
        cls.short_description = _("Integritätsprüfung externer Elemente")
        cls.long_description = _(
            "Gemäß Richtlinie CON.8.A20 des IT-Grundschutzkompendium des BSI, "
            "MÜSSEN externe Komponeneten und Daten von externen Elementen auf ihre "
            "Integrität und Schwachstellen geprüft werden. Die Integrität MUSS "
            "mittels Prüfsummen oder kryptografischen Zertifikaten überprügt werden. "
            "Es SOLLTEN keine veralteten Versionen von externen Komponenten verwendet "
            "werden."
        )
        cls.attribute_names = ["integrity_check"]
        cls.allowed_checks = attributes_dict.attributes[cls.attribute_names[0]][3]

        cls.mitigation_options = [
            _("Prüfsummen oder digitale Zertifikate zur Integritätsprüfung einsetzen")
        ]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[0]][0]
            + _(": one of {")
            + ", ".join(cls.allowed_checks)
            + "}"
        )

    @classmethod
    def _test(cls, edge: Edge, dfd: dataflowdiagram.DataflowDiagram):
        has_external_source = does_edge_have_external_source(edge, dfd)

        uses_allowed_check = cls.attribute_names[
            0
        ] in edge.attributes and meet_any_requirement(
            edge.attributes[cls.attribute_names[0]], cls.allowed_checks
        )

        return has_external_source and not uses_allowed_check


class UseOfProxiesEdgeRule(EdgeRule):
    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Use of Proxies")
        cls.short_description = _("Einsatz von TLS/SSL-Proxies")
        cls.long_description = _(
            "Gemäß Richtlinie DER.1.A10 des IT-Grundschutzkompendium des BSI "
            "SOLLTEN an den Übergängen zu externen Netzen TLS-/SSL-Proxies eingesetzt "
            "werden um übertragene Daten auf Malware zu prüfen. Diese Proxies SOLLTEN "
            "vor unbefugten Zugriffen geschützt werden. Sicherheitsrelevante "
            "Ereignisse SOLLTEN automatisch entdeckt werden."
        )
        cls.attribute_names = ["proxy"]

        cls.mitigation_options = [_("Proxies einsetzen")]
        cls.requirement = attributes_dict.attributes[cls.attribute_names[0]][0] + (
            " = True"
        )

    @classmethod
    def _test(cls, edge: Edge, dfd: dataflowdiagram.DataflowDiagram):
        crosses_boundary = does_edge_cross_cluster_boundary(edge, dfd)

        passes_through_proxy = (
            cls.attribute_names[0] in edge.attributes
            and edge.attributes[cls.attribute_names[0]]
        )

        return crosses_boundary and not passes_through_proxy


class LoggingDataNodeRule(NodeRule):
    allowed_signature_schemes = ""

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Signature of Logging Data")
        cls.short_description = _("Digitale Signatur für Protokollierungsdaten")
        cls.long_description = _(
            "Gemäß Richtlinie OPS.1.1.5.A12 des IT-Grundschutzkompendiums des BSI, "
            "SOLLTEN gespeicherte Protokollierungsdaten digital signiert sein. "
            "Zu den empfohlenen Signaturverfahren gemäß der "
            "Technischen Richtlinie TR-02102 des BSI zählen: "
            "RSA, DSA, ECDSA, ECKDSA, ECGDSA, XMSS, LMS."
        )
        cls.attribute_names = ["handles_logs", "signature_scheme"]
        cls.allowed_signature_schemes = attributes_dict.attributes[
            cls.attribute_names[1]
        ][3]

        cls.mitigation_options = [
            _(
                "Prüfen, dass Protokollierungsdaten mit einem"
                + " empfohlenen Verfahren signiert werden"
            )
        ]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[1]][0]
            + _(": one of {")
            + ", ".join(cls.allowed_signature_schemes)
            + "}"
        )

    @classmethod
    def _test(cls, node: Node, dfd: dataflowdiagram.DataflowDiagram):
        is_datastore = "STRIDE:DataStore" in node.tags

        handles_logging_data = (
            cls.attribute_names[0] in node.attributes
            and node.attributes[cls.attribute_names[0]]
        ) or cls.attribute_names[0] not in node.attributes

        uses_allowed_signature_scheme = cls.attribute_names[
            1
        ] in node.attributes and meet_any_requirement(
            node.attributes[cls.attribute_names[1]], cls.allowed_signature_schemes
        )

        return (
            handles_logging_data and is_datastore and not uses_allowed_signature_scheme
        )


class HashedPasswordsNodeRule(NodeRule):
    allowed_hash_functions = ""

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Hashing of Passwords")
        cls.short_description = _("Passwörter müssen gehashed werden")
        cls.long_description = _(
            "Gemäß Richtlinien CON.8.A5, CON.10.A7, APP.3.1.A14 und APP.3.2.A5 "
            "des IT-Grundschutzkompendium "
            "MÜSSEN Passwörter serverseitig mit einem sicheren Salted Hash "
            "Verfahren gespeichert werden. Dazu zählen gemäß der "
            "Technischen Richtlinie TR-02102 des BSI: "
            "SHA-256, SHA-512/256, SHA-384, SHA-512, SHA3-256, SHA3-384, SHA3-512."
        )
        cls.attribute_names = ["stores_credentials", "hash_function"]
        cls.allowed_hash_functions = attributes_dict.attributes[cls.attribute_names[1]][
            3
        ]

        cls.mitigation_options = [
            _("Prüfen, dass eines der empfohlenen Hash-Verfahren genutzt wird")
        ]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[1]][0]
            + _(": one of {")
            + ", ".join(cls.allowed_hash_functions)
            + "}"
        )

    @classmethod
    def _test(cls, node: Node, dfd: dataflowdiagram.DataflowDiagram):
        is_datastore = "STRIDE:DataStore" in node.tags

        stores_passwords = (
            cls.attribute_names[0] in node.attributes
            and node.attributes[cls.attribute_names[0]]
        ) or cls.attribute_names[0] not in node.attributes

        uses_allowed_hash_function = cls.attribute_names[
            1
        ] in node.attributes and meet_any_requirement(
            node.attributes[cls.attribute_names[1]], cls.allowed_hash_functions
        )

        return is_datastore and stores_passwords and not uses_allowed_hash_function


class EncryptionOfConfidentialDataNodeRule(NodeRule):
    allowed_encryption = ""

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Encryption of Confidential Data")
        cls.short_description = _("Vertrauliche Daten müssen verschlüsselt werden")
        cls.long_description = _(
            "Gemäß der Richtlinien CON.8.A5, CON.10.A18, "
            "APP.4.3.A24 und SYS.1.8.A23 des IT-Grundschutzkompendium "
            "SOLLTEN Vertrauliche Daten mit einem sicheren kryptografischen "
            "Verfahren verschlüsselt werden "
            "Dazu zählen: AES-128, AES-192, AES-256."
        )
        cls.attribute_names = ["handles_confidential_data", "encryption_method"]
        cls.allowed_encryption = attributes_dict.attributes[cls.attribute_names[1]][3]

        cls.mitigation_options = [
            _(
                "Prüfen, dass eines der empfohlenen Verschlüsselungsverfahren genutzt "
                "wird"
            )
        ]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[1]][0]
            + _(": one of {")
            + ", ".join(cls.allowed_encryption)
            + "}"
        )

    @classmethod
    def _test(cls, node: Node, dfd: dataflowdiagram.DataflowDiagram):

        is_datastore = "STRIDE:DataStore" in node.tags

        handles_confidential_data = (
            cls.attribute_names[0] in node.attributes
            and node.attributes[cls.attribute_names[0]]
        ) or cls.attribute_names[0] not in node.attributes

        uses_allowed_encryption = cls.attribute_names[
            1
        ] in node.attributes and meet_any_requirement(
            node.attributes[cls.attribute_names[1]], cls.allowed_encryption
        )

        return (
            is_datastore and handles_confidential_data and not uses_allowed_encryption
        )


class AuthenticationProtocolNodeRule(NodeRule):
    allowed_protocols = ""

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Authentication Protocols for SAN fabric")
        cls.short_description = _(
            "Sicherstellung der Speicher-Integrität durch sichere Protokolle"
        )
        cls.long_description = _(
            "Um die Integrität der Speicherlösung sicherzustellen, "
            "SOLLTEN Protokolle mit zusätzlichen Sicherheitsmerkmalen eingesetzt "
            "und entsprechend konfiguriert werden. Dazu zählen gemäß Richtlinie "
            "SYS.1.8.A24 des IT-Grunschutzkompendium: DH-CHAP, FCAP, FCPAP."
        )
        cls.attribute_names = ["is_san_fabric", "auth_protocol"]
        cls.allowed_protocols = attributes_dict.attributes[cls.attribute_names[1]][3]

        cls.mitigation_options = [
            _("Prüfen, dass eines der empfohlenen Protokolle verwendet wird")
        ]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[1]][0]
            + _(": one of {")
            + ", ".join(cls.allowed_protocols)
            + "}"
        )

    @classmethod
    def _test(cls, node: Node, dfd: dataflowdiagram.DataflowDiagram):
        is_datastore = "STRIDE:DataStore" in node.tags

        is_san_fabric = (
            cls.attribute_names[0] in node.attributes
            and node.attributes[cls.attribute_names[0]]
        ) or cls.attribute_names[0] not in node.attributes

        uses_allowed_protocol = cls.attribute_names[
            1
        ] in node.attributes and meet_any_requirement(
            node.attributes[cls.attribute_names[1]], cls.allowed_protocols
        )

        return is_datastore and is_san_fabric and not uses_allowed_protocol


class MFANodeRule(NodeRule):
    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Multi Factor Authentication")
        cls.short_description = _("Multi-Faktor-Authentisierung")
        cls.long_description = _(
            "Falls eine Authentisierung gemäß Richtlinien CON.10.A16, APP.3.1.A1 und "
            "CON.8.A5 des IT-Grundschutzkompendium erforderlich ist, SOLLTE die Liste "
            "der Authentisierungs-Faktoren zwei oder mehr Elemente umfassen."
        )
        cls.attribute_names = ["auth_req", "auth_factors"]

        cls.mitigation_options = [_("Authentisierungsfaktoren hinzufügen")]
        cls.requirement = attributes_dict.attributes[cls.attribute_names[1]][0] + _(
            ": count >= 2"
        )

    @classmethod
    def _test(cls, node: Node, dfd: dataflowdiagram.DataflowDiagram):
        is_Process_or_Datastore = (
            "STRIDE:DataStore" in node.tags or "STRIDE:Process" in node.tags
        )

        requires_authentication = (
            cls.attribute_names[0] in node.attributes
            and node.attributes[cls.attribute_names[0]]
        ) or cls.attribute_names[0] not in node.attributes

        if cls.attribute_names[1] in node.attributes:
            node_auth_factors = node.attributes[cls.attribute_names[1]]
            if type(node.attributes[cls.attribute_names[1]]) is not str:
                node_auth_factors = ", ".join(node_auth_factors)
            node_auth_factors = re.split(",|;|\\.", node_auth_factors)
        uses_multiple_factors = (
            cls.attribute_names[1] in node.attributes and len(node_auth_factors) >= 2
        )

        return (
            is_Process_or_Datastore
            and requires_authentication
            and not uses_multiple_factors
        )


class MFAHighSecurityNodeRule(NodeRule):
    secure_factors = ""

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Multi Factor Authentication for High Security")
        cls.short_description = _(
            "Authentisierungsfaktoren bei hohem Sicherheitsbedarf"
        )
        cls.long_description = _(
            "Falls hoher Sicherheitsbedarf besteht, SOLLTE gemäß der Richtlinien "
            "ORP.4.A21 und CON.8.A5 des IT-Grundschutzkompendiums eine sichere "
            "Mehr-Faktor-Authentisierung verwendet werden. Zum Beispiel mit "
            "kryptografischen Zertifikaten, Chipkarten oder Tokens."
        )
        cls.attribute_names = ["handles_confidential_data", "auth_factors", "auth_req"]
        cls.secure_factors = attributes_dict.attributes[cls.attribute_names[1]][3]

        cls.mitigation_options = [_("Authentisierungsfaktoren hinzufügen")]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[1]][0]
            + _(": one of {")
            + ", ".join(cls.secure_factors)
            + "}"
        )

    @classmethod
    def _test(cls, node: Node, dfd: dataflowdiagram.DataflowDiagram):
        is_process_or_datastore = (
            "STRIDE:DataStore" in node.tags or "STRIDE:Process" in node.tags
        )
        requires_authentication = (
            cls.attribute_names[2] in node.attributes
            and node.attributes[cls.attribute_names[2]]
        ) or cls.attribute_names[2] not in node.attributes

        handles_confidential_data = (
            cls.attribute_names[0] in node.attributes
            and node.attributes[cls.attribute_names[0]]
        ) or cls.attribute_names[0] not in node.attributes

        uses_secure_factor = False
        if cls.attribute_names[1] in node.attributes:
            for factor in node.attributes[cls.attribute_names[1]]:
                if meet_any_requirement(factor, cls.secure_factors):
                    uses_secure_factor = True

        return (
            is_process_or_datastore
            and requires_authentication
            and handles_confidential_data
            and not uses_secure_factor
        )


class PermissionNodeRule(NodeRule):
    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Least Privileges")
        cls.short_description = _("Nur notwendige Berechtigungen vergeben")
        cls.long_description = _(
            "Prozesse MÜSSEN gemäß Richtlinie CON.8.A5 des IT-Grundschutzkompendium "
            "mit möglichst geringen Privilegien ausgeführt werden können. Nutzer "
            "SOLLTEN nur Berechtigungen erhalten, die zur Dürchführung ihrer Aufgabe "
            "notwendig sind."
        )
        cls.attribute_names = ["req_permissions", "given_permissions"]

        cls.mitigation_options = [_("Prüfen, ob alle vergebenen Rechte notwendig sind")]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[0]][0]
            + _(" same as ")
            + attributes_dict.attributes[cls.attribute_names[1]][0]
        )

    @classmethod
    def _test(cls, node: Node, dfd: dataflowdiagram.DataflowDiagram):
        is_interactor_or_process = (
            "STRIDE:Interactor" in node.tags or "STRIDE:Process" in node.tags
        )
        fullfills_least_privilege = (
            cls.attribute_names[0] in node.attributes
            and cls.attribute_names[1] in node.attributes
        )
        if fullfills_least_privilege:
            for req_perm in node.attributes[cls.attribute_names[1]]:
                if not meet_any_requirement(
                    req_perm, node.attributes[cls.attribute_names[0]]
                ):
                    fullfills_least_privilege = False

        return is_interactor_or_process and not fullfills_least_privilege


class InputValidationNodeRule(NodeRule):
    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Input Validation")
        cls.short_description = _("Eingabevalidierung")
        cls.long_description = _(
            "Gemäß der Richtlinien CON.8.A5 und CON.10.A8 des IT-Grundschutzkompendium "
            "MÜSSEN sämtliche Eingabedaten, Datenströme und Sekundärdaten, wie z.B. "
            "Session-IDs serverseitig validiert werden."
            # "die Liste der Eingabevalidierungen mind. gleich lang sein,"
            # + " wie die Liste der Eingabedaten."
        )
        cls.attribute_names = ["input_data", "input_validation"]

        cls.mitigation_options = [_("Alle Eingabedaten validieren")]
        cls.requirement = (
            attributes_dict.attributes[cls.attribute_names[0]][0]
            + _(" and ")
            + attributes_dict.attributes[cls.attribute_names[1]][0]
        )

    @classmethod
    def _test(cls, node: Node, dfd: dataflowdiagram.DataflowDiagram):
        is_Process = "STRIDE:Process" in node.tags

        # no_sanitization = (
        #     "input_validation" in node.attributes
        #     and "sanitization" not in node.attributes["input_validation"]
        # )
        validation_matches_input = (
            cls.attribute_names[0] in node.attributes
            and cls.attribute_names[1] in node.attributes
            and node.attributes[cls.attribute_names[1]]
            # and len(node.attributes["input_validation"])
            # >= len(node.attributes["input_data"])
        )

        return (
            is_Process and not validation_matches_input
        )  # (not no_sanitization or not validation_matches_input)


class BSIRuleCollection(DataflowDiagramRuleCollection):
    tags = {"bsi_rules"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.name = _("BSI rule collection")

    node_rules = [
        HashedPasswordsNodeRule,
        EncryptionOfConfidentialDataNodeRule,
        AuthenticationProtocolNodeRule,
        MFANodeRule,
        MFAHighSecurityNodeRule,
        PermissionNodeRule,
        InputValidationNodeRule,
        LoggingDataNodeRule,
    ]
    edge_rules = [
        UntrustworthyDataflowEdgeRule,
        ConfidentialDataflowEdgeRule,
        SecureHTTPConfigEdgeRule,
        IntegrityOfExternalEntitiesEdgeRule,
        UseOfProxiesEdgeRule,
    ]


__all__ = ["BSIRuleCollection"]

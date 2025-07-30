# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

from flowstrider import settings
from flowstrider.rules.common_rules import (
    DataflowDiagramRuleCollection,
    EdgeTagRule,
    NodeTagRule,
)


class GenericSpoofingNodeRule(NodeTagRule):
    node_tags_any = {"STRIDE:Process", "STRIDE:Interactor"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Generic Spoofing Node Rule")
        cls.short_description = _("Generic Spoofing Threat")
        cls.long_description = _(
            "Spoofing refers to the attack where an adversary gains unauthorized "
            "access to data or a system by falsifying their identity and pretending "
            "to be a trusted contact. The threat violates the property of "
            "authenticity."
        )


class GenericTamperingNodeRule(NodeTagRule):
    node_tags_any = {"STRIDE:DataStore", "STRIDE:Process"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Generic Tampering Node Rule")
        cls.short_description = _("Generic Tampering Threat")
        cls.long_description = _(
            "Tampering refers to the unlawful modification of data or systems so that "
            "they pose a danger to normal users. The threat violates the property of "
            "integrity."
        )


class GenericTamperingDataflowRule(EdgeTagRule):
    edge_tags_any = {"STRIDE:Dataflow"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Generic Tampering Dataflow Rule")
        cls.short_description = _("Generic Tampering Threat")
        cls.long_description = _(
            "Tampering refers to the unlawful modification of data or systems so that "
            "they pose a danger to normal users. The threat violates the property of "
            "integrity."
        )


class GenericRepudiationNodeRule(NodeTagRule):
    node_tags_any = {"STRIDE:Process", "STRIDE:Interactor"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Generic Repudiation Node Rule")
        cls.short_description = _("Generic Repudiation Threat")
        cls.long_description = _(
            "Repudiation refers to the threat where a contact does not claim "
            "responsibility and rejects the confession of a certain act like modifying "
            "data. The threat violates the property of non-repudiability."
        )


class GenericInformationDisclosureNodeRule(NodeTagRule):
    node_tags_any = {"STRIDE:DataStore", "STRIDE:Process"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Generic Information Disclosure Node Rule")
        cls.short_description = _("Generic Information Disclosure Threat")
        cls.long_description = _(
            "Information disclosure refers to the threat where data leaves the "
            "confines of its supposed authority scope and unauthorized contacts can "
            "access it. The threat violates the property of confidentiality."
        )


class GenericInformationDisclosureDataflowRule(EdgeTagRule):
    edge_tags_any = {"STRIDE:Dataflow"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Generic Information Disclosure Dataflow Rule")
        cls.short_description = _("Generic Information Disclosure Threat")
        cls.long_description = _(
            "Information disclosure refers to the threat where data leaves the "
            "confines of its supposed authority scope and unauthorized contacts can "
            "access it. The threat violates the property of confidentiality."
        )


class GenericDenialOfServiceNodeRule(NodeTagRule):
    node_tags_any = {"STRIDE:DataStore", "STRIDE:Process"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Generic Denial of Service Node Rule")
        cls.short_description = _("Generic Denial of Service Threat")
        cls.long_description = _(
            "Denial of service refers to the threat of maliciously overloading the "
            "resources of the system with the intent of harming usability and making "
            "services unavailable. The thrat violates the property of availability."
        )


class GenericDenialOfServiceDataflowRule(EdgeTagRule):
    edge_tags_any = {"STRIDE:Dataflow"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Generic Denial of Service Dataflow Rule")
        cls.short_description = _("Generic Denial of Service Threat")
        cls.long_description = _(
            "Denial of service refers to the threat of maliciously overloading the "
            "resources of the system with the intent of harming usability and making "
            "services unavailable. The thrat violates the property of availability."
        )


class GenericElevationOfPrivilegeNodeRule(NodeTagRule):
    node_tags_any = {"STRIDE:Process"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.display_name = _("Generic Elevation of Privilege Node Rule")
        cls.short_description = _("Generic Elevation of Privilege Threat")
        cls.long_description = _(
            "Elevation of privilege refers to the threat where an adversary can gain "
            "unlawful authorization to systems or data by escalating their level of "
            "privileges by exploiting bugs or gaps in security. The threat violates "
            "the property of authorization."
        )


class GenericSTRIDERuleCollection(DataflowDiagramRuleCollection):
    tags = {"stride"}

    @classmethod
    def init_texts(cls):
        _ = settings.lang_out.gettext
        cls.name = _("STRIDE rule collection")

    node_rules = [
        GenericSpoofingNodeRule,
        GenericTamperingNodeRule,
        GenericRepudiationNodeRule,
        GenericInformationDisclosureNodeRule,
        GenericDenialOfServiceNodeRule,
        GenericElevationOfPrivilegeNodeRule,
    ]
    edge_rules = [
        GenericTamperingDataflowRule,
        GenericInformationDisclosureDataflowRule,
        GenericDenialOfServiceDataflowRule,
    ]


__all__ = ["GenericSTRIDERuleCollection"]

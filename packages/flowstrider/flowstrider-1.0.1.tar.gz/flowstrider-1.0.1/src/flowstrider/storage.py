# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import typing
from dataclasses import dataclass

import marshmallow_dataclass

from flowstrider import settings
from flowstrider.converters.dfd_to_dot_converter import wrap_text as wrap
from flowstrider.models import dataflowdiagram, threat, threat_management
from flowstrider.rules import collections


@dataclass
class Container:
    dfd: dataflowdiagram.DataflowDiagram


ThreatList = typing.List[threat.Threat]


@dataclass
class ThreatContainer:
    threats: ThreatList


@dataclass
class ThreatManagementContainer:
    threat_management_data: threat_management.ThreatManagementDatabase


container_schema = marshmallow_dataclass.class_schema(Container)()
threat_container_schema = marshmallow_dataclass.class_schema(ThreatContainer)()
threat_management_container_schema = marshmallow_dataclass.class_schema(
    ThreatManagementContainer
)()


@dataclass
class WarningsCounter:
    count = 0

    @classmethod
    def add_warning(cls):
        cls.count += 1


DFD_CORRECT_ELEMENT_TAGS = [
    "STRIDE:Interactor",
    "STRIDE:DataStore",
    "STRIDE:Process",
    "STRIDE:Dataflow",
    "STRIDE:TrustBoundary",
]
DFD_CORRECT_RULE_TAGS = []
for collection in collections.all_collections:
    for tag in collection.tags:
        DFD_CORRECT_RULE_TAGS.append(tag)


def deserialize_dfd(serialized_dfd: str) -> dataflowdiagram.DataflowDiagram:
    """Convert a dfd given as string to a DataflowDiagram class"""
    check_dfd(serialized_dfd)

    dfd: dataflowdiagram.DataflowDiagram = container_schema.loads(serialized_dfd).dfd

    if not isinstance(dfd, dataflowdiagram.DataflowDiagram):
        raise ValueError("Could not deserialize DataflowDiagram: wrong type!")

    return dfd


def check_dfd(serialized_dfd: str) -> None:
    """Check a dfd given as string for errors and print warnings"""

    from flowstrider.rules import attributes_dict

    def print_warning(warning_key: str, line: int, **str_substitutes: str):
        """Function used to print warnings to cmd"""
        global _
        _ = settings.lang_sys.gettext
        warnings = {
            "id_reuse": _('id "{id}" was used for more than one object in the dfd.'),
            "name_id_mismatch": _(
                'element name "{name}" does not correspond with its id "{id}".'
            ),
            "invalid_tag": _('tag "{tag}" is not a valid tag.'),
            "missing_reference": _('id "{id}" was referenced but not found.'),
            "wrong_attribute": _('attribute "{att}" is not a valid attribute.'),
            "wrong_tag_for_attribute": _(
                'attribute "{att}" is not applicable for an element of type {tag}.'
            ),
        }
        print(
            settings.C_WARNING
            + wrap(
                _("Warning: ")
                + _(warnings[warning_key]).format(**str_substitutes)
                + " (JSON "
                + _("line")
                + " "
                + str(line)
                + ")"
            )
            + settings.C_DEFAULT
        )
        WarningsCounter.add_warning()

    # Checking for errors in the JSON:
    # Check for multiple uses of the same id
    unique_ids = []
    lines = serialized_dfd.split("\n")
    for i in range(len(lines)):
        line = lines[i]
        # For each occurence of an id in the JSON
        if '"id":' in line:
            id_check = line[line.find(":") + 1 :]
            id_check = id_check[id_check.find('"') + 1 :]
            id_check = id_check[: id_check.find('"')]
            # Add to unique ids or throw error if already inside
            if id_check in unique_ids:
                print_warning("id_reuse", i + 1, id=id_check)
            else:
                unique_ids.append(id_check)

            # Check, that id corresponds with its node name in JSON
            name_check = lines[i - 1]
            name_check = name_check[name_check.find('"') + 1 :]
            name_check = name_check[: name_check.find('"')]
            if id_check != name_check and name_check != "dfd":
                print_warning("name_id_mismatch", i, name=name_check, id=id_check)

    current_tags = []
    for i in range(len(lines)):
        line = lines[i]
        # Check, that tags are correct
        if '"tags":' in line:
            current_tags = []
            # Tags in one line
            if "]" in line:
                tag_check_list = line[line.find("[") + 1 : line.find("]")].split(",")
                for tag_check in tag_check_list:
                    tag_check = tag_check.replace('"', "").strip()
                    if len(tag_check) == 0:
                        continue
                    current_tags.append(tag_check)
                    if (
                        tag_check not in DFD_CORRECT_ELEMENT_TAGS
                        and tag_check not in DFD_CORRECT_RULE_TAGS
                    ):
                        print_warning("invalid_tag", i + 1, tag=tag_check)
            else:
                # Tags in mutiple lines
                j = i + 1
                while "]" not in lines[j]:
                    tag_check = lines[j][lines[j].find('"') + 1 :]
                    tag_check = tag_check[: tag_check.find('"')]
                    if len(tag_check) == 0:
                        j += 1
                        continue
                    current_tags.append(tag_check)
                    if (
                        tag_check not in DFD_CORRECT_ELEMENT_TAGS
                        and tag_check not in DFD_CORRECT_RULE_TAGS
                    ):
                        print_warning("invalid_tag", j + 1, tag=tag_check)
                    j += 1

        # Check for references to non existing ids
        # Edges referencing source and sink
        if '"source_id":' in line or '"sink_id":' in line:
            id_check = line[line.find(":") + 1 :]
            id_check = id_check[id_check.find('"') + 1 :]
            id_check = id_check[: id_check.find('"')]
            if id_check not in unique_ids:
                print_warning("missing_reference", i + 1, id=id_check)
        # Clusters referencing nodes inside
        elif '"node_ids":' in line:
            # Nodes in one line
            if "]" in line:
                id_check_list = line[line.find("[") + 1 : line.find("]")].split(",")
                for id_check in id_check_list:
                    id_check = id_check.replace('"', "").strip()
                    if id_check not in unique_ids:
                        print_warning("missing_reference", i + 1, id=id_check)
            # Nodes in multiple lines
            else:
                j = i + 1
                while "]" not in lines[j]:
                    id_check = lines[j][lines[j].find('"') + 1 :]
                    id_check = id_check[: id_check.find('"')]
                    if id_check not in unique_ids:
                        print_warning("missing_reference", j + 1, id=id_check)
                    j += 1

        # Check for false attribute usage
        if '"attributes":' in line:
            # Attributes in one line
            if "}" in line:
                att_check_list = line[line.find("{") + 1 : line.find("}")].split(",")
                for att_check in att_check_list:
                    att_key = att_check.split(":")[0].replace('"', "").strip()
                    if not att_key:
                        continue
                    if att_key not in attributes_dict.attributes:
                        print_warning("wrong_attribute", i + 1, att=att_key)
                        continue
                    tags_match = False
                    for tag in current_tags:
                        tag = tag[tag.find(":") + 1 :]
                        for correct_tag in attributes_dict.attributes[att_key][2]:
                            if tag in correct_tag:
                                tags_match = True
                    if not tags_match:
                        print_warning(
                            "wrong_tag_for_attribute",
                            i + 1,
                            att=att_key,
                            tag=", ".join(current_tags),
                        )
            # Attributes in multiple lines
            else:
                j = i + 1
                while "}" not in lines[j]:
                    att_check = lines[j].replace(",", "")
                    # Check if attribute is in line (there could also be just a value)
                    if ":" not in lines[j]:
                        j += 1
                        continue
                    att_key = att_check.split(":")[0].replace('"', "").strip()
                    if att_key not in attributes_dict.attributes:
                        print_warning("wrong_attribute", j + 1, att=att_key)
                        j += 1
                        continue
                    tags_match = False
                    for tag in current_tags:
                        tag = tag[tag.find(":") + 1 :]
                        for correct_tag in attributes_dict.attributes[att_key][2]:
                            if tag in correct_tag:
                                tags_match = True
                    if not tags_match:
                        print_warning(
                            "wrong_tag_for_attribute",
                            j + 1,
                            att=att_key,
                            tag=", ".join(current_tags),
                        )
                    j += 1


def undictify_dfd(dictified_dfd: dict) -> dataflowdiagram.DataflowDiagram:
    dfd: dataflowdiagram.DataflowDiagram = container_schema.load(dictified_dfd).dfd

    if not isinstance(dfd, dataflowdiagram.DataflowDiagram):
        raise ValueError("Could not deserialize DataflowDiagram: wrong type!")

    return dfd


def serialize_dfd(dfd: dataflowdiagram.DataflowDiagram) -> str:
    serialized_dfd: str = container_schema.dumps(Container(dfd), indent=2)

    return serialized_dfd


def dictify_dfd(dfd: dataflowdiagram.DataflowDiagram) -> str:
    dictified_dfd: dict = container_schema.dump(Container(dfd))

    return dictified_dfd


def deserialize_threats(serialized_threats: str) -> ThreatList:
    threats: ThreatList = threat_container_schema.loads(serialized_threats).dfd

    if not isinstance(threats, ThreatList):
        raise ValueError("Could not deserialize Threats: wrong type!")

    return threats


def undictify_threats(dictified_threats: dict) -> ThreatList:
    threats: ThreatList = threat_container_schema.load(dictified_threats).dfd

    if not isinstance(threats, ThreatList):
        raise ValueError("Could not deserialize Threats: wrong type!")

    return threats


def serialize_threats(threats: ThreatList) -> str:
    serialized_threats: str = threat_container_schema.dumps(
        ThreatContainer(threats), indent=2
    )

    return serialized_threats


def dictify_threats(threats: ThreatList) -> str:
    dictified_threats: dict = threat_container_schema.dump(ThreatContainer(threats))

    return dictified_threats


def deserialize_threat_management_database(
    serialized_threat_management_database: str,
) -> threat_management.ThreatManagementDatabase:
    threat_management_database: threat_management.ThreatManagementDatabase = (
        threat_management_container_schema.loads(
            serialized_threat_management_database
        ).threat_management_data
    )

    if not isinstance(
        threat_management_database, threat_management.ThreatManagementDatabase
    ):
        raise ValueError("Could not deserialize ThreatManagementDatabase: wrong type!")

    return threat_management_database


def undictify_threat_management_database(
    dictified_threat_management_database: dict,
) -> threat_management.ThreatManagementDatabase:
    threat_management_database: threat_management.ThreatManagementDatabase = (
        threat_management_container_schema.load(
            dictified_threat_management_database
        ).threat_management_data
    )

    if not isinstance(
        threat_management_database, threat_management.ThreatManagementDatabase
    ):
        raise ValueError("Could not deserialize ThreatManagementDatabase: wrong type!")

    return threat_management_database


def serialize_threat_management_database(
    threat_management_database: threat_management.ThreatManagementDatabase,
) -> str:
    serialized_threat_management_database: str = (
        threat_management_container_schema.dumps(
            ThreatManagementContainer(threat_management_database), indent=2
        )
    )

    return serialized_threat_management_database


def dictify_threat_management_database(
    threat_management_database: threat_management.ThreatManagementDatabase,
) -> str:
    dictified_threat_management_database: dict = (
        threat_management_container_schema.dump(
            ThreatManagementContainer(threat_management_database)
        )
    )

    return dictified_threat_management_database


__all__ = [
    "deserialize_dfd",
    "serialize_dfd",
    "undictify_dfd",
    "dictify_dfd",
    "deserialize_threats",
    "serialize_threats",
    "undictify_threats",
    "dictify_threats",
    "deserialize_threat_management_database",
    "serialize_threat_management_database",
    "undictify_threat_management_database",
    "dictify_threat_management_database",
]

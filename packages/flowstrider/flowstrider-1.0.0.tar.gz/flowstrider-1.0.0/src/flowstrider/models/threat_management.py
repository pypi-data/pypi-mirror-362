# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import typing
from dataclasses import dataclass, field
from enum import Enum, auto

from flowstrider.models import dataflowdiagram, threat


class ThreatManagementState(Enum):
    # These imply future work
    Undecided = auto()
    Delegate = auto()
    Mitigate = auto()
    Avoid = auto()

    # These are final
    Accept = auto()
    Delegated = auto()
    Mitigated = auto()

    def __format__(self, _):
        return f"{self.name}"


@dataclass(frozen=True)
class ThreatManagementItem:
    management_state: ThreatManagementState = ThreatManagementState.Undecided
    explanation: str = ""


ThreatManagementDict = typing.Dict[str, ThreatManagementItem]


@dataclass
class ThreatManagementDatabase:
    per_threat_information: ThreatManagementDict = field(default_factory=dict)

    def update(
        self, threats: typing.List[threat.Threat], dfd: dataflowdiagram.DataflowDiagram
    ):
        # Add new threats to dictionary
        for threat_ in threats:
            threat_uid = threat_.uid(dfd)
            if threat_uid not in self.per_threat_information.keys():
                threat_management_item = ThreatManagementItem()
                self.per_threat_information[threat_uid] = threat_management_item

        # Delete old threat management entries for which no threat exists anymore
        # ...(either because it was resolved or because elements were renamed)
        staged_deletions = []
        for threat_uid in self.per_threat_information.keys():
            found = False
            for threat_ in threats:
                if threat_.uid(dfd) == threat_uid:
                    found = True
                    break
            if not found:
                staged_deletions.append(threat_uid)

        for threat_uid in staged_deletions:
            # TODO: mark management threats as "old"/"depricated"/"resolved"
            # ...instead of deleting?
            del self.per_threat_information[threat_uid]

    def get(self, threat_: threat.Threat, dfd: dataflowdiagram.DataflowDiagram):
        return self.per_threat_information[threat_.uid(dfd)]

    def should_fail(
        self,
        threats: typing.List[threat.Threat],
        dfd: dataflowdiagram.DataflowDiagram,
        level: str,
    ) -> typing.List[threat.Threat]:
        return_value = list()
        if level == "off":
            return return_value

        for threat_ in threats:
            threat_management_item = self.get(threat_, dfd)

            # Levels: "off", "undecided", "todo", "all"
            match threat_management_item.management_state:
                case ThreatManagementState.Undecided:
                    if level in ("undecided", "todo", "all"):
                        return_value.append(threat_)
                case (
                    ThreatManagementState.Delegate
                    | ThreatManagementState.Mitigate
                    | ThreatManagementState.Avoid
                ):
                    if level in ("todo", "all"):
                        return_value.append(threat_)
                case (
                    ThreatManagementState.Accept
                    | ThreatManagementState.Delegated
                    | ThreatManagementState.Mitigated
                ):
                    if level in ("all"):
                        return_value.append(threat_)

        return return_value

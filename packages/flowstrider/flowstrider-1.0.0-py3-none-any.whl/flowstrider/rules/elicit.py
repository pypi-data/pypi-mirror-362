# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import typing

from flowstrider import settings
from flowstrider.models import dataflowdiagram, threat
from flowstrider.rules import collections, common_rules


def elicit(dfd: dataflowdiagram.DataflowDiagram) -> typing.List[threat.Threat]:
    global _
    _ = settings.lang_sys.gettext
    print(_("Eliciting threats for model {id}").format(id=dfd.id))

    active_collections: typing.List[common_rules.DataflowDiagramRuleCollection] = (
        collections.all_collections
    )
    threats: typing.List[threat.Threat] = []

    for rule_collection in active_collections:
        threats += rule_collection.evaluate(dfd)

    return threats

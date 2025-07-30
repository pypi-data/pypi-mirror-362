# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

from .builtin.bsi_rules import BSIRuleCollection
from .builtin.stride_rules import GenericSTRIDERuleCollection

# Don't change order of existing collections!
all_collections = [BSIRuleCollection, GenericSTRIDERuleCollection]

__all__ = ["all_collections"]

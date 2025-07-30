# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

from flowstrider.rules.common_rules import meet_any_requirement


def test_meet_any_requirement():
    requirements = ["req1", "req2", "req3"]
    assert meet_any_requirement("req1", requirements)
    assert meet_any_requirement("Req2", requirements)
    assert meet_any_requirement("Req_3", requirements)
    assert meet_any_requirement(" req 1 ", requirements)
    assert meet_any_requirement("reQ-2 ", requirements)
    assert not meet_any_requirement("req4 ", requirements)
    assert not meet_any_requirement("", requirements)
    assert not meet_any_requirement(None, requirements)

    requirements = []
    assert meet_any_requirement("req1", requirements)
    assert meet_any_requirement("", requirements)
    assert meet_any_requirement(None, requirements)

    requirements = [True]
    assert meet_any_requirement(True, requirements)
    assert not meet_any_requirement(False, requirements)

    requirements = [True, False]
    assert meet_any_requirement(True, requirements)
    assert meet_any_requirement(False, requirements)

    requirements = [True, False]
    assert meet_any_requirement("True", requirements)
    assert meet_any_requirement(" true", requirements)
    assert not meet_any_requirement("Something", requirements)

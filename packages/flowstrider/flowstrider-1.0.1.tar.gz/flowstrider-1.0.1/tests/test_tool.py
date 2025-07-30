# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import pathlib
import re
import sys
from unittest.mock import patch

from openpyxl import load_workbook

from flowstrider import settings
from flowstrider.models.dataflowdiagram import DataflowDiagram
from flowstrider.models.threat import Threat
from flowstrider.models.threat_management import (
    ThreatManagementDatabase,
    ThreatManagementItem,
    ThreatManagementState,
)
from flowstrider.rules import attributes_dict
from flowstrider.rules.builtin.bsi_rules import bsi_rule_collection
from flowstrider.tool import elicit_cmd, main, metadata_cmd, print_threats, update_cmd

__location__ = os.path.dirname(__file__)


def test_tool_init():
    settings.init_localization("en", "sys")
    settings.init_localization("en", "out")


# Smoke test
# Patch replaces the Graphviz source because there is a problem with rendering
# ... dfds in CI
@patch("flowstrider.converters.dfd_to_dot_converter.Source")
def test_smoke(mock_source, capsys):
    example_smoke_test_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_example_smoke_test.json"
    )
    management_file_path: pathlib.Path = os.path.join(
        __location__, "resources/threat_management_smoke_test.json"
    )
    ground_truth_path: pathlib.Path = os.path.join(
        __location__, "resources/ground_truth_smoke_test.txt"
    )
    try:
        sys.argv = [
            "tool.py",
            "elicit",
            example_smoke_test_path,
            "--output",
            "pdf",
            "--management-path",
            str(management_file_path),
        ]
        main()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr().out
    captured_cleaned = re.sub(r"\s+", "", captured)

    with open(ground_truth_path, "r", encoding="utf-8") as f:
        expected_lines = [re.sub(r"\s+", "", line) for line in f.readlines()]

    for expected_line in expected_lines:
        assert (
            expected_line in captured_cleaned
        ), f"Expected line not found:\n{expected_line}"


# Patch replaces the Graphviz source because there is a problem with rendering
# ... dfds in CI
@patch("flowstrider.converters.dfd_to_dot_converter.Source")
def test_localization(mock_source, capsys):
    example_smoke_test_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_example_smoke_test.json"
    )
    ground_truth_path: pathlib.Path = os.path.join(
        __location__, "resources/ground_truth_smoke_test_de.txt"
    )
    try:
        sys.argv = [
            "tool.py",
            "elicit",
            example_smoke_test_path,
            "--output",
            "pdf",
            "--out-lang",
            "de",
        ]
        main()
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr().out
    captured_cleaned = re.sub(r"\s+", "", captured)

    with open(ground_truth_path, "r", encoding="utf-8") as f:
        expected_lines = [re.sub(r"\s+", "", line) for line in f.readlines()]

    for expected_line in expected_lines:
        assert (
            expected_line in captured_cleaned
        ), f"Expected line not found:\n{expected_line}"


# Patch replaces the Graphviz source because there is a problem with rendering
# ... dfds in CI
@patch("flowstrider.converters.dfd_to_dot_converter.Source")
def test_elicit_cmd(mock_source, capsys):
    example_1_path: pathlib.Path = (
        pathlib.Path(__location__) / "resources/dfd_example-1.json"
    )

    example_1_json_error_path: pathlib.Path = (
        pathlib.Path(__location__) / "resources/dfd_example-1_w_json_error.json"
    )

    example_1_mgmt_accept_path: pathlib.Path = (
        pathlib.Path(__location__) / "resources/dfd_example-1-mgmt-accept.json"
    )

    example_1_mgmt_undecided_path: pathlib.Path = (
        pathlib.Path(__location__) / "resources/dfd_example-1-mgmt-undecided.json"
    )

    example_2_path: pathlib.Path = (
        pathlib.Path(__location__) / "resources/dfd_example-2.json"
    )

    example_3_path: pathlib.Path = (
        pathlib.Path(__location__) / "resources/dfd_example-3.json"
    )

    wrong_path: pathlib.Path = (
        pathlib.Path(__location__) / "resources/dfd_shouldnt_exist.json"
    )

    wrong_directory_path: pathlib.Path = pathlib.Path(__location__) / "resources/"

    # Reset a rule value to see if its being properly set in the elicit call
    bsi_rule_collection.AuthenticationProtocolNodeRule.attribute_names = []

    assert elicit_cmd(example_1_path, None, "pdf", "off", "en") == 0
    captured = capsys.readouterr()
    assert "saved as PDF" in captured.out
    assert "output/Example-1_threats.pdf" in captured.out
    assert (
        "Diagram saved as PNG,\nSVG and Graphviz to the output/visualization folder."
        in captured.out
    )

    assert elicit_cmd(example_1_path, None, "pdf", "all", "en") == 1
    assert (
        elicit_cmd(example_1_path, example_1_mgmt_undecided_path, "pdf", "all", "en")
        == 1
    )
    assert (
        elicit_cmd(example_1_path, example_1_mgmt_undecided_path, "pdf", "todo", "en")
        == 1
    )
    assert (
        elicit_cmd(
            example_1_path, example_1_mgmt_undecided_path, "pdf", "undecided", "en"
        )
        == 1
    )
    assert (
        elicit_cmd(example_1_path, example_1_mgmt_undecided_path, "pdf", "off", "en")
        == 0
    )
    assert (
        elicit_cmd(example_1_path, example_1_mgmt_accept_path, "pdf", "all", "en") == 1
    )
    assert (
        elicit_cmd(example_1_path, example_1_mgmt_accept_path, "pdf", "todo", "en") == 0
    )
    assert (
        elicit_cmd(example_1_path, example_1_mgmt_accept_path, "pdf", "undecided", "en")
        == 0
    )
    assert (
        elicit_cmd(example_1_path, example_1_mgmt_accept_path, "pdf", "off", "en") == 0
    )

    assert elicit_cmd(example_2_path, None, "", "off", "en") == 0
    captured = capsys.readouterr()
    assert "No or wrong output format specified. Threats were not saved" in captured.out

    assert elicit_cmd(example_2_path, None, "", "off", "de") == 0
    captured = capsys.readouterr()
    assert "Bedrohungsquelle: Hashing von Passwörtern" in captured.out

    assert elicit_cmd(example_3_path, None, "", "off", "en") == 0
    captured = capsys.readouterr()
    assert "no threats found" in captured.out
    assert "No or wrong output format specified. Threats were not saved" in captured.out

    assert elicit_cmd(example_3_path, None, "off", "off", "en") == 0
    captured = capsys.readouterr()
    assert "no threats found" in captured.out

    assert elicit_cmd(example_3_path, None, "pdf", "all", "en") == 0

    assert elicit_cmd(example_1_path, None, "wrong_output_format", "off", "en") == 0
    captured = capsys.readouterr()
    assert "No or wrong output format specified. Threats were not saved" in captured.out

    assert elicit_cmd(wrong_path, None, "pdf", "off", "en") == 1
    captured = capsys.readouterr()
    assert "not found" in captured.out

    assert elicit_cmd(wrong_directory_path, None, "pdf", "off", "en") == 1
    captured = capsys.readouterr()
    assert ("is a directory" in captured.out) or (
        "No permission to access" in captured.out
    )

    assert elicit_cmd(example_1_json_error_path, None, "pdf", "off", "en") == 1
    captured = capsys.readouterr()
    assert "json error" in captured.out


def test_print_threats(capsys):
    test_threats = [
        Threat(
            source="Test source",
            source_internal="Test source",
            location="Test location",
            short_description="This is a short description",
            long_description="This is a long description",
            mitigation_options=["Test mitigation option 1", "Test mitigation option 2"],
            requirement="Test requirement",
            req_status="Test requirement status",
        ),
        Threat(
            source="Another test source",
            source_internal="Another test source",
            location="Another test location",
            short_description="This is another short description",
            long_description="This is another long description",
            mitigation_options=[
                "Another test mitigation option 1",
                "Another test mitigation option 2",
            ],
            requirement="Another test requirement",
            req_status="Another test requirement status",
        ),
    ]
    test_dfd = DataflowDiagram(
        name="Test DFD",
        id="d1",
        nodes={"node1"},
        edges={"edge1"},
        clusters={},
    )
    threat_management_database = ThreatManagementDatabase(
        per_threat_information={
            test_threats[1].uid(test_dfd): ThreatManagementItem(
                ThreatManagementState.Accept, "Small risk"
            )
        }
    )

    threat_management_database.update(test_threats, test_dfd)

    assert print_threats(test_dfd, test_threats, threat_management_database) == 0
    captured = capsys.readouterr()
    expected_outputs = [
        "#1 Threat source: Test source",
        "Description: This is a short description",
        "Long Description: This is a long description",
        "Mitigation Option: Test mitigation option 1",
        "Mitigation Option: Test mitigation option 2",
        "Requirement: Test requirement",
        "Locations:",
        "Test location",
        "Test requirement status",
        "Management State: Undecided",
        "Management Explanation: ",
        "#2 Threat source: Another test source",
        "Description: This is another short description",
        "Long Description: This is another long description",
        "Mitigation Option: Another test mitigation option 1",
        "Mitigation Option: Another test mitigation option 2",
        "Requirement: Another test requirement",
        "Locations:",
        "Another test location",
        "Another test requirement status",
        "Management State: Accept",
        "Management Explanation: Small risk",
    ]
    for output in expected_outputs:
        assert output in captured.out


def test_metadata_cmd(capsys):
    example_1_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_example-1.json"
    )
    example_2_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_example-2.json"
    )
    example_3_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_example-3.json"
    )
    wrong_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_shouldnt_exist.json"
    )
    wrong_directory_path: pathlib.Path = os.path.join(__location__, "resources/")

    assert metadata_cmd(example_1_path, "en") == 0
    captured = capsys.readouterr()
    assert "Metadata file of diagram 'Example-1' saved to" in captured.out
    assert "output/Example-1_metadata_overview.xlsx" in captured.out
    assert os.path.exists(
        os.path.join(__location__, "../output/Example-1_metadata_overview.xlsx")
    )

    assert metadata_cmd(example_2_path, "en") == 0
    captured = capsys.readouterr()
    assert "Metadata file of diagram 'Example-2' saved to" in captured.out
    assert "output/Example-2_metadata_overview.xlsx" in captured.out
    assert os.path.exists(
        os.path.join(__location__, "../output/Example-2_metadata_overview.xlsx")
    )

    assert metadata_cmd(example_3_path, "en") == 0
    captured = capsys.readouterr()
    assert "Metadata file of diagram 'Example-3' saved to" in captured.out
    assert "output/Example-3_metadata_overview.xlsx" in captured.out
    assert os.path.exists(
        os.path.join(__location__, "../output/Example-3_metadata_overview.xlsx")
    )

    assert metadata_cmd(wrong_path, "en") == 1
    captured = capsys.readouterr()
    assert "not found" in captured.out

    assert metadata_cmd(wrong_directory_path, "en") == 1
    captured = capsys.readouterr()
    assert ("is a directory" in captured.out) or (
        "No permission to access" in captured.out
    )


def test_update_cmd(capsys):
    example_1_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_example-1.json"
    )
    example_2_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_example-2.json"
    )
    example_3_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_example-3.json"
    )
    example_1_metadata_path: pathlib.Path = os.path.join(
        __location__, "resources/Example-1_metadata_overview.xlsx"
    )
    example_2_metadata_path: pathlib.Path = os.path.join(
        __location__, "resources/Example-2_metadata_overview.xlsx"
    )
    example_3_metadata_path: pathlib.Path = os.path.join(
        __location__, "resources/Example-3_metadata_overview.xlsx"
    )
    wrong_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_shouldnt_exist.json"
    )
    wrong_metadata_path: pathlib.Path = os.path.join(
        __location__, "resources/metadata_shouldnt_exist.xlsx"
    )
    wrong_directory_path: pathlib.Path = os.path.join(__location__, "resources/")

    assert update_cmd(example_1_path, example_1_metadata_path) == 0
    captured = capsys.readouterr()
    assert "Successfully updated diagram 'Example-1'" in captured.out

    assert update_cmd(example_2_path, example_2_metadata_path) == 0
    captured = capsys.readouterr()
    assert "Successfully updated diagram 'Example-2'" in captured.out

    assert update_cmd(example_3_path, example_3_metadata_path) == 0
    captured = capsys.readouterr()
    assert "Successfully updated diagram 'Example-3'" in captured.out

    assert update_cmd(wrong_path, example_1_metadata_path) == 1
    captured = capsys.readouterr()
    assert f"'{wrong_path}' not found" in captured.out

    assert update_cmd(wrong_directory_path, example_1_metadata_path) == 1
    captured = capsys.readouterr()
    assert (f"'{wrong_directory_path}' is a directory" in captured.out) or (
        f"No permission to access '{wrong_directory_path}'" in captured.out
    )

    assert update_cmd(example_1_path, wrong_metadata_path) == 1
    captured = capsys.readouterr()
    assert f"'{wrong_metadata_path}' not found" in captured.out

    assert update_cmd(example_1_path, wrong_path) == 1
    captured = capsys.readouterr()
    assert f"'{wrong_path}' is of wrong file format" in captured.out

    assert update_cmd(example_1_path, wrong_directory_path) == 1
    captured = capsys.readouterr()
    assert f"'{wrong_directory_path}' is of wrong file format" in captured.out


# Patch replaces the Graphviz source because there is a problem with rendering
# ... dfds in CI
@patch("flowstrider.converters.dfd_to_dot_converter.Source")
def test_metadata_update_elicit(mock_source, capsys):
    example_4_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_example-4.json"
    )
    example_4_default_path: pathlib.Path = os.path.join(
        __location__, "resources/dfd_example-4-default.json"
    )
    example_4_metadata_path: pathlib.Path = os.path.join(
        __location__, "../output/Example-4_metadata_overview.xlsx"
    )

    # Copy default values of json into working json (because the working json will be
    # ...modified during the test)
    os.remove(example_4_path)
    with open(example_4_default_path, "r") as read_file, open(
        example_4_path, "a"
    ) as write_file:
        for line in read_file:
            write_file.write(line)

    # Elicit JSON
    assert elicit_cmd(example_4_path, None, "off", "off", "en") == 0
    captured = capsys.readouterr().out
    assert (
        ""
        + "               Locations:\n"
        + "                          User data: Application -> Database:\n"
        + "\033[31m                            Attribute missing: Transport "
        + "protocol\033[0m\n"
        + "                          Management State: Undecided\n"
        + "\n"
        + "                          Images: Database -> Bob:\n"
        + "\033[31m                            Attribute missing: Transport "
        "protocol\033[0m\n"
        + "                          Management State: Undecided\n"
        + "\n"
        + "\n"
    ) in captured

    # Generate metadata from JSON
    assert metadata_cmd(example_4_path, "en") == 0

    workbook = load_workbook(filename=example_4_metadata_path)
    sheet = workbook.active

    # Check headers
    all_metadata_keys = sorted([key for key, _ in attributes_dict.attributes.items()])
    all_display_names = []
    for key in all_metadata_keys:
        all_display_names.append(attributes_dict.attributes[key][0])
    headers = [cell.value for cell in sheet[1]]

    found_1 = False
    for i in range(3, len(headers)):
        assert headers[i] == all_display_names[i - 3]

        # Check entries written from JSON file
        if headers[i] == "Transport protocol":
            assert sheet[9][i].value == "TLS 1.3"
            found_1 = True
    assert found_1

    # Modify metadata (simulate user entering values)
    for i in range(3, len(headers)):
        if headers[i] == "Transport protocol":
            sheet[10][i].value = "tls1.3"
            sheet[11][i].value = "nothing"
    workbook.save(example_4_metadata_path)

    # Update JSON from metadata
    assert update_cmd(example_4_path, example_4_metadata_path) == 0

    # Elicit JSON again and check if entered metadata changed the results
    assert elicit_cmd(example_4_path, None, "off", "off", "en") == 0
    captured = capsys.readouterr().out
    assert (
        ""
        + "               Locations:\n"
        + "                          Images: Database -> Bob:\n"
        + "\033[31m                            Transport protocol = nothing\033[0m\n"
        + "                          Management State: Undecided\n"
        + "\n"
        + "\n"
    ) in captured

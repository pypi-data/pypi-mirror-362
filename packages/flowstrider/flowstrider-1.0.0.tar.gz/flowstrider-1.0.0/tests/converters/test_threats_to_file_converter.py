# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

from unittest import mock

import pytest

from flowstrider import settings
from flowstrider.converters.threats_to_file_converter import PDF, create_threats_pdf
from flowstrider.models import threat_management


def test_get_string_line_count():
    pdf = PDF()
    pdf.set_font("Arial", "", 12)
    assert pdf.get_string_line_count(" ", 19) == 1
    assert pdf.get_string_line_count("Short", 19) == 1
    assert pdf.get_string_line_count("Requirement:", 19) == 2
    assert pdf.get_string_line_count("Long Description:", 19) == 3
    assert pdf.get_string_line_count("Mitigation Option:", 19) == 2
    assert pdf.get_string_line_count("Locations:", 19) == 2


@pytest.fixture
def mock_threat():
    threat_mock = mock.Mock()
    threat_mock.source = "Mocked Source"
    threat_mock.short_description = "Short description of the threat."
    threat_mock.long_description = "Detailed description of the threat."
    threat_mock.mitigation_options = ["Mitigation 1", "Mitigation 2"]
    threat_mock.location_str.return_value = "Mocked Location"
    threat_mock.requirement = "Mocked requirement"
    threat_mock.req_status = "Mocked requirement status"
    return threat_mock


@pytest.fixture
def mock_dfd():
    dfd_mock = mock.Mock()
    dfd_mock.id = "mock_dfd_id"
    dfd_mock.tags = []
    return dfd_mock


@pytest.fixture
def mock_threat_management_database():
    threat_management_database_mock = mock.Mock()
    threat_management_database_mock.get.return_value = (
        threat_management.ThreatManagementItem()
    )
    return threat_management_database_mock


@mock.patch("flowstrider.converters.threats_to_file_converter.FPDF.output")
def test_create_threats_pdf(
    mock_output, mock_threat, mock_dfd, mock_threat_management_database
):
    settings.init_localization("en", "sys")
    settings.init_localization("en", "out")

    threats = [mock_threat]

    create_threats_pdf(threats, mock_dfd, mock_threat_management_database)

    mock_output.assert_called_once_with("output/mock_dfd_id_threats.pdf")

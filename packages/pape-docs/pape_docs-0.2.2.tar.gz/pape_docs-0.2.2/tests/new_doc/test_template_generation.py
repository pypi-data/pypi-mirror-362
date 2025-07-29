import pathlib
from unittest.mock import MagicMock, patch

import click
import pytest

# Import the actual helper function
from src.new_doc import _generate_document_content

# --- Template Generation Tests ---


@patch("pathlib.Path.exists")
@patch("pathlib.Path.open")
@patch("pape.utilities.ap_style_date_string")
@patch("tzlocal.get_localzone")
@patch("datetime.datetime")
def test_generate_document_content_simple_template(
    mock_datetime,
    mock_get_localzone,
    mock_ap_style_date,
    mock_open,
    mock_exists,
) -> None:
    """Test _generate_document_content with a simple template."""
    templates_dir = pathlib.Path("/fake/templates")
    template_type = "simple"
    doc_type = "Task"

    mock_exists.return_value = True  # Template file exists
    mock_ap_style_date.return_value = "July 6, 2025"
    mock_get_localzone.return_value = MagicMock()  # Mock timezone

    # Mock reading the template file
    mock_file = MagicMock()
    mock_file.read.return_value = (
        "<!-- date -->\n# A(n) <!-- file type -->\nContent here."
    )
    mock_open.return_value.__enter__.return_value = mock_file

    content = _generate_document_content(templates_dir, template_type, doc_type)

    # Assertions
    expected_template_path = templates_dir / f"{template_type}.md"
    mock_exists.assert_called_once_with()
    mock_open.assert_called_once_with(expected_template_path, "r", encoding="utf-8")
    mock_ap_style_date.assert_called_once()
    mock_get_localzone.assert_called_once()
    assert content == "July 6, 2025\n# A Task\nContent here."


@patch("pathlib.Path.exists")
@patch("pathlib.Path.open")
@patch("pape.utilities.ap_style_date_string")
@patch("tzlocal.get_localzone")
@patch("datetime.datetime")
def test_generate_document_content_complex_template(
    mock_datetime,
    mock_get_localzone,
    mock_ap_style_date,
    mock_open,
    mock_exists,
) -> None:
    """Test _generate_document_content with a complex template."""
    templates_dir = pathlib.Path("/fake/templates")
    template_type = "complex"
    doc_type = "ADR"

    mock_exists.return_value = True  # Template file exists
    mock_ap_style_date.return_value = "July 6, 2025"
    mock_get_localzone.return_value = MagicMock()  # Mock timezone

    # Mock reading the template file
    mock_file = MagicMock()
    mock_file.read.return_value = (
        "Date: <!-- date -->\nType: A(n) <!-- file type -->\nDetails..."
    )
    mock_open.return_value.__enter__.return_value = mock_file

    content = _generate_document_content(templates_dir, template_type, doc_type)

    # Assertions
    expected_template_path = templates_dir / f"{template_type}.md"
    mock_exists.assert_called_once_with()
    mock_open.assert_called_once_with(expected_template_path, "r", encoding="utf-8")
    mock_ap_style_date.assert_called_once()
    mock_get_localzone.assert_called_once()
    assert (
        content == "Date: July 6, 2025\nType: An ADR\nDetails..."
    )  # Check 'An' replacement


@patch("pathlib.Path.exists")
@patch("pathlib.Path.open")
@patch("pape.utilities.ap_style_date_string")
@patch("tzlocal.get_localzone")
@patch("datetime.datetime")
def test_generate_document_content_missing_tags(
    mock_datetime,
    mock_get_localzone,
    mock_ap_style_date,
    mock_open,
    mock_exists,
) -> None:
    """Test _generate_document_content handles template missing tags."""
    templates_dir = pathlib.Path("/fake/templates")
    template_type = "simple"
    doc_type = "Note"

    mock_exists.return_value = True  # Template file exists
    mock_ap_style_date.return_value = "July 6, 2025"
    mock_get_localzone.return_value = MagicMock()  # Mock timezone

    # Mock reading a template file with missing tags
    mock_file = MagicMock()
    mock_file.read.return_value = "Just some text.\nNo tags here."
    mock_open.return_value.__enter__.return_value = mock_file

    content = _generate_document_content(templates_dir, template_type, doc_type)

    # Assertions
    expected_template_path = templates_dir / f"{template_type}.md"
    mock_exists.assert_called_once_with()
    mock_open.assert_called_once_with(expected_template_path, "r", encoding="utf-8")
    # Date generation is still attempted, but the tag isn't replaced
    mock_ap_style_date.assert_called_once()
    mock_get_localzone.assert_called_once()
    assert content == "Just some text.\nNo tags here."  # Content should be unchanged


@patch("pathlib.Path.exists")
@patch("pathlib.Path.open")
@patch("pape.utilities.ap_style_date_string")
@patch("tzlocal.get_localzone")
@patch("datetime.datetime")
def test_generate_document_content_missing_template_file(
    mock_datetime,
    mock_get_localzone,
    mock_ap_style_date,
    mock_open,
    mock_exists,
) -> None:
    """Test _generate_document_content raises error if template file is missing."""
    templates_dir = pathlib.Path("/fake/templates")
    template_type = "nonexistent"
    doc_type = "Test"

    mock_exists.return_value = False  # Template file does NOT exist

    with pytest.raises(click.Abort) as excinfo:
        _generate_document_content(templates_dir, template_type, doc_type)

    # Assertions
    expected_template_path = templates_dir / f"{template_type}.md"
    mock_exists.assert_called_once_with()
    mock_open.assert_not_called()
    mock_ap_style_date.assert_not_called()
    mock_get_localzone.assert_not_called()
    assert f"Error: Template file '{expected_template_path}' not found." in str(
        excinfo.value,
    )

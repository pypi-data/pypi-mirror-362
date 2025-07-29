"""Tests for the 'new' command in the pape-docs CLI."""

import pathlib
from unittest.mock import MagicMock, patch

import click
from click.testing import CliRunner, Result

# Import the actual CLI components using the correct path
from src.new_doc import cli


# Helper to run the command using CliRunner
def run_command(args: list[str] | None = None, cli_input: str | None = None) -> Result:
    """Call the 'new' command using CliRunner."""
    runner = CliRunner()
    # The command is 'new', so we invoke the cli group with ['new'] followed by args
    return runner.invoke(
        cli,
        ["new"] + (args if args is not None else []),
        input=cli_input,
    )


# --- Regular Cases ---


# Patch internal functions that interact with the file system or prompt the user
@patch("src.new_doc._get_docs_directory")
@patch("src.new_doc._ensure_docs_directory_exists")
@patch("src.new_doc._perform_write_test")
@patch("src.new_doc._prompt_for_missing_arguments")
@patch("src.new_doc._sanitize_inputs")
@patch("src.new_doc._generate_document_content")
@patch("src.new_doc.Path.open")  # Mock file writing
@patch("src.new_doc.Path.exists")  # Mock file existence check
@patch("click.confirm")  # Mock user confirmation for overwrite
def test_regular_case_all_args_provided(
    mock_confirm: MagicMock,
    mock_exists: MagicMock,
    mock_open: MagicMock,
    mock_generate_content: MagicMock,
    mock_sanitize: MagicMock,
    mock_prompt: MagicMock,
    mock_perform_write_test: MagicMock,
    mock_ensure_docs_dir: MagicMock,
    mock_get_docs_dir: MagicMock,
) -> None:
    """Test script handles normal case with all arguments provided."""
    # Configure mocks
    mock_get_docs_dir.return_value = pathlib.Path("/fake/docs")
    mock_ensure_docs_dir.return_value = None  # Assume directory exists or is created
    mock_perform_write_test.return_value = None  # Assume write test passes
    # Ensure prompts are not called when args are provided
    mock_prompt.side_effect = AssertionError("Prompt should not be called")
    mock_sanitize.return_value = ("0100", "my-new-doc")
    mock_generate_content.return_value = "Generated content"
    mock_exists.return_value = False  # File does not exist initially
    mock_confirm.side_effect = AssertionError(
        "Confirm should not be called",
    )  # No overwrite needed

    # Mock file writing
    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file

    # Simulate running the command with arguments
    result = run_command(
        args=["--doc-type", "task", "My New Doc", "--priority", "0100"],
    )

    # Assertions
    assert result.exit_code == 0
    mock_get_docs_dir.assert_called_once()
    mock_ensure_docs_dir.assert_called_once_with(pathlib.Path("/fake/docs"))
    mock_perform_write_test.assert_called_once_with(pathlib.Path("/fake/docs"))
    mock_prompt.assert_not_called()  # No prompts expected
    mock_sanitize.assert_called_once_with("My New Doc", "0100")
    # Note: The path here is relative to the test file's location within the project
    # structure
    mock_generate_content.assert_called_once_with(
        pathlib.Path(__file__).parent.parent.parent / "templates",
        "simple",  # Default template type when none is specified
        "task",
    )
    mock_exists.assert_called_once_with()  # Check if the target file exists
    mock_confirm.assert_not_called()  # No overwrite prompt
    mock_open.assert_called_once_with(
        pathlib.Path("/fake/docs/0100-my-new-doc.md"),
        "w",
        encoding="utf-8",
    )
    mock_file.write.assert_called_once_with("Generated content")
    assert "Document created successfully" in result.stdout


@patch("src.new_doc._get_docs_directory")
@patch("src.new_doc._ensure_docs_directory_exists")
@patch("src.new_doc._perform_write_test")
@patch("src.new_doc._prompt_for_missing_arguments")
@patch("src.new_doc._sanitize_inputs")
@patch("src.new_doc._generate_document_content")
@patch("src.new_doc.Path.open")
@patch("src.new_doc.Path.exists")
@patch("click.confirm")
def test_regular_case_missing_args_prompts(
    mock_confirm: MagicMock,
    mock_exists: MagicMock,
    mock_open: MagicMock,
    mock_generate_content: MagicMock,
    mock_sanitize: MagicMock,
    mock_prompt: MagicMock,
    mock_perform_write_test: MagicMock,
    mock_ensure_docs_dir: MagicMock,
    mock_get_docs_dir: MagicMock,
) -> None:
    """Test script prompts for missing arguments."""
    # Configure mocks
    mock_get_docs_dir.return_value = pathlib.Path("/fake/docs")
    mock_ensure_docs_dir.return_value = None
    mock_perform_write_test.return_value = None
    # Configure mock_prompt to return values for each expected prompt
    # The order of prompts in _prompt_for_missing_arguments is:
    # - title
    # - template_type
    # - doc_type
    # - priority
    mock_prompt.side_effect = ["My Prompted Doc", "simple", "task", "0200"]
    mock_sanitize.return_value = ("0200", "my-prompted-doc")
    mock_generate_content.return_value = "Generated content"
    mock_exists.return_value = False
    mock_confirm.side_effect = AssertionError("Confirm should not be called")

    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file

    # Simulate running the command with no arguments
    # We need to provide input for the prompts
    result = run_command(args=[], cli_input="My Prompted Doc\nsimple\ntask\n0200\n")

    # Assertions
    assert result.exit_code == 0
    mock_get_docs_dir.assert_called_once()
    mock_ensure_docs_dir.assert_called_once_with(pathlib.Path("/fake/docs"))
    mock_perform_write_test.assert_called_once_with(pathlib.Path("/fake/docs"))
    # Assert that prompts were called for missing args
    # Note: click.prompt is called inside _prompt_for_missing_arguments
    mock_prompt.assert_any_call("Enter the short title to use in the file name")
    mock_prompt.assert_any_call(
        "Choose template type",
        type=click.Choice(["simple", "complex"], case_sensitive=False),
        default="simple",
        show_default=True,
    )
    mock_prompt.assert_any_call(
        "Enter the document type (e.g., 'RFC', 'ADR', 'Note')",
        default="",
        show_default=False,
    )
    mock_prompt.assert_any_call(
        "Enter the priority number to put at the start of the file name (e.g., '0210')",
        default="????",
        show_default=False,
    )
    assert mock_prompt.call_count == len(
        ["short name", "priority", "doc type", "docs dir"],
    )  # Assuming all 4 prompts are needed
    mock_sanitize.assert_called_once_with("My Prompted Doc", "0200")
    mock_generate_content.assert_called_once_with(
        pathlib.Path(__file__).parent.parent.parent / "templates",
        "simple",
        "task",
    )
    mock_exists.assert_called_once_with()
    mock_confirm.assert_not_called()
    mock_open.assert_called_once_with(
        pathlib.Path("/fake/docs/0200-my-prompted-doc.md"),
        "w",
        encoding="utf-8",
    )
    mock_file.write.assert_called_once_with("Generated content")
    assert "Document created successfully" in result.stdout


@patch("src.new_doc._get_docs_directory")
@patch("src.new_doc._ensure_docs_directory_exists")
@patch("src.new_doc._perform_write_test")
@patch("src.new_doc._prompt_for_missing_arguments")
@patch("src.new_doc._sanitize_inputs")
@patch("src.new_doc._generate_document_content")
@patch("src.new_doc.Path.open")
@patch("src.new_doc.Path.exists")
@patch("click.confirm")
def test_existing_file_prompts_for_overwrite(
    mock_confirm: MagicMock,
    mock_exists: MagicMock,
    mock_open: MagicMock,
    mock_generate_content: MagicMock,
    mock_sanitize: MagicMock,
    mock_prompt: MagicMock,
    mock_perform_write_test: MagicMock,
    mock_ensure_docs_dir: MagicMock,
    mock_get_docs_dir: MagicMock,
) -> None:
    """Test script prompts before overwriting an existing file."""
    # Configure mocks
    mock_get_docs_dir.return_value = pathlib.Path("/fake/docs")
    mock_ensure_docs_dir.return_value = None
    mock_perform_write_test.return_value = None
    mock_prompt.return_value = "dummy"  # Should not be called if args provided
    mock_sanitize.return_value = ("0100", "existing-doc")
    mock_generate_content.return_value = "Generated content"
    mock_exists.return_value = True  # Simulate file exists
    mock_confirm.return_value = True  # Simulate user confirms overwrite

    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file

    # Simulate running the command
    result = run_command(
        args=["--doc-type", "task", "Existing Doc", "--priority", "0100"],
    )

    # Assertions
    assert result.exit_code == 0
    mock_exists.assert_called_once_with()  # Check if the target file exists
    mock_confirm.assert_called_once_with(
        "File '/fake/docs/0100-existing-doc.md' already exists. Overwrite?",
    )
    mock_open.assert_called_once_with(
        pathlib.Path("/fake/docs/0100-existing-doc.md"),
        "w",
        encoding="utf-8",
    )
    mock_file.write.assert_called_once_with("Generated content")
    assert "Document created successfully" in result.stdout


@patch("src.new_doc._get_docs_directory")
@patch("src.new_doc._ensure_docs_directory_exists")
@patch("src.new_doc._perform_write_test")
@patch("src.new_doc._prompt_for_missing_arguments")
@patch("src.new_doc._sanitize_inputs")
@patch("src.new_doc._generate_document_content")
@patch("src.new_doc.Path.open")
@patch("src.new_doc.Path.exists")
@patch("click.confirm")
def test_existing_file_does_not_overwrite_if_denied(
    mock_confirm: MagicMock,
    mock_exists: MagicMock,
    mock_open: MagicMock,
    mock_generate_content: MagicMock,
    mock_sanitize: MagicMock,
    mock_prompt: MagicMock,
    mock_perform_write_test: MagicMock,
    mock_ensure_docs_dir: MagicMock,
    mock_get_docs_dir: MagicMock,
) -> None:
    """Test script does not overwrite if user denies confirmation."""
    # Configure mocks
    mock_get_docs_dir.return_value = pathlib.Path("/fake/docs")
    mock_ensure_docs_dir.return_value = None
    mock_perform_write_test.return_value = None
    mock_prompt.return_value = "dummy"  # Should not be called if args provided
    mock_sanitize.return_value = ("0100", "existing-doc")
    mock_generate_content.return_value = "Generated content"
    mock_exists.return_value = True  # Simulate file exists
    mock_confirm.return_value = False  # Simulate user denies overwrite

    # Simulate running the command
    result = run_command(
        args=["--doc-type", "task", "Existing Doc", "--priority", "0100"],
    )

    # Assertions
    # click.Abort results in exit code 1
    assert result.exit_code == 1
    mock_exists.assert_called_once_with()
    mock_confirm.assert_called_once_with(
        "File '/fake/docs/0100-existing-doc.md' already exists. Overwrite?",
    )
    mock_open.assert_not_called()  # Assert write_document was NOT called
    assert "Operation cancelled." in result.stdout


# --- Edge Cases ---


@patch("src.new_doc._get_docs_directory")
def test_permissions_error_finding_docs_directory(
    mock_get_docs_dir: MagicMock,
) -> None:
    """Test script handles permissions error when finding/accessing docs dir."""
    # Simulate an OSError during directory access in _get_docs_directory
    mock_get_docs_dir.side_effect = OSError(
        13,
        "Permission denied",
    )  # errno 13 is Permission denied

    # Simulate running the command
    result = run_command(args=["--doc-type", "task", "Test", "--priority", "0100"])

    # Assertions
    assert result.exit_code == 1  # click.ClickException results in exit code 1
    assert "Permission denied" in result.stderr
    mock_get_docs_dir.assert_called_once()


@patch("src.new_doc._get_docs_directory")
@patch("src.new_doc._ensure_docs_directory_exists")
@patch("src.new_doc._perform_write_test")
@patch("src.new_doc._prompt_for_missing_arguments")
@patch("src.new_doc._sanitize_inputs")
@patch("src.new_doc._generate_document_content")
@patch("src.new_doc.Path.open")
@patch("src.new_doc.Path.exists")
@patch("click.confirm")
def test_permissions_error_writing_file(
    mock_confirm: MagicMock,
    mock_exists: MagicMock,
    mock_open: MagicMock,
    mock_generate_content: MagicMock,
    mock_sanitize: MagicMock,
    mock_prompt: MagicMock,
    mock_perform_write_test: MagicMock,
    mock_ensure_docs_dir: MagicMock,
    mock_get_docs_dir: MagicMock,
) -> None:
    """Test script handles permissions error when writing the document file."""
    # Configure mocks
    mock_get_docs_dir.return_value = pathlib.Path("/fake/docs")
    mock_ensure_docs_dir.return_value = None
    mock_perform_write_test.return_value = None
    mock_prompt.return_value = "dummy"
    mock_sanitize.return_value = ("0100", "test-doc")
    mock_generate_content.return_value = "Generated content"
    mock_exists.return_value = False
    mock_confirm.return_value = False  # Not relevant if write fails before confirm

    # Simulate an OSError during file writing
    mock_open.side_effect = OSError(13, "Permission denied")

    # Simulate running the command
    result = run_command(args=["--doc-type", "task", "Test Doc", "--priority", "0100"])

    # Assertions
    assert result.exit_code == 1
    assert "Cannot write to docs directory" in result.stderr
    assert "Permission denied" in result.stderr
    mock_open.assert_called_once()


@patch("src.new_doc._get_docs_directory")
@patch("src.new_doc._ensure_docs_directory_exists")
@patch("src.new_doc._perform_write_test")
@patch("src.new_doc._prompt_for_missing_arguments")
@patch("src.new_doc._sanitize_inputs")
@patch("src.new_doc._generate_document_content")
@patch("src.new_doc.Path.open")
@patch("src.new_doc.Path.exists")
@patch("click.confirm")
def test_disk_full_error_writing_file(
    mock_confirm: MagicMock,
    mock_exists: MagicMock,
    mock_open: MagicMock,
    mock_generate_content: MagicMock,
    mock_sanitize: MagicMock,
    mock_prompt: MagicMock,
    mock_perform_write_test: MagicMock,
    mock_ensure_docs_dir: MagicMock,
    mock_get_docs_dir: MagicMock,
) -> None:
    """Test script handles disk full error when writing the document file."""
    # Configure mocks
    mock_get_docs_dir.return_value = pathlib.Path("/fake/docs")
    mock_ensure_docs_dir.return_value = None
    mock_perform_write_test.return_value = None
    mock_prompt.return_value = "dummy"
    mock_sanitize.return_value = ("0100", "test-doc")
    mock_generate_content.return_value = "Generated content"
    mock_exists.return_value = False
    mock_confirm.return_value = False

    # Simulate an OSError indicating disk full (errno 28 is No space on device)
    mock_open.side_effect = OSError(28, "No space on device")

    # Simulate running the command
    result = run_command(args=["--doc-type", "task", "Test Doc", "--priority", "0100"])

    # Assertions
    assert result.exit_code == 1
    assert "Error writing to docs directory" in result.stderr
    assert "No space on device" in result.stderr
    mock_open.assert_called_once()


@patch("src.new_doc._get_docs_directory")
@patch("src.new_doc._ensure_docs_directory_exists")
@patch("src.new_doc._perform_write_test")
@patch("src.new_doc._prompt_for_missing_arguments")
@patch("src.new_doc._sanitize_inputs")
@patch("src.new_doc._generate_document_content")
@patch("src.new_doc.Path.open")
@patch("src.new_doc.Path.exists")
@patch("click.confirm")
def test_missing_template_tags(
    mock_confirm: MagicMock,
    mock_exists: MagicMock,
    mock_open: MagicMock,
    mock_generate_content: MagicMock,
    mock_sanitize: MagicMock,
    mock_prompt: MagicMock,
    mock_perform_write_test: MagicMock,
    mock_ensure_docs_dir: MagicMock,
    mock_get_docs_dir: MagicMock,
) -> None:
    """Test script handles template file missing expected tags."""
    # Configure mocks
    mock_get_docs_dir.return_value = pathlib.Path("/fake/docs")
    mock_ensure_docs_dir.return_value = None
    mock_perform_write_test.return_value = None
    mock_prompt.return_value = "dummy"
    mock_sanitize.return_value = ("0100", "test-doc")
    mock_exists.return_value = False
    mock_confirm.return_value = False

    # Simulate a template missing tags - _generate_document_content handles this
    mock_generate_content.return_value = "# Just some content\nNo tags here."

    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file

    # Simulate running the command
    result = run_command(args=["--doc-type", "task", "Test Doc", "--priority", "0100"])

    # Assertions
    assert result.exit_code == 0
    mock_generate_content.assert_called_once()  # Ensure content generation attempted
    mock_open.assert_called_once()  # Ensure file writing was attempted
    mock_file.write.assert_called_once_with(
        "# Just some content\nNo tags here.",
    )  # Ensure content was written as generated
    assert "Document created successfully" in result.stdout


@patch("src.new_doc._get_docs_directory")
@patch("src.new_doc._ensure_docs_directory_exists")
@patch("src.new_doc._perform_write_test")
@patch("src.new_doc._prompt_for_missing_arguments")
@patch("src.new_doc._sanitize_inputs")
@patch("src.new_doc._generate_document_content")
@patch("src.new_doc.Path.exists")
@patch("click.confirm")
def test_missing_templates_directory(
    mock_confirm: MagicMock,
    mock_exists: MagicMock,
    mock_generate_content: MagicMock,
    mock_sanitize: MagicMock,
    mock_prompt: MagicMock,
    mock_perform_write_test: MagicMock,
    mock_ensure_docs_dir: MagicMock,
    mock_get_docs_dir: MagicMock,
) -> None:
    """Test script handles missing templates directory."""
    # Configure mocks
    mock_get_docs_dir.return_value = pathlib.Path("/fake/docs")
    mock_ensure_docs_dir.return_value = None
    mock_perform_write_test.return_value = None
    mock_prompt.return_value = "dummy"
    mock_sanitize.return_value = ("0100", "test-doc")
    mock_exists.return_value = False
    mock_confirm.return_value = False

    # Simulate FileNotFoundError when reading template inside _generate_document_content
    mock_generate_content.side_effect = FileNotFoundError(
        "Template directory or file not found",
    )

    # Simulate running the command
    result = run_command(args=["--doc-type", "task", "Test Doc", "--priority", "0100"])

    # Assertions
    assert result.exit_code == 1
    assert (
        "Error: Template file" in result.stderr
    )  # Check for the specific error message from _generate_document_content
    assert "not found." in result.stderr
    mock_generate_content.assert_called_once()  # Ensure content generation attempted


# --- uv Integration ---
# These tests are more integration-level and might require setting up a test environment
# or mocking the entry point execution. Unit tests are less suitable here.
# We will skip these as they test uv/click behavior more than our core logic.

# def test_uvx_new_doc_invokes_command():
#     """Test that 'uvx new-doc' correctly invokes the command."""
#     pass # Skip - tests uv/entry point behavior

# def test_uvx_pape_docs_new_invokes_command():
#     """Test that 'uvx pape-docs new' correctly invokes the command."""
#     pass # Skip - tests uv/entry point behavior

# def test_uvx_pape_docs_prints_help():
#     """Test that 'uvx pape-docs' prints help."""
#     pass # Skip - tests click/entry point behavior

# def test_direct_execution_after_uv_install():
#     """Test direct execution of commands after uv install."""
#     pass # Skip - tests installation/environment setup

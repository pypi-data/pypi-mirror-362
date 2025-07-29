from unittest.mock import patch

import click

# Import the actual helper functions
from src.new_doc import _prompt_for_missing_arguments, _sanitize_inputs

# --- Input Processing Tests ---


@patch("click.prompt")
def test_prompt_for_missing_arguments_all_missing(mock_prompt) -> None:
    """Test _prompt_for_missing_arguments prompts for all arguments when none are provided."""
    # Configure mock_prompt to return values for each expected prompt
    # Order: title, template_type, doc_type, priority
    mock_prompt.side_effect = ["Prompted Title", "complex", "Prompted Type", "0300"]

    title, template_type, doc_type, priority = _prompt_for_missing_arguments(
        title=None,
        template_type=None,
        priority=None,
        doc_type=None,
    )

    # Assertions
    assert title == "Prompted Title"
    assert template_type == "complex"
    assert doc_type == "Prompted Type"
    assert priority == "0300"

    # Check that prompts were called with expected messages/defaults
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
    assert mock_prompt.call_count == 4


@patch("click.prompt")
def test_prompt_for_missing_arguments_some_provided(mock_prompt) -> None:
    """Test _prompt_for_missing_arguments only prompts for missing arguments."""
    # Configure mock_prompt to return values for the missing prompts
    # Order: doc_type, priority (title and template_type are provided)
    mock_prompt.side_effect = ["Prompted Type", "0300"]

    title, template_type, doc_type, priority = _prompt_for_missing_arguments(
        title="Provided Title",
        template_type="simple",
        priority=None,
        doc_type=None,
    )

    # Assertions
    assert title == "Provided Title"
    assert template_type == "simple"
    assert doc_type == "Prompted Type"
    assert priority == "0300"

    # Check that prompts were called only for missing args
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
    assert mock_prompt.call_count == 2  # Only doc_type and priority were missing


def test_input_sanitization_title() -> None:
    """Test title sanitization."""
    # Call the actual sanitization function
    sanitized_priority, sanitized_title = _sanitize_inputs("My Doc! @#$ Title", "0100")
    assert sanitized_title == "My-Doc-Title"

    sanitized_priority, sanitized_title = _sanitize_inputs(" Another Title ", "0100")
    assert sanitized_title == "Another-Title"

    sanitized_priority, sanitized_title = _sanitize_inputs("", "0100")
    assert sanitized_title == ""  # Empty string is allowed for title


def test_input_sanitization_priority() -> None:
    """Test priority sanitization."""
    # Call the actual sanitization function
    sanitized_priority, sanitized_title = _sanitize_inputs("My Title", "P-0100!")
    assert sanitized_priority == "P-0100"  # Spaces and hyphens are kept in priority

    sanitized_priority, sanitized_title = _sanitize_inputs("My Title", " 0200 ")
    assert sanitized_priority == "0200"  # Leading/trailing spaces removed

    sanitized_priority, sanitized_title = _sanitize_inputs("My Title", "")
    assert sanitized_priority == "????"  # Empty string defaults to ????

import pathlib
from unittest.mock import MagicMock, patch

import click
import pytest

# Import the actual helper functions
from src.new_doc import (
    _ensure_docs_directory_exists,
    _get_docs_directory,
    _perform_write_test,
)

# --- Directory Helper Tests ---


@patch("os.getenv")
@patch("pathlib.Path.exists")
@patch("pathlib.Path.is_dir")
@patch("pathlib.Path.open")  # To mock pyproject.toml reading
@patch("click.prompt")
def test_get_docs_directory_env_var(
    mock_prompt: MagicMock,
    mock_is_dir: MagicMock,
    mock_exists: MagicMock,
    mock_getenv: MagicMock,
) -> None:
    """Test _get_docs_directory uses PAPE_DOCS_DIR env var if set."""
    mock_getenv.return_value = "/path/from/env"

    # Ensure other checks are not triggered
    mock_exists.return_value = False
    mock_is_dir.return_value = False
    mock_prompt.side_effect = AssertionError("Prompt should not be called")

    docs_dir = _get_docs_directory()

    assert docs_dir == pathlib.Path("/path/from/env")
    mock_getenv.assert_called_once_with("PAPE_DOCS_DIR")
    mock_exists.assert_not_called()
    mock_is_dir.assert_not_called()
    mock_prompt.assert_not_called()


@patch("os.getenv")
@patch("pathlib.Path.exists")
@patch("pathlib.Path.is_dir")
@patch("pathlib.Path.open")
@patch("toml.load")
@patch("click.prompt")
@patch("pathlib.Path.cwd")
def test_get_docs_directory_pyproject_tool_config(
    mock_cwd: MagicMock,
    mock_prompt: MagicMock,
    mock_toml_load: MagicMock,
    mock_open: MagicMock,
    mock_is_dir: MagicMock,
    mock_exists: MagicMock,
    mock_getenv: MagicMock,
) -> None:
    """Test _get_docs_directory uses pyproject.toml tool config."""
    mock_getenv.return_value = None  # No env var
    mock_cwd.return_value = pathlib.Path("/fake/project")

    # Simulate pyproject.toml exists in the current directory
    mock_exists.side_effect = lambda p: p == pathlib.Path(
        "/fake/project/pyproject.toml",
    )
    mock_is_dir.return_value = False  # No existing docs dir
    mock_toml_load.return_value = {"tool": {"pape-docs": {"docs-dir": "custom_docs"}}}
    mock_prompt.side_effect = AssertionError("Prompt should not be called")

    docs_dir = _get_docs_directory()

    assert docs_dir == pathlib.Path("/fake/project/custom_docs")
    mock_getenv.assert_called_once_with("PAPE_DOCS_DIR")
    mock_exists.assert_any_call(pathlib.Path("/fake/project/pyproject.toml"))
    mock_open.assert_called_once_with(
        pathlib.Path("/fake/project/pyproject.toml"),
        "r",
        encoding="utf-8",
    )
    mock_toml_load.assert_called_once()
    mock_is_dir.assert_not_called()  # Existing docs dir check skipped after finding pyproject.toml
    mock_prompt.assert_not_called()


@patch("os.getenv")
@patch("pathlib.Path.exists")
@patch("pathlib.Path.is_dir")
@patch("pathlib.Path.open")
@patch("toml.load")
@patch("click.prompt")
@patch("pathlib.Path.cwd")
def test_get_docs_directory_pyproject_default(
    mock_cwd: MagicMock,
    mock_prompt: MagicMock,
    mock_toml_load: MagicMock,
    mock_open: MagicMock,
    mock_is_dir: MagicMock,
    mock_exists: MagicMock,
    mock_getenv: MagicMock,
) -> None:
    """Test _get_docs_directory uses default docs/ if pyproject.toml exists but no tool config."""
    mock_getenv.return_value = None  # No env var
    mock_cwd.return_value = pathlib.Path("/fake/project")

    # Simulate pyproject.toml exists but no tool config
    mock_exists.side_effect = lambda p: p == pathlib.Path(
        "/fake/project/pyproject.toml",
    )
    mock_is_dir.return_value = False
    mock_toml_load.return_value = {
        "project": {"name": "my-project"},
    }  # No tool.pape-docs
    mock_prompt.side_effect = AssertionError("Prompt should not be called")

    docs_dir = _get_docs_directory()

    assert docs_dir == pathlib.Path("/fake/project/docs")
    mock_getenv.assert_called_once_with("PAPE_DOCS_DIR")
    mock_exists.assert_any_call(pathlib.Path("/fake/project/pyproject.toml"))
    mock_open.assert_called_once_with(
        pathlib.Path("/fake/project/pyproject.toml"),
        "r",
        encoding="utf-8",
    )
    mock_toml_load.assert_called_once()
    mock_is_dir.assert_not_called()
    mock_prompt.assert_not_called()


@patch("os.getenv")
@patch("pathlib.Path.exists")
@patch("pathlib.Path.is_dir")
@patch("pathlib.Path.open")
@patch("toml.load")
@patch("click.prompt")
@patch("pathlib.Path.cwd")
def test_get_docs_directory_existing_docs_dir(
    mock_cwd: MagicMock,
    mock_prompt: MagicMock,
    mock_toml_load: MagicMock,
    mock_open: MagicMock,
    mock_is_dir: MagicMock,
    mock_exists: MagicMock,
    mock_getenv: MagicMock,
) -> None:
    """Test _get_docs_directory finds existing docs/ directory."""
    mock_getenv.return_value = None  # No env var
    mock_cwd.return_value = pathlib.Path("/fake/project")

    # Simulate no pyproject.toml, but existing docs/ dir
    mock_exists.side_effect = lambda p: p != pathlib.Path(
        "/fake/project/pyproject.toml",
    )  # pyproject.toml does not exist
    mock_is_dir.side_effect = lambda p: p == pathlib.Path(
        "/fake/project/docs",
    )  # docs/ exists and is a directory
    mock_prompt.side_effect = AssertionError("Prompt should not be called")

    docs_dir = _get_docs_directory()

    assert docs_dir == pathlib.Path("/fake/project/docs")
    mock_getenv.assert_called_once_with("PAPE_DOCS_DIR")
    mock_exists.assert_any_call(
        pathlib.Path("/fake/project/pyproject.toml"),
    )  # Check for pyproject.toml
    mock_is_dir.assert_any_call(
        pathlib.Path("/fake/project/docs"),
    )  # Check for existing docs/
    mock_open.assert_not_called()
    mock_toml_load.assert_not_called()
    mock_prompt.assert_not_called()


@patch("os.getenv")
@patch("pathlib.Path.exists")
@patch("pathlib.Path.is_dir")
@patch("pathlib.Path.open")
@patch("toml.load")
@patch("click.prompt")
@patch("pathlib.Path.cwd")
def test_get_docs_directory_prompt(
    mock_cwd: MagicMock,
    mock_prompt: MagicMock,
    mock_toml_load: MagicMock,
    mock_open: MagicMock,
    mock_is_dir: MagicMock,
    mock_exists: MagicMock,
    mock_getenv: MagicMock,
) -> None:
    """Test _get_docs_directory prompts user if no directory found."""
    mock_getenv.return_value = None  # No env var
    mock_cwd.return_value = pathlib.Path("/fake/project")

    # Simulate nothing found
    mock_exists.return_value = False
    mock_is_dir.return_value = False
    mock_prompt.return_value = "./user_input_docs"  # Simulate user input

    docs_dir = _get_docs_directory()

    assert docs_dir == pathlib.Path("./user_input_docs")
    mock_getenv.assert_called_once_with("PAPE_DOCS_DIR")
    mock_exists.assert_any_call(pathlib.Path("/fake/project/pyproject.toml"))
    mock_is_dir.assert_any_call(pathlib.Path("/fake/project/docs"))
    mock_prompt.assert_called_once_with(
        "Please provide a docs directory to use",
        default="./docs",
    )
    mock_open.assert_not_called()
    mock_toml_load.assert_not_called()


@patch("pathlib.Path.exists")
@patch("pathlib.Path.mkdir")
@patch("click.confirm")
def test_ensure_docs_directory_exists_creates_if_confirmed(
    mock_confirm: MagicMock,
    mock_mkdir: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Test _ensure_docs_directory_exists creates directory if it doesn't exist and user confirms."""
    docs_dir = pathlib.Path("/fake/new/docs")
    mock_exists.return_value = False  # Directory does not exist
    mock_confirm.return_value = True  # User confirms creation
    mock_mkdir.return_value = None  # mkdir succeeds

    _ensure_docs_directory_exists(docs_dir)

    mock_exists.assert_called_once_with()
    mock_confirm.assert_called_once_with(
        f"Docs directory '{docs_dir}' does not exist. Create it?",
    )
    mock_mkdir.assert_called_once_with(exist_ok=True)


@patch("pathlib.Path.exists")
@patch("pathlib.Path.mkdir")
@patch("click.confirm")
def test_ensure_docs_directory_exists_aborts_if_denied(
    mock_confirm: MagicMock,
    mock_mkdir: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Test _ensure_docs_directory_exists aborts if directory doesn't exist and user denies."""
    docs_dir = pathlib.Path("/fake/new/docs")
    mock_exists.return_value = False  # Directory does not exist
    mock_confirm.return_value = False  # User denies creation
    mock_mkdir.side_effect = AssertionError("mkdir should not be called")

    with pytest.raises(click.Abort):
        _ensure_docs_directory_exists(docs_dir)

    mock_exists.assert_called_once_with()
    mock_confirm.assert_called_once_with(
        f"Docs directory '{docs_dir}' does not exist. Create it?",
    )
    mock_mkdir.assert_not_called()


@patch("pathlib.Path.exists")
@patch("pathlib.Path.mkdir")
@patch("click.confirm")
def test_ensure_docs_directory_exists_does_nothing_if_exists(
    mock_confirm: MagicMock,
    mock_mkdir: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Test _ensure_docs_directory_exists does nothing if directory already exists."""
    docs_dir = pathlib.Path("/fake/existing/docs")
    mock_exists.return_value = True  # Directory exists
    mock_confirm.side_effect = AssertionError("Confirm should not be called")
    mock_mkdir.side_effect = AssertionError("mkdir should not be called")

    _ensure_docs_directory_exists(docs_dir)

    mock_exists.assert_called_once_with()
    mock_confirm.assert_not_called()
    mock_mkdir.assert_not_called()


@patch("pathlib.Path.exists")
@patch("pathlib.Path.mkdir")
@patch("click.confirm")
def test_ensure_docs_directory_exists_handles_permission_error(
    mock_confirm: MagicMock,
    mock_mkdir: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Test _ensure_docs_directory_exists handles PermissionError during creation."""
    docs_dir = pathlib.Path("/fake/new/docs")
    mock_exists.return_value = False
    mock_confirm.return_value = True
    mock_mkdir.side_effect = PermissionError("Insufficient permissions")

    with pytest.raises(click.ClickException) as excinfo:
        _ensure_docs_directory_exists(docs_dir)

    assert "insufficient permissions" in str(excinfo.value)
    mock_exists.assert_called_once_with()
    mock_confirm.assert_called_once_with(
        f"Docs directory '{docs_dir}' does not exist. Create it?",
    )
    mock_mkdir.assert_called_once_with(exist_ok=True)


@patch("pathlib.Path.exists")
@patch("pathlib.Path.mkdir")
@patch("click.confirm")
def test_ensure_docs_directory_exists_handles_file_not_found_error(
    mock_confirm: MagicMock,
    mock_mkdir: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Test _ensure_docs_directory_exists handles FileNotFoundError during creation."""
    docs_dir = pathlib.Path("/nonexistent/parent/new/docs")
    mock_exists.return_value = False
    mock_confirm.return_value = True
    mock_mkdir.side_effect = FileNotFoundError("Parent directory does not exist")

    with pytest.raises(click.ClickException) as excinfo:
        _ensure_docs_directory_exists(docs_dir)

    assert "parent directory does not exist" in str(excinfo.value)
    mock_exists.assert_called_once_with()
    mock_confirm.assert_called_once_with(
        f"Docs directory '{docs_dir}' does not exist. Create it?",
    )
    mock_mkdir.assert_called_once_with(exist_ok=True)


@patch("pathlib.Path.open")
@patch("pathlib.Path.unlink")
def test_perform_write_test_success(mock_unlink, mock_open) -> None:
    """Test _perform_write_test succeeds when writing and deleting are possible."""
    docs_dir = pathlib.Path("/fake/docs")
    test_file = docs_dir / ".pape-docs-write-test.tmp"

    # Mock file operations
    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file
    mock_unlink.return_value = None

    _perform_write_test(docs_dir)

    mock_open.assert_called_once_with(test_file, "w", encoding="utf-8")
    mock_file.write.assert_called_once_with("test")
    mock_unlink.assert_called_once_with()


@patch("pathlib.Path.open")
@patch("pathlib.Path.unlink")
def test_perform_write_test_handles_file_not_found_error(
    mock_unlink: MagicMock,
    mock_open: MagicMock,
) -> None:
    """Test _perform_write_test handles FileNotFoundError during write test."""
    docs_dir = pathlib.Path("/fake/docs")
    test_file = docs_dir / ".pape-docs-write-test.tmp"

    mock_open.side_effect = FileNotFoundError("Directory not accessible")
    mock_unlink.side_effect = AssertionError("unlink should not be called")

    with pytest.raises(click.ClickException) as excinfo:
        _perform_write_test(docs_dir)

    assert "does not exist or is not accessible" in str(excinfo.value)
    mock_open.assert_called_once_with(test_file, "w", encoding="utf-8")
    mock_unlink.assert_not_called()


@patch("pathlib.Path.open")
@patch("pathlib.Path.unlink")
def test_perform_write_test_handles_os_error_writing(
    mock_unlink: MagicMock,
    mock_open: MagicMock,
) -> None:
    """Test _perform_write_test handles OSError during write test."""
    docs_dir = pathlib.Path("/fake/docs")
    test_file = docs_dir / ".pape-docs-write-test.tmp"

    mock_open.side_effect = OSError(13, "Permission denied")
    mock_unlink.side_effect = AssertionError("unlink should not be called")

    with pytest.raises(click.ClickException) as excinfo:
        _perform_write_test(docs_dir)

    assert "Cannot write to docs directory" in str(excinfo.value)
    assert "permission error" in str(excinfo.value)
    mock_open.assert_called_once_with(test_file, "w", encoding="utf-8")
    mock_unlink.assert_not_called()


@patch("pathlib.Path.open")
@patch("pathlib.Path.unlink")
def test_perform_write_test_handles_os_error_unlinking(mock_unlink, mock_open) -> None:
    """Test _perform_write_test handles OSError during unlink."""
    docs_dir = pathlib.Path("/fake/docs")
    test_file = docs_dir / ".pape-docs-write-test.tmp"

    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file
    mock_unlink.side_effect = OSError(13, "Permission denied")

    with pytest.raises(click.ClickException) as excinfo:
        _perform_write_test(docs_dir)

    assert "Error deleting temporary file" in str(excinfo.value)
    assert "Permission denied" in str(excinfo.value)
    mock_open.assert_called_once_with(test_file, "w", encoding="utf-8")
    mock_file.write.assert_called_once_with("test")
    mock_unlink.assert_called_once_with()

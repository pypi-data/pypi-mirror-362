# The test suite

A **task**, created on **July 6, 2025**, about **creating a test suite for this project**

## Status

Accepted and in progress

## Description

I need to create a test suite that tests all of what follows.

Wherever the test I'm describing would really just test how `click` or `uv` or another package/library handles the situation, just skip it and count on that library having sufficient testing.

We should only test our own capabilities; our tests should not be brittle to other libraries changing (unless they are breaking changes we need to account for in package management).

As with my other projects, the test suite should be located in `test` or `tests`, and the structure should mirror `src`.

If one file has many tests that should be broken up into multiple files, it is acceptable to make a directory of test files for a single source document.

### Regular cases

- The script should correctly handle every normal case related to the docs directory and `pyproject.toml` location/variables/existence.
- The script should handle missing arguments by interactively prompting the user for the required information.
- The script should not interactively prompt for arguments provided at invocation.
- The script should properly sanitize inputs. Specifically, for the filename components (title and priority), non-alphanumeric characters should be removed, and spaces should be replaced with hyphens.
- The script should properly fill in the doc template file.
- If the generated filename already exists, the script should prompt the user for confirmation before overwriting the file.

### Edge cases

Come up with unusual or risky scenarios related to all of the cases already described.

Make sure the script handles these edge cases correctly and gives informative error messages to the user.

Here are some potential scenarios:

- The `pyproject.toml` is readable, but the script has insufficient permissions to create the `docs` directory. If possible, we want to warn the user about permissions issues before they waste time providing a doc type, title, and priority.
- The `pyproject.toml` specifies a `docs` directory in a weird location like `/var/root`. It's not the place of the script to judge or warn the user for this kind of thing, but if that `docs` directory isn't writeable, we want to warn the user about that ASAP.
- There is no `pyproject.toml`, and the script finds the `docs` directory at the root of the file system. Again: Weird, but we just want to warn the user if the directory isn't writeable.
- The disk is out of space when attempting to create the `docs` directory or write the new document file. The script should provide an informative error message.
- The docs dir existed when we located it early on in the script, but it no longer exists when we try to write to it.
- If the template file is missing expected tags (e.g., `<!-- date -->`, `<!-- file type -->`), the script should proceed without replacing those tags, leaving them as-is in the generated document.
- If the user provides an empty string for the short title, the script should sanitize it to an empty string, resulting in a filename like `priority-.md`. If the user provides an empty string for the priority, it should sanitize to `????`.
- The user provides both the `--simple` and `--complex` value at invocation. Just provide a warning that we will use the last value provided, or whatever `click` does in this type of situation.
- If the user provides too many options (e.g. `--blah-blah-blah`), the script handles that the way `click` does by default.
- The `docs` directory is found and exists, but the script has insufficient permissions to write the new document file within it. The script should provide an informative error message.
- The `templates` directory or the specific template file (`simple.md` or `complex.md`) within it is missing. The script should provide an informative error message.

### `uv` integration

- When `new-doc` is executed (e.g., via `uvx new-doc`), it should correctly invoke the `new_doc_command`.
- When `pape-docs new` is executed (e.g., via `uvx pape-docs new`), it should correctly invoke the `new_doc_command`.
- When `pape-docs` is executed without a subcommand (e.g., `uvx pape-docs`), it should print the help text for the `cli` group (as handled by `click`).
- When `uv` has installed the tool, the subcommands should be available on the CLI without having to invoke `uvx` (i.e. by directly calling `new-doc` or `pape-docs new`).

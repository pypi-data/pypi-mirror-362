# The script should sanitize to the level determined by the user

A **feature proposal**, created on **July 8, 2025**

## Status

In draft

## Description

File names are allowed to contain spaces in macOS. They can also contain a whole range of other characters.

We should give the user the option to use whatever characters they want to use in their filename, as long as the OS allows those characters in a file name, and those characters don't cause the file to be placed in a different directory (e.g. this is not allowed as a filename: `../../../../../../../../../../../../var/root/ssh`).

This could differ per operating system, so we should handle that gracefully.

This option could go in the `pyproject.toml` or an environment variable `PAPE_DOCS_FILE_NAME_SANITIZATION_LEVEL`.

To start, let's just have two levels: High (use the current behavior of sanitizing anything that's not alphanumeric) and low (sanitize as little as possible).

The default should be high (the current behavior).

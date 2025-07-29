# Show docs directory and related errors early

A **feature request**, created on **July 6, 2025**

## Status

Accepted and completed.

## Description

It would be prudent to ensure we tell the user where we will put the docs as early in the script as possible. We will also want to test the ability to write to the directory ASAP --- before user input, if possible.

## Changes made

- Implemented an early writeability test (`_perform_write_test`) that attempts to create and delete a temporary file in the determined docs directory.
- This test is performed after the docs directory is determined (either automatically or via user input/creation) to ensure write permissions are verified before proceeding with document creation.
- Error messages for write permission issues now provide clear guidance, including a note about manually deleting temporary files if deletion fails.

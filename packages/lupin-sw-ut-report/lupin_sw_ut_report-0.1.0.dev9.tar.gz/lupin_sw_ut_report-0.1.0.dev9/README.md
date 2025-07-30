# lupin_sw_ut_report

This project converts test files (in `.txt` and `.xml` formats) into Markdown reports. The goal is to facilitate the documentation of software test results by providing readable Markdown files that can be used for comprehensive reporting.

## Features

- **TXT and XML File Conversion**: Converts test files into structured Markdown files for better readability.
- **Support for Given-When-Then Formats**: Parses and converts test files defined using the `Given`, `When`, `Then` format.
- **Combined Report Generation**: Creates a single Markdown file summarizing all tests found in the specified folder.
- **Command-Line Interface (CLI) with Typer**: A CLI tool for easy execution of conversions.

## Installation

Run `pip install lupin-sw-ut-report`

## Usage

This project provides a command-line interface to generate reports from a folder containing test files (`.txt` and `.xml`).

To run the script, use the following command:

```bash
sw-ut-report --input-folder <path/to/your/input-folder>
```

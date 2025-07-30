import os
from os import PathLike
from typing import Dict, List, Optional

import typer

from sw_ut_report.__init__ import __version__
from sw_ut_report.parse_txt_file import format_txt_file
from sw_ut_report.parse_xml_file import format_xml_to_dict
from sw_ut_report.template_manager import get_local_template

cli = typer.Typer()


def input_folder_option() -> typer.Option:
    return typer.Option(
        ...,
        "--input-folder",
        help="Path to the folder containing the txt and xml files",
    )


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
    input_folder: str = input_folder_option(),
    generate_markdown: bool = typer.Option(True, "--markdown/--no-markdown", help="Generate markdown report"),
    create_jama_ut: bool = typer.Option(False, "--create-ut", help="Create/update unit tests in Jama"),
    module_name: Optional[str] = typer.Option(None, "--module-name", help="Module name for Jama UT creation (required with --create-ut)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be done without making changes to Jama"),
):
    if ctx.invoked_subcommand is None:
        generate_report(input_folder, generate_markdown, create_jama_ut, module_name, dry_run)


@cli.command()
def generate_report(
    input_folder: str = input_folder_option(),
    generate_markdown: bool = typer.Option(True, "--markdown/--no-markdown", help="Generate markdown report"),
    create_jama_ut: bool = typer.Option(False, "--create-ut", help="Create/update unit tests in Jama"),
    module_name: Optional[str] = typer.Option(None, "--module-name", help="Module name for Jama UT creation (required with --create-ut)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be done without making changes to Jama"),
):
    # Validate parameters
    if create_jama_ut and not module_name:
        typer.echo("Error: --module-name is required when --create-ut is used", err=True)
        raise typer.Exit(code=1)

    if not generate_markdown and not create_jama_ut:
        typer.echo("Error: At least one output option must be specified (--markdown or --create-ut)", err=True)
        raise typer.Exit(code=1)

    # Dry-run validation
    if dry_run and not create_jama_ut:
        typer.echo("Note: --dry-run only applies to Jama operations. Use with --create-ut to see Jama actions.")

    typer.echo("test reports processing started")

    all_reports = []

    try:
        file_list = os.listdir(input_folder)
    except FileNotFoundError:
        typer.echo(f"Path '{input_folder}' does not exist.")
        raise typer.Exit(code=1)
    except PermissionError:
        typer.echo(f"Permission denied for the folder '{input_folder}'.")
        raise typer.Exit(code=1)

    for filename in file_list:
        input_file = os.path.join(input_folder, filename)
        _, file_extension = os.path.splitext(filename)

        match file_extension.lower():
            case ".txt":
                scenarios = format_txt_file(read_file_content(input_file))
                for scenario in scenarios:
                    scenario["filename"] = filename
                all_reports.append(
                    {"type": "txt", "filename": filename, "content": scenarios}
                )

            case ".xml":
                suites_data = format_xml_to_dict(input_file)
                suites_data["filename"] = filename
                all_reports.append(
                    {"type": "xml", "filename": filename, "content": suites_data}
                )

            case _:
                if os.path.isdir(input_file):
                    typer.echo(f"Skipping folder: {filename}")
                    continue
                else:
                    print(f"Skipping unsupported file format: {filename}")
                    continue

    if not all_reports:
        typer.echo("No test files found to process.")
        return

    # Execute requested operations
    success = True

    # Create UTs in Jama if requested
    if create_jama_ut:
        try:
            if dry_run:
                from sw_ut_report.jama_ut_manager import dry_run_unit_tests_creation
                from sw_ut_report.jama_common import JamaConnectionError, setup_logging

                # Setup logging for Jama operations
                setup_logging()

                typer.echo(f"DRY-RUN: Analyzing what would be done for module: {module_name}")
                typer.echo("=" * 60)

                ut_success = dry_run_unit_tests_creation(module_name, all_reports)

                if ut_success:
                    typer.echo("Dry-run completed successfully - no errors detected")
                else:
                    typer.echo("Dry-run detected potential issues", err=True)
                    success = False
            else:
                from sw_ut_report.jama_ut_manager import create_unit_tests_in_jama
                from sw_ut_report.jama_common import JamaConnectionError, setup_logging

                # Setup logging for Jama operations
                setup_logging()

                typer.echo(f"Creating unit tests in Jama for module: {module_name}")

                ut_success = create_unit_tests_in_jama(module_name, all_reports)

                if ut_success:
                    typer.echo("Unit tests created/updated in Jama successfully")
                else:
                    typer.echo("Some unit tests may not have been processed", err=True)
                    success = False

        except JamaConnectionError as e:
            typer.echo(f"Jama operation failed: {e}", err=True)
            success = False
        except ImportError as e:
            typer.echo(f"Jama integration not available: {e}", err=True)
            typer.echo("Please install required dependencies: py-jama-rest-client python-dotenv", err=True)
            success = False
        except Exception as e:
            typer.echo(f"Unexpected error during Jama operation: {e}", err=True)
            success = False

    # Generate markdown report if requested (not affected by dry-run)
    if generate_markdown and not dry_run:
        try:
            generate_single_markdown(all_reports)
            typer.echo("Markdown report generated successfully")
        except Exception as e:
            typer.echo(f"Markdown generation failed: {e}", err=True)
            success = False
    elif generate_markdown and dry_run:
        typer.echo("Would generate markdown report: sw_ut_report.md")

    if success:
        if dry_run:
            typer.echo("Dry-run completed - review the analysis above")
        else:
            typer.echo("All operations completed successfully")
    else:
        typer.echo("Some operations failed - check output above", err=True)
        raise typer.Exit(code=1)


def read_file_content(input_file: PathLike) -> str:
    with open(input_file, "r", encoding="utf-8") as f:
        return f.read()


def generate_single_markdown(all_reports: List[Dict]) -> None:
    template = get_local_template("combined_test_report.j2")
    markdown_content = template.render(reports=all_reports)

    with open("sw_ut_report.md", "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

"""Command-line interface for folder2md4llms."""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress

from .__about__ import __version__
from .processor import RepositoryProcessor
from .utils.config import Config

console = Console()


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=".",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    help="Output file path (default: output.md)",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="Configuration file path",
)
@click.option(
    "--ignore-file",
    type=click.Path(exists=True, path_type=Path),
    help="Custom ignore file path (default: .folder2md_ignore)",
)
@click.option(
    "--format",
    type=click.Choice(["markdown", "html", "plain"]),
    default="markdown",
    help="Output format",
)
@click.option(
    "--include-tree/--no-tree",
    default=True,
    help="Include folder structure tree",
)
@click.option(
    "--include-stats/--no-stats",
    default=True,
    help="Include file statistics",
)
@click.option(
    "--convert-docs/--no-convert-docs",
    default=True,
    help="Convert documents (PDF, DOCX, etc.)",
)
@click.option(
    "--describe-binaries/--no-describe-binaries",
    default=True,
    help="Describe binary files",
)
@click.option(
    "--max-file-size",
    type=int,
    default=1024 * 1024,  # 1MB
    help="Maximum file size to process (bytes)",
)
@click.option(
    "--clipboard",
    is_flag=True,
    help="Copy output to clipboard",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Verbose output",
)
@click.version_option(version=__version__)
def main(
    path: Path,
    output: Optional[Path],
    config: Optional[Path],
    ignore_file: Optional[Path],
    format: str,
    include_tree: bool,
    include_stats: bool,
    convert_docs: bool,
    describe_binaries: bool,
    max_file_size: int,
    clipboard: bool,
    verbose: bool,
) -> None:
    """Convert a folder structure to markdown format for LLM consumption.

    PATH: Directory to process (default: current directory)
    """
    try:
        # Load configuration
        config_obj = Config.load(config_path=config, repo_path=path)

        # Override config with command line options
        if ignore_file:
            config_obj.ignore_file = ignore_file
        config_obj.output_format = format
        config_obj.include_tree = include_tree
        config_obj.include_stats = include_stats
        config_obj.convert_docs = convert_docs
        config_obj.describe_binaries = describe_binaries
        config_obj.max_file_size = max_file_size
        config_obj.verbose = verbose

        # Set output file
        if not output:
            output = Path("output.md")

        # Initialize processor
        processor = RepositoryProcessor(config_obj)

        # Process repository
        with Progress(console=console, disable=not verbose) as progress:
            result = processor.process(path, progress)

        # Write output
        output.write_text(result, encoding="utf-8")

        # Copy to clipboard if requested
        if clipboard:
            try:
                import pyperclip

                pyperclip.copy(result)
                console.print("✅ Output copied to clipboard", style="green")
            except ImportError:
                console.print(
                    "⚠️  pyperclip not available for clipboard support", style="yellow"
                )

        console.print(f"✅ Repository processed successfully: {output}", style="green")

    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        if verbose:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Command-line interface for the document converter using Click.
"""

import click

from .converter import batch_convert


@click.command()
@click.argument("inputs", nargs=-1, type=click.Path(exists=True), required=True)
@click.option(
    "-o",
    "--output",
    default="output",
    help="Output directory for converted files",
    type=click.Path(),
)
@click.option(
    "--output-format",
    default="txt",
    type=click.Choice(["txt", "markdown", "json"]),
    help="Output format (txt, markdown, json)",
)
def main(inputs, output, output_format):
    """
    Convert PowerPoint, Word, Excel, and PDF files to specified format.

    INPUTS: Paths to files or directories to convert. Can be multiple.
    """
    batch_convert(list(inputs), output, output_format)
    click.echo(f"Conversion complete. Output saved to: {output}")

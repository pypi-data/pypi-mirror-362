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
def main(inputs, output):
    """
    Convert PowerPoint, Word, Excel, and PDF files to plain text.

    INPUTS: Paths to files or directories to convert. Can be multiple.
    """
    batch_convert(list(inputs), output)
    click.echo(f"Conversion complete. Output saved to: {output}")

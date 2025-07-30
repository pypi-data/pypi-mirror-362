"""
Document Converter package for converting PowerPoint, Word, and PDF files to plain text.
"""

from .cli import main as cli_main
from .converter import batch_convert, convert_to_text

__all__ = ["convert_to_text", "batch_convert", "cli_main"]

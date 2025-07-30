"""
MCP Server Code Extractor - Core Library

A powerful code extraction library using tree-sitter for precise syntax analysis.
"""

from .models import CodeSymbol, Parameter, SymbolKind
from .extractor import CodeExtractor, create_extractor

__version__ = "0.2.0"
__all__ = ["CodeSymbol", "Parameter", "SymbolKind", "CodeExtractor", "create_extractor"]
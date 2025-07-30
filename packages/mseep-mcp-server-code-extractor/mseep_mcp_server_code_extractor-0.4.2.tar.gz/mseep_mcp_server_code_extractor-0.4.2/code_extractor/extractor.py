"""
Core code extraction engine using tree-sitter queries.

This replaces the manual tree traversal with a query-based approach
that properly distinguishes methods from functions and extracts rich context.
"""

import os
import re
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

from .models import CodeSymbol, Parameter, SymbolKind
from .languages import (
    get_language_for_file,
    get_tree_sitter_parser,
    get_tree_sitter_language,
    is_language_supported
)


class CodeExtractor:
    """
    Advanced code symbol extractor using tree-sitter queries.
    
    This class provides the core functionality for extracting code symbols
    with full context, solving the method vs function classification problem.
    """
    
    def __init__(self, language: str):
        """
        Initialize the extractor for a specific language.
        
        Args:
            language: Programming language name
            
        Raises:
            ValueError: If language is not supported
        """
        self.language = language
        self.parser = get_tree_sitter_parser(language)
        self.ts_language = get_tree_sitter_language(language)
        
        if not self.parser or not self.ts_language:
            raise ValueError(f"Language '{language}' is not supported")
            
        self.query = self._load_query(language)
    
    def _load_query(self, language: str) -> Optional[Any]:
        """Load tree-sitter query for the language."""
        query_file = Path(__file__).parent / "queries" / f"{language}.scm"
        
        if not query_file.exists():
            return None
            
        try:
            with open(query_file, 'r') as f:
                query_text = f.read()
            return self.ts_language.query(query_text)
        except Exception:
            return None
    
    def extract_symbols(self, source_code: str, depth: int = 0) -> List[CodeSymbol]:
        """
        Extract all symbols from source code with full context.
        
        Args:
            source_code: Source code string
            depth: Symbol extraction depth (0=everything, 1=top-level only, 2=classes+methods, etc.)
            
        Returns:
            List of CodeSymbol objects with rich context
        """
        if not self.query:
            return []
            
        try:
            source_bytes = source_code.encode('utf-8')
            tree = self.parser.parse(source_bytes)
            captures = self.query.captures(tree.root_node)
            
            # Process captures into symbols
            symbols_data = self._process_captures(captures, source_bytes)
            
            # Build hierarchical relationships
            symbols = self._build_symbol_hierarchy(symbols_data, source_bytes, depth=depth)
            
            return symbols
            
        except Exception as e:
            return [CodeSymbol(
                name="error",
                kind=SymbolKind.FUNCTION,
                start_line=1,
                end_line=1,
                start_byte=0,
                end_byte=0,
                docstring=f"Extraction failed: {str(e)}"
            )]
    
    def extract_function(self, source_code: str, function_name: str) -> Optional[CodeSymbol]:
        """
        Extract a specific function with full details.
        
        Args:
            source_code: Source code string
            function_name: Name of function to extract
            
        Returns:
            CodeSymbol for the function or None if not found
        """
        symbols = self.extract_symbols(source_code)
        for symbol in symbols:
            if symbol.name == function_name and symbol.kind in [SymbolKind.FUNCTION, SymbolKind.METHOD]:
                return symbol
        return None
    
    def extract_class(self, source_code: str, class_name: str) -> Optional[CodeSymbol]:
        """
        Extract a specific class with all its methods.
        
        Args:
            source_code: Source code string
            class_name: Name of class to extract
            
        Returns:
            CodeSymbol for the class or None if not found
        """
        symbols = self.extract_symbols(source_code)
        for symbol in symbols:
            if symbol.name == class_name and symbol.kind == SymbolKind.CLASS:
                return symbol
        return None
    
    def _process_captures(self, captures: List[Tuple], source_bytes: bytes) -> Dict[int, Dict[str, Any]]:
        """
        Process tree-sitter captures into symbol data.
        
        Args:
            captures: List of (node, capture_name) tuples
            source_bytes: Source code as bytes
            
        Returns:
            Dictionary mapping node IDs to symbol data
        """
        symbols_data = {}
        
        # First pass: collect all captures by symbol (using definition nodes as primary keys)
        symbol_captures = {}
        
        for node, capture_name in captures:
            if '.' in capture_name:
                symbol_type, capture_type = capture_name.split('.', 1)
                
                # Use definition nodes as the primary key for symbols
                if capture_type == 'definition':
                    symbol_id = node.id
                    if symbol_id not in symbol_captures:
                        symbol_captures[symbol_id] = {
                            'definition_node': node,
                            'captures': {},
                            'kind': None
                        }
                    symbol_captures[symbol_id]['captures'][capture_name] = node
                    
                    # Set symbol kind (prioritize more specific types)
                    current_kind = symbol_captures[symbol_id]['kind']
                    
                    if symbol_type == 'class':
                        symbol_captures[symbol_id]['kind'] = SymbolKind.CLASS
                    elif symbol_type in ['method', 'async_method', 'decorated_method']:
                        # Methods take priority over functions
                        symbol_captures[symbol_id]['kind'] = SymbolKind.METHOD
                    elif symbol_type in ['function', 'async_function', 'decorated_function']:
                        # Only set as function if not already a method
                        if current_kind != SymbolKind.METHOD:
                            symbol_captures[symbol_id]['kind'] = SymbolKind.FUNCTION
                    elif symbol_type == 'variable':
                        symbol_captures[symbol_id]['kind'] = SymbolKind.VARIABLE
                    elif symbol_type == 'import':
                        symbol_captures[symbol_id]['kind'] = SymbolKind.IMPORT
                    
        # Second pass: add name and other captures to existing symbols
        for node, capture_name in captures:
            if '.' in capture_name:
                symbol_type, capture_type = capture_name.split('.', 1)
                if capture_type != 'definition':
                    # Find the symbol whose definition contains this node
                    for symbol_id, symbol_data in symbol_captures.items():
                        definition_node = symbol_data['definition_node']
                        # Check if this node is within the definition node's range
                        # and if the symbol type matches
                        definition_capture_name = f"{symbol_type}.definition"
                        if (definition_capture_name in symbol_data['captures'] and
                            definition_node.start_byte <= node.start_byte < definition_node.end_byte):
                            symbol_data['captures'][capture_name] = node
                            break
        
        # Convert to the expected format
        for symbol_id, symbol_data in symbol_captures.items():
            symbols_data[symbol_id] = {
                'node': symbol_data['definition_node'],
                'captures': symbol_data['captures'],
                'kind': symbol_data['kind'],
                'parent_kind': None
            }
        
        return symbols_data
    
    def _build_symbol_hierarchy(self, symbols_data: Dict[int, Dict[str, Any]], source_bytes: bytes, depth: int = 1) -> List[CodeSymbol]:
        """
        Build CodeSymbol objects with hierarchical relationships.
        
        Args:
            symbols_data: Processed symbol data
            source_bytes: Source code as bytes
            depth: Symbol extraction depth (0=everything, 1=top-level only, 2=classes+methods, etc.)
            
        Returns:
            List of CodeSymbol objects
        """
        symbols = []
        
        for node_id, data in symbols_data.items():
            if not data['kind']:
                continue
                
            node = data['node']
            captures = data['captures']
            
            # Extract basic information
            name = self._extract_name(captures, source_bytes)
            if not name:
                continue
            
            # Use definition node for proper byte ranges
            definition_node = None
            for capture_name, capture_node in captures.items():
                if capture_name.endswith('.definition'):
                    definition_node = capture_node
                    break
            
            # Use definition node if available, otherwise use the name node
            range_node = definition_node if definition_node else node
            
            start_line = source_bytes[:range_node.start_byte].count(b'\n') + 1
            end_line = source_bytes[:range_node.end_byte].count(b'\n') + 1
            
            # Create symbol
            symbol = CodeSymbol(
                name=name,
                kind=data['kind'],
                start_line=start_line,
                end_line=end_line,
                start_byte=range_node.start_byte,
                end_byte=range_node.end_byte
            )
            
            # Extract detailed information based on kind
            if symbol.kind in [SymbolKind.FUNCTION, SymbolKind.METHOD]:
                self._extract_function_details(symbol, captures, source_bytes)
            elif symbol.kind == SymbolKind.CLASS:
                self._extract_class_details(symbol, captures, source_bytes)
            elif symbol.kind in [SymbolKind.VARIABLE, SymbolKind.CONSTANT]:
                self._extract_variable_details(symbol, captures, source_bytes)
            elif symbol.kind == SymbolKind.IMPORT:
                self._extract_import_details(symbol, captures, source_bytes)
            
            symbols.append(symbol)
        
        # Add parent relationships for methods
        self._add_parent_relationships(symbols)
        
        # Apply depth filtering if depth > 0
        if depth > 0:
            symbols = self._filter_by_depth(symbols, depth)
        
        return symbols
    
    def _extract_name(self, captures: Dict[str, Any], source_bytes: bytes) -> Optional[str]:
        """Extract symbol name from captures."""
        for capture_name, node in captures.items():
            if capture_name.endswith('.name'):
                return source_bytes[node.start_byte:node.end_byte].decode('utf-8')
        return None
    
    def _extract_function_details(self, symbol: CodeSymbol, captures: Dict[str, Any], source_bytes: bytes):
        """Extract function/method specific details."""
        # Check if async by looking at the function definition node
        definition_node = None
        for capture_name, node in captures.items():
            if capture_name.endswith('.definition'):
                definition_node = node
                break
        
        if definition_node:
            # Check if first child is 'async'
            if definition_node.children and definition_node.children[0].type == 'async':
                symbol.is_async = True
        
        # Extract parameters
        for capture_name, node in captures.items():
            if capture_name.endswith('.parameters'):
                symbol.parameters = self._parse_parameters(node, source_bytes)
                break
        
        # Extract return type
        for capture_name, node in captures.items():
            if capture_name.endswith('.return_type'):
                symbol.return_type = source_bytes[node.start_byte:node.end_byte].decode('utf-8')
                break
        
        # Extract docstring from function body if present
        if definition_node and definition_node.children:
            # Look for function body
            for child in definition_node.children:
                if child.type == 'block' and child.children:
                    first_stmt = child.children[0]
                    if (first_stmt.type == 'expression_statement' and 
                        first_stmt.children and 
                        first_stmt.children[0].type == 'string'):
                        docstring = source_bytes[first_stmt.children[0].start_byte:first_stmt.children[0].end_byte].decode('utf-8')
                        symbol.docstring = docstring.strip('"\'').strip()
                        break
    
    def _extract_class_details(self, symbol: CodeSymbol, captures: Dict[str, Any], source_bytes: bytes):
        """Extract class specific details."""
        # Extract docstring
        for capture_name, node in captures.items():
            if capture_name.endswith('.docstring'):
                docstring = source_bytes[node.start_byte:node.end_byte].decode('utf-8')
                docstring = docstring.strip('"\'').strip()
                if docstring:
                    symbol.docstring = docstring
                break
    
    def _extract_variable_details(self, symbol: CodeSymbol, captures: Dict[str, Any], source_bytes: bytes):
        """Extract variable/constant specific details."""
        # Determine if this is a constant (uppercase name)
        if symbol.name.isupper():
            symbol.kind = SymbolKind.CONSTANT
            
        # Extract type annotation
        for capture_name, node in captures.items():
            if capture_name.endswith('.type'):
                symbol.type_annotation = source_bytes[node.start_byte:node.end_byte].decode('utf-8')
                break
        
        # Extract value
        for capture_name, node in captures.items():
            if capture_name.endswith('.value'):
                value = source_bytes[node.start_byte:node.end_byte].decode('utf-8')
                # Truncate long values
                symbol.value = value[:100] + "..." if len(value) > 100 else value
                break
    
    def _extract_import_details(self, symbol: CodeSymbol, captures: Dict[str, Any], source_bytes: bytes):
        """Extract import specific details."""
        # This would be implemented for import handling
        pass
    
    def _parse_parameters(self, params_node: Any, source_bytes: bytes) -> List[Parameter]:
        """Parse function parameters from parameters node."""
        parameters = []
        
        # Simple parameter extraction - this could be enhanced with more sophisticated parsing
        params_text = source_bytes[params_node.start_byte:params_node.end_byte].decode('utf-8')
        
        # Remove parentheses and split by comma
        params_text = params_text.strip('()')
        if not params_text:
            return parameters
        
        for param in params_text.split(','):
            param = param.strip()
            if not param:
                continue
                
            # Parse parameter with type hints and defaults
            name = param
            type_hint = None
            default_value = None
            
            # Handle default values
            if '=' in param:
                name_part, default_value = param.split('=', 1)
                name = name_part.strip()
                default_value = default_value.strip()
            
            # Handle type hints
            if ':' in name:
                name_part, type_hint = name.split(':', 1)
                name = name_part.strip()
                type_hint = type_hint.strip()
            
            parameters.append(Parameter(
                name=name,
                type_hint=type_hint,
                default_value=default_value
            ))
        
        return parameters
    
    def _add_parent_relationships(self, symbols: List[CodeSymbol]):
        """Add parent relationships for methods inside classes."""
        # Sort by start position to enable proper nesting detection
        symbols.sort(key=lambda s: s.start_byte)
        
        class_stack = []
        
        for symbol in symbols:
            # Pop classes that this symbol is outside of
            while class_stack and class_stack[-1].end_byte < symbol.start_byte:
                class_stack.pop()
            
            # If we're inside a class and this is a method, set parent
            if class_stack and symbol.kind == SymbolKind.METHOD:
                symbol.parent = class_stack[-1].name
            
            # Push classes onto stack
            if symbol.kind == SymbolKind.CLASS:
                class_stack.append(symbol)
    
    def _filter_by_depth(self, symbols: List[CodeSymbol], depth: int) -> List[CodeSymbol]:
        """Filter symbols by nesting depth.
        
        Args:
            symbols: List of all symbols
            depth: Maximum depth to include (1=top-level only, 2=classes+methods, etc.)
            
        Returns:
            Filtered list of symbols
        """
        if depth == 0:
            return symbols
            
        # Calculate nesting depth for each symbol
        # Sort by start position to enable proper nesting detection
        sorted_symbols = sorted(symbols, key=lambda s: s.start_byte)
        
        filtered_symbols = []
        
        for symbol in sorted_symbols:
            symbol_depth = self._calculate_symbol_depth(symbol, sorted_symbols)
            
            if symbol_depth <= depth:
                filtered_symbols.append(symbol)
        
        return filtered_symbols
    
    def _calculate_symbol_depth(self, symbol: CodeSymbol, sorted_symbols: List[CodeSymbol]) -> int:
        """Calculate the nesting depth of a symbol.
        
        Args:
            symbol: Symbol to calculate depth for
            sorted_symbols: All symbols sorted by start position
            
        Returns:
            Nesting depth (1=top-level, 2=inside class, etc.)
        """
        depth = 1  # Start at depth 1 for top-level symbols
        
        # Count how many class symbols contain this symbol
        # Only classes count as depth-increasing containers for this use case
        for other in sorted_symbols:
            if (other != symbol and 
                other.start_byte <= symbol.start_byte and 
                other.end_byte >= symbol.end_byte and
                other.kind == SymbolKind.CLASS):
                depth += 1
        
        return depth


def create_extractor(file_path: str) -> CodeExtractor:
    """
    Create a CodeExtractor for a file.
    
    Args:
        file_path: Path to the source file
        
    Returns:
        CodeExtractor instance
        
    Raises:
        ValueError: If file language is not supported
    """
    language = get_language_for_file(file_path)
    return CodeExtractor(language)
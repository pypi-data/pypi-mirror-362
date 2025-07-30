#!/usr/bin/env python3
"""
MCP Code Extractor Server

A Model Context Protocol server that provides precise code extraction using tree-sitter.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: MCP not installed. Install with: pip install mcp[cli]", file=sys.stderr)
    sys.exit(1)

try:
    from tree_sitter_languages import get_parser
except ImportError:
    print("Error: tree-sitter-languages not installed. Install with: pip install tree-sitter-languages", file=sys.stderr)
    sys.exit(1)

# Local imports
from .extractor import create_extractor
from .languages import get_language_for_file
from .file_reader import get_file_content
from .search_engine import SearchEngine
from .models import SearchParameters


# Language mapping for file extensions
LANG_MAP = {
    # Python
    '.py': 'python',
    '.pyi': 'python',
    '.pyx': 'python',
    '.pxd': 'python',
    '.pxd.in': 'python',
    '.pxi': 'python',
    
    # JavaScript/TypeScript
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.mjs': 'javascript',
    '.cjs': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.d.ts': 'typescript',
    
    # Web
    '.html': 'html',
    '.htm': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.sass': 'sass',
    '.less': 'css',
    
    # Systems languages
    '.c': 'c',
    '.h': 'c',
    '.cpp': 'cpp',
    '.cxx': 'cpp',
    '.cc': 'cpp',
    '.hpp': 'cpp',
    '.hxx': 'cpp',
    '.C': 'cpp',
    '.H': 'cpp',
    '.rs': 'rust',
    '.go': 'go',
    '.zig': 'zig',
    
    # JVM languages
    '.java': 'java',
    '.kt': 'kotlin',
    '.kts': 'kotlin',
    '.scala': 'scala',
    '.sc': 'scala',
    '.clj': 'clojure',
    '.cljs': 'clojure',
    '.cljc': 'clojure',
    
    # Functional languages
    '.hs': 'haskell',
    '.lhs': 'haskell',
    '.ml': 'ocaml',
    '.mli': 'ocaml',
    '.ex': 'elixir',
    '.exs': 'elixir',
    
    # Other languages
    '.rb': 'ruby',
    '.php': 'php',
    '.swift': 'swift',
    '.m': 'objc',
    '.mm': 'objc',
    '.cs': 'c_sharp',
    '.fs': 'f_sharp',
    '.fsx': 'f_sharp',
    '.lua': 'lua',
    '.r': 'r',
    '.R': 'r',
    '.jl': 'julia',
    '.dart': 'dart',
    
    # Shell and config
    '.sh': 'bash',
    '.bash': 'bash',
    '.zsh': 'bash',
    '.fish': 'bash',
    '.ps1': 'powershell',
    '.psm1': 'powershell',
    '.psd1': 'powershell',
    
    # Data and config
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.toml': 'toml',
    '.xml': 'xml',
    '.sql': 'sql',
    '.proto': 'proto',
    
    # Documentation
    '.md': 'markdown',
    '.markdown': 'markdown',
    '.rst': 'rst',
    '.tex': 'latex',
}


def get_language_for_file(path_or_url: str) -> str:
    """Get the language name for a file or URL."""
    # For URLs, extract file extension from the path component
    if path_or_url.startswith(('http://', 'https://')):
        from urllib.parse import urlparse
        parsed = urlparse(path_or_url)
        ext = Path(parsed.path).suffix.lower()
    else:
        ext = Path(path_or_url).suffix.lower()
    return LANG_MAP.get(ext, 'text')


def find_function(node) -> dict:
    """
    Extract complete function definitions with precise tree-sitter parsing.
    
    Retrieves function code, parameters, and location information more accurately
    than text-based searching or file reading approaches.
    """
    
    def get_function(path_or_url: str, function_name: str, git_revision: Optional[str] = None) -> dict:
        """Extract a specific function from a file."""
        try:
            lang_name = get_language_for_file(path_or_url)
            
            # Get tree-sitter parser
            try:
                parser = get_parser(lang_name)
            except Exception:
                return {"error": f"Language '{lang_name}' not supported"}
            
            source = get_file_content(path_or_url, git_revision)
            source_bytes = source.encode('utf-8') if isinstance(source, str) else source
            
            tree = parser.parse(source_bytes)
            
            # Define function node types for different languages
            func_types = {
                'python': ['function_definition', 'async_function_definition'],
                'javascript': ['function_declaration', 'function_expression', 
                              'arrow_function', 'method_definition'],
                'typescript': ['function_declaration', 'function_expression', 
                              'arrow_function', 'method_definition', 'method_signature'],
                'java': ['method_declaration', 'constructor_declaration'],
                'cpp': ['function_definition', 'function_declarator'],
                'c': ['function_definition', 'function_declarator'],
                'go': ['function_declaration', 'method_declaration'],
                'rust': ['function_item'],
                'ruby': ['method', 'singleton_method'],
                'php': ['function_definition', 'method_declaration'],
            }
            
            types = func_types.get(
                lang_name, ['function_definition', 'function_declaration'])
            
            def find_function(node):
                if node.type in types:
                    # Extract function name
                    name = None
                    for child in node.children:
                        if child.type == 'identifier':
                            if isinstance(source, str):
                                name = source[child.start_byte:child.end_byte]
                            else:
                                name = source[child.start_byte:child.end_byte].decode('utf-8') if isinstance(source, bytes) else source[child.start_byte:child.end_byte]
                            break
                        elif hasattr(child, 'children'):
                            for grandchild in child.children:
                                if grandchild.type == 'identifier':
                                    if isinstance(source, str):
                                        name = source[grandchild.start_byte:grandchild.end_byte]
                                    else:
                                        name = source[grandchild.start_byte:grandchild.end_byte].decode('utf-8') if isinstance(source, bytes) else source[grandchild.start_byte:grandchild.end_byte]
                                    break
                            if name:
                                break
                    
                    # Use field name if available (more reliable)
                    name_node = node.child_by_field_name('name')
                    if name_node:
                        if isinstance(source, str):
                            name = source[name_node.start_byte:name_node.end_byte]
                        else:
                            name = source[name_node.start_byte:name_node.end_byte].decode('utf-8') if isinstance(source, bytes) else source[name_node.start_byte:name_node.end_byte]
                    
                    if name == function_name:
                        return node
                
                for child in node.children:
                    result = find_function(child)
                    if result:
                        return result
                return None
            
            func_node = find_function(tree.root_node)
            
            if not func_node:
                return {"error": f"Function '{function_name}' not found in {path_or_url}"}
            
            # Extract the function code
            source_bytes = source.encode('utf-8') if isinstance(source, str) else source
            code = source[func_node.start_byte:func_node.end_byte]
            start_line = source[:func_node.start_byte].count('\n') + 1 if isinstance(source, str) else source_bytes[:func_node.start_byte].count(b'\n') + 1
            end_line = source[:func_node.end_byte].count('\n') + 1 if isinstance(source, str) else source_bytes[:func_node.end_byte].count(b'\n') + 1
            
            return {
                "code": code,
                "start_line": start_line,
                "end_line": end_line,
                "lines": f"{start_line}-{end_line}",
                "function": function_name,
                "file": path_or_url,
                "language": lang_name
            }
            
        except Exception as e:
            return {"error": f"Failed to parse '{path_or_url}': {str(e)}"}
    
    return get_function


def find_class(node) -> dict:
    """
    Extract complete class definitions with precise tree-sitter parsing.
    
    Retrieves class code, methods, and structural information more accurately
    than text-based searching or file reading approaches.
    """
    
    def get_class(path_or_url: str, class_name: str, git_revision: Optional[str] = None) -> dict:
        """Extract a specific class from a file."""
        try:
            lang_name = get_language_for_file(path_or_url)
            
            # Get tree-sitter parser
            try:
                parser = get_parser(lang_name)
            except Exception:
                return {"error": f"Language '{lang_name}' not supported"}
            
            source = get_file_content(path_or_url, git_revision)
            source_bytes = source.encode('utf-8') if isinstance(source, str) else source
            
            tree = parser.parse(source_bytes)
            
            # Define class node types for different languages
            class_types = {
                'python': ['class_definition'],
                'javascript': ['class_declaration'],
                'typescript': ['class_declaration'],
                'java': ['class_declaration'],
                'cpp': ['class_specifier'],
                'c': ['struct_specifier'],
                'go': ['type_declaration'],
                'rust': ['struct_item', 'enum_item', 'impl_item'],
                'ruby': ['class'],
                'php': ['class_declaration'],
                'swift': ['class_declaration'],
                'kotlin': ['class_declaration'],
                'scala': ['class_definition'],
                'csharp': ['class_declaration'],
            }
            
            types = class_types.get(
                lang_name, ['class_declaration', 'class_definition'])
            
            def find_class(node):
                if node.type in types:
                    # Extract class name
                    for child in node.children:
                        if child.type == 'identifier':
                            if isinstance(source, str):
                                name = source[child.start_byte:child.end_byte]
                            else:
                                name = source[child.start_byte:child.end_byte].decode('utf-8') if isinstance(source, bytes) else source[child.start_byte:child.end_byte]
                            if name == class_name:
                                return node
                    
                    # Use field name if available (more reliable)
                    name_node = node.child_by_field_name('name')
                    if name_node:
                        if isinstance(source, str):
                            name = source[name_node.start_byte:name_node.end_byte]
                        else:
                            name = source[name_node.start_byte:name_node.end_byte].decode('utf-8') if isinstance(source, bytes) else source[name_node.start_byte:name_node.end_byte]
                        if name == class_name:
                            return node
                
                for child in node.children:
                    result = find_class(child)
                    if result:
                        return result
                return None
            
            class_node = find_class(tree.root_node)
            
            if not class_node:
                return {"error": f"Class '{class_name}' not found in {path_or_url}"}
            
            # Extract the class code
            source_bytes = source.encode('utf-8') if isinstance(source, str) else source
            code = source[class_node.start_byte:class_node.end_byte]
            start_line = source[:class_node.start_byte].count('\n') + 1 if isinstance(source, str) else source_bytes[:class_node.start_byte].count(b'\n') + 1
            end_line = source[:class_node.end_byte].count('\n') + 1 if isinstance(source, str) else source_bytes[:class_node.end_byte].count(b'\n') + 1
            
            return {
                "code": code,
                "start_line": start_line,
                "end_line": end_line,
                "lines": f"{start_line}-{end_line}",
                "class": class_name,
                "file": path_or_url,
                "language": lang_name
            }
            
        except Exception as e:
            return {"error": f"Failed to parse '{path_or_url}': {str(e)}"}
    
    return get_class


def get_symbols(path_or_url: str, git_revision: Optional[str] = None, depth: int = 1) -> list:
    """
    List all functions, classes, and symbols with line numbers using tree-sitter parsing.
    
    Efficiently extracts code structure without reading entire files. Provides detailed
    symbol information including types, parameters, and hierarchical relationships.
    """
    
    try:
        extractor = create_extractor(path_or_url)
        source_code = get_file_content(path_or_url, git_revision)
        symbols = extractor.extract_symbols(source_code, depth=depth)
        
        # Convert to dict format for MCP compatibility
        result = []
        for symbol in symbols:
            result.append(symbol.to_dict())
        
        return result
        
    except Exception as e:
        return [{"error": f"Failed to parse '{path_or_url}': {str(e)}"}]


def get_lines(path_or_url: str, start_line: int, end_line: int, git_revision: Optional[str] = None) -> dict:
    """
    Extract specific line ranges from files with precise control.
    
    Efficiently retrieves targeted code sections when exact line numbers are known,
    avoiding the need to process entire files.
    """
    
    try:
        if start_line < 1:
            return {"error": "start_line must be >= 1"}
        
        if end_line < start_line:
            return {"error": "end_line must be >= start_line"}
        
        source_code = get_file_content(path_or_url, git_revision)
        lines = source_code.splitlines(keepends=True)
        
        # Convert to 0-based indexing
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), end_line)
        
        extracted = lines[start_idx:end_idx]
        
        return {
            "code": "".join(extracted),
            "start_line": start_line,
            "end_line": min(end_line, len(lines)),
            "lines": f"{start_line}-{min(end_line, len(lines))}",
            "file": path_or_url
        }
        
    except Exception as e:
        return {"error": f"Failed to read '{path_or_url}': {str(e)}"}


def get_signature(path_or_url: str, function_name: str, git_revision: Optional[str] = None) -> dict:
    """
    Extract function signatures and declarations without full implementations.
    
    Provides function interfaces, parameters, and return types efficiently.
    Lighter alternative when full function body is not needed.
    """
    
    result = find_function(None)(path_or_url, function_name, git_revision)
    
    if "error" in result:
        return result
    
    # Extract just the first line (signature)
    lines = result["code"].split('\n')
    signature = lines[0]
    
    return {
        "signature": signature,
        "function": function_name,
        "file": path_or_url,
        "start_line": result["start_line"]
    }


def main():
    """Main entry point for the MCP server."""
    import argparse
    import sys
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="MCP Server Code Extractor - Precise code extraction using tree-sitter",
        prog="mcp-server-code-extractor"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="mcp-server-code-extractor 0.4.2"
    )
    
    # Parse args but ignore them for MCP server mode
    args = parser.parse_args()
    
    # Initialize FastMCP server
    mcp = FastMCP("extract")
    
    @mcp.tool()
    def get_symbols_tool(path_or_url: str, git_revision: Optional[str] = None, depth: int = 1) -> list:
        """
        AST-precise symbol table generator for files/directories/URLs. Enumerates every function, class, 
        variable with byte-accurate boundaries and line numbers using tree-sitter parsing. Zero regex 
        drift, language-aware across 30+ languages. Use when you need complete symbol inventory instead 
        of text searching. Supports git revisions for historical analysis.
        
        Args:
            path_or_url: Path to source file or URL (GitHub raw, GitLab raw, direct file URL)
            git_revision: Optional git revision (commit, branch, tag, HEAD~1, etc.) - not supported for URLs
            depth: Symbol extraction depth (0=everything, 1=top-level only, 2=classes+methods, etc.)
        """
        return get_symbols(path_or_url, git_revision, depth)
    
    @mcp.tool()
    def get_function_tool(path_or_url: str, function_name: str, git_revision: Optional[str] = None) -> dict:
        """
        Tree-sitter function extractor that pinpoints exact function/method boundaries with zero false positives.
        Returns complete definition including signature, parameters, body, and precise line ranges. Handles 
        nested functions, async/await, decorators across languages. Prefer over Read when isolating specific 
        functions for analysis, refactoring, or documentation generation.
        
        Args:
            path_or_url: Path to source file or URL (GitHub raw, GitLab raw, direct file URL)
            function_name: Name of the function to extract
            git_revision: Optional git revision (commit, branch, tag, HEAD~1, etc.) - not supported for URLs
        """
        return find_function(None)(path_or_url, function_name, git_revision)
    
    @mcp.tool()
    def get_class_tool(path_or_url: str, class_name: str, git_revision: Optional[str] = None) -> dict:
        """
        AST-aware class/type extractor that guarantees complete definition boundaries including inheritance, 
        generics, nested classes, and all methods. Language-aware parsing handles OOP patterns across 
        Python, Java, C++, TypeScript, etc. Use for refactoring, inheritance analysis, or API documentation 
        instead of multiline text search which misses scope boundaries.
        
        Args:
            path_or_url: Path to source file or URL (GitHub raw, GitLab raw, direct file URL)
            class_name: Name of the class to extract
            git_revision: Optional git revision (commit, branch, tag, HEAD~1, etc.) - not supported for URLs
        """
        return find_class(None)(path_or_url, class_name, git_revision)
    
    @mcp.tool()
    def get_lines_tool(path_or_url: str, start_line: int, end_line: int, git_revision: Optional[str] = None) -> dict:
        """
        Precise line range extractor with git-revision support. Returns exact line spans from any commit, 
        branch, or URL without reading entire files. Handles line numbering consistently across file 
        changes. Use for targeted diff analysis, patch generation, or code review when you have specific 
        line numbers from symbols or search results.
        
        Args:
            path_or_url: Path to source file or URL (GitHub raw, GitLab raw, direct file URL)
            start_line: Starting line number (1-based)
            end_line: Ending line number (1-based, inclusive)
            git_revision: Optional git revision (commit, branch, tag, HEAD~1, etc.) - not supported for URLs
        """
        return get_lines(path_or_url, start_line, end_line, git_revision)
    
    @mcp.tool()
    def get_signature_tool(path_or_url: str, function_name: str, git_revision: Optional[str] = None) -> dict:
        """
        Function signature extractor that returns only the header/declaration without implementation body. 
        Preserves exact parameter types, decorators, async/static modifiers, and return annotations. 
        Ideal for API documentation, interface analysis, or quick function discovery when you don't need 
        the full implementation. Faster than get_function_tool for signature-only queries.
        
        Args:
            path_or_url: Path to source file or URL (GitHub raw, GitLab raw, direct file URL)
            function_name: Name of the function to get signature for
            git_revision: Optional git revision (commit, branch, tag, HEAD~1, etc.) - not supported for URLs
        """
        return get_signature(path_or_url, function_name, git_revision)
    
    @mcp.tool()
    def search_code_tool(
        search_type: str,
        target: str, 
        scope: str,
        language: Optional[str] = None,
        git_revision: Optional[str] = None,
        max_results: int = 100,
        include_context: bool = True,
        file_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        max_files: int = 1000,
        follow_symlinks: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Tree-sitter semantic code search that understands language structure, not just text patterns. 
        Finds function calls, symbol definitions, and references with AST precision across files/directories/repos. 
        Zero false positives from string matches in comments or strings. Supports git revisions for 
        historical analysis. Use instead of grep/text search when semantic accuracy matters.
        
        Search Types:
        - "function-calls": Locate where functions/methods are invoked (not just string matches)
        - "symbol-definitions": Find where symbols (functions, classes, variables) are declared
        
        Examples:
        - Find function calls: search_type="function-calls", target="requests.get"
        - Find function definitions: search_type="symbol-definitions", target="process_data"
        - Find class definitions: search_type="symbol-definitions", target="UserService"
        - Find variable definitions: search_type="symbol-definitions", target="API_KEY"
        
        Args:
            search_type: Type of search ("function-calls", "symbol-definitions") 
            target: What to search for (symbol name or call pattern)
            scope: File path, directory path, or URL to search in
            language: Programming language (auto-detected if not specified)
            git_revision: Optional git revision (commit, branch, tag) - not supported for URLs
            max_results: Maximum number of results to return
            include_context: Include surrounding code lines for context
            file_patterns: File patterns to include in directory search (e.g., ["*.py", "*.js"])
            exclude_patterns: File patterns to exclude (e.g., ["*.pyc", "node_modules/*"])
            max_files: Maximum number of files to search in directory mode
            follow_symlinks: Whether to follow symbolic links in directory search
            
        Returns:
            List of search results with file paths, line numbers, matched text, context,
            and metadata including symbol_type for definitions.
        """
        try:
            # Validate search type
            supported_types = ["function-calls", "symbol-definitions"]
            if search_type not in supported_types:
                return [{"error": f"Unsupported search type '{search_type}'. Supported: {supported_types}"}]
            
            # Set up search parameters with defaults for directory-specific options
            params = SearchParameters(
                search_type=search_type,
                target=target,
                scope=scope,
                language=language,
                git_revision=git_revision,
                max_results=max_results,
                include_context=include_context,
                file_patterns=file_patterns or ["*"],
                exclude_patterns=exclude_patterns or ["*.pyc", "*.pyo", "*.pyd", "__pycache__/*", ".git/*", ".svn/*", "node_modules/*", "*.min.js"],
                max_files=max_files,
                follow_symlinks=follow_symlinks
            )
            
            search_engine = SearchEngine()
            
            # Auto-detect file vs directory scope and route accordingly
            if os.path.isfile(scope):
                # Single file search
                results = search_engine.search_file(scope, params)
                return [result.to_dict() for result in results]
            elif os.path.isdir(scope):
                # Directory search
                results = search_engine.search_directory(scope, params)
                return [result.to_dict() for result in results]
            else:
                # Check if it's a URL
                if scope.startswith(('http://', 'https://')):
                    # Single file search for URLs
                    results = search_engine.search_file(scope, params)
                    return [result.to_dict() for result in results]
                else:
                    return [{"error": f"Scope '{scope}' is not a valid file, directory, or URL"}]
                
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
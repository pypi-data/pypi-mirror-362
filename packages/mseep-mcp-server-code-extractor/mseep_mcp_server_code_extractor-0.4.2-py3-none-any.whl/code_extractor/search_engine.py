"""
Semantic code search engine using tree-sitter parsing.

Provides sophisticated pattern matching beyond simple text search,
leveraging syntax tree structure for accurate code understanding.
"""

from typing import List, Optional, Dict, Any, Set, Tuple
from pathlib import Path
import os
import fnmatch
from tree_sitter import Node, Query
from tree_sitter_languages import get_parser, get_language

from .models import SearchResult, SearchParameters
from .file_reader import get_file_content
from .languages import get_language_for_file


class SearchEngine:
    """
    Core search engine that executes tree-sitter queries against code files.
    
    Supports caching of parsed ASTs and compiled queries for performance.
    """
    
    def __init__(self):
        self._ast_cache: Dict[str, Any] = {}  # file_hash -> parsed_tree
        self._query_cache: Dict[str, Query] = {}  # (lang, pattern) -> compiled_query
    
    def search_file(self, file_path: str, params: SearchParameters) -> List[SearchResult]:
        """Search a single file for the specified pattern."""
        try:
            # Get language
            lang_name = params.language or get_language_for_file(file_path)
            if lang_name == 'text':
                return []  # Skip unsupported languages
            
            # Get file content
            source_code = get_file_content(file_path, params.git_revision)
            if not source_code.strip():
                return []
            
            # Get or create parser
            parser = get_parser(lang_name)
            tree = parser.parse(source_code.encode('utf-8'))
            
            # Route to appropriate search method
            if params.search_type == "function-calls":
                return self._search_function_calls(file_path, source_code, tree, params, lang_name)
            elif params.search_type == "symbol-definitions":
                return self._search_symbol_definitions(file_path, source_code, tree, params, lang_name)
            
            return []
            
        except Exception as e:
            # Log error but don't crash
            print(f"Error searching {file_path}: {e}")
            return []
    
    def search_directory(self, directory_path: str, params: SearchParameters) -> List[SearchResult]:
        """Search all matching files in a directory tree."""
        try:
            dir_path = Path(directory_path)
            if not dir_path.exists() or not dir_path.is_dir():
                print(f"Directory not found or not a directory: {directory_path}")
                return []
            
            # Get all matching files
            matching_files = self._find_matching_files(dir_path, params)
            
            if len(matching_files) > params.max_files:
                print(f"Found {len(matching_files)} files, limiting to {params.max_files}")
                matching_files = matching_files[:params.max_files]
            
            # Search each file and aggregate results
            all_results = []
            for file_path in matching_files:
                try:
                    file_results = self.search_file(str(file_path), params)
                    all_results.extend(file_results)
                    
                    # Check if we've hit the max results limit
                    if len(all_results) >= params.max_results:
                        all_results = all_results[:params.max_results]
                        break
                        
                except Exception as e:
                    print(f"Error searching file {file_path}: {e}")
                    continue
            
            # Deduplicate and sort results
            return self._deduplicate_results(all_results)
            
        except Exception as e:
            print(f"Error searching directory {directory_path}: {e}")
            return []
    
    def _search_function_calls(self, file_path: str, source_code: str, tree: Any, 
                             params: SearchParameters, lang_name: str) -> List[SearchResult]:
        """Search for function calls in the parsed tree."""
        results = []
        
        # Define query patterns for different languages
        patterns = {
            'python': '''
                ; Method calls like obj.method()
                (call
                  function: (attribute
                    (identifier) @module
                    (identifier) @function
                  )
                ) @call
                
                ; Simple function calls like func()
                (call
                  function: (identifier) @simple_function
                ) @simple_call
            ''',
            'javascript': '''
                ; Method calls like obj.method()
                (call_expression
                  function: (member_expression
                    object: (identifier) @module  
                    property: (property_identifier) @function
                  )
                ) @call
                
                ; Simple function calls like func()
                (call_expression
                  function: (identifier) @simple_function
                ) @simple_call
            ''',
            'typescript': '''
                ; Method calls like obj.method()
                (call_expression
                  function: (member_expression
                    object: (identifier) @module  
                    property: (property_identifier) @function
                  )
                ) @call
                
                ; Simple function calls like func()
                (call_expression
                  function: (identifier) @simple_function
                ) @simple_call
            '''
        }
        
        pattern = patterns.get(lang_name)
        if not pattern:
            return []
        
        # Compile and execute query
        query = self._get_compiled_query(lang_name, pattern)
        captures = query.captures(tree.root_node)
        
        source_lines = source_code.splitlines()
        
        for node, capture_name in captures:
            if capture_name in ['call', 'simple_call']:
                # Check if this matches our target
                call_text = source_code[node.start_byte:node.end_byte]
                if params.target in call_text:
                    start_line = node.start_point[0] + 1
                    end_line = node.end_point[0] + 1
                    
                    # Get context lines
                    context_before = []
                    context_after = []
                    if params.include_context:
                        start_ctx = max(0, start_line - 1 - params.context_lines)
                        end_ctx = min(len(source_lines), end_line + params.context_lines)
                        context_before = source_lines[start_ctx:start_line-1]
                        context_after = source_lines[end_line:end_ctx]
                    
                    result = SearchResult(
                        file_path=file_path,
                        start_line=start_line,
                        end_line=end_line,
                        match_text=call_text,
                        context_before=context_before,
                        context_after=context_after,
                        metadata={"search_type": params.search_type, "target": params.target},
                        language=lang_name
                    )
                    results.append(result)
                    
                    if len(results) >= params.max_results:
                        break
        
        return results
    
    def _search_symbol_definitions(self, file_path: str, source_code: str, tree: Any, 
                                 params: SearchParameters, lang_name: str) -> List[SearchResult]:
        """Search for symbol definitions (classes, functions, variables) in the parsed tree."""
        results = []
        
        # Define query patterns for different languages
        patterns = {
            'python': '''
                ; Function definitions
                (function_definition
                  name: (identifier) @function_name
                ) @function_def
                
                ; Class definitions
                (class_definition
                  name: (identifier) @class_name
                ) @class_def
                
                ; Variable assignments
                (assignment
                  left: (identifier) @variable_name
                ) @variable_def
            ''',
            'javascript': '''
                ; Function declarations
                (function_declaration
                  name: (identifier) @function_name
                ) @function_def
                
                ; Class declarations
                (class_declaration
                  name: (identifier) @class_name
                ) @class_def
                
                ; Variable declarations
                (variable_declaration
                  (variable_declarator
                    name: (identifier) @variable_name
                  )
                ) @variable_def
                
                ; Const declarations
                (lexical_declaration
                  (variable_declarator
                    name: (identifier) @variable_name
                  )
                ) @const_def
            ''',
            'typescript': '''
                ; Function declarations
                (function_declaration
                  name: (identifier) @function_name
                ) @function_def
                
                ; Class declarations
                (class_declaration
                  name: (identifier) @class_name
                ) @class_def
                
                ; Interface declarations
                (interface_declaration
                  name: (type_identifier) @interface_name
                ) @interface_def
                
                ; Type alias declarations
                (type_alias_declaration
                  name: (type_identifier) @type_name
                ) @type_def
                
                ; Variable declarations
                (variable_declaration
                  (variable_declarator
                    name: (identifier) @variable_name
                  )
                ) @variable_def
                
                ; Const declarations
                (lexical_declaration
                  (variable_declarator
                    name: (identifier) @variable_name
                  )
                ) @const_def
            '''
        }
        
        pattern = patterns.get(lang_name)
        if not pattern:
            return []
        
        # Compile and execute query
        query = self._get_compiled_query(lang_name, pattern)
        captures = query.captures(tree.root_node)
        
        source_lines = source_code.splitlines()
        
        for node, capture_name in captures:
            if capture_name.endswith('_def'):
                # Check if this symbol name matches our target
                symbol_text = source_code[node.start_byte:node.end_byte]
                
                # For symbol definitions, we want to check if the target appears in the symbol
                if params.target in symbol_text:
                    start_line = node.start_point[0] + 1
                    end_line = node.end_point[0] + 1
                    
                    # Get context lines
                    context_before = []
                    context_after = []
                    if params.include_context:
                        start_ctx = max(0, start_line - 1 - params.context_lines)
                        end_ctx = min(len(source_lines), end_line + params.context_lines)
                        context_before = source_lines[start_ctx:start_line-1]
                        context_after = source_lines[end_line:end_ctx]
                    
                    # Determine symbol type from capture name
                    symbol_type = capture_name.replace('_def', '').replace('_name', '')
                    
                    result = SearchResult(
                        file_path=file_path,
                        start_line=start_line,
                        end_line=end_line,
                        match_text=symbol_text,
                        context_before=context_before,
                        context_after=context_after,
                        metadata={
                            "search_type": params.search_type, 
                            "target": params.target,
                            "symbol_type": symbol_type
                        },
                        language=lang_name
                    )
                    results.append(result)
                    
                    if len(results) >= params.max_results:
                        break
        
        return results
    
    def _get_compiled_query(self, language: str, pattern: str) -> Query:
        """Get or compile a tree-sitter query."""
        cache_key = f"{language}:{hash(pattern)}"
        if cache_key not in self._query_cache:
            language_obj = get_language(language)
            self._query_cache[cache_key] = language_obj.query(pattern)
        return self._query_cache[cache_key]
    
    def _find_matching_files(self, dir_path: Path, params: SearchParameters) -> List[Path]:
        """Find all files in directory that match the search criteria."""
        matching_files = []
        
        try:
            # Use rglob to recursively find files
            if params.follow_symlinks:
                all_files = [f for f in dir_path.rglob("*") if f.is_file()]
            else:
                all_files = [f for f in dir_path.rglob("*") if f.is_file() and not f.is_symlink()]
            
            for file_path in all_files:
                # Check if file matches include patterns
                if not self._matches_patterns(file_path.name, params.file_patterns):
                    continue
                
                # Check if file matches exclude patterns
                if self._matches_patterns(str(file_path.relative_to(dir_path)), params.exclude_patterns):
                    continue
                
                # Skip binary files
                if self._is_binary_file(file_path):
                    continue
                
                matching_files.append(file_path)
                
        except PermissionError as e:
            print(f"Permission denied accessing {dir_path}: {e}")
        except Exception as e:
            print(f"Error finding files in {dir_path}: {e}")
        
        return matching_files
    
    def _matches_patterns(self, file_path: str, patterns: List[str]) -> bool:
        """Check if file path matches any of the given patterns."""
        for pattern in patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        return False
    
    def _is_binary_file(self, file_path: Path) -> bool:
        """Check if file is binary by reading a small sample."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\0' in chunk
        except Exception:
            return True  # If we can't read it, treat as binary
    
    def _deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Remove duplicate results and sort by relevance."""
        seen: Set[Tuple[str, int, str]] = set()
        unique_results = []
        
        for result in results:
            # Create a unique key based on file, line, and match text
            key = (result.file_path, result.start_line, result.match_text.strip())
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        # Sort by file path, then by line number
        unique_results.sort(key=lambda r: (r.file_path, r.start_line))
        
        return unique_results
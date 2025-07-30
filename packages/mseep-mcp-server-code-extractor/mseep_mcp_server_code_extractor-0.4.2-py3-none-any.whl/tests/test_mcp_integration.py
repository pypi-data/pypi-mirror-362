"""
MCP tool integration tests for search_code_tool.

Tests the auto-detection logic, parameter validation, 
and error handling for the MCP server integration.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch
from typing import List, Dict, Any, Optional

from code_extractor.models import SearchParameters, SearchResult
from code_extractor.search_engine import SearchEngine


def search_code_tool_implementation(
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
    """Test implementation of search_code_tool identical to server.py"""
    try:
        # Validate search type
        supported_types = ["function-calls"]
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


class TestMCPSearchToolIntegration:
    """Test MCP search_code_tool integration and auto-detection."""
    
    def test_file_vs_directory_auto_detection(self, tmp_path):
        """Test automatic detection of file vs directory scope."""
        # Create test file and directory
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")
        
        test_dir = tmp_path / "project"
        test_dir.mkdir()
        (test_dir / "main.py").write_text("print('main')")
        
        # Test file detection 
        result = search_code_tool_implementation(
            search_type="function-calls",
            target="print",
            scope=str(test_file)
        )
        
        assert isinstance(result, list)
        assert len(result) >= 1
        assert "file_path" in result[0]
        
        # Test directory detection
        result = search_code_tool_implementation(
            search_type="function-calls", 
            target="print",
            scope=str(test_dir)
        )
        
        assert isinstance(result, list)
        assert len(result) >= 1
        assert "file_path" in result[0]
    
    def test_url_detection(self):
        """Test URL detection in scope parameter."""
        with patch('code_extractor.search_engine.SearchEngine.search_file') as mock_search:
            mock_search.return_value = []
            
            # Test HTTP URL
            result = search_code_tool_implementation(
                search_type="function-calls",
                target="print",
                scope="https://raw.githubusercontent.com/user/repo/main/file.py"
            )
            
            assert isinstance(result, list)
            mock_search.assert_called_once()
            
            # Test HTTPS URL
            mock_search.reset_mock()
            result = search_code_tool_implementation(
                search_type="function-calls",
                target="print", 
                scope="http://example.com/code.py"
            )
            
            assert isinstance(result, list)
            mock_search.assert_called_once()
    
    def test_invalid_scope_handling(self):
        """Test handling of invalid scope paths."""
        result = search_code_tool_implementation(
            search_type="function-calls",
            target="print",
            scope="/nonexistent/path"
        )
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]
        assert "not a valid file, directory, or URL" in result[0]["error"]
    
    def test_unsupported_search_type(self):
        """Test handling of unsupported search types."""
        result = search_code_tool_implementation(
            search_type="unsupported-type",
            target="print",
            scope="test.py"
        )
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]
        assert "Unsupported search type" in result[0]["error"]
    
    def test_parameter_defaults(self, tmp_path):
        """Test default parameter values."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('test')")
        
        with patch('code_extractor.search_engine.SearchEngine.search_file') as mock_search:
            mock_search.return_value = []
            
            result = search_code_tool_implementation(
                search_type="function-calls",
                target="print",
                scope=str(test_file)
            )
            
            # Check that SearchParameters was called with correct defaults
            args, kwargs = mock_search.call_args
            params = args[1]  # Second argument is SearchParameters
            
            assert isinstance(params, SearchParameters)
            assert params.search_type == "function-calls"
            assert params.target == "print"
            assert params.scope == str(test_file)
            assert params.max_results == 100
            assert params.include_context == True
            assert params.file_patterns == ["*"]
            assert "*.pyc" in params.exclude_patterns
            assert params.max_files == 1000
            assert params.follow_symlinks == False
    
    def test_custom_directory_parameters(self, tmp_path):
        """Test custom directory search parameters."""
        test_dir = tmp_path / "project"
        test_dir.mkdir()
        (test_dir / "test.py").write_text("print('test')")
        
        with patch('code_extractor.search_engine.SearchEngine.search_directory') as mock_search:
            mock_search.return_value = []
            
            result = search_code_tool_implementation(
                search_type="function-calls",
                target="print",
                scope=str(test_dir),
                file_patterns=["*.py", "*.js"],
                exclude_patterns=["test_*", "*.pyc"],
                max_files=500,
                max_results=50,
                follow_symlinks=True
            )
            
            # Check that custom parameters were passed correctly
            args, kwargs = mock_search.call_args
            params = args[1]  # Second argument is SearchParameters
            
            assert params.file_patterns == ["*.py", "*.js"]
            assert params.exclude_patterns == ["test_*", "*.pyc"]
            assert params.max_files == 500
            assert params.max_results == 50
            assert params.follow_symlinks == True
    
    def test_error_handling_in_search(self, tmp_path):
        """Test error handling during search execution."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('test')")
        
        with patch('code_extractor.search_engine.SearchEngine.search_file') as mock_search:
            mock_search.side_effect = Exception("Search failed")
            
            result = search_code_tool_implementation(
                search_type="function-calls",
                target="print",
                scope=str(test_file)
            )
            
            assert isinstance(result, list)
            assert len(result) == 1
            assert "error" in result[0]
            assert "Search failed" in result[0]["error"]
    
    def test_result_format_conversion(self, tmp_path):
        """Test that SearchResult objects are properly converted to dict format."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('test')")
        
        # Mock search result
        mock_result = SearchResult(
            file_path=str(test_file),
            start_line=1,
            end_line=1,
            match_text="print('test')",
            context_before=["# Comment"],
            context_after=[""],
            metadata={"search_type": "function-calls"},
            language="python"
        )
        
        with patch('code_extractor.search_engine.SearchEngine.search_file') as mock_search:
            mock_search.return_value = [mock_result]
            
            result = search_code_tool_implementation(
                search_type="function-calls",
                target="print",
                scope=str(test_file)
            )
            
            assert isinstance(result, list)
            assert len(result) == 1
            
            result_dict = result[0]
            assert isinstance(result_dict, dict)
            assert result_dict["file_path"] == str(test_file)
            assert result_dict["start_line"] == 1
            assert result_dict["end_line"] == 1
            assert result_dict["match_text"] == "print('test')"
            assert result_dict["context_before"] == ["# Comment"]
            assert result_dict["context_after"] == [""]
            assert result_dict["metadata"] == {"search_type": "function-calls"}
            assert result_dict["language"] == "python"


class TestParameterValidation:
    """Test parameter validation and edge cases."""
    
    def test_none_parameters(self, tmp_path):
        """Test handling of None parameters."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('test')")
        
        with patch('code_extractor.search_engine.SearchEngine.search_file') as mock_search:
            mock_search.return_value = []
            
            # Test with None file_patterns and exclude_patterns
            result = search_code_tool_implementation(
                search_type="function-calls",
                target="print",
                scope=str(test_file),
                file_patterns=None,
                exclude_patterns=None
            )
            
            # Should use defaults
            args, kwargs = mock_search.call_args
            params = args[1]
            assert params.file_patterns == ["*"]
            assert "*.pyc" in params.exclude_patterns
    
    def test_empty_string_parameters(self):
        """Test handling of empty string parameters."""
        result = search_code_tool_implementation(
            search_type="",  # Empty search type
            target="print",
            scope="test.py"
        )
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert "error" in result[0]
        assert "Unsupported search type" in result[0]["error"]
    
    def test_boundary_values(self, tmp_path):
        """Test boundary values for numeric parameters."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('test')")
        
        with patch('code_extractor.search_engine.SearchEngine.search_file') as mock_search:
            mock_search.return_value = []
            
            # Test with extreme values
            result = search_code_tool_implementation(
                search_type="function-calls",
                target="print",
                scope=str(test_file),
                max_results=0,  # Minimum
                max_files=1    # Minimum
            )
            
            args, kwargs = mock_search.call_args
            params = args[1]
            assert params.max_results == 0
            assert params.max_files == 1


class TestBackwardCompatibility:
    """Test that directory search doesn't break existing functionality."""
    
    def test_single_file_search_unchanged(self, tmp_path):
        """Test that single file search behavior is unchanged."""
        test_file = tmp_path / "test.py"
        test_file.write_text("""
def test_function():
    print('test')
    get_file_content('data.json')
    return True
""")
        
        # Test single file search
        result = search_code_tool_implementation(
            search_type="function-calls",
            target="print",
            scope=str(test_file)
        )
        
        assert isinstance(result, list)
        assert len(result) >= 1
        
        # Check result format is unchanged
        result_dict = result[0]
        assert "file_path" in result_dict
        assert "start_line" in result_dict
        assert "end_line" in result_dict
        assert "match_text" in result_dict
        assert "language" in result_dict
        
        # Match text should contain the function call
        assert "print" in result_dict["match_text"]
    
    def test_existing_parameters_work(self, tmp_path):
        """Test that existing parameter combinations still work."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('test')")
        
        # Test with existing parameters only (no new directory params)
        result = search_code_tool_implementation(
            search_type="function-calls",
            target="print",
            scope=str(test_file),
            language="python",
            max_results=50,
            include_context=True
        )
        
        assert isinstance(result, list)
        # Should work exactly as before
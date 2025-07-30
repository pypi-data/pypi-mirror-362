"""
Comprehensive tests for SearchEngine directory search functionality.

Tests core directory traversal, file filtering, pattern matching,
and result processing functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open
from typing import List

from code_extractor.search_engine import SearchEngine
from code_extractor.models import SearchParameters, SearchResult


class TestSearchEngineDirectorySearch:
    """Test SearchEngine directory search functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.engine = SearchEngine()
    
    def test_find_matching_files_basic(self, tmp_path):
        """Test basic file discovery in directory."""
        # Create test files
        (tmp_path / "test1.py").write_text("print('hello')")
        (tmp_path / "test2.js").write_text("console.log('hello')")
        (tmp_path / "README.md").write_text("# Test")
        
        params = SearchParameters(
            search_type="function-calls",
            target="test",
            scope=str(tmp_path),
            file_patterns=["*.py", "*.js"]
        )
        
        files = self.engine._find_matching_files(tmp_path, params)
        file_names = {f.name for f in files}
        
        assert "test1.py" in file_names
        assert "test2.js" in file_names
        assert "README.md" not in file_names  # Excluded by pattern
    
    def test_file_pattern_matching(self):
        """Test file pattern matching logic."""
        # Test include patterns
        assert self.engine._matches_patterns("test.py", ["*.py"]) == True
        assert self.engine._matches_patterns("test.js", ["*.py"]) == False
        assert self.engine._matches_patterns("test.py", ["*.py", "*.js"]) == True
        assert self.engine._matches_patterns("test.md", ["*.py", "*.js"]) == False
        
        # Test wildcard pattern
        assert self.engine._matches_patterns("any_file.txt", ["*"]) == True
        
        # Test specific file names
        assert self.engine._matches_patterns("specific.py", ["specific.py"]) == True
        assert self.engine._matches_patterns("other.py", ["specific.py"]) == False
    
    def test_exclude_pattern_matching(self, tmp_path):
        """Test exclusion pattern logic."""
        # Create test structure
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("print('main')")
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / "__pycache__" / "test.pyc").write_text("binary")
        (tmp_path / "test.pyc").write_text("binary")
        (tmp_path / "node_modules").mkdir()
        (tmp_path / "node_modules" / "lib.js").write_text("module")
        
        params = SearchParameters(
            search_type="function-calls",
            target="test",
            scope=str(tmp_path),
            file_patterns=["*"],
            exclude_patterns=["*.pyc", "__pycache__/*", "node_modules/*"]
        )
        
        files = self.engine._find_matching_files(tmp_path, params)
        file_paths = {str(f.relative_to(tmp_path)) for f in files}
        
        assert "src/main.py" in file_paths
        assert "test.pyc" not in file_paths
        assert "__pycache__/test.pyc" not in file_paths
        assert "node_modules/lib.js" not in file_paths
    
    def test_binary_file_detection(self, tmp_path):
        """Test binary file detection."""
        # Create text file
        text_file = tmp_path / "text.py"
        text_file.write_text("print('hello world')")
        
        # Create binary file
        binary_file = tmp_path / "binary.bin"
        binary_file.write_bytes(b'\x00\x01\x02\x03Binary content\x00')
        
        assert self.engine._is_binary_file(text_file) == False
        assert self.engine._is_binary_file(binary_file) == True
    
    def test_binary_file_detection_edge_cases(self, tmp_path):
        """Test binary file detection edge cases."""
        # Empty file
        empty_file = tmp_path / "empty.txt"
        empty_file.touch()
        assert self.engine._is_binary_file(empty_file) == False
        
        # File with unicode
        unicode_file = tmp_path / "unicode.py"
        unicode_file.write_text("print('héllo wörld 🌍')", encoding='utf-8')
        assert self.engine._is_binary_file(unicode_file) == False
        
        # Non-existent file
        fake_file = tmp_path / "nonexistent.txt"
        assert self.engine._is_binary_file(fake_file) == True  # Treat as binary if can't read
    
    def test_result_deduplication(self):
        """Test result deduplication logic."""
        results = [
            SearchResult("file1.py", 10, 10, "func()", language="python"),
            SearchResult("file1.py", 10, 10, "func()", language="python"),  # Duplicate
            SearchResult("file1.py", 20, 20, "func()", language="python"),  # Different line
            SearchResult("file2.py", 10, 10, "func()", language="python"),  # Different file
            SearchResult("file1.py", 10, 10, "func() ", language="python"), # Different whitespace
        ]
        
        deduplicated = self.engine._deduplicate_results(results)
        
        # Should have 3 unique results (whitespace trimmed makes last one duplicate)
        assert len(deduplicated) == 3
        
        # Check sorting by file path then line number
        assert deduplicated[0].file_path == "file1.py"
        assert deduplicated[0].start_line == 10
        assert deduplicated[1].file_path == "file1.py"
        assert deduplicated[1].start_line == 20
        assert deduplicated[2].file_path == "file2.py"
    
    def test_max_files_limit(self, tmp_path):
        """Test max_files limit functionality."""
        # Create more files than the limit
        for i in range(15):
            (tmp_path / f"file_{i:02d}.py").write_text(f"print('file {i}')")
        
        params = SearchParameters(
            search_type="function-calls",
            target="print",
            scope=str(tmp_path),
            max_files=10
        )
        
        with patch('builtins.print') as mock_print:
            self.engine.search_directory(str(tmp_path), params)
            mock_print.assert_any_call(f"Found 15 files, limiting to 10")
    
    def test_max_results_limit(self, tmp_path):
        """Test max_results limit functionality."""
        # Create files with multiple matches each
        for i in range(5):
            content = "\n".join([f"print('line {j}')" for j in range(10)])
            (tmp_path / f"file_{i}.py").write_text(content)
        
        params = SearchParameters(
            search_type="function-calls",
            target="print",
            scope=str(tmp_path),
            max_results=20  # Less than total possible matches
        )
        
        results = self.engine.search_directory(str(tmp_path), params)
        assert len(results) <= 20
    
    def test_symlink_handling(self, tmp_path):
        """Test symlink handling with follow_symlinks parameter."""
        # Create regular file
        real_file = tmp_path / "real.py"
        real_file.write_text("print('real')")
        
        # Create symlink to file
        symlink_file = tmp_path / "link.py"
        try:
            symlink_file.symlink_to(real_file)
        except OSError:
            pytest.skip("Symlinks not supported on this system")
        
        # Test with follow_symlinks=False (default)
        params = SearchParameters(
            search_type="function-calls",
            target="print",
            scope=str(tmp_path),
            follow_symlinks=False
        )
        
        files = self.engine._find_matching_files(tmp_path, params)
        file_names = {f.name for f in files}
        
        assert "real.py" in file_names
        assert "link.py" not in file_names  # Symlink excluded
        
        # Test with follow_symlinks=True
        params.follow_symlinks = True
        files = self.engine._find_matching_files(tmp_path, params)
        file_names = {f.name for f in files}
        
        assert "real.py" in file_names
        assert "link.py" in file_names  # Symlink included
    
    def test_permission_error_handling(self, tmp_path):
        """Test handling of permission errors."""
        # Create a file we can't access (simulate permission error)
        test_file = tmp_path / "restricted.py"
        test_file.write_text("print('restricted')")
        
        params = SearchParameters(
            search_type="function-calls",
            target="print",
            scope=str(tmp_path)
        )
        
        # Mock permission error during file reading
        with patch('pathlib.Path.rglob', side_effect=PermissionError("Access denied")):
            with patch('builtins.print') as mock_print:
                files = self.engine._find_matching_files(tmp_path, params)
                assert files == []
                mock_print.assert_any_call(f"Permission denied accessing {tmp_path}: Access denied")
    
    def test_empty_directory(self, tmp_path):
        """Test handling of empty directories."""
        params = SearchParameters(
            search_type="function-calls",
            target="test",
            scope=str(tmp_path)
        )
        
        results = self.engine.search_directory(str(tmp_path), params)
        assert results == []
    
    def test_nonexistent_directory(self):
        """Test handling of non-existent directories."""
        fake_path = "/nonexistent/directory"
        
        params = SearchParameters(
            search_type="function-calls",
            target="test",
            scope=fake_path
        )
        
        with patch('builtins.print') as mock_print:
            results = self.engine.search_directory(fake_path, params)
            assert results == []
            mock_print.assert_any_call(f"Directory not found or not a directory: {fake_path}")
    
    def test_search_directory_integration(self, tmp_path):
        """Test full directory search integration."""
        # Create test directory structure
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("""
def main():
    print("Starting application")
    get_file_content("config.json")
    return True
""")
        
        (tmp_path / "src" / "utils.py").write_text("""
import os

def get_file_content(filename):
    with open(filename) as f:
        return f.read()

def helper():
    get_file_content("data.txt")
""")
        
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_main.py").write_text("""
def test_main():
    get_file_content("test_data.json")
    assert True
""")
        
        params = SearchParameters(
            search_type="function-calls",
            target="get_file_content",
            scope=str(tmp_path),
            file_patterns=["*.py"]
        )
        
        results = self.engine.search_directory(str(tmp_path), params)
        
        # Should find all 3 calls to get_file_content
        assert len(results) == 3
        
        # Check file paths are correct
        file_paths = {os.path.basename(r.file_path) for r in results}
        assert "main.py" in file_paths
        assert "utils.py" in file_paths
        assert "test_main.py" in file_paths
        
        # Check match text contains function calls
        for result in results:
            assert "get_file_content" in result.match_text
    
    def test_unicode_filename_handling(self, tmp_path):
        """Test handling of Unicode filenames."""
        # Create file with Unicode name
        unicode_file = tmp_path / "tëst_fïlé.py"
        unicode_file.write_text("print('unicode test')")
        
        params = SearchParameters(
            search_type="function-calls",
            target="print",
            scope=str(tmp_path)
        )
        
        results = self.engine.search_directory(str(tmp_path), params)
        assert len(results) == 1
        assert "tëst_fïlé.py" in results[0].file_path


class TestSearchEngineErrorHandling:
    """Test error handling in SearchEngine."""
    
    def setup_method(self):
        """Set up test environment."""
        self.engine = SearchEngine()
    
    def test_file_read_error_handling(self, tmp_path):
        """Test handling of file read errors during search."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('test')")
        
        params = SearchParameters(
            search_type="function-calls",
            target="print",
            scope=str(test_file)
        )
        
        # Mock file read error - use the correct import path from search_engine module
        with patch('code_extractor.search_engine.get_file_content', side_effect=Exception("Read error")):
            with patch('builtins.print') as mock_print:
                results = self.engine.search_file(str(test_file), params)
                # Error is caught and empty list returned
                assert results == []
                mock_print.assert_any_call(f"Error searching {test_file}: Read error")
    
    def test_directory_search_error_handling(self, tmp_path):
        """Test error handling during directory search."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('test')")
        
        params = SearchParameters(
            search_type="function-calls",
            target="print",
            scope=str(tmp_path)
        )
        
        # Mock error during directory search
        with patch.object(self.engine, 'search_file', side_effect=Exception("Search error")):
            with patch('builtins.print') as mock_print:
                results = self.engine.search_directory(str(tmp_path), params)
                # Should continue processing despite individual file errors
                mock_print.assert_any_call(f"Error searching file {test_file}: Search error")
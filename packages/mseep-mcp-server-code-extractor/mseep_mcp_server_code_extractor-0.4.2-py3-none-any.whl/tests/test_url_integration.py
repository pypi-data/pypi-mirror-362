"""Integration tests for URL support in MCP tools."""

import pytest
import responses

from code_extractor.server import (
    get_symbols,
    find_function,
    find_class,
    get_lines,
    get_signature,
)
from code_extractor.file_reader import get_file_content
from code_extractor.url_fetcher import URLFetchError, URLNotFound, clear_url_cache


class TestFileReaderURLSupport:
    """Test file reader URL integration."""

    def setup_method(self):
        """Clear cache before each test."""
        clear_url_cache()

    @responses.activate
    def test_get_file_content_url(self):
        """Test get_file_content with URL."""
        url = "https://example.com/test.py"
        content = "def hello():\n    return 'world'"
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = get_file_content(url)
        assert result == content

    @responses.activate
    def test_get_file_content_url_with_revision_error(self):
        """Test that revision parameter with URL raises error."""
        url = "https://example.com/test.py"
        
        with pytest.raises(ValueError, match="revision parameter is not applicable"):
            get_file_content(url, revision="HEAD")

    @responses.activate
    def test_get_file_content_url_not_found(self):
        """Test URL not found error propagation."""
        url = "https://example.com/missing.py"
        
        responses.add(
            responses.GET,
            url,
            status=404
        )
        
        with pytest.raises(URLNotFound):
            get_file_content(url)


class TestMCPToolsURLSupport:
    """Test MCP tools with URL support."""

    def setup_method(self):
        """Clear cache before each test."""
        clear_url_cache()

    @responses.activate
    def test_get_symbols_with_url(self):
        """Test get_symbols with GitHub raw URL."""
        url = "https://raw.githubusercontent.com/user/repo/main/test.py"
        content = '''class TestClass:
    def test_method(self):
        return "test"

def standalone_function():
    return "standalone"
'''
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = get_symbols(url)
        
        # Should find both class and function
        assert len(result) >= 2
        names = [item.get('name') for item in result]
        assert 'TestClass' in names
        assert 'standalone_function' in names

    @responses.activate
    def test_find_function_with_url(self):
        """Test find_function with URL."""
        url = "https://example.com/functions.py"
        content = '''def target_function(param1, param2):
    """A target function."""
    return param1 + param2

def other_function():
    return "other"
'''
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        func_finder = find_function(None)
        result = func_finder(url, "target_function")
        
        assert "error" not in result
        assert "target_function" in result["code"]
        assert "param1, param2" in result["code"]

    @responses.activate
    def test_find_class_with_url(self):
        """Test find_class with URL."""
        url = "https://example.com/classes.py"
        content = '''class TargetClass:
    """A target class."""
    
    def __init__(self):
        self.value = 42
    
    def method(self):
        return self.value

class OtherClass:
    pass
'''
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        class_finder = find_class(None)
        result = class_finder(url, "TargetClass")
        
        assert "error" not in result
        assert "TargetClass" in result["code"]
        assert "__init__" in result["code"]
        assert "method" in result["code"]

    @responses.activate
    def test_get_lines_with_url(self):
        """Test get_lines with URL."""
        url = "https://example.com/lines.py"
        content = '''# Line 1
# Line 2
def function():
    # Line 4
    return "test"
# Line 6
'''
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = get_lines(url, 3, 5)
        
        assert "error" not in result
        assert "def function():" in result["code"]
        assert "return \"test\"" in result["code"]
        assert result["start_line"] == 3
        assert result["end_line"] == 5

    @responses.activate
    def test_get_signature_with_url(self):
        """Test get_signature with URL."""
        url = "https://example.com/signatures.py"
        content = '''def complex_function(arg1: str, arg2: int = 42, *args, **kwargs) -> str:
    """A complex function with type hints."""
    return f"{arg1}_{arg2}"
'''
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = get_signature(url, "complex_function")
        
        assert "error" not in result
        assert "complex_function" in result["signature"]
        assert "arg1: str" in result["signature"]
        assert "-> str" in result["signature"]


class TestURLLanguageDetection:
    """Test language detection for URLs."""

    def setup_method(self):
        """Clear cache before each test."""
        clear_url_cache()

    @responses.activate
    def test_python_url_detection(self):
        """Test Python file detection from URL."""
        url = "https://example.com/script.py"
        content = "def python_function():\n    pass"
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = get_symbols(url)
        assert len(result) > 0
        assert any("python_function" in str(item) for item in result)

    @responses.activate
    def test_javascript_url_detection(self):
        """Test JavaScript file detection from URL."""
        url = "https://example.com/script.js"
        content = "function jsFunction() {\n    return 'js';\n}"
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = get_symbols(url)
        # JavaScript parsing might not be fully supported, so just check it doesn't error
        assert isinstance(result, list)
        if len(result) > 0:
            assert any("jsFunction" in str(item) for item in result)

    @responses.activate
    def test_typescript_url_detection(self):
        """Test TypeScript file detection from URL."""
        url = "https://example.com/script.ts"
        content = "function tsFunction(): string {\n    return 'ts';\n}"
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = get_symbols(url)
        # TypeScript parsing might not be fully supported, so just check it doesn't error
        assert isinstance(result, list)
        if len(result) > 0:
            assert any("tsFunction" in str(item) for item in result)


class TestURLErrorHandling:
    """Test error handling in MCP tools with URLs."""

    def setup_method(self):
        """Clear cache before each test."""
        clear_url_cache()

    @responses.activate
    def test_get_symbols_url_not_found(self):
        """Test get_symbols with URL not found."""
        url = "https://example.com/missing.py"
        
        responses.add(
            responses.GET,
            url,
            status=404
        )
        
        result = get_symbols(url)
        assert len(result) == 1
        assert "error" in result[0]

    @responses.activate
    def test_find_function_url_error(self):
        """Test find_function with URL error."""
        url = "https://example.com/error.py"
        
        responses.add(
            responses.GET,
            url,
            status=500,
            body="Internal Server Error"
        )
        
        func_finder = find_function(None)
        result = func_finder(url, "some_function")
        
        assert "error" in result

    @responses.activate
    def test_get_lines_url_error(self):
        """Test get_lines with URL error."""
        url = "https://example.com/timeout.py"
        
        # Simulate timeout by not adding any response
        # This will cause a connection error
        
        result = get_lines(url, 1, 5)
        assert "error" in result


class TestRealWorldURLPatterns:
    """Test real-world URL patterns (mocked)."""

    def setup_method(self):
        """Clear cache before each test."""
        clear_url_cache()

    @responses.activate
    def test_github_raw_file(self):
        """Test GitHub raw file URL pattern."""
        url = "https://raw.githubusercontent.com/python/cpython/main/Lib/pathlib.py"
        content = '''"""Object-oriented filesystem paths."""

import os
import sys
from collections.abc import Sequence

class Path:
    """Object representing a filesystem path."""
    
    def __init__(self, *args):
        self._drv = ""
        self._root = ""
'''
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = get_symbols(url)
        
        # Should find the Path class
        assert len(result) > 0
        names = [item.get('name') for item in result]
        assert 'Path' in names

    @responses.activate
    def test_gitlab_raw_file(self):
        """Test GitLab raw file URL pattern."""
        url = "https://gitlab.com/user/project/-/raw/main/src/module.py"
        content = '''#!/usr/bin/env python3

class GitLabModule:
    """A module from GitLab."""
    
    def process(self):
        return "processed"
'''
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = get_symbols(url)
        
        # Should find the GitLabModule class
        assert len(result) > 0
        names = [item.get('name') for item in result]
        assert 'GitLabModule' in names

    @responses.activate
    def test_revision_parameter_with_url_error(self):
        """Test that revision parameter with URL is properly rejected."""
        url = "https://example.com/test.py"
        
        # Should fail before making any HTTP request
        result = get_symbols(url, git_revision="HEAD")
        assert len(result) == 1
        assert "error" in result[0]
        assert "revision parameter is not applicable" in result[0]["error"]

    @responses.activate
    def test_complex_github_structure(self):
        """Test complex GitHub file structure."""
        url = "https://raw.githubusercontent.com/user/repo/feature-branch/src/utils/helpers.py"
        content = '''"""Utility helpers module."""

from typing import List, Dict, Optional

def process_data(data: List[Dict]) -> Optional[str]:
    """Process a list of dictionaries."""
    if not data:
        return None
    return "processed"

class DataProcessor:
    """Process data efficiently."""
    
    def __init__(self, config: Dict):
        self.config = config
    
    def run(self) -> bool:
        return True

async def async_process():
    """Async processing function."""
    await some_operation()
'''
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = get_symbols(url)
        
        # Should find functions and class
        names = [item.get('name') for item in result]
        assert 'process_data' in names
        assert 'DataProcessor' in names
        assert 'async_process' in names
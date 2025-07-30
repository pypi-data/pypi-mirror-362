"""
Tests for language detection and parser management.
"""

import pytest
from code_extractor.languages import (
    get_language_for_file,
    normalize_language,
    get_tree_sitter_parser,
    get_tree_sitter_language,
    is_language_supported
)


class TestLanguageDetection:
    """Test language detection from file extensions."""
    
    def test_python_detection(self):
        """Test Python file detection."""
        assert get_language_for_file("test.py") == "python"
        assert get_language_for_file("/path/to/file.py") == "python"
        assert get_language_for_file("script.PY") == "python"  # Case insensitive
    
    def test_javascript_detection(self):
        """Test JavaScript file detection."""
        assert get_language_for_file("script.js") == "javascript"
        assert get_language_for_file("component.jsx") == "javascript"
    
    def test_typescript_detection(self):
        """Test TypeScript file detection."""
        assert get_language_for_file("module.ts") == "typescript"
        assert get_language_for_file("component.tsx") == "typescript"
    
    def test_other_languages(self):
        """Test other supported languages."""
        assert get_language_for_file("main.go") == "go"
        assert get_language_for_file("lib.rs") == "rust"
        assert get_language_for_file("App.java") == "java"
        assert get_language_for_file("program.c") == "c"
        assert get_language_for_file("program.cpp") == "cpp"
        assert get_language_for_file("program.cc") == "cpp"
        assert get_language_for_file("Program.cs") == "c_sharp"
        assert get_language_for_file("script.rb") == "ruby"
        assert get_language_for_file("web.php") == "php"
        assert get_language_for_file("App.swift") == "swift"
        assert get_language_for_file("Main.kt") == "kotlin"
        assert get_language_for_file("App.scala") == "scala"
    
    def test_unsupported_extensions(self):
        """Test unsupported file extensions."""
        assert get_language_for_file("document.txt") == "text"
        assert get_language_for_file("config.xml") == "text"
        assert get_language_for_file("data.json") == "text"
        assert get_language_for_file("README.md") == "text"
    
    def test_no_extension(self):
        """Test files without extensions."""
        assert get_language_for_file("Makefile") == "text"
        assert get_language_for_file("LICENSE") == "text"
    
    def test_empty_path(self):
        """Test empty or None file paths."""
        assert get_language_for_file("") == "text"
        assert get_language_for_file(None) == "text"


class TestLanguageNormalization:
    """Test language name normalization."""
    
    def test_alias_normalization(self):
        """Test language alias normalization."""
        assert normalize_language("js") == "javascript"
        assert normalize_language("ts") == "typescript"
        assert normalize_language("py") == "python"
        assert normalize_language("rb") == "ruby"
        assert normalize_language("c++") == "cpp"
        assert normalize_language("csharp") == "c_sharp"
    
    def test_case_normalization(self):
        """Test case normalization."""
        assert normalize_language("PYTHON") == "python"
        assert normalize_language("JavaScript") == "javascript"
        assert normalize_language("TypeScript") == "typescript"
    
    def test_no_normalization_needed(self):
        """Test languages that don't need normalization."""
        assert normalize_language("python") == "python"
        assert normalize_language("javascript") == "javascript"
        assert normalize_language("go") == "go"


class TestTreeSitterIntegration:
    """Test tree-sitter parser and language integration."""
    
    def test_supported_languages(self):
        """Test that we can get parsers for supported languages."""
        supported_langs = ["python", "javascript", "typescript"]
        
        for lang in supported_langs:
            parser = get_tree_sitter_parser(lang)
            language = get_tree_sitter_language(lang)
            
            assert parser is not None, f"Should get parser for {lang}"
            assert language is not None, f"Should get language for {lang}"
            assert is_language_supported(lang), f"{lang} should be supported"
    
    def test_unsupported_language(self):
        """Test handling of unsupported languages."""
        parser = get_tree_sitter_parser("unsupported")
        language = get_tree_sitter_language("unsupported")
        
        assert parser is None
        assert language is None
        assert not is_language_supported("unsupported")
    
    def test_text_language(self):
        """Test handling of 'text' language."""
        parser = get_tree_sitter_parser("text")
        language = get_tree_sitter_language("text")
        
        assert parser is None
        assert language is None
        assert not is_language_supported("text")
    
    def test_language_aliases_in_parsers(self):
        """Test that aliases work with parsers."""
        # Test JavaScript aliases
        js_parser = get_tree_sitter_parser("js")
        assert js_parser is not None
        
        # Test Python aliases
        py_parser = get_tree_sitter_parser("py")
        assert py_parser is not None
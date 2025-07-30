"""
Tests for the core extractor functionality.

This tests the critical method vs function classification and other core features.
"""

import pytest
from code_extractor import CodeExtractor
from code_extractor.models import SymbolKind


class TestSymbolExtraction:
    """Test core symbol extraction functionality."""
    
    def test_method_vs_function_classification(self, python_extractor, basic_class_code):
        """
        CRITICAL TEST: Ensure methods are not labeled as functions.
        This was the main issue with the original implementation.
        """
        symbols = python_extractor.extract_symbols(basic_class_code)
        
        # Separate methods and functions
        methods = [s for s in symbols if s.kind == SymbolKind.METHOD]
        functions = [s for s in symbols if s.kind == SymbolKind.FUNCTION]
        classes = [s for s in symbols if s.kind == SymbolKind.CLASS]
        
        # Should have one class
        assert len(classes) == 1
        assert classes[0].name == "Calculator"
        
        # Should have methods, not functions (original bug)
        method_names = {m.name for m in methods}
        expected_methods = {"__init__", "current_value", "add", "multiply", "from_string"}
        assert method_names == expected_methods
        
        # Should have NO top-level functions in this code
        assert len(functions) == 0, f"Found functions where methods expected: {[f.name for f in functions]}"
    
    def test_nested_function_vs_method_distinction(self, python_extractor, nested_classes_code):
        """Test distinction between methods and nested functions."""
        symbols = python_extractor.extract_symbols(nested_classes_code)
        
        methods = [s for s in symbols if s.kind == SymbolKind.METHOD]
        functions = [s for s in symbols if s.kind == SymbolKind.FUNCTION]
        classes = [s for s in symbols if s.kind == SymbolKind.CLASS]
        
        # Should have classes
        class_names = {c.name for c in classes}
        assert "Outer" in class_names
        assert "Inner" in class_names
        
        # Should have methods
        method_names = {m.name for m in methods}
        assert "inner_method" in method_names
        assert "outer_method" in method_names
        
        # Should have standalone function
        function_names = {f.name for f in functions}
        assert "standalone_function" in function_names
        
        # Nested function inside method should NOT appear as separate function
        assert "nested_function" not in function_names
    
    def test_parameter_extraction_with_types_and_defaults(self, python_extractor, basic_class_code):
        """Test parameter extraction with full context."""
        symbols = python_extractor.extract_symbols(basic_class_code)
        
        # Find the add method
        add_method = next((s for s in symbols if s.name == "add"), None)
        assert add_method is not None
        assert add_method.kind == SymbolKind.METHOD
        
        # Check parameters
        params = add_method.parameters
        assert len(params) >= 3  # self, x, y
        
        # Find specific parameters
        param_names = [p.name for p in params]
        assert "self" in param_names
        assert "x" in param_names
        assert "y" in param_names
        
        # Check parameter details
        x_param = next((p for p in params if p.name == "x"), None)
        assert x_param is not None
        assert x_param.type_hint == "int"
        
        y_param = next((p for p in params if p.name == "y"), None)
        assert y_param is not None
        assert y_param.type_hint == "int"
        assert y_param.default_value == "5"
    
    def test_return_type_extraction(self, python_extractor, basic_class_code):
        """Test return type extraction."""
        symbols = python_extractor.extract_symbols(basic_class_code)
        
        # Check return types for various methods
        methods_by_name = {s.name: s for s in symbols if s.kind == SymbolKind.METHOD}
        
        assert "current_value" in methods_by_name
        assert methods_by_name["current_value"].return_type == "int"
        
        assert "add" in methods_by_name
        assert methods_by_name["add"].return_type == "int"
        
        assert "multiply" in methods_by_name
        assert methods_by_name["multiply"].return_type == "int"
    
    def test_hierarchy_and_parent_relationships(self, python_extractor, basic_class_code):
        """Test parent-child relationships."""
        symbols = python_extractor.extract_symbols(basic_class_code)
        
        # All methods should have Calculator as parent
        methods = [s for s in symbols if s.kind == SymbolKind.METHOD]
        for method in methods:
            assert method.parent == "Calculator", f"Method {method.name} should have Calculator as parent"
    
    def test_nested_class_hierarchy(self, python_extractor, nested_classes_code):
        """Test nested class hierarchy detection."""
        symbols = python_extractor.extract_symbols(nested_classes_code)
        
        # Find Inner class and its method
        inner_class = next((s for s in symbols if s.name == "Inner"), None)
        inner_method = next((s for s in symbols if s.name == "inner_method"), None)
        
        assert inner_class is not None
        assert inner_method is not None
        
        # Inner class should have Outer as parent
        assert inner_class.parent == "Outer"
        
        # inner_method should have Inner as parent
        assert inner_method.parent == "Inner"
    
    def test_async_method_detection(self, python_extractor, basic_class_code):
        """Test async method detection."""
        symbols = python_extractor.extract_symbols(basic_class_code)
        
        add_method = next((s for s in symbols if s.name == "add"), None)
        assert add_method is not None
        assert add_method.is_async is True
    
    def test_docstring_extraction(self, python_extractor, basic_class_code):
        """Test docstring extraction."""
        symbols = python_extractor.extract_symbols(basic_class_code)
        
        # Class docstring
        calculator_class = next((s for s in symbols if s.name == "Calculator"), None)
        assert calculator_class is not None
        assert "simple calculator class" in calculator_class.docstring.lower()
        
        # Method docstring
        init_method = next((s for s in symbols if s.name == "__init__"), None)
        assert init_method is not None
        assert "initialize" in init_method.docstring.lower()
    
    def test_variable_extraction(self, python_extractor, variables_and_imports_code):
        """Test variable and constant extraction."""
        symbols = python_extractor.extract_symbols(variables_and_imports_code)
        
        variables = [s for s in symbols if s.kind == SymbolKind.VARIABLE]
        constants = [s for s in symbols if s.kind == SymbolKind.CONSTANT]
        
        # Check constants (uppercase variables)
        constant_names = {c.name for c in constants}
        assert "MAX_SIZE" in constant_names
        assert "DEBUG_MODE" in constant_names
        
        # Check variables with type hints
        var_names = {v.name for v in variables}
        assert "user_count" in var_names
        assert "user_names" in var_names
        
        # Check type annotations
        user_count = next((v for v in variables if v.name == "user_count"), None)
        if user_count:
            assert user_count.type_annotation == "int"
    
    def test_edge_cases(self, python_extractor, edge_cases_code):
        """Test edge cases and error handling."""
        symbols = python_extractor.extract_symbols(edge_cases_code)
        
        # Should handle empty class
        empty_class = next((s for s in symbols if s.name == "EmptyClass"), None)
        assert empty_class is not None
        assert empty_class.kind == SymbolKind.CLASS
        
        # Should handle empty function
        empty_function = next((s for s in symbols if s.name == "empty_function"), None)
        assert empty_function is not None
        assert empty_function.kind == SymbolKind.FUNCTION
        
        # Should handle inheritance
        child_class = next((s for s in symbols if s.name == "Child"), None)
        assert child_class is not None
        assert child_class.kind == SymbolKind.CLASS
    
    def test_malformed_code_handling(self, python_extractor):
        """Test handling of malformed code."""
        malformed_code = """
        class Broken
            def incomplete_method(
                pass
        """
        
        # Should not crash, might return error symbol
        symbols = python_extractor.extract_symbols(malformed_code)
        assert isinstance(symbols, list)  # Should return a list even on error
    
    def test_empty_code_handling(self, python_extractor):
        """Test handling of empty code."""
        symbols = python_extractor.extract_symbols("")
        assert symbols == []
        
        symbols = python_extractor.extract_symbols("   \n  \n  ")
        assert symbols == []


class TestSpecificExtractionMethods:
    """Test specific extraction methods."""
    
    def test_extract_function(self, python_extractor, basic_class_code):
        """Test extracting a specific function."""
        # This should find the method (since it's in a class)
        add_method = python_extractor.extract_function(basic_class_code, "add")
        assert add_method is not None
        assert add_method.name == "add"
        assert add_method.kind == SymbolKind.METHOD
        
        # This should not find anything (doesn't exist)
        nonexistent = python_extractor.extract_function(basic_class_code, "nonexistent")
        assert nonexistent is None
    
    def test_extract_class(self, python_extractor, basic_class_code):
        """Test extracting a specific class."""
        calculator = python_extractor.extract_class(basic_class_code, "Calculator")
        assert calculator is not None
        assert calculator.name == "Calculator"
        assert calculator.kind == SymbolKind.CLASS
        
        # This should not find anything
        nonexistent = python_extractor.extract_class(basic_class_code, "NonExistent")
        assert nonexistent is None


class TestCompatibility:
    """Test compatibility with existing MCP interface."""
    
    def test_to_dict_compatibility(self, python_extractor, basic_class_code):
        """Test that symbols can be converted to dict format for MCP."""
        symbols = python_extractor.extract_symbols(basic_class_code)
        
        for symbol in symbols:
            result = symbol.to_dict()
            
            # Check required fields for MCP compatibility
            assert "name" in result
            assert "type" in result
            assert "start_line" in result
            assert "end_line" in result
            assert "lines" in result
            assert "preview" in result
            
            # Check types
            assert isinstance(result["name"], str)
            assert isinstance(result["type"], str)
            assert isinstance(result["start_line"], int)
            assert isinstance(result["end_line"], int)
            assert isinstance(result["lines"], str)
            assert isinstance(result["preview"], str)
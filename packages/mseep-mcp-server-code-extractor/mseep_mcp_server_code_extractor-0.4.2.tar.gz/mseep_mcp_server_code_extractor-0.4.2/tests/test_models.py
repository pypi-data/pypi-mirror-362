"""
Tests for data models.
"""

import pytest
from code_extractor.models import CodeSymbol, Parameter, SymbolKind


class TestParameter:
    """Test Parameter data model."""
    
    def test_parameter_creation(self):
        """Test basic parameter creation."""
        param = Parameter("name", "str", "default")
        assert param.name == "name"
        assert param.type_hint == "str"
        assert param.default_value == "default"
    
    def test_parameter_str_representation(self):
        """Test parameter string representation."""
        # Parameter with type and default
        param1 = Parameter("x", "int", "5")
        assert str(param1) == "x: int = 5"
        
        # Parameter with type only
        param2 = Parameter("y", "str")
        assert str(param2) == "y: str"
        
        # Parameter with name only
        param3 = Parameter("z")
        assert str(param3) == "z"


class TestCodeSymbol:
    """Test CodeSymbol data model."""
    
    def test_symbol_creation(self):
        """Test basic symbol creation."""
        symbol = CodeSymbol(
            name="test_func",
            kind=SymbolKind.FUNCTION,
            start_line=1,
            end_line=5,
            start_byte=0,
            end_byte=100
        )
        
        assert symbol.name == "test_func"
        assert symbol.kind == SymbolKind.FUNCTION
        assert symbol.start_line == 1
        assert symbol.end_line == 5
        assert symbol.lines == "1-5"
    
    def test_function_signature(self):
        """Test function signature generation."""
        params = [
            Parameter("self"),
            Parameter("x", "int"),
            Parameter("y", "str", "default")
        ]
        
        symbol = CodeSymbol(
            name="my_method",
            kind=SymbolKind.METHOD,
            start_line=1,
            end_line=5,
            start_byte=0,
            end_byte=100,
            parameters=params,
            return_type="bool"
        )
        
        expected = "my_method(self, x: int, y: str = default) -> bool"
        assert symbol.signature == expected
    
    def test_symbol_to_dict(self):
        """Test conversion to dictionary for MCP compatibility."""
        symbol = CodeSymbol(
            name="Calculator",
            kind=SymbolKind.CLASS,
            start_line=1,
            end_line=10,
            start_byte=0,
            end_byte=200,
            docstring="A calculator class"
        )
        
        result = symbol.to_dict()
        
        assert result["name"] == "Calculator"
        assert result["type"] == "class"
        assert result["start_line"] == 1
        assert result["end_line"] == 10
        assert result["lines"] == "1-10"
        assert result["docstring"] == "A calculator class"
        assert "preview" in result
    
    def test_symbol_with_parent(self):
        """Test symbol with parent relationship."""
        symbol = CodeSymbol(
            name="add",
            kind=SymbolKind.METHOD,
            start_line=5,
            end_line=8,
            start_byte=100,
            end_byte=200,
            parent="Calculator"
        )
        
        result = symbol.to_dict()
        assert result["parent"] == "Calculator"
    
    def test_symbol_with_decorators(self):
        """Test symbol with decorators."""
        symbol = CodeSymbol(
            name="get_value",
            kind=SymbolKind.METHOD,
            start_line=10,
            end_line=12,
            start_byte=300,
            end_byte=400,
            decorators=["@property"],
            is_static=False
        )
        
        result = symbol.to_dict()
        assert result["decorators"] == ["@property"]
        assert "is_static" not in result  # False values excluded
    
    def test_symbol_flags(self):
        """Test various symbol flags."""
        symbol = CodeSymbol(
            name="class_method",
            kind=SymbolKind.METHOD,
            start_line=15,
            end_line=18,
            start_byte=500,
            end_byte=600,
            is_static=True,
            is_async=True
        )
        
        result = symbol.to_dict()
        assert result["is_static"] is True
        assert result["is_async"] is True


class TestSymbolKind:
    """Test SymbolKind enum."""
    
    def test_symbol_kinds(self):
        """Test all symbol kinds have correct values."""
        assert SymbolKind.CLASS.value == "class"
        assert SymbolKind.METHOD.value == "method"
        assert SymbolKind.FUNCTION.value == "function"
        assert SymbolKind.VARIABLE.value == "variable"
        assert SymbolKind.CONSTANT.value == "constant"
        assert SymbolKind.IMPORT.value == "import"
        assert SymbolKind.INTERFACE.value == "interface"
        assert SymbolKind.TYPE_ALIAS.value == "type_alias"
        assert SymbolKind.ENUM.value == "enum"
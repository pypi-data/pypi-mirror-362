"""
Pytest configuration and fixtures.
"""

import pytest
from code_extractor import CodeExtractor
from code_extractor.models import SymbolKind


@pytest.fixture
def python_extractor():
    """Create a Python code extractor."""
    return CodeExtractor('python')


@pytest.fixture
def basic_class_code():
    """Sample Python class for testing."""
    return '''
class Calculator:
    """A simple calculator class."""
    
    def __init__(self, initial_value: int = 0):
        """Initialize with optional initial value."""
        self.value = initial_value
    
    @property
    def current_value(self) -> int:
        """Get the current value."""
        return self.value
    
    async def add(self, x: int, y: int = 5) -> int:
        """Add two numbers asynchronously."""
        return x + y
    
    @staticmethod
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b
    
    @classmethod
    def from_string(cls, value_str: str) -> 'Calculator':
        """Create calculator from string."""
        return cls(int(value_str))
'''


@pytest.fixture
def nested_classes_code():
    """Sample code with nested classes and functions."""
    return '''
class Outer:
    """Outer class."""
    
    class Inner:
        """Inner class."""
        
        def inner_method(self):
            """Method in inner class."""
            pass
    
    def outer_method(self):
        """Method in outer class."""
        def nested_function():
            """Function nested in method."""
            return "nested"
        return nested_function()

def standalone_function():
    """A standalone function."""
    return "standalone"
'''


@pytest.fixture
def variables_and_imports_code():
    """Sample code with variables and imports."""
    return '''
import os
from typing import List, Dict
from collections import defaultdict as dd

# Constants
MAX_SIZE = 100
DEBUG_MODE = True

# Variables with type hints
user_count: int = 42
user_names: List[str] = ["Alice", "Bob"]
config: Dict[str, str] = {"debug": "true"}

# Simple variables
total = 0
name = "test"
'''


@pytest.fixture
def edge_cases_code():
    """Edge cases for testing."""
    return '''
class EmptyClass:
    pass

def empty_function():
    pass

class ClassWithNestedFunction:
    def method_with_nested(self):
        def inner():
            pass
        return inner

# Multiple inheritance
class Child(EmptyClass, ClassWithNestedFunction):
    pass
'''
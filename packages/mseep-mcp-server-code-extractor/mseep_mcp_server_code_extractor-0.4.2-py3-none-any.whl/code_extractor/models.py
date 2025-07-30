"""
Data models for code symbols with rich context information.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any


class SymbolKind(Enum):
    """Types of code symbols that can be extracted."""
    CLASS = "class"
    METHOD = "method"          # Functions inside classes
    FUNCTION = "function"      # Top-level functions
    VARIABLE = "variable"
    CONSTANT = "constant"
    IMPORT = "import"
    INTERFACE = "interface"
    TYPE_ALIAS = "type_alias"
    ENUM = "enum"


@dataclass
class Parameter:
    """Represents a function/method parameter with type and default value."""
    name: str
    type_hint: Optional[str] = None
    default_value: Optional[str] = None
    
    def __str__(self) -> str:
        result = self.name
        if self.type_hint:
            result += f": {self.type_hint}"
        if self.default_value:
            result += f" = {self.default_value}"
        return result


@dataclass
class CodeSymbol:
    """
    Rich representation of a code symbol with full context.
    
    This replaces the shallow dict-based approach with structured data
    that captures hierarchical relationships and detailed metadata.
    """
    name: str
    kind: SymbolKind
    start_line: int
    end_line: int
    start_byte: int
    end_byte: int
    
    # Hierarchical context
    parent: Optional[str] = None  # Class name for methods, module for top-level
    
    # Function/method details
    parameters: List[Parameter] = field(default_factory=list)
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    
    # Access and behavior modifiers
    access_modifier: Optional[str] = None  # public, private, protected
    is_static: bool = False
    is_async: bool = False
    is_abstract: bool = False
    is_property: bool = False
    
    # Variable/constant specific
    value: Optional[str] = None
    type_annotation: Optional[str] = None
    
    # Import specific
    import_source: Optional[str] = None
    import_alias: Optional[str] = None
    
    @property
    def lines(self) -> str:
        """Line range as string for compatibility."""
        return f"{self.start_line}-{self.end_line}"
    
    @property
    def signature(self) -> str:
        """Generate a readable signature for functions/methods."""
        if self.kind not in [SymbolKind.FUNCTION, SymbolKind.METHOD]:
            return self.name
            
        params = ", ".join(str(p) for p in self.parameters)
        result = f"{self.name}({params})"
        
        if self.return_type:
            result += f" -> {self.return_type}"
            
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for compatibility with current MCP interface."""
        result = {
            "name": self.name,
            "type": self.kind.value,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "lines": self.lines,
            "preview": self._generate_preview()
        }
        
        # Add rich context if available
        if self.parent:
            result["parent"] = self.parent
        if self.parameters:
            result["parameters"] = [str(p) for p in self.parameters]
        if self.return_type:
            result["return_type"] = self.return_type
        if self.docstring:
            result["docstring"] = self.docstring
        if self.decorators:
            result["decorators"] = self.decorators
        if self.is_static:
            result["is_static"] = True
        if self.is_async:
            result["is_async"] = True
            
        return result
    
    def _generate_preview(self) -> str:
        """Generate a preview line for display."""
        if self.kind == SymbolKind.CLASS:
            preview = f"class {self.name}"
            if self.parent:
                preview += f" (in {self.parent})"
        elif self.kind in [SymbolKind.FUNCTION, SymbolKind.METHOD]:
            preview = ""
            if self.decorators:
                preview += " ".join(self.decorators) + " "
            if self.is_async:
                preview += "async "
            if self.is_static:
                preview += "static "
            preview += self.signature
        elif self.kind == SymbolKind.VARIABLE:
            preview = f"{self.name}"
            if self.type_annotation:
                preview += f": {self.type_annotation}"
            if self.value:
                preview += f" = {self.value}"
        else:
            preview = self.name
            
        return preview[:80]  # Truncate for display


@dataclass
class SearchResult:
    """Represents a search result with context information."""
    file_path: str
    start_line: int
    end_line: int
    match_text: str
    context_before: List[str] = field(default_factory=list)
    context_after: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    language: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MCP compatibility."""
        return {
            "file_path": self.file_path,
            "start_line": self.start_line, 
            "end_line": self.end_line,
            "match_text": self.match_text,
            "context_before": self.context_before,
            "context_after": self.context_after,
            "metadata": self.metadata,
            "language": self.language
        }


@dataclass  
class SearchParameters:
    """Parameters for semantic code search operations."""
    search_type: str
    target: str
    scope: str
    language: Optional[str] = None
    git_revision: Optional[str] = None
    max_results: int = 100
    include_context: bool = True
    context_lines: int = 3
    
    # Directory search specific options
    file_patterns: List[str] = field(default_factory=lambda: ["*"])
    exclude_patterns: List[str] = field(default_factory=lambda: ["*.pyc", "*.pyo", "*.pyd", "__pycache__/*", ".git/*", ".svn/*", "node_modules/*", "*.min.js"])
    max_files: int = 1000
    follow_symlinks: bool = False
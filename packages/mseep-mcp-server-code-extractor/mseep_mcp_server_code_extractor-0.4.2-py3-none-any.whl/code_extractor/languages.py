"""
Language detection and parser management for tree-sitter.
"""

import os
from typing import Dict, Optional
from tree_sitter import Language, Parser
from tree_sitter_languages import get_language, get_parser


# Supported languages mapping
LANGUAGE_EXTENSIONS = {
    '.py': 'python',
    '.js': 'javascript', 
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.go': 'go',
    '.rs': 'rust',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.cc': 'cpp',
    '.cxx': 'cpp',
    '.cs': 'c_sharp',
    '.rb': 'ruby',
    '.php': 'php',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.scala': 'scala',
}

# Language aliases for consistency
LANGUAGE_ALIASES = {
    'js': 'javascript',
    'ts': 'typescript',
    'py': 'python',
    'rb': 'ruby',
    'c++': 'cpp',
    'csharp': 'c_sharp',
}


def get_language_for_file(file_path: str) -> str:
    """
    Determine the programming language from file extension.
    
    Args:
        file_path: Path to the source file
        
    Returns:
        Language name or 'text' if unsupported
    """
    if not file_path:
        return 'text'
        
    ext = os.path.splitext(file_path)[1].lower()
    return LANGUAGE_EXTENSIONS.get(ext, 'text')


def normalize_language(language: str) -> str:
    """
    Normalize language name using aliases.
    
    Args:
        language: Language name or alias
        
    Returns:
        Normalized language name
    """
    return LANGUAGE_ALIASES.get(language.lower(), language.lower())


def get_tree_sitter_parser(language: str) -> Optional[Parser]:
    """
    Get a tree-sitter parser for the specified language.
    
    Args:
        language: Programming language name
        
    Returns:
        Parser instance or None if unsupported
    """
    normalized_lang = normalize_language(language)
    
    if normalized_lang == 'text':
        return None
        
    try:
        return get_parser(normalized_lang)
    except Exception:
        return None


def get_tree_sitter_language(language: str) -> Optional[Language]:
    """
    Get a tree-sitter language for queries.
    
    Args:
        language: Programming language name
        
    Returns:
        Language instance or None if unsupported
    """
    normalized_lang = normalize_language(language)
    
    if normalized_lang == 'text':
        return None
        
    try:
        return get_language(normalized_lang)
    except Exception:
        return None


def is_language_supported(language: str) -> bool:
    """
    Check if a language is supported by tree-sitter.
    
    Args:
        language: Programming language name
        
    Returns:
        True if supported, False otherwise
    """
    return get_tree_sitter_parser(language) is not None
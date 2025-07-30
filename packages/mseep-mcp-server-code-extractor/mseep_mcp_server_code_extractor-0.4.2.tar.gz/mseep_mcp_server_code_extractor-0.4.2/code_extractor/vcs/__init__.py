"""VCS abstraction layer for code extraction."""

from abc import ABC, abstractmethod
from pathlib import Path


class VCSProvider(ABC):
    """Abstract base class for version control system providers."""
    
    @abstractmethod
    def get_file_content(self, file_path: Path, revision: str) -> str:
        """Get file content at specific revision."""
        pass
    
    @abstractmethod
    def find_repo_root(self, file_path: Path) -> Path:
        """Find the repository root for given file path."""
        pass
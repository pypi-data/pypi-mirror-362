"""Git provider implementation for VCS abstraction layer."""

import subprocess
from pathlib import Path

from . import VCSProvider


class GitProvider(VCSProvider):
    """Git implementation of VCSProvider."""
    
    def get_file_content(self, file_path: Path, revision: str) -> str:
        """Get file content at specific git revision."""
        repo_root = self.find_repo_root(file_path)
        relative_path = file_path.resolve().relative_to(repo_root.resolve())
        
        # Convert to forward slashes for git (works on all platforms)
        git_path = str(relative_path).replace('\\', '/')
        
        result = subprocess.run(
            ['git', '-C', str(repo_root), 'show', f'{revision}:{git_path}'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    
    def find_repo_root(self, file_path: Path) -> Path:
        """Find git repository root."""
        search_path = file_path if file_path.is_dir() else file_path.parent
        
        result = subprocess.run(
            ['git', '-C', str(search_path), 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
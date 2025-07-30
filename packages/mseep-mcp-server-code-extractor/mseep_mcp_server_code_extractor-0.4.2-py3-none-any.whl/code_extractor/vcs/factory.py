"""VCS provider factory for auto-detection."""

import subprocess
from pathlib import Path
from typing import Optional

from . import VCSProvider
from .git import GitProvider


def detect_vcs_provider(file_path: Path) -> Optional[VCSProvider]:
    """Auto-detect VCS type and return appropriate provider."""
    search_path = file_path if file_path.is_dir() else file_path.parent
    
    # Check for git repository
    try:
        subprocess.run(
            ['git', '-C', str(search_path), 'rev-parse', '--git-dir'],
            capture_output=True,
            check=True
        )
        return GitProvider()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Future: Check for .hg, .svn, etc.
    return None
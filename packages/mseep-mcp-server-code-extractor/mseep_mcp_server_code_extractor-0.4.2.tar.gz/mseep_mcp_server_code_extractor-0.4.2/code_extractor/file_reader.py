"""Unified file reading with VCS and URL support."""

from pathlib import Path
from typing import Optional, Union

from .vcs.factory import detect_vcs_provider
from .url_fetcher import is_url, fetch_url_content


def get_file_content(path_or_url: Union[str, Path], revision: Optional[str] = None) -> str:
    """
    Get file content from filesystem, VCS revision, or URL.
    
    Args:
        path_or_url: Path to file, or URL to fetch (GitHub raw, GitLab raw, direct file URL)
        revision: Optional VCS revision (commit, branch, tag, etc.) - not supported for URLs
    
    Returns:
        File content as string
        
    Raises:
        ValueError: If revision is specified with URL, or if no VCS found for path
        URLFetchError: For URL-related errors (network, timeout, content issues)
    """
    path_str = str(path_or_url)
    
    # Handle URL case
    if is_url(path_str):
        if revision is not None:
            raise ValueError("revision parameter is not applicable when path_or_url is a URL")
        return fetch_url_content(path_str)
    
    # Handle filesystem/VCS case
    path_obj = Path(path_str) if isinstance(path_or_url, str) else path_or_url
    
    if revision is None:
        # Filesystem read (backward compatible)
        return path_obj.read_text(encoding='utf-8')
    
    # VCS read using detected provider
    vcs_provider = detect_vcs_provider(path_obj)
    if not vcs_provider:
        raise ValueError(f"No VCS found for {path_obj}")
    
    return vcs_provider.get_file_content(path_obj, revision)
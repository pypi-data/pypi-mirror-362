"""URL fetching with robust error handling and caching."""

import os
from typing import Optional
from urllib.parse import urlparse
from cachetools import TTLCache, cached
import requests


# Configuration constants
DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_MAX_SIZE = 1024 * 1024  # 1MB
DEFAULT_CACHE_TTL = 300  # 5 minutes
DEFAULT_CACHE_SIZE = 128

# Environment variable overrides
MAX_FILE_SIZE = int(os.environ.get('MCP_URL_MAX_SIZE', DEFAULT_MAX_SIZE))
REQUEST_TIMEOUT = int(os.environ.get('MCP_URL_TIMEOUT', DEFAULT_TIMEOUT))
CACHE_TTL = int(os.environ.get('MCP_URL_CACHE_TTL', DEFAULT_CACHE_TTL))
CACHE_SIZE = int(os.environ.get('MCP_URL_CACHE_SIZE', DEFAULT_CACHE_SIZE))


# Exception hierarchy for clear error handling
class URLFetchError(Exception):
    """Base exception for URL fetching errors."""
    pass


class URLNetworkError(URLFetchError):
    """Network connectivity or connection issues."""
    pass


class URLNotFound(URLFetchError):
    """Resource not found (404) or similar client errors."""
    pass


class URLTimeout(URLFetchError):
    """Request timeout exceeded."""
    pass


class URLContentError(URLFetchError):
    """Invalid content type or size violations."""
    pass


# TTL cache for URL content
url_cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TTL)


def is_url(path: str) -> bool:
    """
    Check if a path is a valid URL.
    
    Args:
        path: String to check
        
    Returns:
        True if path is a valid HTTP/HTTPS URL
    """
    try:
        parsed = urlparse(path)
        return parsed.scheme in {'http', 'https'} and bool(parsed.netloc)
    except Exception:
        return False


def validate_content_type(content_type: str) -> bool:
    """
    Validate that content type is suitable for code extraction.
    
    Args:
        content_type: HTTP Content-Type header value
        
    Returns:
        True if content type is acceptable
    """
    if not content_type:
        return True  # Allow missing content-type
    
    content_type = content_type.lower().strip()
    
    # Allow text content types
    if content_type.startswith('text/'):
        return True
    
    # Allow specific application types that are text-based
    allowed_app_types = {
        'application/javascript',
        'application/json',
        'application/xml',
        'application/x-python',
        'application/x-typescript',
    }
    
    for allowed in allowed_app_types:
        if content_type.startswith(allowed):
            return True
    
    return False


@cached(url_cache)
def _fetch_url_cached(url: str) -> str:
    """
    Internal cached URL fetching function.
    
    Args:
        url: URL to fetch
        
    Returns:
        Content as string
        
    Raises:
        URLFetchError: For various fetch failures
    """
    try:
        # Make request with streaming to check size early
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            stream=True,
            headers={
                'User-Agent': 'mcp-server-code-extractor/0.2.2',
                'Accept': 'text/*, application/javascript, application/json, application/xml',
            }
        )
        
        # Check HTTP status
        if response.status_code == 404:
            raise URLNotFound(f"Resource not found: {url}")
        elif response.status_code >= 400:
            raise URLNetworkError(f"HTTP {response.status_code}: {response.reason}")
        
        # Validate content type
        content_type = response.headers.get('content-type', '')
        if not validate_content_type(content_type):
            raise URLContentError(f"Unsupported content type: {content_type}")
        
        # Check content length if provided
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > MAX_FILE_SIZE:
            raise URLContentError(f"File too large: {content_length} bytes (max: {MAX_FILE_SIZE})")
        
        # Read content with size limit
        content_bytes = b''
        for chunk in response.iter_content(chunk_size=8192):
            content_bytes += chunk
            if len(content_bytes) > MAX_FILE_SIZE:
                raise URLContentError(f"File too large: >{MAX_FILE_SIZE} bytes")
        
        # Decode content
        try:
            # Try to detect encoding from response
            encoding = response.encoding or 'utf-8'
            content = content_bytes.decode(encoding)
        except UnicodeDecodeError:
            # Fallback to utf-8 with error handling
            content = content_bytes.decode('utf-8', errors='replace')
        
        return content
        
    except requests.exceptions.Timeout:
        raise URLTimeout(f"Request timeout ({REQUEST_TIMEOUT}s): {url}")
    except requests.exceptions.ConnectionError as e:
        raise URLNetworkError(f"Connection error: {e}")
    except requests.exceptions.RequestException as e:
        raise URLNetworkError(f"Request failed: {e}")


def fetch_url_content(url: str, bypass_cache: bool = False) -> str:
    """
    Fetch content from a URL with caching and error handling.
    
    Args:
        url: URL to fetch
        bypass_cache: If True, bypass cache and fetch fresh content
        
    Returns:
        Content as string
        
    Raises:
        URLFetchError: For various fetch failures
    """
    if not is_url(url):
        raise URLFetchError(f"Invalid URL: {url}")
    
    if bypass_cache:
        # Clear this URL from cache and fetch fresh
        cache_key = (url,)  # cachetools uses function args as key
        url_cache.pop(cache_key, None)
    
    return _fetch_url_cached(url)


def clear_url_cache() -> None:
    """Clear the URL content cache."""
    url_cache.clear()


def get_cache_stats() -> dict:
    """
    Get cache statistics.
    
    Returns:
        Dictionary with cache statistics
    """
    return {
        'size': len(url_cache),
        'maxsize': url_cache.maxsize,
        'ttl': url_cache.ttl,
        'hits': getattr(url_cache, 'hits', 0),
        'misses': getattr(url_cache, 'misses', 0),
    }
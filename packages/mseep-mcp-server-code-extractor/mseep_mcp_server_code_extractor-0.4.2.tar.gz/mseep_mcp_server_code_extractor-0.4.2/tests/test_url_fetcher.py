"""Tests for URL fetcher functionality."""

import pytest
import responses
from cachetools import TTLCache

from code_extractor.url_fetcher import (
    is_url,
    validate_content_type,
    fetch_url_content,
    clear_url_cache,
    get_cache_stats,
    URLFetchError,
    URLNetworkError,
    URLNotFound,
    URLTimeout,
    URLContentError,
)


class TestURLValidation:
    """Test URL validation functions."""

    def test_is_url_valid_http(self):
        """Test valid HTTP URLs."""
        assert is_url("http://example.com/file.py")
        assert is_url("https://github.com/user/repo/file.py")

    def test_is_url_valid_https(self):
        """Test valid HTTPS URLs."""
        assert is_url("https://example.com/file.py")
        assert is_url("https://raw.githubusercontent.com/user/repo/main/file.py")

    def test_is_url_invalid_schemes(self):
        """Test invalid URL schemes."""
        assert not is_url("ftp://example.com/file.py")
        assert not is_url("file:///path/to/file.py")
        assert not is_url("javascript:alert('xss')")

    def test_is_url_no_scheme(self):
        """Test strings without URL schemes."""
        assert not is_url("/path/to/file.py")
        assert not is_url("file.py")
        assert not is_url("http_server.py")

    def test_is_url_invalid_format(self):
        """Test malformed URLs."""
        assert not is_url("http://")
        assert not is_url("https://")
        assert not is_url("not-a-url")

    def test_validate_content_type_text(self):
        """Test text content types."""
        assert validate_content_type("text/plain")
        assert validate_content_type("text/python")
        assert validate_content_type("text/javascript")
        assert validate_content_type("TEXT/PLAIN")  # Case insensitive

    def test_validate_content_type_application(self):
        """Test allowed application content types."""
        assert validate_content_type("application/javascript")
        assert validate_content_type("application/json")
        assert validate_content_type("application/xml")
        assert validate_content_type("application/x-python")

    def test_validate_content_type_invalid(self):
        """Test invalid content types."""
        assert not validate_content_type("image/png")
        assert not validate_content_type("application/octet-stream")
        assert not validate_content_type("video/mp4")

    def test_validate_content_type_missing(self):
        """Test missing content type."""
        assert validate_content_type("")
        assert validate_content_type(None)


class TestURLFetching:
    """Test URL fetching with mocked responses."""

    def setup_method(self):
        """Clear cache before each test."""
        clear_url_cache()

    @responses.activate
    def test_fetch_url_success(self):
        """Test successful URL fetching."""
        url = "https://example.com/file.py"
        content = "def hello():\n    return 'world'"
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = fetch_url_content(url)
        assert result == content

    @responses.activate
    def test_fetch_url_404(self):
        """Test 404 error handling."""
        url = "https://example.com/missing.py"
        
        responses.add(
            responses.GET,
            url,
            status=404
        )
        
        with pytest.raises(URLNotFound):
            fetch_url_content(url)

    @responses.activate
    def test_fetch_url_500_error(self):
        """Test server error handling."""
        url = "https://example.com/error.py"
        
        responses.add(
            responses.GET,
            url,
            status=500,
            body="Internal Server Error"
        )
        
        with pytest.raises(URLNetworkError):
            fetch_url_content(url)

    @responses.activate
    def test_fetch_url_timeout(self):
        """Test timeout handling."""
        import requests
        
        # Monkey patch to simulate timeout
        original_get = requests.get
        def mock_get(*args, **kwargs):
            raise requests.exceptions.Timeout("Request timed out")
        
        requests.get = mock_get
        try:
            with pytest.raises(URLTimeout):
                fetch_url_content("https://example.com/file.py")
        finally:
            requests.get = original_get

    @responses.activate
    def test_fetch_url_connection_error(self):
        """Test connection error handling."""
        import requests
        
        # Monkey patch to simulate connection error
        original_get = requests.get
        def mock_get(*args, **kwargs):
            raise requests.exceptions.ConnectionError("Connection failed")
        
        requests.get = mock_get
        try:
            with pytest.raises(URLNetworkError):
                fetch_url_content("https://example.com/file.py")
        finally:
            requests.get = original_get

    @responses.activate
    def test_fetch_url_invalid_content_type(self):
        """Test invalid content type rejection."""
        url = "https://example.com/binary.bin"
        
        responses.add(
            responses.GET,
            url,
            body=b"\x89\x50\x4e\x47",  # PNG header
            status=200,
            content_type="image/png"
        )
        
        with pytest.raises(URLContentError):
            fetch_url_content(url)

    @responses.activate
    def test_fetch_url_large_content_header(self):
        """Test large content size rejection via header."""
        url = "https://example.com/large.py"
        large_size = 2 * 1024 * 1024  # 2MB
        
        responses.add(
            responses.GET,
            url,
            body="# Large file",
            status=200,
            content_type="text/plain",
            headers={"Content-Length": str(large_size)}
        )
        
        with pytest.raises(URLContentError):
            fetch_url_content(url)

    @responses.activate
    def test_fetch_url_large_content_body(self):
        """Test large content size rejection via body size."""
        url = "https://example.com/large.py"
        # Create content larger than 1MB limit
        large_content = "# " + "x" * (1024 * 1024 + 100)
        
        responses.add(
            responses.GET,
            url,
            body=large_content,
            status=200,
            content_type="text/plain"
        )
        
        with pytest.raises(URLContentError):
            fetch_url_content(url)

    @responses.activate
    def test_fetch_url_encoding_detection(self):
        """Test encoding detection and handling."""
        url = "https://example.com/unicode.py"
        content = "# -*- coding: utf-8 -*-\ndef français():\n    return 'bonjour'"
        
        responses.add(
            responses.GET,
            url,
            body=content.encode('utf-8'),
            status=200,
            content_type="text/plain; charset=utf-8"
        )
        
        result = fetch_url_content(url)
        assert result == content

    @responses.activate
    def test_fetch_url_encoding_fallback(self):
        """Test encoding fallback for invalid encoding."""
        url = "https://example.com/invalid.py"
        # Invalid UTF-8 bytes
        invalid_content = b"def test():\n    return '\xff\xfe'"
        
        responses.add(
            responses.GET,
            url,
            body=invalid_content,
            status=200,
            content_type="text/plain"
        )
        
        # Should not raise, but use replacement characters
        result = fetch_url_content(url)
        assert "def test():" in result

    def test_fetch_url_invalid_url(self):
        """Test invalid URL rejection."""
        with pytest.raises(URLFetchError):
            fetch_url_content("not-a-url")
        
        with pytest.raises(URLFetchError):
            fetch_url_content("/local/path")


class TestURLCaching:
    """Test URL content caching."""

    def setup_method(self):
        """Clear cache before each test."""
        clear_url_cache()

    @responses.activate
    def test_cache_hit(self):
        """Test cache hit on repeated requests."""
        url = "https://example.com/cached.py"
        content = "def cached_function():\n    return 'cached'"
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        # First request
        result1 = fetch_url_content(url)
        assert result1 == content
        
        # Second request should hit cache (responses will fail if called again)
        responses.reset()
        result2 = fetch_url_content(url)
        assert result2 == content

    @responses.activate
    def test_cache_bypass(self):
        """Test cache bypass functionality."""
        url = "https://example.com/bypass.py"
        content1 = "def version1():\n    return 'v1'"
        content2 = "def version2():\n    return 'v2'"
        
        # First request
        responses.add(
            responses.GET,
            url,
            body=content1,
            status=200,
            content_type="text/plain"
        )
        result1 = fetch_url_content(url)
        assert result1 == content1
        
        # Second request with cache bypass
        responses.add(
            responses.GET,
            url,
            body=content2,
            status=200,
            content_type="text/plain"
        )
        result2 = fetch_url_content(url, bypass_cache=True)
        assert result2 == content2

    def test_cache_stats(self):
        """Test cache statistics."""
        stats = get_cache_stats()
        assert "size" in stats
        assert "maxsize" in stats
        assert "ttl" in stats
        assert stats["size"] == 0  # Empty cache

    def test_clear_cache(self):
        """Test cache clearing."""
        # This is tested implicitly in setup_method
        clear_url_cache()
        stats = get_cache_stats()
        assert stats["size"] == 0


class TestGitHubIntegration:
    """Test GitHub-specific URL patterns."""

    @responses.activate
    def test_github_raw_url(self):
        """Test GitHub raw URL fetching."""
        url = "https://raw.githubusercontent.com/user/repo/main/src/file.py"
        content = "class GitHubClass:\n    pass"
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = fetch_url_content(url)
        assert result == content

    @responses.activate
    def test_gitlab_raw_url(self):
        """Test GitLab raw URL fetching."""
        url = "https://gitlab.com/user/repo/-/raw/main/src/file.py"
        content = "class GitLabClass:\n    pass"
        
        responses.add(
            responses.GET,
            url,
            body=content,
            status=200,
            content_type="text/plain"
        )
        
        result = fetch_url_content(url)
        assert result == content


class TestErrorHandling:
    """Test comprehensive error handling."""

    def test_url_fetch_error_hierarchy(self):
        """Test exception hierarchy."""
        assert issubclass(URLNetworkError, URLFetchError)
        assert issubclass(URLNotFound, URLFetchError)
        assert issubclass(URLTimeout, URLFetchError)
        assert issubclass(URLContentError, URLFetchError)

    @responses.activate
    def test_user_agent_header(self):
        """Test that User-Agent header is set correctly."""
        url = "https://example.com/file.py"
        
        def request_callback(request):
            assert "mcp-server-code-extractor" in request.headers.get("User-Agent", "")
            return (200, {}, "def test(): pass")
        
        responses.add_callback(
            responses.GET,
            url,
            callback=request_callback,
            content_type="text/plain"
        )
        
        fetch_url_content(url)

    @responses.activate
    def test_accept_header(self):
        """Test that Accept header is set correctly."""
        url = "https://example.com/file.py"
        
        def request_callback(request):
            accept_header = request.headers.get("Accept", "")
            assert "text/*" in accept_header
            assert "application/javascript" in accept_header
            return (200, {}, "def test(): pass")
        
        responses.add_callback(
            responses.GET,
            url,
            callback=request_callback,
            content_type="text/plain"
        )
        
        fetch_url_content(url)
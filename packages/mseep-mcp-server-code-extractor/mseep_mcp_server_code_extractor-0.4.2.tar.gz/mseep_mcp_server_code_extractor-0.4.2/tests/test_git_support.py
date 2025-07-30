"""Tests for git revision support in code extraction."""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from code_extractor.vcs.git import GitProvider
from code_extractor.vcs.factory import detect_vcs_provider
from code_extractor.file_reader import get_file_content


class TestGitProvider:
    """Test GitProvider functionality."""
    
    def test_git_provider_interface(self):
        """Test GitProvider implements VCSProvider interface."""
        provider = GitProvider()
        assert hasattr(provider, 'get_file_content')
        assert hasattr(provider, 'find_repo_root')
    
    @patch('subprocess.run')
    def test_find_repo_root_success(self, mock_run):
        """Test finding git repository root."""
        mock_run.return_value = Mock(stdout='/repo/root', check=True)
        
        provider = GitProvider()
        result = provider.find_repo_root(Path('/repo/root/src/file.py'))
        
        assert result == Path('/repo/root')
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_find_repo_root_failure(self, mock_run):
        """Test handling when not in git repository."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')
        
        provider = GitProvider()
        with pytest.raises(subprocess.CalledProcessError):
            provider.find_repo_root(Path('/not/a/repo/file.py'))
    
    @patch('subprocess.run')
    def test_get_file_content_success(self, mock_run):
        """Test successful file content retrieval from git."""
        # Mock find_repo_root call
        mock_run.side_effect = [
            Mock(stdout='/repo/root', check=True),  # find_repo_root
            Mock(stdout='def test():\n    pass\n', check=True)  # git show
        ]
        
        provider = GitProvider()
        result = provider.get_file_content(Path('/repo/root/src/test.py'), 'HEAD~1')
        
        assert result == 'def test():\n    pass\n'
        assert mock_run.call_count == 2
    
    @patch('subprocess.run')
    def test_get_file_content_invalid_revision(self, mock_run):
        """Test handling invalid git revision."""
        mock_run.side_effect = [
            Mock(stdout='/repo/root', check=True),  # find_repo_root
            subprocess.CalledProcessError(1, 'git')  # git show fails
        ]
        
        provider = GitProvider()
        with pytest.raises(subprocess.CalledProcessError):
            provider.get_file_content(Path('/repo/root/src/test.py'), 'invalid-revision')
    
    def test_path_normalization(self):
        """Test Windows path normalization for git."""
        provider = GitProvider()
        file_path = Path('C:/repo/src/file.py')
        repo_root = Path('C:/repo')
        
        # Mock the actual git operations to test path logic
        with patch.object(provider, 'find_repo_root', return_value=repo_root):
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(stdout='content', check=True)
                
                provider.get_file_content(file_path, 'HEAD')
                
                # Verify git show was called with forward slash path
                args = mock_run.call_args[0][0]
                assert 'HEAD:src/file.py' in args


class TestVCSFactory:
    """Test VCS provider factory."""
    
    @patch('subprocess.run')
    def test_detect_git_provider(self, mock_run):
        """Test detection of git repository."""
        mock_run.return_value = Mock(check=True)
        
        provider = detect_vcs_provider(Path('/repo/file.py'))
        
        assert isinstance(provider, GitProvider)
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_detect_no_vcs(self, mock_run):
        """Test when no VCS is detected."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')
        
        provider = detect_vcs_provider(Path('/not/a/repo/file.py'))
        
        assert provider is None


class TestFileReader:
    """Test unified file reader with VCS support."""
    
    def test_filesystem_read(self, tmp_path):
        """Test reading from filesystem (backward compatibility)."""
        test_file = tmp_path / "test.py"
        test_content = "def hello():\n    return 'world'\n"
        test_file.write_text(test_content)
        
        result = get_file_content(str(test_file))
        assert result == test_content
    
    def test_filesystem_read_pathlib(self, tmp_path):
        """Test reading from filesystem using Path object."""
        test_file = tmp_path / "test.py"
        test_content = "def hello():\n    return 'world'\n"
        test_file.write_text(test_content)
        
        result = get_file_content(test_file)
        assert result == test_content
    
    @patch('code_extractor.file_reader.detect_vcs_provider')
    def test_git_read_success(self, mock_detect):
        """Test reading from git revision."""
        mock_provider = Mock()
        mock_provider.get_file_content.return_value = "git content"
        mock_detect.return_value = mock_provider
        
        result = get_file_content("/repo/file.py", "HEAD~1")
        
        assert result == "git content"
        mock_provider.get_file_content.assert_called_once_with(
            Path("/repo/file.py"), "HEAD~1"
        )
    
    @patch('code_extractor.file_reader.detect_vcs_provider')
    def test_git_read_no_vcs(self, mock_detect):
        """Test error when no VCS provider found."""
        mock_detect.return_value = None
        
        with pytest.raises(ValueError, match="No VCS found"):
            get_file_content("/not/a/repo/file.py", "HEAD~1")


class TestMCPToolsIntegration:
    """Test MCP tools with git revision support."""
    
    @patch('code_extractor.server.get_file_content')
    @patch('code_extractor.server.create_extractor')
    def test_get_symbols_with_git_revision(self, mock_create_extractor, mock_get_content):
        """Test get_symbols with git revision parameter."""
        from code_extractor.server import get_symbols
        
        # Mock extractor and content
        mock_extractor = Mock()
        mock_symbol = Mock()
        mock_symbol.to_dict.return_value = {"name": "test_func", "type": "function"}
        mock_extractor.extract_symbols.return_value = [mock_symbol]
        mock_create_extractor.return_value = mock_extractor
        mock_get_content.return_value = "def test_func(): pass"
        
        result = get_symbols("/repo/file.py", "HEAD~1")
        
        assert len(result) == 1
        assert result[0]["name"] == "test_func"
        mock_get_content.assert_called_once_with("/repo/file.py", "HEAD~1")
    
    @patch('code_extractor.server.get_file_content')
    def test_get_lines_with_git_revision(self, mock_get_content):
        """Test get_lines with git revision parameter."""
        from code_extractor.server import get_lines
        
        mock_get_content.return_value = "line 1\nline 2\nline 3\n"
        
        result = get_lines("/repo/file.py", 1, 2, "HEAD~1")
        
        assert result["code"] == "line 1\nline 2\n"
        assert result["start_line"] == 1
        assert result["end_line"] == 2
        mock_get_content.assert_called_once_with("/repo/file.py", "HEAD~1")


class TestErrorHandling:
    """Test error handling scenarios."""
    
    @patch('subprocess.run')
    def test_git_command_not_found(self, mock_run):
        """Test handling when git command is not found."""
        mock_run.side_effect = FileNotFoundError()
        
        provider = GitProvider()
        with pytest.raises(FileNotFoundError):
            provider.find_repo_root(Path('/some/path'))
    
    @patch('code_extractor.file_reader.detect_vcs_provider')
    def test_vcs_error_propagation(self, mock_detect):
        """Test that VCS errors are properly propagated."""
        mock_provider = Mock()
        mock_provider.get_file_content.side_effect = subprocess.CalledProcessError(1, 'git')
        mock_detect.return_value = mock_provider
        
        with pytest.raises(subprocess.CalledProcessError):
            get_file_content("/repo/file.py", "invalid-ref")


if __name__ == "__main__":
    pytest.main([__file__])
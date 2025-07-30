import pytest
from unittest.mock import patch, MagicMock
from gitme.git_diff import GitDiffAnalyzer


class TestGitDiffAnalyzer:
    def test_init(self):
        with patch('gitme.git_diff.GitDiffAnalyzer._check_git', return_value=True):
            analyzer = GitDiffAnalyzer()
            assert analyzer.git_available is True
    
    def test_check_git_available(self):
        analyzer = GitDiffAnalyzer()
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock()
            result = analyzer._check_git()
            assert result is True
    
    def test_check_git_not_available(self):
        analyzer = GitDiffAnalyzer()
        with patch('subprocess.run', side_effect=FileNotFoundError):
            result = analyzer._check_git()
            assert result is False
    
    def test_format_changes_json(self):
        analyzer = GitDiffAnalyzer()
        with patch.object(analyzer, 'get_file_changes', return_value={'file.py': 'diff content'}):
            result = analyzer.format_changes_json()
            assert '"file.py": "diff content"' in result
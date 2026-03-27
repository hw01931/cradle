import pytest
from unittest.mock import MagicMock, patch
from src.cradle.git import GitManager

def test_git_manager_dry_run_logging(caplog):
    """
    dry_run 모드에서 실제로 명령어가 실행되지 않고 로그만 남는지 확인합니다.
    """
    import logging
    caplog.set_level(logging.INFO, logger="cradle.git")
    
    gm = GitManager(dry_run=True)
    gm.create_branch("test-branch")
    
    assert "🌵 [Dry Run] Would execute: git checkout -b test-branch" in caplog.text

@patch("subprocess.run")
def test_git_manager_real_run(mock_run):
    """
    dry_run=False일 때 subprocess.run이 호출되는지 확인합니다.
    """
    mock_run.return_value = MagicMock(stdout="Success", stderr="", returncode=0)
    
    gm = GitManager(dry_run=False)
    gm._run_git(["status"])
    
    mock_run.assert_called_with(
        ["git", "status"],
        cwd=gm.root_dir,
        capture_output=True,
        text=True,
        check=True
    )

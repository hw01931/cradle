import subprocess
import logging
import os
from typing import List, Optional

logger = logging.getLogger("cradle.git")

class GitManager:
    def __init__(self, root_dir: str = None, dry_run: bool = True):
        self.root_dir = root_dir or os.getcwd()
        self.dry_run = dry_run

    def _run_git(self, args: List[str]) -> str:
        cmd = ["git"] + args
        if self.dry_run and any(x in args for x in ["push", "commit", "branch"]):
            logger.info(f"🌵 [Dry Run] Would execute: {' '.join(cmd)}")
            return "Dry run successful"
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.root_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Git error: {e.stderr}")
            raise e

    def create_branch(self, branch_name: str):
        logger.info(f"🌿 Creating branch: {branch_name}")
        return self._run_git(["checkout", "-b", branch_name])

    def commit_all(self, message: str):
        logger.info(f"💾 Committing changes: {message}")
        try:
            self._run_git(["add", "."])
            return self._run_git(["commit", "-m", message])
        except subprocess.CalledProcessError:
            # Nothing to commit
            return "Nothing to commit"

    def push(self, branch_name: str):
        logger.info(f"🚀 Pushing branch: {branch_name}")
        return self._run_git(["push", "origin", branch_name])

    def open_pull_request(self, title: str, body: str):
        # Stub: GitHub CLI (gh) 명령어를 사용하거나 GitHub API 라이브러리를 사용할 수 있음
        logger.info(f"📝 Opening PR: {title}")
        if self.dry_run:
            logger.info(f"🌵 [Dry Run] PR Body: {body}")
            return "PR opened (mocked)"
        
        # Future: Use GitHub API
        return "PR creation not implemented yet"

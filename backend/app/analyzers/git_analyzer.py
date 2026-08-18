# GIT ANALYZER

#imports
from pathlib import Path
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from app.models.analysis import GitInfo

def analyze_git(project_path: str) -> GitInfo | None:
    root = Path(project_path).expanduser().resolve()

    try:
        repo = Repo(root, search_parent_directories=True)
    except (InvalidGitRepositoryError, NoSuchPathError):
        return None
    
    try:
        branch = repo.active_branch.name
    except TypeError:
        # detached HEAD state
        branch = None

    latest_commit = repo.head.commit

    return GitInfo(
        branch=branch,
        is_dirty=repo.is_dirty(untracked_files=True),
        latest_commit=latest_commit.hexsha[:7],
        latest_commit_message=latest_commit.message.strip(),
        commit_count=sum(1 for _ in repo.iter_commits()),
    )
# ANALYSIS

# imports
from typing import Dict, List
from pydantic import BaseModel

# GitInfo returns branch and is_dirty bool
class GitInfo(BaseModel):
    branch: str | None = None
    is_dirty: bool = False
    latest_commit: str | None = None
    latest_commit_message: str | None = None
    commit_count: int = 0

# AnalysisResult returns project structure
class AnalysisResult(BaseModel):
    project_name: str
    project_path: str
    file_count: int
    directory_count: int
    total_lines: int
    languages: Dict[str, int]
    todos: List[str]
    fixmes: List[str]
    has_readme: bool
    has_dockerfile: bool
    git: GitInfo | None = None
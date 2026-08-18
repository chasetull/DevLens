# ANALYSIS

# imports
from typing import Dict, List
from pydantic import BaseModel

# GitInfo returns branch and is_dirty bool
class GitInto(BaseModel):
    branch: str | None = None
    is_dirty: bool = False

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
    git: GitInto | None = None
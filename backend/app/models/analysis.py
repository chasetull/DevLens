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

# Analyze file data
class FileFinding(BaseModel):
    path: str
    lines: int

class FileAnalysis(BaseModel):
    largest_files: list[FileFinding]
    large_files: list[FileFinding]
    empty_files: list[str]
    extension_counts: dict[str, int]

# Framework detection
class FrameworkDetection(BaseModel):
    name: str
    category: str
    evidence: list[str]

class FrameworkAnalysis(BaseModel):
    frameworks: list[FrameworkDetection]




# AnalysisResult returns project structure - MAIN RETURN SET
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
    files: FileAnalysis
    frameworks: FrameworkAnalysis




    
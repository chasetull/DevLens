# PROJECT SCANNER

# imports
from pathlib import Path
from app.models.analysis import AnalysisResult

# define file extension languages
LANGUAGE_EXTENSIONS = {
    ".py" : "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".java": "Java",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".html": "HTML",
    ".css": "CSS",
    ".sql": "SQL",
    ".md": "Markdown",
}

def scan_project(project_path: str) -> AnalysisResult:
    root = Path(project_path).expanduser().resolve()

    if not root.exists():
        raise FileNotFoundError(f"Project path does not exist: {root}")
    
    if not root.is_dir():
        raise NotADirectoryError(f"Project path is not a directory: {root}")
    
    file_count = 0
    directory_count = 0
    total_lines = 0

    languages = dict[str, int] = {}
    todos = list[str] = []
    fixmes = list[str] = []

    ignored_directories = {
        ".git",
        "node_modules",
        ".venv",
        "venv",
        "__pycache__",
        "dist",
        "build",
    }

    for path in root.rglob("*"):
        if any(part in ignored_directories for part in path.parts):
            continue

        if path.is_dir():
            directory_count += 1
            continue

        if not path.is_file():
            continue

        file_count += 1

        language = LANGUAGE_EXTENSIONS.get(path.suffix.lower())

        if language:
            languages[language] = languages.get(language, 0) + 1

        try:
            text = path.read_text(encoding="utf-8")

            lines = text.splitlines()
            total_lines += len(lines)

            relative_path = path.relative_to(root)

            for line_number, line in enumerate(lines, start=1):
                if "TODO" in line:
                    todos.append(f"{relative_path}:{line_number}")

                if "FIXME" in line:
                    fixmes.append(f"{relative_path}:{line_number}")

        except (UnicodeDecodeError, PermissionError, OSError):
            continue

    # return results
    return AnalysisResult(
        project_name=root.name,
        project_path=str(root),
        file_count=file_count,
        directory_count=directory_count,
        total_lines=total_lines,
        languages=languages,
        todos=todos,
        fixmes=fixmes,
        has_readme=(root / "README.md").exists(),
        has_dockerfile=(root / "Dockerfile").exists(),
        git=None,
    )
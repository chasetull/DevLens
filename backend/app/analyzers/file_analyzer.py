# FILE ANALYZER

#imports
from collections import defaultdict
from pathlib import Path

from app.models.analysis import FileAnalysis, FileFinding

#
LARGE_FILE_LINE_THRESHOLD = 500

def analyze_files(project_path: str) -> FileAnalysis:
    root = Path(project_path).expanduser().resolve()

    ignored_directories = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
    }

    extension_counts: dict[str, int] = defaultdict(int)
    file_sizes: list[FileFinding] = []
    empty_files: list[str] = []

    for path in root.rglob("*"):
        if any(part in ignored_directories for part in path.parts):
            continue
        if not path.is_file():
            continue

        relative_path = str(path.relative_to(root))

        extension = path.suffix.lower() or "[no extension]"
        extension_counts[extension] +=1

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError, OSError):
            continue

        lines = text.splitlines()
        line_count = len(lines)

        if line_count == 0:
            empty_files.append(relative_path)

        file_sizes.append(
            FileFinding(
                path=relative_path,
                lines=line_count,
            )
        )

    largest_files = sorted(
        file_sizes,
        key=lambda file: file.lines,
        reverse=True,
    )[:10]

    large_files = [
        file
        for file in file_sizes
        if file.lines >= LARGE_FILE_LINE_THRESHOLD
    ]

    return FileAnalysis(
        largest_files=largest_files,
        large_files=large_files,
        empty_files=empty_files,
        extension_counts=dict(extension_counts),
    )
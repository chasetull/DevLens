# FRAMEWORK DETECTOR

#imports
import json
from pathlib import Path

from app.models.analysis import FrameworkAnalysis, FrameworkDetection

# MAIN func for infra detection:
def detect_frameworks(project_path: str):
    root = Path(project_path).expanduser().resolve()
    #test path
    #print(f"\n path.exp: {Path(project_path).expanduser()}, .reslv: {Path(project_path).expanduser().resolve()}\n")

    detections: list[FrameworkDetection] = []

    _detect_javascript_frameworks(root, detections)
    _detect_python_frameworks(root, detections)
    _detect_dotnet_frameworks(root, detections)
    _detect_infrastructure(root, detections)

    return FrameworkAnalysis(frameworks=detections)

# HELPER FUNCS:

# javascript
def _detect_javascript_frameworks(
        root: Path,
        detections: list[FrameworkDetection]
) -> None:
    package_json = root / "package.json"

    if not package_json.exists():
        return
    
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))

    except (json.JSONDecodeError, OSError):
        return
    
    dependencies = {
        **data.get("dependencies", {}),
        **data.get("devDependencies", {}),
    }

    framework_map = {
        "react": ("React", "frontend"),
        "@angular/core": ("Angular", "frontend"),
        "vue": ("Vue", "frontend"),
        "next": ("Next.js", "full-stack"),
        "nuxt": ("Nuxt", "full-stack"),
        "express": ("Express", "backend"),
        "vite": ("Vite", "build-tool"),
    }

    for package, (name, category) in framework_map.items():
        if package in dependencies:
            detections.append(
                FrameworkDetection(
                    name=name,
                    category=category,
                    evidence=[f"package.json: {package}"],
                )
            )




def _detect_python_frameworks(
        root: Path, 
        detections: list[FrameworkDetection]
) -> None:
    
    ignored_directories = { # dont search these dirs for requirements
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
    }

    #dependencies: set[str] = set()
    #requirements = root / "requirements.txt" # only searches from root for requirements

    dependencies: dict[str, list[str]] = {}
    
    for requirements in root.rglob("requirements.txt"):
        if any(part in ignored_directories for part in requirements.parts):
            continue

        try:
            for line in requirements.read_text(encoding="utf-8").splitlines():
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                package = (
                    line.split("==")[0]
                    .split(">=")[0]
                    .split("<=")[0]
                    .strip()
                    .lower()
                )

                relative_path = str(requirements.relative_to(root))

                dependencies.setdefault(package, []).append(relative_path)

        except OSError:
            pass

    framework_map = {
        "fastapi": ("FastAPI", "backend"),
        "flask": ("Flask", "backend"),
        "django": ("Django", "backend"),
        "pydantic": ("Pydantic", "library"),
        "gradio": ("Gradio", "frontend"),
        "gitpython": ("GitPython", "library"),
    }

    for package, (name, category) in framework_map.items():
        if package in dependencies:
            evidence = [
                f"{path}: {package}"
                for path in dependencies[package]
            ]

            detections.append(
                FrameworkDetection(
                    name=name,
                    category=category,
                    evidence=evidence,
                )
            )




def _detect_dotnet_frameworks(
        root: Path, 
        detections: list[FrameworkDetection]
) -> None:
    for project_file in root.rglob("*.csproj"):
        try:
            content = project_file.read_text(encoding="utf-8").lower()

        except OSError:
            continue

        relative_path = str(project_file.relative_to(root))

        if "microsoft.aspnetcore" in content or "microsoft.net.sdk.web" in content:
            detections.append(
                FrameworkDetection(
                    name="ASP.NET Core",
                    category="backend",
                    evidence=[relative_path],
                )
            )





def _detect_infrastructure(
        root: Path, 
        detections: list[FrameworkDetection]
) -> None:
    if (root / "Dockerfile").exists():
        detections.append(
            FrameworkDetection(
                name="Docker",
                category="infrastructure",
                evidence=["Dockerfile"],
            )
        )
    
    if any(root.rglob("docker-compose.y*ml")):
        detections.append(
            FrameworkDetection(
                name="Docker Compose",
                category="infrastructure",
                evidence=["docker-compose.yml"],
            )
        )

    if any(root.rglob("*.tf")):
        detections.append(
            FrameworkDetection(
                name="Terraform",
                category="infrastructure",
                evidence=["Terraform files detected"],
            )
        )
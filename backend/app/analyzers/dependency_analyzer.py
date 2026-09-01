# DEPENDENCIES ANALYZER

#imports
import json
from pathlib import Path

from app.models.analysis import DependencyAnalysis, DependencyManifest

from app.core.constants import IGNORED_DIRECTORIES

def _is_ignored(path: Path) -> bool:
    return any(part in IGNORED_DIRECTORIES for part in path.parts)

def analyze_dependencies(project_path: str) -> DependencyAnalysis:
    root = Path(project_path).expanduser().resolve()

    manifests: list[DependencyManifest] = []
    package_managers: set[str] = set()

    total_dependencies = 0
    total_dev_dependencies = 0

    python_manifests = _analyze_python_dependencies(root)
    javascript_manifests = _analyze_javascript_dependencies(root)

    manifests.extend(python_manifests)
    manifests.extend(javascript_manifests)

    for manifest in manifests:
        total_dependencies += manifest.dependencies
        total_dev_dependencies += manifest.dev_dependencies

        if manifest.package_manager:
            package_managers.add(manifest.package_manager)

    return DependencyAnalysis(
        manifests=manifests,
        total_dependencies=total_dependencies,
        total_dev_dependencies=total_dev_dependencies,
        package_managers=sorted(package_managers),
    )


# HELPER FUNCS
# python checker
def _analyze_python_dependencies(
        root: Path,
) -> list[DependencyManifest]:
    results : list[DependencyManifest] = []

    for requirements in root.rglob("requirements.txt"):
        if _is_ignored(requirements):
            continue
        try:
            lines = requirements.read_text(
                encoding="utf-8"
            ).splitlines()

        except OSError:
            continue

        dependencies = [
            line 
            for line in lines
            if line.strip()
            and not line.strip().startswith("#")
        ]

        relative_path = requirements.relative_to(root)

        results.append(
            DependencyManifest(
                path=str(relative_path),
                ecosystem="Python",
                package_manager="pip",
                dependencies=len(dependencies),
                dev_dependencies=0,
                has_lockfile=False,
            )
        )

    return results


# javascript checker
def _analyze_javascript_dependencies(
        root: Path,
) -> list[DependencyManifest]:
    results : list[DependencyManifest] = []

    for package_json in root.rglob("package.json"):
        if _is_ignored(package_json):
            continue

        try:
            data = json.loads(
                package_json.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            continue

        dependencies = data.get("dependencies", {})
        dev_dependencies = data.get("devDependencies", {})

        directory = package_json.parent

        package_manager = None
        has_lockfile = False

        if (directory / "package-lock.json").exists():
            package_manager = "npm"
            has_lockfile = True

        elif (directory / "yarn.lock").exists():
            package_manager = "yarn"
            has_lockfile = True

        elif (directory / "pnpm-lock.yaml").exists():
            package_manager = "pnpm"
            has_lockfile = True

        relative_path = package_json.relative_to(root)

        results.append(
            DependencyManifest(
                path=str(relative_path),
                ecosystem="JavaScript",
                package_manager=package_manager,
                dependencies=len(dependencies),
                dev_dependencies=len(dev_dependencies),
                has_lockfile=has_lockfile,
            )
        )
    return results
    

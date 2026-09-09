// ANALYSIS - mirrors pydantic models
// gitinfo
export interface GitInfo {
    branch: string | null;
    is_dirty: boolean;
    latest_commit: string | null;
    latest_commit_message: string | null;
    commit_count: number;
}

// file finding
export interface FileFinding {
    path: string;
    lines: number;
}

// file analysis
export interface FileAnalysis {
    largest_files: FileFinding[];
    large_files: FileFinding[];
    empty_files: string[];
    extension_counts: Record<string, number>;
}

// framework detection
export interface FrameworkDetection {
    name: string;
    category: string;
    evidence: string[];
}

// framework analysis
export interface FrameworkAnalysis {
    frameworks: FrameworkDetection[];
}

// dependency manifest
export interface DependencyManifest {
    path: string;
    ecosystem: string;
    package_manager: string | null;
    dependencies: number;
    dev_dependencies: number;
    has_lockfile: boolean;
}

// dependency manifest
export interface DependencyAnalysis {
    manifests: DependencyManifest[];
    total_dependencies: number;
    total_dev_dependencies: number;
    package_managers: string[];
}

// analysis result
export interface AnalysisResult {
    project_name: string;
    project_path: string;

    file_count: number;
    directory_count: number;
    total_lines: number;

    languages: Record<string, number>;

    todos: string[];
    fixmes: string[];

    has_readme: boolean;
    has_dockerfile: boolean;

    git: GitInfo | null;

    files: FileAnalysis;
    frameworks: FrameworkAnalysis;
    dependencies: DependencyAnalysis;
}

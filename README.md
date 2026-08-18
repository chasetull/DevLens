# DevLens

DevLens is a developer-focused codebase analysis platform that helps engineers understand the health, structure, and maintainability of their projects.

The initial version analyzes a local codebase and generates a project health dashboard containing code-quality findings, repository statistics, dependency information, documentation coverage, testing signals, and potential security concerns.

Future versions will add AI-assisted codebase exploration, architectural explanations, project memory, automated documentation, test generation, and controlled code modifications.

## Vision

Most AI developer tools begin with a chat window.

DevLens begins by understanding the project.

The long-term goal is to create an AI engineering companion that continuously develops context about a codebase, identifies issues proactively, explains architectural decisions, and helps developers safely improve their software.

## Core Principles

* Provide useful analysis before requiring an AI prompt.
* Analyze projects locally and avoid unnecessary repository cloning.
* Update project context incrementally when files change.
* Combine deterministic static analysis with AI-assisted reasoning.
* Show evidence and file references for every finding.
* Never modify code without explicit user approval.
* Build a polished product rather than a single-purpose AI demo.

## Initial MVP

The first DevLens release will allow a user to select or provide the path to a local project.

DevLens will scan the project and generate a health report containing:

### Project Overview

* Project name
* Primary languages
* Frameworks and libraries
* File and directory counts
* Total lines of code
* Repository size
* Git branch
* Most recent commit

### Code Quality

* TODO and FIXME comments
* Large files
* Large functions
* Duplicate-code candidates
* Deeply nested directories
* Common code-quality warnings

### Testing

* Test directories and files
* Detected testing frameworks
* Approximate source-to-test ratio
* Test coverage data when a coverage report is available

### Documentation

* README detection
* Documentation directories
* Missing or incomplete project documentation
* Documentation coverage indicators
* Public functions or modules without documentation

### Dependencies

* Detected package managers
* Direct dependency counts
* Development dependency counts
* Potentially unused dependencies
* Outdated dependency support in a later MVP iteration

### Security

* Potential hardcoded secrets
* Committed environment files
* Sensitive filenames
* Insecure configuration patterns
* Dependency vulnerability scanning in a later iteration

### Git Health

* Current branch
* Uncommitted changes
* Recent commit activity
* Stale branches
* Repository age
* Contributor count

## Example Dashboard

```text
Project Health: 82 / 100

Code Quality       84
Testing            61
Documentation      72
Security           91
Dependencies       79
Git Health         88

Recent Findings

⚠ 14 TODO comments detected
⚠ 3 source files exceed 500 lines
⚠ Test coverage information was not found
⚠ 2 possible hardcoded secrets require review
✓ README documentation detected
✓ Docker configuration detected
✓ No committed .env file detected
```

The health score will be presented as a helpful summary rather than an absolute measurement of software quality. Every score must be supported by visible findings.

## Product Roadmap

### Phase 1: Project Scanner

Build the local analysis engine.

* Accept a local project path
* Respect `.gitignore`
* Traverse the project safely
* Detect languages and frameworks
* Count files and lines of code
* Detect Git metadata
* Identify TODO and FIXME comments
* Detect large files and functions
* Return structured JSON results
* Add unit tests for scanner behavior

### Phase 2: Project Health Dashboard

Build the user-facing application.

* Create the React and TypeScript frontend
* Create the FastAPI backend
* Display project overview metrics
* Display categorized findings
* Add health scores and explanations
* Add filtering by severity and category
* Link findings to relevant file paths
* Add loading, empty, and error states

### Phase 3: Deeper Static Analysis

Improve the quality of deterministic analysis.

* Parse supported languages using Tree-sitter
* Identify functions, classes, imports, and modules
* Build a project dependency graph
* Detect circular dependencies
* Identify duplicate-code candidates
* Improve large-function detection
* Detect missing documentation
* Add configurable analysis rules

### Phase 4: Persistent Project Index

Allow DevLens to understand a project over time.

* Store project metadata
* Cache analysis results
* Hash files to detect changes
* Reanalyze only modified files
* Watch local projects for file changes
* Maintain analysis history
* Compare project health between scans

### Phase 5: AI Codebase Assistant

Add codebase-aware questions and explanations.

* Ask questions about the project
* Explain application architecture
* Explain individual files and modules
* Retrieve relevant code before answering
* Cite files and line ranges in responses
* Stream responses to the frontend
* Store project-specific conversations
* Prevent unsupported or ungrounded answers

### Phase 6: Engineering Memory

Preserve important project context.

* Record architectural decisions
* Store coding conventions
* Remember previous bugs and resolutions
* Track reasons behind major changes
* Connect memories to files and commits
* Allow users to edit or delete stored memories

### Phase 7: Developer Actions

Allow DevLens to assist with engineering work.

* Generate documentation
* Suggest refactors
* Generate unit tests
* Review Git diffs
* Propose multi-file changes
* Preview changes before applying them
* Run validation commands
* Display resulting diffs
* Require explicit approval before modifying files

### Phase 8: GitHub and Team Integrations

Expand DevLens beyond local projects.

* Connect GitHub repositories
* Analyze pull requests
* Review changed files
* Generate onboarding summaries
* Add issue and TODO tracking
* Support shared team knowledge
* Add role-based access controls

## Proposed Technology Stack

### Frontend

* React
* TypeScript
* Vite
* A component library or custom design system
* A charting library for dashboard visualizations

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### Analysis

* Python standard-library file processing
* Tree-sitter
* Ripgrep
* GitPython
* Language-specific analyzers where useful

### Storage

The initial MVP should not require a database.

Later phases may use:

* PostgreSQL
* pgvector
* Redis for caching or background-job coordination

### AI

AI functionality will be introduced after the deterministic project scanner and dashboard are functional.

Potential components include:

* Large-language-model API
* Embeddings
* Retrieval-augmented generation
* Structured tool calling
* Agent workflows only where they provide clear value

### Infrastructure

* Docker
* GitHub Actions
* Google Cloud Run
* Google Cloud Storage or Cloud SQL when persistent cloud storage becomes necessary

## Proposed Repository Structure

```text
devlens/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── analyzers/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── pyproject.toml
├── docs/
│   ├── architecture.md
│   └── roadmap.md
├── examples/
├── .github/
│   └── workflows/
├── .gitignore
├── docker-compose.yml
├── LICENSE
└── README.md
```

## Initial API Concept

```http
POST /api/v1/analysis
```

Example request:

```json
{
  "project_path": "/Users/example/projects/sample-app"
}
```

Example response:

```json
{
  "project": {
    "name": "sample-app",
    "languages": ["Python", "TypeScript"],
    "frameworks": ["FastAPI", "React"],
    "file_count": 214,
    "lines_of_code": 18420
  },
  "scores": {
    "overall": 82,
    "code_quality": 84,
    "testing": 61,
    "documentation": 72,
    "security": 91,
    "dependencies": 79,
    "git_health": 88
  },
  "findings": [
    {
      "category": "code_quality",
      "severity": "warning",
      "title": "Large source file",
      "description": "This file contains more than 500 lines.",
      "file_path": "backend/app/services/analyzer.py",
      "line": 1
    }
  ]
}
```

## First Development Milestone

The first milestone is complete when DevLens can:

1. Analyze its own repository.
2. Detect the repository's languages and frameworks.
3. Count files and lines of code.
4. identify TODO and FIXME comments.
5. Detect large files.
6. Read basic Git metadata.
7. Return all results through a FastAPI endpoint.
8. Display those results in a basic React dashboard.
9. Run through Docker.
10. Pass automated backend tests.

## Non-Goals for the Initial MVP

The first release will not:

* Edit source code
* Generate commits
* Clone remote repositories
* Require user accounts
* Store source code in the cloud
* Use an autonomous AI agent
* Support every programming language
* Produce a perfect or universal definition of code quality

## Development Status

DevLens is currently in early development.

The initial focus is building the local project scanner and defining a clear, evidence-based project health model.

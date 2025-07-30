# Python-Based CI Script Implementation Plan

> **Note**: This implementation should follow the existing GitHub Actions `python-ci.yml` workflow structure while providing enhanced local development capabilities.

## Overview

Replace bash-based CI with a Python implementation that uses a simple setup script and a main Python CI runner with quiet mode functionality. The implementation should mirror the GitHub Actions workflow for consistency.

## Architecture

### File Structure

```
scripts/
├── setup.py          # Environment setup script
├── ci.py             # Main Python CI runner
├── ci_config.py      # Configuration and utilities
└── README.md         # Updated documentation
```

## 1. Setup Script (`setup.py`)

**Purpose**: Simple environment preparation following python-ci.yml setup steps

```python
#!/usr/bin/env python3
"""
Setup script for CI environment.
Mirrors GitHub Actions setup-python and dependency installation steps.
"""

import subprocess
import sys
import venv
from pathlib import Path

def setup_environment():
    # Check Python 3.12+ requirement (as per python-ci.yml matrix)
    # Create/validate virtual environment
    # Install dependencies: pytest, pytest-cov, pytest-xdist
    # Install project in development mode: pip install -e ".[dev,test]"
    # Install additional tools: flake8, mypy, bandit, safety, build, twine
```

**Features**:

- Minimal output, clear success/failure indicators
- Exit codes for automation integration
- Cross-platform compatibility (Windows/Mac/Linux)

## 2. Main CI Script (`ci.py`)

**Purpose**: Execute all CI checks following python-ci.yml job structure

### CLI Interface

```bash
python scripts/ci.py [--quiet] [--clean] [--verbose] [--help]
```

### Core Architecture

```python
class CIRunner:
    def __init__(self, quiet=False, verbose=False, clean=False):
        self.quiet = quiet
        self.verbose = verbose
        self.results = {}

    def run_all_checks(self) -> Dict[str, Any]:
        """Execute all CI checks following python-ci.yml structure"""
        # Mirror the GitHub Actions jobs:
        # 1. Test job (pytest with coverage)
        # 2. Lint job (flake8, black, isort)
        # 3. Build job (package building)
        # 4. Security checks (bandit, safety)

    def save_results(self, results: Dict) -> None:
        """Save structured results to JSON"""
```

## 3. Quiet Mode Implementation

**Behavior**: Show only essential results, save full output to structured dictionaries

### Console Output Example

```
🔍 Code Quality:  ✅ Ruff  ✅ Black  ❌ MyPy  ✅ isort
🧪 Testing:      ✅ 133/133 tests passed (98.5% coverage)
🔒 Security:     ✅ No vulnerabilities found
📦 Build:        ✅ Package built successfully

Summary: 12/13 checks passed (92.3% success rate)
Details: ci-reports/results.json
Coverage: htmlcov/index.html
```

### Verbose Mode

- Full command output
- Real-time progress
- Detailed error messages
- Execution timing

## 4. Structured Data Output

### Results Dictionary Structure

```python
{
    "metadata": {
        "timestamp": "2025-06-25T16:30:00Z",
        "python_version": "3.12.7",
        "platform": "darwin",
        "project_version": "0.1.0-alpha.14",
        "ci_version": "1.0.0"
    },
    "summary": {
        "total_checks": 13,
        "passed": 12,
        "failed": 1,
        "success_rate": 92.31,
        "execution_time": 45.2
    },
    "jobs": {
        "test": {
            "status": "passed",
            "checks": {
                "pytest": {
                    "status": "passed",
                    "command": "pytest --cov=. --cov-report=xml --cov-report=html -v",
                    "output": "133 passed in 0.31s",
                    "execution_time": 5.2,
                    "details": {
                        "tests_run": 133,
                        "tests_passed": 133,
                        "tests_failed": 0,
                        "coverage_percentage": 98.5
                    }
                }
            }
        },
        "lint": {
            "status": "mixed",
            "checks": {
                "ruff": {
                    "status": "passed",
                    "command": "ruff check .",
                    "output": "All checks passed",
                    "execution_time": 2.1
                },
                "black": {
                    "status": "passed",
                    "command": "black --check --diff .",
                    "output": "would reformat 0 files",
                    "execution_time": 1.8
                },
                "mypy": {
                    "status": "failed",
                    "command": "mypy .",
                    "output": "Found 3 errors in 2 files",
                    "execution_time": 8.4,
                    "errors": ["error details..."]
                }
            }
        },
        "build": {
            "status": "passed",
            "checks": {
                "package_build": {
                    "status": "passed",
                    "command": "python -m build",
                    "output": "Successfully built package",
                    "execution_time": 12.3
                },
                "twine_check": {
                    "status": "passed",
                    "command": "twine check dist/*",
                    "output": "Checking dist files: PASSED",
                    "execution_time": 2.1
                }
            }
        }
    },
    "artifacts": {
        "coverage_xml": "ci-reports/coverage.xml",
        "coverage_html": "htmlcov/index.html",
        "test_results": "ci-reports/pytest.xml",
        "build_dist": "ci-reports/dist/",
        "reports": "ci-reports/"
    }
}
```

## 5. CI Configuration (`ci_config.py`)

```python
"""Configuration for CI tools and commands."""

# Mirror python-ci.yml tool configurations
CI_TOOLS = {
    "pytest": {
        "command": ["pytest", "--cov=.", "--cov-report=xml", "--cov-report=html", "-v", "--tb=short"],
        "env": {"PYTHONPATH": "."}
    },
    "ruff": {
        "command": ["ruff", "check", "."],
        "config_file": "pyproject.toml"
    },
    "black": {
        "command": ["black", "--check", "--diff", "."],
        "config_file": "pyproject.toml"
    },
    "mypy": {
        "command": ["mypy", "."],
        "allow_failure": True  # Continue on mypy errors like in CI
    },
    "flake8": {
        "command": ["flake8", ".", "--select=E9,F63,F7,F82", "--statistics"]
    }
}

# Path configurations
PATHS = {
    "reports": "ci-reports",
    "coverage_html": "htmlcov",
    "venv": ".venv",
    "dist": "dist"
}
```

## 6. Enhanced Features

### Parallel Execution

- Run independent checks concurrently (like GitHub Actions matrix)
- Respect tool dependencies (tests before coverage)
- Timeout handling per tool

### Smart Caching

- Skip unchanged files when possible
- Cache virtual environment
- Incremental test execution

### GitHub Actions Parity

```python
# Mirror the exact same tools and versions from python-ci.yml
GITHUB_ACTIONS_MATRIX = {
    "python_versions": ["3.12"],  # Focus on project requirement
    "tools": {
        "pytest": ">=8.0.0",
        "pytest-cov": ">=4.0.0",
        "black": ">=24.0.0",
        "ruff": ">=0.1.0",
        "mypy": ">=1.8.0"
    }
}
```

## 7. Usage Examples

### Basic Setup and Run

```bash
# One-time setup (like GitHub Actions setup-python step)
python scripts/setup.py

# Full CI run (like GitHub Actions test job)
python scripts/ci.py

# Quiet mode - just results
python scripts/ci.py --quiet

# Clean previous artifacts + run
python scripts/ci.py --clean --quiet
```

### Integration Examples

```bash
# Pre-commit hook
python scripts/ci.py --quiet && git commit

# Quick validation
python scripts/ci.py --quiet || echo "Fix issues before pushing"

# Full validation with cleanup
python scripts/ci.py --clean --verbose
```

## 8. Benefits of Python Approach

### Cross-Platform Compatibility

- Works identically on Windows, macOS, Linux
- No shell script compatibility issues
- Consistent path handling

### Rich Output & Progress

- Rich console library for beautiful output
- Progress bars for long operations
- Colored status indicators
- Structured error reporting

### Machine-Readable Results

- JSON output for automation
- Structured data for reporting
- Easy integration with other tools
- Historical tracking capabilities

### Better Error Handling

- Graceful failure handling
- Detailed error context
- Recovery suggestions
- Non-blocking warnings

### Extensibility

- Easy to add new tools
- Plugin architecture possibility
- Custom reporting formats
- Integration hooks

## 9. GitHub Actions Workflow Compatibility

The Python implementation should maintain 1:1 compatibility with the existing `python-ci.yml`:

### Job Structure Mapping

```yaml
# python-ci.yml jobs become Python CI modules
test: → TestRunner class
lint: → LintRunner class
build: → BuildRunner class
```

### Tool Version Consistency

- Use exact same tool versions as defined in pyproject.toml
- Mirror the GitHub Actions installation steps
- Maintain same configuration files (pyproject.toml, ruff.toml)

### Output Format Compatibility

- Generate same artifacts (coverage.xml, test results)
- Use same directory structure
- Respect same ignore patterns (.gitignore)

This ensures that local CI results accurately predict GitHub Actions outcomes, providing developers with confidence before pushing changes.

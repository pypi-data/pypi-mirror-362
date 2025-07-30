# Scripts Directory

This directory contains utility scripts for the AD User Manager project.

## local-ci.sh

A comprehensive local CI script that mirrors the GitHub Actions workflow for testing and validation before pushing to remote repositories.

### Features

- **Environment Setup**: Validates Python version and creates virtual environment
- **Code Quality**: Runs ruff, black, isort, mypy, and flake8 checks
- **Testing**: Executes pytest with coverage reporting
- **Security**: Runs bandit and safety scans
- **Build Validation**: Tests package building and validation
- **Reporting**: Generates comprehensive reports and summaries

### Usage

```bash
# Run full CI pipeline
./scripts/local-ci.sh

# Clean previous artifacts and run CI
./scripts/local-ci.sh --clean

# Run with verbose output
./scripts/local-ci.sh --verbose

# Show help
./scripts/local-ci.sh --help
```

### Output

The script generates reports in `./ci-reports/` directory:

- `summary.txt` - Overall CI summary
- `pytest.txt` - Test execution output
- `coverage.xml` - Coverage data (XML)
- `htmlcov/` - Coverage report (HTML)
- `ruff.txt` - Ruff linting results
- `black.txt` - Black formatting check results
- `mypy.txt` - MyPy type checking results
- `bandit.json/txt` - Security scan results
- `safety.json/txt` - Vulnerability check results
- `build.txt` - Package build output
- `dist/` - Built packages

### Requirements

- Python 3.12+
- Project dependencies (installed automatically)
- Git (for repository detection)

### GitHub Actions Compatibility

This script mirrors the GitHub Actions workflow defined in `.github/workflows/python-ci.yml`:

- **Python Version**: Tests with Python 3.12
- **Dependencies**: Uses same package versions
- **Test Matrix**: Simulates single platform (local OS)
- **Quality Checks**: Same tools and configurations
- **Security**: Same security scanning tools
- **Build**: Same build and validation process

### Integration with .gitignore

The script respects the project's `.gitignore` file:

- Reports are generated in ignored directories
- Temporary files are automatically cleaned up
- Build artifacts follow ignore patterns
- Coverage files respect ignore rules

### Exit Codes

- `0` - All checks passed
- `1` - One or more checks failed

### Tips

1. **Pre-commit**: Run before committing to catch issues early
2. **Clean Run**: Use `--clean` after major changes
3. **Verbose Mode**: Use `--verbose` for debugging CI issues
4. **Coverage**: Check `htmlcov/index.html` for detailed coverage reports
5. **Security**: Review bandit and safety reports for security issues

### Troubleshooting

**Virtual Environment Issues**:
```bash
# Remove and recreate venv
rm -rf .venv
./scripts/local-ci.sh
```

**Permission Issues**:
```bash
# Make script executable
chmod +x scripts/local-ci.sh
```

**Python Version Issues**:
```bash
# Check Python version
python3 --version
# Should be 3.12 or higher
```

**Dependency Issues**:
```bash
# Clean install
./scripts/local-ci.sh --clean
```
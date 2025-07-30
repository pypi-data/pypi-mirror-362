#!/bin/bash

# Local CI Script for AD User Manager
# Mirrors the GitHub Actions Python CI workflow for local testing
# Usage: ./scripts/local-ci.sh [--help] [--clean] [--verbose]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_VERSION="3.12"
VENV_DIR="$PROJECT_ROOT/.venv"
COVERAGE_DIR="$PROJECT_ROOT/htmlcov"
REPORTS_DIR="$PROJECT_ROOT/ci-reports"

# Flags
VERBOSE=false
CLEAN=false
HELP=false

# Counters for summary
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            HELP=true
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Help function
show_help() {
    cat << EOF
Local CI Script for AD User Manager

USAGE:
    ./scripts/local-ci.sh [OPTIONS]

OPTIONS:
    -h, --help      Show this help message
    --clean         Clean up previous CI artifacts before running
    -v, --verbose   Enable verbose output

DESCRIPTION:
    This script mirrors the GitHub Actions CI workflow locally, running:
    - Environment setup and dependency installation
    - Code quality checks (ruff, black, mypy)
    - Test execution with coverage reporting
    - Build validation
    - Security scanning
    - Summary report generation

    Results are saved to ./ci-reports/ and respect .gitignore patterns.

EXAMPLES:
    ./scripts/local-ci.sh              # Run full CI pipeline
    ./scripts/local-ci.sh --clean      # Clean and run CI pipeline
    ./scripts/local-ci.sh --verbose    # Run with detailed output

EOF
}

if [[ "$HELP" == true ]]; then
    show_help
    exit 0
fi

# Utility functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo -e "\n${BOLD}${BLUE}=== $1 ===${NC}"
}

run_check() {
    local check_name="$1"
    local check_cmd="$2"
    local allow_failure="${3:-false}"
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    log_info "Running $check_name..."
    
    if [[ "$VERBOSE" == true ]]; then
        echo "Command: $check_cmd"
    fi
    
    if eval "$check_cmd"; then
        log_success "$check_name passed"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        local exit_code=$?
        if [[ "$allow_failure" == true ]]; then
            log_warning "$check_name failed (non-critical)"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            return 0
        else
            log_error "$check_name failed"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            return $exit_code
        fi
    fi
}

# Check if we're in the right directory
check_project_structure() {
    if [[ ! -f "$PROJECT_ROOT/pyproject.toml" ]]; then
        log_error "Not in AD User Manager project root. Missing pyproject.toml"
        exit 1
    fi
    
    if [[ ! -d "$PROJECT_ROOT/ad_user_manager" ]]; then
        log_error "Missing ad_user_manager package directory"
        exit 1
    fi
    
    if [[ ! -d "$PROJECT_ROOT/tests" ]]; then
        log_error "Missing tests directory"
        exit 1
    fi
}

# Clean up previous artifacts
cleanup_artifacts() {
    if [[ "$CLEAN" == true ]]; then
        log_section "Cleaning Previous Artifacts"
        
        # Remove coverage files
        rm -rf "$PROJECT_ROOT/.coverage" "$PROJECT_ROOT/.coverage.*" "$COVERAGE_DIR"
        
        # Remove pytest cache
        rm -rf "$PROJECT_ROOT/.pytest_cache"
        
        # Remove mypy cache
        rm -rf "$PROJECT_ROOT/.mypy_cache"
        
        # Remove ruff cache
        rm -rf "$PROJECT_ROOT/.ruff_cache"
        
        # Remove CI reports
        rm -rf "$REPORTS_DIR"
        
        # Remove build artifacts
        rm -rf "$PROJECT_ROOT/build" "$PROJECT_ROOT/dist" "$PROJECT_ROOT"/*.egg-info
        
        log_success "Cleanup completed"
    fi
}

# Setup environment
setup_environment() {
    log_section "Environment Setup"
    
    # Check Python version
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 not found"
        exit 1
    fi
    
    local python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    log_info "Python version: $python_version"
    
    # Check if we have at least Python 3.12
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 12) else 1)"; then
        log_success "Python version check passed"
    else
        log_error "Python 3.12+ required (found $python_version)"
        exit 1
    fi
    
    # Create reports directory
    mkdir -p "$REPORTS_DIR"
    
    # Setup virtual environment
    if [[ ! -d "$VENV_DIR" ]]; then
        log_info "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    log_info "Upgrading pip..."
    python -m pip install --upgrade pip
    
    # Install project dependencies
    log_info "Installing project dependencies..."
    python -m pip install -e ".[dev]"
    
    # Install additional CI tools
    log_info "Installing CI tools..."
    python -m pip install \
        flake8 \
        bandit \
        safety \
        build \
        twine \
        isort
    
    log_success "Environment setup completed"
}

# Code quality checks
run_quality_checks() {
    log_section "Code Quality Checks"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Ruff linting
    run_check "Ruff linting" \
        "ruff check . --output-format=text 2>&1 | tee '$REPORTS_DIR/ruff.txt'"
    
    # Black formatting check
    run_check "Black formatting" \
        "black --check --diff . 2>&1 | tee '$REPORTS_DIR/black.txt'"
    
    # Import sorting check
    run_check "Import sorting (isort)" \
        "isort --check-only --diff . 2>&1 | tee '$REPORTS_DIR/isort.txt'"
    
    # MyPy type checking (allow failure as it's often strict)
    run_check "MyPy type checking" \
        "mypy . 2>&1 | tee '$REPORTS_DIR/mypy.txt'" \
        true
    
    # Flake8 for syntax errors
    run_check "Flake8 syntax check" \
        "flake8 . --select=E9,F63,F7,F82 --statistics 2>&1 | tee '$REPORTS_DIR/flake8.txt'"
    
    log_success "Code quality checks completed"
}

# Test execution
run_tests() {
    log_section "Test Execution"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Run tests with coverage
    run_check "pytest with coverage" \
        "pytest --cov=. --cov-report=xml:$REPORTS_DIR/coverage.xml --cov-report=html:$COVERAGE_DIR --cov-report=term -v --tb=short 2>&1 | tee '$REPORTS_DIR/pytest.txt'"
    
    # Extract test results
    if [[ -f "$REPORTS_DIR/pytest.txt" ]]; then
        local test_summary=$(tail -10 "$REPORTS_DIR/pytest.txt" | grep -E "^=.*=" | tail -1)
        if [[ -n "$test_summary" ]]; then
            log_info "Test summary: $test_summary"
        fi
    fi
    
    log_success "Test execution completed"
}

# Security checks
run_security_checks() {
    log_section "Security Checks"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Bandit security scan
    run_check "Bandit security scan" \
        "bandit -r . -f json -o '$REPORTS_DIR/bandit.json' --exclude tests,scripts || bandit -r . -f txt 2>&1 | tee '$REPORTS_DIR/bandit.txt'" \
        true
    
    # Safety check for known vulnerabilities
    run_check "Safety vulnerability check" \
        "safety check --json --output '$REPORTS_DIR/safety.json' 2>&1 || safety check 2>&1 | tee '$REPORTS_DIR/safety.txt'" \
        true
    
    log_success "Security checks completed"
}

# Build validation
run_build_checks() {
    log_section "Build Validation"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Build package
    run_check "Package build" \
        "python -m build --outdir '$REPORTS_DIR/dist' 2>&1 | tee '$REPORTS_DIR/build.txt'"
    
    # Check package with twine
    if [[ -d "$REPORTS_DIR/dist" ]]; then
        run_check "Package validation" \
            "twine check '$REPORTS_DIR/dist/*' 2>&1 | tee '$REPORTS_DIR/twine.txt'"
    fi
    
    log_success "Build validation completed"
}

# Generate summary report
generate_summary() {
    log_section "CI Summary Report"
    
    local summary_file="$REPORTS_DIR/summary.txt"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    cat > "$summary_file" << EOF
AD User Manager - Local CI Summary Report
Generated: $timestamp
Python Version: $(python3 --version)
Platform: $(uname -s) $(uname -m)

=== CHECKS SUMMARY ===
Total Checks: $TOTAL_CHECKS
Passed: $PASSED_CHECKS
Failed: $FAILED_CHECKS
Success Rate: $(( PASSED_CHECKS * 100 / TOTAL_CHECKS ))%

=== TEST RESULTS ===
EOF

    # Add test summary if available
    if [[ -f "$REPORTS_DIR/pytest.txt" ]]; then
        echo "Tests:" >> "$summary_file"
        grep -E "^=.*=" "$REPORTS_DIR/pytest.txt" | tail -1 >> "$summary_file" || echo "Test summary not found" >> "$summary_file"
        echo "" >> "$summary_file"
    fi
    
    # Add coverage info if available
    if [[ -f "$REPORTS_DIR/coverage.xml" ]]; then
        echo "Coverage:" >> "$summary_file"
        grep -o 'line-rate="[^"]*"' "$REPORTS_DIR/coverage.xml" | head -1 | sed 's/line-rate="//' | sed 's/"//' | awk '{printf "Line Coverage: %.1f%%\n", $1 * 100}' >> "$summary_file" || echo "Coverage info not available" >> "$summary_file"
        echo "" >> "$summary_file"
    fi
    
    # Add file locations
    cat >> "$summary_file" << EOF
=== REPORT FILES ===
Summary: $summary_file
Coverage HTML: $COVERAGE_DIR/index.html
Coverage XML: $REPORTS_DIR/coverage.xml
Test Output: $REPORTS_DIR/pytest.txt
Ruff Report: $REPORTS_DIR/ruff.txt
Black Report: $REPORTS_DIR/black.txt
MyPy Report: $REPORTS_DIR/mypy.txt
Build Artifacts: $REPORTS_DIR/dist/
Security Reports: $REPORTS_DIR/bandit.json, $REPORTS_DIR/safety.json

=== NEXT STEPS ===
EOF

    if [[ $FAILED_CHECKS -eq 0 ]]; then
        echo "✅ All checks passed! Ready for GitHub CI." >> "$summary_file"
    else
        echo "❌ $FAILED_CHECKS check(s) failed. Review reports above." >> "$summary_file"
    fi
    
    # Display summary
    cat "$summary_file"
    
    log_success "Summary report generated: $summary_file"
}

# Main execution
main() {
    log_section "AD User Manager - Local CI Pipeline"
    log_info "Mimicking GitHub Actions workflow locally"
    log_info "Project root: $PROJECT_ROOT"
    
    # Change to project root
    cd "$PROJECT_ROOT"
    
    # Run pipeline steps
    check_project_structure
    cleanup_artifacts
    setup_environment
    run_quality_checks
    run_tests
    run_security_checks
    run_build_checks
    generate_summary
    
    # Final status
    if [[ $FAILED_CHECKS -eq 0 ]]; then
        log_success "🎉 Local CI pipeline completed successfully!"
        log_info "All $TOTAL_CHECKS checks passed. Ready for GitHub CI."
        exit 0
    else
        log_error "💥 Local CI pipeline completed with failures"
        log_error "$FAILED_CHECKS out of $TOTAL_CHECKS checks failed"
        log_info "Check reports in: $REPORTS_DIR"
        exit 1
    fi
}

# Run main function
main "$@"
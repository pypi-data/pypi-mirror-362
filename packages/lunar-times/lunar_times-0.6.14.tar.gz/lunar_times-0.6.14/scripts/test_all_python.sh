#!/bin/bash

# Test script to run linting and tests across multiple Python versions
# This mimics the GitHub Actions CI pipeline locally

set -e  # Exit on any error

echo "🔍 Multi-Python Testing Script"
echo "=============================="
echo ""

# Python versions to test (available locally)
PYTHON_VERSIONS=("3.8.20" "3.9.23" "3.10.15" "3.11.10" "3.12.11")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to run tests for a specific Python version
test_python_version() {
    local version=$1
    echo -e "${BLUE}Testing Python $version${NC}"
    echo "----------------------------------------"
    
    # Install Python version if not available
    if ! uv python list | grep -q "$version"; then
        echo -e "${YELLOW}Installing Python $version...${NC}"
        uv python install "$version"
    fi
    
    # Create temporary environment for this Python version
    local temp_dir=$(mktemp -d)
    cd "$temp_dir"
    
    # Copy project files
    cp -r "$OLDPWD"/* . 2>/dev/null || true
    
    # Create virtual environment with specific Python version
    echo "Creating virtual environment..."
    uv venv --python "$version" .venv-test
    
    # Install dependencies
    echo "Installing dependencies..."
    uv pip install --python .venv-test/bin/python -e ".[dev]"
    
    # Run linting
    echo -e "${YELLOW}Running linting...${NC}"
    if .venv-test/bin/python -m flake8 src/ tests/ --max-line-length=79; then
        echo -e "${GREEN}✓ Linting passed${NC}"
    else
        echo -e "${RED}✗ Linting failed${NC}"
        cd "$OLDPWD"
        rm -rf "$temp_dir"
        return 1
    fi
    
    # Run type checking
    echo -e "${YELLOW}Running type checking...${NC}"
    if .venv-test/bin/python -m mypy src/; then
        echo -e "${GREEN}✓ Type checking passed${NC}"
    else
        echo -e "${RED}✗ Type checking failed${NC}"
        cd "$OLDPWD"
        rm -rf "$temp_dir"
        return 1
    fi
    
    # Run tests
    echo -e "${YELLOW}Running tests...${NC}"
    if .venv-test/bin/python -m pytest tests/ -v; then
        echo -e "${GREEN}✓ Tests passed${NC}"
    else
        echo -e "${RED}✗ Tests failed${NC}"
        cd "$OLDPWD"
        rm -rf "$temp_dir"
        return 1
    fi
    
    # Cleanup
    cd "$OLDPWD"
    rm -rf "$temp_dir"
    
    echo -e "${GREEN}✓ Python $version: ALL TESTS PASSED${NC}"
    echo ""
}

# Main execution
echo "Available Python versions for testing:"
for version in "${PYTHON_VERSIONS[@]}"; do
    if uv python list | grep -q "$version"; then
        echo -e "  ${GREEN}✓${NC} Python $version"
    else
        echo -e "  ${YELLOW}○${NC} Python $version (will install)"
    fi
done
echo ""

# Ask user which versions to test
echo "Select testing mode:"
echo "1. Test all versions (recommended before major commits)"
echo "2. Test Python 3.12 only (quick check for recent linting issues)"
echo "3. Test specific version"
echo "4. Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "Testing all Python versions..."
        failed_versions=()
        for version in "${PYTHON_VERSIONS[@]}"; do
            if ! test_python_version "$version"; then
                failed_versions+=("$version")
            fi
        done
        
        if [ ${#failed_versions[@]} -eq 0 ]; then
            echo -e "${GREEN}🎉 ALL PYTHON VERSIONS PASSED!${NC}"
            echo "Safe to commit and push."
        else
            echo -e "${RED}❌ FAILED VERSIONS: ${failed_versions[*]}${NC}"
            echo "Fix issues before committing."
            exit 1
        fi
        ;;
    2)
        echo "Testing Python 3.12 only..."
        if test_python_version "3.12.11"; then
            echo -e "${GREEN}🎉 Python 3.12 tests passed!${NC}"
        else
            echo -e "${RED}❌ Python 3.12 tests failed!${NC}"
            exit 1
        fi
        ;;
    3)
        echo "Available versions: ${PYTHON_VERSIONS[*]}"
        read -p "Enter Python version (e.g., 3.12.11): " custom_version
        if test_python_version "$custom_version"; then
            echo -e "${GREEN}🎉 Python $custom_version tests passed!${NC}"
        else
            echo -e "${RED}❌ Python $custom_version tests failed!${NC}"
            exit 1
        fi
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac 
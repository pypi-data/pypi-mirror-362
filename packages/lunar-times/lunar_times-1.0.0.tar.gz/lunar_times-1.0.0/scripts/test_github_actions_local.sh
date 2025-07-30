#!/bin/bash

# Test GitHub Actions workflows locally using act
# This requires the 'act' tool: https://github.com/nektos/act

set -e

echo "🚀 GitHub Actions Local Testing"
echo "==============================="
echo ""

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo "❌ 'act' tool is not installed."
    echo ""
    echo "Install act to run GitHub Actions locally:"
    echo "  # On Ubuntu/Debian:"
    echo "  curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"
    echo ""
    echo "  # On macOS:"
    echo "  brew install act"
    echo ""
    echo "  # On Arch Linux:"
    echo "  yay -S act"
    echo ""
    echo "For more installation options, see: https://github.com/nektos/act#installation"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running."
    echo "Please start Docker and try again."
    exit 1
fi

echo "✅ act tool found"
echo "✅ Docker is running"
echo ""

# Show available workflows
echo "Available GitHub Actions workflows:"
act --list
echo ""

# Ask user what to test
echo "Select what to test:"
echo "1. Test CI workflow (full pipeline)"
echo "2. Test specific job"
echo "3. List all workflows"
echo "4. Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "Running CI workflow locally..."
        echo "This will test the full CI pipeline including linting, testing, and building."
        echo ""
        act --workflows .github/workflows/ci.yml -v
        ;;
    2)
        echo "Available jobs:"
        act --list | grep -E "Job|Stage"
        echo ""
        read -p "Enter job name: " job_name
        act --workflows .github/workflows/ci.yml --job "$job_name" -v
        ;;
    3)
        echo "All workflows:"
        act --list
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
#!/bin/bash
set -e

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

# Build the package
echo "Building the package..."
python -m build

# Check the package (optional)
echo "Checking the package..."
twine check dist/*

# Upload to PyPI
echo "Uploading to PyPI..."
if [ -z "$PYPI_TOKEN" ]; then
  echo "Error: PYPI_TOKEN environment variable not set."
  exit 1
fi
twine upload dist/* -u __token__ -p $PYPI_TOKEN

echo "Upload complete!" 
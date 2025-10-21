#!/bin/bash
# Copyright 2025 Alejandro Martínez Corriá and the Thinkube contributors
# SPDX-License-Identifier: Apache-2.0

# Validate that all notebooks are properly cleaned
# Usage: ./scripts/validate_notebooks.sh

set -e

echo "Validating Jupyter notebooks..."

# Find all notebooks
NOTEBOOKS=$(find . -name "*.ipynb" -not -path "./.ipynb_checkpoints/*" -not -path "*/\.*")

if [ -z "$NOTEBOOKS" ]; then
    echo "No notebooks found"
    exit 0
fi

ERRORS=0

for notebook in $NOTEBOOKS; do
    echo "Checking $notebook..."

    # Check for execution output
    if grep -q '"outputs": \[' "$notebook"; then
        # Check if outputs array is not empty
        if ! grep -q '"outputs": \[\]' "$notebook"; then
            echo "  ❌ ERROR: Notebook contains execution output"
            ERRORS=$((ERRORS + 1))
        fi
    fi

    # Check for execution counts
    if grep -q '"execution_count": [0-9]' "$notebook"; then
        echo "  ❌ ERROR: Notebook contains execution counts"
        ERRORS=$((ERRORS + 1))
    fi

    # Check for valid JSON syntax
    if ! python3 -m json.tool "$notebook" > /dev/null 2>&1; then
        echo "  ❌ ERROR: Invalid JSON syntax"
        ERRORS=$((ERRORS + 1))
    fi

    # If no errors for this notebook
    if [ $ERRORS -eq 0 ]; then
        echo "  ✅ Clean"
    fi
done

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "❌ Validation failed with $ERRORS error(s)"
    echo ""
    echo "To clean notebooks, run:"
    echo "  nbstripout <notebook.ipynb>"
    echo ""
    echo "Or install pre-commit hooks to clean automatically:"
    echo "  pip install pre-commit"
    echo "  pre-commit install"
    exit 1
fi

echo ""
echo "✅ All notebooks are clean!"
exit 0

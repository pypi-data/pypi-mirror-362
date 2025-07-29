#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Run pydocstyle
if pydocstyle wizard; then
# Run flake8
  flake8 wizard
else
    echo "pydocstyle check failed, skipping flake8."
    break
fi

pytest --cov=wizard --cov-report=term-missing

# Deactivate the virtual environment
deactivate

# Cleanup temporary coverage files
find . -maxdepth 1 -type f -name ".coverage.*" -delete

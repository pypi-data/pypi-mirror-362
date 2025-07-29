#!/usr/bin/env bash

###
# Run pytest with optional snapshot update
# Usage:
#   bash scripts/test.sh --container ## Run tests in Docker
#   bash scripts/test.sh --container --snapshot-update ## Run tests in Docker with snapshot update
###
set -euo pipefail

# Get the project root directory
SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

cd -- "$DIR"

# Function to run tests in Docker
run_in_docker() {
  echo "Running tests in Docker container..."
  docker run -v "$(pwd)":/tseqmock --rm tseqmock-env-test:py3.10.12 bash -c "cd /tseqmock && pip install -e .[test] && pytest $@"
}

# Check if --container option is passed
if [[ "${1:-}" == "--container" ]]; then
  run_in_docker "${@:2}"  # Pass the remaining arguments to pytest (e.g. --update)
  exit 0
fi

# Setup virtual environment if needed
if [[ ! -e ./venv ]]; then
  echo "Creating virtual environment..."
  bash ./scripts/install_in_venv.sh
fi

# Activate the virtual environment
source ./venv/bin/activate

# Handle optional --update flag
if [[ "${1:-}" == "--update" ]]; then
  echo "Running tests with snapshot update..."
  pytest --snapshot-update  --import-mode=importlib tests/
else
  echo "Running tests..."
  pytest -vv --import-mode=importlib tests/
fi

#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

cd -- "$DIR"

function show_help()
{
  cat << HELP
USAGE

  ${0##*/} [-h] [-v]

OPTIONS

  -h
    Show this help message and exit.

  -v
    Use a Python virtual environment to build the documentation.

HELP
  exit "$1"
}

in_venv=false
while getopts "hv" opt
do
  case "$opt" in
    h) show_help 0 ;;
    v) in_venv=true ;;
    *) show_help 1 ;;
  esac
done

if "$in_venv"
then
  if [[ -e venv ]]
  then
    python -m venv venv
    source venv/bin/activate
    pip install -U pip
  else
    source venv/bin/activate
  fi
fi
pip install -U -r doc/requirements.txt
sphinx-apidoc -o doc/source -f -H "API Documentation" ./src
sphinx-build -b html doc/source public

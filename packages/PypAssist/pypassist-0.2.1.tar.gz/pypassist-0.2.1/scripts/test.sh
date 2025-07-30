#!/usr/bin/env bash
###
#
# Run the test
#
###
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

cd -- "$DIR"
if [[ ! -e ./venv ]]
then
  bash ./scripts/install_in_venv.sh
fi
source ./venv/bin/activate
python -m unittest discover -v ./tests
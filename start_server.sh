#!/bin/sh

set -x

export FLASK_APP=run.py
export FLASK_RUN_PORT=8000

which python

python --version

echo ""

###flask run
python ./${FLASK_APP}

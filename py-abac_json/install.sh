#!/bin/bash

cd "$(dirname "$0")"

python3 -m pip uninstall py_abac --break-system-packages
python3 -m pip install ./py_abac-0.4.1-py3-none-any.whl --break-system-packages

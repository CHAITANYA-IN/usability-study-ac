#!/bin/bash

cd "$(dirname "$0")"

curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static
chmod 755 opa

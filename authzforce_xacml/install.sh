#!/bin/bash

cd "$(dirname "$0")"

curl -o authzforce-pdp-cli https://repo1.maven.org/maven2/org/ow2/authzforce/authzforce-ce-core-pdp-cli/21.0.1/authzforce-ce-core-pdp-cli-21.0.1.jar
chmod a+x ./authzforce-pdp-cli

#!/bin/bash

cd "$(dirname "$0")"

./authzforce-pdp-cli -p -t XACML_XML ./pdp.xml ./request.xml
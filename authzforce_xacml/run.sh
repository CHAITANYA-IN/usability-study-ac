#!/bin/bash

cd "$(dirname "$0")"

for count in {1..3}; do
    echo "Request $count"
    ./authzforce-pdp-cli -p -t XACML_XML ./pdp.xml ./request$count.xml
done

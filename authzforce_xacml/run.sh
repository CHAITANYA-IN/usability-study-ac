#!/bin/bash

cd "$(dirname "$0")"

for filename in $(ls request*.xml); do
    echo "Request from $filename"
    ./authzforce-pdp-cli -p -t XACML_XML ./pdp.xml "$filename"
done

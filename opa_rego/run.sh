#!/bin/bash

cd "$(dirname "$0")"

count=1
for request in $(jq -c '.[]' ./requests.json); do
    echo "Request $count"
    echo $request | ./opa eval -I -d policy.rego "data.evalpro.allow_upload_submission"
    count=$((count + 1))
done

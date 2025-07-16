#!/bin/bash

for request in $(jq -c '.[]' ./requests.json); do
    echo $request | opa eval -I -d policy.rego "data.evalpro.allow_upload_submission"
done

"""Enable Upload Submission"""

import datetime
import ipaddress
import json
import casbin

CONF_PATH = "."

MODEL_CONF_FILE_PATH = f"{CONF_PATH}/policy-meta.conf"
POLICY_RULES_FILE_PATH = f"{CONF_PATH}/policy-rules.csv"
REQUESTS_FILE_PATH = f"{CONF_PATH}/requests.json"

e = casbin.Enforcer(MODEL_CONF_FILE_PATH, POLICY_RULES_FILE_PATH)

def ip_range_check(ip_address, ip_ranges):
    "Check IP address is in given IP range by converting them into 32-bit integers"
    machine_ip = ipaddress.IPv4Address(ip_address)
    for start_ip_address, end_ip_address in ip_ranges:
        start_ip = ipaddress.IPv4Address(start_ip_address)
        end_ip = ipaddress.IPv4Address(end_ip_address)
        if start_ip <= machine_ip <= end_ip:
            return True
    return False


requests = json.load(open(REQUESTS_FILE_PATH, encoding='utf-8'))

"""Resolving IP range check and adding current date time"""
for request in requests:
    request[0]['is_ip_in_range'] = ip_range_check(
        request[0]['ip_address'],
        request[2]['allowed_ip_ranges']
    )
    request[-1]['time'] = datetime.datetime.now().isoformat()

for request in requests:
    if e.enforce(*request):
        print("Permit")
    else:
        print("Deny")

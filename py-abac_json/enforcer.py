import datetime
import json

from py_abac import PDP, Policy, Request, EvaluationAlgorithm
from py_abac.storage.memory import MemoryStorage
from py_abac.provider.base import AttributeProvider

class TimeAttributeProvider(AttributeProvider):
    def get_attribute_value(self, ace, attribute_path, ctx):
        if attribute_path == "$.lab.end":
            start = datetime.datetime.fromisoformat(ctx.get_attribute_value("resource", "$.lab.start"))
            duration = self.get_delta_from_duration_string(ctx.get_attribute_value("resource", "$.lab.duration"))
            return (start + duration).isoformat()

    def get_delta_from_duration_string(self, duration_string):
        return datetime.datetime.strptime(duration_string, "%H:%M:%S") - datetime.datetime.strptime("0", "%S")

policy_json = json.load(open("policy.json", "r", encoding="utf-8"))

policy = Policy.from_json(policy_json)

storage = MemoryStorage()
storage.add(policy)

pdp = PDP(storage, EvaluationAlgorithm.DENY_OVERRIDES, [TimeAttributeProvider()])

requests_json = json.load(open("requests.json", "r", encoding="utf-8"))

for request_json in requests_json:
    request = Request.from_json(request_json)

    if pdp.is_allowed(request):
        print("Allow operation")
    else:
        print("Deny operation")

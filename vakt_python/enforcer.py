import datetime
import json
import vakt
from policy import policies

storage = vakt.MemoryStorage()
for policy in policies:
    storage.add(policy)

guard = vakt.Guard(storage, vakt.RulesChecker())

requests_json = json.load(open("requests.json", "r", encoding="utf-8"))
for request_json in requests_json:
    request_json['resource'] = {
        'course': request_json['course'],
        'lab': request_json['lab'],
        'program': request_json['program'],
    }
    inquiry = vakt.Inquiry(
        resource=request_json['resource'],
        subject=request_json['user'],
        context={
            'currentTime': datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
            # "2025-06-12T10:00:00+05:30"
        }
    )
    print(guard.is_allowed(inquiry))

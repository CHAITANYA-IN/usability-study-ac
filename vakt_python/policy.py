import vakt
from vakt.rules import Any
from vakt_python.additional_rules import InIPRangesResource, DateTimeBetweenResource

policies = [
    vakt.Policy(
        uid="lab-access",
        description="Allow lab access during specified hours from allowed IPs",
        subjects=[{
            'ip_address': InIPRangesResource('lab.allowed_ip_ranges')
        }],
        resources=[Any()],
        actions=[Any()],
        context={
            'currentTime': DateTimeBetweenResource('lab.start', 'lab.end'),
        },
        effect=vakt.ALLOW_ACCESS
    )
]
# !!!!!!!!!!!!!!!!!!!!! ----> DEPTH > 1 ON LHS, DOES NOT WORK
# resources={
#     'lab': {
#         'availableFrom': DateTimeBetweenResource('lab.availableFrom', 'lab.availableTill'),
#         'availableTill': DateTimeBetweenResource('lab.availableFrom', 'lab.availableTill'),
#         'allowedIPRanges': InIPRangesResource('lab.allowedIPRanges')
#     },
# },
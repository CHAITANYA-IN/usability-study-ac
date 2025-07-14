import datetime
import ipaddress
from vakt.rules.base import Rule

class DateTimeBetweenResource(Rule):
    def __init__(self, start_path, end_path):
        self.start_path = start_path.split('.')
        self.end_path = end_path.split('.')

    def _get_value(self, data, path):
        for p in path:
            data = data.get(p, {})
        return data

    def satisfied(self, what, inquiry=None):
        start_str = self._get_value(inquiry.resource, self.start_path)
        end_str = self._get_value(inquiry.resource, self.end_path)

        current_time = datetime.datetime.fromisoformat(what)
        start = datetime.datetime.fromisoformat(start_str)
        end = datetime.datetime.fromisoformat(end_str)
        return start <= current_time <= end

class InIPRangesResource(Rule):
    def __init__(self, resource_ip_range_attr):
        self.resource_ip_range_attr = resource_ip_range_attr.split('.')

    def _get_value(self, data, path):
        for p in path:
            data = data.get(p, {})
        return data

    def _ip_in_range(self, ip, ip_range):
        # Handle CIDR notation
        if '/' in ip_range:
            try:
                return ipaddress.ip_address(ip) in ipaddress.ip_network(ip_range, strict=False)
            except ValueError:
                return False

        # Handle dash-separated range: "startIP-endIP"
        if '-' in ip_range:
            try:
                start_ip, end_ip = ip_range.split('-')
                ip_obj = ipaddress.ip_address(ip)
                start_obj = ipaddress.ip_address(start_ip)
                end_obj = ipaddress.ip_address(end_ip)
                return start_obj <= ip_obj <= end_obj
            except ValueError:
                return False

        # Single IP
        try:
            return ip == ip_range
        except Exception:
            return False

    def satisfied(self, what, inquiry=None):
        subject_ip = what
        resource_ip_ranges = self._get_value(inquiry.resource, self.resource_ip_range_attr)
        return any(self._ip_in_range(subject_ip, r) for r in resource_ip_ranges)

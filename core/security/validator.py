import re
from ipaddress import ip_address, IPv6Address

def validate_ip(ip: str) -> bool:
    try:
        return isinstance(ip_address(ip), (IPv4Address, IPv6Address))
    except ValueError:
        return False

def sanitize_string(input_str: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\-_. ]', '', input_str)[:256]

def validate_packet(packet: dict) -> bool:
    return all([
        validate_ip(packet.get('src_ip')),
        validate_ip(packet.get('dst_ip')),
        0 < packet.get('src_port', 0) < 65535,
        len(packet.get('payload', '')) <= 1500
    ])
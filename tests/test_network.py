import pytest
from core.security.validator import validate_packet

@pytest.fixture
def sample_packet():
    return {
        'src_ip': '192.168.1.1',
        'dst_ip': '10.0.0.1',
        'src_port': 443,
        'payload': 'Normal traffic'
    }

def test_packet_validation(sample_packet):
    assert validate_packet(sample_packet) is True

def test_invalid_packet():
    assert validate_packet({'src_ip': 'invalid'}) is False

def test_ipv6_packet():
    packet = {
        'src_ip': '2001:db8::1',
        'dst_ip': '2001:db8::2',
        'src_port': 80,
        'payload': 'IPv6 traffic'
    }
    assert validate_packet(packet) is True
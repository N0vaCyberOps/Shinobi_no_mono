import pytest
from core.security.validator import validate_ip, validate_packet

def test_validate_ip():
    assert validate_ip("192.168.1.1") is True
    assert validate_ip("2001:db8::1") is True
    assert validate_ip("invalid") is False

def test_validate_packet():
    valid_packet = {
        'src_ip': '192.168.1.1',
        'dst_ip': '10.0.0.1',
        'src_port': 443,
        'payload': 'Normal traffic'
    }
    assert validate_packet(valid_packet) is True

    invalid_packet = {
        'src_ip': 'invalid',
        'dst_ip': '10.0.0.1',
        'src_port': 443,
        'payload': 'Normal traffic'
    }
    assert validate_packet(invalid_packet) is False
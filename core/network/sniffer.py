import asyncio
import redis
from scapy.plist import AsyncSniffer
from scapy.layers.inet6 import IPv6
from core.utils.config import load_config
from core.utils.logger import CyberLogger

config = load_config()
logger = CyberLogger(__name__)
redis_client = redis.Redis(host='redis', port=6379, db=0)

class PacketSniffer:
    def __init__(self):
        self.observers = []
        self.sniffer = None

    def register_observer(self, callback):
        self.observers.append(callback)

    async def start(self):
        self.sniffer = AsyncSniffer(
            prn=self._notify_observers,
            filter=config['bpf_filter'],
            store=False
        )
        self.sniffer.start()

    def _notify_observers(self, packet):
        if packet.haslayer(IPv6):
            src_ip = packet[IPv6].src
            dst_ip = packet[IPv6].dst
        else:
            src_ip = packet.src
            dst_ip = packet.dst

        packet_data = {
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'payload': str(packet.payload)
        }
        redis_client.xadd('packets_stream', packet_data)
import asyncio
import redis
from typing import List, Callable, Optional
from scapy.plist import AsyncSniffer
from scapy.layers.inet6 import IPv6
from core.utils.config import load_config
from core.utils.logger import CyberLogger

config = load_config()
logger = CyberLogger(__name__)

class PacketSniffer:
    def __init__(self):
        self.observers: List[Callable] = []
        self.sniffer: Optional[AsyncSniffer] = None
        self.redis_client = redis.Redis(
            host='redis',
            port=6379,
            db=0,
            socket_timeout=2,
            decode_responses=False
        )

    async def start(self) -> None:
        try:
            self.sniffer = AsyncSniffer(
                prn=self._notify_observers,
                filter=config.get('bpf_filter', 'tcp'),
                store=False
            )
            self.sniffer.start()
            logger.info("Sniffer started successfully")
        except Exception as e:
            logger.error(f"Sniffer initialization failed: {str(e)}")
            raise

    def _notify_observers(self, packet) -> None:
        try:
            if IPv6 in packet:
                src_ip = packet[IPv6].src
                dst_ip = packet[IPv6].dst
            else:
                src_ip = packet.src
                dst_ip = packet.dst

            self.redis_client.xadd(
                'packets_stream',
                {'src_ip': src_ip, 'dst_ip': dst_ip},
                maxlen=1000
            )
        except Exception as e:
            logger.error(f"Packet processing error: {str(e)}")
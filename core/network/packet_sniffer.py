"""
Asynchroniczny sniffer pakietów z dynamicznym filtrem BPF i wzorcem Observer.
"""

import asyncio
from scapy.plist import AsyncSniffer
from scapy.packet import Packet
from typing import List, Callable, Optional
from collections import defaultdict
from core.utils.logger import CyberLogger
from core.utils.config_manager import ConfigManager

class PacketSniffer:
    def __init__(self):
        self._bpf_filter = ConfigManager.get('network.bpf_filter', 'tcp or udp')
        self._observers = defaultdict(list)
        self._sniffer: Optional[AsyncSniffer] = None
        self._logger = CyberLogger(__name__)
        self._update_filter_lock = asyncio.Lock()

    def register_observer(self, event_type: str, callback: Callable[[Packet], None]) -> None:
        """Rejestracja obserwatora dla określonego typu zdarzenia."""
        self._observers[event_type].append(callback)

    async def update_bpf_filter(self, new_filter: str) -> None:
        """Dynamiczna aktualizacja filtra BPF."""
        async with self._update_filter_lock:
            await self.stop()
            self._bpf_filter = new_filter
            await self.start()
            self._logger.info(f"Zaktualizowano filtr BPF: {new_filter}")

    async def start(self) -> None:
        """Uruchomienie sniffera z aktualnym filtrem BPF."""
        self._sniffer = AsyncSniffer(
            filter=self._bpf_filter,
            prn=self._notify_observers,
            store=False
        )
        self._sniffer.start()
        self._logger.info(f"Sniffer uruchomiony z filtrem: {self._bpf_filter}")

    async def stop(self) -> None:
        """Bezpieczne zatrzymanie sniffera."""
        if self._sniffer:
            self._sniffer.stop()
            await asyncio.sleep(1)  # Czas na finalizację
            self._logger.info("Sniffer zatrzymany")

    def _notify_observers(self, packet: Packet) -> None:
        """Powiadomienie obserwatorów o nowym pakiecie."""
        for callback in self._observers.get(packet.type, []):
            asyncio.create_task(callback(packet))
"""
Asynchroniczny sniffer pakietów z buforowaniem i filtrami BPF.
Implementuje wzorzec Observer do dystrybucji zdarzeń.
"""

import asyncio
from scapy.plist import AsyncSniffer
from scapy.packet import Packet
from typing import List, Callable
from core.utils.logger import CyberLogger
from core.utils.config_manager import ConfigManager

class PacketSniffer:
    def __init__(self):
        self._observers: List[Callable[[Packet], None]] = []
        self._sniffer: AsyncSniffer = None
        self._config = ConfigManager.get_network_config()
        self._logger = CyberLogger(__name__)

    def add_observer(self, callback: Callable[[Packet], None]) -> None:
        """Rejestracja funkcji obsługi zdarzeń pakietów."""
        self._observers.append(callback)

    def _notify_observers(self, packet: Packet) -> None:
        """Powiadomienie wszystkich obserwatorów o nowym pakiecie."""
        for observer in self._observers:
            try:
                observer(packet)
            except Exception as e:
                self._logger.error(f"Błąd obserwatora: {e}")

    async def start(self) -> None:
        """Uruchomienie asynchronicznego nasłuchu z filtrami."""
        bpf_filter = self._config.get("bpf_filter", "tcp or udp")
        
        self._sniffer = AsyncSniffer(
            filter=bpf_filter,
            prn=self._notify_observers,
            store=False
        )
        self._sniffer.start()
        self._logger.info("Sniffer uruchomiony z filtrem: %s", bpf_filter)

    async def stop(self) -> None:
        """Bezpieczne zatrzymanie przechwytywania."""
        if self._sniffer:
            self._sniffer.stop()
            await asyncio.sleep(1)  # Czas na finalizację
            self._logger.info("Sniffer zatrzymany")

"""
Zaawansowany system logowania z buforowaniem i rotacją plików.
"""

import logging
from logging.handlers import RotatingFileHandler, MemoryHandler
from pathlib import Path
from datetime import datetime
from typing import Any
from core.utils.config_manager import ConfigManager

class CyberLogger:
    def __init__(self, name: str):
        self._config = ConfigManager.get('logging')
        self._logger = logging.getLogger(name)
        self._logger.setLevel(self._config.get('level', 'INFO'))
        
        if not self._logger.handlers:
            formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%SZ"
            )
            formatter.converter = self._utc_time
            
            # Handler plikowy z rotacją
            logs_dir = Path(self._config.get('dir', '/var/log/cyberwitness'))
            logs_dir.mkdir(exist_ok=True)
            
            file_handler = RotatingFileHandler(
                filename=logs_dir / "cyberwitness.log",
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            
            # Buforowanie w pamięci
            self._memory_handler = MemoryHandler(
                capacity=self._config.get('buffer_size', 1000),
                target=file_handler,
                flushLevel=logging.ERROR
            )
            self._logger.addHandler(self._memory_handler)

    @staticmethod
    def _utc_time(*args: Any) -> tuple:
        return datetime.utcnow().timetuple()

    async def periodic_flush(self) -> None:
        """Asynchroniczne czyszczenie bufora co 60s."""
        while True:
            await asyncio.sleep(60)
            self._memory_handler.flush()
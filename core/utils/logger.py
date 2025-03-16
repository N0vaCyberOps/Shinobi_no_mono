"""
Zaawansowany system logowania z obsługą rotacji plików i formatowaniem.
Zgodny z RFC 5424 (Syslog).
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
from typing import Any
from core.utils.config_manager import ConfigManager

class CyberLogger:
    def __init__(self, name: str):
        self._config = ConfigManager.get_logging_config()
        self._logger = logging.getLogger(name)
        self._logger.setLevel(self._config["level"])
        
        if not self._logger.handlers:
            formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%SZ"
            )
            formatter.converter = self._utc_time
            
            # Handler konsolowy
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            
            # Handler plikowy z rotacją
            logs_dir = Path(self._config["dir"])
            logs_dir.mkdir(exist_ok=True)
            
            file = RotatingFileHandler(
                filename=logs_dir / "cyberwitness.log",
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding="utf-8"
            )
            file.setFormatter(formatter)
            
            self._logger.addHandler(console)
            self._logger.addHandler(file)

    @staticmethod
    def _utc_time(*args: Any) -> tuple:
        return datetime.utcnow().timetuple()

    def info(self, message: str, *args: Any) -> None:
        self._logger.info(message, *args)

    def warning(self, message: str, *args: Any) -> None:
        self._logger.warning(message, *args)

    def error(self, message: str, *args: Any) -> None:
        self._logger.error(message, *args)

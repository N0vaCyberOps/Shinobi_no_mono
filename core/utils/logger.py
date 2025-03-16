import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
from core.utils.config import load_config

config = load_config()

class CyberLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(config.get('log_level', 'INFO'))
        
        if not self.logger.handlers:
            formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%SZ"
            )
            logs_dir = Path(config.get('log_dir', '/var/log/shinobi'))
            logs_dir.mkdir(exist_ok=True)
            
            file_handler = RotatingFileHandler(
                filename=logs_dir / "shinobi.log",
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
                encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str, *args):
        self.logger.info(message, *args)

    def warning(self, message: str, *args):
        self.logger.warning(message, *args)

    def error(self, message: str, *args):
        self.logger.error(message, *args)
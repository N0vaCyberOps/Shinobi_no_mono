import requests
from urllib.parse import urlparse
from core.utils.logger import CyberLogger

logger = CyberLogger(__name__)

class SlackNotifier:
    def __init__(self, webhook_url: str, timeout: int = 5):
        if not self._is_valid_url(webhook_url):
            raise ValueError("Invalid Slack webhook URL format")
        self.webhook_url = webhook_url
        self.timeout = timeout

    def _is_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def send_alert(self, message: str) -> bool:
        try:
            response = requests.post(
                self.webhook_url,
                json={"text": message},
                timeout=self.timeout
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Slack API Error: {str(e)}")
            return False
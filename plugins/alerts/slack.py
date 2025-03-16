import requests
from core.utils.logger import CyberLogger

logger = CyberLogger(__name__)

class SlackNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_alert(self, message):
        try:
            response = requests.post(
                self.webhook_url,
                json={"text": message},
                timeout=5
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
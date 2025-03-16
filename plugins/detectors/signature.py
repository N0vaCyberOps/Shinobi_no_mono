from core.utils.logger import CyberLogger

logger = CyberLogger(__name__)

class SignatureDetector:
    def __init__(self, signatures):
        self.signatures = signatures

    def detect(self, packet):
        for signature in self.signatures:
            if signature in str(packet.payload):
                logger.warning(f"Signature detected: {signature}")
                return True
        return False
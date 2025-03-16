import redis
from core.security.validator import validate_packet
from plugins.detectors.anomaly import AnomalyDetector
from core.utils.logger import CyberLogger

redis_client = redis.Redis(host='redis', port=6379, db=0)
anomaly_detector = AnomalyDetector()
logger = CyberLogger(__name__)

async def process_packets():
    last_id = '0'
    while True:
        packets = redis_client.xread({'packets_stream': last_id}, block=0, count=10)
        for packet in packets:
            packet_id, packet_data = packet
            if validate_packet(packet_data):
                analyze_packet(packet_data)
            last_id = packet_id

def analyze_packet(packet):
    features = extract_features(packet)
    if anomaly_detector.predict(features) > 0.8:
        logger.warning(f"Anomaly detected in packet: {packet}")
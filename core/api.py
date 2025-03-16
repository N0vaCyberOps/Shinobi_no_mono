from fastapi import FastAPI
from core.network.sniffer import PacketSniffer
from core.utils.logger import CyberLogger
from core.utils.config import load_config
import asyncio

app = FastAPI(title="Shinobi API")
logger = CyberLogger(__name__)
config = load_config()

@app.on_event("startup")
async def startup_event():
    sniffer = PacketSniffer()
    await sniffer.start()
    logger.info("Sniffer initialized with filter: %s", config['bpf_filter'])

@app.get("/status")
async def get_status():
    return {"status": "active", "version": "1.3.2"}

@app.get("/packets/{packet_id}")
async def analyze_packet(packet_id: int):
    return {"analysis": "safe", "confidence": 0.95}
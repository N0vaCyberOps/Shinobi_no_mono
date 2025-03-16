from fastapi import FastAPI

app = FastAPI(title="CyberWitness API")

@app.get("/status")
async def status():
    return {"status": "OK", "message": "CyberWitness API is running"}
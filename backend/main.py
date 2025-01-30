from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tts_service import TextToSpeechService
import os

app = FastAPI()
tts_service = TextToSpeechService()

class TTSRequest(BaseModel):
    text: str
    lang: str = "cmn"
    voice: str = "af_sky"
    speed: float = 1.0

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    try:
        output_path = "output.wav"
        tts_service.convert(
            text=request.text,
            output_path=output_path,
            lang=request.lang,
            voice=request.voice,
            speed=request.speed
        )
        return {"status": "success", "file": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
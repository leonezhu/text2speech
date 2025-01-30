import time
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tts_service import TextToSpeechService

app = FastAPI()

# 修改 CORS 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，或者使用具体的域名列表
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 明确指定允许的方法
    allow_headers=["*"],
)

tts_services = {}

# 配置音频文件存储路径
AUDIO_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'audio')
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

# 挂载静态文件服务
app.mount("/api/audio", StaticFiles(directory=AUDIO_FOLDER), name="audio")

class TTSRequest(BaseModel):
    text: str
    lang: str = "cmn"
    voice: str = "af_sky"
    speed: float = 1.0
    model: str = "kokoro"

@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    try:
        # 验证参数
        if not request.text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        if not 0.5 <= request.speed <= 2.0:
            raise HTTPException(status_code=400, detail="Speed must be between 0.5 and 2.0")
        
        # 获取或创建 TTS 服务实例
        if request.model not in tts_services:
            tts_services[request.model] = TextToSpeechService(model_name=request.model)
        
        service = tts_services[request.model]
        
        # 生成文件名和路径
        filename = f"{request.text[:20].replace(' ', '_')}-{time.strftime('%Y%m%d%H%M%S')}.wav"
        filepath = os.path.join(AUDIO_FOLDER, filename)
        
        # 转换文本为语音
        service.convert(
            text=request.text,
            output_path=filepath,
            lang=request.lang,
            voice=request.voice,
            speed=request.speed
        )
        
        # 返回结果
        return {
            "status": "success",
            "audio_url": f"/api/audio/{filename}",
            "lang": request.lang,
            "voice": request.voice,
            "speed": request.speed,
            "model": request.model
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
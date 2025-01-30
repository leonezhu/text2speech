from pathlib import Path
from kokoro_onnx import Kokoro, config
from ...base import BaseTTSModel

class KokoroTTSv019Model(BaseTTSModel):
    def __init__(self):
        self.kokoro = None
        self._model_dir = Path(__file__).parent / 'models'
        
    def initialize(self) -> None:
        model_file = self._model_dir / 'kokoro-v0_19.onnx'
        voices_file = self._model_dir / 'voices.json'
        
        if not model_file.exists() or not voices_file.exists():
            raise FileNotFoundError(
                'Required files not found. Please download:\n'
                'wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx\n'
                'wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.json'
            )
        
        config.MAX_PHONEME_LENGTH = 128
        self.kokoro = Kokoro(str(model_file), str(voices_file))
    
    def generate_speech(self, text: str, lang: str = "cmn", voice: str = "af_sky", speed: float = 1.0):
        if not self.kokoro:
            self.initialize()
            
        return self.kokoro.create(
            text=text,
            voice=voice,
            speed=speed,
            lang=lang
        )
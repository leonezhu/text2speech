import sys
import soundfile as sf
from pathlib import Path
from kokoro_onnx import Kokoro, config

class TextToSpeechService:
    def __init__(self):
        """
        初始化Kokoro TTS服务
        """
        model_file = 'kokoro-v0_19.onnx'
        voices_file = 'voices.json'
        
        # 检查必需文件
        if not Path(model_file).exists() or not Path(voices_file).exists():
            raise FileNotFoundError(
                'kokoro-v0_19.onnx and voices.json must be in the current directory. '
                'Please download them with:\n'
                'wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx\n'
                'wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.json'
            )
        
        # 设置最大音素长度
        config.MAX_PHONEME_LENGTH = 128
        self.kokoro = Kokoro(model_file, voices_file)
        
    def convert(self, text, output_path, lang='cmn', voice='af_sky', speed=1.0):
        """
        将文本转换为语音并保存为音频文件
        
        Args:
            text (str): 要转换的文本
            output_path (str): 输出文件路径
            lang (str): 语言代码，默认中文
            voice (str): 声音类型
            speed (float): 语速，范围0.5-2.0
        """
        try:
            # 生成音频
            samples, sample_rate = self.kokoro.create(
                text=text,
                voice=voice,
                speed=speed,
                lang=lang
            )
            
            # 保存音频文件
            sf.write(output_path, samples, sample_rate)
        except Exception as e:
            print(f"Error in convert: {str(e)}", file=sys.stderr)
            raise 
import sys
import soundfile as sf
from tts.factory import TTSFactory  # 修改导入路径，移除 backend 前缀

class TextToSpeechService:
    def __init__(self, model_name: str = "kokoro"):
        """
        初始化TTS服务
        
        Args:
            model_name: TTS模型名称，默认使用kokoro
        """
        self.model = TTSFactory.get_model(model_name)
        self.model.initialize()
        
    def convert(self, text: str, output_path: str, lang: str = 'cmn', voice: str = 'af_sky', speed: float = 1.0):
        """
        将文本转换为语音并保存为音频文件
        
        Args:
            text: 要转换的文本
            output_path: 输出文件路径
            lang: 语言代码，默认中文
            voice: 声音类型
            speed: 语速，范围0.5-2.0
        """
        try:
            # 生成音频
            samples, sample_rate = self.model.generate_speech(
                text=text,
                lang=lang,
                voice=voice,
                speed=speed
            )
            
            # 保存音频文件
            sf.write(output_path, samples, sample_rate)
        except Exception as e:
            print(f"Error in convert: {str(e)}", file=sys.stderr)
            raise
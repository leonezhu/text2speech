from abc import ABC, abstractmethod
from typing import Tuple, Any

class BaseTTSModel(ABC):
    """TTS 模型的基础接口类"""
    
    @abstractmethod
    def initialize(self) -> None:
        """初始化模型"""
        pass
    
    @abstractmethod
    def generate_speech(
        self,
        text: str,
        lang: str = "cmn",
        voice: str = "default",
        speed: float = 1.0
    ) -> Tuple[Any, int]:
        """
        生成语音
        
        Args:
            text: 要转换的文本
            lang: 语言代码
            voice: 声音类型
            speed: 语速
            
        Returns:
            Tuple[samples, sample_rate]
        """
        pass
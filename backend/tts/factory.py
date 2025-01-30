from typing import Dict, Type
from .base import BaseTTSModel
from .kokoro import KokoroTTSModel  # 修改为新的导入路径

class TTSFactory:
    _models: Dict[str, Type[BaseTTSModel]] = {
        "kokoro": KokoroTTSModel
    }
    
    @classmethod
    def get_model(cls, model_name: str) -> BaseTTSModel:
        """
        获取指定的 TTS 模型实例
        
        Args:
            model_name: 模型名称
            
        Returns:
            TTS 模型实例
        """
        if model_name not in cls._models:
            raise ValueError(f"Unknown TTS model: {model_name}")
            
        model_class = cls._models[model_name]
        return model_class()
    
    @classmethod
    def register_model(cls, name: str, model_class: Type[BaseTTSModel]) -> None:
        """
        注册新的 TTS 模型
        
        Args:
            name: 模型名称
            model_class: 模型类
        """
        cls._models[name] = model_class
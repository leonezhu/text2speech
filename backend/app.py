import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from tts_service import TextToSpeechService
import os

app = Flask(__name__)
CORS(app)

# 配置音频文件存储路径
AUDIO_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'audio')
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

tts_service = TextToSpeechService()

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text')
        lang = data.get('lang', 'cmn')  # 默认中文
        voice = data.get('voice', 'af_sky')  # 默认声音
        speed = float(data.get('speed', 1.0))  # 默认语速
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # 验证speed范围
        if not 0.5 <= speed <= 2.0:
            return jsonify({'error': 'Speed must be between 0.5 and 2.0'}), 400
        
        # 生成音频文件名
        # filename 用text的前 20个字符再加时间，空格用下划线替换
        filename = f"{text[:20].replace(' ', '_')}-{time.strftime('%Y%m%d%H%M%S')}.wav"
        # filename = f"{hash(text)}.wav"
        filepath = os.path.join(AUDIO_FOLDER, filename)
        
        # 转换文本为语音
        tts_service.convert(
            text=text,
            output_path=filepath,
            lang=lang,
            voice=voice,
            speed=speed
        )
        
        # 返回音频文件的URL
        audio_url = f'/api/audio/{filename}'
        return jsonify({
            'audio_url': audio_url,
            'lang': lang,
            'voice': voice,
            'speed': speed
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio/<filename>')
def get_audio(filename):
    try:
        return send_file(
            os.path.join(AUDIO_FOLDER, filename),
            mimetype='audio/wav'  # 改为wav格式
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True) 
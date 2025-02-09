0. 创建虚拟环境python3 -m venv venv
> 无证书按照依赖pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org fastapi uvicorn > pydantic kokoro-onnx soundfile
1. 安装依赖
> pip install kokoro-onnx soundfile 
2. 下载 voices.json 和 kokoro-v0_19.onnx 文件，放在backend目录下
3. 在 /backend 中，使用以下命令，进入虚拟环境
> source venv/bin/activate 
4. 然后运行命令，启动服务
> python app.py

5. 在 /frontend 中启动前端服务
> npm run serve



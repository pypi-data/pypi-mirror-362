# deeplin
Deep Learning Toolbox for LinXueyuan

## Hexin Server

详见 [docs/README_FASTAPI.md](docs/README_FASTAPI.md)

启动 FastAPI 服务器以代理 OpenAI API 并使用 hexin_engine 后端处理请求。

```sh
python -m deeplin.inference_engine.hexin_server
python -m deeplin.inference_engine.hexin_server --host 0.0.0.0 --port 8777
```

服务器使用固定的 API key 进行认证：

```python
from openai import OpenAI
OPENAI_API_KEY="sk-deeplin-fastapi-proxy-key-12345"
OPENAI_BASE_URL="http://localhost:8777/v1"
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)
messages = [
    {"role": "user", "content": "Hello!"},
]
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)
print(response.choices[0].message.content)
```

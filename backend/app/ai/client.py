import base64
import requests
from typing import Generator, Optional
from app.core.config import settings


def get_ai_response(prompt: str, image_data: Optional[bytes] = None, model: Optional[str] = None) -> str:
    model = model or settings.MISTRAL_MODEL
    api_url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {settings.MISTRAL_API_KEY}", "Content-Type": "application/json"}

    if image_data:
        encoded = base64.b64encode(image_data).decode()
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded}"}]}]
    else:
        messages = [{"role": "user", "content": prompt}]

    payload = {"model": model, "messages": messages, "max_tokens": 1000, "temperature": 0.7}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erreur IA: {str(e)}"


def get_ai_stream(prompt: str, image_data: Optional[bytes] = None, model: Optional[str] = None) -> Generator[str, None, None]:
    model = model or settings.MISTRAL_MODEL
    api_url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {settings.MISTRAL_API_KEY}", "Content-Type": "application/json"}

    if image_data:
        encoded = base64.b64encode(image_data).decode()
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded}"}]}]
    else:
        messages = [{"role": "user", "content": prompt}]

    payload = {"model": model, "messages": messages, "max_tokens": 1000, "temperature": 0.7, "stream": True}

    try:
        response = requests.post(api_url, headers=headers, json=payload, stream=True, timeout=30)
        response.raise_for_status()
        for chunk in response.iter_lines():
            if chunk:
                decoded = chunk.decode()
                if decoded.startswith("data:"):
                    import json
                    data = json.loads(decoded[5:])
                    if "choices" in data:
                        yield data["choices"][0]["delta"].get("content", "")
    except Exception as e:
        yield f"Erreur IA: {str(e)}"

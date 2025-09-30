from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import requests

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ImageRequest(BaseModel):
    image: str  # base64 string

@app.post("/analyze")
async def analyze(request: ImageRequest):
    try:
        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4.1-mini",
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": "What food is in this picture? Provide nutritional info."},
                            {"type": "input_image", "image_base64": request.image},
                        ],
                    }
                ],
            },
        )
        data = response.json()
        return {"output": data}
    except Exception as e:
        return {"error": str(e)}

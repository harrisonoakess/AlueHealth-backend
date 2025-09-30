from fastapi import FastAPI
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ Missing OPENAI_API_KEY. Set it in .env (local) or Railway Variables.")


@app.get("/")
def root():
    return {"message": "✅ Backend is running!"}

@app.get("/test-openai")
def test_openai():
    """
    Simple test call to OpenAI to confirm connection works.
    """
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
                    {"role": "user", "content": [{"type": "input_text", "text": "Say hello, backend is connected!"}]}
                ],
            },
        )
        data = response.json()
        return {"openai_response": data}
    except Exception as e:
        return {"error": str(e)}

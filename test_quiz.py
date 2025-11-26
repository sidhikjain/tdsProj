import httpx
import os

# Load secret from .env or set directly
SECRET = os.getenv("APP_SECRET", "your_secret_here")
EMAIL = "24f1002708@ds.study.iitm.ac.in"  # change to your email
QUIZ_URL = "https://tds-llm-analysis.s-anand.net/submit"

payload = {
    "email": EMAIL,
    "secret": SECRET,
    "url": QUIZ_URL
}

async def test_quiz_endpoint():
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://localhost:8000/endpoint", json=payload)
        print("Status:", resp.status_code)
        try:
            print("Response:", resp.json())
        except Exception:
            print("Raw response:", resp.text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_quiz_endpoint())

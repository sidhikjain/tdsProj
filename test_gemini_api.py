#!/usr/bin/env python3
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Gemini API endpoint (official Google endpoint)
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

print("🔍 Testing Gemini API Key...")
print(f"   Model: {MODEL}")
print(f"   API Key: {API_KEY[:20]}..." if API_KEY else "   API Key: NOT SET")
print()

if not API_KEY:
    print("❌ GEMINI_API_KEY not found in .env file!")
    exit(1)

# Test with a simple prompt
payload = {
    "contents": [{
        "parts": [{
            "text": "Say 'Hello' if you can read this."
        }]
    }]
}

try:
    print("📡 Sending test request to Gemini API...")
    resp = httpx.post(
        f"{API_URL}?key={API_KEY}",
        json=payload,
        timeout=30.0
    )
    
    print(f"Status Code: {resp.status_code}")
    print()
    
    if resp.status_code == 200:
        print("✅ API Key is VALID!")
        data = resp.json()
        
        # Extract the response text
        if "candidates" in data:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"Response: {text}")
        else:
            print("Full Response:", data)
    elif resp.status_code == 400:
        print("❌ API Key is INVALID or request malformed")
        print("Response:", resp.json())
    elif resp.status_code == 403:
        print("❌ API Key lacks permissions or quota exceeded")
        print("Response:", resp.json())
    elif resp.status_code == 404:
        print("❌ Model not found. Check GEMINI_MODEL in .env")
        print("Response:", resp.json())
    else:
        print(f"❌ Unexpected status: {resp.status_code}")
        print("Response:", resp.text)
        
except httpx.TimeoutException:
    print("❌ Request timed out - check your internet connection")
except Exception as e:
    print(f"❌ Error: {e}")

# test_env.py
from dotenv import load_dotenv
import os, json, requests, sys

load_dotenv()  # loads .env in current dir

print("GEMINI_API_URL repr:", repr(os.getenv("GEMINI_API_URL")))
print("GEMINI_API_KEY SET?:", bool(os.getenv("GEMINI_API_KEY")))

url = os.getenv("GEMINI_API_URL")
key = os.getenv("GEMINI_API_KEY")
if not url or not key:
    print("Missing GEMINI_API_URL or GEMINI_API_KEY. Fix .env format (no quotes, no spaces).")
    sys.exit(1)

payload = {
  "contents": [{"parts":[{"text":"Test: reply with short acknowledgement"}]}]
}
try:
    r = requests.post(url + "?key=" + key, json=payload, timeout=20)
    print("HTTP status:", r.status_code)
    try:
        j = r.json()
        print("Response keys:", list(j.keys())[:10])
        print("Response preview:", json.dumps(j, indent=2)[:1000])
    except Exception:
        print("Response text preview:", r.text[:1000])
except Exception as e:
    print("Request failed:", type(e).__name__, str(e)[:500])

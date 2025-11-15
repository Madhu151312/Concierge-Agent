# inside agent/llm.py -> GeminiLLM class
import json, requests
from config import GEMINI_API_URL, GEMINI_API_KEY

class GeminiLLM:
    def __init__(self, model='gemini-2.0-flash'):
        self.model = model
        self.api = GEMINI_API_URL
        self.key = GEMINI_API_KEY

    def _extract_text_from_response(self, data):
        if not isinstance(data, dict):
            return None
        # new-style response: candidates -> content -> parts -> text
        try:
            cands = data.get("candidates")
            if cands and isinstance(cands, list):
                first = cands[0]
                content = first.get("content", {})
                parts = content.get("parts") or []
                if parts:
                    return "".join([p.get("text","") for p in parts])
        except Exception:
            pass
        # fallback checks
        if "output_text" in data:
            return data.get("output_text")
        if "text" in data:
            return data.get("text")
        return None

    def generate(self, prompt):
        # If no API configured, keep mock behavior
        if not self.api or not self.key:
            print("[GeminiLLM] Using MOCK response")
            return self._mock_response(prompt)

        # Minimal payload shape that the REST endpoint expects
        payload = {
            "contents": [{"parts":[{"text": prompt}]}]
        }

        headers = {"Content-Type": "application/json"}
        # Build URL but DO NOT print the key
        url = self.api if "?" in self.api else f"{self.api}?key={self.key}"
        print("[GeminiLLM] Calling real Gemini API:", self.api)  # safe: don't show key

        try:
            r = requests.post(url, json=payload, headers=headers, timeout=30)
            # If the API returns an HTTP error (400/401/404/...), we handle it gracefully
            r.raise_for_status()
            data = r.json()
            text = self._extract_text_from_response(data)
            if text is None:
                # If structure unexpected, return a helpful debug string (without key)
                return "[GeminiLLM] Unexpected response shape from Gemini; see logs for raw output.\n" + json.dumps(data)
            return text
        except requests.HTTPError as he:
            # Give user-friendly info; include status and server message
            try:
                err = r.json()
            except Exception:
                err = r.text
            print("[GeminiLLM] HTTP error:", r.status_code, err)
            return f"[GeminiLLM] HTTP error {r.status_code}: {err}"
        except Exception as e:
            print("[GeminiLLM] Error calling Gemini:", type(e).__name__, e)
            return f"[GeminiLLM] Error calling Gemini: {type(e).__name__} {e}"

    def _mock_response(self, prompt):
        import json
        if 'create_event' in prompt or 'schedule' in prompt.lower():
            return json.dumps({
                "tool":"calendar",
                "action":"create_event",
                "args":{
                    "title":"Sync with Alice",
                    "start":"2025-11-21T10:00:00+05:30",
                    "end":"2025-11-21T10:30:00+05:30",
                    "attendees":["alice@example.com"]
                }
            })
        if 'morning briefing' in prompt.lower() or 'briefing' in prompt.lower():
            return "Today's briefing:\n- 2 meetings\n- 3 important unread emails\n- Top priority: reply to Acme."
        return "I'm ready to help. (Mock response)"

import json, requests
from src.supabase_adapter import SupabaseLogAdapter
class GManSpeechEngine:
    def __init__(self):
        self.gateway_url = "https://workers.dev"
        self.db = SupabaseLogAdapter()
        print("[G-MAN MASTER CORE ONLINE]: Unified framework coupled with database adapters.")
    def process_vocal_input(self, text_prompt):
        payload = {"messages": [{"role": "system", "content": "Speak like G-Man."}, {"role": "user", "content": text_prompt}]}
        try:
            res = requests.post(self.gateway_url, json=payload)
            data = res.json()
            ai_response = data["result"]["response"] if "result" in data else data["choices"]["message"]["content"]
            print(f"\n[G-MAN OUTPUT]: {ai_response}\n")
            self.db.log_avatar_conversation(text_prompt, ai_response, 0)
            return ai_response
        except Exception as e:
            print(f"[FAILOVER]: {e}")
            return "Consequences... Mr. Freeman..."

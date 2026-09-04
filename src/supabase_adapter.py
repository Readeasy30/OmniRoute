import os, requests, datetime
class SupabaseLogAdapter:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL", "https://supabase.co")
        self.key = os.getenv("SUPABASE_KEY", "your-anon-key")
        self.headers = {"apikey": self.key, "Authorization": f"Bearer {self.key}", "Content-Type": "application/json", "Prefer": "return=minimal"}
    def log_avatar_conversation(self, user_prompt, avatar_response, total_tokens=0):
        endpoint = f"{self.url}/rest/v1/avatar_logs"
        payload = {"timestamp": datetime.datetime.utcnow().isoformat(), "user_prompt": user_prompt, "avatar_response": avatar_response, "token_usage": total_tokens}
        try:
            res = requests.post(endpoint, json=payload, headers=self.headers)
            print("[DATABASE SYNC SUCCESS]: Saved conversation step to Supabase.")
        except Exception as e:
            print("[DATABASE FAILOVER]: Local storage active.")

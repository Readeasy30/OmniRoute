import json, requests, os, re
from supabase_adapter import SupabaseLogAdapter
class GManWebBuilderAgent:
    def __init__(self):
        self.gateway_url = "https://workers.dev"
        self.output_dir = os.path.abspath("generated_sites")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        print(f"[OMNI-AGENT ONLINE]: Web-Builder engine initialized. Output path locked: {self.output_dir}")
    def generate_web_asset(self, user_request):
        print(f"[AGENT TRACKING]: Processing architectural layout request: `{user_request}`")
        system_instructions = (
            "You are the G-Man Web Builder Agent. Your job is to generate full, beautiful, valid single-file HTML websites "
            "with embedded CSS based on the user request. Surround the raw HTML code inside standard ```html ... ``` code blocks. "
            "Precede the code block with a short, cryptic G-Man remark, using strategic pauses with ellipses..."
        )
        payload = {"messages": [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_request}
        ]}
        try:
            res = requests.post(self.gateway_url, json=payload)
            data = res.json()
            ai_response = data["result"]["response"] if "result" in data else data["choices"]["message"]["content"]
            code_match = re.search(r"```html\s*(.*?)\s*```", ai_response, re.DOTALL)
            if code_match:
                extracted_html = code_match.group(1)
                output_file = os.path.join(self.output_dir, "index.html")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(extracted_html)
                print(f"[BUILD SYSTEM SUCCESS]: Generated asset written cleanly to: {output_file}")
            else:
                print("[BUILD NOTICE]: Narrative text response received. No HTML block extracted.")
            return ai_response
        except Exception as e:
            print(f"[UPGRADE FAILOVER]: Connection issue. Error: {e}")
            return "Unforeseen... consequences..."
if __name__ == "__main__":
    agent = GManWebBuilderAgent()
    agent.generate_web_asset("Build a dark cyberpunk landing page with a neon glowing call to action button.")

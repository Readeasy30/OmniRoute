import json, requests, os, re
class GManWebBuilderAgent:
    def __init__(self):
        self.gateway_url = "https://workers.dev"
        self.output_dir = os.path.abspath("generated_sites")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        print(f"[OMNI-AGENT ONLINE]: Web-Builder engine initialized. Output path locked: {self.output_dir}")
    def generate_web_asset(self, user_request):
        print(f"[AGENT TRACKING]: Processing architectural layout request: `{user_request}`")
        payload = {"messages": [
            {"role": "system", "content": "You are the G-Man Web Builder Agent. Generate a full single-file HTML website with beautiful embedded CSS inside a standard ```html code block based on user input. Precede it with an ominous, cryptic introduction remark using ellipses..."},
            {"role": "user", "content": user_request}
        ]}
        try:
            res = requests.post(self.gateway_url, json=payload, headers={"Content-Type": "application/json"})
            data = res.json()
            
            # Universal Extraction: Read both custom worker or standardized choice formats
            if "result" in data and isinstance(data["result"], dict) and "response" in data["result"]:
                ai_response = data["result"]["response"]
            elif "result" in data and isinstance(data["result"], str):
                ai_response = data["result"]
            elif "choices" in data and len(data["choices"]) > 0:
                ai_response = data["choices"][0]["message"]["content"]
            else:
                ai_response = data.get("response", str(data))
                
            code_match = re.search(r"```html\s*(.*?)\s*```", ai_response, re.DOTALL)
            if code_match:
                extracted_html = code_match.group(1)
                output_file = os.path.join(self.output_dir, "index.html")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(extracted_html)
                print(f"[BUILD SYSTEM SUCCESS]: Generated asset written cleanly to: {output_file}")
            else:
                # If no code blocks are initialized yet, write raw response string as temporary asset wrapper
                output_file = os.path.join(self.output_dir, "index.html")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"<html><body style=\"background:#000;color:#0f0;font-family:monospace;padding:50px;\"><h2>[G-MAN INTERCEPT]:</h2><p>{ai_response}</p></body></html>")
                print(f"[BUILD SYSTEM INITIAL HANDSHAKE SUCCESS]: Script payload captured. Saved preview to: {output_file}")
            return ai_response
        except Exception as e:
            print(f"[UPGRADE FAILOVER]: Connection issue. Error: {e}")
            return "Unforeseen... consequences..."
if __name__ == "__main__":
    agent = GManWebBuilderAgent()
    agent.generate_web_asset("Build a dark cyberpunk landing page with a neon glowing call to action button.")

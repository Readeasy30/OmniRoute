import os, re, requests
from openai import OpenAI

class GManWebBuilderAgent:
    def __init__(self):
        # Establish connection using the official SDK pointed directly at your serverless edge gateway
        self.client = OpenAI(
            base_url="https://workers.dev",
            api_key="auto"
        )
        self.output_dir = os.path.abspath("generated_sites")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        print(f"[OMNI-AGENT PRODUCTION ONLINE]: Mapped via verified OpenAI SDK pipeline.")

    def generate_web_asset(self, user_request):
        print(f"[AGENT TRACKING]: Processing architectural layout request: `{user_request}`")
        
        try:
            # Query your worker architecture using official completion schemas
            completion = self.client.chat.completions.create(
                model="qwen-3.8-27b-edge",
                messages=[
                    {"role": "system", "content": "You are the G-Man Web Builder Agent. Generate a full single-file HTML website with beautiful embedded CSS inside a standard ```html ... ``` code block based on user input. Precede it with an ominous, cryptic introduction remark using ellipses..."},
                    {"role": "user", "content": user_request}
                ]
            )
            
            ai_response = completion.choices[0].message.content
            
            # Automated Extraction Loop: Pull the clean code out of the markdown blocks
            code_match = re.search(r"```html\s*(.*?)\s*```", ai_response, re.DOTALL)
            if code_match:
                extracted_html = code_match.group(1)
                output_file = os.path.join(self.output_dir, "index.html")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(extracted_html)
                print(f"\n[BUILD SYSTEM SUCCESS]: Generated asset written cleanly to: {output_file}\n")
            else:
                output_file = os.path.join(self.output_dir, "index.html")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"<html><body style=\"background:#000;color:#0f0;font-family:monospace;padding:50px;\"><h2>[G-MAN INTERCEPT]:</h2><p>{ai_response}</p></body></html>")
                print(f"\n[BUILD SYSTEM INITIAL HANDSHAKE SUCCESS]: Script preview saved to: {output_file}\n")
                
            return ai_response
            
        except Exception as e:
            print(f"[UPGRADE FAILOVER]: Connection path blocked. Error: {e}")
            return "Unforeseen... consequences..."

if __name__ == "__main__":
    agent = GManWebBuilderAgent()
    agent.generate_web_asset("Build a dark cyberpunk landing page with a neon glowing call to action button.")

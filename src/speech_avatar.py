import json, requests, os, re

class GManMultiPageAgent:
    def __init__(self):
        # HARD DATA TRACK FIXED: Explicit endpoint mapping path for direct JSON extraction
        self.gateway_url = "https://omniroute-edge-gateway.wholelychit.workers.dev"
        self.output_dir = os.path.abspath("generated_sites")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        print(f"[OMNI-AGENT V3 ONLINE]: Autonomous Multi-Page Architect deployed. Path locked: {self.output_dir}")

    def build_complete_website(self, user_request):
        print(f"[AGENT TRACKING]: Architecting multi-page site structure for: `{user_request}`")
        
        system_instructions = (
            "You are the G-Man Multi-Page Web Builder Agent. Your job is to output the code for THREE distinct pages: "
            "index.html, about.html, and contact.html based on the user request. They must share a matching professional CSS theme "
            "and link to each other via a navigation bar. Wrap each file inside standard markdown blocks labeled with its filename, "
            "like this:\n---index.html---\n```html\n...\n```\n---about.html---\n```html\n...\n```\n---contact.html---\n```html\n...\n```"
        )

        payload = {"messages": [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_request}
        ]}
        
        try:
            res = requests.post(self.gateway_url, json=payload, headers={"Content-Type": "application/json"})
            data = res.json()
            
            if "result" in data and isinstance(data["result"], dict) and "response" in data["result"]:
                ai_response = data["result"]["response"]
            elif "choices" in data and len(data["choices"]) > 0:
                ai_response = data["choices"][0]["message"]["content"]
            else:
                ai_response = str(data)

            # Automated Page Multi-Scraper Matrix
            files_to_extract = ["index.html", "about.html", "contact.html"]
            found_any = False

            for filename in files_to_extract:
                pattern = rf"---{filename}---\s*```html\s*(.*?)\s*```"
                match = re.search(pattern, ai_response, re.DOTALL)
                
                if match:
                    extracted_code = match.group(1)
                    target_file = os.path.join(self.output_dir, filename)
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(extracted_code)
                    print(f"[BUILD SUCCESS]: Autonomous layout written cleanly to: {target_file}")
                    found_any = True

            if not found_any:
                fallback_match = re.search(r"```html\s*(.*?)\s*```", ai_response, re.DOTALL)
                extracted_code = fallback_match.group(1) if fallback_match else ai_response
                target_file = os.path.join(self.output_dir, "index.html")
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(extracted_code)
                print(f"[BUILD STANDALONE SUCCESS]: Structured single-file asset written cleanly to: {target_file}")

            return ai_response
        except Exception as e:
            print(f"[UPGRADE FAILOVER]: Trace circuit hit a lock. Error: {e}")
            return "Unforeseen... complications..."

if __name__ == "__main__":
    agent = GManMultiPageAgent()
    agent.generate_web_asset = agent.build_complete_website
    agent.build_complete_website("Create an enterprise portfolio website for a modern web design agency with smooth aesthetics.")

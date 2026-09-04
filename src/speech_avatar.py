import urllib.request, urllib.error, json, os, re

class GManMultiPageAgent:
    def __init__(self):
        self.gateway_url = "https://workers.dev"
        self.output_dir = os.path.abspath("generated_sites")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        print(f"[OMNI-AGENT V3.2 ONLINE]: Core urllib network engine loaded. Path: {self.output_dir}")

    def build_complete_website(self, user_request):
        print(f"[AGENT TRACKING]: Architecting site layout structures for: `{user_request}`")
        
        system_instructions = (
            "You are the G-Man Multi-Page Web Builder Agent. You must generate full code for THREE separate files: "
            "index.html, about.html, and contact.html matching the user theme. You MUST output each file inside its own "
            "explicit code block structure, preceded by its exact file marker on a line by itself, like this:\n"
            "FILE:index.html\n```html\n(code here)\n```\n"
            "FILE:about.html\n```html\n(code here)\n```\n"
            "FILE:contact.html\n```html\n(code here)\n```"
        )

        payload = {"messages": [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_request}
        ]}
        
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.gateway_url, 
            data=data_bytes, 
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                raw_data = response.read().decode("utf-8")
                data = json.loads(raw_data)
            
            ai_response = data["result"]["response"] if "result" in data else data["choices"][0]["message"]["content"]

            files_to_extract = ["index.html", "about.html", "contact.html"]
            found_any = False

            for filename in files_to_extract:
                pattern = rf"FILE:{filename}\s*```html\s*(.*?)\s*```"
                match = re.search(pattern, ai_response, re.DOTALL)
                
                if match:
                    extracted_code = match.group(1)
                    target_file = os.path.join(self.output_dir, filename)
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(extracted_code)
                    print(f"[FILE GENERATION SUCCESS]: Written to disk -> {target_file}")
                    found_any = True

            if not found_any:
                fallback_match = re.search(r"```html\s*(.*?)\s*```", ai_response, re.DOTALL)
                extracted_code = fallback_match.group(1) if fallback_match else ai_response
                target_file = os.path.join(self.output_dir, "index.html")
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(extracted_code)
                print(f"[FALLBACK SINGLE BLOCK SUCCESS]: Asset saved -> {target_file}")

            return ai_response
        except Exception as e:
            print(f"[UPGRADE FAILOVER]: Trace circuit hit a lock. Error: {e}")
            return "Unforeseen... complications..."

if __name__ == "__main__":
    agent = GManMultiPageAgent()
    agent.build_complete_website("Create an enterprise portfolio website for a modern web design agency with smooth aesthetics.")

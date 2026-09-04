import requests
url = "https://omniroute-edge-gateway.wholelychit.workers.dev"
payload = {"messages": [{"role": "user", "content": "Respond with the phrase CENTRAL GATEWAY WORKING if you can read this."}]}
print("Sending request to your cloud architecture...")
try:
    response = requests.post(url, json=payload)
    data = response.json()
    if "result" in data and "response" in data["result"]:
        print("\n=== SYSTEM ONLINE ===\n", data["result"]["response"])
    else:
        print("\n=== RAW INSTANCE OUTPUT ===\n", data)
except Exception as e:
    print(f"\nConnection Error: {e}")

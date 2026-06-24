import os
import requests
import json

token = os.environ["CODOLIO_TOKEN"]

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(
    "https://api.codolio.com/user",
    headers=headers,
    timeout=30
)

with open("assets/codolio-response.json", "w", encoding="utf-8") as f:
    json.dump(response.json(), f, indent=2)

print("Status:", response.status_code)
print("Response saved.")
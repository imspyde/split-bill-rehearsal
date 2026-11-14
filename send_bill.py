import hashlib
import hmac
import json
import os
import time
import urllib.request

url = os.environ["HOOK_URL"]
secret = os.environ["HOOK_SECRET"]

body = json.dumps({"amount": 3000, "tip_percent": 15, "people": 5}).encode()
timestamp = str(int(time.time()))
signature = hmac.new(secret.encode(), timestamp.encode() + b"." + body, hashlib.sha256).hexdigest()

request = urllib.request.Request(
    url,
    data=body,
    headers={
        "Content-Type": "application/json",
        "X-Dagflows-Signature": f"t={timestamp},v1={signature}",
    },
)
with urllib.request.urlopen(request) as response:
    print(response.status, response.read().decode())

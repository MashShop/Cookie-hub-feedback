import os, time, hashlib
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1362275778682818690/iE04DIwklUddKS9IpiFhUnBObT1uuW0tw4uebATvY-uKAS0gbqj2ruoFywuDcG9fmNyr"
COOLDOWN = 600  # 10 minutes

# Track IPs anonymously using hashed version
ip_timers = {}

@app.route('/send-feedback', methods=['POST'])
def send_feedback():
    ip = request.remote_addr
    hashed_ip = hashlib.sha256(ip.encode()).hexdigest()
    now = time.time()

    data = request.get_json() or {}
    msg = data.get('message', '').strip()

    if not msg:
        return jsonify(success=False, error="Feedback cannot be empty."), 400

    last_time = ip_timers.get(hashed_ip, 0)
    if now - last_time < COOLDOWN:
        wait = int(COOLDOWN - (now - last_time))
        return jsonify(success=False, error=f"Please wait {wait} seconds before submitting again."), 429

    # Send to Discord webhook
    payload = { "content": f"**New Feedback**\n{msg}" }
    resp = requests.post(WEBHOOK_URL, json=payload)
    if not resp.ok:
        return jsonify(success=False, error="Failed to send feedback."), 500

    # Update timestamp
    ip_timers[hashed_ip] = now

    return jsonify(success=True, message="Feedback sent successfully."), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

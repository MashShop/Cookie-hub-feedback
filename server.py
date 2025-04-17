import os
import time
import hashlib
import logging
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder='static')

# enable debug logging to console
logging.basicConfig(level=logging.INFO)

# Your secret webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1362275778682818690/iE04DIwklUddKS9IpiFhUnBObT1uuW0tw4uebATvY-uKAS0gbqj2ruoFywuDcG9fmNyr"

COOLDOWN = 600  # seconds

# track last‑sent timestamps by hashed IP
ip_timers = {}

@app.route('/')
def index():
    # serve feedback.html
    return send_from_directory('static', 'feedback.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/send-feedback', methods=['POST'])
def send_feedback():
    ip_raw = request.remote_addr or 'unknown'
    hashed_ip = hashlib.sha256(ip_raw.encode()).hexdigest()
    now = time.time()

    data = request.get_json(silent=True)
    if not data:
        return jsonify(success=False, error="Invalid JSON"), 400

    msg = data.get('message', '').strip()
    if not msg:
        return jsonify(success=False, error="Feedback cannot be empty."), 400

    last_time = ip_timers.get(hashed_ip, 0)
    if now - last_time < COOLDOWN:
        wait = int(COOLDOWN - (now - last_time))
        return jsonify(success=False, error=f"Please wait {wait}s before sending again."), 429

    try:
        # send to Discord
        payload = { "content": f"**New Feedback**\n{msg}" }
        resp = requests.post(WEBHOOK_URL, json=payload)
        logging.info(f"Discord webhook response: {resp.status_code} {resp.text!r}")
        resp.raise_for_status()

    except requests.RequestException as e:
        logging.error(f"Failed to send webhook: {e}")
        return jsonify(success=False, error="Failed to send feedback."), 500

    # on success, update cooldown
    ip_timers[hashed_ip] = now
    return jsonify(success=True, message="Feedback sent successfully."), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)

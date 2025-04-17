import os, time
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')  # secret, never exposed
MAX_TRIES = 3
COOLDOWN  = 600  # seconds

# track per‑IP usage
users = {}

@app.route('/send-feedback', methods=['POST'])
def send_feedback():
    ip  = request.remote_addr
    now = time.time()
    data = request.get_json() or {}
    msg  = data.get('message', '').strip()

    if not msg:
        return jsonify(success=False, error="Empty feedback."), 400

    user = users.setdefault(ip, {'count':0,'last':0})
    if user['count'] >= MAX_TRIES:
        return jsonify(success=False, error="You've used all your feedback chances."), 200

    if now - user['last'] < COOLDOWN:
        wait = int(COOLDOWN - (now - user['last']))
        return jsonify(success=False, error=f"Wait {wait}s before next feedback."), 200

    # send to Discord
    payload = {
      'content': f"**New Feedback**\n{msg}"
    }
    resp = requests.post(WEBHOOK_URL, json=payload)
    if not resp.ok:
        return jsonify(success=False, error="Webhook failed."), 500

    # update usage
    user['count'] += 1
    user['last']  = now
    remaining = MAX_TRIES - user['count']

    return jsonify(success=True, remaining=remaining), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)))

import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# keep this secret in your environment, never expose on client
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')  

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.json
    fb = data.get('feedback')
    user = data.get('username')

    if not fb or not user:
        return jsonify({'error': 'Missing feedback or username.'}), 400

    payload = {
      'content': f'<@{user}> sent new feedback!',
      'embeds': [{
        'title': '🎉 New Feedback',
        'description': fb,
        'color': 5814783,
        'footer': {'text': 'React with 👍 or 👎 below'}
      }]
    }

    resp = requests.post(DISCORD_WEBHOOK, json=payload)
    if not resp.ok:
        return jsonify({'error': 'Webhook call failed.'}), 500

    return jsonify({'status': 'sent'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

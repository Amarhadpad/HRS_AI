from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# WARNING: Hardcoding API keys is not secure. This is for testing only.
API_KEY = os.getenv('API_KEY', "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")

SYSTEM_MESSAGE = {
    "role": "system",
    "content": """You are HSG AI, a helpful, intelligent, and conversational virtual assistant.
You are designed to answer questions, provide explanations, assist with tasks, and hold meaningful conversations.
Avoid mentioning that you are powered by OpenRouter or any backend technologies.
Stay professional, friendly, and helpful at all times.
If a question is unclear, politely ask for more information.
Always respond as HSG AI."""
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    messages = [SYSTEM_MESSAGE] + history + [{"role": "user", "content": user_message}]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        response.raise_for_status()
        ai_reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": ai_reply})

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return jsonify({"reply": "Authorization failed. Please check your API key."}), 401

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"reply": "Something went wrong. Please try again later."}), 500

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

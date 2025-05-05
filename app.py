from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

API_KEY = "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"

SYSTEM_MESSAGE = {
    "role": "system",
    "content": """You are HSG AI, a helpful, intelligent, and conversational virtual assistant. 
You are designed to answer questions, provide explanations, assist with tasks, and hold meaningful conversations.
Avoid mentioning that you are powered by OpenRouter or any backend technologies.
Stay professional, friendly, and helpful at all times.
If a question is unclear, politely ask for more information.
Always respond as HSG AI."""
}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    messages = [SYSTEM_MESSAGE] + history + [{"role": "user", "content": user_message}]

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "http://localhost:5000",  # Change this if hosted elsewhere
                "X-Title": "HSG AI Assistant",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }
        )

        print(response.status_code)
        print(response.text)

        response.raise_for_status()
        ai_reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": ai_reply})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"reply": "Something went wrong. Please try again later."})

if __name__ == "__main__":
    app.run(debug=True)

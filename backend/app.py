import sys
import os
from flask import Flask, request, jsonify, render_template

# Add the project root directory to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from models.chat_logic import generate_chat_response

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def college_home():
    print("🔵 Serving college homepage")
    return render_template("college_home.html")

@app.route("/chat-ui")
def chat_ui():
    print("🟢 Serving chatbot UI")
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        print("📨 Received POST to /chat:", data)

        user_query = data.get("message", "")
        if not user_query:
            return jsonify({"status": "error", "message": "No message provided"}), 400

        bot_reply = generate_chat_response(user_query)
        print("🤖 Bot reply:", bot_reply)

        return jsonify({"status": "success", "response": bot_reply})
    
    except Exception as e:
        print("❌ Exception in /chat:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable if available
    print(f"🚀 Flask server running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)

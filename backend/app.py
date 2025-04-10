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
    return render_template("college_home.html")

@app.route("/chat-ui")
def chat_ui():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_query = data.get("message", "")
    if not user_query:
        return jsonify({"status": "error", "message": "No message provided"}), 400

    try:
        bot_reply = generate_chat_response(user_query)
        return jsonify({"status": "success", "response": bot_reply})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(host="0.0.0.0", port=port)

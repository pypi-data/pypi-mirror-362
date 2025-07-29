# aider_rag/api_server.py

from flask import Flask, request, jsonify
from src.aider_follama.rag_runner import run_combined_rag_pipeline

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing prompt"}), 400

    result = run_combined_rag_pipeline(data["prompt"])
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=11435, debug=True)

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PREPROCESS_URL = "http://preprocess-service:5002/preprocess"
SENTIMENT_URL = "http://sentiment-service:5001/predict"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    # 1️⃣ Preprocess
    preprocessed = requests.post(PREPROCESS_URL, json={"text": text}).json()

    # 2️⃣ Run Sentiment Analysis
    result = requests.post(SENTIMENT_URL, json=preprocessed).json()

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
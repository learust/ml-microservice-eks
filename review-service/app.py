from flask import Flask, request, jsonify
from flask_cors import CORS
from sentiment import polarity_scores, stars

app = Flask(__name__)
CORS(app)

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.post("/api/review")
def review():
    data = request.get_json(silent=True) or {}
    text = (data.get("review") or "").strip()
    if not text:
        return jsonify({"error": "Provide 'review' text"}), 400

    pol = polarity_scores(text)
    rating = stars(text)
    return jsonify({"review": text, "polarity": pol, "stars": rating}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
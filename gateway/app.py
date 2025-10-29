from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CAR_VALUE_URL = "http://car-value-service:5001/api/trade"
REVIEW_URL = "http://review-service:5002/api/review"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    # 1️⃣ Get car value (using text as placeholder for now)
    car_value_response = requests.post(CAR_VALUE_URL, json={"year": 2020, "mileage": 50000}).json()

    # 2️⃣ Run Sentiment Analysis
    result = requests.post(REVIEW_URL, json={"review": text}).json()

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
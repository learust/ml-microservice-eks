from flask import Flask, request, jsonify
from price import trade

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.post("/api/trade")
def trade_endpoint():
    data = request.get_json(silent=True) or {}
    try:
        year = int(data.get("year"))
        mileage = float(data.get("mileage"))
    except (TypeError, ValueError):
        return jsonify({"error": "Provide numeric 'year' and 'mileage'"}), 400

    value = trade(year, mileage)
    return jsonify({"year": year, "mileage": mileage, "value": value}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
from flask import Flask, request, jsonify
import uuid, datetime

app = Flask(__name__)
transactions = []

@app.route("/billing/pay", methods=["POST"])
def pay():
    data = request.get_json() or {}

    required = ["amount", "card_number"]
    missing = [x for x in required if x not in data]
    if missing:
        return jsonify({"error": f"Missing: {', '.join(missing)}"}), 400

    txn = {
        "id": str(uuid.uuid4()),
        "amount": float(data["amount"]),
        "card_last4": data["card_number"][-4:],
        "status": "success",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    transactions.append(txn)

    return jsonify({"message": "Payment successful", "transaction": txn})

@app.route("/billing/history", methods=["GET"])
def history():
    return jsonify(transactions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6200)

from flask import Flask, request, jsonify
import math

app = Flask(__name__)

@app.route("/finance/calculate", methods=["POST"])
def calculate_financing():
    data = request.get_json() or {}

    required = ["price", "down_payment", "loan_years", "interest_rate"]
    missing = [x for x in required if x not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    price = float(data["price"])
    down = float(data["down_payment"])
    rate = float(data["interest_rate"]) / 100
    years = int(data["loan_years"])

    loan_amount = max(price - down, 0)
    months = years * 12
    monthly_rate = rate / 12

    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**months) / (
        (1 + monthly_rate)**months - 1
    ) if monthly_rate > 0 else loan_amount / months

    return jsonify({
        "loan_amount": round(loan_amount, 2),
        "monthly_payment": round(monthly_payment, 2),
        "months": months
    })

@app.route("/finance/approve", methods=["POST"])
def approve_credit():
    data = request.get_json() or {}
    if "credit_score" not in data:
        return jsonify({"error": "credit_score required"}), 400

    approved = data["credit_score"] >= 600
    return jsonify({
        "approved": approved,
        "message": "Approved ✅" if approved else "Denied ❌"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6100)

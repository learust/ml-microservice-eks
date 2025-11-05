from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Existing services
CAR_VALUE_URL = "http://car-value-service:5001/api/trade"
REVIEW_URL = "http://review-service:5002/api/review"

# New services
FINANCE_URL = "http://finance-service:6100"
BILLING_URL = "http://billing-service:6200"

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "api-gateway"}), 200

# ------------------ Combined car analysis ------------------
@app.route("/api/car-analysis", methods=["POST"])
def car_analysis():
    """Combined car value estimation and review sentiment analysis"""
    try:
        data = request.get_json(silent=True) or {}
        
        required_fields = ["year", "mileage", "review"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}",
                "required": required_fields
            }), 400
        
        results, errors = {}, []

        # Car Value Service
        try:
            car_data = {"year": data["year"], "mileage": data["mileage"]}
            logger.info(f"Requesting car value for: {car_data}")
            car_response = requests.post(CAR_VALUE_URL, json=car_data, timeout=5)

            if car_response.status_code == 200:
                results["car_value"] = car_response.json()
            else:
                errors.append(f"Car value service returned {car_response.status_code}")
        except requests.exceptions.Timeout:
            errors.append("Car value service timeout")
        except Exception as e:
            errors.append(f"Car value error: {str(e)}")

        # Sentiment Service
        try:
            review_data = {"review": data["review"]}
            logger.info(f"Requesting sentiment analysis")
            review_response = requests.post(REVIEW_URL, json=review_data, timeout=5)

            if review_response.status_code == 200:
                results["sentiment"] = review_response.json()
            else:
                errors.append(f"Review service returned {review_response.status_code}")
        except requests.exceptions.Timeout:
            errors.append("Review service timeout")
        except Exception as e:
            errors.append(f"Review error: {str(e)}")

        if not results:
            return jsonify({"error": "All services failed", "details": errors}), 503

        response = {"results": results}
        if errors: response["warnings"] = errors
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# ------------------ Car Value Only ------------------
@app.route("/api/car-value", methods=["POST"])
def car_value():
    try:
        data = request.get_json(silent=True) or {}
        if not data.get("year") or not data.get("mileage"):
            return jsonify({"error": "Provide 'year' and 'mileage'"}), 400

        response = requests.post(CAR_VALUE_URL, json=data, timeout=5)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "Car value timeout"}), 504
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Car value service unavailable"}), 503

# ------------------ Review Only ------------------
@app.route("/api/review-sentiment", methods=["POST"])
def review_sentiment():
    try:
        data = request.get_json(silent=True) or {}
        if not data.get("review"):
            return jsonify({"error": "Provide 'review' text"}), 400

        response = requests.post(REVIEW_URL, json=data, timeout=5)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "Review service timeout"}), 504
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Review service unavailable"}), 503

# ------------------ Finance Routes ------------------
@app.route("/api/finance/calculate", methods=["POST"])
def finance_calculate():
    try:
        data = request.get_json(silent=True) or {}
        response = requests.post(f"{FINANCE_URL}/finance/calculate", json=data, timeout=5)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "Finance service timeout"}), 504
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Finance service unavailable"}), 503

@app.route("/api/finance/approve", methods=["POST"])
def finance_approve():
    try:
        data = request.get_json(silent=True) or {}
        response = requests.post(f"{FINANCE_URL}/finance/approve", json=data, timeout=5)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "Finance service timeout"}), 504
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Finance service unavailable"}), 503

# ------------------ Billing Routes ------------------
@app.route("/api/billing/pay", methods=["POST"])
def billing_pay():
    try:
        data = request.get_json(silent=True) or {}
        response = requests.post(f"{BILLING_URL}/billing/pay", json=data, timeout=5)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "Billing service timeout"}), 504
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Billing service unavailable"}), 503

@app.route("/api/billing/history", methods=["GET"])
def billing_history():
    try:
        response = requests.get(f"{BILLING_URL}/billing/history", timeout=5)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "Billing history timeout"}), 504
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": "Billing service unavailable"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

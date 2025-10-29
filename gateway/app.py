from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CAR_VALUE_URL = "http://car-value-service:5001/api/trade"
REVIEW_URL = "http://review-service:5002/api/review"

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "api-gateway"}), 200

@app.route("/api/car-analysis", methods=["POST"])
def car_analysis():
    """Combined car value estimation and review sentiment analysis"""
    try:
        data = request.get_json(silent=True) or {}
        
        # Validate required fields
        required_fields = ["year", "mileage", "review"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}",
                "required": required_fields
            }), 400
        
        results = {}
        errors = []
        
        # 1️⃣ Get car value estimation
        try:
            car_data = {"year": data["year"], "mileage": data["mileage"]}
            logger.info(f"Requesting car value for: {car_data}")
            
            car_response = requests.post(CAR_VALUE_URL, json=car_data, timeout=5)
            
            if car_response.status_code == 200:
                results["car_value"] = car_response.json()
                logger.info("Car value estimation successful")
            else:
                error_msg = f"Car value service returned status {car_response.status_code}"
                logger.error(error_msg)
                errors.append(error_msg)
                
        except requests.exceptions.Timeout:
            error_msg = "Car value service timeout"
            logger.error(error_msg)
            errors.append(error_msg)
        except Exception as e:
            error_msg = f"Car value service error: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
        
        # 2️⃣ Get review sentiment analysis
        try:
            review_data = {"review": data["review"]}
            logger.info(f"Requesting sentiment analysis for review")
            
            review_response = requests.post(REVIEW_URL, json=review_data, timeout=5)
            
            if review_response.status_code == 200:
                results["sentiment"] = review_response.json()
                logger.info("Sentiment analysis successful")
            else:
                error_msg = f"Review service returned status {review_response.status_code}"
                logger.error(error_msg)
                errors.append(error_msg)
                
        except requests.exceptions.Timeout:
            error_msg = "Review service timeout"
            logger.error(error_msg)
            errors.append(error_msg)
        except Exception as e:
            error_msg = f"Review service error: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
        
        # Return combined results
        if not results:
            return jsonify({
                "error": "All services failed",
                "details": errors
            }), 503
        
        response = {"results": results}
        if errors:
            response["warnings"] = errors
            
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/car-value", methods=["POST"])
def car_value():
    """Get car trade-in value estimation only"""
    try:
        data = request.get_json(silent=True) or {}
        
        if not data.get("year") or not data.get("mileage"):
            return jsonify({"error": "Provide 'year' and 'mileage'"}), 400
        
        response = requests.post(CAR_VALUE_URL, json=data, timeout=5)
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.Timeout:
        return jsonify({"error": "Service timeout"}), 504
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": "Service unavailable"}), 503

@app.route("/api/review-sentiment", methods=["POST"])
def review_sentiment():
    """Get review sentiment analysis only"""
    try:
        data = request.get_json(silent=True) or {}
        
        if not data.get("review"):
            return jsonify({"error": "Provide 'review' text"}), 400
        
        response = requests.post(REVIEW_URL, json=data, timeout=5)
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.Timeout:
        return jsonify({"error": "Service timeout"}), 504
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"error": "Service unavailable"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
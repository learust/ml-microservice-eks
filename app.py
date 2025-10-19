from flask import Flask, request, jsonify
from sentiment import tokenizer, model  # imports directly from your script
from scipy.special import softmax
import torch
from sentiment import polarity_scores

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get text from user request
    data = request.get_json()
    example = data.get("text", "")
    
    # Use imported tokenizer and model directly
    polarity_scores(data)

    return jsonify(polarity_scores)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

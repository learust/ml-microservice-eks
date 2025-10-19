  from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import torch

Model = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(Model)
model = AutoModelForSequenceClassification.from_pretrained(Model)

# Simple text example for eval:
example = "I hate this restaurant, there was nothing good about the food and the service quality was bad"

# Roberta model 
encoded_text = tokenizer(example, return_tensors="pt")
output = model(**encoded_text) 
scores = output[0][0].detach().numpy()
scores = softmax(scores)
print(scores)
scores_dict = {
        'roberta_neg' : scores [0],
        'roberta_neu' : scores [1],
        'roberta_pos' : scores [2]
    }
print(scores_dict)

def polarity_scores(example):
    encoded_text = tokenizer(example, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores_dict = {
        'roberta_neg' : scores [0],
        'roberta_neu' : scores [1],
        'roberta_pos' : scores [2]
    }
    return scores_dict

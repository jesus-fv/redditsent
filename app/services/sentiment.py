from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

device = -1

classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)

async def sentiment_analysis(text):
    
    if len(text) < 5 or text == "[deleted]" or text == "[removed]":
        return {"label": "unknown", "score": None}
    
    res = classifier(text)[0]
    label = res['label']
    confidence = res['score']
    
    if label == 'positive':
        sentiment_score = confidence
    elif label == 'negative':
        sentiment_score = -confidence
    else:
        sentiment_score = 0.0

    return {
        "label": label,
        "score": round(sentiment_score, 4)
    }
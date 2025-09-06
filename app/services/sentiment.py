from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

device = 0 if torch.cuda.is_available() else -1
if device == 0:
    model.cuda()

classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)

def sentiment_analysis(text):

    res = classifier(text)[0]
    
    if len(text) < 5 or text == "[deleted]" or text == "[removed]":
        sent = "unknown"

    res['score'] = round(res['score'], 2)
    
    return res
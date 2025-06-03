from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

model_name = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

device = 0 if torch.cuda.is_available() else -1
if device == 0:
    model.cuda()

classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)

def sentiment_analysis(text):

    res = classifier(text)[0]
    
    sent = res["label"]
    
    if len(text) < 5 or text == "[deleted]" or text == "[removed]":
        sent = "Unknown"
    
    return sent

from transformers import pipeline

emotion_pipe = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def analyze_emotions(text: str, threshold: float = 0.4):
    results = emotion_pipe(text)[0]  # [0] porque pipeline devuelve una lista de listas
    # Filtrar emociones por score
    filtered = [res for res in results if res["score"] >= threshold]
    return filtered

print(analyze_emotions("I love programming!"))
print(analyze_emotions("I hate bugs!"))
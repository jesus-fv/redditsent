import re

def text_cleaner(text: str) -> str:
    # Eliminar saltos de línea, tabulaciones y espacios múltiples
    text = text.replace("\\n", " ").replace("\n", " ").replace("\t", " ")
    text = text.replace('\\"', '"').replace("\\'", "'")
    text = re.sub(r'\s+', ' ', text)
    
    # Eliminar líneas que parezcan parte de una tabla
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[-| ]+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\|{2,}\s*$', '', text, flags=re.MULTILINE)
    
    text = re.sub(r'\|+', ' ', text)
    text = re.sub(r'-{3,}', ' ', text)

    # Eliminar markdown y símbolos
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[\]', '', text)
    text = re.sub(r'\{.*?\}', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'`', '', text)
    
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text
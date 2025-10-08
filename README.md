# Explorador de Opiniones en Reddit

## Descripción

Esta aplicación analiza publicaciones en Reddit para determinar la opinión en **tiempo real** sobre un temma en concreto.

## Instalación 

### Requisitos previos  

Antes de comenzar, asegúrate de tener instalado:  
- [Python 3.10+](https://www.python.org/downloads/)  
- [pip](https://pip.pypa.io/en/stable/) 

### Pasos  
1. Clona este repositorio:  

```bash
git clone https://github.com/jesus-fv/redditsent.git
cd redditsent
```

2. Crea y activa un entorno virtual

```bash
python -m venv venv
source venv/bin/activate
```

3. Instala las dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

Para levantar la aplicación, **necesitarás tener dos terminales abiertas simultáneamente**, una para el backend y otra para el frontend.

Asegurate de estar en la raiz del proyecto.

### **Terminal 1: Iniciar el Backend (FastAPI)**

```bash
uvicorn app.main:app --reload
```

### **Terminal 2: Iniciar el Frontend (Streamlit)**

```bash
streamlit run frontend/app.py
```

Una vez en ejecución, abre el navegador en http://localhost:8501 o la URL indicada en consola.



# Explorador de Opiniones en Reddit

### Descripción

Este proyecto consiste en un sistema integral de análisis de sentimientos para Reddit. A partir de un criterio de búsqueda, la aplicación extrae las publicaciones más relevantes (recientes o populares) y clasifica sus comentarios según su polaridad: positiva, neutral o negativa. El objetivo es proporcionar una herramienta intuitiva para visualizar, en tiempo real, la percepción pública sobre cualquier tema.

#### La arquitectura está dividida en dos partes:

- Backend (API REST): Desarrollado sobre FastAPI, este componente orquesta la conexión con la API oficial de Reddit mediante el cliente PRAW. Su función principal es la extracción eficiente de publicaciones y comentarios, así como la ejecución del pipeline de análisis de sentimiento utilizando el modelo pre-entrenado cardiffnlp/twitter-roberta-base-sentiment-latest.

- Frontend (UI): Implementado en Streamlit, proporciona una interfaz gráfica interactiva que permite al usuario realizar consultas de búsqueda, visualizar métricas de datos y explorar detalladamente la clasificación de sentimientos inferida por el modelo.

#### El proyecto ha sido construido utilizando las siguientes tecnologías y librerías:

- Python 3.10+: Entorno de ejecución base.

- FastAPI: Framework moderno de alto rendimiento para la construcción de la API REST.

- Streamlit: Herramienta para el desarrollo ágil de la interfaz de usuario y visualización de datos.

- PRAW (Python Reddit API Wrapper): Librería para la integración y acceso a datos de Reddit mediante autenticación OAuth2.

- Hugging Face Transformers: Biblioteca para la implementación e inferencia del modelo de NLP (RoBERTa).

- Pydantic: Gestión de esquemas, serialización y validación rigurosa de datos.

- Uvicorn: Servidor ASGI ligero para el despliegue de la aplicación asíncrona.

- Docker & Docker Compose: Solución para la contenerización de servicios y orquestación del despliegue local.

## Instalación y Ejecución

El proyecto puede ejecutarse de dos formas: utilizando **Docker** (recomendado) o mediante una instalación manual con **Python**.

1. Clona el repositorio:

```bash
git clone https://github.com/jesus-fv/redditsent.git
cd redditsent
```

* Antes de comenzar, asegúrate de configurar tus variables de entorno:

## Opción 1 — Ejecutar con Docker


### Levanta los servicios:

```bash
docker compose up --build -d
```

### Esto iniciará:

| Servicio | URL | Descripción |
|--------------|--------------|--------------|
| Frontend (Streamlit) | http://localhost:8501 | Interfaz de usuario |
| Backend (FastAPI) | http://localhost:8000/docs | Documentación interactiva (Swagger) |

### Detener los servicios:

```bash
docker compose down
```

## Opción 2 — Instalación Manual (Python)

### Requisitos

- Python 3.10+

- pip

### Instalación

### Crea y activa un entorno virtual

```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Ejecución manual

Necesitarás dos terminales abiertas.

Asegúrate de estar en la raíz del proyecto.

### Terminal 1 — Backend (FastAPI)

```bash
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

### Acceso

Frontend: http://localhost:8501

Backend Docs: http://localhost:8000/docs
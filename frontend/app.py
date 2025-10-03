import streamlit as st
import requests
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

API_URL = "http://localhost:8000"


positive = Image.open("frontend/public/positive.png")
negative = Image.open("frontend/public/negative.png")
neutral = Image.open("frontend/public/neutral.png")
unknown = Image.open("frontend/public/unknown.png")

st.set_page_config(page_title="Reddit Sentiment Dashboard", layout="wide")

st.title("Análisis de Sentimientos en Reddit")


with st.form(key="search_form"):
    c1, c2 = st.columns([6,2])
    with c1:
        topic = st.text_input("Buscar tema", placeholder="Ej: Spain")
    with c2:
        order = st.selectbox("Orden", ["hot", "new", "top", "relevant"])
        
    st.markdown(" ")
    submit = st.form_submit_button("Buscar")
    

if not submit:
    #st.info("Introduce un tema y pulsa Buscar para ver los resultados.")
    st.stop()


with st.spinner("Buscando en Reddit..."):

    params = {"query": topic, "sort": order}
    resp = requests.get(f"{API_URL}/search/", params=params)

    if resp.status_code != 200:
        st.error(f"Error {resp.status_code}: {resp.text}")
        st.stop()
        
    data = resp.json()
    
st.write("")
st.write("")

top_subreddit = None
if data.get("subreddits"):
    top_subreddit = sorted(data["subreddits"], key=lambda s: s.get("total_comments",0), reverse=True)[0]["subreddit"]

col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

col1.metric("Publicaciones Analizadas", data['global']['total_posts'])
col2.metric("Comentarios Totales", data['global']['total_comments'])
col3.metric("Sentimiento dominante", data['global']['dominant'])
col4.metric("Top subreddit", top_subreddit)

st.markdown("---")
st.write("")

left_col, right_col = st.columns([2, 2])

with left_col:
    counts = data.get("global", {}).get("counts", {})
    df_counts = pd.DataFrame(list(counts.items()), columns=["sentiment", "count"])
    if not df_counts.empty:
        
        color_map = {
            "positive": "#8BC34A",
            "negative": "#F44336",
            "neutral": "#FFEB3B",
            "unknown": "lightgray"
        }
        
        fig = px.pie(df_counts, names="sentiment", values="count", hole=0.45, title="Distribución global de sentimientos", color="sentiment", color_discrete_map=color_map)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos.")

with right_col:
    
    sentiment_score = data['global']['mean_sentiment_score']

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Puntuacion Media de Sentimiento"},
        gauge = {
            'axis': {'range': [-1, 1]},
            'bar': {'color': "#424242"},
            'steps': [
                {'range': [-1, -0.3], 'color': "#F44336"},
                {'range': [-0.3, 0.3], 'color': "#FFEB3B"},
                {'range': [0.3, 1], 'color': "#8BC34A"},
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

        
st.markdown("---")

# ===== Posts list (full width) =====
st.subheader("Posts encontrados")
posts = []
for s in data.get("subreddits", []):
    for p in s.get("posts", []):
        posts.append({
            "id": p["id"],
            "title": p["title"],
            "subreddit": s["subreddit"],
            "karma": p.get("karma", p.get("score", None)),
            "num_comments": p.get("num_comments", None),
            "dominant": p.get("sentiments", {}).get("dominant")
        })
df_posts = pd.DataFrame(posts)
if not df_posts.empty:
    st.dataframe(df_posts.sort_values("karma", ascending=False).reset_index(drop=True), height=300)
else:
    st.info("No se encontraron posts.")

st.markdown("---")

# ===== Post detail: select and expand =====
st.subheader("Detalle de un post")
post_ids = df_posts["id"].tolist() if not df_posts.empty else []
selected_id = st.selectbox("Selecciona un post para ver detalle", options=post_ids) if post_ids else None

st.markdown("---")
st.caption("Dashboard creado con Streamlit • Backend: FastAPI • Repo: tu-repo-link")
    
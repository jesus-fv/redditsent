import streamlit as st
import os
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from urllib.parse import quote_plus

API_URL = os.getenv("API_URL", "http://api:8000")

st.set_page_config(page_title="Reddit Sentiment Dashboard", layout="wide")

DEFAULT_IMAGE = "https://placehold.co/800x450/eeeeee/ff4500?text=Reddit+Post"

#<========= FORMULARIO BÚSQUEDA =========>#

st.title("Reddit Sentiment Dashboard")

with st.form(key="search_form"):
    cols_form = st.columns([6,2])
    with cols_form[0]:
        topic = st.text_input("Buscar tema", placeholder="Ej: Spain")
    with cols_form[1]:
        order = st.selectbox("Orden", [ "hot", "relevant", "new", "top"])
        
    st.markdown("")
    submit = st.form_submit_button("Buscar")

if not submit:
    st.info("Introduce un tema y pulsa Buscar para ver los resultados.")
    st.stop()

with st.spinner("Buscando en Reddit..."):

    params = {"query": topic, "sort": order}
    resp = requests.get(f"{API_URL}/search/", params=params)

    if resp.status_code != 200:
        st.error(f"Error {resp.status_code}: {resp.text}")
        st.stop()
        
    data = resp.json()

#<========= END/FORMULARIO BÚSQUEDA =========>#

r_global = data.get('global', {})
subs = data.get("subreddits", {})
posts = data.get("posts", {})

COLOR_MAP = {
    "positive": "#8BC34A",
    "negative": "#F44336",
    "neutral": "#FFEB3B",
    "unknown": "lightgray"
}

def space(lines: int = 1):
    st.markdown("<br>" * lines, unsafe_allow_html=True)

def is_media_accessible(url):
    try:
        r = requests.head(url, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True, timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def get_posts(p, section):

    cols_posts = st.columns([2,3,2,2,2,2])
    
    title = p['title']
    max_len = 70
    display_title = title if len(title) <= max_len else title[:max_len] + "..."
    title_md = f"[{display_title}]({p['url']})"
    
    subreddit = f'[r/{p.get("subreddit")}](https://www.reddit.com/r/{quote_plus(p.get("subreddit"))})'

    media_url = p.get("media_url")

    if media_url and is_media_accessible(media_url):
        cols_posts[0].image(media_url, use_container_width=True, width=200)
    else:
        cols_posts[0].image(DEFAULT_IMAGE, use_container_width=True, width=200)

    cols_posts[1].write("📌 " + title_md, unsafe_allow_html=True)
    
    if section == "s":
        cols_posts[2].write(f'🧑‍💻 {p.get("author")}')
        
    else:
        cols_posts[2].write(subreddit, unsafe_allow_html=True)
    
    cols_posts[3].write(f'🔺 {p.get("karma")}')
    
    cols_posts[4].write(f'💬 {p.get("num_comments")}')
    
    dom_sent = p["sentiments"]["dominant"]
    icons = {
        "positive": "✅",
        "negative": "❌",
        "neutral": "😐"
    }
    dom = f"{icons.get(dom_sent, '❓')} {dom_sent}"
    cols_posts[5].write(f"**{dom.capitalize()}**")

#<========= DATOS GLOBAL =========>#

space(1)

top_subreddit = sorted(subs, key=lambda s: s.get("total_comments",0), reverse=True)[0]["subreddit"]

cols_kpi= st.columns([2, 2, 2, 3])

cols_kpi[0].metric("Publicaciones Analizadas", r_global.get('total_posts'))
cols_kpi[1].metric("Comentarios Totales", r_global.get('total_comments'))
cols_kpi[2].metric("Sentimiento dominante", r_global.get('dominant'))
cols_kpi[3].metric("Subreddit con mas posts", "r/" + top_subreddit)

st.divider()
space(1)

cols_global = st.columns([2, 2])

with cols_global[0]:
    counts = data.get("global", {}).get("counts", {})
    df_counts = pd.DataFrame(list(counts.items()), columns=["sentiment", "count"])
    if not df_counts.empty:
        
        fig = px.pie(df_counts, names="sentiment", values="count", hole=0.45, color="sentiment", color_discrete_map=COLOR_MAP)
        fig.update_layout(
            title="Distribución global de sentimientos",
            title_x=0.18
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos.")

with cols_global[1]:
    
    sentiment_score = r_global.get('mean_sentiment_score')

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = sentiment_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Puntuacion Media de Sentimiento"},
        gauge = {
            'axis': {'range': [-1, 1]},
            'bar': {'color': "#424242"},
            'steps': [
                {'range': [-1, -0.3], 'color': COLOR_MAP.get("negative")},
                {'range': [-0.3, 0.3], 'color': COLOR_MAP.get("neutral")},
                {'range': [0.3, 1], 'color': COLOR_MAP.get("positive")},
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)
    
#<========= END/DATOS GLOBAL =========>#
        
st.divider()

#<========= SUBREDDIT =========>#

st.subheader("Subreddits")
st.markdown("Los subreddits más activos en los posts analizados")

if not subs:
    st.info("No hay subreddits para mostrar.")
else:
    
    subs_sorted = sorted(subs, key=lambda s: s.get("total_comments", 0), reverse=True)

    for s in subs_sorted[:10]:
        name = s.get("subreddit") or "unknown"
        total_posts = s.get("total_posts", 0)
        total_comments = s.get("total_comments", 0)
        pct_pos = s.get("percentages", {}).get("positive", 0.0)
        pct_neg = s.get("percentages", {}).get("negative", 0.0)

        cols_subreddit = st.columns(5)
        
        with cols_subreddit[0]:
            st.markdown(f"**[r/{name}](https://www.reddit.com/r/{quote_plus(name)})**", unsafe_allow_html=True)                
                
        with cols_subreddit[1]:
            st.write(f"📌 {total_posts}")
            
        with cols_subreddit[2]:
            st.write(f"💬 {total_comments}")

        with cols_subreddit[3]:
            st.write(f"✅ {pct_pos:.1f}%")
            
        with cols_subreddit[4]:
            st.write(f"❌ {pct_neg:.1f}%")
        
        with st.expander("Ver posts"):
            for p in posts:
                if p.get("subreddit") == name:
                    get_posts(p, "s")
            
 
#<========= END/SUBREDDIT =========>#

#<========= POSTS =========>#

space(1)
st.divider()

st.subheader("Posts")
st.markdown("Los posts más activos")

space(1)
      
posts_sorted = sorted(posts, key=lambda p: p.get("num_comments", 0), reverse=True)

for p in posts_sorted[:10]:
    
    get_posts(p, "p")
        
    with st.expander("Ver detalle"):
        if "comments" not in p:
            detail = requests.get(f"{API_URL}/posts/{p['id']}").json()
        else:
            detail = p
        dfc = pd.DataFrame(list(detail["sentiments"]["counts"].items()), columns=["s","c"])
        fig = px.pie(dfc, names="s", values="c", hole=0.5, color="s", color_discrete_map=COLOR_MAP)
        st.plotly_chart(fig, use_container_width=True, key=f'pie_sub_{p.get("id")}')
        for c in detail.get("top_comments", [])[:5]:
            st.markdown(f"- **{c['sentiment'].upper()}** ({c.get('sentiment_score',0):.2f}) — {c['body'][:200]}")  

    comments = p.get("comments", [])

    comments_sorted = sorted(
        comments,
        key=lambda p: p.get("karma", 0),
        reverse=True
    )
    
    with st.expander("Ver cometarios"):
        if "comments" not in p:
            st.info("Sin comentarios para mostrar.")
        else:
            for c in comments_sorted[:5]:
                st.markdown(f"‧ {c.get('text')}")
                
    space(1)                
#<========= END/POSTS =========>#

space(1)
st.markdown("*Nota: Se toma una muestra de hasta 50 publicaciones, y para cada una se analizan un máximo de 15 comentarios, con el fin de no saturar el proceso. En el apartado de *posts*, los comentarios mostrados no coinciden con los analizados individualmente, ya que se presenta el total de comentarios por publicación, no solo los que fueron analizados.")
st.divider()
st.caption("Dashboard creado con Streamlit • Backend: FastAPI • Análisis de sentimientos: cardiffnlp/twitter-roberta-base-sentiment-latest")
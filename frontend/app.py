import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Reddit Sentiment Dashboard", layout="wide")

st.title("Análisis de Sentimientos en Reddit")


topic = st.text_input("Escribe un tema para buscar en Reddit:")
order = st.selectbox("Ordenar por:", ["hot", "new", "top", "relevant"], index=0)

if st.button("Buscar"):
    with st.spinner("Buscando en Reddit..."):

        params = {"query": topic, "sort": order}
        resp = requests.get(f"{API_URL}/search/", params=params)

        if resp.status_code == 200:
            data = resp.json()
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")
            st.stop()

    st.subheader("Resultados")
    st.json(data)
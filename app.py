import streamlit as st


cerita_konten = st.Page(
    "Cerita_Konten.py",
    title="Cerita Konten",
    icon="📖",
    default=True
)

pg = st.navigation([
    cerita_konten
])

pg.run()

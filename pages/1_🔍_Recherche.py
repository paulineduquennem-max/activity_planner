import streamlit as st

# --- MENU LATÉRAL PERSONNALISÉ ---
st.sidebar.markdown("# 🏙️ UrbanPulse")
st.sidebar.caption("Votre planificateur intelligent")
st.sidebar.write("---")

# Liens de navigation propres
st.sidebar.page_link("app.py", label="Accueil", icon="🏠")
st.sidebar.page_link("pages/1_🔍_Recherche.py", label="Recherche d'activités", icon="🔍")
st.sidebar.page_link("pages/2_📚_Catalogue.py", label="Catalogue des lieux", icon="📚")
st.sidebar.write("---")
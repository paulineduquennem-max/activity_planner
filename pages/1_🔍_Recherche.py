import streamlit as st
import datetime as dt

# --- MENU LATÉRAL PERSONNALISÉ ---
st.sidebar.markdown("# 🏙️ UrbanPulse")
st.sidebar.caption("Votre planificateur intelligent")
st.sidebar.write("---")

# Liens de navigation propres
st.sidebar.page_link("app.py", label="Accueil", icon="🏠")
st.sidebar.page_link("pages/1_🔍_Recherche.py", label="Recherche d'activités", icon="🔍")
st.sidebar.page_link("pages/2_📚_Catalogue.py", label="Catalogue des lieux", icon="📚")
st.sidebar.write("---")

# Structure de la page principale

c1, c2 = st.columns(2)

today = dt.date.today()
with c1 : 
    date_choisie = st.date_input("**Choisissez le jour d'activité**", min_value= today, max_value= today + dt.timedelta(days=5), format= "DD/MM/YYYY")

with c2 :
    creneau_choisi = st.selectbox("**Choisissez la période de la journée**", ["Matin ⛅", "Après-midi ☀️", "Soir 🌙"])
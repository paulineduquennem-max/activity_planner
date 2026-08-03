import streamlit as st
import datetime as dt
from services import GeocodingService, WeatherService

# --- MENU LATÉRAL PERSONNALISÉ ---
st.sidebar.markdown("# 🏙️ UrbanPulse")
st.sidebar.caption("Votre planificateur intelligent")
st.sidebar.write("---")

# Liens de navigation propres
st.sidebar.page_link("app.py", label="Accueil", icon="🏠")
st.sidebar.page_link("pages/1_🔍_Recherche.py", label="Recherche d'activités", icon="🔍")
st.sidebar.page_link("pages/2_📚_Catalogue.py", label="Catalogue des lieux", icon="📚")
st.sidebar.write("---")

# Appel des services
geo_service = GeocodingService()

# Injection CSS pour le style de la page

st.markdown(f""" 
    <style>
    /* Titres et textes de la page principale forcés en bleu marine */
                    .stMain h1, .stMain h2, .stMain h3, .stMain p, .stMain .stMarkdown {{
                        color: #0A192F !important;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    }}
                    
                    /* Amélioration de la taille de la typo pour la lecture */
                    .stMain p, .stMain .stMarkdown {{
                        font-size: 1.15rem !important;
                    }}

                    /* Style appliqué à la barre de recherche */
                    .stTextInput input {{
                        background-color: #0A192F !important; /* Fond bleu marine */
                        color: #F2F2F2 !important;            /* Texte blanc cassé */
                        font-size: 1.1rem !important;
                    }}
                    
                    /* Style appliqué à la date choisie dans le calendrier*/
                    .stDateInput input {{
                        color: #F2F2F2 !important;            /* Texte blanc cassé */
                        background-color: #0A192F !important; /* Fond bleu marine */
                    }}

                    /* Style appliqué au texte dans la barre moment de la journée*/
                    [data-testid="stSelectbox"] div, 
                    [data-testid="stSelectbox"] span {{
                        color: #F2F2F2 !important;
                    }}
                    
                    /* 🛠️ SÉCURISATION DE LA SIDEBAR : On force le texte en blanc/clair */
                    [data-testid="stSidebar"] h1, 
                    [data-testid="stSidebar"] p, 
                    [data-testid="stSidebar"] span,
                    [data-testid="stSidebar"] a {{
                        color: #F2F2F2 !important;
                    }}
                    
                    /* On adoucit la couleur du sous-titre de la sidebar */
                    [data-testid="stSidebar"] caption {{
                        color: #A0AEC0 !important;
                    }}
                    </style>
                """, unsafe_allow_html=True)

# Structure de la page principale

c1, c2, c3 = st.columns(3)

today = dt.date.today()
with c1 : 
    date_choisie = st.date_input("**Quel jour ?**", min_value= today, max_value= today + dt.timedelta(days=5), format= "DD/MM/YYYY")

with c2 :
    creneau_choisi = st.selectbox("**Quand ?**", ["Matin ⛅", "Après-midi ☀️", "Soir 🌙", "Nuit 🌕"])

with c3 :
    ville_choisie = st.text_input("**Où ?**", value= "Paris")

with st.container() :
    if ville_choisie:
       # Récupération du géocodage
       geo_info =  geo_service.get_coordinates(ville_choisie)

       if not geo_info:
           st.error(f"Impossible de localiser la ville : '{ville_choisie}'. Vérifiez l'orthographe.")

       else :
           lat = geo_info["lat"]
           lon = geo_info["lon"]
           display_name = geo_info["display_name"]

    # Récupération de la prévision météo
           forecasts = WeatherService.get_forecast(lat,lon)

           if not forecasts:
               st.warning("Les données météo ne sont pas disponible pour le moment")
           else:
               meteo_actuelle = forecasts[0] 
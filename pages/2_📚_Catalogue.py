import streamlit as st
import datetime as dt
from services import GeocodingService, WeatherService, ActivityService
from models import Weather, Activity

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
weather_service = WeatherService()
activity_service = ActivityService()

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

if "recherche_lancee" not in st.session_state:
    st.session_state.recherche_lancee = False
with st.form("form_recherche"):
    c1, c2 = st.columns(2)

    with c1:
        target_city = st.text_input("**Où**", value= "Paris")

    with c2:
        distance = st.slider("**Rayon ?**", min_value= 5, max_value= 50, step= 5, format= "%d km", on_change= "ignore")

     # Bouton de validation obligatoire dans un st.form
    btn_rechercher = st.form_submit_button("🔍 Trouver des activités", use_container_width=True)
if btn_rechercher:
        st.session_state.recherche_lancee = True

# Récupération des coordonnées géographique
if st.session_state.recherche_lancee:
    if target_city:
    # Récupération du géocodage
        geo_info =  geo_service.get_coordinates(target_city)

        if not geo_info:
            st.error(f"Impossible de localiser la ville : '{target_city}'. Vérifiez l'orthographe.")

        else :
            lat = geo_info["lat"]
            lon = geo_info["lon"]
            display_name = geo_info["display_name"]

            activity_recomended = activity_service.get_activities(lat, lon)


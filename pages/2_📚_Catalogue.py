import streamlit as st
import datetime as dt
from services import GeocodingService, WeatherService, ActivityService
from models import Weather, Activity
import math

cat_indoor = ["entertainment.museum","entertainment.cinema", "entertainment.culture", "entertainment.escape_game", 
                      "entertainment.bowling_alley", "entertainment.amusement_arcade", "entertainment.planetarium",
                      "entertainment.aquarium","leisure.spa"]

cat_outdoor = ["leisure.park", "leisure.playground", "leisure.picnic", "entertainment.theme_park", 
                       "entertainment.water_park", "entertainment.zoo", "entertainment.miniature_golf", 
                       "entertainment.activity_park"]

# Fonction pour le calcul de distance
def calculer_distance(lat1, lon1, lat2, lon2):
    """Calcule la distance orthodromique en km entre deux points GPS."""
    r = 6371.0  # Rayon moyen de la Terre en km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(r * c, 1)

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
#activity_service = ActivityService()

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
        distance = st.slider("**Rayon ?**", min_value= 5, max_value= 50, step= 5, format= "%d km")

    st.write("---")

    f1, f2, f3 = st.columns(3)
    with f1 :
        recherche_nom = st.text_input("**Nom ou mot-clé**", placeholder="Ex : Musée, Parc...")
    with f2 :
        type_environnement = st.selectbox("**Type d'environnement**", options= ["Tous", "Intérieur", "Extérieur"])
    with f3:
        pmr_access = st.toggle("♿ Accessible PMR")
        dog_ok = st.toggle("🐶 Chiens bienvenus")

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

            activity_recomended = ActivityService.get_activities(lat, lon, rayon=distance*1000, environment_type= type_environnement) #on transforme la distance en km en mètre

            for act in activity_recomended:
                act_lat = act.coordinates[0]
                act_lon = act.coordinates[1]
                act.distance = calculer_distance(act_lat, act_lon, lat, lon)

            activity_recomended.sort(key= lambda act: act.distance)
            st.session_state["catalogue_activites"] = activity_recomended

activites = st.session_state.get("catalogue_activites", [])
if activites:
    st.write("---")
    st.subheader("Affiner les résultats")

    with st.container():
        activites_filtrees = []
        for act in activites:
            if recherche_nom:
                if recherche_nom.lower() not in act.name.lower():
                    continue
               
            if type_environnement == "Intérieur" and act.category not in cat_indoor:
                    continue
            elif type_environnement == "Extérieur" and act.category not in cat_outdoor:
                    continue

            # On vérifie si facilities est bien un dico, sinon on considère que c'est vide
            facs = act.facilities if isinstance(act.facilities, dict) else {}
            if pmr_access == True:
                has_pmr = facs.get("wheelchair") is True or facs.get("wheelchair.yes") is True or facs.get("wheelchair.limited") is True
                if not has_pmr:
                    continue # Si pas PMR alors que le toggle est activé, on zappe
            if dog_ok == True:
                 has_dog = facs.get("dogs") is True or facs.get("dogs.yes") is True or facs.get("dogs.leashed") is True
                 if not has_dog:
                    continue
            activites_filtrees.append(act)

        st.write(f"**{len(activites_filtrees)} activité(s) affichée(s)**")

        for i, act in enumerate(activites_filtrees):
            if i % 3 == 0:
                cols = st.columns(3)
            
            # On choisit la colonne active (0, 1 ou 2) grâce au modulo (%)
            colonne_actuelle = cols[i % 3]
            
            # On dessine la carte dans cette colonne
            with colonne_actuelle:
                with st.container(border=True):
                    st.markdown(act.to_popup_html(), unsafe_allow_html=True)


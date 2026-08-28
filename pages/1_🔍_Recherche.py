import streamlit as st
import datetime as dt
from services import GeocodingService, WeatherService, ActivityService
from models import Weather, Activity
from streamlit_folium import st_folium
import folium

# --- STYLES DES MARQUEURS ---
STYLE_CATEGORIES = {
                    # Culture & Spectacles
                    "entertainment.museum": ("darkblue", "landmark"),
                    "entertainment.cinema": ("purple", "film"),
                    "entertainment.culture": ("purple", "theater-masks"),
                    "entertainment.culture.theatre": ("purple", "theater-masks"),
                    "entertainment.culture.arts_centre": ("purple", "palette"),
                    "entertainment.culture.gallery": ("purple", "image"),
                    "entertainment.planetarium": ("darkblue", "globe"),

                    # Jeux & Loisirs intérieurs
                    "entertainment.escape_game": ("darkpurple", "key"),
                    "entertainment.bowling_alley": ("cadetblue", "bowling-ball"),
                    "entertainment.amusement_arcade": ("cadetblue", "gamepad"),
                    "entertainment.aquarium": ("blue", "fish"),
                    "leisure.spa": ("cadetblue", "spa"),
                    "leisure.spa.sauna": ("cadetblue", "hot-tub"),
                    "leisure.spa.public_bath": ("cadetblue", "bath"),

                    # Plein air & Nature
                    "leisure.park": ("green", "tree"),
                    "leisure.park.garden": ("lightgreen", "leaf"),
                    "leisure.park.nature_reserve": ("darkgreen", "tree"),
                    "leisure.playground": ("orange", "child"),
                    "leisure.picnic": ("lightgreen", "utensils"),
                    "leisure.picnic.picnic_site": ("lightgreen", "utensils"),
                    "leisure.picnic.bbq": ("lightred", "fire"),

                    # Parcs & Attractions
                    "entertainment.theme_park": ("orange", "ticket-alt"),
                    "entertainment.water_park": ("blue", "swimming-pool"),
                    "entertainment.zoo": ("green", "paw"),
                    "entertainment.miniature_golf": ("lightgreen", "golf-ball"),
                    "entertainment.activity_park": ("orange", "running"),
                    "entertainment.activity_park.climbing": ("darkred", "mountain"),
                    "entertainment.activity_park.trampoline": ("orange", "arrows-alt-v"),
                    "entertainment.flying_fox": ("darkgreen", "hiking"),
                }

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
if "recherche_lancee" not in st.session_state:
    st.session_state.recherche_lancee = False
with st.form("form_recherche"):
    c1, c2, c3 = st.columns(3)

    today = dt.date.today()
    with c1 : 
        date_choisie = st.date_input("**Quel jour ?**", min_value= today, max_value= today + dt.timedelta(days=5), format= "DD/MM/YYYY")

    with c2 :
        creneau_choisi = st.selectbox("**Quand ?**", ["Matin ⛅", "Après-midi ☀️", "Soir 🌙", "Nuit 🌕"])

    with c3 :
        ville_choisie = st.text_input("**Où ?**", value= "Paris")

    # Bouton de validation obligatoire dans un st.form
    btn_rechercher = st.form_submit_button("🔍 Trouver des activités", use_container_width=True)
if btn_rechercher:
    st.session_state.recherche_lancee = True
with st.container() :
    if st.session_state.recherche_lancee:
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
                #st.write("👉 Tentative d'appel de l'API Météo...")
                forecasts = weather_service.get_forecast(lat,lon)

                if not forecasts:
                    st.warning("Les données météo ne sont pas disponible pour le moment")
                else:
                    dic_horaire = {
                                        "Matin ⛅": range(6, 12), 
                                        "Après-midi ☀️" : range(12, 18), 
                                        "Soir 🌙" : range(18, 22), 
                                        "Nuit 🌕" : [22, 23, 0, 1, 2, 3, 4, 5]
                                        }
                    heure_cible = dic_horaire[creneau_choisi]
                    date_choisie_str = date_choisie.strftime("%Y-%m-%d") # conversion de l'objet date en str car str dans la classe WeatherService

                    meteo_actuelle = None # Sécurité dans le cas ou aucun créneau correspondant
                    
                    for f in forecasts:
                            heure_int = int(f.heure_affichage.split(":")[0])
                            if f.date == date_choisie_str and heure_int in heure_cible :
                                meteo_actuelle = f
                                break

                if meteo_actuelle:
                        suggestion = meteo_actuelle.suggest_environment()
                        #st.info(f"💡 Indice pour ce créneau : **{suggestion}**") => Vérification du fonctionnement de la récupération des éléments
                else:
                        st.warning("Aucune prévision exacte trouvée pour ce créneau précis.")
                        suggestion = "Outdoor" #Sécurité donnée une valeur par défaut à suggestion dans le cas météo actuelle ne renvoie rien
                        
                activity_recomended = activity_service.get_activities(lat, lon, suggestion)
                if not activity_recomended :
                        st.warning("Aucune activité trouvé dans ce rayon pour cette zone.")
                else: 
                        m= folium.Map(location=[lat, lon], zoom_start= 15)
                        
                        # Marqueur du centre (point de recherche)
                        folium.Marker(
                            location=[lat, lon],
                            popup=f"<b>Centre :</b> {display_name}",
                            tooltip="Point central",
                            icon=folium.Icon(color="red", icon="info-sign")
                        ).add_to(m)

                        # Marqueurs des activités
                        for act in activity_recomended:
                            # Création du marqueur avec le style défini
                            style = STYLE_CATEGORIES.get(act.category, ("blue", "map-marker"))
                            couleur, icone = style

                            folium.Marker(
                                location=act.coordinates,
                                popup=folium.Popup(act.to_popup_html(), max_width=300),
                                tooltip=act.name,
                                icon=folium.Icon(color=couleur, icon=icone, prefix="fa")
                            ).add_to(m)
                        
                        st_folium(m, width= 1000, height= 500, returned_objects=[])
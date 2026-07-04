from models import Weather, Activity
import streamlit as st
from services import GeocodingService, WeatherService

# Configuration globale de la page d'accueil
st.set_page_config(page_title="UrbanPulse Planner | Accueil", page_icon="🌦️", layout="wide")

# --- MENU LATÉRAL PERSONNALISÉ ---
st.sidebar.markdown("# 🏙️ UrbanPulse")
st.sidebar.caption("Votre planificateur intelligent")
st.sidebar.write("---")

# Liens de navigation propres
st.sidebar.page_link("app.py", label="Accueil", icon="🏠")
st.sidebar.page_link("pages/1_🔍_Recherche.py", label="Recherche d'activités", icon="🔍")
st.sidebar.page_link("pages/2_📚_Catalogue.py", label="Catalogue des lieux", icon="📚")
st.sidebar.write("---")

# Initialisation des briques de services
geo_service = GeocodingService()
weather_service = WeatherService()

#SECTION 1 : En-tête et explication du projet
st.title("UrbanPulse Planner 🌦️🏃")
st.markdown("""
    ### Simplifiez vos sorties, maîtrisez votre journée !
Bienvenue sur **UrbanPulse Planner**, l'application intelligente qui connecte la météo locale avec vos envies d'exploration. 

* **Comment ça marche ?** Indiquez votre ville et votre créneau, notre algorithme analyse en direct les prévisions météo pour vous recommander instantanément le meilleur environnement (**Intérieur** ou **Extérieur**).
* **Le plus ?** Profitez de recommandations de lieux précis (musées, parcs, complexes sportifs) géo-localisés autour de vous, avec toutes leurs informations pratiques accessibles en un clic.
            """)

st.write("---")

#SECTION 2 : Module météo express
st.subheader("🔍 Météo Express")
st.write("Consultez rapidement les conditions météo actuelles de la ville de votre choix.")

# Barre de recherche avec "Paris" comme valeur textuelle par défaut
ville_recherche = st.text_input("Entrez une ville pour voir sa météo :", value="Paris")

# On lance la recherche dès que l'utilisateur valide ou que la page se charge
if ville_recherche :
    with st.spinner(f"Récupération de la météo pour {ville_recherche}..."):
        # 1. Appel du Géocodage
        geo_info = geo_service.get_coordinates(ville_recherche)
        if not geo_info:
            st.error(f"Impossible de localiser la ville : '{ville_recherche}'. Vérifiez l'orthographe.")
        else:
            lat = geo_info["lat"]
            lon = geo_info["lon"]
            display_name = geo_info["display_name"]

            # 2. Appel de la météo
            forecasts = weather_service.get_forecast(lat, lon)
            
            if not forecasts:
                st.warning("Les données météo ne sont pas disponibles pour le moment.")
            else:
                # On récupère la prévision immédiate (le premier objet Weather de la liste)
                meteo_actuelle = forecasts[0]

                # Affichage des résultats dans un encadré propre
                with st.container(border=True):
                    st.write(f"### 📍 {meteo_actuelle.city}")
                    st.caption(f"Nom complet : {display_name}")
                    
                    # Mise en page en colonnes pour les métriques météo
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Température", f"{meteo_actuelle.temperature} °C")
                    c2.metric("Ressenti", f"{meteo_actuelle.temp_ressenti} °C")
                    c3.metric("Vent", f"{meteo_actuelle.wind_speed} m/s")
                    c4.metric("Pluie / Nuages", f"{meteo_actuelle.cloudiness} %")
                    
                    # Petite description en français
                    st.write(f"**Conditions actuelles :** {meteo_actuelle.weather_description.capitalize()}")
                    
                    # Suggestion dynamique calculée par votre méthode de classe POO !
                    suggestion = meteo_actuelle.suggest_environment()
                    st.info(f"💡 **Indice UrbanPulse :** Météo favorable pour des activités en **{suggestion}**.")
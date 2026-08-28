# Import des bibliothèques
import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from models import Weather, Activity
import streamlit as st

# On récupère le chemin absolu du dossier où se trouve le script actuel
base_dir = Path(__file__).resolve().parent
env_path = base_dir / ".env"

# On force load_dotenv à lire ce chemin précis
load_dotenv(dotenv_path=env_path)

#Test de connexion à la clé API
#def test_connexion():
    #print(f"Ma clé OpenWeather est bien chargée : {weather_api_key}")

# test = test_connexion()

class GeocodingService : 
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"

    def get_coordinates(self, city_name):
        # Prend un nom de ville et renvoie un dictionnaire avec lat et lon
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        params = {
            "city" : city_name,
            "format": "json",
            "limit": "1", 
            "countrycodes": "fr"
        }
        try:
            response = requests.get(self.base_url, headers= headers, params= params)
            if response.status_code != 200:
                return None
            
            data = response.json()

            if not data:
                return None
            
            lon = float(data[0]['lon'])
            lat = float(data[0]['lat'])
            return {
                "lat": lat,
                "lon": lon,
                "display_name": data[0].get('display_name')
            }
        
        except requests.exceptions.RequestException:
            return None

class WeatherService :
    def __init__(self):
        # Récupération de la clé API Weather
        self.api_key = os.getenv("OPENWEATHER_KEY")
        # URL pour les prévisions 5jours / 3 heures
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"

    def get_forecast(self, lat, lon):
        # Prend une ville en paramètre, interroge l'API et retourne une liste d'objets Weather
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric", # Pour avoir des degrès celsius
            "lang": "fr" # Pour avoir les données en français
        }

        try:
            response = requests.get(self.base_url, params = params)
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            # Extraction des infos communes de la ville
            city_info = data.get("city", {})
            city_name = city_info.get("name")
            sunrise = city_info.get("sunrise")
            sunset = city_info.get("sunset")

            # Céation d'une liste vide pour stocker les futurs objets Weather
            weather_objects = []

            # boucle sur les 40 éléments de prévision du json
            for forecast in data.get("list", []):
                main_data = forecast.get("main", {})
                weather_details = forecast.get("weather", [{}])[0]
                date_complete = forecast.get("dt_txt") 
                date_seule = date_complete.split(" ")[0] 
                heure_seule = date_complete.split(" ")[1]

             # Création de l'objet en lui passant les valeurs extraites du json
                objet_meteo = Weather(
                    date=date_seule,
                    time=forecast.get("dt"),
                    heure_affichage=heure_seule,
                    part_of_day=forecast.get("sys", {}).get("pod"),
                    temperature=main_data.get("temp"),
                    temp_ressenti=main_data.get("feels_like"),
                    min_temp=main_data.get("temp_min"),
                    max_temp=main_data.get("temp_max"),
                    weather=weather_details.get("main"),
                    weather_description=weather_details.get("description"),
                    cloudiness=forecast.get("clouds", {}).get("all", 0),  # Valeur par défaut si absent
                    wind_speed=forecast.get("wind", {}).get("speed", 0),  # Valeur par défaut si absent
                    prob_of_precipitation=forecast.get("pop", 0),
                    city=city_name,
                    city_sunset=sunset,
                    city_sunrise=sunrise
                )

            # On ajoute l'objet à la liste
                weather_objects.append(objet_meteo)
        
            return weather_objects

        except requests.exceptions.RequestException:
            return []
        
class ActivityService:
    def __init__(self):
        self.api_key = os.getenv("PLACESAPI_KEY")
        self.base_url = "https://api.geoapify.com/v2/places"

    #@st.cache_data(ttl=86400) # Ajout d'un cache qui s'efface toutes les 24 heures
    def get_activities(self, lat, lon, environment_type = "Outdoor"):
        
        # Choix dynamique des catégories Geoapify selon la suggestion de la classe Weather
        if environment_type == "Indoor":
            categories = (
                "entertainment.museum,"
                "entertainment.cinema,"
                "entertainment.culture,"
                "entertainment.escape_game,"
                "entertainment.bowling_alley,"
                "entertainment.amusement_arcade,"
                "entertainment.planetarium,"
                "entertainment.aquarium,"
                "leisure.spa"
            )
        else:
            categories = (
                "leisure.park,"
                "leisure.playground,"
                "leisure.picnic,"
                "entertainment.theme_park,"
                "entertainment.water_park,"
                "entertainment.zoo,"
                "entertainment.miniature_golf,"
                "entertainment.activity_park"
            )
        
        params = {
            "categories" : categories,
            "filter" : f"circle:{lon},{lat},30000", # recherche dans un rayon de 30km
            "bias" : f"proximity:{lon},{lat}", # on priorise les lieux les plus proches
            "limit" : 200, # on limite à 200 résultats
            "apiKey": self.api_key,
            "lang": "fr"
        }

        try:
            response = requests.get(self.base_url, params= params)
            
            if response.status_code != 200:
                print(f"Erreur Geoapify : {response.status_code}")
                return []
            
            data = response.json()
            if not data or "features" not in data:
                return []
            
            activity_objects = []

            for activity in data.get("features", []):
                properties = activity.get("properties", {})
                geometry = activity.get("geometry", {})
                website= properties.get("website")
                opening_hours= properties.get("opening_hours")
                raw_data = properties.get("datasource", {}).get("raw", {})
                phone = raw_data.get("phone")
                image = raw_data.get("image")

                coords_brutes = geometry.get("coordinates", [0,0])

                # Sécurité pour ignorer l'activité si elle n'a pas de nom
                name = properties.get("name")
                if not name:
                    continue

                categories_brutes = properties.get("categories", [])
                # On cherche en priorité une sous-catégorie de loisirs/culture
                cat_choisie = next(
                    (c for c in categories_brutes if c.startswith("entertainment.") or c.startswith("leisure.")),
                    next((c for c in categories_brutes if "." in c), "Activité")
                )
                
                objet_activite = Activity(
                    name = name,
                    state=properties.get("state"),
                    county= properties.get("county"),
                    address= properties.get("formatted"),
                    # Inversion de l'ordre pour respecter le tuple lat lon
                    coordinates= (coords_brutes[1], coords_brutes[0]),
                    phone= phone,
                    website= website,
                    image= image,
                    category= cat_choisie,
                    opening_hours= opening_hours,
                    facilities= properties.get("facilities")
                )

                activity_objects.append(objet_activite)

            return activity_objects
        
        except requests.exceptions.RequestException:
            return []
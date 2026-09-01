# Import des bibliothèques
import requests
import pandas as pd
import streamlit as st

# Création des classes

class Weather :
    def __init__(self, date, time, heure_affichage, part_of_day, temperature, temp_ressenti, min_temp, max_temp, weather, 
                 weather_description, cloudiness, wind_speed, prob_of_precipitation, city, city_sunset, city_sunrise):
        self.date = date
        self.time = time
        self.heure_affichage = heure_affichage
        self.part_of_day = part_of_day
        self.temperature = temperature
        self.temp_ressenti = temp_ressenti
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.weather = weather
        self.weather_description = weather_description
        self.cloudiness = cloudiness
        self.wind_speed = wind_speed
        self.prob_of_precipitation = prob_of_precipitation
        self.city = city
        self.city_sunset = city_sunset
        self.city_sunrise = city_sunrise

    # Méthode pour déterminer s'il fait nuit et proposer les activités en conséquence 
    def is_nighttime(self) -> bool:
        # "n" = night (nuit), "d" = day (jour)
        return self.part_of_day == "n"
    
    # Méthode pour suggérer des activités intérieur ou extérieur en fonction de la météo
    def suggest_environment(self):
        # 🛠️ Sécurisation : On force la température à devenir un nombre décimal
        try:
            temp_numerique = float(self.temperature)
        except (TypeError, ValueError):
            temp_numerique = 20.0 # Valeur de secours par défaut si bug
            
        # Petit espionnage dans le terminal Git Bash pour vérifier
        print(f"--- DEBUG URBANPULSE : Ville={self.city} | Temp={temp_numerique} | Type={type(temp_numerique)} ---")

        mauvais_temps = self.weather in ["Rain", "Snow", "Thunderstorm"]
        temperature_extreme = temp_numerique >= 30.0 or temp_numerique < 15.0

        if mauvais_temps or temperature_extreme or self.is_nighttime():
            return "Indoor"
        return "Outdoor"
    
class Activity : 
    def __init__(self, name, state, county, address, coordinates, phone, website, image,category, opening_hours, facilities):
        self.name = name
        self.state = state
        self.county = county
        self.address = address
        self.coordinates = coordinates # Tuple de coordonnées latitude, longitude
        self.phone = phone
        self.website = website
        self.image = image
        self.category = category
        self.opening_hours = opening_hours
        self.facilities = facilities
    
    def to_geojson(self):
        pass

    def format_opening_hours(self):
        if not self.opening_hours or not isinstance(self.opening_hours, str):
            return None
        
        texte = self.opening_hours
        
        traductions = {
            # Jours de la semaine
            "Mo": "Lun", "Tu": "Mar", "We": "Mer", "Th": "Jeu",
            "Fr": "Ven", "Sa": "Sam", "Su": "Dim",
            
            # Mois (norme OSM 3 lettres)
            "Jan": "Janv.", "Feb": "Févr.", "Mar": "Mars", "Apr": "Avr.",
            "May": "Mai", "Jun": "Juin", "Jul": "Juil.", "Aug": "Août",
            "Sep": "Sept.", "Oct": "Oct.", "Nov": "Nov.", "Dec": "Déc.",

            # Mois en anglais complet (au cas où)
            "January": "Janvier", "February": "Février", "March": "Mars",
            "April": "Avril", "June": "Juin", "July": "Juillet",
            "August": "Août", "September": "Septembre", "October": "Octobre",
            "November": "Novembre", "December": "Décembre",

            # Statuts et mentions spéciales
            "off": "Fermé",
            "closed": "Fermé",
            "open": "Ouvert",
            "PH": "Jours fériés",
            "SH": "Vacances scolaires"
        }
        
        # Remplacement des termes anglais
        for en, fr in traductions.items():
            texte = texte.replace(en, fr)
            
        # Remplacement du séparateur par des retours à la ligne propres ou des tirets
        texte = texte.replace(";", "<br>&nbsp;&nbsp;&nbsp;&nbsp;")
        
        return f"🕒 <b>Horaires :</b><br>&nbsp;&nbsp;&nbsp;&nbsp;{texte}"

    def to_popup_html(self):
        elements = []
        elements.append(f"<strong>{self.name}</strong>")
        TRADUCTION_CATEGORIES = {# Culture & Spectacle
                                "entertainment.museum": "🏛️ Musée",
                                "entertainment.cinema": "🎬 Cinéma",
                                "entertainment.culture": "🎭 Espace culturel",
                                "entertainment.culture.theatre": "🎭 Théâtre",
                                "entertainment.culture.arts_centre": "🎨 Centre d'art",
                                "entertainment.culture.gallery": "🖼️ Galerie d'art",
                                "entertainment.planetarium": "🌌 Planétarium",

                                # Jeux & Détente couverte
                                "entertainment.escape_game": "🗝️ Escape Game",
                                "entertainment.bowling_alley": "🎳 Bowling",
                                "entertainment.amusement_arcade": "🕹️ Salle d'arcade",
                                "entertainment.aquarium": "🐠 Aquarium",
                                "leisure.spa": "🧖 Spa & Bien-être",
                                "leisure.spa.sauna": "🧖 Sauna",
                                "leisure.spa.public_bath": "🛁 Bains publics",

                                # Plein air & Nature
                                "leisure.park": "🌳 Parc / Jardin",
                                "leisure.park.garden": "🌷 Jardin",
                                "leisure.park.nature_reserve": "🌲 Réserve naturelle",
                                "leisure.playground": "🛝 Aire de jeux",
                                "leisure.picnic": "🧺 Espace pique-nique",
                                "leisure.picnic.picnic_site": "🧺 Aire de pique-nique",
                                "leisure.picnic.bbq": "🍖 Zone barbecue",

                                # Attractions & Sports
                                "entertainment.theme_park": "🎡 Parc d'attractions",
                                "entertainment.water_park": "🌊 Parc aquatique",
                                "entertainment.zoo": "🦁 Zoo",
                                "entertainment.miniature_golf": "⛳ Mini-golf",
                                "entertainment.activity_park": "🧗 Parc d'aventure",
                                "entertainment.activity_park.climbing": "🧗 Escalade",
                                "entertainment.activity_park.trampoline": "🤸 Trampoline park",
                                "entertainment.flying_fox": "🌲 Tyrolienne",
                            }
        categorie_lisible = TRADUCTION_CATEGORIES.get(self.category, self.category.replace(".", " ").capitalize())
        elements.append(f"<span>{categorie_lisible}</span>")
        if self.address is not None:
            elements.append(f"📍 {self.address}")
        if self.phone is not None:
            elements.append(f"📞 <a href='tel:{self.phone}'>{self.phone}</a>")
        if self.website is not None:
            elements.append(f"🌐<a href= '{self.website}' target='_blank'>Visiter le site</a>")
        horaires_format = self.format_opening_hours()
        if horaires_format:
            elements.append(horaires_format)
        if isinstance(self.facilities, dict):
            dic_labels = {#Accssibilité
                          "wheelchair" : "♿ Accessible PMR",
                          "wheelchair.yes" : "♿ Accessible PMR",
                          "wheelchair.limited" : "♿ Accessibilité partielle",
                          # Animaux
                          "dogs" : "🐶 Chiens bienvenus",
                          "dogs.yes" : "🐶 Chiens bienvenus",
                          "dogs.leashed" : "🐕 Chiens en laisse",
                          "no-dogs" : "🚫 Chiens interdits",
                          # Connexion
                          "internet_access" : "📶 Wi-Fi",
                          "internet_access.free" : "📶 Wi-Fi gratuit",
                          "internet_access.for_customers" : "📶 Wi-Fi réservé",
                          # Tarifs
                          "no_fee.no" : "🎟️ Entrée gratuite",
                          "no_fee" : "🎟️ Entrée gratuite",
                          "fee" : "💳 Entrée payante"}
            for k, v in self.facilities.items():
                if v is True and k in dic_labels.keys():
                    elements.append(dic_labels[k])
        return "<br>".join(elements)
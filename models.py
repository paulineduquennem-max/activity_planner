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
    def is_nighttime(self):
        if self.time > self.city_sunset or self.time < self.city_sunrise:
            return "Night time"
        return "Day time"
    
    # Méthode pour suggérer des activités intérieur ou extérieur en fonction de la météo
    def suggest_environment(self):
        if self.weather in ["Rain", "Snow", "Thunderstorm"]:
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
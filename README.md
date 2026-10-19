# 🏙️ UrbanPulse

**UrbanPulse** est un planificateur urbain intelligent et interactif développé en Python avec **Streamlit**. L'application croise les prévisions météorologiques locales et des données géolocalisées pour recommander et filtrer les meilleures activités (culturelles, de loisirs, en plein air ou en intérieur) autour d'une ville donnée.

🔗 **Application en ligne :** https://activityplanner-urban-planner.streamlit.app/

---

## 🚀 Fonctionnalités principales

- **Recherche géolocalisée intelligente :** Saisie d'une ville (géocodage) et définition d'un rayon de recherche personnalisable.
- **Recommandation météo dynamique :** Intégration des prévisions météo pour suggérer automatiquement un type d'activité adapté (en intérieur ou en extérieur selon le temps et la température).
- **Filtres avancés et fluides :** Filtrage par mots-clés, type d'environnement, accessibilité PMR et compatibilité avec les animaux de compagnie (chiens bienvenus), sans rechargement intempestif de la page grâce à l'utilisation de formulaires optimisés (`st.form`).
- **Cartographie interactive :** Visualisation des lieux et du point central de recherche via une carte interactive (Folium).
- **Catalogue persistant :** Maintien d'un état global des activités via `st.session_state` pour naviguer fluidement entre la recherche et la vue catalogue.

---

## 🛠️ Stack technique & Architecture

- **Langage :** Python
- **Interface utilisateur :** Streamlit
- **Architecture :** Programmation Orientée Objet (POO) avec séparation des services et des modèles de données.
- **APIs externes :** 
  - *Geoapify Places API* (pour la récupération des lieux et des équipements)
  - *OpenWeather API* (pour les prévisions météo)
- **Bibliothèques clés :** 
  - `requests` (appels API)
  - `streamlit-folium` & `folium` (cartographie)
  - `@st.cache_data` (optimisation des performances et mise en cache des requêtes sur 24h)

---

## 📂 Structure du projet

```text
projet_python_weather_and_activity/
│
├── app.py                  # Page d'accueil de l'application
├── pages/
│   ├── 1_🔍_Recherche.py   # Page principale de recherche et météo
│   └── 2_📚_Catalogue.py   # Page de consultation et affichage en grille
│
├── services.py             # Services métier (Géocodage, Météo, Activités & Cache)
├── models.py               # Modèles de données orientés objet (Activity, Weather)
├── requirements.txt        # Dépendances du projet
└── README.md               # Documentation du projet


⚙️ Installation et lancement local
Si tu souhaites exécuter le projet en local sur ta machine :

1. Cloner le dépôt :
git clone [https://github.com/ton-nom-utilisateur/projet_python_weather_and_activity.git](https://github.com/ton-nom-utilisateur/projet_python_weather_and_activity.git)
cd projet_python_weather_and_activity

2. Créer et activer un environnement virtuel :
python -m venv .venv
# Sur Windows :
.venv\Scripts\activate
# Sur macOS/Linux :
source .venv/bin/activate

3. Installer les dépendances :
pip install -r requirements.txt

4. Configurer les clés API :
Crée un fichier .env à la racine du projet et ajoute tes clés personnelles :
PLACESAPI_KEY=ta_cle_geoapify
WEATHER_API_KEY=ta_cle_openweather

5. Lancer l'application Streamlit :
streamlit run app.py

💡 Défis techniques & Résolutions
Gestion du cache et des méthodes statiques : Contournement des erreurs de hachage de Streamlit (UnhashableParamError) sur les objets d'instance en structurant les appels via des méthodes statiques et des fonctions indépendantes.

Expérience utilisateur (UX) : Intégration de l'ensemble des critères de recherche et des filtres dans un st.form unique pour éviter les rechargements de page à chaque modification de paramètre.

👩‍💻 Auteure
Projet développé par Pauline Duquenne - Data Analyst.

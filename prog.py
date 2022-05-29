from time import sleep # Pour le délai entre les mesures
from datetime import datetime # Pour le timestamp
import subprocess # Pour l'execution de commandes dans le terminal
from pymongo import MongoClient # Pour la connexion à la bdd
import json # Pour la gestion des JSON
import requests # Pour les paramètres HTTP

#==============================VARIABLES===============================#
delai = 5 # nombre de secondes entre les mesures
#gpio = "21" # Numéro du GPIO data du RPI
ipMongo = "203.0.113.1" # IP de la base de donnée MongoDB (npo /etc/mongodb.conf)
portMongo = 27017
nom = "meunier"
proxy = { "http": "http://cache.univ-pau.fr:3128" } # Ajouter à la requête si décommenté
#======================================================================#

while 1 : # On répète à l'infini
    try: # Si la valeur récupérée est conforme (pas d'erreur de DHTReader)
        output = subprocess.run(["dhtReader", "--pin", "21", "--type", "DHT11"], capture_output=True) # Récupère les valeurs du capteur en un JSON
        #print("Données simulées - capteur désactivé")
        #output = '{"temperature":21.0,"humidity":47.0}' # Données de test, JSON
        #print(output.stdout)
        result = json.loads(output.stdout) # Place le JSON dans result
        print(datetime.utcnow())

        timestamp = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000) # Récupère la timestamp

        # Données vers la console
        print("")
        print("Timestamp :" , timestamp)
        print("Température :" , result['temperature'])
        print("Humidité :" , result['humidity'])
        print("")

        client = MongoClient(ipMongo, portMongo) # Connexion à la base Mongodb

        db = client.iut # bdd "iut"
        table = db.at04w # collection "at04w"
        ligne = {"temperature": result['temperature'], "humidity": result['humidity'],"timestamp": timestamp} # Préparation de la ligne à insérer
        table.insert_one(ligne) # Insertion de la ligne

        url = "http://at04w.otf.cloud/insertdata" # URL de la requête
        params = {  "collection":nom,"timestamp":timestamp,"temp":result['temperature'],"humidity":result['humidity'] } # Paramètres à passer
        r = requests.get(url, params=params, proxies=proxy) # Envoi de la requête (décommenter la dernière partie pour utilisation du proxy UPPA)
        sleep(delai) # Pause de durée déterminée lors de l'initialisation des variables

    except (ValueError): # En cas d'erreur de DHTReader
        print("Erreur") # On prévient l'utilisateur
        continue # Le programme reprend son cours
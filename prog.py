from time import sleep # Pour le délai entre les mesures
import datetime # Pour le timestamp
import subprocess # Pour l'execution de commandes dans le terminal
from pymongo import MongoClient # Pour la connexion à la bdd
import json # Pour la gestion des JSON
import requests # Pour les paramètres HTTP

#==============================VARIABLES===============================#
delai = 5 # Nombre de secondes entre les mesures
gpio = 21 # Numéro du GPIO data du RPI
ipMongo = "192.168.1.23" # IP de la base de donnée MongoDB (npo /etc/mongodb.conf)
portMongo = 27017
nom = "meunier" # Collection sur at04w.otf.cloud
# proxy = { "http": "http://cache.univ-pau.fr:3128" } # Ajouter à la requête si décommenté
#======================================================================#

while 1 :
    #output = subprocess.run(["./dhtReader", "--pin",gpio, "--type", "DHT11"]) # Récupère les valeurs du capteur en un JSON
    print("Données simulées - capteur désactivé")
    output = '{"temperature":21.0,"humidity":47.0}' # Données de test, JSON
    result = json.loads(output) # Place le JSON dans result

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
    r = requests.get(url, params=params)#, proxies=proxy) # Envoi de la requête (décommenter la dernière partie pour utilisation du proxy UPPA)
    sleep(delai)
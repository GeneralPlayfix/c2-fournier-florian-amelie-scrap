from time import sleep
import urllib.parse
import requests
import json
from bs4 import BeautifulSoup


def main():
    departement = None
    profession = ""
    while departement is None or profession == "" : 
        profession = str(input("Rentrer une profression : \n") or "Médecin généralist")
        departement = int(input("Rentrer un département (numéro): \n") or 34)
    scrap(departement=departement, professionNom=profession)

def scrap(departement, professionNom):

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    professionUrl = 'http://annuairesante.ameli.fr/xhr/profession?' + urllib.parse.urlencode({'acte': '', 'term':professionNom})
    profession = requests.get(professionUrl, headers=headers)  
    if profession.status_code != 200:
        print("error")
        return
    profession = profession.json()[0]  

    localisationUrl= 'http://annuairesante.ameli.fr/xhr/location-ps?term='+str(departement)    
    localisation = requests.get(localisationUrl, headers=headers).json()[0]
    print(localisation['value'])

    payload = {"type":"ps","ps_profession":profession['id'], "ps_profession_label":profession["label"], "ps_localisation":localisation['value'],"localisation_category":localisation['categoryParam']}


    r = requests.post("http://annuairesante.ameli.fr/recherche.html", params=payload)
    soup = BeautifulSoup(r.content, 'lxml')

    medecins = soup.find_all("div", class_="item-professionnel")
    
    validMedecins = [] 
    for medecin in medecins:
        name = medecin.find("a").get_text()
        tel = medecin.find("div", class_="tel")
        if tel is not None:
            tel = tel.get_text()
        adresse = medecin.find("div", class_="adresse").get_text()
        validMedecins.append({name, tel, adresse})
    
    print(validMedecins)

main()


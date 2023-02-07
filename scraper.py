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
   
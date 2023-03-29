#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 13:22:01 2023

@author: inesamar
"""

import pickle
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# The Logement class shows the housing's data
class Logement:
    def __init__(self, prix, localisation, nbpieces, taille, appart):
        assert prix.isnumeric(), "L'attribut prix doit être de type numérique"
        assert nbpieces.isnumeric(), "L'attribut nbpieces doit être de type numérique"
        assert taille.isnumeric(), "L'attribut taille doit être de type numérique"
        self.prix = prix
        self.localisation = localisation
        self.nbpieces = nbpieces
        self.taille = taille
        self.appart = appart
        
    def __str__(self):
        return "{} de {} pièces et {} m², à {}, au prix de {}€".format(self.appart, self.nbpieces, self.taille, self.localisation, self.prix)

# The Annonce class shows the agency's and platform's data, and the housing's data
class Annonce:
    def __init__(self, plateforme, agence, logement):
        self.plateforme = plateforme
        self.agence = agence
        self.logement = logement
    
    def __str__(self):
        return "Annonce de la plateforme {}, venant de l'agence {}, à propos du logement suivant : {}".format(self.plateforme, self.agence, self.logement)


# The Candidature class is a recapitulative of the applicant's data and the housing's data
class Candidature:
    def __init__(self, mail, tel, date, annonce, typ):
        assert '@' in mail, "La'ttribut mail doit contenir le caractère @"
        assert len(tel) == 10, "L'attribut tel doit faire 10 caractères"
        assert tel.isnumeric(), "L'attribut tel doit être de type numérique"
        self.mail = mail
        self.tel = tel
        self.date = date
        self.annonce = annonce
        self.typ = typ
    
    def __str__(self):
        return "Le candidat {} a pour adresse mail : {} et pour numéro de téléphone : {}.\nSa candidature a été reçue le {}/{}/{} à {}h{}, en réponse à l'annonce suivante : {}.".format(self.typ, self.mail, self.tel, self.date.day, self.date.month, self.date.year, self.date.hour, self.date.minute, self.annonce)



# The users puts here the path to the pickle file with the e-mail data
path = input("Enter the path to the pickle file :\n(Example : ../email_technical_test.pickle)\n")
file_path = path

# Opening the pickle file and loading the data
file = open(file_path, 'rb')
data = pickle.load(file)
# Closing the pickle file
file.close()

# Spliting the data to find the most important informations
# Finding the email of the applicant
mail = data["reply_to"][0]['email']

# Finding the date of the application
date = data["received_at"]

# Separating the "body" part of the file to make the research easiest
body = data["body"]

# Finding the number of the applicant
ind_tel = body.find("06&nbsp")
# In case of a 07 type of number (and not 06) :
if ind_tel == -1:
    ind_tel = body.find("07&nbsp")

tel0 = body[ind_tel:ind_tel+34]
# Replacing the character from html
tel = tel0.replace('&nbsp;', '')

# Finding the platform that shared the ad
plateforme = data["from"][0]["name"]
ref_ind = body.find("RÉFÉRENCE")
ref_ind_fin = body[ref_ind:len(body)].find("</a>")
agence = body[ref_ind+17:ref_ind+ref_ind_fin]

# Finding the price of the place
prix_ind_fin = body.find("€")
prix_ind = body[prix_ind_fin-20:prix_ind_fin-6].find(">")
prix = body[prix_ind_fin-prix_ind+1:prix_ind_fin-6]

# Finding the description of the place
desc_ind = body.find("Appartement")
if desc_ind == -1:
    desc_ind = body.find("Maison")
desc_ind_fin = body[desc_ind:len(body)].find("<")
desc = body[desc_ind:desc_ind+desc_ind_fin].replace("&nbsp;", " ")

# Finding the size and number of rooms
nbpieces_ind = desc.find("pièces")
if nbpieces_ind == -1:
    nbpieces_ind = desc.find("pièce")

taille_ind = desc.find("m²")
taille_ind_deb = desc[taille_ind-15:taille_ind].find(" ")

nbpieces = desc[nbpieces_ind-2:nbpieces_ind-1]
taille = desc[taille_ind - taille_ind_deb-1:taille_ind-1]

# Finding if it's an appartment or a house
appart_ind = desc.find(" ")
appart = desc[0:appart_ind]

# Finding the localization
loc_ind = data["subject"].find("à")
loc = data["subject"][loc_ind+2:len(data["subject"])]

# Finding what type of application it is (rent or buying)
typ = body.find("locataire")
location = "locataire"
if typ == -1:
    location = ""



# Initialization of the objects of the new classes, with the data found in the pickle file
l1 = Logement(prix, loc, nbpieces, taille, appart)
a1 = Annonce(plateforme, agence, l1)
c1 = Candidature(mail, tel, date, a1, location)
print(c1)

# Conversion of the date to String in order to put it in the json file
date_str = date.strftime("%d/%m/%Y %H:%M")

# Creation of a dictionnary to export it as a json file
export = {
	"mail": c1.mail,
	"telephone": c1.tel,
    "type de demande": c1.typ,
	"date": date_str,
	"plateforme": a1.plateforme,
    "agence": a1.agence,
    "description": l1.appart,
    "localisation": l1.localisation,
    "pieces": l1.nbpieces,
    "taille": l1.taille,
    "prix": l1.prix
}

# The user puts here where he wants the json file to be
path2 = input("Enter the path to where you want to record the json file :\n")

# Export of the json file
with open(path2 + 'data.json', 'w') as mon_fichier:
	json.dump(export, mon_fichier)
print("json file exported with success")

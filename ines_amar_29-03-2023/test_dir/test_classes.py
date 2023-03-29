
import unittest


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



class TestCandidature(unittest.TestCase):
    def setUp(self):
        self.l = Logement("1000", "Paris", "3", "30", "Appartement")
        self.a = Annonce("Bien'Ici", "Avesia", self.l)
        self.c = Candidature("test@gmail.com", "0612345678", "01-01-2023 13h12", self.a, "locataire")
        
    def test_logement_is_instanceof_logement(self):
        self.assertIsInstance(self.l, Logement)
    
    def test_annnonce_is_instanceof_annonce(self):
        self.assertIsInstance(self.a, Annonce)
    
    def test_candidature_is_instanceof_candidature(self):
        self.assertIsInstance(self.c, Candidature)
    

if __name__ == '__main__':
    unittest.main()

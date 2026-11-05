import requests

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

API_URL = "http://127.0.0.1:8000/rendezvous/"

class GestionRendezVous(App):
    def build(self):


        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        titre = Label(
            text="GESTION DEQ RENDZ-VOUS",
            font_size=24,
            size_hint_y=None,
            height=60
        )

        layout.add_widget(titre)

        self.nom = TextInput(
            hint_text="Nom du client",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        self.date = TextInput(
            hint_text="Date (AAAA-MM-JJ)",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        layout.add_widget(self.nom)
        layout.add_widget(self.date)
        layout.add_widget(self.heure)
        layout.add_widget(self.motif)

        #bouton ajouter
        btn_ajouter = Button(
            text="Ajouter un rendez-vous",
            size_hint_y=None,
            height=50
        )

        btn_ajouter.bind(on_press=self.ajouter)
        layout.add_widget(btn_ajouter)

        #bouton afficher
        btn_afficher = Button(
            text="Afficher les rendez-vous",
            size_hint_y=None,
            height=50
        )

        btn_afficher.bind(on_press=self.afficher)
        layout.add_widget(btn_afficher)

        #affichage

        scroll = ScrollView()

        self.resultat = Label(
            text="Aucun rendez-vous",
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        self.resultat.bind(
            texture_size=self.resultat.setter("size")
        )

        scroll.add_widget(self.resultat)
        layout.add_widget(scroll)

        return layout

    #Ajouter un rendez-vous
    def ajouter(self, instance):

        donnees = {
            "nom": self.nom.text,
            "date": self.date.text,
            "heure": self.heure.text,
            "motif": self.motif.text
        }

        if not all(donnees.values()):
            self.resultat.text = "veuillez remplir tous les champs "
            return

        try:

            reponse = requests.post(
                API_URL,
                json=donnees,
                timeout=5
            )

            if reponse.status_code == 200:
                self.resultat.text = "Rendez-vous ajouté avec succès !"

                self.nom.text = ""
                self.date.text = ""
                self.heure.text = ""
                self.motif.text = ""

            else:
                self.resultat.text = "Erreur lors de l'ajout."

        except requests.exceptions.RequestsException as e:
            self.resultat.text = f"Erreur de connexion : {e}"

    #Afficher les rendez-vous                    
    def afficher(self, instance):

        try:
            reponse = requests.get(API_URL, timeout=5)

            if reponse.status_code == 200:
                rendezvous = reponse.json()

                if reponse.status_code == 200:
                    self.resultat.text = "Aucun rendez-vous enregistré."
                else:
                    texte = ""

                    for rdv in rendezvous:
                        texte += (
                            f"ID : {rdv['id']}\n"
                            f"Nom : {rdv['nom']}\n"
                            f"Date : {rdv['date']}\n"
                            f"Heure : {rdv['heure']}\n"
                            f"Motif : {rdv['motif']}\n"
                            "-------------------------\n"

                        )   
                    
                    self.resultat.text = texte     

            else:
                self.resultat.text = "Erreur lors de l'affichage."

        except requests.exceptions.RequestsException as e:
            self.resultat.text = f"Erreur de connexion : {e}"

    if __name__ == "_main_":
    GestionRendezVous().run                    
                



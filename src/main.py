"""
Interface graphique Tkinter et orchestrateur de jeu pour le Puissance 4.
"""

import os
import sys

# Injection propre du dossier src dans le chemin de recherche des modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from constantes import COMBINAISONS_GAGNANTES
from gestion_minimax import minimax, trouver_ligne_basse_simulation


class Cellule:
    """Représente une case individuelle du plateau liée à un bouton Tkinter."""

    def __init__(self, indice, action_joueur):
        self.indice = indice
        self.bouton = tk.Button(
            text='', font=('Arial', 24, 'bold'), width=4, height=1,
            bg='#a19ea1', command=lambda: action_joueur(self)
        )

    def effectuer_action(self, joueur_actuel, annonceur, verifier_fin):
        """Met à jour l'apparence de la case et retourne l'état de la partie après le coup."""
        nom_joueur_texte = "Rouge" if joueur_actuel == 'X' else "Jaune"

        if annonceur.cget('text').startswith(f"Joueur {nom_joueur_texte}") and not self.bouton.cget('text'):
            couleur_pion = "#F12922" if joueur_actuel == 'X' else "#FFED00"
            self.bouton.config(text=joueur_actuel, bg=couleur_pion, fg=couleur_pion, relief='flat')

            resultat_fin = verifier_fin()
            if resultat_fin == "victoire":
                annonceur.config(text=f"Victoire du joueur {nom_joueur_texte}", fg=couleur_pion)
                return "fin"
            elif resultat_fin == "egalite":
                annonceur.config(text="Fin de partie : égalité", fg='black')
                return "fin"
            else:
                prochain_joueur = 'O' if joueur_actuel == 'X' else 'X'
                prochain_nom = "Jaune" if prochain_joueur == 'O' else "Rouge"
                prochaine_couleur = "#FFED00" if prochain_joueur == 'O' else "#F12922"
                annonceur.config(text=f"Joueur {prochain_nom} à votre tour", fg=prochaine_couleur)
                return "continue"
        return "invalide"


class Puissance4:
    """Contrôleur principal gérant l'état du jeu, les tours et l'interface."""

    def __init__(self, root):
        self.root = root
        self.mode_bot = False
        self.root.title("Puissance 4 - Minimax")
        self.root.configure(bg="#ffffff")

        # Variables d'état de jeu
        self.joueur_actuel = 'X'
        self.joueur_demarrage = 'X'
        self.partie_terminee = False
        self.victoires_x = 0
        self.victoires_o = 0
        self.egalites = 0

        # Raccourcis clavier
        self.root.bind("<r>", lambda event: self.nouvelle_partie())
        self.root.bind("<Escape>", lambda event: self.root.quit())

        # Bannière d'état
        self.annonceur = tk.Label(root, text="Joueur Rouge à votre tour", font=('Arial', 16, 'italic'), bg="#d1d1d1")

        # Grille de jeu (7 colonnes x 6 lignes = 42 cellules)
        self.zone_jeu = tk.Frame(root, bg='#0052cc', padx=10, pady=10)
        self.cellules = []
        for i in range(42):
            cellule = Cellule(i, self.jouer_tour)
            cellule.bouton.grid(row=i // 7, column=i % 7, padx=5, pady=5, in_=self.zone_jeu)
            self.cellules.append(cellule)

        # Contrôles de jeu
        self.bouton_rejouer = tk.Button(root, text="Rejouer", command=self.nouvelle_partie, bg='yellow', font=('Arial', 12, 'bold'))
        self.bouton_reset_score = tk.Button(root, text="Réinitialiser le score", command=self.reinitialiser_scores, bg='#66b3ff', font=('Arial', 12, 'bold'))
        self.bouton_quitter = tk.Button(root, text="Quitter", command=root.quit, bg='red', font=('Arial', 12, 'bold'))
        self.bouton_menu = tk.Button(root, text="Menu", command=self.retour_menu, bg='orange', font=('Arial', 12, 'bold'))

        # Compteurs de scores
        self.compteur_x = tk.Label(root, text="Victoires Rouge : 0", font=('Arial', 12, "bold"), fg='black', bg="#F12922")
        self.compteur_o = tk.Label(root, text="Victoires Jaune : 0", font=('Arial', 12, "bold"), fg='black', bg="#f3db00")
        self.compteur_egalite = tk.Label(root, text="Égalités : 0", font=('Arial', 12, "bold"), fg='black', bg="#e0dde0")

        self.afficher_menu()
        self.root.configure(bg="#a19ea1")

    def afficher_menu(self):
        """Masque l'interface de jeu et affiche l'écran d'accueil."""
        self.zone_jeu.pack_forget()
        self.compteur_egalite.pack_forget()
        self.compteur_o.pack_forget()
        self.compteur_x.pack_forget()
        self.bouton_reset_score.pack_forget()
        self.bouton_rejouer.pack_forget()
        self.bouton_menu.pack_forget()
        self.bouton_quitter.pack_forget()
        self.annonceur.pack_forget()

        self.home_page = tk.Frame(self.root, bg='#a19ea1')
        self.home_page.pack(pady=20)

        tk.Label(self.home_page, text="Choisissez le mode de jeu", font=('Arial', 18), bg="#a19ea1").pack(pady=10)
        tk.Button(self.home_page, text="jouer contre un ami", command=self.lancer_1v1).pack(fill='x', pady=5, padx=10)
        tk.Button(self.home_page, text="jouer contre une ia", command=self.lancer_bot).pack(fill='x', pady=5, padx=10)
        tk.Button(self.home_page, text="Quitter", bg='red', fg='white', font=('Arial', 10, 'bold'), command=self.root.quit).pack(fill='x', pady=10, padx=10)

    def afficher_interface_jeu(self):
        """Affiche les éléments interactifs du plateau et de commande."""
        self.annonceur.pack(pady=10)
        self.zone_jeu.pack()
        self.bouton_rejouer.pack(side='left', padx=10, pady=10)
        self.bouton_reset_score.pack(side='left', padx=10, pady=10)
        self.bouton_quitter.pack(side='right', padx=10, pady=10)
        self.bouton_menu.pack(side='right', padx=10, pady=10)
        self.compteur_x.pack(side='left', padx=10)
        self.compteur_o.pack(side='left', padx=10)
        self.compteur_egalite.pack(side='left', padx=10)

    def lancer_bot(self):
        """Initialise une partie en mode Joueur contre Minimax."""
        self.mode_bot = True
        self.home_page.pack_forget()
        self.afficher_interface_jeu()
        self.joueur_demarrage = 'X'
        self.nouvelle_partie()

    def lancer_1v1(self):
        """Initialise une partie en mode deux joueurs local."""
        self.mode_bot = False
        self.home_page.pack_forget()
        self.afficher_interface_jeu()
        self.joueur_demarrage = 'X'
        self.nouvelle_partie()

    def nouvelle_partie(self):
        """Réinitialise la grille et alterne le joueur de départ."""
        self.partie_terminee = False
        self.joueur_actuel = self.joueur_demarrage
        self.joueur_demarrage = 'O' if self.joueur_demarrage == 'X' else 'X'

        couleur_pion = "#F12922" if self.joueur_actuel == 'X' else "#FFED00"
        nom_couleur = "Rouge" if self.joueur_actuel == 'X' else "Jaune"

        for cellule in self.cellules:
            cellule.bouton.config(text='', fg='black', bg="#e6e6e6")

        self.annonceur.config(text=f"Joueur {nom_couleur} à votre tour", fg=couleur_pion)

        # Déclenchement automatique si le bot commence
        if self.joueur_actuel == 'O' and self.mode_bot:
            self.root.after(500, self.choisir_meilleur_score)

    def retour_menu(self):
        """Retourne au menu principal en masquant l'interface de jeu."""
        self.zone_jeu.pack_forget()
        self.annonceur.pack_forget()
        self.bouton_rejouer.pack_forget()
        self.bouton_reset_score.pack_forget()
        self.bouton_menu.pack_forget()
        self.bouton_quitter.pack_forget()
        self.compteur_x.pack_forget()
        self.compteur_o.pack_forget()
        self.compteur_egalite.pack_forget()
        self.home_page.pack(pady=20)

    def reinitialiser_scores(self):
        """Remet l'ensemble des scores à zéro."""
        self.victoires_x = 0
        self.victoires_o = 0
        self.egalites = 0
        self.compteur_x.config(text="Victoires Rouge : 0")
        self.compteur_o.config(text="Victoires Jaune : 0")
        self.compteur_egalite.config(text="Égalités : 0")
        self.annonceur.config(text="Scores remis à zéro !", fg='black')

    def trouver_ligne_basse(self, colonne):
        """Trouve la ligne la plus basse disponible sur le plateau réel Tkinter."""
        for ligne in range(5, -1, -1):
            indice = ligne * 7 + colonne
            if self.cellules[indice].bouton.cget('text') == "":
                return indice
        return None

    def jouer_tour(self, cellule):
        """Traite le coup sélectionné par l'utilisateur et déclenche l'IA si nécessaire."""
        if self.partie_terminee:
            return

        colonne = cellule.indice % 7
        position = self.trouver_ligne_basse(colonne)

        if position is not None:
            position_cellule = self.cellules[position]
            etat_coup = position_cellule.effectuer_action(self.joueur_actuel, self.annonceur, self.verifier_fin)

            if etat_coup == "fin":
                self.partie_terminee = True
                return

            if etat_coup == "continue":
                self.joueur_actuel = 'O' if self.joueur_actuel == 'X' else 'X'
                if self.joueur_actuel == 'O' and self.mode_bot and not self.partie_terminee:
                    self.root.after(500, self.choisir_meilleur_score)

    def verifier_fin(self):
        """Vérifie la présence d'un alignement de 4 pions ou d'un match nul."""
        for combo in COMBINAISONS_GAGNANTES:
            if (self.cellules[combo[0]].bouton.cget('text') == self.joueur_actuel ==
                self.cellules[combo[1]].bouton.cget('text') == self.joueur_actuel ==
                self.cellules[combo[2]].bouton.cget('text') == self.joueur_actuel ==
                self.cellules[combo[3]].bouton.cget('text') == self.joueur_actuel):

                for i in combo:
                    self.cellules[i].bouton.config(bg='green', fg="green")

                if self.joueur_actuel == 'X':
                    self.victoires_x += 1
                    self.compteur_x.config(text=f"Victoires Rouge : {self.victoires_x}")
                else:
                    self.victoires_o += 1
                    self.compteur_o.config(text=f"Victoires Jaune : {self.victoires_o}")
                return "victoire"

        if all(cellule.bouton.cget('text') != '' for cellule in self.cellules):
            self.egalites += 1
            self.compteur_egalite.config(text=f"Égalités : {self.egalites}")
            return "egalite"

        return None

    def recuperer_etat_plateau(self):
        """Extrait l'état courant de la grille sous forme d'une liste de chaînes."""
        etat_plateau = []
        for i in range(len(self.cellules)):
            etat_plateau.append(self.cellules[i].bouton.cget('text'))
        return etat_plateau

    def choisir_meilleur_score(self):
        """Évalue tous les coups légaux possibles et exécute le choix optimal via Minimax."""
        if self.partie_terminee:
            return

        etat_plateau = self.recuperer_etat_plateau()
        meilleur_score = -float('inf')
        meilleur_colonne = 3

        for i in [3, 2, 4, 1, 5, 0, 6]:
            ligne_vide = trouver_ligne_basse_simulation(etat_plateau, i)
            if ligne_vide is not None:
                etat_plateau[ligne_vide] = "O"
                score = minimax(etat_plateau, 0, -float('inf'), float('inf'), False)
                etat_plateau[ligne_vide] = ""

                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_colonne = i

        self.jouer_tour(self.cellules[meilleur_colonne])


if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = Puissance4(fenetre)
    fenetre.mainloop()
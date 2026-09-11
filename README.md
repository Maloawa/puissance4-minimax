# Puissance 4 — Jeu Python & Bot Minimax (Alpha-Bêta)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Interface](https://img.shields.io/badge/Interface-Tkinter-orange)
![Algorithme](https://img.shields.io/badge/Algorithme-Minimax%20Alpha--Beta-green)

Projet de Puissance 4 développé en Python avec une interface graphique Tkinter. Le jeu permet d'affronter un autre joueur en local ou de jouer contre un bot basé sur l'algorithme Minimax optimisé par élagage Alpha-Bêta.

---

## Aperçu du jeu

![Capture d'écran du Puissance 4](assets/demo.png)

---

## Fonctionnalités

* **2 modes de jeu :** Joueur contre Joueur (local) ou Joueur contre Ordinateur (Bot).
* **Interface Tkinter :** Grille interactive, gestion de la gravité des pions, affichage du tour et détection automatique des victoires ou égalités.
* **Gestion des scores :** Compteur de victoires pour chaque joueur et suivi des égalités.
* **Architecture modulaire :** Séparation du code entre les constantes, l'algorithme de décision et l'interface graphique.

---

## Fonctionnement du Bot

Pour déterminer le coup optimal, le bot simule les prochains tours via un arbre de jeu :

* **Minimax (profondeur 5) :** Analyse les coups possibles jusqu'à 5 coups d'avance en cherchant à maximiser le gain du bot face aux meilleures réponses adverses.
* **Élagage Alpha-Bêta :** Stoppe l'exploration des branches dès qu'une option s'avère moins avantageuse qu'un coup déjà validé, assurant une réponse fluide sans temps d'attente.
* **Ordre de test des colonnes :** Analyse prioritaire du centre vers les bords (`[3, 2, 4, 1, 5, 0, 6]`) pour déclencher un maximum de coupes Alpha-Bêta rapides.
* **Fonction d'évaluation :**
  * Une grille de pondération favorise le contrôle des cases centrales.
  * Détection tactique des alignements de 3 pions pour concrétiser une victoire (+100 points) ou bloquer immédiatement l'adversaire (-150 points).

---

## Installation et lancement

### Prérequis

* Python 3.10 ou supérieur.
* `tkinter` (intégré par défaut sous Windows et macOS).

### Démarrage

Cloner le dépôt et lancer le jeux : 
   ```bash
   git clone [https://github.com/TON-PSEUDO/puissance-4-ia.git](https://github.com/TON-PSEUDO/puissance-4-ia.git)
   cd puissance-4-ia 
   python src/main.py
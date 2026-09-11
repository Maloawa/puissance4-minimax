"""
Moteur de décision automatisé : algorithme Minimax avec élagage Alpha-Bêta
et fonction d'évaluation heuristique.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constantes import COMBINAISONS_GAGNANTES, MATRICE_POINTS


def trouver_ligne_basse_simulation(plateau_simule, colonne):
    """
    Identifie l'indice le plus bas disponible dans une colonne (gravité).
    Retourne l'indice (0-41) ou None si la colonne est pleine.
    """
    for ligne in range(5, -1, -1):
        indice = ligne * 7 + colonne
        if plateau_simule[indice] == "":
            return indice
    return None


def evaluer_victoire(plateau, joueur):
    """Vérifie si le joueur spécifié ('X' ou 'O') possède un alignement gagnant."""
    for combo in COMBINAISONS_GAGNANTES:
        if plateau[combo[0]] == plateau[combo[1]] == plateau[combo[2]] == plateau[combo[3]] == joueur != "":
            return True
    return False


def evaluer_plateau(plateau):
    """
    Heuristique évaluant un état non terminal du plateau :
    1. Score de position basé sur la matrice de contrôle spatial.
    2. Bonus/malus tactiques sur les menaces d'alignement direct de 3 pions.
    """
    score = 0
    for i in range(42):
        if plateau[i] == 'O':
            score += MATRICE_POINTS[i]
        elif plateau[i] == 'X':
            score -= MATRICE_POINTS[i]

    for combo in COMBINAISONS_GAGNANTES:
        pions = [plateau[i] for i in combo]
        bot = pions.count('O')
        humain = pions.count('X')
        vide = pions.count('')

        if bot == 3 and vide == 1:
            score += 100  # Menace d'alignement favorable au bot
        elif humain == 3 and vide == 1:
            score -= 150  # Blocage défensif prioritaire

    return score


def minimax(plateau, profondeur, alpha, beta, est_max):
    """
    Recherche arborescente Minimax bornée en profondeur (d=5)
    avec coupes Alpha-Bêta pour optimiser l'espace d'exploration.
    """
    # Conditions d'arrêt : victoire, défaite ou match nul
    if evaluer_victoire(plateau, 'O'):
        return 10000 - profondeur
    if evaluer_victoire(plateau, 'X'):
        return -10000 + profondeur
    if "" not in plateau:
        return 0

    # Limite de profondeur atteinte : recours à l'heuristique
    if profondeur >= 5:
        return evaluer_plateau(plateau)

    # Heuristique d'ordonnancement : tester le centre en premier maximise les coupes
    colonnes_ordre = [3, 2, 4, 1, 5, 0, 6]

    if est_max:
        meilleur_score = -float('inf')
        for i in colonnes_ordre:
            ligne_vide = trouver_ligne_basse_simulation(plateau, i)
            if ligne_vide is not None:
                plateau[ligne_vide] = 'O'
                score = minimax(plateau, profondeur + 1, alpha, beta, False)
                plateau[ligne_vide] = ""

                meilleur_score = max(score, meilleur_score)
                alpha = max(alpha, meilleur_score)
                if beta <= alpha:
                    break  # Élagage Alpha : branche inutile pour Min
        return meilleur_score

    else:
        pire_score = float('inf')
        for i in colonnes_ordre:
            ligne_vide = trouver_ligne_basse_simulation(plateau, i)
            if ligne_vide is not None:
                plateau[ligne_vide] = "X"
                score = minimax(plateau, profondeur + 1, alpha, beta, True)
                plateau[ligne_vide] = ""

                pire_score = min(score, pire_score)
                beta = min(beta, pire_score)
                if beta <= alpha:
                    break  # Élagage Bêta : branche inutile pour Max
        return pire_score
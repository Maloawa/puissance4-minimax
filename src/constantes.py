"""
Définition des constantes et de la configuration du plateau de jeu.
"""

def generer_combinaisons_gagnantes():
    """
    Calcule l'ensemble des 69 combinaisons gagnantes possibles (4 pions alignés)
    sur une grille de dimensions 7x6 (lignes, colonnes et diagonales).
    """
    combos = []
    # Lignes
    for i in range(6):
        for j in range(4):
            combos.append([j + i * 7, (j + 1) + i * 7, (j + 2) + i * 7, (j + 3) + i * 7])

    # Colonnes
    for i in range(3):
        for j in range(7):
            combos.append([j + i * 7, j + (1 + i) * 7, j + (2 + i) * 7, j + (3 + i) * 7])

    # Diagonales descendantes (\)
    for i in range(3):
        for j in range(4):
            combos.append([j + i * 7, (j + i * 7) + 8, (j + i * 7) + 2 * 8, (j + i * 7) + 3 * 8])

    # Diagonales montantes (/)
    for i in range(3):
        for j in range(3, 7):
            combos.append([j + i * 7, (j + i * 7) + 6, (j + i * 7) + 2 * 6, (j + i * 7) + 3 * 6])

    return combos


COMBINAISONS_GAGNANTES = generer_combinaisons_gagnantes()

# Matrice de pondération statique : favorise l'occupation tactique du centre du plateau
MATRICE_POINTS = [
    3, 4, 5, 7, 5, 4, 3,
    4, 6, 8, 10, 8, 6, 4,
    5, 8, 11, 14, 11, 8, 5,
    5, 8, 11, 14, 11, 8, 5,
    4, 6, 8, 10, 8, 6, 4,
    3, 4, 5, 7, 5, 4, 3
]
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
JOUR 2 : NumPy — Calculs vectorisés et statistiques
Résumé complet et commenté
================================================================================
Ce script reprend l'ensemble des concepts vus au Jour 2 :
  2.1 Opérations universelles (ufuncs)
  2.2 Agrégations
  2.3 Opérations booléennes et ensembles
  2.4 Diffusions (broadcasting)
  2.5 Algèbre linéaire
  2.6 Génération aléatoire
"""

import numpy as np

# ==============================================================================
# 2.1 OPÉRATIONS UNIVERSELLES (ufuncs)
# ==============================================================================
print("=" * 70)
print("2.1 OPÉRATIONS UNIVERSELLES (ufuncs)")
print("=" * 70)

a = np.array([1, 2, 3, 4])
b = np.array([10, 10, 10, 10])

print(f"a = {a}")
print(f"b = {b}")
print(f"\nnp.add(a, b)       = {np.add(a, b)}       (a + b)")
print(f"np.subtract(a, b)  = {np.subtract(a, b)}   (a - b)")
print(f"np.multiply(a, b)  = {np.multiply(a, b)}   (a * b)")
print(f"np.divide(a, b)    = {np.divide(a, b)}     (a / b)")
print(f"np.power(a, 2)     = {np.power(a, 2)}       (a ** 2)")
print(f"np.mod(a, 3)       = {np.mod(a, 3)}         (a % 3)")
print(f"np.sqrt(a)         = {np.sqrt(a)}")
print(f"np.exp(a)          = {np.exp(a)}")
print(f"np.log(a)          = {np.log(a)}           (naturel)")
print(f"np.log10(a)        = {np.log10(a)}          (base 10)")
print(f"np.log2(a)         = {np.log2(a)}           (base 2)")

# Paramètre out (optimisation mémoire)
print(f"\n--- Paramètre out ---")
result = np.empty_like(a, dtype=float)
np.sqrt(a.astype(float), out=result)
print(f"sqrt avec out=result : {result}")

# Paramètre where (calcul conditionnel)
print(f"\n--- Paramètre where ---")
arr = np.array([1, 4, 9, 16, 25], dtype=float)
res_where = np.sqrt(arr, where=arr > 4)
print(f"sqrt(where=arr>4) : {res_where}")
print(f"  (valeurs <=4 non initialisées)")


# ==============================================================================
# 2.2 AGRÉGATIONS
# ==============================================================================
print("\n" + "=" * 70)
print("2.2 AGRÉGATIONS")
print("=" * 70)

mat = np.array([[1, 2, 3],
                [4, 5, 6]])
print(f"Matrice :\n{mat}")
print(f"\nnp.sum(mat)           = {np.sum(mat)}          (total)")
print(f"np.sum(mat, axis=0)   = {np.sum(mat, axis=0)}   (par colonne)")
print(f"np.sum(mat, axis=1)   = {np.sum(mat, axis=1)}   (par ligne)")
print(f"np.prod(mat)          = {np.prod(mat)}")
print(f"np.mean(mat)          = {np.mean(mat)}")
print(f"np.std(mat)           = {np.std(mat):.4f}")
print(f"np.var(mat)           = {np.var(mat):.4f}")
print(f"np.min(mat)           = {np.min(mat)}")
print(f"np.max(mat)           = {np.max(mat)}")
print(f"np.argmin(mat)        = {np.argmin(mat)}         (indice aplati)")
print(f"np.argmax(mat)        = {np.argmax(mat)}         (indice aplati)")
print(f"np.median(mat)        = {np.median(mat)}")
print(f"np.percentile(mat, 25)= {np.percentile(mat, 25)}")
print(f"np.percentile(mat,[25,50,75]) = {np.percentile(mat, [25, 50, 75])}")

# keepdims
print(f"\n--- keepdims ---")
sum_keep = np.sum(mat, axis=1, keepdims=True)
print(f"sum(axis=1, keepdims=True) : shape {sum_keep.shape}\n{sum_keep}")

# Méthodes vs fonctions
print(f"\n--- Méthodes ---")
print(f"mat.sum(axis=0)  = {mat.sum(axis=0)}")
print(f"mat.mean()       = {mat.mean()}")
print(f"mat.std(ddof=1)  = {mat.std(ddof=1):.4f}  (échantillon, ddof=1)")

# Gestion des NaN
arr_nan = np.array([1.0, 2.0, np.nan, 4.0])
print(f"\nAvec NaN : {arr_nan}")
print(f"np.mean(arr_nan)     = {np.mean(arr_nan)}  (NaN !)")
print(f"np.nanmean(arr_nan)  = {np.nanmean(arr_nan)}  (ignore NaN)")
print(f"np.nansum(arr_nan)   = {np.nansum(arr_nan)}")


# ==============================================================================
# 2.3 OPÉRATIONS BOOLÉENNES ET ENSEMBLES
# ==============================================================================
print("\n" + "=" * 70)
print("2.3 OPÉRATIONS BOOLÉENNES ET ENSEMBLES")
print("=" * 70)

x = np.array([True, False, True, False])
y = np.array([True, True, False, False])
print(f"x = {x}")
print(f"y = {y}")
print(f"logical_and = {np.logical_and(x, y)}")
print(f"logical_or  = {np.logical_or(x, y)}")
print(f"logical_not = {np.logical_not(x)}")
print(f"logical_xor = {np.logical_xor(x, y)}")

# any / all
nums = np.array([0, 1, 2, 3])
print(f"\nnums = {nums}")
print(f"np.any(nums > 2)  = {np.any(nums > 2)}")
print(f"np.all(nums > 0)  = {np.all(nums > 0)}")
print(f"np.any(nums == 0) = {np.any(nums == 0)}")

# Ensembles
A = np.array([1, 2, 3, 4, 5, 5, 3])
B = np.array([4, 5, 6, 7, 8])
print(f"\nA = {A}")
print(f"B = {B}")
print(f"np.unique(A)         = {np.unique(A)}")
print(f"np.intersect1d(A,B)  = {np.intersect1d(A, B)}")
print(f"np.union1d(A,B)      = {np.union1d(A, B)}")
print(f"np.setdiff1d(A,B)    = {np.setdiff1d(A, B)}   (dans A, pas dans B)")


# ==============================================================================
# 2.4 DIFFUSIONS (broadcasting)
# ==============================================================================
print("\n" + "=" * 70)
print("2.4 DIFFUSIONS (broadcasting)")
print("=" * 70)

# Exemple 1 : matrice (3,3) + vecteur (3,)
M = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
v = np.array([10, 20, 30])
print(f"M (3x3) :\n{M}")
print(f"v (3,)  : {v}")
print(f"M + v   :\n{M + v}")
print(f"  (v est diffusé en 3 lignes identiques)")

# Exemple 2 : colonne (3,1) + ligne (1,3)
col = np.array([[1], [2], [3]])      # shape (3, 1)
ligne = np.array([10, 20, 30])       # shape (3,) → broadcast (1, 3)
print(f"\ncol (3,1)   :\n{col}")
print(f"ligne (3,)   : {ligne}")
print(f"col + ligne  :\n{col + ligne}")
print(f"  (diffusion en grille 3x3)")

# Exemple 3 : échelle par colonne
mat = np.ones((4, 3))
facteurs = np.array([2, 3, 4])
print(f"\nmat (4x3) de 1 :\n{mat}")
print(f"facteurs : {facteurs}")
print(f"mat * facteurs :\n{mat * facteurs}")


# ==============================================================================
# 2.5 ALGÈBRE LINÉAIRE
# ==============================================================================
print("\n" + "=" * 70)
print("2.5 ALGÈBRE LINÉAIRE")
print("=" * 70)

A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])
print(f"A =\n{A}")
print(f"B =\n{B}")

# Produit matriciel
print(f"\nnp.dot(A, B)    =\n{np.dot(A, B)}")
print(f"A @ B           =\n{A @ B}")
print(f"np.matmul(A, B) =\n{np.matmul(A, B)}")

# Inversion et déterminant
print(f"\nnp.linalg.inv(A) =\n{np.linalg.inv(A)}")
print(f"np.linalg.det(A) = {np.linalg.det(A):.4f}")

# Valeurs et vecteurs propres
vals, vecs = np.linalg.eig(A)
print(f"\nValeurs propres  : {vals}")
print(f"Vecteurs propres :\n{vecs}")
print(f"  (chaque COLONNE est un vecteur propre)")

# Résolution de système linéaire : A·x = b
A_sys = np.array([[3, 1],
                  [1, 2]], dtype=float)
b_sys = np.array([9, 8], dtype=float)
x = np.linalg.solve(A_sys, b_sys)
print(f"\nRésolution A·x = b")
print(f"A =\n{A_sys}")
print(f"b = {b_sys}")
print(f"x = {x}")
print(f"Vérification A@x = {A_sys @ x}")

# Normes et trace
print(f"\nNorme de Frobenius : {np.linalg.norm(A):.4f}")
print(f"Norme L1 de [3,-4] : {np.linalg.norm([3, -4], ord=1):.4f}")
print(f"Norme L2 de [3,-4] : {np.linalg.norm([3, -4], ord=2):.4f}")
print(f"Norme infinie      : {np.linalg.norm([3, -4], ord=np.inf):.4f}")
print(f"Trace de A         : {np.trace(A)}")


# ==============================================================================
# 2.6 GÉNÉRATION ALÉATOIRE
# ==============================================================================
print("\n" + "=" * 70)
print("2.6 GÉNÉRATION ALÉATOIRE")
print("=" * 70)

# API moderne avec Generator
rng = np.random.default_rng(seed=42)

print("--- API moderne (recommandée) ---")
print(f"random(5)        : {rng.random(5)}")
print(f"integers(0,10,5) : {rng.integers(0, 10, 5)}")
print(f"normal(0,1,5)    : {rng.normal(0, 1, 5)}")
print(f"uniform(0,1,5)   : {rng.uniform(0, 1, 5)}")

# choice avec probabilités
options = np.array([10, 20, 30, 40])
probas = np.array([0.5, 0.3, 0.15, 0.05])
print(f"\nchoice([10,20,30,40], p=[0.5,0.3,0.15,0.05], size=10) :")
print(f"  {rng.choice(options, size=10, p=probas)}")

# shuffle vs permutation
seq = np.array([1, 2, 3, 4, 5])
print(f"\nOriginal      : {seq}")
print(f"permutation   : {rng.permutation(seq)}  (nouveau tableau)")
print(f"Original reste: {seq}")
rng.shuffle(seq)
print(f"après shuffle : {seq}  (modifié en place)")

# Distributions
print(f"\n--- Distributions ---")
print(f"binomial(n=10,p=0.5)  : {rng.binomial(10, 0.5, 5)}")
print(f"poisson(lam=3)        : {rng.poisson(3, 5)}")
print(f"exponential(scale=1)  : {rng.exponential(1, 5)}")

# Ancienne API (toujours fonctionnelle)
print(f"\n--- Ancienne API ---")
np.random.seed(42)
print(f"np.random.rand(3)     : {np.random.rand(3)}")
print(f"np.random.randn(3)    : {np.random.randn(3)}")
print(f"np.random.randint(0,10,5): {np.random.randint(0, 10, 5)}")

print("\n" + "=" * 70)
print("FIN DU JOUR 2 — Résumé exécuté avec succès !")
print("=" * 70)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
JOUR 1 : NumPy — Les fondations (tableaux et opérations de base)
Résumé complet et commenté
================================================================================
Ce script reprend l'ensemble des concepts vus au Jour 1 :
  1.1 Création de tableaux
  1.2 Types de données (dtype)
  1.3 Indexation et slicing
  1.4 Manipulation de forme
  1.5 Copie vs Vue
  1.6 Concaténation et split

Exécutez-le section par section pour observer les résultats.
"""

import numpy as np

# ==============================================================================
# 1.1 CRÉATION DE TABLEAUX
# ==============================================================================
print("=" * 70)
print("1.1 CRÉATION DE TABLEAUX")
print("=" * 70)

# np.array() — conversion d'une séquence Python en ndarray
# Paramètres clés : object, dtype, copy, order, ndmin
arr_liste = [1, 2, 3, 4, 5]
a = np.array(arr_liste)
print(f"np.array([1,2,3,4,5])         : {a}")
print(f"  dtype={a.dtype}, shape={a.shape}, ndim={a.ndim}, size={a.size}")

# Avec dtype et ndmin
b = np.array([1, 2, 3], dtype=float, ndmin=2)
print(f"\nAvec dtype=float, ndmin=2     : {b}")
print(f"  shape={b.shape}, ndim={b.ndim}")

# np.zeros() — tableau de 0
z = np.zeros((2, 3))
print(f"\nnp.zeros((2, 3))              :\n{z}")

# np.ones() — tableau de 1
o = np.ones((2, 3), dtype=int)
print(f"\nnp.ones((2, 3), dtype=int)    :\n{o}")

# np.empty() — mémoire non initialisée (vite, mais valeurs indéterminées)
e = np.empty((2, 2))
print(f"\nnp.empty((2, 2))              :\n{e}")

# np.full() — valeur constante
f = np.full((2, 3), 7)
print(f"\nnp.full((2, 3), 7)            :\n{f}")

# np.arange() — séquence d'entiers (stop EXCLU)
r = np.arange(0, 10, 2)
print(f"\nnp.arange(0, 10, 2)           : {r}")

# np.linspace() — valeurs uniformément espacées (stop INCLUS par défaut)
l = np.linspace(0, 1, 5)
print(f"\nnp.linspace(0, 1, 5)          : {l}")
l2 = np.linspace(0, 1, 5, endpoint=False)
print(f"np.linspace(0, 1, 5, endpoint=False) : {l2}")

# np.logspace() — espacement logarithmique (base 10 par défaut)
lg = np.logspace(0, 2, 3)
print(f"\nnp.logspace(0, 2, 3)          : {lg}")

# np.eye() — matrice identité avec diagonale décalable
i = np.eye(3)
print(f"\nnp.eye(3)                     :\n{i}")
i2 = np.eye(3, k=1)
print(f"np.eye(3, k=1)                :\n{i2}")

# np.identity() — identité carrée uniquement
id_mat = np.identity(3, dtype=int)
print(f"\nnp.identity(3, dtype=int)     :\n{id_mat}")

# np.diag() — création ou extraction de diagonale
d = np.diag([1, 2, 3])
print(f"\nnp.diag([1, 2, 3])            :\n{d}")
extract = np.diag([[1, 2], [3, 4]])
print(f"np.diag([[1,2],[3,4]])        : {extract}")

# Attributs fondamentaux
sample = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n--- Attributs de ndarray ---")
print(f"Tableau :\n{sample}")
print(f"  dtype     = {sample.dtype}    (type des éléments)")
print(f"  shape     = {sample.shape}       (dimensions)")
print(f"  ndim      = {sample.ndim}        (nombre de dimensions)")
print(f"  size      = {sample.size}        (nombre total d'éléments)")
print(f"  itemsize  = {sample.itemsize} octets  (taille d'un élément)")
print(f"  nbytes    = {sample.nbytes} octets  (taille totale en mémoire)")


# ==============================================================================
# 1.2 TYPES DE DONNÉES (dtype)
# ==============================================================================
print("\n" + "=" * 70)
print("1.2 TYPES DE DONNÉES (dtype)")
print("=" * 70)

# Types entiers
i8 = np.array([1, 2], dtype=np.int8)
i32 = np.array([1, 2], dtype=np.int32)
i64 = np.array([1, 2], dtype=np.int64)
print(f"int8  : {i8.dtype}, itemsize={i8.itemsize}")
print(f"int32 : {i32.dtype}, itemsize={i32.itemsize}")
print(f"int64 : {i64.dtype}, itemsize={i64.itemsize}")

# Types flottants
f16 = np.array([1.0], dtype=np.float16)
f64 = np.array([1.0], dtype=np.float64)
print(f"\nfloat16 : {f16.dtype}, itemsize={f16.itemsize}")
print(f"float64 : {f64.dtype}, itemsize={f64.itemsize}")

# Booléens
bl = np.array([True, False, 1, 0], dtype=bool)
print(f"\nbool : {bl}")

# astype() — conversion de type (retourne une copie)
original = np.array([1.5, 2.7, 3.9])
converti = original.astype(int)
print(f"\nastype() : {original} -> {converti} (tronquature !)")
converti_f32 = original.astype(np.float32)
print(f"astype(np.float32) : {converti_f32.dtype}")

# Ordre des octets
print(f"\nOrdre des octets : {np.array([1]).dtype.str}")


# ==============================================================================
# 1.3 INDEXATION ET SLICING
# ==============================================================================
print("\n" + "=" * 70)
print("1.3 INDEXATION ET SLICING")
print("=" * 70)

# Indexation 1D
a1d = np.array([10, 20, 30, 40, 50])
print(f"Tableau 1D : {a1d}")
print(f"  a[0]   = {a1d[0]}")
print(f"  a[-1]  = {a1d[-1]}   (dernier élément)")

# Slicing 1D
print(f"\nSlicing 1D :")
print(f"  a[1:4]   = {a1d[1:4]}    (indices 1 à 3)")
print(f"  a[:3]    = {a1d[:3]}     (début à 2)")
print(f"  a[3:]    = {a1d[3:]}     (3 à la fin)")
print(f"  a[::2]   = {a1d[::2]}    (pas de 2)")
print(f"  a[::-1]  = {a1d[::-1]}   (inversé)")

# Indexation 2D
a2d = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])
print(f"\nTableau 2D :\n{a2d}")
print(f"  a[0, 1]    = {a2d[0, 1]}    (ligne 0, colonne 1)")
print(f"  a[2, -1]   = {a2d[2, -1]}   (ligne 2, dernière colonne)")
print(f"  a[1, :]    = {a2d[1, :]}    (ligne 1 entière)")
print(f"  a[:, 0]    = {a2d[:, 0]}    (colonne 0 entière)")
print(f"  a[0:2, 1:3]=\n{a2d[0:2, 1:3]}   (sous-matrice)")
print(f"  a[:, ::2]  =\n{a2d[:, ::2]}   (colonnes 0 et 2)")

# Indexation booléenne (filtres)
print(f"\n--- Indexation booléenne ---")
print(f"a > 5  : {a1d > 5}")
print(f"a[a > 5] : {a1d[a1d > 5]}")
print(f"a[(a > 15) & (a < 45)] : {a1d[(a1d > 15) & (a1d < 45)]}")

# Fancy indexing (indexation par tableau d'entiers)
print(f"\n--- Fancy indexing ---")
indices = np.array([0, 2, 4])
print(f"a[{indices}] = {a1d[indices]}")
print(f"a2d[[0, 2], [1, 2]] = {a2d[[0, 2], [1, 2]]}   (éléments (0,1) et (2,2))")
print(f"a2d[[0, 2], :] =\n{a2d[[0, 2], :]}")

# np.where()
print(f"\n--- np.where() ---")
result = np.where(a1d > 25, a1d * 10, a1d)
print(f"np.where(a > 25, a*10, a) : {result}")
indices_true = np.where(a1d > 25)
print(f"np.where(a > 25) indices  : {indices_true}")


# ==============================================================================
# 1.4 MANIPULATION DE FORME
# ==============================================================================
print("\n" + "=" * 70)
print("1.4 MANIPULATION DE FORME")
print("=" * 70)

# reshape()
base = np.arange(12)
print(f"Tableau de base : {base}, shape={base.shape}")
r1 = base.reshape((3, 4))
print(f"\nreshape((3, 4))       :\n{r1}, shape={r1.shape}")
r2 = base.reshape((2, 2, 3))
print(f"reshape((2, 2, 3))    :\n{r2}, shape={r2.shape}")
r3 = base.reshape((3, -1))
print(f"reshape((3, -1))      :\n{r3}, shape={r3.shape}  (-1 calculé auto)")

# ravel() vs flatten()
mat = np.array([[1, 2], [3, 4]])
print(f"\nTableau 2D :\n{mat}")
rv = mat.ravel()
fl = mat.flatten()
print(f"ravel()   : {rv}  (vue, partage mémoire)")
print(f"flatten() : {fl}  (copie indépendante)")

# transpose() et .T
a2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\nTableau :\n{a2d}, shape={a2d.shape}")
print(f".T :\n{a2d.T}, shape={a2d.T.shape}")

# 3D transpose personnalisé
a3d = np.arange(24).reshape(2, 3, 4)
print(f"\n3D shape original : {a3d.shape}")
a3d_t = a3d.transpose(1, 0, 2)
print(f"transpose(1, 0, 2)  : {a3d_t.shape}")

# swapaxes()
sw = a3d.swapaxes(0, 2)
print(f"swapaxes(0, 2)      : {sw.shape}")

# np.newaxis et expand_dims()
vec = np.array([1, 2, 3])
print(f"\nVecteur : {vec}, shape={vec.shape}")
print(f"vec[np.newaxis, :]  : shape {vec[np.newaxis, :].shape}")
print(f"vec[:, np.newaxis]  : shape {vec[:, np.newaxis].shape}")
print(f"expand_dims(axis=0) : shape {np.expand_dims(vec, axis=0).shape}")
print(f"expand_dims(axis=1) : shape {np.expand_dims(vec, axis=1).shape}")

# squeeze()
sq = np.array([[[1, 2, 3]]])   # shape (1, 1, 3)
print(f"\nAvant squeeze : shape {sq.shape}")
print(f"squeeze()      : shape {np.squeeze(sq).shape}")
print(f"squeeze(axis=0): shape {np.squeeze(sq, axis=0).shape}")


# ==============================================================================
# 1.5 COPIE VS VUE
# ==============================================================================
print("\n" + "=" * 70)
print("1.5 COPIE VS VUE")
print("=" * 70)

# .view() — partage les données
original = np.array([[1, 2, 3], [4, 5, 6]])
vue = original.view()
print(f"Original :\n{original}")
vue[0, 0] = 999
print(f"Après modification de la vue[0,0]=999 :\n{original}")
print(f"Partage mémoire ? {np.shares_memory(original, vue)}")

# .copy() — copie indépendante
copie = original.copy()
copie[0, 0] = 111
print(f"\nAprès modification de la copie[0,0]=111 :")
print(f"Original :\n{original}")
print(f"Copie    :\n{copie}")
print(f"Partage mémoire ? {np.shares_memory(original, copie)}")

# reshape() retourne une vue quand c'est possible
r = original.reshape(6)
print(f"\nreshape(6) partage mémoire ? {np.shares_memory(original, r)}")


# ==============================================================================
# 1.6 CONCATÉNATION ET SPLIT
# ==============================================================================
print("\n" + "=" * 70)
print("1.6 CONCATÉNATION ET SPLIT")
print("=" * 70)

# np.concatenate()
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
c = np.concatenate((a, b), axis=0)
print(f"concatenate axis=0 :\n{c}")

d = np.array([[7], [8]])
e = np.concatenate((a, d), axis=1)
print(f"\nconcatenate axis=1 :\n{e}")

# vstack, hstack, dstack
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
print(f"\nvstack(([1,2,3], [4,5,6])) :\n{np.vstack((v1, v2))}")
print(f"hstack(([1,2,3], [4,5,6])) : {np.hstack((v1, v2))}")

m1 = np.array([[1, 2], [3, 4]])
m2 = np.array([[5, 6], [7, 8]])
print(f"\ndstack sur deux matrices 2x2 : shape {np.dstack((m1, m2)).shape}")

# np.split()
sp = np.arange(10)
print(f"\nTableau : {sp}")
s1, s2 = np.split(sp, 2)
print(f"split(2) : {s1} | {s2}")
p1, p2, p3 = np.split(sp, [2, 5])
print(f"split([2,5]) : {p1} | {p2} | {p3}")

# hsplit et vsplit sur 2D
mat2d = np.arange(12).reshape(3, 4)
print(f"\nMatrice 3x4 :\n{mat2d}")
h1, h2 = np.hsplit(mat2d, 2)
print(f"hsplit(2) :\n{h1}\n---\n{h2}")
v_parts = np.vsplit(mat2d, 3)
print(f"vsplit(3) : {len(v_parts)} parties de shape {v_parts[0].shape}")

print("\n" + "=" * 70)
print("FIN DU JOUR 1 — Résumé exécuté avec succès !")
print("=" * 70)
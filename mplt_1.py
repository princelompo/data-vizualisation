#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
JOUR 3 : Matplotlib — Bases et personnalisation
Résumé complet et commenté
================================================================================
Ce script reprend l'ensemble des concepts vus au Jour 3 :
  3.1 Architecture de Matplotlib
  3.2 Graphiques de base (plot, scatter, bar, barh, hist, pie, boxplot)
  3.3 Personnalisation des axes
  3.4 Texte et annotations
  3.5 Sauvegarde et formats
  3.6 Styles et paramètres globaux

Note : Ce script utilise le backend 'Agg' pour la génération de fichiers
sans fenêtre interactive. Les figures sont sauvegardées en PNG.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend non interactif (rendu fichier)
import matplotlib.pyplot as plt
from pathlib import Path

# Création du dossier de sortie pour les images
import os
chemin = Path.cwd() / 'jour3_images'
os.makedirs(chemin, exist_ok=True)

# ==============================================================================
# 3.1 ARCHITECTURE : pyplot vs API orientée objet
# ==============================================================================
print("=" * 70)
print("3.1 ARCHITECTURE DE MATPLOTLIB")
print("=" * 70)

# Approche pyplot (rapide, style MATLAB)
plt.figure(figsize=(6, 4))
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro-', label='pyplot rapide')
plt.title('Approche pyplot')
plt.legend()
plt.savefig(chemin / '01_pyplot.png', dpi=150)
plt.close()
print("Figure 01_pyplot.png sauvegardée (approche pyplot)")

# Approche orientée objet (contrôle total)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], 'bs--', label='API OO')
ax.set_title('Approche orientée objet')
ax.set_xlabel('Axe X')
ax.set_ylabel('Axe Y')
ax.legend()
fig.savefig(chemin / '02_api_oo.png', dpi=150)
plt.close()
print("Figure 02_api_oo.png sauvegardée (approche OO)")

print("\nHiérarchie : Figure > Axes > Axis > Line2D/Patch/Text")
print("  - Figure : conteneur principal")
print("  - Axes   : zone de tracé individuelle")
print("  - Axis   : axes x et y (graduations)")


# ==============================================================================
# 3.2 GRAPHiques DE BASE
# ==============================================================================
print("\n" + "=" * 70)
print("3.2 GRAPHiques DE BASE")
print("=" * 70)

# --- plt.plot() : courbes ---
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots(figsize=(10, 5))
# Paramètres détaillés : color, linewidth, linestyle, marker, alpha, label
ax.plot(x, y1, color='blue', linewidth=2, linestyle='-', 
        marker='', alpha=0.8, label='sin(x)')
ax.plot(x, y2, color='red', linewidth=2, linestyle='--', 
        marker='', alpha=0.8, label='cos(x)')
# Format court : 'go-' = vert, cercle, ligne pleine
ax.plot(x, np.sin(x) * 0.5, 'go:', markersize=2, label='0.5·sin(x)')
ax.set_title('plt.plot() — Courbes avec paramètres complets')
ax.set_xlabel('x (radians)')
ax.set_ylabel('Amplitude')
ax.legend(loc='upper right', frameon=True, shadow=True, fancybox=True)
ax.grid(True, linestyle=':', alpha=0.5)
fig.savefig(chemin / '03_plot.png', dpi=150)
plt.close()
print("Figure 03_plot.png sauvegardée")

# --- plt.scatter() : nuage de points ---
np.random.seed(42)
x_scat = np.random.rand(50)
y_scat = np.random.rand(50)
colors = np.random.rand(50)           # Valeurs pour colormap
sizes = 1000 * np.random.rand(50)   # Tailles variables

fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(x_scat, y_scat, s=sizes, c=colors, cmap='viridis',
                     alpha=0.7, edgecolors='black', linewidths=0.5)
ax.set_title('plt.scatter() — Taille, couleur et colormap')
ax.set_xlabel('X')
ax.set_ylabel('Y')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Valeur de couleur')
fig.savefig(chemin / '04_scatter.png', dpi=150)
plt.close()
print("Figure 04_scatter.png sauvegardée")

# --- plt.bar() : barres verticales ---
categories = ['A', 'B', 'C', 'D', 'E']
valeurs = [23, 45, 12, 38, 29]
colors_bar = ['#e74c3c', '#2ecc71', '#3498db', '#f39c12', '#9b59b6']

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(categories, valeurs, color=colors_bar, edgecolor='black', 
       linewidth=1.5, width=0.6, align='center')
ax.set_title('plt.bar() — Barres verticales personnalisées')
ax.set_xlabel('Catégories')
ax.set_ylabel('Valeurs')
ax.set_ylim(0, 55)
for i, v in enumerate(valeurs):
    ax.text(i, v + 1.5, str(v), ha='center', fontweight='bold')
fig.savefig(chemin / '05_bar.png', dpi=150)
plt.close()
print("Figure 05_bar.png sauvegardée")

# --- plt.barh() : barres horizontales ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(categories, valeurs, color='skyblue', edgecolor='navy', linewidth=1)
ax.set_title('plt.barh() — Barres horizontales')
ax.set_xlabel('Valeurs')
ax.set_xlim(0, 55)
fig.savefig(chemin / '06_barh.png', dpi=150)
plt.close()
print("Figure 06_barh.png sauvegardée")

# --- plt.hist() : histogramme ---
data1 = np.random.normal(0, 1, 1000)
data2 = np.random.normal(2, 1.5, 1000)

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(data1, bins=30, range=(-5, 7), density=True, alpha=0.6,
        color='steelblue', edgecolor='black', histtype='stepfilled', label='N(0,1)')
ax.hist(data2, bins=30, range=(-5, 7), density=True, alpha=0.6,
        color='coral', edgecolor='black', histtype='stepfilled', label='N(2,1.5)')
ax.set_title('plt.hist() — Histogrammes avec density et superposition')
ax.set_xlabel('Valeur')
ax.set_ylabel('Densité')
ax.legend()
fig.savefig(chemin / '07_hist.png', dpi=150)
plt.close()
print("Figure 07_hist.png sauvegardée")

# --- plt.pie() : camembert ---
fig, ax = plt.subplots(figsize=(8, 8))
parts = [30, 20, 25, 15, 10]
labels = ['A', 'B', 'C', 'D', 'E']
explode = [0.1, 0, 0, 0, 0]
colors_pie = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']
ax.pie(parts, explode=explode, labels=labels, autopct='%1.1f%%',
       shadow=True, startangle=90, colors=colors_pie,
       textprops={'fontsize': 12})
ax.set_title('plt.pie() — Camembert avec explode et shadow')
fig.savefig(chemin / '08_pie.png', dpi=150)
plt.close()
print("Figure 08_pie.png sauvegardée")

# --- plt.boxplot() : boîte à moustaches ---
fig, ax = plt.subplots(figsize=(8, 6))
data_box = [np.random.normal(0, 1, 100),
            np.random.normal(2, 1.5, 100),
            np.random.normal(-1, 0.5, 100)]
bp = ax.boxplot(data_box, patch_artist=True, notch=True, sym='r+', widths=0.5)
ax.set_xticklabels(['Groupe A', 'Groupe B', 'Groupe C'])
# Colorer les boîtes
for patch, color in zip(bp['boxes'], ['lightblue', 'lightgreen', 'lightcoral']):
    patch.set_facecolor(color)
ax.set_title('plt.boxplot() — Boîtes à moustaches (patch_artist + notch)')
ax.set_ylabel('Valeur')
ax.grid(axis='y', linestyle='--', alpha=0.5)
fig.savefig(chemin / '09_boxplot.png', dpi=150)
plt.close()
print("Figure 09_boxplot.png sauvegardée")


# ==============================================================================
# 3.3 PERSONNALISATION DES AXES
# ==============================================================================
print("\n" + "=" * 70)
print("3.3 PERSONNALISATION DES AXES")
print("=" * 70)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, np.sin(x), label='sin(x)')

# Limites
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)

# Graduations personnalisées
ax.set_xticks([0, np.pi, 2*np.pi, 3*np.pi])
ax.set_xticklabels(['0', 'π', '2π', '3π'], rotation=0)
ax.set_yticks([-1, -0.5, 0, 0.5, 1])

# Labels et titre avec style
ax.set_xlabel('Temps (s)', fontsize=12, color='navy', fontweight='bold')
ax.set_ylabel('Amplitude', fontsize=12, color='navy')
ax.set_title('Personnalisation complète des axes', fontsize=14, loc='center', pad=20)

# Légende
ax.legend(loc='upper right', frameon=True, shadow=True, fancybox=True, 
          ncol=1, title='Fonctions', title_fontsize=10)

# Grille
ax.grid(True, linestyle='--', alpha=0.5, color='gray')

fig.savefig(chemin / '10_axes_custom.png', dpi=150)
plt.close()
print("Figure 10_axes_custom.png sauvegardée")

# axis() en une ligne
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot([0, 1, 2], [0, 1, 0])
ax.axis('equal')  # Échelle égale
ax.set_title('axis("equal") — Échelle 1:1')
fig.savefig(chemin / '11_axis_equal.png', dpi=150)
plt.close()
print("Figure 11_axis_equal.png sauvegardée")


# ==============================================================================
# 3.4 TEXTE ET ANNOTATIONS
# ==============================================================================
print("\n" + "=" * 70)
print("3.4 TEXTE ET ANNOTATIONS")
print("=" * 70)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')

# plt.text() — texte libre
ax.text(2, 0.5, 'Zone stable', fontsize=12, color='green', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7))

# plt.annotate() — annotation avec flèche
xmax = np.pi / 2
ymax = 1.0
ax.annotate('Maximum local', xy=(xmax, ymax), xytext=(5, 0.5),
            arrowprops=dict(arrowstyle='->', color='red', lw=2,
                           connectionstyle='arc3,rad=0.2'),
            fontsize=11, color='red', fontweight='bold')

# Deuxième annotation avec style différent
ax.annotate('Minimum local', xy=(3*np.pi/2, -1), xytext=(7, -0.5),
            arrowprops=dict(arrowstyle='-|>', color='purple', lw=2),
            fontsize=11, color='purple')

ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)
ax.set_title('Texte et annotations avec flèches')
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')
ax.grid(True, alpha=0.3)

fig.savefig(chemin / '12_annotations.png', dpi=150)
plt.close()
print("Figure 12_annotations.png sauvegardée")

# figtext() — texte en coordonnées figure
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([1, 2, 3], [1, 4, 2])
ax.set_title('plt.figtext() — Coordonnées figure')
plt.figtext(0.5, 0.02, 'Note : données préliminaires — 2026', 
            ha='center', fontsize=10, style='italic', color='gray')
fig.savefig(chemin / '13_figtext.png', dpi=150)
plt.close()
print("Figure 13_figtext.png sauvegardée")


# ==============================================================================
# 3.5 SAUVEGARDE ET FORMATS
# ==============================================================================
print("\n" + "=" * 70)
print("3.5 SAUVEGARDE ET FORMATS")
print("=" * 70)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, np.sin(x), 'b-', linewidth=2)
ax.set_title('Sauvegarde en différents formats')
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')
ax.grid(True, alpha=0.3)

# PNG haute résolution
fig.savefig(chemin / '14_save_png.png', dpi=300, 
            bbox_inches='tight', facecolor='white')
print("Figure 14_save_png.png sauvegardée (PNG 300 DPI, bbox_inches='tight')")

# PDF vectoriel
fig.savefig(chemin / '14_save_pdf.pdf', format='pdf',
            bbox_inches='tight')
print("Figure 14_save_pdf.pdf sauvegardée (PDF vectoriel)")

# SVG vectoriel web
fig.savefig(chemin / '14_save_svg.svg', format='svg',
            bbox_inches='tight')
print("Figure 14_save_svg.svg sauvegardée (SVG vectoriel)")

# Transparent
fig.savefig(chemin / '14_save_transparent.png', 
            dpi=150, transparent=True)
print("Figure 14_save_transparent.png sauvegardée (fond transparent)")
plt.close()


# ==============================================================================
# 3.6 STYLES ET PARAMÈTRES GLOBAUX
# ==============================================================================
print("\n" + "=" * 70)
print("3.6 STYLES ET PARAMÈTRES GLOBAUX")
print("=" * 70)

styles_demo = ['default', 'ggplot', 'bmh', 'fivethirtyeight', 'dark_background']
for style in styles_demo:
    plt.style.use(style)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, np.sin(x), label='sin(x)')
    ax.plot(x, np.cos(x), label='cos(x)')
    ax.set_title(f'Style : "{style}"')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    fig.savefig(f'{chemin}/15_style_{style}.png', dpi=150)
    plt.close()
    print(f"Figure 15_style_{style}.png sauvegardée")

# Réinitialiser au style par défaut
plt.style.use('default')

# rcParams personnalisés
print("\n--- rcParams personnalisés ---")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['lines.linewidth'] = 2.5

fig, ax = plt.subplots()
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')
ax.set_title('Avec rcParams personnalisés')
ax.legend()
fig.savefig(chemin / '16_rcparams.png', dpi=150)
plt.close()
print("Figure 16_rcparams.png sauvegardée")

# Réinitialiser rcParams
plt.rcdefaults()

# Méthode plt.rc() alternative
plt.rc('figure', figsize=(8, 4), dpi=100)
plt.rc('lines', linewidth=1.5)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x))
ax.set_title('Avec plt.rc()')
fig.savefig(chemin / '17_plt_rc.png', dpi=150)
plt.close()
print("Figure 17_plt_rc.png sauvegardée")
plt.rcdefaults()

print("\n" + "=" * 70)
print("FIN DU JOUR 3 — Résumé exécuté avec succès !")
print("=" * 70)
print(f"\nToutes les figures sont dans : /mnt/agents/output/jour3_images/")
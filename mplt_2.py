#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
JOUR 4 : Matplotlib — Figures, subplots et styles avancés
Résumé complet et commenté
================================================================================
Ce script reprend l'ensemble des concepts vus au Jour 4 :
  4.1 Figures et tailles
  4.2 Subplots (subplots, GridSpec, subplot_mosaic)
  4.3 Graphiques avancés (fill_between, stackplot, errorbar, violinplot)
  4.4 Axes secondaires (twinx, twiny)
  4.5 Couleurs, colormaps et normalisation
  4.6 Graphiques 3D (aperçu)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize, LogNorm, BoundaryNorm
from cycler import cycler
from mpl_toolkits.mplot3d import Axes3D
import os
from pathlib import Path

chemin = Path.cwd() / 'jour4_images'
os.makedirs(chemin, exist_ok=True)

# ==============================================================================
# 4.1 FIGURES ET TAILLES
# ==============================================================================
print("=" * 70)
print("4.1 FIGURES ET TAILLES")
print("=" * 70)

# plt.figure() avec paramètres complets
fig = plt.figure(num='ma_figure', figsize=(10, 6), dpi=150,
                 facecolor='lightyellow', edgecolor='red', frameon=True)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4], [1, 4, 2, 3], 'o-', color='navy')
ax.set_title('figure() avec facecolor, edgecolor, dpi=150')
ax.set_facecolor('white')
fig.savefig(chemin / '01_figure_params.png', dpi=150)
plt.close()
print("Figure 01_figure_params.png sauvegardée")

# tight_layout
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for i, ax in enumerate(axes.flat):
    ax.plot(np.random.rand(10))
    ax.set_title(f'Subplot {i+1}')
fig.suptitle('Titre global avec suptitle()', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout(pad=3.0, h_pad=2.0, w_pad=2.0)
fig.savefig(chemin / '02_tight_layout.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 02_tight_layout.png sauvegardée")


# ==============================================================================
# 4.2 SUBPLOTS
# ==============================================================================
print("\n" + "=" * 70)
print("4.2 SUBPLOTS")
print("=" * 70)

# plt.subplot() style MATLAB
fig = plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
plt.plot(np.random.rand(10), 'r-')
plt.title('subplot(2,2,1)')

plt.subplot(2, 2, 2)
plt.scatter(np.random.rand(20), np.random.rand(20), c='blue')
plt.title('subplot(2,2,2)')

plt.subplot(2, 2, 3)
plt.bar(['A', 'B', 'C'], [3, 7, 2], color='green')
plt.title('subplot(2,2,3)')

plt.subplot(2, 2, 4)
plt.hist(np.random.randn(100), bins=15, color='orange')
plt.title('subplot(2,2,4)')

plt.tight_layout()
fig.savefig(chemin / '03_subplot_matlab.png', dpi=150)
plt.close()
print("Figure 03_subplot_matlab.png sauvegardée")

# plt.subplots() — méthode recommandée
fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True, sharey=False,
                         gridspec_kw={'width_ratios': [1, 2, 1]})
for i, ax in enumerate(axes.flat):
    ax.plot(np.random.rand(20))
    ax.set_title(f'axes[{i//3},{i%3}]')
fig.suptitle('plt.subplots() avec sharex=True et width_ratios', fontsize=14)
plt.tight_layout()
fig.savefig(chemin / '04_subplots_recommande.png', dpi=150)
plt.close()
print("Figure 04_subplots_recommande.png sauvegardée")

# subplot_mosaic (Matplotlib >= 3.3)
fig, ax_dict = plt.subplot_mosaic(
    [['A', 'B'],
     ['C', 'C']],
    figsize=(10, 8)
)
ax_dict['A'].plot(np.random.rand(20), 'r-')
ax_dict['A'].set_title('A (haut gauche)')
ax_dict['B'].scatter(np.random.rand(20), np.random.rand(20), c='blue')
ax_dict['B'].set_title('B (haut droite)')
ax_dict['C'].hist(np.random.randn(100), bins=20, color='green', alpha=0.7)
ax_dict['C'].set_title('C (toute la ligne du bas)')
fig.suptitle('subplot_mosaic() — Disposition textuelle', fontsize=14)
plt.tight_layout()
fig.savefig(chemin / '05_subplot_mosaic.png', dpi=150)
plt.close()
print("Figure 05_subplot_mosaic.png sauvegardée")

# GridSpec — contrôle fin
fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(3, 3, width_ratios=[1, 2, 1], height_ratios=[1, 2, 1],
                       wspace=0.3, hspace=0.4)

ax1 = fig.add_subplot(gs[0, :])
ax1.plot(np.random.rand(50), 'r-')
ax1.set_title('gs[0, :] — Ligne 0, toutes les colonnes')

ax2 = fig.add_subplot(gs[1, :-1])
ax2.scatter(np.random.rand(30), np.random.rand(30), c='blue')
ax2.set_title('gs[1, :-1] — Lignes 1, colonnes 0 et 1')

ax3 = fig.add_subplot(gs[1:, -1])
ax3.bar(['X', 'Y', 'Z'], [5, 3, 8], color='green')
ax3.set_title('gs[1:, -1] — Lignes 1-2, dernière colonne')

ax4 = fig.add_subplot(gs[2, 0])
ax4.plot(np.random.rand(10), 'm-')
ax4.set_title('gs[2, 0]')

ax5 = fig.add_subplot(gs[2, 1])
ax5.plot(np.random.rand(10), 'c-')
ax5.set_title('gs[2, 1]')

fig.suptitle('GridSpec avec width_ratios et height_ratios', fontsize=14)
fig.savefig(chemin / '06_gridspec.png', dpi=150)
plt.close()
print("Figure 06_gridspec.png sauvegardée")

# subplots_adjust
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax in axes.flat:
    ax.plot(np.random.rand(10))
fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.1,
                    wspace=0.4, hspace=0.5)
fig.suptitle('subplots_adjust() — Marges et espacements manuels')
fig.savefig(chemin / '07_subplots_adjust.png', dpi=150)
plt.close()
print("Figure 07_subplots_adjust.png sauvegardée")


# ==============================================================================
# 4.3 GRAPHiques AVANCÉS
# ==============================================================================
print("\n" + "=" * 70)
print("4.3 GRAPHiques AVANCÉS")
print("=" * 70)

# fill_between
x = np.linspace(0, 10, 200)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y1, 'b-', label='sin(x)')
ax.plot(x, y2, 'r-', label='cos(x)')
ax.fill_between(x, y1, y2, where=(y1 > y2), alpha=0.3, color='green',
                interpolate=True, label='sin > cos')
ax.fill_between(x, y1, y2, where=(y1 <= y2), alpha=0.3, color='red',
                interpolate=True, label='sin <= cos')
ax.set_title('fill_between() avec where et interpolate')
ax.legend()
ax.grid(True, alpha=0.3)
fig.savefig(chemin / '08_fill_between.png', dpi=150)
plt.close()
print("Figure 08_fill_between.png sauvegardée")

# stackplot
x = np.arange(10)
y1 = np.array([3, 5, 2, 7, 4, 6, 3, 5, 4, 6])
y2 = np.array([2, 3, 5, 2, 6, 3, 5, 2, 7, 3])
y3 = np.array([1, 2, 3, 4, 2, 5, 3, 4, 2, 5])

fig, ax = plt.subplots(figsize=(10, 6))
ax.stackplot(x, y1, y2, y3, labels=['Série A', 'Série B', 'Série C'],
             colors=['#ff9999', '#66b3ff', '#99ff99'], alpha=0.8)
ax.set_title('stackplot() — Aires empilées')
ax.set_xlabel('Temps')
ax.set_ylabel('Valeur')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3, axis='y')
fig.savefig(chemin / ' 09_stackplot.png', dpi=150)
plt.close()
print("Figure 09_stackplot.png sauvegardée")

# errorbar
x = np.arange(5)
y = np.array([2, 3, 5, 4, 6])
yerr = np.array([0.5, 0.3, 0.8, 0.4, 0.6])
xerr = np.array([0.2, 0.15, 0.3, 0.2, 0.25])

fig, ax = plt.subplots(figsize=(8, 6))
ax.errorbar(x, y, yerr=yerr, xerr=xerr, fmt='o', color='blue',
            ecolor='red', elinewidth=2, capsize=6, capthick=2,
            markersize=8, label='Mesures ± erreur')
ax.set_title('errorbar() — Barres d\'erreur en X et Y')
ax.set_xlabel('Index')
ax.set_ylabel('Valeur')
ax.legend()
ax.grid(True, alpha=0.3)
fig.savefig(chemin / '10_errorbar.png', dpi=150)
plt.close()
print("Figure 10_errorbar.png sauvegardée")

# violinplot
np.random.seed(42)
data_violin = [np.random.normal(0, 1, 100),
               np.random.normal(2, 1.5, 100),
               np.random.normal(-1, 0.5, 100)]

fig, ax = plt.subplots(figsize=(10, 6))
parts = ax.violinplot(data_violin, positions=[1, 2, 3],
                       showmeans=True, showmedians=True, showextrema=True)
# Colorer les violons
for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(['lightblue', 'lightcoral', 'lightgreen'][i])
    pc.set_alpha(0.7)
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(['Groupe A', 'Groupe B', 'Groupe C'])
ax.set_title('violinplot() — Distributions en violon')
ax.set_ylabel('Valeur')
ax.grid(True, alpha=0.3, axis='y')
fig.savefig(chemin / '11_violinplot.png', dpi=150)
plt.close()
print("Figure 11_violinplot.png sauvegardée")

# Couleurs cycliques (prop_cycle)
fig, ax = plt.subplots(figsize=(10, 6))
for i in range(5):
    ax.plot(x, np.random.rand(5) + i, linewidth=2, label=f'Courbe {i+1}')
ax.set_title('Couleurs cycliques par défaut (axes.prop_cycle)')
ax.legend()
fig.savefig(chemin / '12_prop_cycle.png', dpi=150)
plt.close()
print("Figure 12_prop_cycle.png sauvegardée")

# Personnalisation du prop_cycle
plt.rc('axes', prop_cycle=cycler(color=['crimson', 'forestgreen', 'royalblue']) +
                cycler(linestyle=['-', '--', ':']))
fig, ax = plt.subplots(figsize=(10, 6))
for i in range(6):
    ax.plot(np.linspace(0, 10, 50), np.sin(np.linspace(0, 10, 50) + i), linewidth=2)
ax.set_title('prop_cycle personnalisé (3 couleurs × 3 linestyles)')
fig.savefig(chemin / '13_custom_cycle.png', dpi=150)
plt.close()
plt.rcdefaults()
print("Figure 13_custom_cycle.png sauvegardée")


# ==============================================================================
# 4.4 AXES SECONDAIRES
# ==============================================================================
print("\n" + "=" * 70)
print("4.4 AXES SECONDAIRES")
print("=" * 70)

# twinx — deuxième axe y
t = np.linspace(0, 24, 100)
temp = 20 + 10 * np.sin(2 * np.pi * t / 24)
humidite = 60 - 15 * np.sin(2 * np.pi * t / 24)

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(t, temp, 'b-', linewidth=2, label='Température (°C)')
ax1.set_xlabel('Heure')
ax1.set_ylabel('Température (°C)', color='blue', fontsize=12)
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_ylim(0, 40)

ax2 = ax1.twinx()
ax2.plot(t, humidite, 'r-', linewidth=2, label='Humidité (%)')
ax2.set_ylabel('Humidité (%)', color='red', fontsize=12)
ax2.tick_params(axis='y', labelcolor='red')
ax2.set_ylim(20, 100)

ax1.set_title('twinx() — Deux échelles Y sur le même graphique')
ax1.grid(True, alpha=0.3)
fig.savefig(chemin / '14_twinx.png', dpi=150)
plt.close()
print("Figure 14_twinx.png sauvegardée")

# twiny — deuxième axe x
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(np.linspace(0, 100, 50), np.random.rand(50), 'b-', label='Échelle 1')
ax1.set_xlabel('Échelle principale (0-100)')
ax1.set_ylabel('Valeur')

ax2 = ax1.twiny()
ax2.set_xlim(0, 10)
ax2.set_xlabel('Échelle secondaire (0-10)')
ax2.plot(np.linspace(0, 10, 50), np.random.rand(50), 'r--', label='Échelle 2')

ax1.set_title('twiny() — Deux échelles X')
ax1.legend(loc='lower left')
ax2.legend(loc='lower right')
fig.savefig(chemin / '15_twiny.png', dpi=150)
plt.close()
print("Figure 15_twiny.png sauvegardée")


# ==============================================================================
# 4.5 COULEURS, COLORMAPS ET NORMALISATION
# ==============================================================================
print("\n" + "=" * 70)
print("4.5 COULEURS, COLORMAPS ET NORMALISATION")
print("=" * 70)

# Démonstration des colormaps
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
cmaps = ['viridis', 'plasma', 'coolwarm', 'RdBu', 'tab10', 'twilight']
for ax, cmap_name in zip(axes.flat, cmaps):
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    ax.imshow(gradient, aspect='auto', cmap=cmap_name)
    ax.set_title(f'"{cmap_name}"')
    ax.set_xticks([])
    ax.set_yticks([])
fig.suptitle('Colormaps intégrées — Séquentielles, Divergentes, Qualitatives, Cycliques')
plt.tight_layout()
fig.savefig(chemin / '16_colormaps.png', dpi=150)
plt.close()
print("Figure 16_colormaps.png sauvegardée")

# Normalize et colorbar
np.random.seed(42)
x = np.random.rand(100) * 10
y = np.random.rand(100) * 10
z = np.random.rand(100) * 100

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Normalisation linéaire
ax1 = axes[0]
norm_lin = Normalize(vmin=0, vmax=100)
sc1 = ax1.scatter(x, y, c=z, cmap='viridis', norm=norm_lin, s=80, edgecolors='black')
ax1.set_title('Normalize(vmin=0, vmax=100)')
cbar1 = fig.colorbar(sc1, ax=ax1, shrink=0.8)
cbar1.set_label('Valeur (linéaire)')

# Normalisation logarithmique
ax2 = axes[1]
z_log = np.abs(np.random.randn(100)) * 100 + 0.1
norm_log = LogNorm(vmin=0.1, vmax=1000)
sc2 = ax2.scatter(x, y, c=z_log, cmap='plasma', norm=norm_log, s=80, edgecolors='black')
ax2.set_title('LogNorm(vmin=0.1, vmax=1000)')
cbar2 = fig.colorbar(sc2, ax=ax2, shrink=0.8)
cbar2.set_label('Valeur (log)')

# BoundaryNorm (discrète)
ax3 = axes[2]
bounds = [0, 20, 40, 60, 80, 100]
norm_bn = BoundaryNorm(bounds, plt.cm.RdBu.N)
sc3 = ax3.scatter(x, y, c=z, cmap='RdBu', norm=norm_bn, s=80, edgecolors='black')
ax3.set_title('BoundaryNorm([0,20,40,60,80,100])')
cbar3 = fig.colorbar(sc3, ax=ax3, shrink=0.8)
cbar3.set_label('Classes')

plt.tight_layout()
fig.savefig(chemin / '17_normalisation.png', dpi=150)
plt.close()
print("Figure 17_normalisation.png sauvegardée")

# plt.cm — accès direct aux couleurs
fig, ax = plt.subplots(figsize=(10, 2))
cmap = plt.cm.viridis
for i in range(10):
    color = cmap(i / 9)
    ax.barh(0, 1, left=i, color=color, height=0.8, edgecolor='black')
    ax.text(i + 0.5, 0, f'{i/9:.1f}', ha='center', va='center', color='white', fontweight='bold')
ax.set_xlim(0, 10)
ax.set_ylim(-0.5, 0.5)
ax.set_title('plt.cm.viridis — 10 couleurs extraites manuellement')
ax.set_xticks([])
ax.set_yticks([])
fig.savefig(chemin / '18_cm_access.png', dpi=150)
plt.close()
print("Figure 18_cm_access.png sauvegardée")


# ==============================================================================
# 4.6 GRAPHiques 3D (APERÇU)
# ==============================================================================
print("\n" + "=" * 70)
print("4.6 GRAPHiques 3D (APERÇU)")
print("=" * 70)

# Courbe 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z_3d = np.linspace(-2, 2, 100)
r = z_3d**2 + 1
x_3d = r * np.sin(theta)
y_3d = r * np.cos(theta)
ax.plot3D(x_3d, y_3d, z_3d, 'b-', linewidth=2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('plot3D() — Courbe 3D (spirale)')
fig.savefig(chemin / '19_plot3d.png', dpi=150)
plt.close()
print("Figure 19_plot3d.png sauvegardée")

# Scatter 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
n = 100
xs = np.random.rand(n) * 10
ys = np.random.rand(n) * 10
zs = np.random.rand(n) * 10
colors_3d = zs
ax.scatter3D(xs, ys, zs, c=colors_3d, cmap='plasma', s=60, alpha=0.8, edgecolors='black')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('scatter3D() — Nuage de points 3D avec colormap')
fig.savefig(chemin / '20_scatter3d.png', dpi=150)
plt.close()
print("Figure 20_scatter3d.png sauvegardée")

# Surface 3D avec view_init
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
x_surf = np.linspace(-5, 5, 50)
y_surf = np.linspace(-5, 5, 50)
X_surf, Y_surf = np.meshgrid(x_surf, y_surf)
Z_surf = np.sin(np.sqrt(X_surf**2 + Y_surf**2))

surf = ax.plot_surface(X_surf, Y_surf, Z_surf, cmap='viridis', alpha=0.9,
                       edgecolor='none', antialiased=True)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('plot_surface() — Surface 3D\nview_init(elev=30, azim=45)')
ax.view_init(elev=30, azim=45)
fig.colorbar(surf, shrink=0.5, aspect=10, label='Amplitude')
fig.savefig(chemin / '21_surface3d.png', dpi=150)
plt.close()
print("Figure 21_surface3d.png sauvegardée")

# Wireframe 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(X_surf, Y_surf, Z_surf, color='blue', alpha=0.5, rstride=3, cstride=3)
ax.set_title('plot_wireframe() — Fil de fer 3D')
ax.view_init(elev=25, azim=60)
fig.savefig(chemin / '22_wireframe3d.png', dpi=150)
plt.close()
print("Figure 22_wireframe3d.png sauvegardée")

print("\n" + "=" * 70)
print("FIN DU JOUR 4 — Résumé exécuté avec succès !")
print("=" * 70)
print(f"\nToutes les figures sont dans : {chemin }")
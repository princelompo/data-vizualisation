"""
RESUME JOUR 4 : Matplotlib - Figures, subplots et styles
Ce script couvre la création de figures complexes, les subplots,
les GridSpec, et les styles avancés.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap

# Configuration globale
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

print("=" * 60)
print("1. FIGURE AVEC SUBPLOTS (MÉTHODE STANDARD)")
print("=" * 60)

# ============================================
# 1. SUBPLOTS STANDARD AVEC FIGURE
# ============================================

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Génération des données
np.random.seed(42)
x = np.linspace(0, 10, 50)

# Remplir chaque subplot
plots = [
    ('sin(x)', np.sin(x)),
    ('cos(x)', np.cos(x)),
    ('sin(x)*cos(x)', np.sin(x) * np.cos(x)),
    ('sin(2x)', np.sin(2*x)),
    ('cos(2x)', np.cos(2*x)),
    ('sin(x)+cos(x)', np.sin(x) + np.cos(x))
]

for idx, (title, y) in enumerate(plots): 
    i, j = idx // 3, idx % 3
    ax = axes[i, j]
    ax.plot(x, y, linewidth=2)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)

# Titre global
fig.suptitle('Fonctions trigonométriques - Subplots 2x3',
             fontsize=16, fontweight='bold', y=0.98)

plt.tight_layout()
plt.savefig('subplots_standard_jour4.png', dpi=300, bbox_inches='tight')

print("Graphique 1 sauvegardé : subplots_standard_jour4.png")

# ============================================
# 2. GRIDSPEC - LAYOUT PERSONNALISÉ
# ============================================

print("\n" + "=" * 60)
print("2. GRIDSPEC - LAYOUT PERSONNALISÉ")
print("=" * 60)

fig = plt.figure(figsize=(14, 10))

# Création d'une grille complexe
gs = GridSpec(4, 4,
              figure=fig,
              left=0.08, right=0.92,
              bottom=0.08, top=0.92,
              wspace=0.3, hspace=0.3,
              width_ratios=[1, 1.5, 1, 1],
              height_ratios=[1, 1.2, 1, 1])

# Création des axes avec différentes tailles
ax_main = fig.add_subplot(gs[:2, :2])    # En haut à gauche (2x2)
ax_top_right = fig.add_subplot(gs[:2, 2:])  # En haut à droite (2x2)
ax_bottom_left = fig.add_subplot(gs[2:, :1])  # En bas à gauche (2x1)
ax_bottom_mid = fig.add_subplot(gs[2:, 1:3])  # En bas au milieu (2x2)
ax_bottom_right = fig.add_subplot(gs[2:, 3:])  # En bas à droite (2x1)

# Tracer dans chaque axe
x = np.linspace(0, 10, 200)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.exp(-x/5)
y4 = np.cos(x) * np.exp(-x/5)

# Axe principal : courbes avec légende
ax_main.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
ax_main.plot(x, y2, 'r-', linewidth=2, label='cos(x)')
ax_main.plot(x, y3, 'g--', linewidth=2, label='sin(x)e^(-x/5)')
ax_main.set_title('Courbes principales', fontsize=14, fontweight='bold')
ax_main.set_xlabel('x')
ax_main.set_ylabel('y')
ax_main.legend(loc='upper right')
ax_main.grid(True, alpha=0.3)

# Axe top right : histogramme
data = np.random.randn(1000)
ax_top_right.hist(data, bins=30, density=True, alpha=0.7, 
                  color='blue', edgecolor='black')
ax_top_right.set_title('Histogramme', fontsize=14, fontweight='bold')
ax_top_right.set_xlabel('Valeur')
ax_top_right.set_ylabel('Densité')
ax_top_right.grid(True, alpha=0.3)

# Axe bottom left : barres
categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 12, 67, 34]
ax_bottom_left.bar(categories, values, color='steelblue', alpha=0.7)
ax_bottom_left.set_title('Barres', fontsize=14, fontweight='bold')
ax_bottom_left.set_ylabel('Valeurs')
ax_bottom_left.grid(True, axis='y', alpha=0.3)

# Axe bottom mid : nuage de points
n = 150
x_scatter = np.random.randn(n)
y_scatter = 0.5 * x_scatter + 0.3 * np.random.randn(n)
colors = np.random.rand(n)
ax_bottom_mid.scatter(x_scatter, y_scatter, c=colors, 
                      cmap='viridis', alpha=0.6, s=40)
ax_bottom_mid.set_title('Nuage de points', fontsize=14, fontweight='bold')
ax_bottom_mid.set_xlabel('x')
ax_bottom_mid.set_ylabel('y')
ax_bottom_mid.grid(True, alpha=0.3)

# Axe bottom right : boxplot
box_data = [np.random.normal(0, std, 50) for std in [1, 2, 3, 4]]
ax_bottom_right.boxplot(box_data, patch_artist=True,
                       boxprops=dict(facecolor='lightblue', alpha=0.7))
ax_bottom_right.set_title('Boxplot', fontsize=14, fontweight='bold')
ax_bottom_right.set_xticklabels(['G1', 'G2', 'G3', 'G4'])
ax_bottom_right.grid(True, alpha=0.3)

# Titre global
fig.suptitle('Layout personnalisé avec GridSpec',
             fontsize=18, fontweight='bold', y=0.98)

plt.savefig('gridspec_jour4.png', dpi=300, bbox_inches='tight')

print("Graphique 2 sauvegardé : gridspec_jour4.png")

# ============================================
# 3. STYLES AVANCÉS ET DOUBLE AXE
# ============================================

print("\n" + "=" * 60)
print("3. STYLES AVANCÉS ET DOUBLE AXE")
print("=" * 60)

fig, ax1 = plt.subplots(figsize=(12, 7))

# Données
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.exp(x/3)  # Croissance exponentielle

# Premier axe (gauche)
ax1.plot(x, y1, 'b-', linewidth=2.5, label='sin(x)')
ax1.set_xlabel('x', fontsize=12)
ax1.set_ylabel('sin(x)', fontsize=12, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(-1.5, 1.5)

# Deuxième axe (droite)
ax2 = ax1.twinx()
ax2.plot(x, y2, 'r-', linewidth=2.5, label='e^(x/3)')
ax2.set_ylabel('e^(x/3)', fontsize=12, color='red')
ax2.tick_params(axis='y', labelcolor='red')
ax2.set_ylim(0, 30)

# Titre
ax1.set_title('Double axe - sin(x) et e^(x/3)', fontsize=16, fontweight='bold')

# Légende combinée
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.savefig('double_axe_jour4.png', dpi=300, bbox_inches='tight')

print("Graphique 3 sauvegardé : double_axe_jour4.png")

# ============================================
# 4. COMPARAISON DES STYLES
# ============================================

print("\n" + "=" * 60)
print("4. COMPARAISON DES STYLES")
print("=" * 60)

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x) * np.exp(-x/5)

styles_a_tester = ['default', 'seaborn-v0_8', 'ggplot', 
                   'fivethirtyeight', 'dark_background', 'bmh']

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

for ax, style in zip(axes.flat, styles_a_tester):
    with plt.style.context(style):
        ax.plot(x, y1, label='sin(x)', linewidth=2)
        ax.plot(x, y2, label='cos(x)e^(-x/5)', linewidth=2)
        ax.set_title(f'Style : {style}', fontsize=12, fontweight='bold')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

plt.suptitle('Comparaison des styles Matplotlib',
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('styles_comparaison_jour4.png', dpi=300, bbox_inches='tight')

print("Graphique 4 sauvegardé : styles_comparaison_jour4.png")

# ============================================
# 5. EXEMPLE AVEC SUBPLOTS ET SHARING
# ============================================

print("\n" + "=" * 60)
print("5. SUBPLOTS AVEC SHARING")
print("=" * 60)

# Création de subplots avec partage d'axes
fig, axes = plt.subplots(2, 2, figsize=(12, 8),
                         sharex=True,
                         sharey=True)

# Données
x = np.linspace(0, 10, 50)
params = [(1, 1), (2, 1), (1, 2), (2, 2)]

for ax, (a, b) in zip(axes.flat, params):
    y = np.sin(a * x) * np.cos(b * x)
    ax.plot(x, y, linewidth=2)
    ax.set_title(f'a={a}, b={b}', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.3)

# Labels seulement en bas et à gauche
fig.text(0.5, 0.02, 'x (partagé)', ha='center', fontsize=14)
fig.text(0.02, 0.5, 'y (partagé)', va='center', rotation=90, fontsize=14)

fig.suptitle('Subplots avec axes partagés', fontsize=16, fontweight='bold')

plt.tight_layout()
plt.savefig('shared_axes_jour4.png', dpi=300, bbox_inches='tight')

print("Graphique 5 sauvegardé : shared_axes_jour4.png")

# ============================================
# 6. AJOUT DE COLORBAR SUR SUBPLOT
# ============================================

print("\n" + "=" * 60)
print("6. SUBPLOT AVEC COLORBAR")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Création de données 2D
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2)) * np.cos(2 * X) * np.sin(2 * Y)

# Contourf avec colorbar
im1 = axes[0].contourf(X, Y, Z, levels=20, cmap='viridis')
axes[0].set_title('Contourf avec colorbar', fontsize=14, fontweight='bold')
axes[0].set_xlabel('x')
axes[0].set_ylabel('y')
plt.colorbar(im1, ax=axes[0])

# Imshow avec colorbar
im2 = axes[1].imshow(Z, extent=[-3, 3, -3, 3], cmap='plasma', aspect='auto')
axes[1].set_title('Imshow avec colorbar', fontsize=14, fontweight='bold')
axes[1].set_xlabel('x')
axes[1].set_ylabel('y')
plt.colorbar(im2, ax=axes[1])

plt.suptitle('Visualisation 2D avec colorbars', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('colorbar_jour4.png', dpi=300, bbox_inches='tight')

print("Graphique 6 sauvegardé : colorbar_jour4.png")

# ============================================
# 7. SAUVEGARDE DE LA FIGURE COMPLÈTE
# ============================================

print("\n" + "=" * 60)
print("Tous les graphiques ont été générés avec succès !")
print("=" * 60)

# Afficher tous les graphiques (optionnel)
plt.show()

print("\n" + "=" * 60)
print("FIN DU RÉSUMÉ JOUR 4")
print("=" * 60)
print("Graphiques générés :")
print("  - subplots_standard_jour4.png")
print("  - gridspec_jour4.png")
print("  - double_axe_jour4.png")
print("  - styles_comparaison_jour4.png")
print("  - shared_axes_jour4.png")
print("  - colorbar_jour4.png")
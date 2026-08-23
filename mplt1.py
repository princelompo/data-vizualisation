"""
RESUME JOUR 3 : Matplotlib - Bases et personnalisation
Ce script couvre la création de graphiques, la personnalisation
des axes, des légendes, et des styles.
"""

import matplotlib.pyplot as plt
import numpy as np

# Configuration globale
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# ============================================
# 1. PRÉPARATION DES DONNÉES
# ============================================

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.exp(-x/5)

print("=" * 60)
print("1. GRAPHIQUE AVEC MULTIPLES COURBES")
print("=" * 60)

# ============================================
# 2. CRÉATION DU GRAPHIQUE
# ============================================

fig, ax = plt.subplots(figsize=(12, 8))

# -------------------- COURBE 1 --------------------
line1, = ax.plot(x, y1,
                 color='#2E86C1',        # Bleu
                 linestyle='-',
                 linewidth=2.5,
                 marker='o',
                 markersize=4,
                 markerfacecolor='white',
                 markeredgecolor='#2E86C1',
                 markeredgewidth=1.5,
                 label='sin(x)',
                 alpha=0.9,
                 zorder=3)

# -------------------- COURBE 2 --------------------
line2, = ax.plot(x, y2,
                 color='#E74C3C',        # Rouge
                 linestyle='--',
                 linewidth=2.5,
                 marker='s',
                 markersize=4,
                 markerfacecolor='white',
                 markeredgecolor='#E74C3C',
                 markeredgewidth=1.5,
                 label='cos(x)',
                 alpha=0.9,
                 zorder=2)

# -------------------- COURBE 3 --------------------
line3, = ax.plot(x, y3,
                 color='#28B463',        # Vert
                 linestyle='-.',
                 linewidth=2.5,
                 marker='^',
                 markersize=4,
                 markerfacecolor='white',
                 markeredgecolor='#28B463',
                 markeredgewidth=1.5,
                 label='sin(x) × e^(-x/5)',
                 alpha=0.9,
                 zorder=1)

# ============================================
# 3. PERSONNALISATION DES AXES
# ============================================

# Limites
ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-1.5, 1.5)

# Labels
ax.set_xlabel('Temps (s)',
              fontsize=14,
              fontweight='bold',
              color='#2C3E50',
              labelpad=12)

ax.set_ylabel('Amplitude',
              fontsize=14,
              fontweight='bold',
              color='#2C3E50',
              labelpad=12)

# Titre
ax.set_title('Fonctions trigonométriques avec amortissement',
             fontsize=18,
             fontweight='bold',
             color='#1A1A2E',
             pad=25)

# ============================================
# 4. TICKS PERSONNALISÉS
# ============================================

# Ticks en fonction de π
ticks_x = np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi, 5*np.pi/2, 3*np.pi])
labels_x = ['0', 'π/2', 'π', '3π/2', '2π', '5π/2', '3π']

ax.set_xticks(ticks_x)
ax.set_xticklabels(labels_x, fontsize=11)

ax.set_yticks([-1, -0.5, 0, 0.5, 1])
ax.set_yticklabels([-1, -0.5, 0, 0.5, 1], fontsize=11)

# Personnalisation des ticks
ax.tick_params(axis='both',
               direction='inout',
               length=6,
               width=1.5,
               colors='#2C3E50',
               labelsize=11,
               pad=8)

# ============================================
# 5. GRILLE
# ============================================

ax.grid(True,
        linestyle='--',
        linewidth=0.8,
        color='#BDC3C7',
        alpha=0.6,
        axis='both',
        which='major')          # 'major', 'minor', 'both'

# Grille mineure (plus fine)
ax.grid(True,
        linestyle=':',
        linewidth=0.3,
        color='#BDC3C7',
        alpha=0.4,
        axis='both',
        which='minor')

# ============================================
# 6. LÉGENDE COMPLÈTE
# ============================================

legend = ax.legend(
    loc='upper right',
    fontsize=12,
    frameon=True,
    fancybox=True,
    framealpha=0.95,
    edgecolor='#2C3E50',
    facecolor='white',
    shadow=True,
    title='Légende',
    title_fontsize=13,
    labelspacing=0.8,
    handlelength=2.5,
    handletextpad=0.8
)

# Personnalisation du titre de légende
legend.get_title().set_fontweight('bold')

# ============================================
# 7. ANNOTATIONS
# ============================================

# Annotation du maximum
ax.annotate('Maximum de sin(x)',
            xy=(np.pi/2, 1),
            xytext=(3.5, 0.8),
            fontsize=12,
            fontweight='bold',
            color='#2E86C1',
            arrowprops=dict(
                arrowstyle='->',
                connectionstyle='arc3,rad=0.2',
                color='#2E86C1',
                linewidth=2
            ),
            bbox=dict(
                boxstyle='round,pad=0.3',
                facecolor='white',
                edgecolor='#2E86C1',
                alpha=0.8
            ))

# Annotation de l'amortissement
ax.annotate('Amortissement exponentiel',
            xy=(8, y3[np.where(x >= 8)[0][0]]),
            xytext=(6.5, -0.8),
            fontsize=12,
            fontweight='bold',
            color='#28B463',
            arrowprops=dict(
                arrowstyle='->',
                connectionstyle='arc3,rad=0.1',
                color='#28B463',
                linewidth=2
            ),
            bbox=dict(
                boxstyle='round,pad=0.3',
                facecolor='white',
                edgecolor='#28B463',
                alpha=0.8
            ))

# ============================================
# 8. LIGNES VERTICALES ET HORIZONTALES
# ============================================

# Ligne verticale à x = π
ax.axvline(x=np.pi,
           ymin=0, ymax=1,
           color='#8E44AD',
           linestyle=':',
           linewidth=2,
           alpha=0.7,
           label='x = π')

# Ligne horizontale à y = 0.5
ax.axhline(y=0.5,
           xmin=0, xmax=1,
           color='#E67E22',
           linestyle=':',
           linewidth=2,
           alpha=0.7,
           label='y = 0.5')

# Ajout d'une région ombrée
ax.axvspan(2, 3, 
           alpha=0.2,
           color='#F1C40F',
           label='Zone d\'intérêt')

# ============================================
# 9. TEXTE AJOUTÉ
# ============================================

ax.text(8.5, 1.3,
        'Graphique créé avec\nMatplotlib',
        fontsize=10,
        color='#7F8C8D',
        ha='center',
        va='center',
        bbox=dict(
            boxstyle='round,pad=0.3',
            facecolor='#ECF0F1',
            edgecolor='#BDC3C7',
            alpha=0.7
        ))

# ============================================
# 10. AJUSTEMENT FINAL
# ============================================

plt.tight_layout()

# ============================================
# 11. SAUVEGARDE
# ============================================

# Sauvegarder avec haute qualité
plt.savefig('graphique_synthese_jour3.png',
            dpi=300,
            bbox_inches='tight',
            pad_inches=0.2,
            facecolor='white',
            transparent=False)

print("Graphique sauvegardé : graphique_synthese_jour3.png")

# ============================================
# 12. DEUXIÈME EXEMPLE : BARRES D'ERREUR
# ============================================

print("\n" + "=" * 60)
print("2. BARRES D'ERREUR")
print("=" * 60)

fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ---- Sous-graphique 1 : Barres d'erreur simples ----
x_data = np.arange(6)
y_data = np.array([2, 3.5, 2.8, 4.2, 3.9, 4.8])
y_err = np.array([0.3, 0.5, 0.4, 0.6, 0.5, 0.7])

ax1.errorbar(x_data, y_data,
             yerr=y_err,
             fmt='o-',
             color='#2E86C1',
             markerfacecolor='white',
             markeredgecolor='#2E86C1',
             markeredgewidth=2,
             markersize=10,
             capsize=6,
             capthick=2,
             elinewidth=2,
             ecolor='#E74C3C',
             label='Mesures')

ax1.set_xlabel('Échantillon', fontsize=12, fontweight='bold')
ax1.set_ylabel('Valeur mesurée', fontsize=12, fontweight='bold')
ax1.set_title('Barres d\'erreur', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=11)

# ---- Sous-graphique 2 : Barres d'erreur asymétriques ----
y_err_low = np.array([0.2, 0.3, 0.3, 0.4, 0.3, 0.4])
y_err_high = np.array([0.4, 0.6, 0.5, 0.8, 0.7, 0.9])

ax2.errorbar(x_data, y_data,
             yerr=[y_err_low, y_err_high],
             fmt='s-',
             color='#28B463',
             markerfacecolor='white',
             markeredgecolor='#28B463',
             markeredgewidth=2,
             markersize=10,
             capsize=6,
             capthick=2,
             elinewidth=2,
             ecolor='#E67E22',
             label='Mesures asymétriques')

ax2.set_xlabel('Échantillon', fontsize=12, fontweight='bold')
ax2.set_ylabel('Valeur mesurée', fontsize=12, fontweight='bold')
ax2.set_title('Barres d\'erreur asymétriques', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=11)

plt.tight_layout()
plt.savefig('barres_erreur_jour3.png', dpi=300, bbox_inches='tight')

# ============================================
# 13. TROISIÈME EXEMPLE : STYLES PRÉDÉFINIS
# ============================================

print("\n" + "=" * 60)
print("3. COMPARAISON DES STYLES")
print("=" * 60)

fig3, axes = plt.subplots(2, 3, figsize=(15, 10))

styles = ['default', 'ggplot', 'seaborn-v0_8', 'fivethirtyeight', 'dark_background', 'classic']

for ax, style in zip(axes.flat, styles):
    with plt.style.context(style):
        ax.plot(x, y1, label='sin(x)', linewidth=2)
        ax.plot(x, y2, label='cos(x)', linewidth=2)
        ax.set_title(f'Style: {style}', fontsize=12, fontweight='bold')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('styles_comparaison_jour3.png', dpi=300, bbox_inches='tight')

# ============================================
# 14. AFFICHAGE
# ============================================

plt.show()

print("\n" + "=" * 60)
print("FIN DU RÉSUMÉ JOUR 3")
print("=" * 60)
print(f"Graphiques générés :")
print("  - graphique_synthese_jour3.png")
print("  - barres_erreur_jour3.png")
print("  - styles_comparaison_jour3.png")
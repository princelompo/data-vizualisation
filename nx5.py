import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# ================================================================
# ÉTAPE 1 : DONNÉES — VILLES ET COORDONNÉES (approximatives)
# ================================================================
positions_villes = {
    "Paris":     (2.35, 48.85),
    "Lyon":      (4.83, 45.76),
    "Marseille": (5.37, 43.30),
    "Toulouse":  (1.44, 43.60),
    "Bordeaux":  (-0.58, 44.84),
    "Nantes":    (-1.55, 47.22),
    "Lille":     (3.06, 50.63),
    "Strasbourg":(7.75, 48.58),
}

# Liaisons routières existantes (paires de villes reliées)
liaisons = [
    ("Paris", "Lyon"), ("Paris", "Nantes"), ("Paris", "Lille"),
    ("Paris", "Strasbourg"), ("Lyon", "Marseille"), ("Lyon", "Toulouse"),
    ("Toulouse", "Bordeaux"), ("Bordeaux", "Nantes"), ("Marseille", "Toulouse"),
]

# ================================================================
# ÉTAPE 2 : CONSTRUCTION DU GRAPHE PONDÉRÉ (NumPy + NetworkX)
# ================================================================
def distance_euclidienne(p1, p2):
    """Calcule une distance approximative entre deux coordonnées (NumPy)."""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) * 100  # facteur d'échelle

G = nx.Graph()

# Ajout des nœuds avec leur position comme attribut
for ville, coord in positions_villes.items():
    G.add_node(ville, pos=coord)

# Ajout des arêtes avec un poids = distance calculée automatiquement
for ville1, ville2 in liaisons:
    d = distance_euclidienne(positions_villes[ville1], positions_villes[ville2])
    G.add_edge(ville1, ville2, weight=round(d, 1))

print("Réseau routier construit :")
for u, v, w in G.edges(data='weight'):
    print(f"  {u} — {v} : {w} km")

# ================================================================
# ÉTAPE 3 : PLUS COURT CHEMIN ENTRE DEUX VILLES
# ================================================================
depart, arrivee = "Nantes", "Strasbourg"

chemin = nx.dijkstra_path(G, depart, arrivee, weight='weight')
distance_totale = nx.dijkstra_path_length(G, depart, arrivee, weight='weight')

print(f"\nTrajet optimal {depart} → {arrivee} :")
print(f"  Chemin : {' → '.join(chemin)}")
print(f"  Distance totale : {distance_totale:.1f} km")

# ================================================================
# ÉTAPE 4 : VILLE LA PLUS CENTRALE (analyse réseau)
# ================================================================
centralite = nx.betweenness_centrality(G, weight='weight')
ville_pivot = max(centralite, key=centralite.get)
print(f"\nVille la plus 'stratégique' (betweenness) : {ville_pivot} ({centralite[ville_pivot]:.3f})")

# ================================================================
# ÉTAPE 5 : ARBRE COUVRANT MINIMAL (réseau routier minimal)
# ================================================================
arbre_minimal = nx.minimum_spanning_tree(G, weight='weight', algorithm='kruskal')
poids_total_arbre = sum(w for u, v, w in arbre_minimal.edges(data='weight'))
poids_total_reseau = sum(w for u, v, w in G.edges(data='weight'))

print(f"\nRéseau complet : {poids_total_reseau:.1f} km de routes")
print(f"Réseau minimal (arbre couvrant) : {poids_total_arbre:.1f} km de routes")
print(f"Économie potentielle : {poids_total_reseau - poids_total_arbre:.1f} km")

# ================================================================
# ÉTAPE 6 : MATRICE DES DISTANCES (NumPy)
# ================================================================
noeuds = list(G.nodes())
n = len(noeuds)
matrice_distances = np.full((n, n), np.inf)

toutes_distances = dict(nx.all_pairs_dijkstra_path_length(G, weight='weight'))
for i, u in enumerate(noeuds):
    for j, v in enumerate(noeuds):
        if v in toutes_distances[u]:
            matrice_distances[i, j] = toutes_distances[u][v]

print(f"\nDistance moyenne entre toutes les villes connectées : "
      f"{matrice_distances[np.isfinite(matrice_distances) & (matrice_distances > 0)].mean():.1f} km")

# ================================================================
# ÉTAPE 7 : VISUALISATION (Matplotlib + NetworkX)
# ================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
pos = nx.get_node_attributes(G, 'pos')   # utilise les vraies coordonnées géographiques

# --- Graphique 1 : réseau complet avec chemin optimal surligné ---
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700, 
                        edgecolors='black', ax=axes[0])
nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5, ax=axes[0])
nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', ax=axes[0])

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, ax=axes[0])

# Surligner le chemin optimal en rouge
chemin_aretes = list(zip(chemin, chemin[1:]))
nx.draw_networkx_edges(G, pos, edgelist=chemin_aretes, edge_color='red', width=3, ax=axes[0])
nx.draw_networkx_nodes(G, pos, nodelist=chemin, node_color='salmon', 
                        node_size=700, edgecolors='red', linewidths=2, ax=axes[0])

axes[0].set_title(f"Trajet optimal : {depart} → {arrivee}", fontsize=13)
axes[0].axis('off')

# --- Graphique 2 : arbre couvrant minimal ---
nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=700, 
                        edgecolors='black', ax=axes[1])
nx.draw_networkx_edges(G, pos, edge_color='lightgray', alpha=0.3, style='dashed', ax=axes[1])
nx.draw_networkx_edges(arbre_minimal, pos, edge_color='green', width=3, ax=axes[1])
nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', ax=axes[1])

axes[1].set_title(f"Réseau routier minimal ({poids_total_arbre:.0f} km)", fontsize=13)
axes[1].axis('off')

fig.suptitle("Analyse d'un réseau routier pondéré", fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
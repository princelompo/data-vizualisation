#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
JOUR 7 : NetworkX — Algorithmes de base (centralité, chemins)
Résumé complet et commenté
================================================================================
Ce script reprend l'ensemble des concepts vus au Jour 7 :
  7.1 Connexité
  7.2 Mesures de centralité
  7.3 Plus courts chemins
  7.4 Chemins et cycles
  7.5 Densité et clustering
  7.6 Arbres et MST
"""

import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

my_dir = Path.cwd()/"NX3"
if not my_dir.exists():
    my_dir.mkdir(parents=True, exist_ok=True)
# ==============================================================================
# 7.1 CONNEXITÉ
# ==============================================================================
print("=" * 70)
print("7.1 CONNEXITÉ")
print("=" * 70)

# --- Graphe non orienté ---
G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6)])
print("\n--- Graphe non orienté ---")
print(f"Arêtes : {list(G.edges())}")
print(f"is_connected(G)                = {nx.is_connected(G)}")
print(f"number_connected_components(G) = {nx.number_connected_components(G)}")
print(f"Composantes connexes :")
for i, comp in enumerate(nx.connected_components(G), 1):
    print(f"  Composante {i} : {comp}")
print(f"node_connected_component(G, 1) = {nx.node_connected_component(G, 1)}")
print(f"node_connected_component(G, 4) = {nx.node_connected_component(G, 4)}")

# Biconnexité
G2 = nx.Graph()
G2.add_edges_from([(1, 2), (2, 3), (3, 1), (2, 4), (4, 5), (5, 2)])  # 2 est point d'articulation
print(f"\n--- Biconnexité ---")
print(f"is_biconnected(G2)             = {nx.is_biconnected(G2)}")
print(f"Points d'articulation          = {list(nx.articulation_points(G2))}")
print(f"Composantes biconnexes :")
for comp in nx.biconnected_components(G2):
    print(f"  {comp}")

# --- Graphe orienté ---
D = nx.DiGraph()
D.add_edges_from([(1, 2), (2, 3), (3, 1), (3, 4)])
print(f"\n--- Graphe orienté ---")
print(f"Arêtes orientées : {list(D.edges())}")
print(f"is_strongly_connected(D)       = {nx.is_strongly_connected(D)}")
print(f"is_weakly_connected(D)         = {nx.is_weakly_connected(D)}")
print(f"Composantes fortement connexes :")
for comp in nx.strongly_connected_components(D):
    print(f"  {comp}")
print(f"Nombre de SCC                  = {nx.number_strongly_connected_components(D)}")


# ==============================================================================
# 7.2 MESURES DE CENTRALITÉ
# ==============================================================================
print("\n" + "=" * 70)
print("7.2 MESURES DE CENTRALITÉ")
print("=" * 70)

G = nx.karate_club_graph()

# Degré
dc = nx.degree_centrality(G)
print(f"\n--- Degré de centralité (top 5) ---")
for node, val in sorted(dc.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  Nœud {node:2d} : {val:.4f}")

# Betweenness
bc = nx.betweenness_centrality(G, normalized=True)
print(f"\n--- Betweenness centrality (top 5) ---")
for node, val in sorted(bc.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  Nœud {node:2d} : {val:.4f}")

# Betweenness avec échantillonnage (k) pour grands graphes
bc_approx = nx.betweenness_centrality(G, k=10, seed=42)
print(f"\nBetweenness approximée (k=10) nœud 0 : {bc_approx[0]:.4f}")

# Closeness
cc = nx.closeness_centrality(G)
print(f"\n--- Closeness centrality (top 5) ---")
for node, val in sorted(cc.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  Nœud {node:2d} : {val:.4f}")

# Eigenvector
eig = nx.eigenvector_centrality(G, max_iter=500, tol=1e-08)
print(f"\n--- Eigenvector centrality (top 5) ---")
for node, val in sorted(eig.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  Nœud {node:2d} : {val:.4f}")

# Eigenvector avec numpy (plus stable)
eig_np = nx.eigenvector_centrality_numpy(G)
print(f"\nEigenvector (numpy) nœud 0 : {eig_np[0]:.4f}")

# PageRank
pr = nx.pagerank(G, alpha=0.85)
print(f"\n--- PageRank (top 5) ---")
for node, val in sorted(pr.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  Nœud {node:2d} : {val:.4f}")

# Visualisation des centralités
pos = nx.spring_layout(G, seed=42)
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
centralities = [
    ('Degré', dc),
    ('Betweenness', bc),
    ('Closeness', cc),
    ('Eigenvector', eig),
    ('PageRank', pr),
]
for ax, (name, cent) in zip(axes.flat, centralities):
    vals = [cent[n] for n in G.nodes()]
    nx.draw(G, pos, ax=ax, node_color=vals, cmap='plasma',
            node_size=[v * 3000 for v in vals], with_labels=True,
            font_size=7, edge_color='gray', alpha=0.8)
    ax.set_title(f'{name} centrality')
    ax.axis('off')
# Dernier subplot : comparaison
ax = axes[1, 2]
nodes = list(G.nodes())
x_pos = np.arange(len(nodes))
ax.bar(x_pos - 0.2, [dc[n] for n in nodes], 0.15, label='Degré', alpha=0.7)
ax.bar(x_pos, [bc[n] for n in nodes], 0.15, label='Betweenness', alpha=0.7)
ax.bar(x_pos + 0.2, [pr[n] for n in nodes], 0.15, label='PageRank', alpha=0.7)
ax.set_title('Comparaison des centralités')
ax.set_xlabel('Nœud')
ax.set_ylabel('Valeur')
ax.legend()
fig.suptitle('Visualisation des différentes centralités', fontsize=16, fontweight='bold')
plt.tight_layout()
fig.savefig(my_dir/"01_centralites.png", dpi=150, bbox_inches='tight')
plt.close()
print("\nFigure 01_centralites.png sauvegardée")


# ==============================================================================
# 7.3 PLUS COURTS CHEMINS
# ==============================================================================
print("\n" + "=" * 70)
print("7.3 PLUS COURTS CHEMINS")
print("=" * 70)

G = nx.Graph()
G.add_weighted_edges_from([
    (1, 2, 4), (1, 3, 2), (2, 3, 1), (2, 4, 5),
    (3, 4, 8), (3, 5, 10), (4, 5, 2), (4, 6, 6), (5, 6, 3)
])

print(f"\nGraphe pondéré : {list(G.edges(data=True))}")

# shortest_path
path = nx.shortest_path(G, source=1, target=6, weight='weight', method='dijkstra')
print(f"\nshortest_path(1 -> 6, dijkstra) : {path}")

# shortest_path_length
length = nx.shortest_path_length(G, source=1, target=6, weight='weight')
print(f"shortest_path_length(1 -> 6)     : {length}")

# Tous les chemins depuis une source
paths_from_1 = nx.shortest_path(G, source=1, weight='weight')
print(f"\nChemins depuis 1 :")
for target, p in paths_from_1.items():
    print(f"  1 -> {target} : {p}")

# Toutes les longueurs depuis une source
lengths_from_1 = nx.shortest_path_length(G, source=1, weight='weight')
print(f"\nLongueurs depuis 1 : {dict(lengths_from_1)}")

# Toutes les paires
all_lengths = dict(nx.shortest_path_length(G, weight='weight'))
print(f"\nMatrice des distances (extrait) :")
for src in [1, 2, 3]:
    row = {tgt: all_lengths[src][tgt] for tgt in [1, 2, 3, 4, 5, 6]}
    print(f"  Depuis {src} : {row}")

# all_shortest_paths
print(f"\nTous les plus courts chemins 1 -> 4 (non pondéré) :")
for p in nx.all_shortest_paths(G, source=1, target=4):
    print(f"  {p}")

# average_shortest_path_length
avg = nx.average_shortest_path_length(G, weight='weight')
print(f"\naverage_shortest_path_length     : {avg:.4f}")

# Diamètre, rayon, excentricité
print(f"\n--- Diamètre, rayon, excentricité ---")
ecc = nx.eccentricity(G)
print(f"Eccentricité                     : {ecc}")
print(f"Diameter(G)                      = {nx.diameter(G, e=ecc)}")
print(f"Radius(G)                        = {nx.radius(G, e=ecc)}")
print(f"Center(G)                        = {nx.center(G, e=ecc)}")
print(f"Periphery(G)                     = {nx.periphery(G, e=ecc)}")

# has_path
print(f"\nhas_path(G, 1, 6)                = {nx.has_path(G, 1, 6)}")
print(f"has_path(G, 1, 99)               = {nx.has_path(G, 1, 99) if 99 in G else 'Nœud 99 absent'}")

# Visualisation du plus court chemin
pos = nx.spring_layout(G, seed=42)
fig, ax = plt.subplots(figsize=(10, 8))
# Toutes les arêtes en gris clair
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1500, edgecolors='black', ax=ax)
nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=2, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', ax=ax)
edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=11, ax=ax)
# Chemin optimal en rouge épais
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=4, ax=ax)
# Source et cible en vert/orange
nx.draw_networkx_nodes(G, pos, nodelist=[path[0]], node_color='limegreen', node_size=1800, edgecolors='black', linewidths=2, ax=ax)
nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]], node_color='orange', node_size=1800, edgecolors='black', linewidths=2, ax=ax)
ax.set_title(f'Plus court chemin 1 -> 6 : {path} (longueur={length})')
ax.axis('off')
fig.savefig(my_dir/"02_shortest_path.png", dpi=150, bbox_inches='tight')
plt.close()
print("\nFigure 02_shortest_path.png sauvegardée")


# ==============================================================================
# 7.4 CHEMINS ET CYCLES
# ==============================================================================
print("\n" + "=" * 70)
print("7.4 CHEMINS ET CYCLES")
print("=" * 70)

# simple_cycles (DiGraph)
D = nx.DiGraph()
D.add_edges_from([(1, 2), (2, 3), (3, 1), (2, 4), (4, 5), (5, 2)])
print(f"\n--- Cycles simples (DiGraph) ---")
print(f"Arêtes : {list(D.edges())}")
cycles = list(nx.simple_cycles(D))
print(f"Cycles simples : {cycles}")

# cycle_basis (Graph)
G_und = nx.Graph()
G_und.add_edges_from([(1, 2), (2, 3), (3, 1), (1, 4), (4, 5), (5, 1)])
print(f"\n--- Base de cycles (Graph) ---")
print(f"Arêtes : {list(G_und.edges())}")
print(f"cycle_basis(G_und, root=1)       = {nx.cycle_basis(G_und, root=1)}")

# find_cycle
print(f"find_cycle(G_und)                = {nx.find_cycle(G_und)}")

# minimum_cycle_basis
G_cycle = nx.Graph()
G_cycle.add_weighted_edges_from([
    (1, 2, 1), (2, 3, 1), (3, 1, 1),  # Triangle poids 3
    (1, 4, 2), (4, 5, 2), (5, 1, 2),  # Triangle poids 6
    (2, 4, 1)                          # Diagonale
])
print(f"\n--- Minimum cycle basis ---")
mcb = nx.minimum_cycle_basis(G_cycle, weight='weight')
print(f"minimum_cycle_basis              = {mcb}")


# ==============================================================================
# 7.5 DENSITÉ ET CLUSTERING
# ==============================================================================
print("\n" + "=" * 70)
print("7.5 DENSITÉ ET CLUSTERING")
print("=" * 70)

G = nx.Graph()
G.add_edges_from([
    (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4),  # K4 complet
    (4, 5), (5, 6), (6, 4)                           # Triangle 4-5-6
])

print(f"\nArêtes : {list(G.edges())}")
print(f"Density(G)                       = {nx.density(G):.4f}")
print(f"Clustering local                 = {nx.clustering(G)}")
print(f"Average clustering               = {nx.average_clustering(G):.4f}")
print(f"Average clustering (sans zéros)  = {nx.average_clustering(G, count_zeros=False):.4f}")
print(f"Transitivity                     = {nx.transitivity(G):.4f}")
print(f"Triangles par nœud               = {nx.triangles(G)}")
print(f"Square clustering                = {nx.square_clustering(G)}")


# ==============================================================================
# 7.6 ARBRES ET MST
# ==============================================================================
print("\n" + "=" * 70)
print("7.6 ARBRES ET MST")
print("=" * 70)

G = nx.Graph()
G.add_weighted_edges_from([
    (1, 2, 4), (1, 3, 2), (2, 3, 1), (2, 4, 5),
    (3, 4, 8), (3, 5, 10), (4, 5, 2), (4, 6, 6), (5, 6, 3)
])

print(f"\nGraphe original : {list(G.edges(data=True))}")
print(f"is_tree(G)                       = {nx.is_tree(G)}")
print(f"is_forest(G)                     = {nx.is_forest(G)}")

# Minimum Spanning Tree
mst = nx.minimum_spanning_tree(G, weight='weight', algorithm='kruskal')
print(f"\n--- Minimum Spanning Tree (Kruskal) ---")
print(f"Arêtes du MST : {list(mst.edges(data=True))}")
mst_weight = sum(d['weight'] for _, _, d in mst.edges(data=True))
print(f"Poids total du MST               = {mst_weight}")

# Maximum Spanning Tree
maxst = nx.maximum_spanning_tree(G, weight='weight', algorithm='kruskal')
print(f"\n--- Maximum Spanning Tree ---")
print(f"Arêtes du MaxST : {list(maxst.edges(data=True))}")
maxst_weight = sum(d['weight'] for _, _, d in maxst.edges(data=True))
print(f"Poids total du MaxST             = {maxst_weight}")

# Générateur d'arêtes du MST
print(f"\n--- Générateur minimum_spanning_edges ---")
for u, v, d in nx.minimum_spanning_edges(G, weight='weight', data=True):
    print(f"  ({u}, {v}) : poids = {d['weight']}")

# Visualisation MST vs graphe original
pos = nx.spring_layout(G, seed=42)
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Graphe original
ax = axes[0]
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1500, edgecolors='black', ax=ax)
nx.draw_networkx_edges(G, pos, edge_color='gray', width=2, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', ax=ax)
edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=11, ax=ax)
ax.set_title('Graphe original')
ax.axis('off')

# MST
ax = axes[1]
nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=1500, edgecolors='black', ax=ax)
# Arêtes du MST en vert épais
nx.draw_networkx_edges(G, pos, edgelist=list(mst.edges()), edge_color='green', width=4, ax=ax)
# Arêtes non-MST en gris clair
non_mst = [e for e in G.edges() if e not in mst.edges()]
nx.draw_networkx_edges(G, pos, edgelist=non_mst, edge_color='lightgray', width=1, style='--', ax=ax)
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', ax=ax)
# Labels des arêtes MST
mst_labels = {(u, v): d['weight'] for u, v, d in mst.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=mst_labels, font_size=11, ax=ax)
ax.set_title(f'Minimum Spanning Tree (poids total = {mst_weight})')
ax.axis('off')

fig.suptitle('Arbre Couvrant Minimum (Kruskal)', fontsize=16, fontweight='bold')
plt.tight_layout()
fig.savefig(my_dir/"03_mst.png", dpi=150, bbox_inches='tight')
plt.close()
print("\nFigure 03_mst.png sauvegardée")

print("\n" + "=" * 70)
print("FIN DU JOUR 7 — Résumé exécuté avec succès !")
print("=" * 70)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
JOUR 8 : Projet intégré 1 — Analyse d'un réseau social fictif
================================================================================
Ce projet intègre NumPy, Matplotlib et NetworkX :
  8.1 Construction du dataset (graphe social 60 nœuds, 3 communautés)
  8.2 Analyse structurelle (degrés, centralités, influençeurs)
  8.3 Détection de communautés (Louvain, modularité)
  8.4 Visualisation avancée (couleurs, tailles, poids, influençeurs)
  8.5 Rapport d'analyse (histogrammes, barres, heatmap, comparaison)
"""

import os

import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from collections import Counter
from pathlib import Path

My_dir = Path.cwd()/"NX4"
if not My_dir.exists():
    My_dir.mkdir(parents=True, exist_ok=True)

np.random.seed(42)  # Pour reproductibilité
# ==============================================================================
# 8.1 CONSTRUCTION DU DATASET
# ==============================================================================
print("=" * 70)
print("8.1 CONSTRUCTION DU DATASET")
print("=" * 70)

N = 60                          # Nombre de personnes
n_communities = 3               # Nombre de communautés
comm_names = ['Sport', 'Musique', 'Tech']
comm_colors = ['#e74c3c', '#3498db', '#2ecc71']

# Prénoms fictifs
prenoms = [
    'Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hugo', 'Iris', 'Jack',
    'Kara', 'Liam', 'Mia', 'Noah', 'Olivia', 'Paul', 'Quinn', 'Rose', 'Sam', 'Tina',
    'Uma', 'Victor', 'Wendy', 'Xavier', 'Yara', 'Zack', 'Anna', 'Ben', 'Cara', 'Dan',
    'Ella', 'Finn', 'Gina', 'Henry', 'Ines', 'Jules', 'Kia', 'Leo', 'Mila', 'Nico',
    'Opal', 'Pete', 'Rita', 'Sean', 'Tara', 'Ugo', 'Vera', 'Will', 'Xena', 'Yves',
    'Zoe', 'Adam', 'Beth', 'Cole', 'Dana', 'Evan', 'Faye', 'Gabe', 'Hope', 'Ian'
]

# Attribuer les communautés (ground truth)
communities_gt = np.repeat(np.arange(n_communities), N // n_communities)
# Ajouter les restants à la dernière communauté
if len(communities_gt) < N:
    communities_gt = np.concatenate([communities_gt, np.full(N - len(communities_gt), n_communities - 1)])
np.random.shuffle(communities_gt)

# Créer le graphe
G = nx.Graph()
for i in range(N):
    G.add_node(i, nom=prenoms[i], age=int(np.random.randint(18, 66)),
               communaute=int(communities_gt[i]),
               genre=np.random.choice(['F', 'M']))

print(f"Nœuds créés : {G.number_of_nodes()}")
print(f"Attributs d'un nœud (ex: nœud 0) : {G.nodes[0]}")

# Générer les arêtes avec homophilie
# Probabilité de lien : 0.25 intra-communautaire, 0.03 inter-communautaire
for i in range(N):
    for j in range(i + 1, N):
        same_comm = (communities_gt[i] == communities_gt[j])
        p = 0.25 if same_comm else 0.03
        if np.random.rand() < p:
            poids = int(np.random.randint(1, 11))
            type_lien = 'fort' if same_comm else 'faible'
            G.add_edge(i, j, poids=poids, type=type_lien)

print(f"Arêtes créées : {G.number_of_edges()}")
print(f"Attributs d'une arête (ex: {list(G.edges(data=True))[0]})")


# ==============================================================================
# 8.2 ANALYSE STRUCTURELLE
# ==============================================================================
print("\n" + "=" * 70)
print("8.2 ANALYSE STRUCTURELLE")
print("=" * 70)

# --- Degrés ---
degrees = dict(G.degree())
deg_vals = np.array(list(degrees.values()))
print(f"\n--- Degrés ---")
print(f"Degré min  = {deg_vals.min()}")
print(f"Degré max  = {deg_vals.max()}")
print(f"Degré moy  = {deg_vals.mean():.2f}")
print(f"Degré méd  = {np.median(deg_vals):.1f}")
print(f"Écart-type = {deg_vals.std():.2f}")

# --- Centralités ---
dc = nx.degree_centrality(G)
bc = nx.betweenness_centrality(G)
cc = nx.closeness_centrality(G)
ec = nx.eigenvector_centrality(G, max_iter=500)
pr = nx.pagerank(G)

centralities = {
    'Degré': dc,
    'Betweenness': bc,
    'Closeness': cc,
    'Eigenvector': ec,
    'PageRank': pr
}

print(f"\n--- Top 5 influençeurs par métrique ---")
for name, cent in centralities.items():
    top5 = sorted(cent.items(), key=lambda x: x[1], reverse=True)[:5]
    noms_top5 = [G.nodes[n]['nom'] for n, _ in top5]
    print(f"{name:12s} : {', '.join(noms_top5)}")


# ==============================================================================
# 8.3 DÉTECTION DE COMMUNAUTÉS (LOUVAIN)
# ==============================================================================
print("\n" + "=" * 70)
print("8.3 DÉTECTION DE COMMUNAUTÉS")
print("=" * 70)

# Louvain communities (NetworkX >= 2.8)
try:
    communities_detected = nx.community.louvain_communities(G, weight='poids', seed=42)
    print(f"Algorithme : Louvain communities")
except Exception as e:
    # Fallback
    communities_detected = nx.community.greedy_modularity_communities(G, weight='poids')
    print(f"Algorithme : Greedy modularity (fallback)")

print(f"Nombre de communautés détectées : {len(communities_detected)}")
for i, comm in enumerate(communities_detected):
    print(f"  Communauté détectée {i} : {len(comm)} nœuds")

# Assigner les communautés détectées comme attribut
comm_detected_dict = {}
for idx, comm in enumerate(communities_detected):
    for node in comm:
        comm_detected_dict[node] = idx
nx.set_node_attributes(G, comm_detected_dict, name='communaute_detectee')

# Modularité
modularity = nx.community.modularity(G, communities_detected, weight='poids')
print(f"Modularité de la partition      : {modularity:.4f}")

# Comparaison avec ground truth
gt_list = [G.nodes[n]['communaute'] for n in G.nodes()]
det_list = [G.nodes[n]['communaute_detectee'] for n in G.nodes()]

print(f"\n--- Comparaison Ground Truth vs Détecté ---")
for det_id in sorted(set(det_list)):
    nodes_in_det = [n for n in G.nodes() if G.nodes[n]['communaute_detectee'] == det_id]
    gt_in_det = [G.nodes[n]['communaute'] for n in nodes_in_det]
    most_common = Counter(gt_in_det).most_common(1)[0]
    print(f"  Détectée {det_id} ({len(nodes_in_det)} nœuds) → majoritairement {comm_names[most_common[0]]} ({most_common[1]}/{len(nodes_in_det)})")


# ==============================================================================
# 8.4 VISUALISATION AVANCÉE
# ==============================================================================
print("\n" + "=" * 70)
print("8.4 VISUALISATION AVANCÉE")
print("=" * 70)

pos = nx.spring_layout(G, seed=42, k=0.6, iterations=100, weight='poids')

# Couleurs selon communauté détectée
detected_colors = [comm_detected_dict[n] for n in G.nodes()]
n_comm_det = len(set(detected_colors))
cmap_nodes = plt.colormaps['tab10'].resampled(n_comm_det)
node_colors = [cmap_nodes(comm_detected_dict[n]) for n in G.nodes()]

# Tailles selon centralité de degré
node_sizes = [dc[n] * 4000 + 200 for n in G.nodes()]

# Épaisseurs selon poids
weights_edges = [G[u][v]['poids'] for u, v in G.edges()]
edge_widths = [0.5 + 2.5 * w / max(weights_edges) for w in weights_edges]

# Top 5 influençeurs (PageRank)
top5_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)[:5]
top5_nodes = [n for n, _ in top5_pr]

fig, ax = plt.subplots(figsize=(14, 12))

# Arêtes
nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.4, edge_color='gray', ax=ax)

# Nœuds normaux
normal_nodes = [n for n in G.nodes() if n not in top5_nodes]
nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes, node_color=[node_colors[n] for n in normal_nodes],
                       node_size=[node_sizes[n] for n in normal_nodes],
                       edgecolors='black', linewidths=1, ax=ax)

# Top 5 influençeurs avec contour doré
nx.draw_networkx_nodes(G, pos, nodelist=top5_nodes, node_color=[node_colors[n] for n in top5_nodes],
                       node_size=[node_sizes[n] for n in top5_nodes],
                       edgecolors='gold', linewidths=3, ax=ax)

# Labels (noms)
labels = {n: G.nodes[n]['nom'] for n in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_weight='bold', ax=ax)

# Légende des communautés
det_names = [f'Communauté {i}' for i in range(n_comm_det)]
legend_elements = [Patch(facecolor=cmap_nodes(i), edgecolor='black', label=det_names[i])
                   for i in range(n_comm_det)]
legend_elements.append(Patch(facecolor='white', edgecolor='gold', linewidth=3, label='Top 5 influençeurs'))
ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

ax.set_title(f"Réseau social fictif — {N} personnes, {G.number_of_edges()} liens\n"
             f"Couleurs = communautés détectées (Louvain) | Taille ∝ centralité | Contour doré = influençeurs",
             fontsize=13)
ax.axis('off')
fig.savefig(My_dir/"01_reseau_complet.png", dpi=200, bbox_inches='tight')
plt.close()
print("Figure 01_reseau_complet.png sauvegardée")


# ==============================================================================
# 8.5 RAPPORT D'ANALYSE (DASHBOARD)
# ==============================================================================
print("\n" + "=" * 70)
print("8.5 RAPPORT D'ANALYSE")
print("=" * 70)

fig = plt.figure(figsize=(18, 14))
fig.suptitle(f"Rapport d'analyse — Réseau social fictif ({N} nœuds, {G.number_of_edges()} arêtes) | "
             f"Modularité = {modularity:.3f}", fontsize=16, fontweight='bold', y=0.98)

# --- 1. Histogramme des degrés ---
ax1 = fig.add_subplot(2, 2, 1)
ax1.hist(deg_vals, bins=range(deg_vals.min(), deg_vals.max() + 2), 
         color='steelblue', edgecolor='black', alpha=0.8)
ax1.axvline(deg_vals.mean(), color='red', linestyle='--', linewidth=2, label=f"Moyenne = {deg_vals.mean():.1f}")
ax1.axvline(np.median(deg_vals), color='green', linestyle='--', linewidth=2, label=f"Médiane = {np.median(deg_vals):.1f}")
ax1.set_xlabel('Degré')
ax1.set_ylabel('Nombre de nœuds')
ax1.set_title('Distribution des degrés')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# --- 2. Top 10 centralités ---
ax2 = fig.add_subplot(2, 2, 2)
metric_name = 'PageRank'
metric_vals = pr
top10 = sorted(metric_vals.items(), key=lambda x: x[1], reverse=True)[:10]
noms = [G.nodes[n]['nom'] for n, _ in top10]
vals = [v for _, v in top10]
colors_bar = [comm_colors[G.nodes[n]['communaute']] for n, _ in top10]
bars = ax2.barh(range(len(noms)), vals, color=colors_bar, edgecolor='black')
ax2.set_yticks(range(len(noms)))
ax2.set_yticklabels(noms)
ax2.invert_yaxis()
ax2.set_xlabel('PageRank')
ax2.set_title('Top 10 — PageRank')
# Légende communautés réelles
legend_comm = [Patch(facecolor=comm_colors[i], edgecolor='black', label=comm_names[i]) for i in range(n_communities)]
ax2.legend(handles=legend_comm, loc='lower right', fontsize=9)
ax2.grid(axis='x', alpha=0.3)

# --- 3. Heatmap d'adjacence réordonnée par communauté ---
ax3 = fig.add_subplot(2, 2, 3)
# Réordonner les nœuds par communauté détectée
nodes_ordered = []
for c in range(n_comm_det):
    nodes_ordered.extend(sorted([n for n in G.nodes() if comm_detected_dict[n] == c]))

# Matrice d'adjacence
adj = nx.to_numpy_array(G, nodelist=nodes_ordered, weight='poids')
im = ax3.imshow(adj, cmap='YlOrRd', aspect='auto')
ax3.set_title("Matrice d'adjacence (réordonnée par communauté détectée)")
ax3.set_xlabel('Nœud')
ax3.set_ylabel('Nœud')
# Lignes de séparation entre communautés
cumsum = 0
for c in range(n_comm_det - 1):
    cumsum += len([n for n in G.nodes() if comm_detected_dict[n] == c])
    ax3.axhline(cumsum - 0.5, color='blue', linewidth=1.5)
    ax3.axvline(cumsum - 0.5, color='blue', linewidth=1.5)
plt.colorbar(im, ax=ax3, shrink=0.6, label='Poids')

# --- 4. Comparaison communautés réelles vs détectées ---
ax4 = fig.add_subplot(2, 2, 4)
x_pos = np.arange(n_communities)
width = 0.35
sizes_gt = [sum(1 for n in G.nodes() if G.nodes[n]['communaute'] == i) for i in range(n_communities)]
# Mapper les détectées vers les réelles pour la comparaison visuelle
sizes_det_mapped = [0] * n_communities
for det_id in range(n_comm_det):
    nodes_in_det = [n for n in G.nodes() if G.nodes[n]['communaute_detectee'] == det_id]
    gt_in_det = [G.nodes[n]['communaute'] for n in nodes_in_det]
    most_common_gt = Counter(gt_in_det).most_common(1)[0][0]
    sizes_det_mapped[most_common_gt] += len(nodes_in_det)

bars1 = ax4.bar(x_pos - width/2, sizes_gt, width, label='Réelles (ground truth)', color='lightblue', edgecolor='black')
bars2 = ax4.bar(x_pos + width/2, sizes_det_mapped, width, label='Détectées (Louvain)', color='lightcoral', edgecolor='black')
ax4.set_xticks(x_pos)
ax4.set_xticklabels(comm_names)
ax4.set_ylabel('Nombre de nœuds')
ax4.set_title('Taille des communautés : Réelles vs Détectées')
ax4.legend()
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(My_dir/"02_rapport_analyse.png", dpi=200, bbox_inches='tight')
plt.close()
print("Figure 02_rapport_analyse.png sauvegardée")


# ==============================================================================
# SYNTHÈSE DES RÉSULTATS
# ==============================================================================
print("\n" + "=" * 70)
print("SYNTHÈSE DES RÉSULTATS")
print("=" * 70)
print(f"""
RÉSEAU SOCIAL FICTIF — RAPPORT FINAL
─────────────────────────────────────
• Nœuds                : {N}
• Arêtes               : {G.number_of_edges()}
• Densité              : {nx.density(G):.4f}
• Connexe              : {nx.is_connected(G)}
• Degré moyen          : {deg_vals.mean():.2f}
• Clustering moyen     : {nx.average_clustering(G):.4f}
• Modularité (Louvain) : {modularity:.4f}

TOP 5 INFLUENÇEURS (PageRank) :
  1. {G.nodes[top5_nodes[0]]['nom']} (PR={pr[top5_nodes[0]]:.4f})
  2. {G.nodes[top5_nodes[1]]['nom']} (PR={pr[top5_nodes[1]]:.4f})
  3. {G.nodes[top5_nodes[2]]['nom']} (PR={pr[top5_nodes[2]]:.4f})
  4. {G.nodes[top5_nodes[3]]['nom']} (PR={pr[top5_nodes[3]]:.4f})
  5. {G.nodes[top5_nodes[4]]['nom']} (PR={pr[top5_nodes[4]]:.4f})

COMMUNAUTÉS DÉTECTÉES :
  • {len(communities_detected)} groupes trouvés par l'algorithme de Louvain
  • Forte correspondance avec les communautés réelles (homophilie)
""")

print("\n" + "=" * 70)
print("FIN DU JOUR 8 — Projet intégré 1 exécuté avec succès !")
print("=" * 70)
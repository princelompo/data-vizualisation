"""
MINI-PROJET FINAL : PLATEFORME D'ANALYSE DE RÉSEAUX
====================================================
Objectif : Créer un outil complet d'analyse de réseau qui intègre
tous les concepts vus pendant la formation.
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.gridspec import GridSpec
from networkx.algorithms import community
import pandas as pd
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("MINI-PROJET FINAL : PLATEFORME D'ANALYSE DE RÉSEAUX")
print("=" * 80)
print("\n" + "=" * 80)

# ============================================
# 1. MODULE DE GÉNÉRATION DE GRAPHES
# ============================================

class GraphGenerator:
    """Génère différents types de graphes pour l'analyse"""
    
    @staticmethod
    def generate_social_network(n_nodes=50, p_connect=0.15):
        """Génère un réseau social"""
        G = nx.Graph()
        
        # Ajout des nœuds avec attributs
        departments = ['IT', 'RH', 'Finance', 'Marketing', 'R&D', 'Commercial']
        for i in range(n_nodes):
            G.add_node(i,
                      name=f"User_{i:02d}",
                      department=np.random.choice(departments),
                      age=np.random.randint(22, 60),
                      seniority=np.random.randint(0, 20))
        
        # Ajout des arêtes
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                # Probabilité basée sur le département et l'âge
                prob = p_connect
                if G.nodes[i]['department'] == G.nodes[j]['department']:
                    prob *= 1.5
                if abs(G.nodes[i]['age'] - G.nodes[j]['age']) < 5:
                    prob *= 1.3
                
                if np.random.random() < prob:
                    G.add_edge(i, j, weight=np.random.randint(1, 10))
        
        return G
    
    @staticmethod
    def generate_transport_network(n_cities=20):
        """Génère un réseau de transport"""
        G = nx.Graph()
        
        # Coordonnées des villes
        cities = [f"City_{i:02d}" for i in range(n_cities)]
        pos = {city: (np.random.randn(), np.random.randn()) for city in cities}
        
        for city in cities:
            G.add_node(city, pos=pos[city], population=np.random.randint(50000, 2000000))
        
        # Ajout des routes
        for i in range(n_cities):
            for j in range(i+1, n_cities):
                dist = np.sqrt((pos[cities[i]][0] - pos[cities[j]][0])**2 + 
                             (pos[cities[i]][1] - pos[cities[j]][1])**2)
                prob = 0.3 * np.exp(-dist * 0.5)
                
                if np.random.random() < prob:
                    G.add_edge(cities[i], cities[j],
                              distance=dist * 100 + np.random.randint(10, 50),
                              cost=dist * 100 + np.random.randint(20, 80),
                              time=dist * 80 + np.random.randint(10, 40))
        
        return G
    
    @staticmethod
    def generate_scale_free_network(n_nodes=100, m=3):
        """Génère un réseau scale-free (Barabási-Albert)"""
        G = nx.barabasi_albert_graph(n_nodes, m)
        
        # Ajout d'attributs
        for node in G.nodes():
            G.nodes[node]['degree'] = G.degree(node)
            G.nodes[node]['cluster'] = nx.clustering(G, node)
        
        return G
    
    @staticmethod
    def generate_community_network(n_nodes=80, n_communities=4, p_in=0.3, p_out=0.02):
        """Génère un réseau avec structure de communautés"""
        G = nx.Graph()
        
        # Création des communautés
        community_sizes = [n_nodes // n_communities] * n_communities
        community_sizes[-1] += n_nodes - sum(community_sizes)
        
        node_to_community = {}
        node_id = 0
        
        for comm_id, size in enumerate(community_sizes):
            for _ in range(size):
                G.add_node(node_id, community=comm_id)
                node_to_community[node_id] = comm_id
                node_id += 1
        
        # Ajout des arêtes
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                if node_to_community[i] == node_to_community[j]:
                    prob = p_in
                else:
                    prob = p_out
                
                if np.random.random() < prob:
                    G.add_edge(i, j)
        
        return G

# ============================================
# 2. MODULE D'ANALYSE DE GRAPHES
# ============================================

class GraphAnalyzer:
    """Analyse les propriétés des graphes"""
    
    def __init__(self, G):
        self.G = G
        self.results = {}
    
    def analyze_basic_properties(self):
        """Analyse les propriétés de base"""
        self.results['basic'] = {
            'n_nodes': self.G.number_of_nodes(),
            'n_edges': self.G.number_of_edges(),
            'density': nx.density(self.G),
            'is_connected': nx.is_connected(self.G),
            'diameter': nx.diameter(self.G) if nx.is_connected(self.G) else None,
            'avg_degree': np.mean([d for n, d in self.G.degree()]),
            'avg_clustering': nx.average_clustering(self.G),
            'n_components': nx.number_connected_components(self.G)
        }
        return self.results['basic']
    
    def analyze_centralities(self):
        """Calcule toutes les centralités"""
        self.results['centralities'] = {
            'degree': nx.degree_centrality(self.G),
            'betweenness': nx.betweenness_centrality(self.G),
            'closeness': nx.closeness_centrality(self.G),
            'eigenvector': nx.eigenvector_centrality(self.G, max_iter=1000),
            'pagerank': nx.pagerank(self.G, alpha=0.85)
        }
        return self.results['centralities']
    
    def analyze_communities(self):
        """Détecte les communautés"""
        try:
            communities = community.louvain_communities(self.G, seed=42)
            self.results['communities'] = {
                'n_communities': len(communities),
                'communities': communities,
                'modularity': community.modularity(self.G, communities),
                'sizes': [len(c) for c in communities]
            }
        except:
            self.results['communities'] = None
        return self.results['communities']
    
    def analyze_paths(self, source=None, target=None):
        """Analyse les chemins"""
        if source is None or target is None:
            # Choisir deux nœuds éloignés
            if nx.is_connected(self.G):
                nodes = list(self.G.nodes())
                source = nodes[0]
                target = nodes[-1]
                try:
                    path = nx.shortest_path(self.G, source=source, target=target)
                    length = nx.shortest_path_length(self.G, source=source, target=target)
                except:
                    path = None
                    length = None
            else:
                path = None
                length = None
        else:
            try:
                path = nx.shortest_path(self.G, source=source, target=target)
                length = nx.shortest_path_length(self.G, source=source, target=target)
            except:
                path = None
                length = None
        
        self.results['paths'] = {
            'source': source,
            'target': target,
            'path': path,
            'length': length
        }
        
        if nx.is_connected(self.G):
            self.results['paths']['avg_length'] = nx.average_shortest_path_length(self.G)
        else:
            self.results['paths']['avg_length'] = None
        
        return self.results['paths']
    
    def get_summary(self):
        """Retourne un résumé complet"""
        self.analyze_basic_properties()
        self.analyze_centralities()
        self.analyze_communities()
        self.analyze_paths()
        return self.results

# ============================================
# 3. MODULE DE VISUALISATION
# ============================================

class GraphVisualizer:
    """Visualise les graphes avec différentes options"""
    
    def __init__(self, G):
        self.G = G
        self.pos = self._get_layout()
    
    def _get_layout(self):
        """Détermine le meilleur layout"""
        if self.G.number_of_nodes() < 50:
            return nx.spring_layout(self.G, seed=42)
        else:
            return nx.spring_layout(self.G, seed=42, k=0.3, iterations=50)
    
    def plot_overview(self, title="Vue d'ensemble du réseau"):
        """Vue d'ensemble du réseau"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Graphe principal
        ax = axes[0, 0]
        nx.draw(self.G, self.pos, ax=ax,
                node_size=100, node_color='lightblue',
                edge_color='gray', alpha=0.6,
                with_labels=False)
        ax.set_title('Vue d\'ensemble', fontsize=12, fontweight='bold')
        ax.axis('off')
        
        # 2. Distribution des degrés
        ax = axes[0, 1]
        degrees = [d for n, d in self.G.degree()]
        ax.hist(degrees, bins=range(1, max(degrees)+2),
               edgecolor='black', alpha=0.7, color='steelblue')
        ax.set_xlabel('Degré', fontsize=10)
        ax.set_ylabel('Fréquence', fontsize=10)
        ax.set_title('Distribution des degrés', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 3. Centralité de degré
        ax = axes[1, 0]
        degree_cent = nx.degree_centrality(self.G)
        node_colors = [degree_cent[n] for n in self.G.nodes()]
        nx.draw(self.G, self.pos, ax=ax,
                node_color=node_colors, cmap='viridis',
                node_size=150, edge_color='gray', alpha=0.6,
                with_labels=False)
        ax.set_title('Centralité de degré', fontsize=12, fontweight='bold')
        ax.axis('off')
        
        # 4. Informations statistiques
        ax = axes[1, 1]
        ax.axis('off')
        
        stats = [
            f"Nœuds: {self.G.number_of_nodes()}",
            f"Arêtes: {self.G.number_of_edges()}",
            f"Densité: {nx.density(self.G):.4f}",
            f"Connexe: {'Oui' if nx.is_connected(self.G) else 'Non'}",
        ]
        
        if nx.is_connected(self.G):
            stats.append(f"Diamètre: {nx.diameter(self.G)}")
        
        stats.extend([
            f"Degré moyen: {np.mean([d for n,d in self.G.degree()]):.2f}",
            f"Clustering moyen: {nx.average_clustering(self.G):.4f}"
        ])
        
        y_pos = 0.9
        for stat in stats:
            ax.text(0.1, y_pos, stat, fontsize=12, transform=ax.transAxes)
            y_pos -= 0.08
        
        plt.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        return fig
    
    def plot_centralities_comparison(self):
        """Compare les différentes centralités"""
        analyzer = GraphAnalyzer(self.G)
        centralities = analyzer.analyze_centralities()
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        
        for ax, (name, cent) in zip(axes.flat, centralities.items()):
            values = np.array(list(cent.values()))
            normalized = values / values.max() if values.max() > 0 else values
            
            node_colors = plt.cm.plasma(normalized)
            node_sizes = 100 + 400 * normalized
            
            nx.draw(self.G, self.pos, ax=ax,
                    node_color=node_colors,
                    node_size=node_sizes,
                    edge_color='gray', alpha=0.6,
                    with_labels=False)
            
            ax.set_title(f'Centralité de {name}', fontsize=12, fontweight='bold')
            ax.axis('off')
        
        plt.suptitle('Comparaison des centralités', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        return fig
    
    def plot_communities(self):
        """Visualise les communautés"""
        analyzer = GraphAnalyzer(self.G)
        comm_data = analyzer.analyze_communities()
        
        if comm_data is None:
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.text(0.5, 0.5, 'Pas de communautés détectées', 
                   fontsize=16, ha='center', va='center')
            ax.axis('off')
            return fig
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        
        # 1. Visualisation des communautés
        ax = axes[0]
        communities = comm_data['communities']
        
        # Couleurs pour les communautés
        colors = plt.cm.tab20(np.linspace(0, 1, len(communities)))
        node_colors = {}
        for i, comm in enumerate(communities):
            for node in comm:
                node_colors[node] = colors[i]
        
        node_colors_list = [node_colors[n] for n in self.G.nodes()]
        
        nx.draw(self.G, self.pos, ax=ax,
                node_color=node_colors_list,
                node_size=150,
                edge_color='gray', alpha=0.6,
                with_labels=False)
        
        # Ajout des labels des communautés
        for i, comm in enumerate(communities):
            comm_pos = np.mean([self.pos[n] for n in comm], axis=0)
            ax.text(comm_pos[0], comm_pos[1], f'C{i+1}',
                   fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.set_title(f'Communautés ({len(communities)} groupes)', 
                    fontsize=12, fontweight='bold')
        ax.axis('off')
        
        # 2. Statistiques des communautés
        ax = axes[1]
        ax.axis('off')
        
        sizes = comm_data['sizes']
        y_pos = 0.9
        ax.text(0.1, y_pos, f"Nombre de communautés: {comm_data['n_communities']}",
               fontsize=12, fontweight='bold')
        y_pos -= 0.08
        ax.text(0.1, y_pos, f"Modularité: {comm_data['modularity']:.4f}",
               fontsize=12)
        y_pos -= 0.08
        ax.text(0.1, y_pos, f"Tailles: {sizes}", fontsize=12)
        y_pos -= 0.08
        ax.text(0.1, y_pos, f"Moyenne: {np.mean(sizes):.1f}", fontsize=12)
        y_pos -= 0.08
        ax.text(0.1, y_pos, f"Médiane: {np.median(sizes):.0f}", fontsize=12)
        y_pos -= 0.08
        ax.text(0.1, y_pos, f"Écart-type: {np.std(sizes):.2f}", fontsize=12)
        
        plt.suptitle('Détection de communautés', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        return fig
    
    def plot_path_analysis(self, source=None, target=None):
        """Visualise l'analyse des chemins"""
        analyzer = GraphAnalyzer(self.G)
        path_data = analyzer.analyze_paths(source, target)
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        
        # 1. Plus court chemin
        ax = axes[0]
        nx.draw(self.G, self.pos, ax=ax,
                node_color='lightblue', node_size=200,
                edge_color='gray', alpha=0.3,
                with_labels=False)
        
        if path_data['path']:
            path = path_data['path']
            path_edges = list(zip(path, path[1:]))
            
            nx.draw_networkx_edges(self.G, self.pos, edgelist=path_edges,
                                  edge_color='red', width=4, ax=ax)
            nx.draw_networkx_nodes(self.G, self.pos, nodelist=path,
                                  node_color='red', node_size=300, ax=ax)
            
            ax.set_title(f'Plus court chemin ({path_data["source"]} → {path_data["target"]})',
                        fontsize=12, fontweight='bold')
        else:
            ax.set_title('Pas de chemin trouvé', fontsize=12, fontweight='bold')
        
        ax.axis('off')
        
        # 2. Statistiques des chemins
        ax = axes[1]
        ax.axis('off')
        
        stats = [
            f"Source: {path_data['source']}",
            f"Cible: {path_data['target']}",
            f"Longueur: {path_data['length'] if path_data['length'] else 'N/A'}",
        ]
        
        if path_data['avg_length']:
            stats.append(f"Longueur moyenne: {path_data['avg_length']:.3f}")
        
        if nx.is_connected(self.G):
            stats.append(f"Diamètre: {nx.diameter(self.G)}")
            stats.append(f"Rayon: {nx.radius(self.G)}")
        
        y_pos = 0.9
        for stat in stats:
            ax.text(0.1, y_pos, stat, fontsize=12)
            y_pos -= 0.08
        
        plt.suptitle('Analyse des chemins', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        return fig
    
    def create_dashboard(self, title="Tableau de bord - Analyse de réseau"):
        """Crée un tableau de bord complet"""
        fig = plt.figure(figsize=(18, 12))
        gs = GridSpec(3, 4, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. Vue d'ensemble (2x2)
        ax1 = fig.add_subplot(gs[:2, :2])
        nx.draw(self.G, self.pos, ax=ax1,
                node_size=80, node_color='lightblue',
                edge_color='gray', alpha=0.5,
                with_labels=False)
        ax1.set_title('Réseau', fontsize=14, fontweight='bold')
        ax1.axis('off')
        
        # 2. Distribution des degrés
        ax2 = fig.add_subplot(gs[2, 0])
        degrees = [d for n, d in self.G.degree()]
        ax2.hist(degrees, bins=range(1, max(degrees)+2),
                edgecolor='black', alpha=0.7, color='steelblue')
        ax2.set_xlabel('Degré', fontsize=10)
        ax2.set_ylabel('Fréquence', fontsize=10)
        ax2.set_title('Distribution des degrés', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # 3. Centralité de degré
        ax3 = fig.add_subplot(gs[2, 1])
        degree_cent = nx.degree_centrality(self.G)
        node_colors = [degree_cent[n] for n in self.G.nodes()]
        nx.draw(self.G, self.pos, ax=ax3,
                node_color=node_colors, cmap='viridis',
                node_size=100, edge_color='gray', alpha=0.5,
                with_labels=False)
        ax3.set_title('Centralité de degré', fontsize=12, fontweight='bold')
        ax3.axis('off')
        
        # 4. Communautés (si disponibles)
        ax4 = fig.add_subplot(gs[:2, 2])
        try:
            communities = community.louvain_communities(self.G, seed=42)
            colors = plt.cm.tab20(np.linspace(0, 1, len(communities)))
            node_colors_comm = {}
            for i, comm in enumerate(communities):
                for node in comm:
                    node_colors_comm[node] = colors[i]
            node_colors_list = [node_colors_comm[n] for n in self.G.nodes()]
            
            nx.draw(self.G, self.pos, ax=ax4,
                    node_color=node_colors_list,
                    node_size=80, edge_color='gray', alpha=0.5,
                    with_labels=False)
            ax4.set_title(f'Communautés ({len(communities)})', 
                         fontsize=12, fontweight='bold')
        except:
            nx.draw(self.G, self.pos, ax=ax4,
                    node_size=80, node_color='lightgray',
                    edge_color='gray', alpha=0.5,
                    with_labels=False)
            ax4.set_title('Communautés (non détectées)', 
                         fontsize=12, fontweight='bold')
        ax4.axis('off')
        
        # 5. Plus court chemin
        ax5 = fig.add_subplot(gs[2, 2])
        if nx.is_connected(self.G):
            nodes = list(self.G.nodes())
            source, target = nodes[0], nodes[-1]
            try:
                path = nx.shortest_path(self.G, source=source, target=target)
                path_edges = list(zip(path, path[1:]))
                
                nx.draw(self.G, self.pos, ax=ax5,
                        node_color='lightgray', node_size=80,
                        edge_color='gray', alpha=0.3,
                        with_labels=False)
                nx.draw_networkx_edges(self.G, self.pos, edgelist=path_edges,
                                      edge_color='red', width=3, ax=ax5)
                nx.draw_networkx_nodes(self.G, self.pos, nodelist=path,
                                      node_color='red', node_size=120, ax=ax5)
                ax5.set_title(f'Chemin {source}→{target}', 
                             fontsize=12, fontweight='bold')
            except:
                ax5.set_title('Pas de chemin', fontsize=12, fontweight='bold')
        else:
            ax5.set_title('Graphe non connexe', fontsize=12, fontweight='bold')
        ax5.axis('off')
        
        # 6. Statistiques (côté droit)
        ax6 = fig.add_subplot(gs[:2, 3])
        ax6.axis('off')
        
        stats = [
            f"Propriétés du réseau",
            "-" * 30,
            f"Nœuds: {self.G.number_of_nodes()}",
            f"Arêtes: {self.G.number_of_edges()}",
            f"Densité: {nx.density(self.G):.4f}",
            f"Connexe: {'Oui' if nx.is_connected(self.G) else 'Non'}",
            f"Degré moyen: {np.mean([d for n,d in self.G.degree()]):.2f}",
            f"Clustering: {nx.average_clustering(self.G):.4f}",
            "",
            f"Centralités (top)",
            "-" * 30,
        ]
        
        # Top centralité
        cent = nx.degree_centrality(self.G)
        top_node = max(cent.items(), key=lambda x: x[1])
        stats.append(f"Degré max: {top_node[0]} ({top_node[1]:.3f})")
        
        cent = nx.betweenness_centrality(self.G)
        top_node = max(cent.items(), key=lambda x: x[1])
        stats.append(f"Betweenness: {top_node[0]} ({top_node[1]:.3f})")
        
        if nx.is_connected(self.G):
            stats.append(f"Diamètre: {nx.diameter(self.G)}")
        
        y_pos = 0.95
        for stat in stats:
            ax6.text(0.1, y_pos, stat, fontsize=11, transform=ax6.transAxes)
            y_pos -= 0.04
        
        # 7. Évolution (placeholder)
        ax7 = fig.add_subplot(gs[2, 3])
        ax7.axis('off')
        ax7.text(0.5, 0.5, 'Analyse terminée', 
                fontsize=14, ha='center', va='center')
        
        plt.suptitle(title, fontsize=18, fontweight='bold', y=1.02)
        return fig

# ============================================
# 4. APPLICATION PRINCIPALE
# ============================================

class NetworkAnalysisApp:
    """Application principale d'analyse de réseau"""
    
    def __init__(self):
        self.G = None
        self.analyzer = None
        self.visualizer = None
    
    def load_graph(self, G):
        """Charge un graphe"""
        self.G = G
        self.analyzer = GraphAnalyzer(G)
        self.visualizer = GraphVisualizer(G)
        return self
    
    def generate_graph(self, graph_type='social', **kwargs):
        """Génère un graphe selon le type"""
        if graph_type == 'social':
            self.G = GraphGenerator.generate_social_network(**kwargs)
        elif graph_type == 'transport':
            self.G = GraphGenerator.generate_transport_network(**kwargs)
        elif graph_type == 'scale_free':
            self.G = GraphGenerator.generate_scale_free_network(**kwargs)
        elif graph_type == 'communities':
            self.G = GraphGenerator.generate_community_network(**kwargs)
        else:
            raise ValueError(f"Type de graphe inconnu: {graph_type}")
        
        self.analyzer = GraphAnalyzer(self.G)
        self.visualizer = GraphVisualizer(self.G)
        return self
    
    def analyze(self):
        """Analyse complète du graphe"""
        if self.G is None:
            raise ValueError("Aucun graphe chargé")
        return self.analyzer.get_summary()
    
    def visualize(self, plot_type='dashboard', **kwargs):
        """Visualise le graphe"""
        if self.G is None:
            raise ValueError("Aucun graphe chargé")
        
        if plot_type == 'overview':
            return self.visualizer.plot_overview(**kwargs)
        elif plot_type == 'centralities':
            return self.visualizer.plot_centralities_comparison()
        elif plot_type == 'communities':
            return self.visualizer.plot_communities()
        elif plot_type == 'paths':
            return self.visualizer.plot_path_analysis(**kwargs)
        elif plot_type == 'dashboard':
            return self.visualizer.create_dashboard(**kwargs)
        else:
            raise ValueError(f"Type de visualisation inconnu: {plot_type}")
    
    def export_results(self, prefix="network_analysis"):
        """Exporte les résultats"""
        if self.G is None:
            raise ValueError("Aucun graphe chargé")
        
        # Export du graphe
        nx.write_graphml(self.G, f"{prefix}.graphml")
        
        # Export des données
        nodes_data = []
        for node in self.G.nodes():
            data = {'node': node}
            data.update(self.G.nodes[node])
            nodes_data.append(data)
        
        edges_data = []
        for u, v, data in self.G.edges(data=True):
            edges_data.append({'source': u, 'target': v, **data})
        
        pd.DataFrame(nodes_data).to_csv(f"{prefix}_nodes.csv", index=False)
        pd.DataFrame(edges_data).to_csv(f"{prefix}_edges.csv", index=False)
        
        print(f"✓ Résultats exportés avec préfixe '{prefix}'")

# ============================================
# 5. DÉMONSTRATION COMPLÈTE
# ============================================

print("\n" + "=" * 80)
print("DÉMONSTRATION DE L'APPLICATION")
print("=" * 80)

# Création de l'application
app = NetworkAnalysisApp()

# Test 1: Réseau social
print("\n1. ANALYSE D'UN RÉSEAU SOCIAL")
print("-" * 40)

app.generate_graph('social', n_nodes=50, p_connect=0.12)
results = app.analyze()

print("Propriétés de base:")
basic = results['basic']
print(f"  Nœuds: {basic['n_nodes']}")
print(f"  Arêtes: {basic['n_edges']}")
print(f"  Densité: {basic['density']:.4f}")
print(f"  Degré moyen: {basic['avg_degree']:.2f}")
print(f"  Connexe: {'Oui' if basic['is_connected'] else 'Non'}")

if results['communities']:
    print(f"  Communautés: {results['communities']['n_communities']}")
    print(f"  Modularité: {results['communities']['modularity']:.4f}")

# Visualisations
fig1 = app.visualize('dashboard', title="Réseau Social - Analyse complète")
fig1.savefig('social_network_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Dashboard sauvegardé : social_network_dashboard.png")

fig2 = app.visualize('centralities')
fig2.savefig('social_network_centralities.png', dpi=300, bbox_inches='tight')
print("✓ Centralités sauvegardées : social_network_centralities.png")

# Test 2: Réseau de transport
print("\n2. ANALYSE D'UN RÉSEAU DE TRANSPORT")
print("-" * 40)

app.generate_graph('transport', n_cities=25)
results = app.analyze()

print("Propriétés de base:")
basic = results['basic']
print(f"  Nœuds: {basic['n_nodes']}")
print(f"  Arêtes: {basic['n_edges']}")
print(f"  Densité: {basic['density']:.4f}")
print(f"  Degré moyen: {basic['avg_degree']:.2f}")
print(f"  Connexe: {'Oui' if basic['is_connected'] else 'Non'}")

fig3 = app.visualize('overview', title="Réseau de Transport")
fig3.savefig('transport_network_overview.png', dpi=300, bbox_inches='tight')
print("✓ Vue d'ensemble sauvegardée : transport_network_overview.png")

fig4 = app.visualize('paths', source='City_00', target='City_19')
fig4.savefig('transport_network_paths.png', dpi=300, bbox_inches='tight')
print("✓ Analyse des chemins sauvegardée : transport_network_paths.png")

# Test 3: Réseau avec communautés
print("\n3. ANALYSE D'UN RÉSEAU AVEC COMMUNAUTÉS")
print("-" * 40)

app.generate_graph('communities', n_nodes=80, n_communities=4, p_in=0.3, p_out=0.02)
results = app.analyze()

print("Propriétés de base:")
basic = results['basic']
print(f"  Nœuds: {basic['n_nodes']}")
print(f"  Arêtes: {basic['n_edges']}")

if results['communities']:
    print(f"  Communautés détectées: {results['communities']['n_communities']}")
    print(f"  Tailles: {results['communities']['sizes']}")
    print(f"  Modularité: {results['communities']['modularity']:.4f}")

fig5 = app.visualize('communities')
fig5.savefig('community_network_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Analyse des communautés sauvegardée : community_network_analysis.png")

# Test 4: Scale-free network
print("\n4. ANALYSE D'UN RÉSEAU SCALE-FREE")
print("-" * 40)

app.generate_graph('scale_free', n_nodes=100, m=2)
results = app.analyze()

print("Propriétés de base:")
basic = results['basic']
print(f"  Nœuds: {basic['n_nodes']}")
print(f"  Arêtes: {basic['n_edges']}")
print(f"  Densité: {basic['density']:.4f}")
print(f"  Degré moyen: {basic['avg_degree']:.2f}")

if results['communities']:
    print(f"  Communautés: {results['communities']['n_communities']}")

fig6 = app.visualize('overview', title="Réseau Scale-Free")
fig6.savefig('scale_free_network.png', dpi=300, bbox_inches='tight')
print("✓ Vue d'ensemble sauvegardée : scale_free_network.png")

# Export des résultats
app.export_results("final_analysis")
print("✓ Résultats exportés")

# ============================================
# 6. RAPPORT FINAL
# ============================================

print("\n" + "=" * 80)
print("RAPPORT FINAL - MINI-PROJET D'ANALYSE DE RÉSEAUX")
print("=" * 80)

print("""
COMPÉTENCES DÉMONTRÉES:
1. Génération de différents types de graphes
2. Analyse des propriétés de base (degrés, densité, connexité)
3. Calcul des mesures de centralité (5 méthodes)
4. Détection de communautés (Louvain)
5. Analyse des plus courts chemins
6. Visualisation avancée avec Matplotlib
7. Export des données pour analyses futures

FONCTIONNALITÉS IMPLÉMENTÉES:
- Module de génération de graphes
- Module d'analyse complète
- Module de visualisation multi-vues
- Interface cohérente et réutilisable
- Support de différents types de réseaux

MÉTHODES UTILISÉES:
- NetworkX pour la manipulation de graphes
- Matplotlib pour la visualisation
- Pandas pour l'export de données
- NumPy pour les calculs numériques

APPLICATIONS POTENTIELLES:
- Analyse de réseaux sociaux
- Optimisation de réseaux de transport
- Détection de communautés
- Identification d'influenceurs
- Analyse de graphes biologiques ou technologiques
- Génération de rapports automatisés pour la prise de décision
- Visualisation interactive pour la présentation des résultats
- Intégration dans des pipelines d'analyse de données
- Extension pour l'analyse de graphes dynamiques
- Déploiement en tant qu'application web pour l'analyse de réseaux
- Intégration avec des bases de données pour l'analyse de grands graphes
- Développement de fonctionnalités d'export avancées (JSON, Excel)
- Ajout de tests unitaires pour la validation des modules
- Documentation complète pour l'utilisation et l'extension de l'outil
- Optimisation des performances pour les grands graphes
- Utilisation de techniques de visualisation avancées (3D, animations)
- Développement d'une interface utilisateur graphique (GUI)
- Intégration avec des bibliothèques de machine learning pour l'analyse prédictive
- Création de tutoriels et d'exemples pour faciliter l'apprentissage
- Mise en place d'un système de logging pour le suivi des analyses
- Développement de fonctionnalités de filtrage et de recherche dans les graphes
- Ajout de fonctionnalités d'interaction pour explorer les graphes
- Développement d'algorithmes personnalisés pour l'analyse de graphes spécifiques
- Intégration avec des outils de visualisation interactifs (Plotly, Bokeh)
""")    
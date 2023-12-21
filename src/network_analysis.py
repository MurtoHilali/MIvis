import networkx as nx

def create_protein_network():
    G = nx.Graph()
    return G

def add_protein_node(G, protein_name, protein_obj):
    G.add_node(protein_name, protein=protein_obj)

def add_interaction_edge(G, protein1_name, protein2_name, interaction_obj):
    G.add_edge(protein1_name, protein2_name, interaction=interaction_obj)

def add_missense_edge(G, wt_protein_name, variant_protein_name, mutation_code):
    G.add_edge(wt_protein_name, variant_protein_name, mutation=mutation_code)

# Additional functions for network analysis and manipulation

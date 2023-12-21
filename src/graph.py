import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G):
    """
    Draws the graph G using matplotlib.

    Parameters:
    - G (networkx.Graph): The graph to be drawn.
    """
    # Set font
    plt.rcParams['font.family'] = 'Open Sans'
    
    # Define node labels and colors
    labels = {}
    for node, data in G.nodes(data=True):
        protein = data['protein']
        labels[node] = f"{protein.name}\n{protein.variant_code}" if protein.variant_code else protein.name
    
    # Define edge colors and labels
    edge_colors = []
    edge_labels = {}
    for u, v, data in G.edges(data=True):
        if 'interaction' in data:
            interaction = data['interaction']
            edge_labels[(u, v)] = (
                f"Interacting residues: {interaction.bait_residues}, "
                f"{interaction.candidate_residues}\nf: {interaction.metrics['f1']}"
            )
            edge_colors.append('red' if interaction.is_variant_interaction else 'black')
        elif 'type' in data and data['type'] == 'missense':
            edge_labels[(u, v)] = f"Missense mutation: {data['variant_code']}"
            edge_colors.append('blue')
        else:
            edge_labels[(u, v)] = "Unknown edge type"
            edge_colors.append('grey')
    
    # Define node positions using shell_layout
    bait_and_variants = [node for node, data in G.nodes(data=True) if data['protein'].name == "P73880"]
    candidates = list(set(G.nodes) - set(bait_and_variants))
    shells = [bait_and_variants, candidates]
    pos = nx.shell_layout(G, shells)
    
    # Draw nodes, edges, and labels
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color=edge_colors)
    nx.draw_networkx_labels(G, pos, labels, font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title("Protein Interaction Graph")
    plt.axis("off")
    plt.show()
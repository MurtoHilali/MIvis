import os
import csv
import json
import networkx as nx
import pandas as pd
from src.protein import Protein
from src.interaction import Interaction
from src.graph import draw_graph

def extract_variant_code(protein_name): 
    if "_" in protein_name:
        name, variant_code = protein_name.split("_") # e.g. "CDK2_T160I" -> "CDK2", "T160I"
        return name, variant_code
    return protein_name, None

def create_protein_network(models_dir, predictions_csv):
    """
    Creates a protein network from a directory of protein models and a CSV file of structural and variant features.

    Args:
        models_dir (str): Path to directory containing protein models.
        predictions_csv (str): Path to CSV file containing structural & variant features.

    Returns:
        G (networkx.Graph): A networkx graph representing the protein network.
    """
    with open(predictions_csv, 'r') as infile:
        reader = csv.DictReader(infile)
        predictions_data = {row['jobs']: row for row in reader}
    
    G = nx.Graph()
    print(f'Entering {models_dir}')
    for protein_pair_dir in os.listdir(models_dir):
        if os.path.isdir(os.path.join(models_dir, protein_pair_dir)):
            candidate_protein, bait_protein = protein_pair_dir.split('_and_')
            interaction_data = predictions_data[protein_pair_dir]

            print(f'Now loading {bait_protein} and {candidate_protein}')
            
            # Get variant codes
            bait_protein, bait_variant_code = extract_variant_code(bait_protein)
            candidate_protein, candidate_variant_code = extract_variant_code(candidate_protein) # Note: not currently used, here for future proofing

            print(f'bait_variant_code: {bait_variant_code}, candidate_variant_code: {candidate_variant_code}')

            # Assign states
            bait_state = "variant" if bait_variant_code else "wildtype"
            candidate_state = "variant" if candidate_variant_code else "wildtype"

            print(f'bait_state: {bait_state}, candidate_state: {candidate_state}')  # Debugging line

            # Add nodes for wildtype and variant proteins
            if bait_protein not in G.nodes:
                print(f'Adding node for {bait_protein} which is {bait_state}\n')
                # Instantiate a Protein object
                protein = Protein(
                    name = bait_protein,
                    state = "wildtype"
                )
                # Add it as a node to the graph
                G.add_node(
                    bait_protein, 
                    protein = protein
                )
            
            # Bait protein is now in the graph for sure, so we check to see if it's a variant
            if bait_variant_code:
                print(f'Adding node for {bait_protein}_p.{bait_variant_code} which is: {bait_state}\n')
                G.add_node(
                    f"{bait_protein}_p.{bait_variant_code}", 
                        protein = Protein(
                        name = bait_protein, 
                        state = "variant", 
                        variant_code = bait_variant_code,
                        frequency = "null",
                        path_am = "null",
                        path_clinvar = "null",
                        path_revel = "null"
                    )
                )
                    # Add missense edge between wildtype and variant bait
                G.add_edge(
                    bait_protein, f"{bait_protein}_p.{bait_variant_code}",
                    type="missense", 
                    variant_code = bait_variant_code
                )
            if candidate_protein not in G.nodes:
                protein = Protein(
                    name=candidate_protein,
                    state=candidate_state,
                )
                G.add_node(
                    candidate_protein, 
                    protein=protein
                )
            
            if candidate_variant_code:
                G.add_node(f"{candidate_protein}_p.{candidate_variant_code}", protein=Protein(candidate_protein, candidate_state, candidate_variant_code))
                # Add missense edge between wildtype and variant candidate
                G.add_edge(candidate_protein, f"{candidate_protein}_p.{candidate_variant_code}", type="missense", variant_code=candidate_variant_code)

            # Add interactions            
            structure_path = os.path.join(models_dir, protein_pair_dir, "ranked_0.pdb")
            is_variant_interaction = bait_state == "variant" or candidate_state == "variant"
            variant_code = bait_variant_code or candidate_variant_code
            
            #variant_interaction = interactions_data[bait_protein][bait_variant_code]["interactions"][candidate_protein]
            print(f'Adding interaction between {bait_protein} and {candidate_protein}')
            
            interaction = Interaction(
                bait_residues = None, # take interface from PRODIGY
                candidate_residues = None, # take interface from PRODIGY
                metrics = interaction_data,
                structure_path = structure_path,
                is_variant_interaction = is_variant_interaction,
                variant_code = variant_code if is_variant_interaction else None
            )
            
            # Add interaction edge
            bait_node = f"{bait_protein}_p.{bait_variant_code}" if bait_variant_code else bait_protein
            candidate_node = f"{candidate_protein}_p.{candidate_variant_code}" if candidate_variant_code else candidate_protein
            G.add_edge(bait_node, candidate_node, interaction=interaction)
    
    return G

# Example usage
models_dir = "/path/to/output/models"
predictions_csv = "/path/to/feature_data/features.csv"

G = create_protein_network(models_dir, predictions_csv)

def encoder(obj):
    if isinstance(obj, Interaction):
        return obj.to_dict()
    elif isinstance(obj, Protein):
        return obj.to_dict()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

cytoscape_dict = nx.cytoscape_data(G)

with open('tmp.json', 'w') as outfile:
    json.dump(cytoscape_dict, outfile, default=encoder)  # provide the protein_encoder function to json.dump

with open('tmp.json', 'r') as infile:
    cytoscape_dict = json.load(infile)

for edge in cytoscape_dict['elements']['edges']:
    # If there's an 'interaction' key, move its sub-keys up one level
    if 'interaction' in edge['data']:
        for key, value in edge['data']['interaction'].items():
            edge['data'][key] = value
        # Remove the original 'interaction' key
        del edge['data']['interaction']

for node in cytoscape_dict['elements']['nodes']:
    if 'protein' in node['data']:
        for key, value in node['data']['protein'].items():
            node['data'][key] = value
        del node['data']['protein']

styles = [
    {
        "selector": 'node[state="wildtype"]',
        "style": {
            "background-color": "#69D2E7"
        }
    },
    {
        "selector": 'node[state="variant"]',
        "style": {
            "background-color": "#F38630"
        }
    },
    {
        "selector": 'edge[?is_variant_interaction]',
        "style": {
            "line-color": "#E94C6F"
        }
    }
]

# Add classes to nodes and edges
for node in cytoscape_dict['elements']['nodes']:
    if 'protein' in node['data']:
        for key, value in node['data']['protein'].items():
            node['data'][key] = value
        # Assign class based on protein state
        node['classes'] = node['data']['state']
        del node['data']['protein']

for edge in cytoscape_dict['elements']['edges']:
    if 'interaction' in edge['data']:
        for key, value in edge['data']['interaction'].items():
            edge['data'][key] = value
        # Remove the original 'interaction' key
        del edge['data']['interaction']
        # Assign class if it's a variant interaction
        if edge['data'].get('is_variant_interaction'):
            edge['classes'] = 'variant_interaction'

# Include styles in the JSON output
cytoscape_json_output = {
    'elements': cytoscape_dict['elements'],
    'style': styles  # Add styles here
}

with open('cytoscape.json', 'w') as outfile:
    json.dump(cytoscape_json_output, outfile)
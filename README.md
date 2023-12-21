# MIvis: A Protein Network Analysis Tool

## Overview

This Protein Network Analysis Tool is designed to create and analyze protein networks based on structural and variant features. It utilizes protein models and predictions from AlphaPulldown output to generate a network that can be visualized and studied for various protein interactions, particularly focusing on variant and wildtype interactions.

## Requirements

- Python 3.x
- Libraries:
  - `os`
  - `csv`
  - `json`
  - `networkx`
  - `pandas`

## Installation

Ensure that Python 3.x is installed on your system. Install the required libraries using pip:

```bash
pip install networkx pandas
```

## Usage

### Modules

1. `src.protein`: Defines the `Protein` class.
2. `src.interaction`: Defines the `Interaction` class.
3. `src.graph`: Contains the `draw_graph` function for visualizing the protein network.

### Classes

#### `Protein`

- **Description**: Represents a protein, storing its state, variant code, structural data, and other relevant properties.
- **Attributes**:
  - `name`: Name of the protein.
  - `state`: State of the protein ('wildtype' or 'variant').
  - `variant_code`: Variant code (if applicable).
  - `pdb_structure`: PDB structure data.
  - `frequency`, `path_revel`, `path_am`, `path_clinvar`: Various properties and predictions related to the protein.
    - NOTE: temporary values, come from enrichment via a preprocessing step that is under development.
- **Methods**:
  - `add_interacting_residue(residue)`: Adds an interacting residue to the protein.
  - `get_conservation_score(residue)`: Retrieves the conservation score of a residue.
  - `get_residue_properties(residue)`: Retrieves various properties of a residue.
  - `to_dict()`: Converts the Protein object to a dictionary.
    - NOTE: most of these are TODO

#### `Interaction`

- **Description**: Represents an interaction between proteins, containing details about the interacting residues, metrics, and structure.
- **Attributes**:
  - `bait_residues`, `candidate_residues`: Lists of residues involved in the interaction.
  - `metrics`: Interaction metrics.
  - `structure_path`: Path to the PDB structure file.
  - `is_variant_interaction`: Flag indicating if it's a variant interaction.
  - `variant_code`: Variant code of the interaction.
- **Methods**:
  - `to_dict()`: Converts the Interaction object to a dictionary.
  - `get_structure()`: Retrieves the PDB structure as a string.

### Functions

#### `create_protein_network(models_dir, predictions_csv)`

- **Description**: Creates a protein network from a directory of protein models and a CSV file of predictions.
- **Inputs**:
  - `models_dir`: Path to the directory containing protein models.
  - `predictions_csv`: Path to the CSV file containing structural and variant features.
- **Output**: A `networkx.Graph` object representing the protein network.

#### `extract_variant_code(protein_name)`

- **Description**: Extracts the variant code from a protein name.
- **Input**: `protein_name`: Name of the protein.
- **Output**: Tuple of protein name and variant code.

### Workflow

1. **Data Preparation**: Ensure your protein models and predictions are in the correct format and located in the specified directories.
2. **Network Creation**:
   - Call `create_protein_network(models_dir, predictions_csv)` to generate the protein network.
3. **Data Serialization**:
   - Serialize the network into JSON format for visualization or further analysis.
4. **Visualization**:
   - Use the serialized data to visualize the network using tools like Cytoscape.

### Example Usage

```python
models_dir = "/path/to/output/models"
predictions_csv = "/path/to/feature_data/features.csv"

G = create_protein_network(models_dir, predictions_csv)
```

### Output Format

The output is a `networkx.Graph` object which can be serialized into JSON format for visualization. The graph nodes represent proteins, and the edges represent interactions between these proteins.

## Contributing

Contributions to this project are welcome. Please follow the existing coding style and add unit tests for any new or changed functionality.
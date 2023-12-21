class Protein:
    def __init__(self, name, state, variant_code=None, pdb_structure=None, 
                 frequency=None, path_revel=None, path_am=None, path_clinvar=None):
        """
        Initializes a Protein object.

        Parameters:
        - name (str): The name of the protein.
        - state (str): The state of the protein, either "wildtype" or "variant".
        - variant_code (str): The variant code if the protein is a variant, otherwise None.
        - pdb_structure (str): The PDB structure data.
        - frequency (float): The population frequency of the protein variant, None by default.
        - path_revel (float): Pathogenicity prediction from REVEL, None by default.
        - path_am (float): Pathogenicity prediction from AlphaMissense, None by default.
        - path_clinvar (str): Pathogenicity classification from ClinVar, None by default.
        """
        self.name = name
        self.state = state  # wildtype or variant
        self.variant_code = variant_code  # None for wildtype
        self.pdb_structure = pdb_structure  # PDB structure data
        self.interacting_residues = []  # List of interacting residues, if any
        self.frequency = frequency  # Population frequency of the variant
        self.path_revel = path_revel  # Pathogenicity prediction from REVEL
        self.path_am = path_am  # Pathogenicity prediction from AlphaMissense
        self.path_clinvar = path_clinvar  # Pathogenicity classification from ClinVar

    def add_interacting_residue(self, residue):
        """
        Adds an interacting residue to the protein.

        Parameters:
        - residue (str): The residue to be added.
        """
        self.interacting_residues.append(residue)

    def get_conservation_score(self, residue):
        """
        Retrieves the conservation score of a reference residue.

        Parameters:
        - residue (str): The residue for which to retrieve the conservation score.

        Returns:
        - float: The conservation score of the residue.
        """
        # Implement logic to retrieve conservation score
        # This might involve looking up a database or performing a calculation
        # For now, returning a placeholder value
        return 0.85

    def get_residue_properties(self, residue):
        """
        Retrieves the properties of a reference residue.

        Parameters:
        - residue (str): The residue for which to retrieve the properties.

        Returns:
        - dict: A dictionary containing various properties of the residue.
        """
        # Implement logic to retrieve residue properties
        # This might involve looking up a database or performing a calculation
        # For now, returning a placeholder value
        return {
            "hydrophobicity": 0.75,
            "size": "medium",
            "charge": "neutral",
            # Additional properties as needed
        }

    def to_dict(self):
        """
        Converts the Protein object to a dictionary.

        Returns:
        - dict: A dictionary representation of the Protein object.
        """
        return {
            "name": self.name,
            "state": self.state,
            "variant_code": self.variant_code,
            "pdb_structure": self.pdb_structure,
            "interacting_residues": self.interacting_residues,
            "frequency": self.frequency,
            "path_revel": self.path_revel,
            "path_am": self.path_am,
            "path_clinvar": self.path_clinvar,
        }

    @classmethod
    def from_dict(cls, dict):
        return cls(
            name=dict["name"],
            state=dict["state"],
            variant_code=dict["variant_code"],
            pdb_structure=dict["pdb_structure"],
            frequency=dict["frequency"],
            path_revel=dict["path_revel"],
            path_am=dict["path_am"],
            path_clinvar=dict["path_clinvar"]
    )

    def get_structure(self):
        """
        Retrieves the PDB structure.

        Returns:
        - str: The PDB structure as a string.
        """
        return self.pdb_structure
    # Additional methods as per your requirement

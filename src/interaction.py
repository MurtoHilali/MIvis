class Interaction:
    def __init__(self, bait_residues, candidate_residues, metrics, structure_path, is_variant_interaction=False, variant_code=None):
        """
        Initializes an Interaction object.

        Parameters:
        - bait_residues (list): List of residues involved in the interaction from the bait protein.
        - candidate_residues (list): List of residues involved in the interaction from the candidate protein.
        - metrics (dict): Interaction metrics (e.g., f).
        - structure_path (str): Path to the PDB structure file.
        - is_variant_interaction (bool): Whether the interaction is a variant interaction.
        - variant_code (str): Variant code of the variant interaction.
        """
        self.bait_residues = bait_residues
        self.candidate_residues = candidate_residues
        self.metrics = metrics
        self.structure_path = structure_path
        self.is_variant_interaction = is_variant_interaction
        self.variant_code = variant_code

    def to_dict(self):
        """
        Converts the Interaction object to a dictionary.

        Returns:
        - dict: A dictionary representation of the Interaction object.
        """
        return {
            "bait_residues": self.bait_residues,
            "candidate_residues": self.candidate_residues,
            "metrics": self.metrics,
            "structure_path": self.structure_path,
            "is_variant_interaction": self.is_variant_interaction,
            "variant_code": self.variant_code,
        }

    @classmethod
    def from_dict(cls, dict):
        """
        Creates an Interaction object from a dictionary.

        Args:
        - dict (dict): The dictionary containing the Interaction data.

        Returns:
        - Interaction: The created Interaction object.
        """
        return cls(
            bait_residues=dict["bait_residues"],
            candidate_residues=dict["candidate_residues"],
            metrics=dict["metrics"],
            structure_path=dict["structure_path"],
            is_variant_interaction=dict["is_variant_interaction"],
            variant_code=dict["variant_code"]
        )
 

    def get_structure(self):
        """
        Retrieves the PDB structure.

        Returns:
        - str: The PDB structure as a string.
        """
        with open(self.structure_path, 'r') as file:
            structure = file.read()
        return structure

    # Additional methods as per your requirement
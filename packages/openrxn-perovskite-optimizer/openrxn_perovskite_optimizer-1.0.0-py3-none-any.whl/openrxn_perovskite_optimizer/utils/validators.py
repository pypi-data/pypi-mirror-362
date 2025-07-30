def validate_composition(composition: str):
    """Validates a perovskite composition string."""
    if not composition:
        raise ValueError("Composition cannot be empty.")
    # Add more validation logic here, e.g., using pymatgen
    return True
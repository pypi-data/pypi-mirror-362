import numpy as np

# Mapping of space group numbers to lattice types
SPACE_GROUPS = {
    "P": list(range(1, 231, 1)),  # All space groups start with primitive
    "I": list(range(71, 142 + 1)),  # Body-centered
    "F": list(range(196, 230 + 1)),  # Face-centered
    "A": list(range(38, 41 + 1)),  # A-centered monoclinic
    "B": list(range(42, 46 + 1)),  # B-centered monoclinic
    "C": list(range(47, 68 + 1)),  # C-centered orthorhombic
    "R": list(range(146, 167 + 1)),  # Rhombohedral
}

def get_lattice_type(space_group):
    """ Determine the Bravais lattice type from space group number """
    for lattice, groups in SPACE_GROUPS.items():
        if space_group in groups:
            return lattice
    return "P"  # Default to Primitive if not found

def reflection_conditions_bravais(space_group, h, k, l):
    """ Apply general reflection conditions based on space group """
    lattice_type = get_lattice_type(space_group)
    
    if lattice_type == "I":  # Body-Centered
        return (h + k + l) % 2 == 0
    elif lattice_type == "F":  # Face-Centered
        return (h % 2 == k % 2 == l % 2)
    elif lattice_type == "A":  # A-Centered
        return k % 2 == l % 2
    elif lattice_type == "B":  # B-Centered
        return h % 2 == l % 2
    elif lattice_type == "C":  # C-Centered
        return h % 2 == k % 2
    elif lattice_type == "R":  # Rhombohedral in hexagonal setting
        return (-h + k + l) % 3 == 0
    return True  # Primitive (P) has no restrictions

# Define reflection conditions for glide planes
GLIDE_PLANE_CONDITIONS = {
    'a': lambda h, k, l: h % 2 == 0,
    'b': lambda h, k, l: k % 2 == 0,
    'c': lambda h, k, l: l % 2 == 0,
    'n': lambda h, k, l: (h + k) % 2 == 0 or (k + l) % 2 == 0 or (h + l) % 2 == 0,
    # 'd' glide conditions are more complex and space-group specific
}

# Define reflection conditions for screw axes
SCREW_AXIS_CONDITIONS = {
    '2_1': lambda h, k, l: h % 2 == 0 and k % 2 == 0 and l % 2 == 0,
    '3_1': lambda h, k, l: (h + k + l) % 3 == 0,
    '3_2': lambda h, k, l: (h + k + l) % 3 == 0,
    '4_1': lambda h, k, l: (h + k + l) % 4 == 0,
    '4_2': lambda h, k, l: (h + k + l) % 2 == 0,
    '4_3': lambda h, k, l: (h + k + l) % 4 == 0,
    '6_1': lambda h, k, l: (h + k + l) % 6 == 0,
    '6_2': lambda h, k, l: (h + k + l) % 3 == 0,
    '6_3': lambda h, k, l: (h + k + l) % 2 == 0,
    '6_4': lambda h, k, l: (h + k + l) % 3 == 0,
    '6_5': lambda h, k, l: (h + k + l) % 6 == 0,
}

def get_space_group_conditions(space_group_number):
    """
    Retrieve the reflection conditions for a given space group number.
    This function should map each space group number to its specific
    glide planes and screw axes.
    """
    # Placeholder for actual mapping
    space_group_conditions = {
        1: [],  # P1: No glide planes or screw axes
        2: ['a'],  # P-1: Example entry
        62: ['2_1','a','b','c']
        # Add mappings for all 230 space groups
    }
    return space_group_conditions.get(space_group_number, [])

def get_glide_screw_conditions(space_group):
    """ Assign glide plane or screw axis conditions based on space group """
    # Example mappings (should be refined based on actual space group tables)
    if space_group in range(200, 230):  # Example for F-centered cubic space groups
        return ["n"]  # Has n-glide
    elif space_group in range(150, 170):  # Example for hexagonal groups
        return [6]  # Has 6-fold screw axis
    elif space_group in range(100, 130):  # Example for tetragonal groups
        return [4]  # Has 4-fold screw axis
    return []  # Default: No additional conditions
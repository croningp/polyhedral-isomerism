"""
Various tools used for calculations and comparisons of structures
"""

import itertools

import numpy as np

import geometry
import symmetry


"""
node class: a convenient way of assigning different combinations of node positions
            and allowed bonding combinations.
            origin:  cartesian coordinates of where the node is located (defined above)
            bonds: list of vectors to neighbour nodes where bonding is present - calculated by 
                    "this node origin" - "neighbour node origin"
                An node with no bonds has an empty list, whereas an node with 3 bonds has a list
                with 3 vectors in it.
"""

np.set_printoptions(precision=2)    
np.set_printoptions(suppress=True)

class Node:

    def __init__(self, origin, bonds):
        
        self.origin = origin
        self.bonds = bonds

    def print_bonds(self):
        return np.array([i for i in self.bonds])

    def __repr__(self):
        return f"<Node:origin{self.origin}.bonds{self.print_bonds()}>"


""" simple functions to help explain purpose of algebra being applied"""    
    
def get_bond_len(node1, node2):
    v1, v2 = node1.origin, node2.origin
    bond_len = get_vector_len(v1, v2)
    return bond_len

def get_vector_len(v1, v2=[]):
    v1 = np.asarray(v1)
    v2 = np.asarray(v2)

    if len(v2) == 0:
        v2 = np.zeros(v1.shape)
    vector = v2-v1
    vector_len = np.sqrt(vector.dot(vector))
    return vector_len

def get_neighbour_origin(node, bond):
    return node.origin+bond

def get_edge_length(target_shape):
    return  min([get_vector_len(target_shape[0], a) for a in target_shape[1:]])

def sort_nodes(structure):
    for node in structure:
        sorted(node.bonds, key=lambda x: (x[0], x[1], x[2]))
    structure = sorted(structure, key=lambda x: (x.origin[2], x.origin[0], x.origin[1]))
    return structure

"""
Functions to check whether a set of atoms is permitted.
main rule is that each edge must have EXACTLY one bond
"""

def check_bond_presence(bond_vector, atom):
    for bond in atom.bonds:       
        if np.array(bond_vector==bond).all():  
            return True
    return False

def check_exactly_one_bond(atom1, atom2):
        atom1_vector = atom2.origin-atom1.origin
        atom2_vector = atom1.origin-atom2.origin
        
        bond1_exists = check_bond_presence(atom1_vector, atom1)
        bond2_exists = check_bond_presence(atom2_vector, atom2)
        
        exactly_one_bond = bond1_exists ^ bond2_exists 
        return exactly_one_bond
    
def check_allowed_combination(atom1, atom2, edge_length):
    allowed = True
    this_bond_len = get_bond_len(atom1, atom2) 
    if this_bond_len == edge_length:
        exactly_one_bond = check_exactly_one_bond(atom1, atom2)
        if not exactly_one_bond:
            allowed = False
    return allowed

def check_atom_vs_other_atoms(atom1, other_atoms, edge_length):
    
    all_atom_pairs_okay = True
    for atom2 in other_atoms:
        allowed = check_allowed_combination(atom1, atom2, edge_length)
        if not allowed:
            all_atom_pairs_okay = False  
            break
    return all_atom_pairs_okay

def check_conformation_ok(conformation, edge_length):
    all_atom_pairs_okay = True
    for atom_idx, atom in enumerate(conformation[:-1]):

        other_atoms = conformation[atom_idx:]
        all_atom_pairs_okay = check_atom_vs_other_atoms(atom, other_atoms, edge_length)
        if not all_atom_pairs_okay:
            all_atom_pairs_okay = False
            break
    return all_atom_pairs_okay


def check_node_vs_other_nodes(node1, other_nodes, edge_length):
    
    all_node_pairs_okay = True
    for node2 in other_nodes:
        allowed = check_allowed_combination(node1, node2, edge_length)
        if not allowed:
            all_node_pairs_okay = False  
            break
    return all_node_pairs_okay

def check_configuration_ok(configuration, edge_length):
    all_node_pairs_okay = True
    for node_idx, node in enumerate(configuration[:-1]):
        other_nodes = configuration[node_idx:]
        all_node_pairs_okay = check_node_vs_other_nodes(node, other_nodes, edge_length)
        if not all_node_pairs_okay:
            all_node_pairs_okay = False
            break
    return all_node_pairs_okay

"""
Functions to check whether a previous conformation has been recorded, but in a different
orientation. Does so by generating entire set of rotational isomers (using group theory and
rotational matrices), and checking if any of these are in primary list
"""

def apply_rotation(atom, matrix):

    new_origin = np.matmul(matrix, atom.origin)
    new_bonds = []
    for bond in atom.bonds:      
        new_bond = np.matmul(matrix, bond)
        new_bonds.append(new_bond)
    new_atom = Node(new_origin, new_bonds)

    return new_atom

def apply_rotations(atom, matrices):

    if type(matrices) != list:
        matrices = [matrices]
    for m in matrices:
        atom = apply_rotation(atom, m)
    
    return atom

def apply_rotation_set(atom, rotation_set):

    if type(rotation_set) != list:
        rotation_set = [rotation_set]
    rotated = []
    for idx, matrix in enumerate(rotation_set):
        new_orientation = apply_rotations(atom, matrix)
        rotated.append(new_orientation)
    return rotated

def rotate_molecule(combination, rotation_set):
    each_atoms_rotation_set = []
    for atom in combination:
        set_of_rotated_atoms = apply_rotation_set(atom, rotation_set)
        each_atoms_rotation_set.append(set_of_rotated_atoms)
    new_combinations = list(zip(*each_atoms_rotation_set))
    if len(new_combinations) == 1:
        new_combinations = new_combinations[0]
    return new_combinations

def check_if_bonds_are_identical(atom1, atom2):
    identical = True
    # find if the bonding is the same
    if len(atom1.bonds) != len(atom2.bonds):  
        identical = False
    else:
        for bond1 in atom1.bonds:
            identical = tuple(bond1) in [tuple(b) for b in atom2.bonds]
            if not identical:
                identical = False
                break                
    return identical

def check_if_two_combinations_are_identical(combination1, combination2):
    identical = True
    # find the atoms in the same positions in each combination
    for atom1 in combination1:
        for atom2 in combination2:    
            if tuple(atom1.origin) == tuple(atom2.origin):
                #check if atoms have identical bonds
                identical = check_if_bonds_are_identical(atom1, atom2)
                if not identical:                
                    return identical
    return identical

def check_known_combinations(rotated_combinations, unique_combinations):
    # if any of the rotated combinations are in the unique set, then this combination is not unique
    unique_structure = True
    for idx, old_combination in enumerate(unique_combinations):
        for rotated_combination in rotated_combinations:
            identical = check_if_two_combinations_are_identical(rotated_combination, old_combination)
            if identical:          
                unique_structure = False
                break
        if not unique_structure:
            break
    return unique_structure



def build_node_pool(polyhedron):
    node_coordinates = geometry.polyhedron[polyhedron]
    edge_length = get_edge_length(geometry.polyhedron[polyhedron])

    nodes = []
    for _, node1 in enumerate(node_coordinates):
        bonds = []
        for _, node2 in enumerate(node_coordinates):
            this_bond = np.array(node2-node1)
            this_bond_len = get_vector_len(this_bond)       
            if this_bond_len == edge_length:
                bonds.append(this_bond)
        combinations = []
        for i in range(len(bonds)+1):
            allowed_combinations = list(itertools.combinations(bonds, i)) 
            combinations.extend(allowed_combinations)
        node_objs = []
        for bond_combination in combinations:
            node_obj = Node(node1, bond_combination)
            node_objs.append(node_obj)
        nodes.append(node_objs)
    return nodes
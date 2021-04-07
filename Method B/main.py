import argparse
import itertools
import numpy as np


import symmetry
import geometry
import visualise
import tools


DEFAULT_GEOMETRY = 'octahedron'

def generate_dummy(nodes):
    dummy = [p[0] for p in nodes]
    dummy[0] = nodes[0][1]
    return dummy

def build_polyhedron(all_nodes, assigned_nodes):
    if len(assigned_nodes) < len(all_nodes):
        next_node_position_idx = len(assigned_nodes)
        next_node_position = all_nodes[next_node_position_idx] 
        for bonding_configuration in next_node_position:  
            this_conformation = assigned_nodes.copy()
            this_conformation.append(bonding_configuration)
            all_node_pairs_okay = tools.check_configuration_ok(this_conformation, edge_length)
            if all_node_pairs_okay:              
                if len(this_conformation) < len(all_nodes):               
                    build_polyhedron(all_nodes,this_conformation)
                else:
                    rotated_combinations = tools.rotate_molecule(this_conformation, rotation_set)
                    unique_structure = tools.check_known_combinations(rotated_combinations, unique_conformations)
                    if unique_structure: 
                        unique_conformations.append(this_conformation)


def main(polyhedron):
    global unique_conformations, rotation_set, edge_length
    unique_conformations = []
    
    rotation_set = symmetry.rotations[polyhedron]
    edge_length = tools.get_edge_length(geometry.polyhedron[polyhedron])
    node_pool = tools.build_node_pool(polyhedron)

    build_polyhedron(node_pool, [])
    return unique_conformations

def write_to_csv(unique_conformations):
    pass



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--polyhedron', '-p', default=DEFAULT_GEOMETRY, help="geometry of system: tetrahedral, octahedral, cubic")
    args = parser.parse_args()

    unique_conformations = main(args.polyhedron)
    visualise.show_structure(unique_conformations[0])


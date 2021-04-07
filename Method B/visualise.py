import matplotlib.pyplot as plt
import numpy as np
import tools

"""
Display a particular structure.
     configuration: list of nodes.
        -> each node is an object with attributes:
             origin: cartesian coordinates of node origin
             bonds: list of internodal vectors originating from this node
     save: string with filepath. Won't save if directory doesn't exist
     cmap: matplotlib colour map. 
"""

def show_structure(configuration, save = '', cmap='jet', show=True, figsize = (6, 4), viewing_angle = (10, 10)):
    
    colours = [plt.cm.get_cmap(cmap)(i) for i in np.linspace(0, 1, len(configuration)+1) ][:-1]
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    all_bonds = []
    configuration = tools.sort_nodes(configuration)
    edge_length = tools.get_edge_length([c.origin for c in configuration])
    for idx, a1 in enumerate(configuration):
        o1 = a1.origin
        for a2 in configuration[idx:]:   
            if tools.get_bond_len(a1, a2) == edge_length:
                o2 = a2.origin
                xyz = list(zip(*[o1, o2]))
                ax.plot(*xyz, c = 'k', linewidth=1) 
            
            
    for idx,(a, c) in enumerate(zip(configuration, colours)):
        node_origin = a.origin
#         ax.scatter(*node_origin, c=[c], s=100, alpha=1)
            
        for b in a.bonds:
            end = node_origin + b/2           
            xyz = list(zip(*[node_origin, end]))
            frame_xyz =  list(zip(*[node_origin, node_origin+b]))
            all_bonds.append((xyz, c, frame_xyz))    
 
#         ax.text(*node_origin, node_origin, size=figsize[0]*3)
    
    
    ax.view_init(*viewing_angle)
    for bond in all_bonds:
        xyz, c, frame_xyz = bond
        ax.plot(*xyz, c = 'b', linewidth=8) 
    ax._axis3don = False

    if save:
        plt.savefig(save)
    if show:
        plt.show()
    plt.close(fig)

def show_rotations(configuration, rotations):
    show_structure(configuration)
    for r in rotations:
        res = tools.rotate_molecule(configuration, r)
        show_structure(res)
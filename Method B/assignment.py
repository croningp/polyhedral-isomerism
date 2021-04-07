import tools
import visualise

node_mappings = [0,3,1,4,2,5]
label_mappings = {'0':[0],
                    '1':[1,2,3,4],
                    '2':[5,7,9,10],
                    "2'":[6,8],
                    "3":[11,12,13,14],
                    '4':[15],
                    }

def get_configuration(configuration, node, label):
    possibilities = label_mappings[label]
    if len(possibilities) == 1:
        return node[possibilities[0]]
    else:
        for possibility in possibilities:
            pass

def from_octahedron_code(code):
    node_pool = tools.build_node_pool('octahedron')
    empty = [n[0] for n in node_pool]

    # for idx, label in enumerate(code):
    #     node = node_pool[node_mappings[idx]]
    #     node_configuration = get_configuration(configuration, node, label)
 
    configs = []
    for cfg in node_pool[0]:
        empty[0] = cfg
        visualise.show_structure(empty)
    

from_octahedron_code('442200')
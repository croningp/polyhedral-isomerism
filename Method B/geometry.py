"""
basic shapes are defined by the cartesian coordinates of their vertices.
"""

import numpy as np


def vertex(x, y, z): 
    """ Return vertex coordinates fixed to the unit sphere """  
    xyz = np.array([x,y,z])
    length = np.sqrt(xyz.dot(xyz))   
    return np.array([i/length for i in xyz])

PHI = (1 + np.sqrt(5)) / 2 


polyhedron = {
    'tetrahedron': 
            [vertex(-1,-1,-1), 
            vertex(-1,1,1), 
            vertex(1,-1,1), 
            vertex(1,1,-1), ],
    'octahedron':  
        [vertex(1,0,0), 
        vertex(0,1,0),                            
        vertex(0,0,1), 
        vertex(-1,0,0),                        
        vertex(0,-1,0), 
        vertex(0,0,-1),]  ,
    'icosahedron': 
        [vertex(-1, PHI, 0), 
         vertex( 1, PHI, 0), 
         vertex(-1, -PHI, 0), 
         vertex( 1, -PHI, 0), 
         
         vertex(0, -1, PHI), 
         vertex(0, 1, PHI), 
         vertex(0, -1, -PHI), 
         vertex(0, 1, -PHI), 
         
         vertex( PHI, 0, -1), 
         vertex( PHI, 0, 1), 
         vertex(-PHI, 0, -1), 
         vertex(-PHI, 0, 1), ]
    }
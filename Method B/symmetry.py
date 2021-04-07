""" rotational symmetry elements represented as vectors """  
import numpy as np

a = np.array([1,0,0])
b = np.array([0,1,0])
c = np.array([0,0,1])

E = np.array([a,b,c])
c4z = np.array([-b,a,c])
c4y = np.array([c,b,-a])
c4x = np.array([a,-c,b])

c4x1 = c4x
c4x2 = np.matmul(c4x1, c4x)
c4x3 = np.matmul(c4x2, c4x)

c4z1 = c4y 
c4z2 = np.matmul(c4z1, c4x)
c4z3 = np.matmul(c4z2, c4x)
c4z4 = np.matmul(c4z3, c4x)

c4y1 = c4z 
c4y2 = np.matmul(c4y1, c4x)
c4y3 = np.matmul(c4y2, c4x)
c4y4 = np.matmul(c4y3, c4x)

c4x1b = np.matmul(c4y, c4y)
c4x2b = np.matmul(c4x1b, c4x)
c4x3b = np.matmul(c4x2b, c4x)
c4x4b = np.matmul(c4x3b, c4x)

c4y1b = np.matmul(c4x4b, c4y)
c4y2b = np.matmul(c4y1b, c4x)
c4y3b = np.matmul(c4y2b, c4x)
c4y4b = np.matmul(c4y3b, c4x)

c4z1b = np.matmul(c4x4b, c4z)
c4z2b = np.matmul(c4z1b, c4x)
c4z3b = np.matmul(c4z2b, c4x)
c4z4b = np.matmul(c4z3b, c4x)

rotations = {
    'tetrahedron':[c4x2,
                    c4z2,c4z4,
                    c4y2,c4y4,
                    c4x1b,c4x3b,
                    c4z1b,c4z3b,
                    c4y1b,c4y3b],
    'octahedron': [c4x1,c4x2,c4x3,
                    c4z1,c4z2,c4z3,c4z4,
                    c4y1,c4y2,c4y3,c4y4,
                    c4x1b,c4x2b,c4x3b,c4x4b,
                    c4z1b,c4z2b,c4z3b,c4z4b,
                    c4y1b,c4y2b,c4y3b,c4y4b]}

    

# -*- coding: utf-8 -*-
from src01 import *
from integr01 import *
from numpy import *
start=time.clock()

def filter_clipped_tri(mesh):
    """
    Return a list triangles clipped by xy plane
    """
    def predicate(x):
        [x1,y1,z1],[x2,y2,z2],[x3,y3,z3] = x
        return (((z1>0) ^ (z2>0)) or ((z2>0) ^ (z3>0)) or ((z3>0) ^ (z1>0)) or
                (z1 + z2 ==0) or (z2 + z3 ==0) or (z3+z1 ==0))

    return filter(predicate, mesh)

def getBarycenter(aem):
    """
        Compute barycenter from AffineEulerMat.

        Parameters
        ----------
        aem : list of list of triple [x,y,z]
            affine Euler matrix

        Returns
        -------
        barycenter : real
            barycenter
        """
    return (array(aem[-1])/aem[-1][-1])[:-1]

def allign(mesh):
    pass

def rotate(mesh, rotation_matrix):
    res = []
    for tri in mesh:
        res.append([])
        for v in tri:
            res[-1].append(dot(rotation_matrix, v))
    return array(res)

def translate(mesh, t_coords):
    res = []
    for tri in mesh:
        res.append([])
        for v in tri:
            res[-1].append(v - array(t_coords))
    return array(res)

def getPrincipalAxes(aem):
    eigen_vec = transpose(linalg.eig(aem)[1])
    eigen_val = linalg.eigvals(aem)

    return [ eigen_vec[i] for i in eigen_val.argsort() ]


off_file_name = "cow1.off"
off_file_path = "/home/bolod/Dropbox/UNI/TESI/ShapeEuler/aim@shape_models/"
#off_file_path = "C:\\Users\\ivanagloriosi\\Documents\\My Dropbox\\UNI\\TESI\\ShapeEuler\\aim@shape_models"
mesh, vertexes, indexes = parseOFF(off_file_name, off_file_path)
c_vol = III(mesh, 0,0,0)
area = II(mesh, 0,0,0)
print 'volume:', c_vol, '- area:', area, '\n'
aem = AffineEulerMat(mesh, II)
print 'aem:', aem, '\n'

#per normalizzare decommentare la seguente (divido tutto per il volume)
aem_3x3 = array([ [val / aem[-1][-1] for val in row] for row in aem])[0:3, 0:3]

# se non normalizzo decommentare la seguente
#aem_3x3 = array(aem)[0:3, 0:3]

print 'aem_norm:', aem_3x3, '\n'
bar = getBarycenter(aem) #oppure i primi 3 elementi dell'ultima riga di aem_norm
print 'baricentre:', bar, '\n'
p_axes = getPrincipalAxes(aem_3x3)
print 'principal axes:', array(p_axes), '\n'

#m = rotate(translate(mesh, bar),p_axes)
mt = translate(mesh, bar)
#mt_aem = AffineEulerMat(mt, III)
mtr = rotate(mt, p_axes)
mtr_aem = AffineEulerMat(mtr, II)
print 'mtr_aem:', mtr_aem, '\n'

print "ended in",(time.clock() - start),"seconds"

print 'mtr', mtr 
### Visualizzazione
filtered_mesh = array(filter_clipped_tri(mtr))
#mucca_tagliata = SKELETON(1)(STRUCT([MKPOL([tri, [[1,2,3]], [1]]) for tri in filtered_mesh.tolist()]))
mucca_intera = SKELETON(1)(STRUCT([MKPOL([tri, [[1,2,3]], [1]]) for tri in mtr.tolist()]))
#taglio = COLOR(RED)(DIFF([mucca_intera, mucca_tagliata]))
pol_taglio = STRUCT([MKPOL([tri, [[1,2,3]], [1]]) for tri in filtered_mesh.tolist()])
skel_taglio = SKELETON(1)(pol_taglio)
to_view = STRUCT([mucca_intera, COLOR(RED)(pol_taglio)])
VIEW(to_view)

#VIEW(STRUCT([SKELETON(1)(T([1,2,3])(-bar)(off_in_plasm(vertexes, indexes)))] + [(COLOR(RED)(CUBOID([0.1, 0.1, 0.1])))]))

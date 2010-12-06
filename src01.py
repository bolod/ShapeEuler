import os
from pyplasm import *
import re

def parseOFF(off_file_name, off_file_path="."):
    file_path_name = os.path.join(off_file_path, off_file_name)
    
    off_file_list = filter(lambda s: not(s.startswith('#') or
                                         s.startswith('\n') or
                                         s.startswith('\r') or
                                         not(re.findall('([a-z]|[A-Z]|[0-9])+', s))), open(file_path_name, "r").readlines())
    vertex_count, face_count, edge_count = map(lambda x: int(x), re.split(' +', off_file_list[1].strip()))
    vertex_list = map(lambda x: map(lambda y: float(y), re.split(' +', x.strip())), off_file_list[2:vertex_count+2])
    face_et_al_list = map( lambda x: map( lambda y: int(float(y)), re.split('[ ]+', x.strip())), off_file_list[vertex_count+2:vertex_count+2+face_count])
    face_list = [ l[1:l[0]+1] for l in face_et_al_list]
    return [[vertex_list[i] for i in vertexes_in_face] for vertexes_in_face in face_list], vertex_list, face_list

def off_in_plasm(vertexes, indexes):
    return MKPOL([vertexes, AA(AA(lambda x: x+1))(indexes), [1]])
    
if __name__ == "__main__":
    off_file_name = "tetra.off"
    off_file_path = "/home/ivanagloriosi/Dropbox/UNI/TESI/ShapeEuler/aim@shape_models/"
    #off_file_path = "C:\\Users\\ivanagloriosi\\Documents\\My Dropbox\\UNI\\TESI\\ShapeEuler\\aim@shape_models"
    a, b, c = parseOFF(off_file_name, off_file_path)
    VIEW(off_in_plasm(b, c))

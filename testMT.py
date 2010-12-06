# -*- coding: utf-8 -*-
from src01 import *
from integr02 import *
from numpy import *


off_file_name = "camel.off"
#off_file_path = "/home/bolod/Dropbox/UNI/TESI/ShapeEuler/aim@shape_models/"
off_file_path = "aim@shape_models"
mesh, vertexes, indexes = parseOFF(off_file_name, off_file_path)
print 'starting calculating AffineEulerMat...'
start=time.clock()
aem = AffineEulerMat(mesh, II)
print "ended in",(time.clock() - start),"seconds"

print 'starting calculating AffineEulerMatMT...'
start=time.clock()
aemMT = AffineEulerMatMT(mesh, II)
print "ended in",(time.clock() - start),"seconds"

print 'test:', array(aem) - array(aemMT)


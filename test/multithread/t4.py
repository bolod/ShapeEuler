from multiprocessing import *
from pyplasm import *
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double


class Point(Structure):
    _fields_ = [('x', c_double), ('y', c_double), ('z', c_double)]
    
class Triangle(Structure):
    _fields_ = [('p1', Point), ('p2', Point), ('p3', Point)]
        
class Mesh(Structure):
    _fields_ = [('t1', Triangle), ('t2', Triangle), ('t3', Triangle)]

def f_m(coef, x):
    i = 0
    while i < 9876:
        i += 1 
    return coef*x*x
    
def f_m_l(args):
    coef, x = args
    i = 0
    while i < 9876:
        i += 1 
    return coef*x*x


def f(x):
    i = 0
    while i < 9876:
        i += 1 
    return x*x 

if __name__ == "__main__":
    #Structure test
    point1 = Point(0.11, 0.22, 0.33)
    point2 = Point(0.44, 0.55, 0.66)
    point3 = Point(0.77, 0.88, 0.99)
    tri1 = Triangle(point1, point2, point3)
    tri2 = Triangle((1,2,3),(4,5,6))
    print tri2.p1.x, tri2.p2.y, tri2.p2.z
    print tri2.p3.x, tri2.p3.y, tri2.p3.z
    t = [
        ((1.875,-6.25,7.90), (-5.75,2.0,5.1), (2.375,9.5,9.0)),
        ((66.6,-89.9,3.7), (4.56,5.677,54.46), (44.4,7.0,9.0))
        ]
    A = Array(Triangle, t)
    
    
    #End Structure test
    p = Pool()
    print p.map(f, range(1000))
    print C(f_m_l)(2)(5)
    print curry(f_m, 2)(5)



from numpy import *
from pyplasm import *
from ParserOff import *
from Mesh import *

if __name__ == "__main__":
	
	file_name_list = { 
		1 : "camel.off", 
		2 : "chair.off",
		3 : "cow.off",
		4 : "cube.off",
		5 : "cube_tri.off",
		6 : "cube_unit.off",
		7 : "hand_h.off",
		8 : "hand_l.off",
		9 : "icosa.off",
		10: "paral.off",
		11: "paral_2.off",
		12: "tetra.off"
	}
	
	file_name = file_name_list[11]
	parser = ParserOff()
	mesh = parser.parse(file_name)
#	a, b = mesh.split_z()

#	print "\n--A--\n", a
#	print "\n--B--\n", b	

#	struct_a = COLOR(RED)(a.to_plasm())
#	struct_b = COLOR(GREEN)(b.to_plasm())

#	struct = STRUCT([ struct_a, struct_b ])
#	rot = [[1,0,0],[0,sqrt(3)/2, -1./2],[0, 1./2, sqrt(3)/2]]
	
#	mesh.align();
	struct = SKELETON(1)(mesh.to_plasm())
	VIEW((struct))
	
	mesh.align()
	struct = SKELETON(1)(mesh.to_plasm())
	VIEW((struct))
	
	mesh.align()
	struct = SKELETON(1)(mesh.to_plasm())
	VIEW((struct))
	
	mesh.align()
	struct = SKELETON(1)(mesh.to_plasm())
	VIEW((struct))


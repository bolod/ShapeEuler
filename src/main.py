from numpy import *
from pyplasm import *
from ParserOff import *
from Mesh import *

if __name__ == "__main__":
	
	file_name_list = { 
		1: "camel.off", 
		2: "cow1.off",
		3: "cube.off",
		4: "cube4norm.off",
		5: "hand-olivier-isotropic.off",
		6: "hand-olivier-uniform-50kv.off",
		7: "icosa.off",
		8: "tetra.off",
		9: "chair.off"}
	
	file_name = file_name_list[3]
	parser = ParserOff()
	mesh = parser.parse(file_name)
	print mesh
	a, b = mesh.split_z()

	print "\n--A--\n", a
	print "\n--B--\n", b	

	struct_a = COLOR(RED)(a.to_plasm())
	struct_b = COLOR(GREEN)(b.to_plasm())

	struct = STRUCT([ struct_a, struct_b ])
#	struct = mesh.to_plasm()
	VIEW((struct))


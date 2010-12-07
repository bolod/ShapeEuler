from numpy import *
from pyplasm import *
from ParserOff import *
from Mesh import *

if __name__ == "__main__":
	
	file_name_list = [ 
		"camel.off",
		"cow1.off",
		"cube.off",
		"cube4norm.off",
		"hand-olivier-isotropic.off",
		"hand-olivier-uniform-50kv.off",
		"icosa.off",
		"tetra.off"]
	
	file_name = file_name_list[5]

	parser = ParserOff()
	#NOTE: before align, update the euler matrix
	mesh = parser.parse(file_name).update_euler().align()
	struct = mesh.to_plasm()
	VIEW(SKELETON(1)(struct))
	

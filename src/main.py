from numpy import *
from pyplasm import *
from ParserOff import *
from Mesh import *

if __name__ == "__main__":
	
	FILE_NAME = "cow1.off"

	parser = ParserOff()
	#NOTE: before align, update the euler matrix
	mesh = parser.parse(FILE_NAME).update_euler().align()
	struct = mesh.to_plasm()
	VIEW(SKELETON(1)(struct))
	

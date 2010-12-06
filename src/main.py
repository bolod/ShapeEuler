from numpy import *
from pyplasm import *
from ParserOff import *
from Mesh import *

if __name__ == "__main__":
	
	FILE_NAME = "cow1.off"

	parser = ParserOff()
	mesh = parser.parse(FILE_NAME)
	struct = mesh.to_plasm()
	VIEW(SKELETON(1)(struct))
	

from numpy import *
from pyplams import *

if __name__ == "__main__":
	
	FILE_NAME = "cow1.off"

	parser = ParserOff()
	mesh = parser(FILE_NAME)
	struct = mesh.to_plasm()
	VIEW(SKELETON(1)(struct))
	
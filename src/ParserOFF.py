import os
import re
from Mesh import *

class ParserOff():
	
	def __init__(self):
		
		self.descr = "Parser for .off file"
	
	def __repr__(self):
		"""
		Gets the info of this parser.
		
		Returns
		-------
		info : String
			info of this parser
		"""
		
		info = "{\n"
		info += "descr: " + self.descr + "}\n"
		info += "}"
		
		return info
	
	def parse(self, file_name, file_path="../resources"):
		"""
		Parses the file .off with the given name in the given path.
		
		Parameters
		----------
		file_name : String
			the name of the file to parse
		file_path : String
			the path of the file to parse
			
		Returns
		-------
		mesh : Mesh
			the mesh of which have been parsed the coordinates of the vertices
		"""
		
		file_path_name = os.path.join(file_path, file_name)
		file_lines = open(file_path_name, "r").readlines()

		filtered_lines = \
			filter(lambda s: not(s.startswith('#')),
				(filter(lambda s: not(s.startswith('\n')),
					(filter(lambda s: not(s.startswith('\r')), 
						(filter(lambda s: re.findall('([a-z]|[A-Z]|[0-9])+', s), file_lines)))
					))
				))
		
		vertex_count, face_count, edge_count = map(lambda x: int(x), re.split(' +', filtered_lines[1].strip()))
		vertex_list = map(lambda x: map(lambda y: float(y), re.split(' +', x.strip())), filtered_lines[2:vertex_count+2])
		face_et_al_list = map( lambda x: map( lambda y: int(float(y)), re.split('[ ]+', x.strip())), filtered_lines[vertex_count+2:vertex_count+2+face_count])
		face_list = [ l[1:l[0]+1] for l in face_et_al_list]
		
		mesh = Mesh(vertex_list, face_list)
		
		return mesh
		
if __name__ == "__main__":
	
	file_name = "tetra.off"
	parser = ParserOff()
	mesh = parser.parse(file_name)
	print mesh

from numpy import *

class Mesh():

	def __init__(self, triangles=array([])):
		
		self.triangles = triangles
	
	def __repr__(self):
		"""
		Gets the info of this mesh.
		
		Returns
		-------
		info : String
			info of this triangle
		"""
		
		info = "{\n"
		info += "triangles: \n" + self.triangles + "\n"
		info += "}"
		
		return info
	
	def clone(self):
		"""
		Clones this mesh.
		
		Returns
		-------
		clone :  Mesh
			the clone of this mesh
		"""
		
		clone = Mesh()
		
		for triangle in self.triangles:
			clone.triangles.append(triangle.clone())
		
		return clone
	
	def get_triangles(self):
		"""
		Gets the triangles of this mesh.
		
		Returns
		-------
		triangles : Triangle array
			triangles of this atom
		"""
		
		return self.triangles
	
	def rotate(self, rotation):
		"""
		Rotates this mesh by the given rotation matrix.
		
		Parameters
		----------
		rotation: ndarray, shape(3, 3)
			the rotation matrix
		
		Returns
		-------
		self : Mesh
			this mesh rotated,
			for chaining purpose
		"""
		
		for triangle in self.triangles:
			triangle.rotate(rotation)
		
		return self

	def scale(self, scale):
		"""
		Scales this mesh by the given scale value vector.
		
		Parameters
		----------
		scale: ndarray, shape(3, )
			the scale value vector
		
		Returns
		-------
		self : Mesh
			this mesh scaled,
			for chaining purpose
		"""
		
		for triangle in self.triangles:
			triangle.scale(scale)
		
		return self
	
	def translate(self, translation):
		"""
		Translates this mesh by the given translation vector.
		
		Parameters
		----------
		translation: ndarray, shape(3, )
			the translation vector
		
		Returns
		-------
		self : Mesh
			this mesh translated,
			for chaining purpose
		"""
		
		for triangle in self.triangles:
			triangle.translate(translation)
		
		return self
	

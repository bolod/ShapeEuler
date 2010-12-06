from numpy import *

class Triangle():

	def __init__(self, p1, p2, p3):
		
		self.points = array([p1,p2,p3])
	
	def __repr__(self):
		"""
		Gets the info of this triangle.
		
		Returns
		-------
		info : String
			info of this triangle
		"""
		
		info = "{\n"
		info += "points: " + self.points + "\n"
		info += "}"
		
		return info
	
	def clone(self):
		"""
		Clones this triangle.
		
		Returns
		-------
		clone :  Point
			the clone of this point
		"""
		
		return Triangle(self.points[0].clone(), self.points[1].clone(), self.points[2].clone())
	
	def get_points(self):
		"""
		Gets the points of this triangle.
		
		Returns
		-------
		points : Point array
			points of this atom
		"""
		
		return self.points
	
	def rotate(self, rotation):
		"""
		Rotates this triangle by the given rotation matrix.
		
		Parameters
		----------
		rotation: ndarray, shape(3, 3)
			the rotation matrix
		
		Returns
		-------
		self : Triangle
			this triangle rotated,
			for chaining purpose
		"""
		
		for point in self.points:
			point.rotate(rotation)
		
		return self

	def scale(self, scale):
		"""
		Scales this triangle by the given scale value vector.
		
		Parameters
		----------
		scale: ndarray, shape(3, )
			the scale value vector
		
		Returns
		-------
		self : Triangle
			this triangle scaled,
			for chaining purpose
		"""
		
		for point in self.points:
			point.scale(scale)
		
		return self
	
	def translate(self, translation):
		"""
		Translates this triangle by the given translation vector.
		
		Parameters
		----------
		translation: ndarray, shape(3, )
			the translation vector
		
		Returns
		-------
		self : Triangle
			this point translated,
			for chaining purpose
		"""
		
		for point in self.points:
			point.translate(translation)
		
		return self
	
	def to_plasm(self):
		"""
		Gets the PLaSM HPC of this triangle.
		
		Returns
		-------
		struct : PLaSM HPC
			the PLaSM HPC of this triangle
		"""
		
		points = [ point.get_coords().tolist() for point in self.points]
		pol = MKPOL([points, [[1,2,3]], [1]])
		struct = STRUCT(pol)
		
		return struct
from numpy import *
from Point import *
from pyplasm import *

class Triangle():

	def __init__(self, points=[Point(), Point(), Point()]):
		
		self.points = points
	
	def __repr__(self):
		"""
		Gets the info of this triangle.
		
		Returns
		-------
		info : String
			info of this triangle
		"""
		
		info = "\ntriangle:\n"
		for point in self.points:
			info += str(point) + "\n"
		
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
	
	def get_point(self, i):
		"""
		Gets the i-th point of this triangle.
		
		Patameters
		----------
		i : int 
			the index of point to get
		
		Returns
		-------
		points : Point array
			the i-th point of this triangle
		"""
		
		return self.points[i]
	
	def set_point(self, i, point):
		"""
		Sets the i-th point of this triangle by the given point.
		
		Parameters
		----------
		i : int
			the index of point to set
			
		point : Point array
			the point to copy
		
		Returns
		-------
		self : Triangle
			this triangle,
			for chaining purpose
		"""
		
		self.points[i][0] = point[0]
		self.points[i][1] = point[1]
		self.points[i][2] = point[2]
		
		return self
	
	def get_p1(self):
		"""
		Gets the first point of this triangle.
		
		Returns
		-------
		point : Point
			the first point of this triangle
		"""
	
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
		struct = STRUCT([pol])
		
		return struct
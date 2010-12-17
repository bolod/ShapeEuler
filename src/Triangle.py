from numpy import *
from pyplasm import *

class Triangle():

	def __init__(self, points=[[0.,0.,0.], [0.,0.,0.], [0.,0.,0.]]):
		
		self.current = 0
		self.points = [ array(point) for point in points ]
	
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
	
	def __getitem__(self, i):
		
		return self.points[i]
	
	def __setitem__(self, i, point):
		
		self.points[i] = array(point)

	def __iter__(self):
		
		return self

	def next(self):
		
		if self.current >= len(self.points):
			raise StopIteration
		else:
			self.current += 1
			return self.points[self.current - 1]
	
	def index(self, point):
		
		for i in range(len(self.points)):
			if point[0] == self.points[i][0] and point[1] == self.points[i][1] and point[2] == self.points[i][2]: 
				return i
		
		return -1
	
	def contains(self, point):
		
		return self.index(point) > 0
	
	def clone(self):
		"""
		Clones this triangle.
		
		Returns
		-------
		clone :  Point
			the clone of this point
		"""
		
		return Triangle([ point[:] for point in self.points ])
		
	def get_points(self):
		"""
		Gets the point list of this triangle.
		
		Returns
		-------
		points : array (3,3)
		the point list of this triangle
		"""
		
		return self.points
        
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
		
		self.points[i] = point[:]
		
		return self
	
	
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

		self.points = [ dot(rotation, point) for point in self.points ]
		
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
		
		self.points = [ point * scale for point in self.points ]
		
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
		
		self.points = [ point - translation for point in self.points ]
		
		return self
	
	def to_plasm(self):
		"""
		Gets the PLaSM HPC of this triangle.
		
		Returns
		-------
		struct : PLaSM HPC
			the PLaSM HPC of this triangle
		"""
		points = [ point.tolist() for point in self.points ]
		pol = MKPOL([ points, [[1,2,3]], [1] ])
		struct = STRUCT([pol])
		
		return struct

	def is_over(self, plane=2):
		"""
		Tests if this triangle has all points over the plane xy.
		
		Returns
		-------
		test : boolean
		true if this triangle has all points over the plane xy 
		false otherwise
		"""
		
		return self.points[0][plane] >= 0 and self.points[1][plane] >= 0 and self.points[2][plane] >= 0

	def is_under(self, plane=2):
		"""
		Tests if this triangle has all points under the plane xy.

		Returns
		-------
		test : boolean
		true if this triangle has all points under the plane xy 
		false otherwise
		"""
		
		return self.points[0][plane] <= 0 and self.points[1][plane] <= 0 and self.points[2][plane] <= 0
		
	def is_on(self, plane=2):
		"""
		Tests if this triangle lie on xy plane.
		
		Returns
		-------
		test : boolean
		true if this triangle lie on xy plane
		false otherwise
		"""
		
		return self.points[0][plane] == 0 and self.points[1][plane] == 0 and self.points[2][plane] == 0


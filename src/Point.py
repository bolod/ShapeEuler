from numpy import *

class Point():

	def __init__(self, coords=array([0.,0.,0.])):
		
		self.coords = array(coords)
	
	def __repr__(self):
		"""
		Gets the info of this point.
		
		Returns
		-------
		info : String
			info of this point
		"""
		
		info = str(self.coords.tolist())
		
		return info
	
	def clone(self):
		"""
		Clones this point.
		
		Returns
		-------
		clone :  Point
			the clone of this point
		"""
		
		return Point(self.coords[0], self.coords[1], self.coords[2])
	
	def get_coords(self):
		"""
		Gets the coordinates of this point.
		
		Returns
		-------
		coords : ndarray, shape (3, )
			coords of this point
		"""
		
		return self.coords
	
	def get_x(self):
		"""
		Gets the x coordinate of this point.
		
		Returns
		-------
		x : float
			x coord of this point
		"""
		
		return self.coords[0]
	
	def get_y(self):
		"""
		Gets the y coordinate of this point.
		
		Returns
		-------
		y : float
			y coord of this point
		"""
		
		return self.coords[1]
	
	def get_z(self):
		"""
		Gets the z coordinate of this point.
		
		Returns
		-------
		z : float
			z coord of this point
		"""
		
		return self.coords[2]
	
	def get_distance(self, point):
		"""
		Gets the distance between this point and the given point.
				
		Parameters
		----------
		point : Point
			the point to calculate the distance to this point
		
		Returns
		-------
		distance : float
			the distance between this point and the given point
		"""
		
		return sqrt(sum(pow(self.coords - point.coords),2)) 
	
	def rotate(self, rotation):
		"""
		Rotates this point by the given rotation matrix.
		
		Parameters
		----------
		rotation: ndarray, shape(3, 3)
			the rotation matrix
		
		Returns
		-------
		self : Point
			this point rotated,
			for chaining purpose
		"""

		self.coords = dot(rotation, self.coords)
		
		return self
	
	def scale(self, scale):
		"""
		Scales this point by the given scale value vector.
		
		Parameters
		----------
		scale: ndarray, shape(3, )
			the scale value vector
		
		Returns
		-------
		self : Point
			this point scaled,
			for chaining purpose
		"""
		
		self.coords = self.coords * scale
		
		return self
	
	def translate(self, translation):
		"""
		Translates this point by the given translation vector.
		
		Parameters
		----------
		translation: ndarray, shape(3, )
			the translation vector
		
		Returns
		-------
		self : Point
			this point translated,
			for chaining purpose
		"""
		
		self.coords = self.coords - translation
		
		return self
	
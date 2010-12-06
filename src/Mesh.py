from numpy import *
from pyplasm import *
from ShapeEuler import *
from Triangle import *

class Mesh():

	def __init__(self, triangles=[]):
		
		self.triangles = triangles
		self.euler = array([])
		self.barycenter = array([])
	
	def __repr__(self):
		"""
		Gets the info of this mesh.
		
		Returns
		-------
		info : String
			info of this triangle
		"""
		
		info = "\nmesh:\n"
		for triangle in self.triangles:
			info += str(self.triangles) + "\n"
		
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
	
	def to_list(self):
		"""
		Gets the triangles of this mesh.
		
		Returns
		-------
		triangles : Triangle array
			triangles of this atom
		"""
		
		return self.triangles
		
	def add(self, triangle):
		"""
		Adds the given triangle to this mesh.
		
		Parameters
		----------
		triangle : Triangle
			the triangle to add
		
		Returns
		-------
		self : Mesh
			this mesh, 
			for chaining purpose
		"""
		
		self.triangles.append(triangle)
		
		return self
	
	def add_all(self, triangle_list):
		"""
		Adds the given triangles to this mesh.
		
		Parameters
		----------
		triangle_list : Triangle list
			the triangle list to add
		
		Returns
		-------
		self : Mesh
			this mesh, 
			for chaining purpose
		"""
		
		for triangle in triangle_list:
			self.add(triangle)
		
		return self
	
	def size(self):
		"""
		Gets the number of triangles of this mesh.
		
		Returns
		-------
		size : int
			the number of triangles of this mesh
		"""
		
		return len(self.triangles)
	
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
	
	def update_euler(self):
		"""
		Updates the affine euler matrix of this mesh.
		
		Returns
		-------
		self : Mesh
			this mesh,
			for chaining purpose
		"""
		
		tri_list = [ [ p.coords.tolist() for p in tri.points] for tri in self.triangles]
		
		self.euler = AffineEulerMat(tri_list, II)
		
		return self
		
	
	def get_euler(self):
		"""
		Gets the affine euler matrix of this mesh.
		
		Returns
		-------
		euler : float matrix 4 x 4
			the affine euler matrix of this mesh
		"""
		
		return self.euler
	
	def update_barycenter(self):
		"""
		Updates the barycenter of this mesh.
		
		Returns
		-------
		self : Mesh
			this mesh,
			for chaining purpose
		"""
		
		euler = self.update_euler().get_euler()
		
		self.barycenter = (array(euler[-1]) / euler[-1][-1])[:-1]
		
		return self	
	
	def get_barycenter(self):
		"""
		Gets the barycenter of this mesh.
		
		Returns
		-------
		self : float array
			the barycenter of this mesh
		"""
				
		return self.barycenter
	
	def get_principal_axis(self):
		"""
		Gets the principal axes of this mesh.
		
		Returns
		-------
		axes : matrix
			the principal axes of this mesh
		"""
		
		euler = self.euler
		eigen_vec = transpose(linalg.eig(euler)[1])
		eigen_val = linalg.eigvals(euler)
		
		return [eigen_vec[i] for i in eigen_val.argsort()]
	
	def align(self):
		"""
		Align this mesh by its principal axis.
		
		Do the following steps:
		1. translate the mesh bringing the barycenter in the origin
		2. rotate the mesh by its principal axes
		
		Returns
		-------
		self : Mesh
			this mesh aligned,
			for chaining purpose
		"""
		
		return self.translate(self.get_barycenter()).rotate(self.get_principal_axes())
	
	def filter_clipped_tri(self):
		"""
		Gets the portion of this mesh clipped by the xy plane.
		
		Returns
		-------
		filtered_mesh: Mesh
			the portion of this mesh clipped by the xy plane
		"""
		
		filtered_mesh = Mesh()
		
		#TODO: waiting for bolod
		#def predicate(x):
		#	[x1,y1,z1],[x2,y2,z2],[x3,y3,z3] = x
		#	return (((z1>0) ^ (z2>0)) or ((z2>0) ^ (z3>0)) or ((z3>0) ^ (z1>0)) or
		#			(z1 + z2 ==0) or (z2 + z3 ==0) or (z3+z1 ==0))
		#
		#return filter(predicate, mesh)
		
		return filtered_mesh
	
	def to_plasm(self):
		"""
		Gets the PLaSM HPC of this mesh.
		
		Returns
		-------
		struct : PLaSM HPC
			the PLaSM HPC of this mesh
		"""
		
		triangles = [ triangle.to_plasm() for triangle in self.triangles ]
		struct = STRUCT(triangles)
		
		return struct
	
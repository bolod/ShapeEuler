from numpy import *
import ShapeEuler

class Mesh():

	def __init__(self, triangles=array([])):
		
		self.triangles = triangles
		self.euler = arrat([])
		self.barycenter = array([])
	
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
	
	def update_euler(self):
		"""
		Updates the affine euler matrix of this mesh.
		
		Returns
		-------
		self : Mesh
			this mesh,
			for chaining purpose
		"""
		
		tri_list = [ [ point.coords.tolist() for point in triangle.points] for triangle in self.triangles]
		
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
	
	def get_principal_axes(aem):
		"""
		Gets the principal axes of this mesh.
		
		Returns
		-------
		axes : matrix
			the principal axes of this mesh
		"""
		
		eigen_vec = transpose(linalg.eig(aem)[1])
		eigen_val = linalg.eigvals(aem)
		
		return [eigen_vec[i] for i in eigen_val.argsort()]
	
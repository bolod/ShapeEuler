from numpy import *
from pyplasm import *
from ShapeEuler import *
from Triangle import *

class Mesh():

	def __init__(self, triangle_list):
		
		self.current = 0
		self.triangles = triangle_list
		self.euler = array([[1.,0.,0.,0.],[0.,1.,0.,0.],[0.,0.,1.,0.], [0.,0.,0.,1.]])
		self.barycenter = array([0.,0.,0.])
	
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
			info += str(triangle) + "\n"
		
		return info
		
	def __getitem__(self, i):
		
		return self.triangles[i]
	
	def __setitem__(self, i, value):
		
		self.triangles[i] = value
	
	def __iter__(self):
		
		return self
		
	def next(self):
		
		if self.current >= len(self.triangles):
			raise StopIteration
		else:
			self.current += 1
			return self.triangles[self.current - 1]
	
	def index(self, value):
		
		return self.triangles.index(value)
		
	def clone(self):
		"""
		Clones this mesh.
		
		Returns
		-------
		clone :  Mesh
			the clone of this mesh
		"""
		
		clone = Mesh([])
		
		for triangle in self.triangles:
			clone.add(triangle.clone())
		
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
	
	def update_euler(self, fun=II):
		"""
		Updates the affine euler matrix of this mesh.
		
		Parameters
		----------
		fun : function
			the integral function
		
		Returns
		-------
		self : Mesh
			this mesh,
			for chaining purpose
		"""
		
		tri_list = [ triangle.get_points() for triangle in self.triangles]
		self.euler = array(AffineEulerMat(tri_list, fun))
		
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
		
		self.barycenter = (array(self.euler[-1]) / self.euler[-1][-1])[:-1]
		
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
	
	def update(self, fun=II):
		"""
		Updates this mesh.
		
		Returns
		-------
			self : Mesh
				this mesh,
				for chaning purpose
		"""
		
		self.update_barycenter()
		self.update_euler(fun)
		
		return self
	
	def get_principal_axes(self):
		"""
		Gets the principal axes of this mesh.
		
		Returns
		-------
		axes : matrix
			the principal axes of this mesh
		"""
		
		euler_3x3 = [ row[:3] for row in self.euler[:3]]
		
		eigen_vec = transpose(linalg.eig(euler_3x3)[1])
		eigen_val = linalg.eigvals(euler_3x3)
		axes = [eigen_vec[i] for i in eigen_val.argsort()]
		
		print "\naxes\n", axes
		
		return axes
	
	def align(self, fun=II):
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
		
		self.update(fun)
		
		return self.translate(self.get_barycenter()).rotate(self.get_principal_axes())
		
	def to_plasm(self):
		"""
		Gets the PLaSM HPC of this mesh.
		
		Returns
		-------
		struct : PLaSM HPC
			the PLaSM HPC of this mesh
		"""
		print "to plasm"
		triangles = [ triangle.to_plasm() for triangle in self.triangles ]
		print array(triangles)
		struct = STRUCT(triangles)
		
		return struct

	def split_z(self):
		
		cloned = self.clone()
		
		clipped_mesh = Mesh([])
		z_positive_mesh = Mesh([])
		z_negative_mesh = Mesh([])
		
		for tri in cloned:
			if tri.is_over(2):
				#print "is over!", tri
				z_positive_mesh.add(tri)
			elif tri.is_under(2) or tri.is_on(2):
				#print "is under!\n"
				z_negative_mesh.add(tri)
			else:
				#print "is clipped!\n"
				clipped_mesh.add(tri)
		
		print "clipped mesh:\n", z_positive_mesh
		#single=[]
		#none=[]
		for clipped_tri in clipped_mesh:
			print "clipped_tri", clipped_tri.points
			(x1,y1,z1),(x2,y2,z2),(x3,y3,z3) = clipped_tri.points
			if (int(z1==0))+(int(z2==0))+(int(z3==0)) == 1: #one vertex on xy-plane
				assert((int(z1==0))+(int(z2==0))+(int(z3==0)) == 1)
				#single.append(clipped_tri)
				#just enough
				pos_ver =  filter(lambda (x,y,z): z>0, clipped_tri)[0]
				neg_ver =  filter(lambda (x,y,z): z<0, clipped_tri)[0]
				a_pos_ver = array(pos_ver)
				a_neg_ver = array(neg_ver)
				
				line = pos_ver - neg_ver
				t = -1 * line[2]
				
				new_ver = neg_ver + t*line
				
				line = pos_ver - neg_ver
				t = -1*neg_ver[2] / line[2]
				point_A = [ neg_ver[0] + line[0]*t, 
							neg_ver[1] + line[1]*t, 
							neg_ver[2] + line[2]*t]
				
				#pay attention to normals direction
				pos_list = pos_ver.tolist()
				neg_list = neg_ver.tolist()
				pos_new_tri = clipped_tri.clone()
				#print 'pos_new_tri', type(pos_new_tri)
				#print 'neg_list:', neg_list
				#print 'INDICE:', pos_new_tri.index(neg_list)
				pos_new_tri[pos_new_tri.index(neg_list)] = pos_list
				
				neg_new_tri = clipped_tri.clone()
				pos_new_tri[pos_new_tri.index(pos_list)] = neg_list

				z_positive_mesh.add(pos_new_tri)
				z_negative_mesh.add(neg_new_tri)

			else: #no vertexes on xy-plane
				assert((int(z1==0))+(int(z2==0))+(int(z3==0)) == 0)
				#none.append(clipped_tri)
				n_zeta_positive = (int(z1>0))+(int(z2>0))+(int(z3>0))
				n_zeta_negative = (int(z1<0))+(int(z2<0))+(int(z3<0))
				assert( (n_zeta_positive == 1 and n_zeta_negative == 2) or (n_zeta_positive == 2 and n_zeta_negative == 1) )

				#SUPER JUST ENOUGH
				pos_vers = filter(lambda (x,y,z): z>0, clipped_tri.points)
				neg_vers = filter(lambda (x,y,z): z<0, clipped_tri.points)

				if len(pos_vers) == 2:
					uno = array(neg_vers[0])
					due = array(pos_vers)
				else:
					uno = array(pos_vers[0])
					due = array(neg_vers)

				assert(len(due) == 2)
				assert(len(uno) == 3)

				#punto A = (due[0] - uno)
				line_A = due[0] - uno
				t_A = -1*uno[2] / line_A[2]
				point_A = [ uno[0] + line_A[0]*t_A, 
							uno[1] + line_A[1]*t_A, 
							uno[2] + line_A[2]*t_A]

				#punto B = (due[1] - uno)
				line_B = due[1] - uno
				t_B = -1*uno[2] / line_B[2]
				point_B = [ uno[0] + line_B[0]*t_B, 
							uno[1] + line_B[1]*t_B, 
							uno[2] + line_B[2]*t_B]

				#pay attention to normals direction
				uno_new_tri = clipped_tri.clone()
				uno_new_tri[uno_new_tri.index(due[0].tolist())] = point_A
				uno_new_tri[uno_new_tri.index(due[1].tolist())] = point_B

				due_new_tri = [clipped_tri.clone(), clipped_tri.clone()]
				due_new_tri[0][due_new_tri[0].index(uno.tolist())] = point_A
				due_new_tri[0][due_new_tri[0].index(due[1].tolist())] = point_B
				due_new_tri[1][due_new_tri[1].index(uno.tolist())] = point_B

				if (int(z1>0)+int(z2>0)+int(z3>0)) < 2:
					to_add_uno = z_positive_mesh
					to_add_due = z_negative_mesh
				else:
					to_add_due = z_positive_mesh
					to_add_uno = z_negative_mesh

				to_add_uno.add(uno_new_tri)
				to_add_due.add(due_new_tri[0])
				to_add_due.add(due_new_tri[1])

		#print 'len(single):', len(single), ' - len(none):', len(none)
		return z_positive_mesh, z_negative_mesh
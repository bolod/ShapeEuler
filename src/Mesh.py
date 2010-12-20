from numpy import *
from pyplasm import *
from ShapeEuler import *

class Mesh():

	def __init__(self, point_list, tri_index_list):
		
		self.current = 0
		self.point_list = point_list
		self.tri_index_list = tri_index_list
		self.updated = True
		self.euler = identity(4)
		self.axes = identity(4)
		self.barycenter = zeros(3)
	
	def __repr__(self):
		"""
		Gets the info of this mesh.
		
		Returns
		-------
		info : String
			info of this triangle
		"""
		
		info = "\nmesh:"
		info += "\nn triangles: " + str(len(self.tri_index_list))
		info += "\ntriangles: \n" + str(array(self.to_list()))
		info += "\npoints: \n" + str(array(self.point_list))
		info += "\nindex_list \n" + str(array(self.tri_index_list))
		info += "\nn points: " + str(len(self.point_list))
		info += "\neuler: \n" + str(array(self.euler))
		info += "\nbarycenter: \n" + str(array(self.barycenter))
		info += "\naxes: \n" + str(array(self.axes))
		info += "\nupdated: " + str(self.updated)
		
		return info
		
	def __getitem__(self, i):
		
		return [ self.point_list[index] for index in self.tri_index_list[i] ]
	
	def __iter__(self):
		
		return self
		
	def next(self):
		
		if self.current >= len(self.tri_index_list):
			raise StopIteration
		else:
			self.current += 1
			return self[self.current - 1]
	
	def to_list(self):
		"""
		Gets the triangles of this mesh.

		Returns
		-------
		triangles : Triangle array
			triangles of this atom
		"""

		return [ [ self.point_list[index] for index in tri_index ] for tri_index in self.tri_index_list ]
	
	
	def clone(self):
		"""
		Clones this mesh.
		
		Returns
		-------
		clone :  Mesh
			the clone of this mesh
		"""
		
		clone = Mesh(self.point_list[:], self.tri_index_list[:])
		
		return clone
	
	def index_point(self, point, tollerance=10**-7):
		"""
		Gets the index of the given point with the given tollerance.

		Parameters
		----------
		point : list
			point

		tollerance : float
			tollerance

		Returns
		-------
		index : int
			the index of the given point with the given tollerance
		"""
		
		for index in range(len(self.point_list)):
			p = array(self.point_list[index])
			if (sign(p) == sign(array(point))).all() and (abs(p - array(point)) < tollerance).all():
				return index 
		return -1
	
	def contains_point(self, point, tollerance=10**-7):
		"""
		Tests if this mesh contains the given point with the given tollerance.

		Parameters
		----------
		point : list
			point

		tollerance : float
			tollerance

		Returns
		-------
		test : boolean
			true if this mesh contains the given point with the given tollerance, 
			false otherwise
		"""

		return self.index_point(point, tollerance) >= 0
	
	def add_point(self, point):
		
		index = self.index_point(point)
		
		if (index < 0):
			self.point_list.append(point)
			index = len(self.point_list) - 1
			
		return index
	
	def add_tri(self, triangle):
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
		
		self.tri_index_list.append([ self.add_point(point) for point in triangle ])
		
		self.updated = False
		
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
		
		self.updated = False
		
		return self
	
	def size(self):
		"""
		Gets the number of triangles of this mesh.
		
		Returns
		-------
		size : int
			the number of triangles of this mesh
		"""
		
		return len(self.tri_index_list)
	
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
		
		self.point_list = [ (dot(rotation, array(point))).tolist() for point in self.point_list ]
		
		self.updated = False
		
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
		
		self.point_list = [ (array(point) * scale).tolist() for point in self.point_list ]
		
		self.updated = False
		
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
		
		self.point_list = [ (array(point) - translation).tolist() for point in self.point_list ]
		
		self.updated = False
		
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
		
		self.euler = array(AffineEulerMat(self.to_list(), fun))
		self.barycenter = (array(self.euler[-1]) / self.euler[-1][-1])[:-1]
		
		self.updated = True
		
		return self
	
	def get_principal_axes(self, fun=II):
		"""
		Gets the principal axes of this mesh.
		
		Returns
		-------
		axes : matrix
			the principal axes of this mesh
		"""
		
		if not self.updated:
			self.update(fun)
		
		euler_3x3 = self.euler[:3,:3]
		
		eigen_vec = transpose(linalg.eig(euler_3x3)[1])
		eigen_val = linalg.eigvals(euler_3x3)
		axes = [eigen_vec[i] for i in eigen_val.argsort()]
		
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
		
		if not self.updated:
			self.update(fun)
		
		self.translate(self.get_barycenter()).rotate(self.get_principal_axes())
		
		self.updated = False
		
		return self
		
	def to_plasm(self):
		"""
		Gets the PLaSM HPC of this mesh.
		
		Returns
		-------
		struct : PLaSM HPC
			the PLaSM HPC of this mesh
		"""
		
		struct = STRUCT([ MKPOL([triangle, [[1,2,3]], [1]]) for triangle in self.to_list() ])
		
		return struct

	def split_z(self):
	
		tri_list = self.to_list()
	
		z_positive_mesh = Mesh([],[])
		z_negative_mesh = Mesh([],[])
		
		z_pos_mesh_point_list = []
		z_pos_mesh_tri_list = [] 
		
		z_neg_mesh_point_list = []
		z_neg_mesh_tri_list = []
		
		z_cli_mesh_point_list = []
		z_cli_mesh_tri_list = []
		
		for tri in tri_list:
			[point0,point1,point2] = tri
			# index0 = tri_index[0]
			# index1 = tri_index[1]
			# index2 = tri_index[2]
			# 
			# point0 = self.point_list[0]
			# point1 = self.point_list[1]
			# point2 = self.point_list[2]
			
			[x1,y1,z1] = point0
			[x2,y2,z2] = point1
			[x3,y3,z3] = point2
			
			if z1 >= 0 and z2 >= 0 and z3 >= 0:
				new_tri = [-1,-1,-1]
				
				if not point0 in z_pos_mesh_point_list:
					z_pos_mesh_point_list.append(point0)
				new_tri[0] = z_pos_mesh_point_list.index(point0)
				
				if not point1 in z_pos_mesh_point_list:
					z_pos_mesh_point_list.append(point1)
				new_tri[1] = z_pos_mesh_point_list.index(point1)
				
				if not point2 in z_pos_mesh_point_list:
					z_pos_mesh_point_list.append(point2)
				new_tri[2] = z_pos_mesh_point_list.index(point2)
				
				z_pos_mesh_tri_list.append(new_tri)
				
			elif (z1 < 0 and z2 < 0 and z3 < 0) or (z1 == 0 and z2 == 0 and z3 == 0):
				new_tri = [-1,-1,-1]
				
				if not point0 in z_neg_mesh_point_list:
					z_neg_mesh_point_list.append(point0)
				new_tri[0] = z_neg_mesh_point_list.index(point0)
				
				if not point1 in z_neg_mesh_point_list:
					z_neg_mesh_point_list.append(point1)
				new_tri[1] = z_neg_mesh_point_list.index(point1)
				
				if not point2 in z_neg_mesh_point_list:
					z_neg_mesh_point_list.append(point2)
				new_tri[2] = z_neg_mesh_point_list.index(point2)
				
				z_neg_mesh_tri_list.append(new_tri)
				
			else:
				new_tri = [-1,-1,-1]
				
				if not point0 in z_cli_mesh_point_list:
					z_cli_mesh_point_list.append(point0)
				new_tri[0] = z_cli_mesh_point_list.index(point0)
				
				if not point1 in z_cli_mesh_point_list:
					z_cli_mesh_point_list.append(point1)
				new_tri[1] = z_cli_mesh_point_list.index(point1)
				
				if not point2 in z_cli_mesh_point_list:
					z_cli_mesh_point_list.append(point2)
				new_tri[2] = z_cli_mesh_point_list.index(point2)
				
				z_cli_mesh_tri_list.append(new_tri)
		
		for tri_index in z_cli_mesh_tri_list:
			
			point0 = z_cli_mesh_point_list[tri_index[0]]
			point1 = z_cli_mesh_point_list[tri_index[1]]
			point2 = z_cli_mesh_point_list[tri_index[2]]
			
			[x1,y1,z1] = point0
			[x2,y2,z2] = point1
			[x3,y3,z3] = point2
			
			tri = [point0, point1, point2]
		
			#if there is one vertex on xy-plane
			if (int(z1 == 0) + int(z2 == 0) + int(z3 == 0)) == 1: 
			
				pos_ver = filter(lambda (x,y,z): z > 0, tri)[0]
				neg_ver = filter(lambda (x,y,z): z < 0, tri)[0]
			
				# begin math stuff...
				pos_ver = array(pos_ver)
				neg_ver = array(neg_ver)
			
				line = pos_ver - neg_ver
				t = -1 * line[2]
				point_a = neg_ver + t * line
			
				line = pos_ver - neg_ver
				t = -1 * neg_ver[2] / line[2]
				point_b = neg_ver + t * line
			
				pos_ver = pos_ver.tolist()
				neg_ver = neg_ver.tolist()
				# end math stuff!
			
				new_pos_tri = tri[:]
				new_pos_tri[new_pos_tri.index(neg_ver)] = pos_ver
			
				new_neg_tri = tri[:]
				new_neg_tri[new_pos_tri.index(pos_ver)] = neg_ver

				#z_positive_mesh.add_tri(new_pos_tri)
				new_tri = [-1,-1,-1]
				point0 = new_pos_tri[0]
				point1 = new_pos_tri[1]
				point2 = new_pos_tri[2]
				
				if not point0 in z_pos_mesh_point_list:
					z_pos_mesh_point_list.append(point0)
				new_tri[0] = z_pos_mesh_point_list.index(point0)
				
				if not point1 in z_pos_mesh_point_list:
					z_pos_mesh_point_list.append(point1)
				new_tri[1] = z_pos_mesh_point_list.index(point1)
				
				if not point2 in z_pos_mesh_point_list:
					z_pos_mesh_point_list.append(point2)
				new_tri[2] = z_pos_mesh_point_list.index(point2)
				
				z_pos_mesh_tri_list.append(new_tri)
				
				#z_negative_mesh.add_tri(neg_new_tri)
				new_tri = [-1,-1,-1]
				point0 = new_neg_tri[0]
				point1 = new_neg_tri[1]
				point2 = new_neg_tri[2]
				
				if not point0 in z_neg_mesh_point_list:
					z_neg_mesh_point_list.append(point0)
				new_tri[0] = z_neg_mesh_point_list.index(point0)
				
				if not point1 in z_neg_mesh_point_list:
					z_neg_mesh_point_list.append(point1)
				new_tri[1] = z_neg_mesh_point_list.index(point1)
				
				if not point2 in z_neg_mesh_point_list:
					z_neg_mesh_point_list.append(point2)
				new_tri[2] = z_neg_mesh_point_list.index(point2)
				
				z_neg_mesh_tri_list.append(new_tri)
				
			else: 
				
				pos_ver = filter(lambda (x,y,z): z > 0, tri)
				neg_ver = filter(lambda (x,y,z): z < 0, tri)
				
				if len(pos_ver) == 2:
					one_ver = neg_ver[0]
					two_ver = pos_ver
				else:
					one_ver = pos_ver[0]
					two_ver = neg_ver
				
				# begin math stuff...
				two_ver_0 = array(two_ver[0])
				two_ver_1 = array(two_ver[1])
				one_ver = array(one_ver)
				
				line_a = two_ver_0 - one_ver
				t_a = -1 * one_ver[2] / line_a[2]
				point_a = one_ver + t_a * line_a
			
				line_b = two_ver_1 - one_ver
				t_b = -1 * one_ver[2] / line_b[2]
				point_b = one_ver + t_b * line_b 
			
				two_ver_0 = two_ver_0.tolist()
				two_ver_1 = two_ver_1.tolist()
				one_ver = one_ver.tolist()
				point_a = point_a.tolist()
				point_b = point_b.tolist()
				# end math stuff!
			
				#pay attention to normals direction
				one_new_tri = tri[:]
				one_new_tri[one_new_tri.index(two_ver_0)] = point_a
				one_new_tri[one_new_tri.index(two_ver_1)] = point_b

				two_new_tri = [tri[:], tri[:]]
				two_new_tri[0][two_new_tri[0].index(one_ver)] = point_a
				two_new_tri[0][two_new_tri[0].index(two_ver_1)] = point_b
				two_new_tri[1][two_new_tri[1].index(one_ver)] = point_b

				if (int(z1>0) + int(z2>0) + int(z3>0)) < 2:
					to_add_one_point_list = z_pos_mesh_point_list
					to_add_one_tri_list = z_pos_mesh_tri_list
					
					to_add_two_point_list = z_neg_mesh_point_list
					to_add_two_tri_list = z_neg_mesh_tri_list
				else:
					to_add_one_point_list = z_neg_mesh_point_list
					to_add_one_tri_list = z_neg_mesh_tri_list
					
					to_add_two_point_list = z_pos_mesh_point_list
					to_add_two_tri_list = z_pos_mesh_tri_list

				#to_add_one.add_tri(one_new_tri)
				new_tri = [-1,-1,-1]
				point0 = one_new_tri[0]
				point1 = one_new_tri[1]
				point2 = one_new_tri[2]
				
				if not point0 in to_add_one_point_list:
					to_add_one_point_list.append(point0)
				new_tri[0] = to_add_one_point_list.index(point0)
				
				if not point1 in to_add_one_point_list:
					to_add_one_point_list.append(point1)
				new_tri[1] = to_add_one_point_list.index(point1)
				
				if not point2 in to_add_one_point_list:
					to_add_one_point_list.append(point2)
				new_tri[2] = to_add_one_point_list.index(point2)
				
				to_add_one_tri_list.append(new_tri)
				
				#to_add_two.add_tri(two_new_tri[0])
				new_tri = [-1,-1,-1]
				point0 = two_new_tri[0][0]
				point1 = two_new_tri[0][1]
				point2 = two_new_tri[0][2]
				
				if not point0 in to_add_two_point_list:
					to_add_two_point_list.append(point0)
				new_tri[0] = to_add_two_point_list.index(point0)
				
				if not point1 in to_add_two_point_list:
					to_add_two_point_list.append(point1)
				new_tri[1] = to_add_two_point_list.index(point1)
				
				if not point2 in to_add_two_point_list:
					to_add_two_point_list.append(point2)
				new_tri[2] = to_add_two_point_list.index(point2)
				
				to_add_two_tri_list.append(new_tri)
				
				#to_add_two.add_tri(two_new_tri[1])
				new_tri = [-1,-1,-1]
				point0 = two_new_tri[1][0]
				point1 = two_new_tri[1][1]
				point2 = two_new_tri[1][2]
				
				if not point0 in to_add_two_point_list:
					to_add_two_point_list.append(point0)
				new_tri[0] = to_add_two_point_list.index(point0)
				
				if not point1 in to_add_two_point_list:
					to_add_two_point_list.append(point1)
				new_tri[1] = to_add_two_point_list.index(point1)
				
				if not point2 in to_add_two_point_list:
					to_add_two_point_list.append(point2)
				new_tri[2] = to_add_two_point_list.index(point2)
				
				to_add_two_tri_list.append(new_tri)
				
		
		z_positive_mesh.point_list = z_pos_mesh_point_list
		z_positive_mesh.tri_index_list = z_pos_mesh_tri_list
		
		z_negative_mesh.point_list = z_neg_mesh_point_list
		z_negative_mesh.tri_index_list = z_neg_mesh_tri_list
		
		return z_positive_mesh, z_negative_mesh

if __name__ == "__main__":
	
	m = Mesh([],[])
	m.add_tri([[0,0,1],[0,1,-1],[1,0,-1]])
	m.add_tri([[0,0,1],[0,0,2],[0,1,-1]])
	print m
	p = m.to_plasm()
	a, b = m.split_z()
	p_a = COLOR(RED)(a.to_plasm())
	p_b = COLOR(GREEN)(b.to_plasm())
	VIEW(STRUCT([p_a, p_b]))

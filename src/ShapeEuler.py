# -*- coding: utf-8 -*-

## This program provides a prototype library for simplicial complexes.
## Includes input, output, skeleton and boundary evaluation, linear
## extrusion, boundary and coboundary operators, and linear combination
## of chains.
## Author: Alberto Paoluzzi (paoluzzi@dia.uniroma3.it)
## Copyright (C) 2009 Dipartimento Informatica e Automazione,
## Università Roma Tre, Rome, Italy.

## This library is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public
## License as published by the Free Software Foundation; either
## version 2.1 of the License, or (at your option) any later version.

## This library is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## Lesser General Public License for more details.

## You should have received a copy of the GNU Lesser General Public
## License along with this library; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""
Module for boundary integration of polynomials over three-dimensional
simplicial domains.

Look for method documentation in:
C, Cattani and A. Paoluzzi: Boundary integration over linear polyhedra.
Computer-Aided Design 22(2): 130-135 (1990) (doi:10.1016/0010-4485(90)90007-Y

"""

from math import *
from numpy import *
from scipy import *
from pyplasm import *

## --------------------------------------------------
## --Utility functions-------------------------------
## --------------------------------------------------

def __evalprint__(string):
	
	print string + " => ", eval(string), "\n"

def choose (n,k):
	"""
	Computes a binomial number.
	Efficient linear recursion implemented.
	
	Returns
	-------
	choose : int
	 	binomial number of n on k
	"""
	
	if k == 0 or n == k: 
		return 1
	else: 
		return choose(n-1, k-1) * n/k


def times(a,b):
	
	c = array([0,0,0])
	c[0] = a[1]*b[2] - a[2]*b[1]
	c[1] = a[2]*b[0] - a[0]*b[2]
	c[2] = a[0]*b[1] - a[1]*b[0]
	
	return c


## --------------------------------------------------
## --Format conversion-------------------------------
## --------------------------------------------------

def complex2surface (obj):
	"""
	Transforms the 2-skeleton of a simplicial complex in a triangulated surface.
	
	Returns 
	-------
	surface: list
		a list of triples of surface vertices (nD points).
	"""
	
	cells = obj.cells
	verts = obj.vertices.points
	surface = [[verts[i-1],verts[j-1],verts[k-1]] for [i,j,k] in obj.cells[2]]
	
	return surface


## --------------------------------------------------
## --Integration utilities---------------------------
## --------------------------------------------------

def M (alpha, beta):
	
	a = 0.0
	for h in range(alpha+2):
		a += choose(alpha+1,h) * ((-1)**h / float(h+beta+1))
	
	return a / (alpha + 1)


def T3 (triangle, alpha,beta,gamma):
	
	def magnitude(vect):
		return math.sqrt(sum(x*x for x in vect))
	
	t = mat(triangle)
	a = (t[1] - t[0]).tolist()[0]
	b = (t[2] - t[0]).tolist()[0]
	c = [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]
	s1 = 0.0
	t = triangle
	for h in range(alpha+1):
		for k in range(beta+1):
			for m in range(gamma+1):
				s2 = 0.0
				for i in range(h+1):
					s3 = 0.0
					for j in range(k+1):
						s4 = 0.0
						for l in range(m+1):
							s4 += choose(m,l) * a[2]**(m-l) * b[2]**l * M(h+k+m-i-j-l,i+j+l)
						s3 += choose(k,j) * a[1]**(k-j) * b[1]**j * s4
					s2 += choose(h,i) * a[0]**(h-i) * b[0]**i * s3
				s1 += choose(alpha,h) * choose(beta,k) * choose(gamma,m) \
						* (t[0][0]**(alpha-h)) * (t[0][1]**(beta-k)) \
						* (t[0][2]**(gamma-m)) * s2
	return s1 * magnitude(c)
	

## --------------------------------------------------
## --Surface integrals-------------------------------
## --------------------------------------------------


def II(surface,alpha,beta,gamma):
	
	w = 0.0
	for triangle in surface:
		w += T3(triangle,alpha,beta,gamma)
	
	return w


## --------------------------------------------------
## --Volume integrals--------------------------------
## --------------------------------------------------


def III(surface,alpha,beta,gamma):
	
	def magnitude(vect):
		return math.sqrt(sum(x*x for x in vect))

	w = 0.0
	for triangle in surface:
		t = mat(triangle)
		a = (t[1] - t[0]).tolist()[0]
		b = (t[2] - t[0]).tolist()[0]
		c = [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]
		w += (c[0] / magnitude(c)) * T3(triangle,alpha+1,beta,gamma)
	
	return w/(alpha + 1)


def AffineEulerMat(surface, fun=III):
	
	def integFun(surface):
		def integFun0(pars):
			return fun(surface,pars[0],pars[1],pars[2])
		return integFun0
	
	exps = [[2,0,0],[1,1,0],[1,0,1],[1,0,0],
					[0,2,0],[0,1,1],[0,1,0],
							[0,0,2],[0,0,1],
									[0,0,0]]
	vals = AA(integFun(surface))(exps)
	
	return [[vals[0],vals[1],vals[2],vals[3]],
			[vals[1],vals[4],vals[5],vals[6]],
			[vals[2],vals[5],vals[7],vals[8]],
			[vals[3],vals[6],vals[8],vals[9]]]

if __name__ == "__main__":
	print "\n## -- Surface integral --------------"
	
	__evalprint__("""
		II([[[0,0,0],[10,0,0],[0,10,0]], 
			[[10,0,0],[10,10,0],[0,10,0]]], 
			0,0,0) """)
	
	__evalprint__(""" 
		II([[[0,0,0],[10,0,0],[0,10,0]], 
			[[10,0,0],[10,10,0],[0,10,0]]], 
			1,0,0) """)

	t0 = [[1, 0, 0], [0, 0, 0], [1, 1, 0]]
	t1 = [[1, 1, 0], [0, 0, 0], [0, 1, 0]]

	t2 = [[0, 0, 1], [1, 0, 1], [1, 1, 1]]
	t3 = [[0, 0, 1], [1, 1, 1], [0, 1, 1]]

	t4 = [[0, 0, 0], [1, 0, 0], [1, 0, 1]]
	t5 = [[0, 0, 0], [1, 0, 1], [0, 0, 1]]

	t6 = [[1, 1, 0], [0, 1, 0], [1, 1, 1]]
	t7 = [[1, 1, 1], [0, 1, 0], [0, 1, 1]]

	t8 = [[0, 0, 0], [0, 1, 1], [0, 1, 0]]
	t9 = [[0, 0, 0], [0, 0, 1], [0, 1, 1]]

	t10 = [[1, 1, 1], [1, 0, 0], [1, 1, 0]]
	t11 = [[1, 0, 1], [1, 0, 0], [1, 1, 1]]

	cube_v1 = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]

	__evalprint__(""" II(cube_v1, 0, 0, 0) """)

	__evalprint__(""" III(cube_v1, 0, 0, 0) """)

	__evalprint__(""" AffineEulerMat(cube_v1) """)

	__evalprint__(""" AffineEulerMat(cube_v1, II) """)

	t0 = [[5, 0, 0], [0, 0, 0], [5, 5, 0]]
	t1 = [[5, 5, 0], [0, 0, 0], [0, 5, 0]]

	t2 = [[0, 0, 5], [5, 0, 5], [5, 5, 5]]
	t3 = [[0, 0, 5], [5, 5, 5], [0, 5, 5]]

	t4 = [[0, 0, 0], [5, 0, 0], [5, 0, 5]]
	t5 = [[0, 0, 0], [5, 0, 5], [0, 0, 5]]

	t6 = [[5, 5, 0], [0, 5, 0], [5, 5, 5]]
	t7 = [[5, 5, 5], [0, 5, 0], [0, 5, 5]]

	t8 = [[0, 0, 0], [0, 5, 5], [0, 5, 0]]
	t9 = [[0, 0, 0], [0, 0, 5], [0, 5, 5]]

	t10 = [[5, 5, 5], [5, 0, 0], [5, 5, 0]]
	t11 = [[5, 0, 5], [5, 0, 0], [5, 5, 5]]
	
	cube_v2 = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]

	__evalprint__(""" II(cube_v2, 0, 0, 0) """)

	__evalprint__(""" III(cube_v2, 0, 0, 0) """)

	__evalprint__(""" AffineEulerMat(cube_v2) """)

	__evalprint__(""" AffineEulerMat(cube_v2, II) """)
	
	__evalprint__(""" 
		II([[[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
			[[1.0, 1.0, 0.0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0]], 
			[[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [0.0, 0.0, 1.0]], 
			[[0.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 1.0]], 
			[[1.0, 1.0, 1.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]],
			[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], 
			[[1.0, 1.0, 1.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], 
			[[0.0, 1.0, 1.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], 
			[[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0]],
			[[1.0, 0.0, 1.0], [0.0, 0.0, 1.0], [1.0, 1.0, 0.0]], 
			[[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]], 
			[[1.0, 0.0, 1.0], [1.0, 1.0, 0.0], [1.0, 0.0, 0.0]]], 
			0,0,0) """)

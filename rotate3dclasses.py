import numpy as np

class Object3d:
	"""represents a 3d object"""
	def __init__(self, g, v, vn, f):
		self.g = g
		self.v = v
		self.vn = vn
		self.f = f

	def rotate(self, rmatrix):
		self.v = self.v.dot(rmatrix)
		self.vn = self.vn.dot(rmatrix)

	def write_to_file(self, filename):
		file = open(filename, 'w')
		file.write('g {}\n'.format(self.g))
		write_section(file, 'v', self.v)
		write_section(file, 'vn', self.vn)
		write_section(file, 'f', self.f)

def write_section(f, identifier, array):
	f.write('\n')
	for item in array:
		f.write('{} {} {} {}\n'.format(identifier, item[0], item[1], item[2]))


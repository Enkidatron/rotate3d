import numpy as np
import math
import argparse

class Object3d:
	"""represents a 3d object parsed from a .obj file"""
	def __init__(self, g, v, vn, f):
		self.g = g
		self.v = v
		self.vn = vn
		self.f = f

	def rotate(self, rmatrix, center_by_volume = False):
		"""Rotate this object by the provided rotation matrix.

		center_by_volume -- if true, use the center of the volume as the rotation point, 
			otherwise, use the mean of the vertexes"""
		if center_by_volume:
			offset = (self.v.max(axis=0) + self.v.min(axis=0)) / 2
		else:
			offset = self.v.mean(axis=0)
		self.v = (self.v - offset).dot(rmatrix) + offset
		self.vn = self.vn.dot(rmatrix)

	def write_to_file(self, filename):
		"""Write the current state of this object to a file in .obj format."""
		file = open(filename, 'w')
		file.write('g {}\n'.format(self.g))
		write_section(file, 'v', self.v)
		write_section(file, 'vn', self.vn)
		write_section(file, 'f', self.f)

def write_section(f, identifier, array):
	"""Write the identifier and points from array to file f."""
	f.write('\n')
	for item in array:
		f.write('{}  {}  {}  {}\n'.format(identifier, round(item[0],6), round(item[1],6), round(item[2],6)))

def read_obj(filename):
	"""Open the provided file and parse the contents as an .obj file. 
	Return the parsed object."""
	file = open(filename, 'r')
	g = ''
	v = []
	vn = []
	f = []
	for line in file:
		tokens = line.split()
		if len(tokens) > 0:
			if tokens[0] == "g":
				g = tokens[1]
			elif tokens[0] == "v":
				v.append(tokens[1:4])
			elif tokens[0] == "vn":
				vn.append(tokens[1:4])
			elif tokens[0] == "f":
				f.append(tokens[1:4])
	return Object3d(g, np.array(v, float), np.array(vn, float), np.array(f, int))

def normalize(x,y,z):
	"""Normalize the given 3d vector."""
	length = (x*x + y*y + z*z)**0.5
	return (x/length, y/length, z/length)

def axis_angle_to_rotation_matrix(x, y, z, angle):
	"""Convert the provided vector and angle to a rotation matrix and return it.

	x,y,z -- the axis vector
	angle -- the angle (in radians) to rotate around the given axis
	"""
	(x,y,z) = normalize(x,y,z)
	first = math.cos(angle) * np.eye(3)
	second = (1 - math.cos(angle)) * np.array([[x*x, x*y, x*z],[y*x,y*y,y*z],[z*x,z*y,z*z]])
	third = math.sin(angle) * np.array([[0,-z,y],[z,0,-x],[-y,x,0]])
	return first + second + third

def main():
	"""Load 3d object from file (default teapot.obj), rotate it 90 degrees around the Z axis, 
	and write the result to a new file."""
	parser = argparse.ArgumentParser(description="Load a 3d object, rotate it, and write the result to a new file.")
	parser.add_argument('input', nargs="?", default="teapot.obj", help="The path to the input file.")
	parser.add_argument('-d', '--degrees', type=float, default=90.0, help="The number of degrees to rotate the object.")
	parser.add_argument('-v', '--volume-center', action='store_true', help="Use the center of the objects volume as the rotation point (default: mean of the vertices)")
	parser.add_argument('-x', type=float, default=0, help="X coordinate of axis vector (default: 0) (default vector: 0,0,1)")
	parser.add_argument('-y', type=float, default=0, help="Y coordinate of axis vector (default: 0) (default vector: 0,0,1)")
	parser.add_argument('-z', type=float, default=0, help="Z coordinate of axis vector (default: 0) (default vector: 0,0,1)")
	args = parser.parse_args()
	if args.x == 0 and args.y == 0 and args.z == 0:
		(x,y,z) = (0,0,1)
	else:
		(x,y,z) = (args.x, args.y, args.z)

	outputfilename = 'rotated_{}'.format(args.input)
	obj3d = read_obj(args.input)
	rotation = axis_angle_to_rotation_matrix(x,y,z,math.radians(args.degrees))
	obj3d.rotate(rotation, args.volume_center)
	obj3d.write_to_file(outputfilename)

if __name__ == '__main__':
	main()
import numpy as np
import math
from rotate3dclasses import Object3d

def read_obj(filename):
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
	length = (x*x + y*y + z*z)**0.5
	return (x/length, y/length, z/length)

def axis_angle_to_rotation_matrix(x, y, z, angle):
	(x,y,z) = normalize(x,y,z)
	first = math.cos(angle) * np.eye(3)
	second = (1 - math.cos(angle)) * np.array([[x*x, x*y, x*z],[y*x,y*y,y*z],[z*x,z*y,z*z]])
	third = math.sin(angle) * np.array([[0,-z,y],[z,0,-x],[-y,x,0]])
	return first + second + third

def main():
	inputfilename = "C:\\dev\\rotate3d\\teapot.obj"
	outputfilename = "rotated_teapot.obj"
	obj3d = read_obj(inputfilename)
	rotation = axis_angle_to_rotation_matrix(0,0,1,(np.pi/2))
	obj3d.rotate(rotation)
	obj3d.write_to_file(outputfilename)

if __name__ == '__main__':
	main()
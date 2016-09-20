import unittest
import numpy as np
import math
import rotate3d

class TestRotate3dMisc(unittest.TestCase):
	"""A basic test suite for rotate3d helper functions"""
	
	def test_normalize_x(self):
		(x,y,z) = rotate3d.normalize(5,0,0)
		np.testing.assert_almost_equal(x, 1)
		np.testing.assert_almost_equal(y, 0)
		np.testing.assert_almost_equal(z, 0)

	def test_normalize_y(self):
		(x,y,z) = rotate3d.normalize(0,10,0)
		np.testing.assert_almost_equal(x, 0)
		np.testing.assert_almost_equal(y, 1)
		np.testing.assert_almost_equal(z, 0)

	def test_normalize_x(self):
		(x,y,z) = rotate3d.normalize(0,0,20)
		np.testing.assert_almost_equal(x, 0)
		np.testing.assert_almost_equal(y, 0)
		np.testing.assert_almost_equal(z, 1)

	def test_normalize_xy(self):
		(x,y,z) = rotate3d.normalize(5,5,0)
		np.testing.assert_almost_equal(x, 1/math.sqrt(2))
		np.testing.assert_almost_equal(y, 1/math.sqrt(2))
		np.testing.assert_almost_equal(z, 0)

	def test_rotation_matrix_x(self):
		matrix1 = rotate3d.axis_angle_to_rotation_matrix(1,0,0,math.radians(90))
		matrix2 = np.array([[1,0,0],[0,0,-1],[0,1,0]])
		np.testing.assert_array_almost_equal(matrix1,matrix2)

	def test_rotation_matrix_y(self):
		matrix1 = rotate3d.axis_angle_to_rotation_matrix(0,1,0,math.radians(90))
		matrix2 = np.array([[0,0,1],[0,1,0],[-1,0,0]])
		np.testing.assert_array_almost_equal(matrix1,matrix2)


class TestRotate3dObject3d(unittest.TestCase):
	"""A basic test suite for rotate3d.Object3d"""

	def setUp(self):
		v = [[1,1,-1],[1,-1,-1],[-1,-1,-1],[-1,1,-1],[0,0,1]]
		vn = []
		f = [[1,2,5],[2,3,5],[3,4,5],[4,1,5]]
		self.obj1 = rotate3d.Object3d('test_object_1', np.array(v), np.array(vn), np.array(f))
		self.obj2 = rotate3d.Object3d('test_object_2', np.array(v), np.array(vn), np.array(f))

	def test_value_equivalence(self):
		np.testing.assert_array_equal(self.obj1.v, self.obj2.v)
		np.testing.assert_array_equal(self.obj1.vn, self.obj2.vn)
		np.testing.assert_array_equal(self.obj1.f, self.obj2.f)

	def test_rotate_and_reverse_x(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(1,0,0,math.radians(90)), False)
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(1,0,0,math.radians(-90)), False)
		np.testing.assert_array_almost_equal(self.obj1.v, self.obj2.v)

	def test_rotate_and_reverse_y(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,1,0,math.radians(90)), False)
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,1,0,math.radians(-90)), False)
		np.testing.assert_array_almost_equal(self.obj1.v, self.obj2.v)

	def test_rotate_and_reverse_z(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,0,1,math.radians(90)), False)
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,0,1,math.radians(-90)), False)
		np.testing.assert_array_almost_equal(self.obj1.v, self.obj2.v)

	def test_cw_90_equals_ccw_270_x(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(1,0,0,math.radians(90)), False)
		self.obj2.rotate(rotate3d.axis_angle_to_rotation_matrix(1,0,0, math.radians(-270)), False)
		np.testing.assert_array_almost_equal(self.obj1.v, self.obj2.v)

	def test_cw_90_equals_ccw_270_y(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,1,0,math.radians(90)), False)
		self.obj2.rotate(rotate3d.axis_angle_to_rotation_matrix(0,1,0, math.radians(-270)), False)
		np.testing.assert_array_almost_equal(self.obj1.v, self.obj2.v)

	def test_cw_90_equals_ccw_270_z(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,0,1,math.radians(90)), False)
		self.obj2.rotate(rotate3d.axis_angle_to_rotation_matrix(0,0,1, math.radians(-270)), False)
		np.testing.assert_array_almost_equal(self.obj1.v, self.obj2.v)

	def test_colinear_axis(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,0,1,math.radians(90)), False)
		self.obj2.rotate(rotate3d.axis_angle_to_rotation_matrix(0,0,1,math.radians(90)), True)
		np.testing.assert_array_equal(self.obj1.v, self.obj2.v)

	def test_rotation_does_not_affect_faces(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,0,1,math.radians(90)), False)
		np.testing.assert_array_equal(self.obj1.f, self.obj2.f)

	def test_axis_rotations_x_y_negative_x_equals_z(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(1,0,0,math.radians(90)), True)
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,1,0,math.radians(90)), True)
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(1,0,0,math.radians(-90)), True)
		self.obj2.rotate(rotate3d.axis_angle_to_rotation_matrix(0,0,1,math.radians(90)), True)
		np.testing.assert_array_almost_equal(self.obj1.v, self.obj2.v)

	def test_45_degree_math_check_x(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(1,0,0,math.radians(45)), True)
		v = np.array([[1,0,-math.sqrt(2)],[1,-math.sqrt(2),0],[-1,-math.sqrt(2),0],[-1,0,-math.sqrt(2)],[0,1/math.sqrt(2),1/math.sqrt(2)]])
		np.testing.assert_array_almost_equal(self.obj1.v, v)

	def test_45_degree_math_check_y(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,1,0,math.radians(45)), True)
		v = np.array([[math.sqrt(2),1,0],[math.sqrt(2),-1,0],[0,-1,-math.sqrt(2)],[0,1,-math.sqrt(2)],[-1/math.sqrt(2),0,1/math.sqrt(2)]])
		np.testing.assert_array_almost_equal(self.obj1.v, v)

	def test_45_degree_math_check_z(self):
		self.obj1.rotate(rotate3d.axis_angle_to_rotation_matrix(0,0,1,math.radians(45)), True)
		v = np.array([[math.sqrt(2),0,-1],[0,-math.sqrt(2),-1],[-math.sqrt(2),0,-1],[0,math.sqrt(2),-1],[0,0,1]])
		np.testing.assert_array_almost_equal(self.obj1.v, v)


if __name__ == '__main__':
	unittest.main()

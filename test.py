# from utility.objects import *;
# #import sys
# from PIL import Image
# import matplotlib.pyplot as plt
import math
import numpy as np

#vec_1 = (0,1)
vec_1 = (615,575,345)
scalar_1 = 34
scalar_2 = 35

param_tuple = (scalar_1,scalar_2,*vec_1)
print(f'param_tuple: {param_tuple}')

# unit_vec_1 = vec_1 / np.linalg.norm(vec_1)
# cos_angle = np.dot(unit_vec_1,vec_2)
# print(f'cos_angle is {cos_angle}')
# angle = np.arccos(cos_angle)
# print(f'Angle in radians is {angle}')
# angle = math.degrees(angle)
# print(f'Degree in angles: {angle}')
#np.set_printoptions(threshold=sys.maxsize)
# im = Image.fromarray(grid * 255)
# im.show()
# pt_1 = (10,9)
# pt_2 = (2,4)
# mid = []
# for i,j in zip(pt_1,pt_2):
#     print(f'i={i} and j = {j}')
#     print(f'The value of i+j is {i+j}')
#     print(f'The value appended: {(i+j)/2.0}')
#     mid.append((i+j)/2.0)
# mid = tuple(mid)
# mid = tuple( (i+j)/2.0 for i,j in zip(pt_1,pt_2))
# test_1 = [1,2,3,4]
# test_2 = [3,4,5,6]
# test_1 += test_2

# def angle_between_vectors(vec_1,vec_2):
#     unit_vec_1 = vec_1 / np.linalg.norm(vec_1)
#     unit_vec_2 = vec_2 / np.linalg.norm(vec_2)
#     cos_angle = np.dot(unit_vec_1,unit_vec_2)
#     angle_radians = np.arccos(cos_angle)
#     return math.degrees(angle_radians)

# vec_1 = (1,1)
# vec_2 = (0,-1)

# print(f'Angle between vector 1 and vector 2 is {angle_between_vectors(vec_1,vec_2)}')
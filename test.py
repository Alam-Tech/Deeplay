# from utility.objects import *;
# #import sys
# from PIL import Image
# import matplotlib.pyplot as plt

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
test_1 = [1,2,3,4]
test_2 = [3,4,5,6]
test_1 += test_2

print(test_1)
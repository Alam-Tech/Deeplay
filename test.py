test_list = [1,2,3,4]
test_tuple = tuple(['iterate bro!',*test_list])
print('The contents of the tuple are:')
for element in test_tuple:
    print(element,end=' ')
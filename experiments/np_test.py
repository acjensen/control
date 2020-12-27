import numpy as np

a = range(100)
A = np.array(a).reshape(len(a)//2, 2)
A = A.ravel().view([('col1', 'i8'), ('col2', 'i8'), ]
                   ).astype([('col1', 'i4'), ('col2', 'i8'), ])
print(A[:5])
# array([(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)],
#       dtype=[('col1', '<i4'), ('col2', '<i8')])

print(A.dtype)
# dtype([('col1', '<i4'), ('col2', '<i8')])

print(A['col1']*A['col2'])

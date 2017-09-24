
# I collaborated with Masud Parvez on this assignment.

import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

x = np.genfromtxt('q4.csv', delimiter = ',')

# number of data points to work with 
m = x.shape[0]

# Subtracting the mean of the dataset
mu = x.sum(axis=1) / m
mu  = mu.reshape((mu.shape[0],1))
xc = x - mu

# Finding the covariance 
C = xc.T.dot(xc)

#Finding the eigenvalues & vectors
S, V = np.linalg.eigh(C)
sortidx = S.argsort()[::-1] 
S = S[sortidx][0:62]
V = V[:,sortidx][:,0:62]
V = xc.dot(V)

S = S[::-1]
for i in range(0,62):
    V[:,i] = V[:,i]/np.linalg.norm(V[:,i])

#displaying eigenvalues in descending order
vals = np.arange(62) + 1
plt.scatter(vals, S)
plt.show()

j = 2
#reconstructing the 0th face
refx0 = np.zeros(4500)
for k in range(0,j):
    eig = V.T[k]
    val = eig.T.dot(x.T[0])
    refx0 = refx0 + val*(eig)
    
#reconstructing the 1st face
refx1 = np.zeros(4500)
for k in range(0,j):
    eig = V.T[k]
    val = eig.T.dot(x.T[1])
    refx1 = refx1 + val*(eig)

#displaying reconstructed 0th face
face0 = refx0 
img = np.reshape(face0, (75, 60), order='F')
imgplot = plt.imshow(img, cmap = 'gray')
plt.show()

#displaying reconstruced 1st face
face1 = refx1 
img = np.reshape(face1, (75, 60), order='F')
imgplot = plt.imshow(img, cmap = 'gray')
plt.show()

#finding reconstruction error for 0th face
error0 = np.linalg.norm(x[:,0] - face0, 2)
print(error0)

#finding reconstruction error for 1th face
error1 = np.linalg.norm(x[:,1] - face1, 2)
print(error1)

#displaying the eigenfaces used
for k in range(0,j):
    img = np.reshape(V.T[k], (75, 60), order='F')
    imgplot = plt.imshow(img, cmap = 'gray')
    plt.show()



"""
    Your goal of this assignment is implementing your own K-means.

    Input:
         pixels: data set. Each row contains one data point. For image
         dataset, it contains 3 columns, each column corresponding to Red,
         Green, and Blue component.

         K: the number of desired clusters. Too high value of K may result in
         empty cluster error. Then, you need to reduce it.

    Output:
         assignment: the class assignment of each data point in pixels. The
         assignment should be 1, 2, 3, etc. For K = 5, for example, each cell
         of class should be either 1, 2, 3, 4, or 5. The output should be a
         column vector with size(pixels, 1) elements.

         centroid: the location of K centroids in your result. With images,
         each centroid corresponds to the representative color of each
         cluster. The output should be a matrix with size(pixels, 1) rows and
         3 columns. The range of values should be [0, 255].

     To illustrate, sklearn's kmeans function was used. Your job is to replace
     the call to sklearn's kemans function with your OWN implementation.

     You will get ZERO points for not modifying this script, or using other library
     to call k-means clustering.
"""
import numpy as np
from sklearn.cluster import KMeans

def mykmeans(pixels, K):
    # ===== COMMENT BELOW LINES OUT AND IMPLEMENT YOUR OWN FUNCTION HERE =====
    #kmeans = KMeans(n_clusters=int(K), random_state=0).fit(pixels)
    #assignment1 = kmeans.labels_
    #centroid1 = kmeans.cluster_centers_
    # ========================================================================
    K = int(K)
    centroid = pixels[np.random.randint(pixels.shape[0], size=K), :]
    assignment = np.zeros(pixels.shape[0])
    distances = np.zeros((pixels.shape[0], K))
    iterations = 100
    for iteration in range(iterations):
        for i in range(pixels.shape[0]):
            for k in range(K):
                distances[i][k] = (np.linalg.norm(pixels[i]-centroid[k]))
                assignment[i] = np.argmin(distances[i])
        for k in range(K):
            total = ([0,0,0])
            count = 0
            for i in range(pixels.shape[0]):
                if assignment[i] == k:
                    count += 1
                    total += pixels[i]
            total[:] = [int(x / count) for x in total]
            centroid[k] = total

    return(assignment, centroid)


import numpy as np
import matplotlib.pyplot as plt

def multiclass_logistic_regression(xtrain, ytrain, xtest, ytest, stepsize, total_iter):
    """

    :param xtrain:
    :param ytrain:
    :param xtest:
    :param ytest:
    :param stepsize: learning rate
    :param total_iter: maximum number of iterations for updating
    :return:
    """
    total_iter = int(total_iter)
    C = 3
    trainerr = np.zeros(total_iter)
    testerr = np.zeros(total_iter)
    W = 0.001*np.ones((xtrain.shape[1], C))
    y = np.zeros((xtrain.shape[0], C))

    indices1 = np.where(ytrain==1)[0]
    indices2 = np.where(ytrain==2)[0]
    indices3 = np.where(ytrain==3)[0]
    y[indices1] = [1, 0, 0]
    y[indices2] = [0, 1, 0]
    y[indices3] = [0, 0, 1]

    trainerr = np.zeros(total_iter)
    testerr = np.zeros(total_iter)
   
    for n in range(total_iter):
        grad1 = np.zeros(xtrain.shape[1])
        grad2 = np.zeros(xtrain.shape[1])
        grad3 = np.zeros(xtrain.shape[1])
        for x in range(xtrain.shape[0]):
            total = 0
            for c in range(C):
                total += np.exp(np.dot(W[:,c].T, xtrain[x]))
            z11 = np.dot(y[x,0], xtrain[x])
            z12 = np.dot(np.exp(np.dot(W[:,0].T, xtrain[x])), xtrain[x])/total
            z21 = np.dot(y[x,1], xtrain[x])
            z22 = np.dot(np.exp(np.dot(W[:,1].T, xtrain[x])), xtrain[x])/total
            z31 = np.dot(y[x,2], xtrain[x])
            z32 = np.dot(np.exp(np.dot(W[:,2].T, xtrain[x])), xtrain[x])/total
            grad1 += (z11 - z12)
            grad2 += (z21 - z22)
            grad3 += (z31 - z32)
        W[:,0] += stepsize*grad1
        W[:,1] += stepsize*grad2
        W[:,2] += stepsize*grad3
        traincount = 0
        testcount = 0
        
        for x in range(xtrain.shape[0]):
            total = 0
            for c in range(C):
                total += np.exp(np.dot(W[:,c].T, xtrain[x]))
            p1 = np.exp(np.dot(W[:,0].T, xtrain[x]))/total
            p2 = np.exp(np.dot(W[:,1].T, xtrain[x]))/total
            p3 = np.exp(np.dot(W[:,2].T, xtrain[x]))/total
            if ytrain[x] == 1 and max(p1, p2, p3) != p1:
                traincount += 1
            elif ytrain[x] == 2 and max(p1, p2, p3) != p2:
                traincount += 1
            elif ytrain[x] == 3 and max(p1, p2, p3) != p3:
                traincount += 1
                
        for x in range(xtest.shape[0]):
            total = 0
            for c in range(C):
                total += np.exp(np.dot(W[:,c].T, xtest[x]))
            p1 = np.exp(np.dot(W[:,0].T, xtest[x]))/total
            p2 = np.exp(np.dot(W[:,1].T, xtest[x]))/total
            p3 = np.exp(np.dot(W[:,2].T, xtest[x]))/total
            if ytest[x] == 1 and max(p1, p2, p3) != p1:
                testcount += 1
            elif ytest[x] == 2 and max(p1, p2, p3) != p2:
                testcount += 1
            elif ytest[x] == 3 and max(p1, p2, p3) != p3:
                testcount += 1              
        trainerr[n] = traincount/(1.0*xtrain.shape[0])
        testerr[n] = testcount/(1.0*xtest.shape[0])

    plt.plot(trainerr)
    plt.ylabel('train error')
    plt.xlabel('iteration')
    plt.show()

    plt.plot(testerr)
    plt.ylabel('test error')
    plt.xlabel('iteration')
    plt.show()
    return W, trainerr, testerr


def my_recommender(rate_matrix, low_rank):
    """

    :param rate_matrix:
    :param low_rank:
    :return:
    """

    # Parameters
    maxIter = 0 # CHOOSE YOUR OWN
    learningRate = 0 # CHOOSE YOUR OWN
    regularizer = 0 # CHOOSE YOUR OWN

    U = None # PERFORM INITIALIZATION
    V = None # PERFORM INITIALIZATION

    # PERFORM GRADIENT DESCENT
    # IMPLEMENT YOUR CODE HERE

    return U, V

"""
    Implement your functions here for Bayes classification.clear

    Each function takes in training and testing sets as input,
    and returns accuracy on classification for training and testing sets, respectively.
"""

def modelFull(train, test):
    cno = 2
    import numpy as np
    ytrain = train[:,-1]
    ytest = test[:,-1]
    xtrain = train[:,:-1]
    xtest = test[:,:-1]
    d = xtrain.shape[1] #number of attributes
    m = xtrain.shape[0] #number of datapoints
    
    indices0 = np.where(ytrain==0)[0]
    indices1 = np.where(ytrain==1)[0]
    xtrain0 = xtrain[indices0]
    xtrain1 = xtrain[indices1]
    
    py = np.zeros(cno)
    for c in range(cno):
        py[c] = (ytrain == c).sum() / (1.0*m)
    
    xmean0 = np.mean(xtrain0, axis = 0)
    xmean1 = np.mean(xtrain1, axis = 0)
    
    xcov0 = np.cov(xtrain0, rowvar = False)
    xcov1 = np.cov(xtrain1, rowvar = False)
    
    traincount = 0
    testcount = 0

    #making matrices non-singular
    xcov0 = 0.01*np.identity(d)+xcov0 
    xcov1 = 0.01*np.identity(d)+xcov1

    #calculating constants so they don't have to be done in loops
    c1 = (d/2)*np.log(2*np.pi) 
    c2 = .5*np.linalg.slogdet(xcov0)[1]
    c3 = .5*np.linalg.slogdet(xcov1)[1]

    for i in range(xtest.shape[0]):
        x = xtest[i]
        px0 = -.5*np.dot((x-xmean0), np.dot((x-xmean0).T, np.linalg.inv(xcov0))) -c1 - c2
        px1 = -.5*np.dot((x-xmean1), np.dot((x-xmean1).T, np.linalg.inv(xcov1))) -c1 - c3
        px0 += np.log(py[0]) 
        px1 += np.log(py[1])
        if px1 > px0:
            if ytest[i] == 0:
                testcount += 1
        else:
            if ytest[i] == 1:
                testcount += 1
                
    for i in range(m):
        x = xtrain[i]
        px0 = -.5*np.dot((x-xmean0), np.dot((x-xmean0).T, np.linalg.inv(xcov0))) -c1 - c2
        px1 = -.5*np.dot((x-xmean1), np.dot((x-xmean1).T, np.linalg.inv(xcov1))) -c1 - c3
        px0 += np.log(py[0]) 
        px1 += np.log(py[1])
        if px1 > px0:
            if ytrain[i] == 0:
                traincount += 1
        else:
            if ytrain[i] == 1:
                traincount += 1
    
    err_train = traincount/(1.0*m)
    err_test = testcount/(1.0*xtest.shape[0])

    return err_train, err_test

def modelDiagional(train, test):
    cno = 2
    import numpy as np
    ytrain = train[:,-1]
    ytest = test[:,-1]
    xtrain = train[:,:-1]
    xtest = test[:,:-1]
    d = xtrain.shape[1] #number of attributes
    m = xtrain.shape[0] #number of datapoints
    
    indices0 = np.where(ytrain==0)[0]
    indices1 = np.where(ytrain==1)[0]
    xtrain0 = xtrain[indices0]
    xtrain1 = xtrain[indices1]
    
    py = np.zeros(cno)
    for c in range(cno):
        py[c] = (ytrain == c).sum() / (1.0*m)
    
    xmean0 = np.mean(xtrain0, axis = 0)
    xmean1 = np.mean(xtrain1, axis = 0)
    
    xcov0 = np.diag(np.cov(xtrain0, rowvar = False)+ 0.01*np.identity(d))
    xcov1 = np.diag(np.cov(xtrain1, rowvar = False)+ 0.01*np.identity(d))
    
    traincount = 0
    testcount = 0

    #calculating constants so they don't have to be done in loops
    c1 = (d/2)*np.log(2*np.pi) 
    c2 = .5*np.sum(np.log(xcov0))
    c3 = .5*np.sum(np.log(xcov1))

    for i in range(xtest.shape[0]):
        x = xtest[i]
        px0 = -.5*np.sum((x-xmean0)**2/xcov0) -c1 - c2
        px1 = -.5*np.sum((x-xmean1)**2/xcov1) -c1 - c3
        px0 += np.log(py[0]) 
        px1 += np.log(py[1])
        if px1 > px0:
            if ytest[i] == 0:
                testcount += 1
        else:
            if ytest[i] == 1:
                testcount += 1
                
    for i in range(m):
        x = xtrain[i]
        px0 = -.5*np.sum((x-xmean0)**2/xcov0) -c1 - c2
        px1 = -.5*np.sum((x-xmean1)**2/xcov1) -c1 - c3
        px0 += np.log(py[0])
        px1 += np.log(py[1])
        if px1 > px0:
            if ytrain[i] == 0:
                traincount += 1
        else:
            if ytrain[i] == 1:
                traincount += 1
    
    err_train = traincount/(1.0*m)
    err_test = testcount/(1.0*xtest.shape[0])

    return err_train, err_test

def modelSpherical(train, test):
    cno = 2
    import numpy as np
    ytrain = train[:,-1]
    ytest = test[:,-1]
    xtrain = train[:,:-1]
    xtest = test[:,:-1]
    d = xtrain.shape[1] #number of attributes
    m = xtrain.shape[0] #number of datapoints
    
    indices0 = np.where(ytrain==0)[0]
    indices1 = np.where(ytrain==1)[0]
    xtrain0 = xtrain[indices0]
    xtrain1 = xtrain[indices1]
    
    py = np.zeros(cno)
    for c in range(cno):
        py[c] = (ytrain == c).sum() / (1.0*m)
    
    xmean0 = np.mean(xtrain0, axis = 0)
    xmean1 = np.mean(xtrain1, axis = 0)
    
    xcov0 = np.mean(np.diag(np.cov(xtrain0, rowvar = False)))
    xcov1 = np.mean(np.diag(np.cov(xtrain1, rowvar = False)))
    
    traincount = 0
    testcount = 0

    #calculating constants so they don't have to be done in loops
    c1 = (d/2)*np.log(2*np.pi*xcov0)
    c2 = (d/2)*np.log(2*np.pi*xcov1)

    for i in range(xtest.shape[0]):
        x = xtest[i]
        px0 = -(np.linalg.norm(x-xmean0)**2)/(2*xcov0) -c1
        px1 = -(np.linalg.norm(x-xmean1)**2)/(2*xcov1) -c2
        px0 += np.log(py[0]) 
        px1 += np.log(py[1])
        if px1 > px0:
            if ytest[i] == 0:
                testcount += 1
        else:
            if ytest[i] == 1:
                testcount += 1
                
    for i in range(m):
        x = xtrain[i]
        px0 = -(np.linalg.norm(x-xmean0)**2)/(2*xcov0) -c1
        px1 = -(np.linalg.norm(x-xmean1)**2)/(2*xcov1) -c2
        px0 += np.log(py[0])
        px1 += np.log(py[1])
        if px1 > px0:
            if ytrain[i] == 0:
                traincount += 1
        else:
            if ytrain[i] == 1:
                traincount += 1
    
    err_train = traincount/(1.0*m)
    err_test = testcount/(1.0*xtest.shape[0])

    return err_train, err_test






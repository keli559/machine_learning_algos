class data4ml:
    # ==== 1. download data =====
    import numpy as np
    import random as rd
    import pixelLookup as pl
    import kmeans4nrain as k4n
    fname = '20050316.41787.7.dat'
    data = np.genfromtxt(fname)
    #
    pixelDict = pl.pixelLookup().buildDictionary()
    SurfTypeDict = k4n.kmeans4nrain().buildSurfTypeDict()
    X = []
    y = []
    surf = []
    for ii in range(len(data)):
        pixel = pl.pixelLookup().\
                lookupPixel(data[ii, 0], \
                            data[ii, 1], pixelDict)
        try:
            SurfType = SurfTypeDict[pixel]
            if np.max(data[ii, 2:11]) > 300:
                pass
            else:
                X.append(\
                         np.concatenate(\
                                        (data[ii, [0, 1]], \
                                        np.log(300.0-data[ii, 2:11])),\
                                        axis = 0)
                         )
                y.append(data[ii, 11])
                surf.append(SurfType)
        except:
            pass

    X = np.array(X)
    y = np.array(y)
    surf = np.array(surf)
    m = len(X)
    # =====2. split into Train/CrossVal/Test ====
    # 60% of the data is ramdomly picked for training
    # 20% for cross validation
    # 20% for testing
    index = range(m)
    indShuffled = rd.sample(index, len(index))
    indicesTrain = indShuffled[0:int(0.6*m)]
    indicesVal = indShuffled[int(0.6*m):int(0.8*m)]
    indicesTest = indShuffled[int(0.8*m):m]

    Xtrain = X[indicesTrain, :]
    Xval = X[indicesVal, :]
    Xtest = X[indicesTest, :]

    ytrain = y[indicesTrain]
    yval = y[indicesVal]
    ytest = y[indicesTest]
    
    surftrain = surf[indicesTrain]
    surfval = surf[indicesVal]
    surftest = surf[indicesTest]
    #
    g = open('Train.dat', 'w')
    for ii in indicesTrain:
        printLine = (2*'{:8.2f}').format(X[ii, 0], X[ii, 1]) +\
                    (9*'{:8.2f}').format(X[ii, 2], X[ii, 3], \
                                         X[ii, 4], X[ii, 5], \
                                         X[ii, 6], X[ii, 7], \
                                         X[ii, 8], X[ii, 9], \
                                         X[ii, 10]) + \
                    '{0:8.2f}'.format(y[ii]) +\
                    '{0:3d}'.format(int(surf[ii]))
        print>>g, printLine
    g.close()

    g = open('Validation.dat', 'w')
    for ii in indicesVal:
        printLine = (2*'{:8.2f}').format(X[ii, 0], X[ii, 1]) +\
                    (9*'{:8.2f}').format(X[ii, 2], X[ii, 3], \
                                         X[ii, 4], X[ii, 5], \
                                         X[ii, 6], X[ii, 7], \
                                         X[ii, 8], X[ii, 9], \
                                         X[ii, 10]) + \
                    '{0:8.2f}'.format(y[ii]) +\
                    '{0:3d}'.format(int(surf[ii]))
        print>>g, printLine
    g.close()

    g = open('Test.dat', 'w')
    for ii in indicesTest:
        printLine = (2*'{:8.2f}').format(X[ii, 0], X[ii, 1]) +\
                    (9*'{:8.2f}').format(X[ii, 2], X[ii, 3], \
                                         X[ii, 4], X[ii, 5], \
                                         X[ii, 6], X[ii, 7], \
                                         X[ii, 8], X[ii, 9], \
                                         X[ii, 10]) + \
                    '{0:8.2f}'.format(y[ii]) +\
                    '{0:3d}'.format(int(surf[ii]))
        print>>g, printLine
    g.close()
        
                    
    
    
    


    

    
    
    
    

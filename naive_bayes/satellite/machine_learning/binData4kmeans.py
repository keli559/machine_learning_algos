class binData4kmeans:
    import numpy as np
    import pixelLookup as plu
    import scipy.cluster.vq as scv
    #====== 1. load data ======
    print('Loading the data...\n')

    pDict = plu.pixelLookup().buildDictionary()
    pDictRev =  plu.pixelLookup().buildDictionaryRev()
    pixelTbDict = {}

    # ===== 2. Bin non-rain samples ===
    print('Bin non-rain samples...\n')

    f = open('filelist', 'r')
    for fname in f:
        fname = fname.strip()
        print fname
        data = np.genfromtxt(fname)
        m = len(data)
        for ii in range(m):
            lat = data[ii, 0]
            lon = data[ii, 1]
            tbs = data[ii, 2:11]
            rain = data[ii, 11]
            pixel = plu.pixelLookup().lookupPixel(lat, lon, pDict)
            if max(tbs) < 300.0:
                logTbs = np.log(300-tbs)
                if rain == 0.0:
                    if pixel != -999:
                        if pixel not in pixelTbDict.keys():
                            pixelTbDict[pixel] = [1, logTbs]
                        else:
                            pixelTbDict[pixel][0] += 1
                            pixelTbDict[pixel][1] += logTbs
    f.close()
    # === 3.calculate average===
    print('Calcualte the average Tbs...\n')
    g = open('pixelData.dat', 'w')
    mPTD = len(pixelTbDict.keys())
    for ii in range(mPTD):
        pixel = pixelTbDict.keys()[ii]
        count = pixelTbDict.values()[ii][0]
        sumLogTbs = pixelTbDict.values()[ii][1]
        aveLogTbs = sumLogTbs/float(count)
        printLine =  '{0:8d}'.format(pixel) +\
                     (9*'{:8.2f}').format(aveLogTbs[0], aveLogTbs[1], \
                                          aveLogTbs[2], aveLogTbs[3], \
                                          aveLogTbs[4], aveLogTbs[5], \
                                          aveLogTbs[6], aveLogTbs[7], \
                                          aveLogTbs[8])
        print >> g, printLine
    g.close()
         
#    #====== 2. collect non-rain samples===
#    nrain= data[data[:, 11]==0.0]
#    X = nrain[:, 2:10] # brightness temperatures
#    #====== 3. kmeans clustering====
#    cluster_centroids2, closest_centroids = scv.kmeans2(X, 6, iter=50)
#    #====== 4. count land types ====

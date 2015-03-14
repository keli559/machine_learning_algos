class pixelLookup:
    import numpy as np
#    def __init__(self):
    latCut = np.arange(-40, 40, 0.5)
    lonCut = np.arange(-180, 180, 0.5)
    m = len(latCut)
    n = len(lonCut)
    def buildDictionary(self):
        pixelDict = dict()
        pixelSeq = range((self.m-1)*(self.n-1))
        kk = 0
        for ii in range(self.m-1):
            for jj in range(self.n-1):
                pixelDict[(self.latCut[ii], self.latCut[ii+1] \
                           , self.lonCut[jj], self.lonCut[jj+1])] \
                    = pixelSeq[kk]
                kk += 1
        return pixelDict
    def buildDictionaryRev(self):
        pixelDictRev = dict()
        pixelSeq = range((self.m-1)*(self.n-1))
        kk = 0
        for ii in range(self.m-1):
            for jj in range(self.n-1):
                pixelDictRev[pixelSeq[kk]] = \
                           [(self.latCut[ii], self.latCut[ii+1] \
                           , self.lonCut[jj], self.lonCut[jj+1])]
                kk += 1
        return pixelDictRev

    def findRange(self, lat, lon):
        for ii in range(self.m-1):
            if self.latCut[ii] < lat<= self.latCut[ii+1]:
                latFloor = self.latCut[ii]
                latCeil = self.latCut[ii+1]
        for jj in range(self.n-1):
            if self.lonCut[jj] < lon<= self.lonCut[jj+1]:
                lonFloor = self.lonCut[jj]
                lonCeil = self.lonCut[jj+1]
        return (latFloor, latCeil, lonFloor, lonCeil)
    def findRange_faster(self, lat, lon):
        intLat = int(lat)
        intLon = int(lon)
        decLat = lat - intLat
        decLon = lon - intLon
        if 0<=decLat<0.5:
            latFloor = intLat
            latCeiling = intLat + 0.5
        else:
            latFloor = intLat + 0.5
            latCeiling = intLat + 1.0

        if 0<=decLon<0.5:
            lonFloor = intLon
            lonCeiling = intLon + 0.5
        else:
            lonFloor = intLon + 0.5
            lonCeiling = intLon + 1.0
        return (latFloor, latCeiling, lonFloor, lonCeiling)

    def lookupPixel(self, lat, lon, pixelDict):
        pixelNum = -999
        try:
            latlonRange = self.findRange_faster(lat, lon)
            pixelNum = pixelDict[latlonRange]
        except:
            pass
        return pixelNum
        
        
       
        
        
        




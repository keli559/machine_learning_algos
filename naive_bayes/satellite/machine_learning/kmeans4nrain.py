import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def cb_setup():
#                                                                                                                                        
# it serves to produce a color bar provided by Prof Petty.                                                                               
#                                                                                                                                        
   cvalue = np.linspace(0, 1.0, 8)
   cdict = {'red': (
                 (cvalue[0], 0.0, 0.0),
                 (cvalue[2], 0.0, 0.0),
                 (cvalue[3], 1.0, 1.0),
                 (cvalue[7], 1.0, 1.0)
                   ),
             'green': (
                   (cvalue[0], 0.0, 0.0),
                   (cvalue[1], 0.0, 0.0),
                   (cvalue[2], 1.0, 1.0),
                   (cvalue[3], 1.0, 1.0),
                   (cvalue[5], 0.0, 0.0),
                   (cvalue[6], 0.0, 0.0),
                   (cvalue[7], 1.0, 1.0)
                     ),
            'blue': (
                  (cvalue[0], 0.0, 0.0),
                  (cvalue[1], 1.0, 1.0),
                  (cvalue[2], 0.0, 0.0),
                  (cvalue[5], 0.0, 0.0),
                  (cvalue[6], 1.0, 1.0),
                  (cvalue[7], 1.0, 1.0),
                    )}
   my_cmap = plt.matplotlib.\
          colors.LinearSegmentedColormap('my_colormap',cdict,256)
   return my_cmap


class kmeans4nrain:
    import scipy.cluster.vq as scv
    data = np.genfromtxt('pixelData.dat')
    X = data[:, 1:]
    X = scv.whiten(X)

    initClust = np.array([\
       [ 5.40537965,  6.9414287 ,  5.00155048,  6.46733489, \
         6.06645943,  6.67625689,  7.04979324,  8.42085976, \
         8.06725299],\
       [ 4.29619145,  5.43382856,  4.22199185,  5.26505412, \
         5.48116489,  6.05874133,  5.98643509,  9.68003757, \
         8.30679181],\
       [ 5.4407308 ,  6.96549997,  5.13717944,  6.6179713 , \
         6.4003951 ,  6.83727572,  7.20389284,  9.22587997, \
         8.83097016],\
       [ 3.20164772,  4.54381514,  2.90826365,  4.09287009, \
         3.89807414,  4.45094419,  4.68186561,  6.93197967, \
         6.18554413],\
       [ 3.83568664,  5.26730824,  3.63297475,  4.90886069, \
         4.71204917,  5.22139821,  5.45312607,  8.08485787, \
         7.19202815],\
       [ 2.28203895,  4.31184433,  1.62857942,  3.68636259, \
         2.89921004,  3.42254833,  4.22406922,  5.69402771, \
         5.55372006],\
       [ 5.36293963,  6.90367231,  4.83684629,  6.28106608, \
         5.6669195 ,  6.46387638,  6.8476799 ,  7.71250864,  \
         7.30455517]])\



    [centroid, label] = scv.kmeans2(X, initClust)
    surfTypeNum = len(initClust)
#    surfTypeNum = 7
#    [centroid, label] = scv.kmeans2(X, k=surfTypeNum)
    def buildSurfTypeDict(self):
       dictionary = {}
       try:
          dictionary = dict(zip(self.data[:, 0].astype(int), self.label))
       except:
          print 'no elements are added to SurfTypeDict'
       return dictionary
    def plotSerfType(self):
       import pixelLookup as pl
       dictRev = pl.pixelLookup().buildDictionaryRev()
       m = len(self.data)
       latlon = []
       for ii in range(m):
           pixel = int(self.data[ii, 0])
           tmp = dictRev[pixel][0]
           lat = (tmp[0]+tmp[1])/2.0
           lon = (tmp[2]+tmp[3])/2.0
           latlon.append([lat, lon, self.label[ii]])
           
           
       latlon = np.array(latlon)
       canvas_size = 8
       fig = plt.figure(0, figsize = (2*canvas_size, canvas_size))
       ax=fig.add_subplot(111)
       marg = 0.0
       map = Basemap(projection='cyl',llcrnrlon=-180,urcrnrlon=180,\
                     llcrnrlat=-80,urcrnrlat=80,resolution='l')
       #map.bluemarble()
       map.drawcoastlines()
       map.drawcountries()
       mycolormap = cb_setup()
       x1, y1 = map(latlon[:, 1], latlon[:, 0])
       map.scatter(x1, y1, cmap = mycolormap,\
                   c = latlon[:, 2]+1, vmin = 0, vmax = self.surfTypeNum+1, lw = 0)
       plt.savefig('landTypes.png')
       plt.show()


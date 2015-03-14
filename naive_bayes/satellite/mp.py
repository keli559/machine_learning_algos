# 
from pyhdf.SD import SD, SDC
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from math import radians, degrees
from pyhdf.SD import *
from pyhdf.VS import *
from string import split, find
from os import chdir, system
from StringIO import StringIO
import os
from time import clock
import pickle
from TRMMquery import *

############## subfunctions ##############
   
###   
def read_tmi(filename, variable):
  # print filename
#
# it serves to read in hdf data according to its filename, and extract
# the variable we are interested in
#
# input: filename   -    the file name including '.HDF' of 1B11 data
#        variable   -    variable name in the data instruction list, or by using
#                           "mygroup.datasets()" command and check the list
# output: dset      -    data set in the format of array in python.
#
   mygroup = SD(filename, SDC.READ)   
   data_tran = mygroup.select(variable)
   dset = np.array(data_tran[:])
   return dset

###
def channel_extract(filename, channel):
#
# it serves to extract brightness temperature at certain channel with its CORRESPONDING
# latitude and longitude. Be reminded that there are low resolution data and hight resolutions data.
# low resolution data sets are: 10 v,h, 19 v,h, 21 v, 37 v,h
# high resolution data sets are: 85 v,h
# 
# 
# input: filename  -   the file name including '.HDF' of 1B11 data
#        channel   -   orderal number that refers to certain channels
#                      0  ->   10 v
#                      1  ->   10 h
#                      2  ->   19 v
#                      3  ->   19 h
#                      4  ->   21 v
#                      5  ->   37 v
#                      6  ->   37 h
#                      7  ->   85 v
#                      8  ->   85 h
# output: lats       -    latitude 2D matrix
#         lons       -    longitude 2D matrix
#         tb_channel -    brightness temperature at a chosen channel
#         swath_res  -    swath resolution of this chosen channel (low or high resolution)
#
   lat_hi = read_tmi(filename, 'Latitude')
   lon_hi = read_tmi(filename, 'Longitude')
   #print lon_hi.shape
   ihi, jhi = lat_hi.shape    
   if (channel <= 6): # demonstrates the 7 lower resolution channels: 10 v,h, 19 v,h, 21 v, 37 v,h.
      swath_res = 10.2 # in the unit of kilometers
      lats = lat_hi[:, 0:jhi:2]
      lons = lon_hi[:, 0:jhi:2]
      #print lats.shape
     
      tempb = read_tmi(filename, 'lowResCh')
      tempb = (tempb/100.0) + 100.0
      tb_channel = tempb[:, :, channel]

      return lats, lons, tb_channel, swath_res
   
   elif (8>=channel>=7):# demonstrates the 2 higher resolution channels: 85 v,h
      swath_res = 5.1 # in the unit of kilometers
      lats = lat_hi
      lons = lon_hi

      tempb = read_tmi(filename, 'highResCh')
      tempb = (tempb/100.0) + 100.0
      tb_channel = tempb[:, :, channel-7]

      return lats, lons, tb_channel, swath_res
   else:
      raise IOError('please make sure channel is within 0 and 8, representing 9 channels in 1B11 data!')
###
#
def getflag(filename):
   validity = read_tmi(filename, 'validity')
   geoqual = read_tmi(filename, 'geoQuality')
   missing = read_tmi(filename, 'missing')
   dataqual = read_tmi(filename, 'dataQuality')
   flag =  (missing == 0.0) & (validity == 0.0) & (geoqual == 0.0) & (dataqual == 0.0)
   scori = read_tmi(filename, 'SCorientation')
   return flag, scori

      
###
def gc_angle(lat1, lat2, lon1, lon2):
    #
    # This subfunction serves to calculate the great circle angle
    # between to chosen points on the earth.
    # input: lat1, lat2, lon1, lon2   -  geolocations of two points
    #                                    (lon1, lat1) and (lon2, lat2)
    # output: ang/ang_r      - great circle angle between two points
    #               
    #
    if (lat1 > 90.0)|(lat1 < -90.0)|(lat2 > 90.0)|(lat2 < -90.0):
        raise IOError('Latitudes are out of range, please check your input!')
    elif (lat1 == 90.0) & (lat2 == -90.0):
        ang = lat1 - lat2
        return ang
    elif (lat2 == 90.0) & (lat1 == -90.0):
        ang = lat2 - lat1
        return ang
    else:
        # convert to radians
        dlat1 = radians(lat1)
        dlat2 = radians(lat2)
        dlon1 = radians(lon1)
        dlon2 = radians(lon2)
        # calculate great circle angle
        ang_r = np.arccos(np.sin(dlat1)*np.sin(dlat2)\
                          + np.cos(dlat1)*np.cos(dlat2)*np.cos(dlon1 - dlon2))
        # convert back to degrees and return
        #ang = degrees(ang_r)
        return ang_r
###
def gc_angle_matr(lat1, lat2, lon1, lon2):
    #
    # This subfunction serves to calculate the great circle angle
    # between to chosen points on the earth.
    # input: matrices of lat1, lat2, lon1, lon2   -  geolocations of two points
    #                                    (lon1, lat1) and (lon2, lat2)
    # output: ang/ang_r      - great circle angle between two points
    #               
    #


    if (np.max(lat1) > 90.0)|(np.min(lat1) < -90.0)|(np.max(lat2) > 90.0)|(np.min(lat2) < -90.0):
        raise IOError('Latitudes are out of range, please check your input!')
    else:
    # convert to radians
        dlat1 = np.radians(lat1)
        dlat2 = np.radians(lat2)
        dlon1 = np.radians(lon1)
        dlon2 = np.radians(lon2)
        # calculate great circle angle
        trans = np.sin(dlat1)*np.sin(dlat2)\
                          + np.cos(dlat1)*np.cos(dlat2)*np.cos(dlon1 - dlon2)
        trans[np.where(trans > 1.0)] = 1.0
        trans[np.where(trans < -1.0)] = -1.0
        ang_r = np.arccos(trans)
        # convert back to degrees and return
        #ang = degrees(ang_r)
        return ang_r
###
def rainrate_extract(filename):
    lat = read_tmi(filename, 'Latitude')
    lon = read_tmi(filename, 'Longitude')
    rainrate = read_tmi(filename, 'nearSurfRain')
    return lat, lon, rainrate
#
###

def window_search(istart, jstart, lats, lons, lat0, lon0, deltai, deltaj):
#
# lat_array and lon_array are from 2A25 data!
#
   M, N = lats.shape
   R_earth = 6378.1 # Radius of the Earth
   mindis = 1e10
   mm = 0
   nn = 0

   i0 = istart - deltai
   i1 = istart + deltai
   if i0<0:
      i0=0
   if i1>M-1:
      i1 = M-1

   j0 = jstart - deltaj
   j1 = jstart + deltaj
   if j0<0:
      j0 = 0
   if j1 > N-1:
      j1 = N-1

# calculate the distance as a matrix.
   lat = lats[i0:i1+1, j0:j1+1]
   lon = lons[i0:i1+1, j0:j1+1]
   distance = R_earth*gc_angle_matr(lat0, lat, lon0, lon)
   
   for ii in range(i0,i1+1):
      for jj in range(j0,j1+1):
         if (distance[ii-i0, jj-j0] < mindis):
            mindis = distance[ii-i0, jj-j0]
            mm = ii
            nn = jj
            mindis_index = (ii, jj)
   return  mindis_index, mindis
#
###

def radius_search(istart, jstart, lats, lons, lat0, lon0, deltai, deltaj, radius):
#
# lats and lons are from 2A25 data!
#
   M, N = lats.shape
   R_earth = 6378.1 # Radius of the Earth

   i0 = istart - deltai
   i1 = istart + deltai
   if i0<0:
      i0=0
   if i1>M-1:
      i1 = M-1

   j0 = jstart - deltaj
   j1 = jstart + deltaj
   if j0<0:
      j0 = 0
   if j1 > N-1:
      j1 = N-1
   chosenind = []
   chosendis = []
   lat_matr = lats[i0:i1+1, j0:j1+1]
   lon_matr = lons[i0:i1+1, j0:j1+1]
   dist_matr = R_earth* gc_angle_matr(lat0, lat_matr, lon0, lon_matr)
   
   for ii in range(i0,i1+1):
      for jj in range(j0, j1+1):
         if (dist_matr[ii - i0, jj - j0] < radius):
            chosenind.append((ii, jj))
            chosendis.append(dist_matr[ii-i0, jj-j0])
   return  chosenind, chosendis
#
###
def Denary2Binary(n):
    #'''convert denary integer n to binary string bStr'''
    bStr = ''
    if n < 0: raise ValueError, "must be a positive integer"
    if n == 0: return '0'
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    return bStr
###
def linear_tmi2pr(lat_tmi, lon_tmi, lat_pr, lon_pr, flag_tmi):
   n1 = 300
   n2 = 2500
   while True:
       #print n1
       if flag_tmi[n1] == False:
           n1 = n1 + 1
       else:
           break
   lat = lat_tmi[n1, 52]
   lon = lon_tmi[n1, 52]
   pr_irange = 150
   while True:
       [ipair0, mindis0] = window_search(775, 0, lat_pr, lon_pr, lat, lon, pr_irange, 400)
       #print 775 - ipair0[0], pr_irange, mindis0
       if np.abs(775 - ipair0[0]) != pr_irange:
           break
       else:
           pr_irange = pr_irange + 10
   #
   while True:
       #print n2
       if flag_tmi[n2] == False:
           n2 = n2 - 1
       else:
           break
   lat = lat_tmi[n2, 52]
   lon = lon_tmi[n2, 52]
   pr_irange = 150
   while True:
       #print pr_irange
       [ipair1, mindis0] = window_search(7765, 0, lat_pr, lon_pr, lat, lon, pr_irange, 400)
       if np.abs(7765 - ipair1[0]) != pr_irange:
           break
       else:
           pr_irange = pr_irange + 10
   # 
   tmipr_scangradient = (ipair1[0]-ipair0[0])/float(n2 - n1)
   tmipr_scanoffset = int(ipair0[0] - tmipr_scangradient*n1 + 0.5)
   tmi_pr_start = int(-tmipr_scanoffset/tmipr_scangradient + 0.5)
   tmi_pr_end = int((M_pr-tmipr_scanoffset)/tmipr_scangradient + 0.5)
   return tmipr_scangradient, tmipr_scanoffset, tmi_pr_start, tmi_pr_end
###
#
def pr_match(lat_tmi, lon_tmi, lat_pr, lon_pr, radius, M_tmi, N_tmi, gradient, offset, scori_tmi, flag):
   R_earth = 6378.1
   di_min, di_max, dj_min, dj_max = 50, -50, 50, -50
   Sr = radius/np.sqrt(np.log(2))
   jprmatch = ( -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999,   48,   48,   48,   48,   48,   47,   45,   44,   42,   40,   38,   35,   33,   31,   29,   27,   25,   23,   21,   19,   16,   14,   12,   10,    8,    6,    4,    2,    0,    0,    0,    0,    0,    0, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999)
   iproffset = (-999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -8, -7, -7, -6, -5, -4, -4, -3, -3, -2, -2, -2, -1, -1, -1, -1, -1,  0,  0, -1, -1, -1, -1, -1, -2, -2, -2, -3, -3, -4, -5, -6, -6, -7, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999)
   result = []
   for itmi in range(M_tmi):
      for jtmi in range(N_tmi): 

         jpr = jprmatch[jtmi]
         if jpr < 0:
            ipr = -999
         else:
            # the attitude flag decides which way to add the iproffset
            ipr = int(gradient*itmi + 0.5) + offset + (-1)**(scori_tmi[0]/180)*iproffset[jtmi]
            if (ipr<0)|(ipr>M_pr-1):
               ipr, jpr = [-999, -999]
         #
         lat, lon = lat_tmi[(itmi, jtmi)], lon_tmi[(itmi, jtmi)] # tmi
         if (ipr < 0) | (jpr < 0) | (flag[itmi] == False):
            pool = []
            pooldis = []
            distance = -999.0
         else:
            [pool, pooldis] = radius_search(ipr, jpr, lat_pr, lon_pr, lat, lon, 10, 10, radius)
            #distance = R_earth* gc_angle(lat, lat_pr[ipr, jpr], lon, lon_pr[ipr, jpr])
            #Once get the distances of the chosen dots, calculate the weighting for averaging
         weight = np.exp(-(pooldis/Sr)**2.0)
         num = len(pool)
         #
         #
         pr_chosen = []
         sum1 = 0.0
         sum2 = 0.0
         # calculate the weighed average
         for ii in range(num):
            pr_chosen.append(pr[pool[ii]])
            sum1 = sum1 + weight[ii]*pr[pool[ii]]
            sum2 = sum2 + weight[ii]
            #calculate the index distance di and dj
            # di
            if (pool[ii][0] - ipr) < di_min:
               di_min = pool[ii][0] - ipr
            if (pool[ii][0] - ipr) > di_max:
               di_max = pool[ii][0] - ipr
            if (pool[ii][1] - jpr) < dj_min:
               dj_min = pool[ii][1] - jpr
            if (pool[ii][1] - jpr) > dj_max:
               dj_max = pool[ii][1] - jpr
         #if jtmi == 103:
         #    print itmi, di_min, di_max, dj_min, dj_max, flag[itmi]
             
         #
         #if itmi == 1539:

         #print (itmi, jtmi), di_min, di_max, dj_min, dj_max
         #
         if num == 0: # if there is absolutely no pr pixels chosen at all
             w_ave = -999.0
         elif (np.min(pr_chosen) < 0.0) | (flag[itmi] == False): # judge whether both pr and tmi data is valid
            #print np.min(pr_chosen)
            w_ave = -999.0
         elif (num < int(0.11*(radius**2) + 0.5)): # judge whether tmi pixel is fully covered by pr
             if (45 < jtmi < 61)  & (tmi_pr_start + 5 < itmi < tmi_pr_end - 5):
                 print 'At (',itmi, ', ', jtmi, '), number of chosen PR pixels: ', num, '< ', int(0.11*(radius**2) + 0.5)
             w_ave = -999.0
         else:
            w_ave = float(sum1)/sum2
         #print '{0:6d}{1:6d} -> {2:6d}{3:6d} {4:8.2f} {5:6d} {6: 8.2f}'.format(itmi, jtmi, ipr, jpr,distance ,num, w_ave)
         result.append(w_ave)
         #print >> file, '{:7.2f}'.format(float(w_ave)),
         #if jtmi == N_tmi-1:
         #   print >> file, '\n',
   #return pool
   #print pr_chosen
   return np.array(result).reshape((M_tmi, N_tmi))
###
#
def download_conv_coef_oldcoef(path):
    chdir(path)
    # dimension of convolution coef: 94 x 11 x 11
    w10v = readin_weigh_oldcoef('BG_COEF_10V_TO_19_TMI_PREBOOST.TXT', 94, 11)
    w10h = readin_weigh_oldcoef('BG_COEF_10H_TO_19_TMI_PREBOOST.TXT', 94, 11)
    w21v = readin_weigh_oldcoef('BG_COEF_21_TO_19_TMI_PREBOOST.TXT', 94, 11)
    w37v = readin_weigh_oldcoef('BG_COEF_37V_TO_19_TMI_PREBOOST.TXT', 94, 11)
    w37h = readin_weigh_oldcoef('BG_COEF_37H_TO_19_TMI_PREBOOST.TXT', 94, 11)
    # dimension of convolution coef: 198 x 11 x 11
    w85v = readin_weigh_oldcoef('BG_COEF_85V_TO_19_TMI_PREBOOST.TXT', 198, 11)
    w85h = readin_weigh_oldcoef('BG_COEF_85H_TO_19_TMI_PREBOOST.TXT', 198, 11)
    return w10v, w10h, w21v, w37v, w37h, w85v, w85h
###
#
def readin_weigh_oldcoef(filename, pixel, nline):
# it functions to extract the weigh matrix for a certain channel. 
    f = open(filename, 'r')
    f.readline()
    f.readline()
    weigh = []
    for line in range(pixel):
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        arr = []
        for ii in range(nline):
            file = f.readline()
            data = np.genfromtxt(StringIO(file), delimiter = 20)[0:nline]
            arr.append(data)
        norm = np.array(arr)/np.sum(arr)
        weigh.append(norm)
        del(arr)
    f.close()
    return weigh
###
def resolution_match_oldcoef(t10v, t10h, t19v, t19h, t21v, t37v, t37h, t85v, t85h, \
                         w10v, w10h, w21v, w37v, w37h, w85v, w85h, flag, scori):
    # this function serves to multiply the weighting matrix to the 11x11 tmi data window to generated data of same resolutions
    # as 19GHz.
    # input t...        :     tmi data of brightness temperature of different channel except 19, since 19v and 19h don't need
    #                         a change.
    #       flag        :     "Missing", "Validity", and "Geolocation Quality" flags of EACH SCAN
    #                         "True" gives valid, "False" gives not valid
    # output mt....     :     Matched Tmi (mt) data in different channels
    #
    
    [M, N] = t10v.shape
    if scori[0]!=scori[M-1]:
        raise IOError('orbit changes directions!')
    elif scori[0] == 180:
        co10v = np.flipud(w10v)
        co10h = np.flipud(w10h)
        co21v = np.flipud(w21v)
        co37v = np.flipud(w37v)
        co37h = np.flipud(w37h)
        co85v = np.flipud(w85v)
        co85h = np.flipud(w85h)
    else:
        co10v = w10v
        co10h = w10h
        co21v = w21v
        co37v = w37v
        co37h = w37h
        co85v = w85v
        co85h = w85h
    #print M,N
    mt10v = np.zeros((M, N))
    mt10h = np.zeros((M, N))
    mt19v = np.zeros((M, N))
    mt19h = np.zeros((M, N))
    mt21v = np.zeros((M, N))
    mt37v = np.zeros((M, N))
    mt37h = np.zeros((M, N))
    mt85v = np.zeros((M, N))
    mt85h = np.zeros((M, N))
    for scan in range(M):
       for pixel in range(N):
            if (not flag[scan]): # calculate it at least when the center data is valid
                mt10v[scan, pixel] = -999.0
                mt10h[scan, pixel] = -999.0
                mt19v[scan, pixel] = -999.0
                mt19h[scan, pixel] = -999.0
                mt21v[scan, pixel] = -999.0
                mt37v[scan, pixel] = -999.0
                mt37h[scan, pixel] = -999.0
                mt85v[scan, pixel] = -999.0
                mt85h[scan, pixel] = -999.0
            elif (scan<5)|(scan>M-6)|(pixel<5)|(pixel>N-6): # no edges
                mt10v[scan, pixel] = -999.0
                mt10h[scan, pixel] = -999.0
                mt19v[scan, pixel] = -999.0
                mt19h[scan, pixel] = -999.0                    
                mt21v[scan, pixel] = -999.0
                mt37v[scan, pixel] = -999.0
                mt37h[scan, pixel] = -999.0
                mt85v[scan, pixel] = -999.0
                mt85h[scan, pixel] = -999.0
            elif (sum(flag[scan-5: scan+6]) < 11): # every single data in the pool should be valid
                mt10v[scan, pixel] = -999.0
                mt10h[scan, pixel] = -999.0
                mt19v[scan, pixel] = -999.0
                mt19h[scan, pixel] = -999.0
                mt21v[scan, pixel] = -999.0
                mt37v[scan, pixel] = -999.0
                mt37h[scan, pixel] = -999.0
                mt85v[scan, pixel] = -999.0
                mt85h[scan, pixel] = -999.0
            else:
                mt10v[scan,pixel] = np.sum(t10v[scan-5: scan+6, pixel-5:pixel+6]*co10v[pixel - 5])
                mt10h[scan,pixel] = np.sum(t10h[scan-5: scan+6, pixel-5:pixel+6]*co10h[pixel - 5])
                mt19v[scan,pixel] = t19v[scan, pixel]
                mt19h[scan,pixel] = t19h[scan, pixel]
                mt21v[scan,pixel] = np.sum(t21v[scan-5: scan+6, pixel-5:pixel+6]*co21v[pixel - 5])
                mt37v[scan,pixel] = np.sum(t37v[scan-5: scan+6, pixel-5:pixel+6]*co37v[pixel - 5])
                mt37h[scan,pixel] = np.sum(t37h[scan-5: scan+6, pixel-5:pixel+6]*co37h[pixel - 5])
                mt85v[scan,pixel] = np.sum(t85v[scan-5: scan+6, 2*pixel-5:2*pixel+6]*co85v[2*pixel - 5])
                mt85h[scan,pixel] = np.sum(t85h[scan-5: scan+6, 2*pixel-5:2*pixel+6]*co85h[2*pixel - 5])
    return mt10v, mt10h, mt19v, mt19h, mt21v, mt37v, mt37h, mt85v, mt85h
##################### Main Program ######################
# parameters:
radius = 11.0
path = ('../files_reading')
path_data = ('/Volumes/data2b/TRMM/PR_TMI')

# read in weighting function for resolution matching:
# it opens a txt file and extracts its data.
# the subfunction also normalizes the weighed matrices
# the pixel starts at 6 and ends at 99 for low sampling channels and 203 for high sampling channels
[w10v, w10h, w21v, w37v, w37h, w85v, w85h] = download_conv_coef_oldcoef('../tmi_pr_data')
#

# Download the orbit:
chdir(path)
# 23551, 29239
for iorbit in range(11918, 12050):
  #print iorbit 
  resulttmi = TMIfetch(iorbit)
  resultpr = PRfetch(iorbit)
# check for valid file
  #print resulttmi.exists
  if  resulttmi.exists and resultpr.exists:
    fnametmi = resulttmi.localpath
    #print fnametmi
    fnamepr = resultpr.localpath
    #print fnamepr
    line = fnametmi
    # open the files, download the data
    tmi = line.strip()
    pr = tmi.replace('TMI', 'PR').replace('1B11', '2A25')+'.Z'
    fn_pr = pr[pr.index('.HDF')-21: pr.index('.HDF')+4]
    fn_sum_up = pr[pr.index('.HDF')-16: pr.index('.HDF')+1] + 'dat'
    print fn_sum_up
    fn_tmi = tmi[38:63]
    sysp = os.popen('ls -lt '+tmi)
    syss = sysp.readline()
    size_tmi = float(syss.split()[4])
    sysp = os.popen('ls -lt '+pr)
    syss = sysp.readline()
    size_pr = float(syss.split()[4])
    #print size_tmi, size_pr
    #print os.path.exists(tmi), os.path.exists(pr)
    if (not os.path.exists(tmi))|(not os.path.exists(pr)): # loop over if either one of TMI or PR file doesn't exist.
       print 'files missing!' 
       continue
    elif (size_tmi < 13000000.0)|(size_pr < 17000000.0): # check the size of tmi and pr files before reading them
       print 'files are damaged!'
       continue
    else:
       #print (not os.path.exists(fn_pr + '.Z') ) & (not os.path.exists(fn_pr))
       #if (not os.path.exists(fn_pr + '.Z') ) & (not os.path.exists(fn_pr)):
       #   system('cp '+ pr + ' ' + path_data)
       system('cp '+ pr + ' ' + path_data)
       #if os.path.exists(fn_tmi) == False:
       #   system('cp '+ tmi+ ' ' + path_data)
       system('cp '+ tmi+ ' ' + path_data)
       #print fn_pr
       #print not os.path.exists(fn_pr)
       #if not os.path.exists(fn_pr):
       #   system('uncompress ' + fn_pr + '.Z')
       chdir(path_data)
       system('uncompress -f ' + fn_pr + '.Z')
       [lat_pr, lon_pr, pr] = rainrate_extract(fn_pr)
       #
       [lat_tmi, lon_tmi, t10v, swath_low] = channel_extract(fn_tmi, 0)
       [lat, lon, t10h, swath] = channel_extract(fn_tmi, 1)
       [lat, lon, t19v, swath] = channel_extract(fn_tmi, 2)
       [lat, lon, t19h, swath] = channel_extract(fn_tmi, 3)
       [lat, lon, t21v, swath] = channel_extract(fn_tmi, 4)
       [lat, lon, t37v, swath] = channel_extract(fn_tmi, 5)
       [lat, lon, t37h, swath] = channel_extract(fn_tmi, 6)
       [lat_hi, lon_hi, t85v, swath_hi] = channel_extract(fn_tmi, 7)
       [lat, lon, t85h, swath] = channel_extract(fn_tmi, 8)
       del(lat, lon, swath)
       swath_tmi = swath_low*np.sqrt(2)
       
       #
       [M_pr, N_pr] = lat_pr.shape
       [M_tmi, N_tmi] = lat_tmi.shape
       #print M_pr, M_tmi
       [flag_tmi, scori_tmi] = getflag(fn_tmi)
       [flag_pr, scori_pr] = getflag(fn_pr)
       #
       if (scori_tmi[0] != scori_tmi[M_tmi-1])|(M_tmi < 2800)|(M_pr < 8900): # loop over if the orbit is in the process of changing directions
          print 'orbit is too short!'
          pass
       elif (np.min(lat_tmi) < -90.0)|(np.max(lat_tmi) > 90.0)|(np.min(lat_pr) < -90.0)|(np.max(lat_pr) >\
 90.0):
          print 'Latitudes error!'
          pass

       else:
          #
          # 2. Using to points at scan 300 and scan 2500 in TMI to define index slope in PR, and its offset
          #    so that:
          #                        PR = slope x TMI + offset 
          # 
          #print fn_tmi
          [gradient, offset, tmi_pr_start, tmi_pr_end] = linear_tmi2pr(lat_tmi, lon_tmi, lat_pr, lon_pr, flag_tmi)
          #print tmi_pr_start, tmi_pr_end
          #print scori_tmi
          # 3. Do PR matching
          pr_interp = pr_match(lat_tmi, lon_tmi, lat_pr, lon_pr, radius, M_tmi, N_tmi, gradient, offset, scori_tmi, flag_tmi)
          # 4. Do the resolution matching
          #
          [mt10v, mt10h, mt19v, mt19h, mt21v, mt37v, mt37h, mt85v, mt85h] \
                  = resolution_match_oldcoef(t10v, t10h, t19v, t19h, t21v, t37v, t37h, t85v, t85h, \
                                         w10v, w10h, w21v, w37v, w37h, w85v, w85h, flag_tmi, scori_tmi)
          # write them to a file
          file = open(fn_sum_up,'w')
          for ii in range(M_tmi):
              for jj in range(N_tmi):
#                  print >> file, '{0:7.2f}{1:8.2f}'.format(float(lat_tmi[ii, jj]), float(lon_tmi[ii, jj])),
#                  print >> file, ('{:7.1f}'*9).format(float(mt10v[ii,jj]), float(mt10h[ii,jj]), float(mt19v[ii,jj]), float(mt19h[ii,jj]), float(mt21v[ii,jj]), float(mt37v[ii,jj]), float(mt37h[ii,jj]), float(mt85v[ii,jj]), float(mt85h[ii,jj])), 
#                  print >> file, '{:7.2f}'.format(float(pr_interp[ii, jj]))

                   outline = '{0:7.2f}{1:8.2f}'.format(float(lat_tmi[ii, jj]), float(lon_tmi[ii, jj]))+\
              ('{:7.1f}'*9).format(float(mt10v[ii,jj]), float(mt10h[ii,jj]), float(mt19v[ii,jj]), \
              float(mt19h[ii,jj]), float(mt21v[ii,jj]), float(mt37v[ii,jj]), \
              float(mt37h[ii,jj]), float(mt85v[ii,jj]), float(mt85h[ii,jj]))+\
              '{:7.2f}'.format(float(pr_interp[ii, jj]))

                   valid = (outline.find("-999.0") == -1)
                   if (valid):
                       print >> file, outline


          file.close()
    # delete both '1B11' and '2A25' if they exist
    chdir(path_data)
    if os.path.exists(fn_pr):
        system('rm '+ fn_pr)
    if os.path.exists(fn_tmi):
        system('rm '+ fn_tmi)
    
          
          
          
          
                
    
    

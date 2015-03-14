# ==== 0. Load in data ====
import numpy as np
import matplotlib.pyplot as plt
print('Loading sample data ...\n')

data = np.genfromtxt('20050316.41789.7.dat')
m = len(data)
n = len(data[1, ])
print('Data has ' +  str(m) + ' records, and '+ str(n)+ ' variables.\n')
titleLine = (4*'{:7s}').format('   lat', '   lon', '   Ch1', '   Ch2') +\
            ' ... '+\
            '{:5s}'.format('  rain')
print titleLine
for ii in range(10):
    dataLine = (4*'{:7.1f}').format(data[ii, 0], data[ii, 1], \
                                    data[ii, 2], data[ii, 3]) +\
            ' ... '+\
            '{:5.1f}'.format(data[ii, 11])
    print dataLine

plt.scatter(data[:, 11], data[:, 4], linewidth = 0)
plt.ylim(180,300)
plt.xlim(0, 40)
plt.ylabel('Ch3')
plt.xlabel('Rain Rate')
plt.title('Ch v.s. rain')
plt.savefig('signal_rain.png')
plt.show()
# ==== 1. Bin Data into 0.5x0.5 Pixels ===
print('==Bin Data==')
print('Bin data into 0.5 x 0.5 degree pixels for surface categorization.\n')
import os.path
if not os.path.isfile('pixelData.dat'):
    import binData4means as bd4m
else:
    pass

raw_input('Press any key to continue.\n')
#=====2. Kmeans Clustering ====
print('==K-means Clustering==')
import kmeans4nrain as k4n
tmp = k4n.kmeans4nrain()
print('Number of Clusters: '+str(tmp.surfTypeNum))
print('\n')
tmp.plotSerfType()

#====3. Split Data into Train/Val/Test ===
print('==Split Data==')
print('Split data into train, val, test sets...\n')
import data4ml as d4m
mtrain = len(d4m.data4ml().Xtrain)
mval = len(d4m.data4ml().Xval)
mtest = len(d4m.data4ml().Xtest)
print('Training set has '+ str(mtrain)+ ' records\n')
print('Cross Val set has '+ str(mval)+ ' records\n')
print('Test set has '+str(mtest)+' records\n')







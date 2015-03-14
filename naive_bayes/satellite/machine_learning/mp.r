rm(list=ls())
fname = '20050316.41792.7.dat'
titles = as.matrix(read.table('titles', sep = ','))
data = read.table(fname)
#
colnames(data)= titles
# check whether ggmap is installed
if(!require('ggmap')){
	library('ggmap')
	require(ggmap)
}
if(!require('rworldmap')){
	library('rworldmap')
	require(rworldmap)
}
# assume that surface temperature is constantly 300 degrees
# get rid of any records with max value >= 300
maxTb = apply(data[, -c(1, 2, 12)], 1, max)
data = subset(data, maxTb < 300.0)
# log(Tsurf - Tb)
data[, -c(1, 2, 12)] = log(300.0 - data[, -c(1, 2, 12)])
# scale the data
X = data[, -c(1, 2, 12)]
y = data[, c(12)]
loc = data[, c(1, 2)]
means = apply(X, 2, mean)
stds = apply(X, 2, sd)
X = t(apply(X, 1, function(x) (x-means)/stds))
nrain = subset(X, y == 0.00)
nrainLoc = subset(loc, y == 0.00)

#-- kmean clustering---
numberClusters = 6
set.seed(1)
kClust = kmeans(nrain, centers = numberClusters, nstart = 100)
#newmap = getMap(resolution='low')
#plot(newmap, xlim=c(-180, 180), ylim = c(-35, 35), asp = 1)
#points(nrainLoc[, 2], nrainLoc[, 1], col = kClust$cluster, lwd = 0.0, pch = 19)
#

#--- Bin Sample Surface types---
lonCut = seq(-180, 180, by = 0.5)
latCut = seq(-40, 40, by = 0.5)
lonBin = cut(nrainLoc[, 2], lonCut)
latBin = cut(nrainLoc[, 1], latCut)
nrainLoc = data.frame(nrainLoc)
nrainLoc$latlonBins = paste0(latBin, lonBin)
nrainLoc$Surface = kClust$cluster
nrainLoc$lon = NULL
nrainLoc$lat = NULL
if(!require(stringr)){
	require(stringr)
	library(stringr)
}
### Within the same bin, choose the surface 
### with the highest counts as the landtype.
#source('unifySurfaceTypes.r')

if(!require('reshape2')){
	library('reshape2')
	require('reshape2')
}

nrainLoc$Surface = paste0('Surface.',str_trim(as.character(nrainLoc$Surface)))
nrainLoc$value = rep(1, length(nrainLoc[, 1]))
tmp = dcast(nrainLoc, latlonBins ~ Surface)
#####
save(tmp, file='tmp.rda')
#####
#tmp$Surface = paste0('Surface.', 
#	    as.character(apply(tmp[, 2:(numberClusters+1)], 1, which.max)))
#nrainLoc = tmp[,-c(2:(numberClusters+1))]
#rm(tmp)
#
## --- Merge to All Bins ---
#source('makeAllBins.r')
#
## --- Categorize Surface Type on Training sets ---
#loc$latlonBins = with(loc, paste0(cut(lat, latCut), cut(lon, lonCut)))
#loc$Surface = as.factor(latlon2type[loc$latlonBins])
#loc$latlonBins = NULL
##
## --- 2. Dimension Reduction ---
#svd1 = svd(X)
#u1 = svd1$u[, 1]
#u2 = svd1$u[, 2]
#u3 = svd1$u[, 3]
#pcs = data.frame(cbind(u1, u2, u3, y))
#colnames(pcs) = c('pc1', 'pc2', 'pc3', 'rain')
#
## --- 3. Naive Bayes ----
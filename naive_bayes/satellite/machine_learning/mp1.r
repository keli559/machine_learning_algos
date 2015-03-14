rm(list=ls())
if(!require('irlba')){
	library('irlba')
	require(irlba)
}
data = read.table('Train.dat')
colnames(data)= list('lat', 'lon', 'ch1', 'ch2',
		'ch3', 'ch4',
		'ch5', 'ch6',
		'ch7', 'ch8',
		'ch9', 'rain', 'type')
loc = data[, c(1:2)]
X = data[, c(3:11)]
y = data[, c(12)]
surf = data[, c(13)]
# ==== perform SVD for each SurfType ===

alltypes = unique(surf)
result = data.frame()

for (type in alltypes){
    Xsub = X[surf ==type, ]
    Xsub = scale(Xsub)
    locsub = loc[surf == type, ]
    ysub = y[surf==type]
    Ssub=irlba(as.matrix(Xsub), nu = 3, nv = 3)
    result=rbind(result, cbind(locsub, Ssub$u, ysub, surf[surf==type]))
}
colnames(result) = c('lat', 'lon', 'pc1', 'pc2', 'pc3', 'rain', 'type')




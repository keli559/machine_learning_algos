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
#
result[, 3:5] = round(result[, 3:5], 2)
rainBins = c(-0.0001, 0, 0.01, 0.02, 0.03, 
	 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 1.7, 
	 3.0, 5.2, 10.0, 17.0, 30)
result$range = cut(result$rain, rainBins)

#
#par(mfrow = c(1, 3))
#plot(result[, 3], pch=19, col = result$type, ylab=names(result)[3])
#legend('topleft', legend = unique(result$type), col=unique(result$type), pch=1)
#plot(result[, 4], pch=19, col = result$type, ylab=names(result)[4])
#plot(result[, 5], pch=19, col = result$type, ylab=names(result)[5])
#
subData = subset(result, (type == 3)&(pc1==0.04))
predict = mean(subData$rain)
barplot(table(subData$range))


if(!file.exists('./samsungData.rda')){
	url = 'https://d396qusza40orc.cloudfront.net/exdata/data/clusteringEx_data.zip'
	download.file(url, 'data.zip', method = 'curl')
	unzip('data.zip')
	file.remove('data.zip')
	file.copy('./data/samsungData.rda', './samsungData.rda')
	unlink('./data', recursive=T)
}

load('./samsungData.rda')
par(mfrow = c(1, 2), mar=c(5, 4, 1, 1))
samsungData = transform(samsungData, activity = factor(activity))
sub1 = subset(samsungData, subject == 1)
plot(sub1[, 1], col = sub1$activity, ylab=names(sub1)[1])
plot(sub1[, 2], col = sub1$activity, ylab = names(sub1)[2])
legend('bottomright', legend = unique(sub1$activity), col = unique(sub1$activity), pch=1)

distanceMatrix = dist(sub1[, 1:3])
hclustering = hclust(distanceMatrix)
myplclust(hclustering, lab.col = unclass(sub1$activity))
plot(hclustering)

par(mfrow = c(1, 2))
plot(sub1[, 10], pch=19, col = sub1$activity, ylab=names(sub1)[10])
plot(sub1[, 11], pch=19, col = sub1$activity, ylab=names(sub1)[11])

# svd analysis, trying to figure out which variables have the most influence on learning Y. 
svd1 = svd(scale(sub1[, -c(562, 563)]))
#distMatr = dist(
#	 cbind(
#		
#		data.matrix(sub1[, -c(562, 563)]) %*% svd1$v[, 1],
#		data.matrix(sub1[, -c(562, 563)]) %*% svd1$v[, 2],
#		data.matrix(sub1[, -c(562, 563)]) %*% svd1$v[, 3],
#		data.matrix(sub1[, -c(562, 563)]) %*% svd1$v[, 4],
#		data.matrix(sub1[, -c(562, 563)]) %*% svd1$v[, 5],
#		data.matrix(sub1[, -c(562, 563)]) %*% svd1$v[, 6],
#		data.matrix(sub1[, -c(562, 563)]) %*% svd1$v[, 7]
#	 ))
distMatr = dist(
	 cbind(
		sub1[, c(10:12)], 
		sub1[, 66],
		svd1$u[, c(5)]
		)
	 )

#distMatr = dist(cbind(sub1[, c(10:12)], svd1$u[, 2]))
hcl = hclust(distMatr)
par(mfrow = c(1, 1))
myplclust(hcl, lab = as.character(sub1$activity), lab.col = unclass(sub1$activity))




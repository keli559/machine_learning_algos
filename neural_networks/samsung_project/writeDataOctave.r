# write the accelerometer data to file. 
# 1. write activity into file 'y.csv'
write.table(unclass(sub1$activity), './y.csv', sep=',', row.names = F, col.names=F)
# 2. write activity into file 'X.csv'
write.table(unclass(sub1[,c(1:561)]), './X.csv', sep=',', row.names = F, col.names=F)


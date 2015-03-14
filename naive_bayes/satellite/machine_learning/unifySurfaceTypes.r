# unifySurfaceTypes

if(!require('reshape2')){
	library('reshape2')
	require('reshape2')
}

nrainLoc$Surface = paste0('Surface.',str_trim(as.character(nrainLoc$Surface)))
nrainLoc$value = rep(1, length(nrainLoc[, 1]))
tmp = dcast(nrainLoc, latlonBins ~ Surface)
tmp$Surface = paste0('Surface.', 
	    as.character(apply(tmp[, 2:(numberClusters+1)], 1, which.max)))
nrainLoc = tmp[,-c(2:(numberClusters+1))]
rm(tmp)

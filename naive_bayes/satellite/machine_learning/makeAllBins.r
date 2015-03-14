m = length(lonCut)
n = length(latCut)
a2 = rep(lonCut[1:(m-1)], each=n-1)
a3 = rep(latCut[1:(n-1)], m-1)
surfBins = data.frame(cbind(a2, a3))
colnames(surfBins) = c('lonStart', 'latStart')
surfBins$lonEnd = surfBins$lonStart + 0.5
surfBins$latEnd = surfBins$latStart + 0.5
surfBins$lonBins = paste0('(', as.character(surfBins$lonStart), ',',
as.character(surfBins$lonEnd), ']')
surfBins$latBins = paste0('(', as.character(surfBins$latStart), ',',
as.character(surfBins$latEnd), ']')
surfBins$latlonBins = paste0(surfBins$latBins, surfBins$lonBins)
surfBins$Surface = 'NA'
tmp = surfBins[, c(7, 8)]
rm(surfBins)

cc <- function(name, value) {
    ret <- c(value)
    names(ret) <- name
    ret
}
latlon2type = cc(tmp[, 1], tmp[, 2])
latlon2type[nrainLoc[,1]] = nrainLoc[,2]


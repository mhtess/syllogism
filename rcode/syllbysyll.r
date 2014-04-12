library(reshape2)
require(ggplot2)
require(plyr)

setwd("/Users/mht/Documents/research/models")
phmeta <- read.csv('phmeta.csv')
jlmeta <- read.csv('jlmetac.csv')
phmeta <- phmeta[-1]
jlmeta<-jlmeta[order(jlmeta$syll),]
phmeta<-phmeta[order(phmeta$syll),]
###load pqr models
pqr00 <- read.csv('OPTIM_00/lattice_N0_M0_EP1_alphQ1.0_alphR1.0_n6_base0.05_s100k.csv')
pqr10 <- read.csv('OPTIM_10/lattice_N1_M0_EP1_alphQ3.8_alphR1.0_n5_base0.27_s100k.csv')
pqr01 <- read.csv('OPTIM_01/lattice_N0_M1_EP1_alphQ1.0_alphR3.5_n6_base0.15_s100k.csv')
pqr11 <- read.csv('OPTIM_11/lattice_N1_M1_dgn_EP1_alphQ3.1_alphR3.1_n6_base0.20_s100k.csv')
syllorder <- read.csv('/Users/mht/Documents/research/models/syllorder_churchlattice.csv',header=FALSE)[,1]
#### order pqr models
pqr00 <- pqr00[order(syllorder),]
pqr10 <- pqr10[order(syllorder),]
pqr01 <- pqr01[order(syllorder),]
pqr11 <- pqr11[order(syllorder),]
### correlations
l = 53
b = 56
rng = c(1:20,25:52,57:64)
rng = 1:64
rng = l:b
rng = seq(4,64,4)
cor(melt((phmeta)[rng,2:5])$value,melt(pqr00[rng,1:4]+pqr00[rng,5:8])$value)
cor(melt((phmeta)[rng,2:5])$value,melt(pqr10[rng,1:4]+pqr10[rng,5:8])$value)
cor(melt((phmeta)[rng,2:5])$value,melt(pqr01[rng,1:4]+pqr01[rng,5:8])$value)
cor(melt((phmeta)[rng,2:5])$value,melt(pqr11[rng,1:4]+pqr11[rng,5:8])$value)
###
cor(melt((jlmeta)[l:b,1:9])$value,melt(pqr00[l:b,])$value)
cor(melt((jlmeta)[l:b,1:9])$value,melt(pqr10[l:b,])$value)
cor(melt((jlmeta)[l:b,1:9])$value,melt(pqr01[l:b,])$value)
cor(melt((jlmeta)[l:b,1:9])$value,melt(pqr11[l:b,])$value)

#### modal responses
md = max.col(phmeta[,2:5]) 
m00 = max.col(pqr00[,1:4]+pqr00[,5:8])
m01 = max.col(pqr01[,1:4]+pqr01[,5:8])
m10 = max.col(pqr10[,1:4]+pqr10[,5:8])
m11 = max.col(pqr11[,1:4]+pqr11[,5:8])

### differences
setdiff(phmeta[md==m01,]$syll,phmeta[md==m00,]$syll)

row.names(phmeta) = phmeta$syll
row.names(pqr00) = phmeta$syll
row.names(pqr10) = phmeta$syll
row.names(pqr01) = phmeta$syll
row.names(pqr11) = phmeta$syll

## phmeta data for items captured by 00 not by 11
phmeta[setdiff(phmeta[md==m00,]$syll,phmeta[md==m11,]$syll),]
## phmeta data for items not catpured by either 00 or 11
phmeta[!(md==m11 | md==m00),]


### max difference between 00 and 10
maxdiff10 = apply(abs(100*(pqr10[,1:4]+pqr10[,5:8])-100*(pqr00[,1:4]+pqr00[,5:8])),1,max)

### sum of squared dev between phmeta and 01
dev01<-rowSums((100*(pqr01[,1:4]+pqr01[,5:8])-phmeta[2:5])^2)

### sum of squared dev between phmeta and 10
dev10<-rowSums((100*(pqr10[,1:4]+pqr10[,5:8])-phmeta[2:5])^2)


#################################################################
### pqr00 for which pqr10 makes the best predictions
### and same for phmeta
#################################################################
a <- 100*(pqr00[order(dev10)[1:16],1:4]+pqr00[order(dev10)[1:16],5:8])
b <- phmeta[order(dev10)[1:16],]
c <- 100*(pqr10[order(dev10)[1:16],1:4]+pqr10[order(dev10)[1:16],5:8])
# best fit for 10, in order of worst fit for 00
a0 <- a[order(-rowSums((a-b[2:5])^2)),]
b0 <- b[order(-rowSums((a-b[2:5])^2)),]
c0 <- c[order(-rowSums((a-b[2:5])^2)),]
# ", in order of largest deviation from 00
b[order(-rowSums((a-c)^2)),]$syll
##############################################################################
##############################################################################
#### deviation between 00 and 10
#################################################################
dev00_10 <- rowSums((100*(pqr10[,1:4]+pqr10[,5:8])-100*(pqr00[,1:4]+pqr00[,5:8]))^2)
### pqr00 for which pqr10 makes the best predictions
### and same for phmeta
a <- 100*(pqr00[order(-dev00_10)[1:16],1:4]+pqr00[order(-dev00_10)[1:16],5:8])
b <- phmeta[order(-dev00_10)[1:16],]
c <- 100*(pqr10[order(-dev00_10)[1:16],1:4]+pqr10[order(-dev00_10)[1:16],5:8])
# best fit for 10, in order of worst fit for 00
a0 <- a[order(-rowSums((a-b[2:5])^2)),]
b0 <- b[order(-rowSums((a-b[2:5])^2)),]
c0 <- c[order(-rowSums((a-b[2:5])^2)),]
# ", in order of largest deviation from 00
b[order(-rowSums((a-c)^2)),]$syll



####
pm = setdiff(phmeta[md==m11,]$syll,phmeta[md==m00,]$syll)
rng = pm
cor(melt((phmeta)[rng,2:5])$value,melt(pqr00[rng,1:4]+pqr00[rng,5:8])$value)
cor(melt((phmeta)[rng,2:5])$value,melt(pqr10[rng,1:4]+pqr10[rng,5:8])$value)
cor(melt((phmeta)[rng,2:5])$value,melt(pqr01[rng,1:4]+pqr01[rng,5:8])$value)
cor(melt((phmeta)[rng,2:5])$value,melt(pqr11[rng,1:4]+pqr11[rng,5:8])$value)

i = 21
phmeta[i,]
jlmeta[i,]
100*pqr00[i,]
100*pqr10[i,]
100*pqr01[i,]
100*pqr11[i,]

lit <- pqr00[,1:4]+pqr00[,5:8]
lit <- lit + 0.00001
prior <- c(8,39,11,42)
lit$dev <- rowSums(log(lit*prior))
lit$syll<- syllorder[order(syllorder)]
lit<- lit[order(lit$dev),]

data1[substring(rownames(data1),1,2) == 'AE',]*100
model_c[(substring(rownames(model_c),1,2) == 'AE'),]*100

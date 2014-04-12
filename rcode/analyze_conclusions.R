rawdata = read.csv('syllogism00_conclusions.csv')
rawdata <- rawdata[order(rawdata$syll),1:12]
summary(rawdata$syll)
summary(rawdata$time)
f0<-rawdata[rawdata$time>7,]
summary(f0$syll)

#####
tmp = ddply(f0, .(syll, condition), function(x) {
  ok = x[,c('A','E','I','O')]
  ok[1:4] / rowSums(ok[1:4])
})
tmp$syll = paste(tmp$syll,tmp$condition)


mdd<-melt(tmp[-2],id.vars=c('syll'),na.rm=TRUE)

dfc<-summarySE(melt(tmp,id.vars=c('syll','condition')),measurevar='value',groupvars=c("syll","variable"))
pd <- position_dodge(.5)

ggplot(dfc, aes(x=variable, y=value, colour=syll)) + 
  geom_errorbar(aes(ymin=value-ci, ymax=value+ci), width=.7, position=pd)+
  geom_point(position=pd)




cs <- tmp[,3:6]+tmp[,7:10]
cs$syll <- tmp$syll

phmeta[phmeta$syll%in%cs$syll,]
pqr00$syll<-syllorder[order(syllorder)]
pqr10$syll<-syllorder[order(syllorder)]

# correlation with pqr00 collapsed across 4 quantifiers
cor(melt(cs)$value,melt(pqr00[pqr00$syll%in%cs$syll,1:4]+pqr00[syllorder[order(syllorder)]%in%cs$syll,5:8])$value)
cor(melt(cs)$value,melt(pqr10[pqr10$syll%in%cs$syll,1:4]+pqr10[syllorder[order(syllorder)]%in%cs$syll,5:8])$value)

# correlation with pqr10 with all 8 conclusions
cor(melt(pqr00[pqr00$syll%in%cs$syll,])$value,melt(tmp[3:10])$value)
cor(melt(pqr10[pqr10$syll%in%cs$syll,])$value,melt(tmp[3:10])$value)


### distribution of responses over all syllogisms
(colSums(phmeta[2:5])/sum(colSums(phmeta[2:5])))*100
### 
(colSums(jlmeta[2:9])/sum(colSums(jlmeta[2:9])))*100
###
colMeans(tmp[3:10])*100

priorm <- read.csv('lattice_N0_M0_emprior_n9_s100k.csv')
litm <- read.csv('lattice_N0_M0_ePriors_EP1_alphQ1.0_alphR1.0_n9_s100k.csv')
testcase<-pqr00[pqr00$syll%in%cs$syll,1:8]
testcase<-pqr00[$syll%in%cs$syll,1:8]

cor(melt(tmp[c(1,2,4,5),3:10])$value,melt(priorm[c(1,2,4,5),])$value)

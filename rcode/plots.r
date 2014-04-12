## for bootstrapping 95% confidence intervals
library(bootstrap)
theta <- function(x,xdata,na.rm=T) {mean(xdata[x],na.rm=na.rm)}
ci.low <- function(x,na.rm=T) {
  mean(x,na.rm=na.rm) - quantile(bootstrap(1:length(x),1000,theta,x,na.rm=na.rm)$thetastar,.025,na.rm=na.rm)}
ci.high <- function(x,na.rm=T) {
  quantile(bootstrap(1:length(x),1000,theta,x,na.rm=na.rm)$thetastar,.975,na.rm=na.rm) - mean(x,na.rm=na.rm)}

# plot confidence intervals
agr = aggregate(value ~ variable + syll, data=mdd, FUN=mean)
agr$CILow = aggregate(value ~ variable + syll, data=mdd, FUN=ci.low)$value
agr$CIHigh = aggregate(value ~ variable + syll, data=mdd, FUN=ci.high)$value
agr$YMin = agr$value - agr$CILow
agr$YMax = agr$value + agr$CIHigh

pd <- position_dodge(.5)


ggplot(agr, aes(x=variable,y=value,color=factor(condition),group=factor(condition))) +
  geom_point(position=pd) +
#  geom_line() +
  geom_errorbar(aes(ymin=YMin,ymax=YMax),width=0.25, position=pd) +
  facet_wrap(~syll)

ggplot(agr, aes(x=variable,y=value,color=syll,group=syll)) +
  geom_point(position=pd) +
  #  geom_line() +
  geom_errorbar(aes(ymin=YMin,ymax=YMax),width=0.25, position=pd)

+
  facet_wrap(~condition)


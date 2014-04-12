rawdata = read.csv('/Users/mht/Documents/research/data/00syllogism/syllogism00_conclusions.csv')
### remove EI3 condition 2
rawdata <- rawdata[order(rawdata$syll),1:13]
rawdata <-rawdata[!(rawdata$syll == 'EI3' & rawdata$condition == '2'),]
summary(rawdata$syll)
summary(rawdata$time)
f0<-rawdata[rawdata$time>7,]
summary(f0$syll)
oldmeans = read.csv('/Users/mht/Documents/research/data/00syllogism/syllogism0_means_11.csv')
syllorder = oldmeans$X
pqr10<-read.csv('/Users/mht/Documents/research/data/00syllogism/MODEL_10/lattice_N1_M0_ePriors4_EP1_alphQ2.5_alphR1.0_n6_s100k.csv')
pqr00<-read.csv('/Users/mht/Documents/research/data/00syllogism/MODEL_00/lattice_N0_M0_ePriors4_EP1_alphQ1.0_alphR1.0_n6_s100k.csv')
prior<-read.csv('/Users/mht/Documents/research/data/00syllogism/MODEL_00/lattice_N0_M0_emprior_n6_s100k.csv')

##### DONT EVER RUN THIS CODE AGAIN
# pqr00<-read.csv('/Users/mht/Documents/research/models/OPTIM_00/lattice_N0_M0_EP1_alphQ1.0_alphR1.0_n6_base0.39_s10k.csv')
# pqr00$syll <- syllorder2
# pqr00a<-pqr00[syllorder2%in%substring(syllorder,1,3),]
# pqr00b<-rbind(pqr00a,pqr00a)
# pqr00c<-cbind(pqr00b[1:4]+pqr00b[5:8],pqr00b$syll)
# pqr00d<-pqr00c[c(1:8,10,11,12),]
# names(pqr00d)<-c('A','E','I','O','syll')
# pqr00d$type<-'lbr'
# pqr00d$condition<-c(rep(1,6),rep(2,5))
# ###

pqr00m=pqr00[-10,]
pqr10m=pqr10[-10,]
priorm=prior[-10,1:4]+prior[-10,5:8]
pqr00m$syll<-syllorder
pqr10m$syll<-syllorder
priorm$syll<-syllorder

#pqr00[order(pqr00[-10,]$syll),]

#####
tmp = ddply(f0, .(syll, condition), function(x) {
  means = colMeans(x[,c('A','E','I','O')])
  means[1:4] / sum(means[1:4])
})

nmp = ddply(f0, .(syll, condition), function(x) {
  means = x[,c('A','E','I','O')]
  means[1:4] / rowSums(means[1:4])
})

### 

cor(melt(tmp,id.vars=c('syll','condition'))$value,melt(pqr00m[order(pqr00m$syll),])$value)
cor(melt(tmp,id.vars=c('syll','condition'))$value,melt(pqr10m[order(pqr10m$syll),])$value)
cor(melt(tmp,id.vars=c('syll','condition'))$value,melt(priorm[order(priorm$syll),])$value)
###
names(pqr00m)<- c('A','E','I','O','syll')
pqr00m$condition<-substring(pqr00m$syll,5)
pqr00m$syll<-substring(pqr00m$syll,1,3)
pqr00m$type<-'lbr'
####
### 
names(pqr10m)<- c('A','E','I','O','syll')
pqr10m$condition<-substring(pqr10m$syll,5)
pqr10m$syll<-substring(pqr10m$syll,1,3)
pqr10m$type<-'pbr'
####
names(priorm)<- c('A','E','I','O','syll')
priorm$condition<-substring(priorm$syll,5)
priorm$syll<-substring(priorm$syll,1,3)
priorm$type<-'prior'
####
tmp$type<-'data'
nmp$type<-'data'
cmp<-rbind(pqr10m,pqr00m,priorm,nmp)
mdd<-melt(cmp,id.vars=c('syll','condition','type'),na.rm=TRUE)
mdd$type<-factor(mdd$type,levels=c('data','prior','lbr','pbr')) 

theta <- function(x,xdata,na.rm=T) {mean(xdata[x],na.rm=na.rm)}
ci.low <- function(x,na.rm=T) {
  mean(x,na.rm=na.rm) - quantile(bootstrap(1:length(x),1000,theta,x,na.rm=na.rm)$thetastar,.025,na.rm=na.rm)}
ci.high <- function(x,na.rm=T) {
  quantile(bootstrap(1:length(x),1000,theta,x,na.rm=na.rm)$thetastar,.975,na.rm=na.rm) - mean(x,na.rm=na.rm)}

# plot confidence intervals
agr = aggregate(value ~ variable + syll + condition+type, data=mdd, FUN=mean)
agr$CILow = aggregate(value ~ variable + syll + condition+type, data=mdd, FUN=ci.low)$value
agr$CIHigh = aggregate(value ~ variable + syll + condition+type, data=mdd, FUN=ci.high)$value
agr$YMin = agr$value - agr$CILow
agr$YMax = agr$value + agr$CIHigh

#### LONG'S MAGIC
long<-ddply(agr, .(variable, syll, condition), function(e) { 
  
  human.data = subset(e, type == "data")[,c("value","YMin","YMax")]
  
  transform(subset(e, type != "data"),
            human.value = human.data$value,
            human.YMin = human.data$YMin,
            human.YMax = human.data$YMax)
})

## combine variable, syll, condition into a single factor called
## grouping factor
long = transform(long, grouping.factor = paste(variable, syll, condition, sep = "."))

long$variable<-factor(long$variable, levels=c('A','I','O','E'),labels=c('All','Some','Not all','No'))

ggplot(subset(long,type=='lbr'), aes(x=value,y=human.value,group=grouping.factor,colour=variable)) +
  ylab("Endorsement Probability")+
  xlab("Model Predictions")+
  ggtitle("Data from 6 syllogisms vs. Naive Prior Literal Bayesian")+
  geom_errorbar(aes(ymin=human.YMin,ymax=human.YMax),width=0.005,alpha=0.6)+
  geom_point(aes(color=variable),size =5)+
  geom_abline(intercept = 0, slope = 1, linetype = 3,alpha = 0.4)+
  #  facet_wrap(~type,scales='free')+
  xlim(-0.005,0.75)+
  #coord_equal()+
  ylim(-0.005,0.75)+
  theme_bw()+
#  facet_wrap(~type,scales='free')+
  theme(plot.title=element_text(size=32),
      axis.line = element_line(colour = "black"),
        axis.title.x = element_text(size=26),
        axis.title.y = element_text(size=26),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        #   panel.border = element_blank(),
        panel.background = element_blank(),
        legend.text = element_text(size=20),
        # legend.key = element_rect(size = 4),
        legend.title = element_text(size=20),
        # legend.position = 'bottom',
        strip.text.x = element_text(size=18),#, face="bold"),
        strip.text.y = element_text(size=18),#, face="bold"),
        strip.background = element_rect(colour="white", fill="white"))+
  scale_colour_manual(values = rbspectr,name='Conclusion')


pd <- position_dodge(.5)

agr$type <- factor(agr$type,levels=c('data','10-model','00-model','prior'),labels=c('Data','Listener model','Bayesian model','Prior'))
#agr$type <- 
#agr$var = factor(paste(agr$type,agr$condition),levels=c('Data arbitrary', 'Data meaningful','Prior arbitrary', 'Prior meaningful','Bayesian model arbitrary', 'Bayesian model meaningful', 'Listener model arbitrary', 'Listener model meaningful'))
agr$variable <- factor(agr$variable,levels=c('A','I','O','E'),labels=c('All','Some','Not all','No'))
#agr<-agr[order(agr$type),]
#agr<-within(agr,type<-factor(type,levels = names(sort())))
levels(factor(agr$syll))
ggplot(long, aes(x=value,y=human.value,group=type,fill=type)) +
  geom_bar(position=pd,stat='identity',width=.5) +
 # scale_colour_manual(values=c("#e41a1c", "#377eb8", "#4daf4a","#984ea3","#ff7f00","black"))+
  #  geom_line() +
  geom_errorbar(aes(ymin=YMin,ymax=YMax),width=0.10, position=pd)+
  facet_wrap(~condition)+
  scale_alpha_manual(values=c(1, 0.25,0.5,0.75))+
  ylab("Endorsement Probability")+
  xlab("Conclusion Quantifier")+
  theme_bw()+
  theme(axis.line = element_line(colour = "black"),
        axis.title.x = element_text(size=14),
        axis.title.y = element_text(size=14),
        axis.text.x  = element_text(size=16),
        axis.text.y  = element_text(size=16),
        strip.background = element_blank(),
        legend.text = element_text(size=14),
        legend.title = element_text(size=14),
        panel.grid.major = element_blank(),
    #    panel.grid.minor = element_blank(),
        panel.background = element_blank(),
        panel.border = element_rect(colour="black"),
        strip.background = element_rect(colour="white", fill="white"))


levels(agr$type) <- c('data','pbr','lbr','prior')
h <- dcast(agr, value.var = c('value','CILow','CIHigh','YMin','YMax') , ... ~ type)
h <- dcast(melt(agr), value.var = 'value', ... ~ type )
h<-dcast(agr,syll~type+YMin+YMax,function(x){ x$syll = 1:nrow(x); x})
h <- dcast(mdd,value.var='value',...~type)
h <- dcast(agr[,1:5],value.var='value',...~type)

ggplot(h, aes(x=pbr,y=data)) +
  ylab("Endorsement Probability")+
  xlab("Endorsement Probability (Pragmatic Bayesian Reasoner)")+
  #ggtitle(d_title)+
  geom_point(aes(color=variable),size =4)+
  theme_bw()+
  theme(axis.line = element_line(colour = "black"),
        axis.title.x = element_text(size=22),
        axis.title.y = element_text(size=22),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        #   panel.border = element_blank(),
        panel.background = element_blank(),
        legend.text = element_text(size=14),
        # legend.key = element_rect(size = 4),
        legend.title = element_text(size=16),
        # legend.position = 'bottom',
        strip.text.x = element_text(size=18),#, face="bold"),
        strip.text.y = element_text(size=18),#, face="bold"),
        strip.background = element_rect(colour="white", fill="white"))+
  scale_colour_manual(values = c('#a6611a','#dfc27d','#80cdc1','#018571'))

ggplot(h, aes(x=prior,y=data)) +
  ylab("Endorsement Probability")+
  xlab("Endorsement Probability (Prior)")+
  #ggtitle(d_title)+
  geom_point(aes(color=variable),size =4)+
  theme_bw()+
  theme(axis.line = element_line(colour = "black"),
        axis.title.x = element_text(size=22),
        axis.title.y = element_text(size=22),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        #   panel.border = element_blank(),
        panel.background = element_blank(),
        legend.text = element_text(size=14),
        # legend.key = element_rect(size = 4),
        legend.title = element_text(size=16),
        # legend.position = 'bottom',
        strip.text.x = element_text(size=18),#, face="bold"),
        strip.text.y = element_text(size=18),#, face="bold"),
        strip.background = element_rect(colour="white", fill="white"))+
  scale_colour_manual(values = c('#a6611a','#dfc27d','#80cdc1','#018571'))


### RIPS 1994

r0<-read.csv('/Users/mht/Documents/research/models/rips/model_00/lattice_N0_M0_EP1_alphQ1.0_alphR1.0_n6_base0.35_s100k.csv',col.names=c('A','E','I','O'))
r0$syll <- read.csv('/Users/mht/Documents/research/models/rips/ripsmodel_syllorder.csv',header=T)[,1]
r0$src <- 'lbr'

r1<-read.csv('/Users/mht/Documents/research/models/rips/model_10/lattice_N1_M0_EP1_alphQ2.2_alphR1.0_n6_base0.35_s100k.csv',col.names=c('A','E','I','O'))
#r1<-read.csv('/Users/mht/Documents/research/models/rips/model_10/lattice_N1_M0_EP1_alphQ2.5_alphR1.0_n7_base0.35_s100k.csv',col.names=c('A','E','I','O'))
r1$syll <- read.csv('/Users/mht/Documents/research/models/rips/ripsmodel_syllorder.csv',header=T)[,1]
r1$src <- 'pbr'

rips<-read.csv('/Users/mht/Documents/research/models/rips/rips-data.csv',header=F,col.names=c('syll','A','E','I','O'))
nrips <- rips[2:5]/rowSums(rips[2:5])
nrips$syll <- rips$syll
nrips$src <- 'data'
#cor(melt(r0[order(r0$syll),])$value,melt(nrips)$value)


df<-rbind(nrips,r0,r1)
dfm <- melt(df)
h <- dcast(dfm, value.var = 'value', ... ~ src)
names(h)[2] <- "Conclusion"
h$Conclusion <- factor(h$Conclusion, levels =c('A','I','O','E') ,labels=c("All",'Some','Not all',"No"))


####
rbspectr <- c('#ca0020','#f4a582','#92c5de','#0571b0')
med <- summary(endrips$endorsement)[3]

######## OVERALL endorsement
endrips <- data.frame(endorsement = rowSums(rips[2:5]), syll = rips$syll)
endrips$syll <- rips$syll
endrips$topmed<-endrips$syll %in% endrips[endrips$endorsement > med,]$syll
endrips$Median<-factor(endrips$topmed, levels = c('TRUE','FALSE'), labels = c("Top","Bottom"))

### QUARTILES
endrips$quartile <- with(endrips, cut(endorsement, 
                                      breaks=quantile(endorsement, probs=seq(0,1, by=0.25)), 
                                      include.lowest=TRUE))
endrips$quartile<-factor(as.numeric(endrips$quartile),levels=c('4','3','2','1'))
h<-merge(h,endrips[,c(2,5)],by="syll")





######## Megabarplot
mega <- melt(rips,id.vars='syll')
####Logical reasoners data
v0<-read.csv('/Users/mht/Documents/research/models/allvalid.txt')
v0$cncl = substring(v0$syll,3,3)
v0$syll = paste(substring(v0$syll,1,2),substring(v0$syll,4),sep='')
v1 = data.frame(syll=mega$syll, cncl=mega$variable)
v2<-merge(v0,v1)
nv1 = data.frame(syll=v1[!(v1$syll%in%v0$syll),]$syll,cncl=v1[!(v1$syll%in%v0$syll),]$cncl,value=0)
v3<-rbind(v2,nv1)
v3$cncl <- factor(v3$cncl, levels = c('A','I','O','E'), labels = c('All','Some','Not all','No'))

####

mega$variable <- factor(mega$variable, levels = c('A','I','O','E'), labels = c('All','Some','Not all','No'))

ggplot(mega, aes(x=syll, y=value,fill=variable)) +   
  geom_bar(position="dodge",stat='identity')+
  xlab("Syllogism")+
  ylab("% (of Subjects) Endorsement")+
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
  scale_fill_manual(name="Conclusion", values=rbspectr)
##################
##LOGICAL REASONER
ggplot(v3, aes(x=syll, y=value,fill=cncl)) +   
  geom_bar(position="dodge",stat='identity')+
  xlab("Syllogism")+
  ylab("% Endorsement")+
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
  scale_fill_manual(name="Conclusion", values=rbspectr)
##################


qual4deep<-c('#e41a1c','#377eb8','#4daf4a','#984ea3')

ggplot(endrips, aes(x=syll, y=endorsement))+#, fill=quartile)) +   
  geom_bar(position="dodge",stat='identity')+
  scale_fill_manual(values = qual4deep,name='Quartile')+
  xlab("Syllogism")+
  ylab("% Total Endorsement")+
  theme(axis.line = element_line(colour = "black"),
        axis.title.x = element_text(size=24),
        axis.title.y = element_text(size=24),
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
        strip.background = element_rect(colour="white", fill="white"))
##################

####### FULL LBR/PBR SCATTERPLOT
ggplot(h, aes(x=pbr,y=data)) +
  ylab("Endorsement Probability (Rips 1994)")+
  xlab("Endorsement Probability (Pragmatic Bayesian Reasoner)")+
  #ggtitle(d_title)+
  geom_point(aes(color=Conclusion),size =5)+
  theme_bw()+
  xlim(0,1)+
  ylim(0,1)+
  geom_abline(intercept = 0, slope = 1, linetype = 4,alpha = 0.8)+
  theme(axis.line = element_line(colour = "black"),
        axis.title.x = element_text(size=30),
        axis.title.y = element_text(size=30),
        axis.text.x  = element_text(size=30),
        axis.text.y  = element_text(size=30),
        strip.background = element_blank(),
        legend.text = element_text(size=26),
        legend.title = element_text(size=26),
        panel.grid.major = element_blank(),
        #   panel.border = element_blank(),
        panel.background = element_blank(),
        # legend.key = element_rect(size = 4),
        legend.title = element_text(size=26),
        strip.text.x = element_text(size=24),#, face="bold"),
        strip.text.y = element_text(size=24),#, face="bold"),
        strip.background = element_rect(colour="white", fill="white"))+
scale_colour_manual(values = rbspectr)
 ########################                   

## PBR SCATTER by QUARTILE
###
h$quartile<-factor(h$quartile,  levels = c('3','4','2','1'), labels =c("Quartile 3","Top Quartile","Quartile 2","Bottom Quartile"))


ggplot(h, aes(x=pbr,y=data)) +
  ylab("Endorsement Probability (Rips 1994)")+
  xlab("Endorsement Probability (Pragmatic Bayesian Reasoner)")+
  #ggtitle(d_title)+
  geom_point(aes(color=Conclusion),size =4)+
  theme_bw()+
  xlim(0,1)+
  ylim(0,1)+
  coord_fixed()+
  facet_wrap(~quartile,scales = "fixed")+
  geom_abline(intercept = 0, slope = 1, linetype = 3,alpha = 0.4)+
  ggtitle("Data vs. Model by Quartile of Total Endorsement")+
  theme(plot.title = element_text(size=32),
        axis.line = element_line(colour = "black"),
        axis.title.x = element_text(size=30),
        axis.title.y = element_text(size=30),
        axis.text = element_text(size=20),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        #   panel.border = element_blank(),
        panel.background = element_blank(),
        legend.text = element_text(size=26),
        # legend.key = element_rect(size = 4),
        legend.title = element_text(size=26),
        # legend.position = 'bottom',
        strip.text.x = element_text(size=24),#, face="bold"),
        strip.text.y = element_text(size=24),#, face="bold"),
        strip.background = element_rect(colour="white", fill="white"))+
  scale_colour_manual(values = rbspectr)


###### bar plots
d2m<-c('#8856a7','#99d8c9','#2ca25f')

pd <- position_dodge(.8)
mh<-melt(h[h$syll=='EA1',])
mh$variable <- factor(mh$variable, levels=c('data','lbr','pbr'),labels=c('Rips (1994) Data','Literal Bayesian','Pragmatic Bayesian'))
ggplot(mh, aes(x=Conclusion,y=value,fill=variable)) +
  geom_bar(position="dodge",stat='identity',width=.8) +
 scale_fill_manual(values=d2m,name='Source')+
  #  geom_line() +
 # geom_errorbar(aes(ymin=YMin,ymax=YMax),width=0.10, position=pd)+
#  facet_wrap(~condition)+
  scale_alpha_manual(values=c(1,0.5,0.75))+
  ylab("Endorsement Probability")+
  xlab("Conclusion Quantifier")+
 theme_bw()+
  theme(axis.line = element_line(colour = "black"),
        axis.title.x = element_text(size=30),
        axis.title.y = element_text(size=30),
        axis.text.x  = element_text(size=30),
        axis.text.y  = element_text(size=30),
        strip.background = element_blank(),
        legend.text = element_text(size=26),
        legend.title = element_text(size=26),
       # panel.grid.major = element_blank(),
        #    panel.grid.minor = element_blank(),
        panel.background = element_blank(),
        panel.border = element_rect(colour="black"),
        strip.background = element_rect(colour="white", fill="white"))




+
  facet_wrap(~ variable,scales = 'free')+#,labeller=mf_labeller)+
  scale_shape_manual(values=c(3,15),name='',breaks=c("TRUE","FALSE"),labels=c("Valid","Invalid"))+
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
        legend.position = 'bottom',
        strip.text.x = element_text(size=18),#, face="bold"),
        strip.text.y = element_text(size=18),#, face="bold"),
        
        strip.background = element_rect(colour="white", fill="white"))#+
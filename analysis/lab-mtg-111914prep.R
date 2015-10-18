library(reshape2)
library(ggplot2)
library(plyr)
library(R2jags)
library(gridExtra)
library(bootstrap)

theta <- function(x,xdata,na.rm=T) {mean(xdata[x],na.rm=na.rm)}
ci.low <- function(x,na.rm=T) {
  mean(x,na.rm=na.rm) - quantile(bootstrap(1:length(x),1000,theta,x,na.rm=na.rm)$thetastar,.025,na.rm=na.rm)}
ci.high <- function(x,na.rm=T) {
  quantile(bootstrap(1:length(x),1000,theta,x,na.rm=na.rm)$thetastar,.975,na.rm=na.rm) - mean(x,na.rm=na.rm)}

agr.ci.collapsed <- function(x){
  agr = aggregate(value ~ domain + syll + variable + experiment, data=x, FUN=mean)
  agr$CILow = aggregate(value ~ domain + syll + variable + experiment, data=x, FUN=ci.low)$value
  agr$CIHigh = aggregate(value ~ domain + syll + variable + experiment, data=x, FUN=ci.high)$value
  agr$YMin = agr$value - agr$CILow
  agr$YMax = agr$value + agr$CIHigh
  return(agr)
}

setwd("~/Documents/research/syllogism/presentations/labmtg-111914")
map_radio_to_continuous <- function(rad,cts){50+(2*rad-1)*(cts/2)}


exp_domains = c('_ crackers that have lots of flavor are soggy',
                '_ knives that cut well are sharp',
                '_ lightbulbs that are hot are on',
                '_ strawberries that are warm are in the freezer')
resp_labels<-c("Q_A","Q_E","Q_I","Q_O")
conclusion_labels<- c('all','none','some','some...not')
domains<- c('cracker', 'knife', 'lightbulb', 'strawberry')


# Load data from 2 experiments
fpath = '/Users/mht/Documents/research/syllogism/data/03syllogism_reasoning/'
fpath2 = '/Users/mht/Documents/research/syllogism/data/04syllogism_reasoning/'

df<-read.csv((paste(fpath,'syllbelief-exp-mturk_all_n250.csv',sep="")))
df$experiment <- factor(1)

df2<-read.csv((paste(fpath2,'syllbelief-exp2-mturk.csv',sep="")))
df2$condition<-paste(df2$condition,'2',sep='.')
df2$experiment <- factor(2)

exp1sylls<-levels(df$syll)
exp2sylls<-levels(df2$syll)


# remove extreme RTs
df<-subset(df,rt<mean(df$rt)+2*sqrt(var(df$rt)))
df2<-subset(df2,rt<mean(df2$rt)+2*sqrt(var(df2$rt)))
# ddply(df,.(domain,experiment,syll), summarise, mean(rt))
# ddply(df2,.(domain,experiment,syll),  
#       function(x){sum(x[,c("Q_A","Q_E","Q_I","Q_O")])})






df2$subj<- factor(df2$subj, labels=as.integer(substring(levels(df2$subj),2,4))+length(levels(df$subj)))

df.c <- rbind(df,df2)
df.c$condition<-factor(df.c$condition,levels=c('slide','radio','radio.2'))

# map radio + slider to just radio
for (i in 1:length(df.c$subj)){
  if (substring(df.c[i,]$condition,1,5)=='radio'){
    df.c[i,]$Q_A <- map_radio_to_continuous(df.c[i,]$radio_A,df.c[i,]$Q_A)
    df.c[i,]$Q_E <- map_radio_to_continuous(df.c[i,]$radio_E,df.c[i,]$Q_E)
    df.c[i,]$Q_I <- map_radio_to_continuous(df.c[i,]$radio_I,df.c[i,]$Q_I)
    df.c[i,]$Q_O <- map_radio_to_continuous(df.c[i,]$radio_O,df.c[i,]$Q_O)
  }
}

df.norm = ddply(df.c, .(domain,condition,syll,experiment), 
                function(x) {resp = x[,resp_labels]
                             resp / rowSums(resp)})

EP = 1

# plot experiment 1 data

collapsed.bs1 <- subset(agr.ci.collapsed(melt(df.norm)),experiment==1)
collapsed.bs1$conclusion = factor(collapsed.bs1$variable, labels=c('all','none','some','some...not'))
collapsed.bs1$domain = factor(collapsed.bs1$domain, labels=exp_domains)

collapsed.bs1$syll<-factor(collapsed.bs1$syll, 
                          labels = c("Some of the As are not Bs\n All of the Cs are Bs",
                                     "All of the Bs are As\n None of Bs are Cs",
                                     "None of the As are Bs\n Some of the Bs are Cs",
                                     "All of the As are Bs\n Some of the Bs are not Cs"))

a<-ggplot(collapsed.bs1,  aes(x=conclusion, y=value, fill=conclusion)) + 
  geom_bar(position=position_dodge(.6), 
           width = .6,
           stat='identity')+
  geom_errorbar(aes(ymin=YMin,ymax=YMax),
                width=0.3,
                position=position_dodge(.6),
                colour='white')+
  xlab("\nconclusion")+
  ylab('proportion endorsement\n')+
  facet_grid(domain~syll)+
  theme_blackDisplay()+
  guides(fill=F)+
  theme(
    axis.text.x=element_text(angle=90,hjust=1,vjust=.5,colour='gray50'),
    strip.text.x = element_text(size=30),
    strip.text.y = element_text(angle=0, size=30)
    )+
  coord_cartesian(ylim=c(0, 0.7)) + 
  scale_y_continuous(breaks=c(0.25,0.5))

ggsave(filename = 'exp1data_collapsed.png',a, width=32, height=16)

# plot experiment 2 data

collapsed.bs2 <- subset(agr.ci.collapsed(melt(df.norm)),experiment==2)
collapsed.bs2$conclusion = factor(collapsed.bs2$variable, labels=c('all','none','some','some...not'))
collapsed.bs2$domain = factor(collapsed.bs2$domain, labels=exp_domains)

collapsed.bs2$syll<-factor(collapsed.bs2$syll, 
                          labels = c("All of the As are Bs\n All of the Bs are Cs",
                                     "Some of the As are Bs\n All of the Bs are Cs",
                                     "All of the As are Bs\n None of the Bs are Cs",
                                     "Some of the As are Bs\n None of the Bs are Cs"
                                     ))

b<-ggplot(collapsed.bs2,  aes(x=conclusion, y=value, fill=conclusion)) + 
  geom_bar(position=position_dodge(.6), 
           width = .6,
           stat='identity')+
  geom_errorbar(aes(ymin=YMin,ymax=YMax),
                width=0.3,
                position=position_dodge(.6),
                colour='white')+
  xlab("\nconclusion")+
  ylab('proportion endorsement\n')+
  facet_grid(domain~syll)+
  theme_blackDisplay()+
  guides(fill=F)+
  theme(
    axis.text.x=element_text(angle=90,hjust=1,vjust=.5,colour='gray50'),
    strip.text.x = element_text(size=30),
    strip.text.y = element_text(angle=0, size=30)
  )+
  coord_cartesian(ylim=c(0, 0.7)) + 
  scale_y_continuous(breaks=c(0.25,0.5))

ggsave(filename = 'exp2data.png',b, width=32, height=16)

### Models

# I will begin by exploring literal models with different existential presuppositions

# I have simulated results for 3 different presuppositions. What I'm calling: plentify, aristotle, and determiner
# For each, they are run with empirical priors, using the collapsed means (both frequency and plausibility)
# Each is run with various n_object parameter settings





collapsed.bs <- agr.ci.collapsed(melt(df.norm))
collapsed.bs$conclusion <- factor(collapsed.bs$variable, labels=conclusion_labels)
collapsed.bs$domain <- factor(collapsed.bs$domain, labels=domains)

## Literal models

# Load model predictions, for different parameter (n_object) values
model.dir<-'/Users/mht/Documents/research/syllogism/models/modeldata/LATTICE_4_tfbt/'
syllogisms = c('AO2', 'EA3', 'IE1', 'OA1','AA1','AI1','EA1','EI1')
corrs = c()
if (exists('models')){remove(models)}
EP = 1
total_objs = seq(3,11,1)
for (n_obj in total_objs){
  model.domains = data.frame()
  for (d in domains){
    model.all<-read.csv(paste(model.dir,'/00/csv/lis_N0_M0_tfbt',
                              d,'_qud1figFull_AIEOc4CAEP',EP,'_n',n_obj,
                              '_base0.00_s100k_alphQ1_alphR1_bsmean.csv',sep=''))[c(1,6:9)]
    model.sub<-model.all[model.all$X..syll%in%syllogisms,]
    model.sub$domain <- d
    model.m<-melt(model.sub,
                  id.vars=c('X..syll','domain'))
    model.domains<-rbind(model.domains, model.m)
  }
  #rename for merging
  names(model.domains)<-c('syll','domain','conclusion',paste('n',n_obj,sep=''))
  if (exists('models')){
    models = merge(models,model.domains)
  } else {
    models = model.domains
  }
}


models$syll <- factor(models$syll)
models$domain <- factor(models$domain)
models$conclusion <- factor(models$conclusion, labels = conclusion_labels)
m.models<-melt(models, id.vars=c('syll','domain','conclusion'))

all.stuff<-merge(m.models,
                 collapsed.bs[c('domain','syll','value','conclusion')], 
                 by=c('syll','domain','conclusion'))

model.fits<-ddply(all.stuff, .(variable), summarise, cor(value.x, value.y))

names(model.fits)<-c('n','correlation')
model.fits$n<-as.integer(substring(model.fits$n,2,3))
max.loc<-which.max(model.fits$correlation)


plot1<-ggplot(model.fits, aes(x=n,y=correlation))+
  geom_bar(stat='identity',
           fill='white')+
  geom_text(aes(x=n,y=0.7, label=round(correlation,2)),size=10,colour='black')+
  theme_blackDisplay()+
  scale_x_continuous(breaks=seq(3,11,1))+
  coord_cartesian(ylim=c(0,1)) + 
  scale_y_continuous(breaks=c(0,1))+
  xlab('\n n_objects')+
  ylab('correlation\n')

ggsave(filename = paste('literalEP',EP,'_corrbars_bothExp.png',sep=''),plot1, width=16, height=12)



#models$syll <- factor(models$syll, labels = sylllabels)
models$syllogism <- factor(models$syll, levels = c('AO2', 'EA3', 'IE1', 'OA1','AA1','AI1','EA1','EI1'),
                           labels=c("Some of the As are not Bs\n All of the Cs are Bs",
                                    "All of the Bs are As\n None of Bs are Cs",
                                    "None of the As are Bs\n Some of the Bs are Cs",
                                    "All of the As are Bs\n Some of the Bs are not Cs",
                                    "All of the As are Bs\n All of the Bs are Cs",
                                    "Some of the As are Bs\n All of the Bs are Cs",
                                    "All of the As are Bs\n None of the Bs are Cs",
                                    "Some of the As are Bs\n None of the Bs are Cs"
                           ))
                                    
models$domain <- factor(models$domain, labels = exp_domains)
models$conclusion<-factor(models$conclusion, labels = c('all','none','some','some...not'))

# Faceted grids of model predictions (Syll X Domain)

plot2<-ggplot(subset(models,syll%in%c('AO2', 'EA3', 'IE1', 'OA1')),
              aes(x=conclusion,y=n7,fill=conclusion))+
  geom_bar(position=position_dodge(.6), 
               width = .6,
              stat='identity')+
  facet_grid(domain~syllogism)+
  theme_blackDisplay()+
  guides(fill=F)+
  theme(
    axis.text.x=element_text(angle=90,hjust=1,vjust=.5,colour='gray50'),
    strip.text.x = element_text(size=30),
    strip.text.y = element_text(angle=0, size=30)
  )+
  coord_cartesian(ylim=c(0, 0.7)) + 
  scale_y_continuous(breaks=c(0.25,0.5))+
  xlab("\nconclusion")+
  ylab('posterior probability\n')

ggsave(filename = paste('literal_EP',EP,'_n7_exp1.png',sep=''),plot2, width=32, height=16)


plot3<-ggplot(subset(models,syll%in%c('AA1','AI1','EA1','EI1')),
              aes(x=conclusion,y=n7,fill=conclusion))+
  geom_bar(position=position_dodge(.6), 
           width = .6,
           stat='identity')+
  facet_grid(domain~syllogism)+
  theme_blackDisplay()+
  guides(fill=F)+
  theme(
    axis.text.x=element_text(angle=90,hjust=1,vjust=.5,colour='gray50'),
    strip.text.x = element_text(size=30),
    strip.text.y = element_text(angle=0, size=30)
  )+
  coord_cartesian(ylim=c(0, 0.7)) + 
  scale_y_continuous(breaks=c(0.25,0.5))+
  xlab("\nconclusion")+
  ylab('posterior probability\n')

ggsave(filename = paste('literal_EP',EP,'_n7_exp2.png',sep=''),plot3, width=32, height=16)


# Scatterplots, faceted by Experiment
maxcorr.stuff<-subset(all.stuff,variable=='n7')
maxcorr.stuff$experiment<-maxcorr.stuff$syll%in%c('AA1','AI1','EA1','EI1')
maxcorr.stuff$experiment<-factor(maxcorr.stuff$experiment,labels=c('experiment 1','experiment 2'))
corrs <- data.frame(correlations=c(with(subset(maxcorr.stuff,experiment=='experiment 1'), cor(value.x,value.y)),
           with(subset(maxcorr.stuff,experiment=='experiment 2'), cor(value.x,value.y))
           ))
corrs$xpos<- 0.1
corrs$ypos<- 0.55
corrs$experiment <- c('experiment 1','experiment 2')


plot4<-ggplot(maxcorr.stuff,aes(x=value.x,y=value.y,colour=conclusion))+
  geom_point(size=4)+
  geom_text(data=corrs,aes(x=xpos,y=ypos, label=paste('r =',round(correlations,2))),size=10,colour='white')+
  geom_abline(intercept=0,slope=1,colour='grey50')+
  facet_wrap(~experiment)+
  theme_blackDisplay()+
  coord_fixed(ratio=1,xlim = c(-0.02,0.7), ylim = c(-0.02,0.7))+
  scale_y_continuous(breaks=c(0.25,0.5))+
  scale_x_continuous(breaks=c(0.25,0.5))+
  xlab('\n model posterior')+
  ylab('human endorsement\n')+
  #scale_colour_di(guide = guide_legend()) +
  theme(legend.position="bottom",
        legend.direction='horizontal',
        legend.title=element_blank())

ggsave(filename =paste('literal_EP',EP,'_n7_scatter.png',sep=''), plot4, height=14, width=14)


### Pragmatics models

# Load model predictions, for different parameter (n_object, alpha) values
model.dir<-'/Users/mht/Documents/research/syllogism/models/modeldata/LATTICE_4_tfbt/'
syllogisms = c('AO2', 'EA3', 'IE1', 'OA1','AA1','AI1','EA1','EI1')
if (exists('models')){remove(models)}
EP = 1
alt = 0
total_objs = seq(3,10,1)
total_objs = c(7)
total_alphas = seq(1,6,1)
for (n_obj in total_objs){
  model.domains = data.frame()
  for (alpha in total_alphas){
  for (d in domains){
    model.all<-read.csv(paste(model.dir,'10/csv/lis_N1_M0_tfbt',
                              d,'_qud1figFull_AIEOc4CAEP',EP,'Alt',alt,'_n',n_obj,
                              '_base0.00_s100k_alphQ',alpha,'_alphR1_bsmean.csv',sep=''))[c(1,6:9)]
#      model.all<-read.csv(paste(model.dir,'10/csv/lis_N1_M0_tfbt',
#                               d,'_qud1figFull_AIEOc4CAEP',EP,'_n',n_obj,
#                               '_base0.00_s100k_alphQ',alpha,'_alphR1_bsmean.csv',sep=''))[c(1,6:9)]
    model.sub<-model.all[model.all$X..syll%in%syllogisms,]
    model.sub$domain <- d
    model.sub$alpha <- alpha
    model.m<-melt(model.sub,
                  id.vars=c('X..syll','domain','alpha'))
    model.domains<-rbind(model.domains, model.m)
  }
}
  #rename for merging
  names(model.domains)<-c('syll','domain','alpha','conclusion',paste('n',n_obj,sep=''))
  if (exists('models')){
    models = merge(models,model.domains)
  } else {
    models = model.domains
}
}

models$syll <- factor(models$syll)
models$domain <- factor(models$domain)
models$conclusion <- factor(models$conclusion, labels = conclusion_labels)
models$alpha <- factor(models$alpha)

m.models<-melt(models, id.vars=c('syll','domain','conclusion','alpha'))

all.stuff<-merge(m.models,
                 collapsed.bs[c('domain','syll','value','conclusion')], 
                 by=c('syll','domain','conclusion'))

model.fits<-ddply(all.stuff, .(variable,alpha), summarise, cor(value.x, value.y))

names(model.fits)<-c('n','alpha','correlation')

model.fits$n<-as.integer(substring(model.fits$n,2,3))

max.loc<-which.max(model.fits$correlation)

plot5<-ggplot(model.fits, aes(x=n,y=alpha))+
  geom_tile(aes(fill = correlation), colour = "white") + 
  geom_tile(data=model.fits[max.loc,], aes(x=n,y=alpha, fill=correlation),
            size=3,colour='black')+
  geom_text(data=model.fits[max.loc,], aes(x=n,y=alpha, label=round(correlation,2)),
            size=10,colour='black')+
  scale_fill_gradient(low = "white", high = "steelblue",limits=c(0.5,0.85),
                      breaks=c(0.5,0.8))+
  theme_blackDisplay()+
  scale_x_continuous(breaks=seq(3,11,2))+
  xlab("\n n")+
  ylab("alpha\n")

ggsave(filename = paste('pragmaticEP',EP,'Alt',alt,'_corrTiles_ExpBoth.png',sep=''),plot5, width=16, height=12)







#models$syll <- factor(models$syll, labels = sylllabels)
models$syllogism <- factor(models$syll, levels = c('AO2', 'EA3', 'IE1', 'OA1','AA1','AI1','EA1','EI1'),
                           labels=c("Some of the As are not Bs\n All of the Cs are Bs",
                                    "All of the Bs are As\n None of Bs are Cs",
                                    "None of the As are Bs\n Some of the Bs are Cs",
                                    "All of the As are Bs\n Some of the Bs are not Cs",
                                    "All of the As are Bs\n All of the Bs are Cs",
                                    "Some of the As are Bs\n All of the Bs are Cs",
                                    "All of the As are Bs\n None of the Bs are Cs",
                                    "Some of the As are Bs\n None of the Bs are Cs"
                           ))

models$domain <- factor(models$domain, labels = exp_domains)
models$conclusion<-factor(models$conclusion, labels = c('all','none','some','some...not'))

# Faceted grids of model predictions (Syll X Domain)

plot2<-ggplot(subset(models,syll%in%c('AO2', 'EA3', 'IE1', 'OA1') & alpha==2),
              aes(x=conclusion,y=n7,fill=conclusion))+
  geom_bar(position=position_dodge(.6), 
           width = .6,
           stat='identity')+
  facet_grid(domain~syllogism)+
  theme_blackDisplay()+
  guides(fill=F)+
  theme(
    axis.text.x=element_text(angle=90,hjust=1,vjust=.5,colour='gray50'),
    strip.text.x = element_text(size=30),
    strip.text.y = element_text(angle=0, size=30)
  )+
  coord_cartesian(ylim=c(0, 0.7)) + 
  scale_y_continuous(breaks=c(0.25,0.5))+
  xlab("\nconclusion")+
  ylab('posterior probability\n')

ggsave(filename = paste('pragmatics_EP',EP,'alt',alt,'_n5alpha2_exp1.png',sep=''),plot2, width=32, height=16)


plot3<-ggplot(subset(models,syll%in%c('AA1','AI1','EA1','EI1') & alpha==4),
              aes(x=conclusion,y=n7,fill=conclusion))+
  geom_bar(position=position_dodge(.6), 
           width = .6,
           stat='identity')+
  facet_grid(domain~syllogism)+
  theme_blackDisplay()+
  guides(fill=F)+
  theme(
    axis.text.x=element_text(angle=90,hjust=1,vjust=.5,colour='gray50'),
    strip.text.x = element_text(size=30),
    strip.text.y = element_text(angle=0, size=30)
  )+
  coord_cartesian(ylim=c(0, 0.7)) + 
  scale_y_continuous(breaks=c(0.25,0.5))+
  xlab("\nconclusion")+
  ylab('posterior probability\n')

ggsave(filename = paste('pragmatics_EP',EP,'alt',alt,'_n7alpha2_exp2.png',sep=''),plot3, width=32, height=16)


# Scatterplots, faceted by Experiment
maxcorr.stuff<-subset(all.stuff,variable=='n3' & alpha==1)
maxcorr.stuff$experiment<-maxcorr.stuff$syll%in%c('AA1','AI1','EA1','EI1')
maxcorr.stuff$experiment<-factor(maxcorr.stuff$experiment,labels=c('experiment 1','experiment 2'))
corrs <- data.frame(correlations=c(with(subset(maxcorr.stuff,experiment=='experiment 1'), cor(value.x,value.y)),
                                   with(subset(maxcorr.stuff,experiment=='experiment 2'), cor(value.x,value.y))
))
corrs$xpos<- 0.1
corrs$ypos<- 0.55
corrs$experiment <- c('experiment 1','experiment 2')


plot4<-ggplot(maxcorr.stuff,aes(x=value.x,y=value.y,colour=conclusion))+
  geom_point(size=4)+
  geom_text(data=corrs,aes(x=xpos,y=ypos, label=paste('r =',round(correlations,2))),size=10,colour='white')+
  geom_abline(intercept=0,slope=1,colour='grey50')+
  facet_wrap(~experiment)+
  theme_blackDisplay()+
  coord_fixed(ratio=1,xlim = c(-0.02,0.7), ylim = c(-0.02,0.7))+
  scale_y_continuous(breaks=c(0.25,0.5))+
  scale_x_continuous(breaks=c(0.25,0.5))+
  xlab('\n model posterior')+
  ylab('human endorsement\n')+
  #scale_colour_di(guide = guide_legend()) +
  theme(legend.position="bottom",
        legend.direction='horizontal',
        legend.title=element_blank())

ggsave(filename =paste('pragmatics_EP',EP,'alt',alt,'_n3alpha1_scatter.png',sep=''), plot4, height=14, width=14)


### Pragmatics models with mad-world RV

model.dir<-'/Users/mht/Documents/research/syllogism/models/modeldata/LATTICE_4_tfbt/'
syllogisms = c('AO2', 'EA3', 'IE1', 'OA1','AA1','AI1','EA1','EI1')
EP = 1
alt = 1
MW = 1
total_objs = seq(3,10,1)
#total_objs = c(7)
total_alphas = seq(1,9,1)
if (exists('models')){remove(models)}

for (n_obj in total_objs){
  #print(n_obj)
  model.domains = data.frame()
  for (alpha in total_alphas){
    #print(alpha)
    for (d in domains){
      #print(d)
      file.pattern <-paste(model.dir,'10/csv/lis_N1_M0_tfbt',
                            d,'_qud1MW',MW,'figFull_AIEOc4CAEP',EP,'Alt',alt,'_n',n_obj,
                            '_base*_s100k_alphQ',alpha,'_alphR1_bsmean.csv',sep='')
      all.files<- Sys.glob(file.pattern)
      for (fl in all.files){
        model.all<-read.csv(fl)[c(1,6:9)]
        model.sub<-model.all[model.all$X..syll%in%syllogisms,]
        model.sub$base<-as.numeric(strsplit(strsplit(fl,'base')[[1]][2],'_s')[[1]][1])
        model.sub$domain <- factor(d)
        model.sub$alpha <- alpha
        model.m<-melt(model.sub,
                    id.vars=c('X..syll','domain','alpha','base'))
        model.domains<-rbind(model.domains, model.m)
      }
    }
  }
  #rename for merging
  names(model.domains)<-c('syll','domain','alpha','base','conclusion',paste('n',n_obj,sep=''))
  if (exists('models')){
    models = merge(models,model.domains,all=TRUE)
  } else {
    models = model.domains
  }
}

models$syll <- factor(models$syll)
models$domain <- factor(models$domain)
models$conclusion <- factor(models$conclusion, labels = conclusion_labels)
models$alpha <- factor(models$alpha)
models$base<-factor(models$base)
m.models<-melt(models, id.vars=c('syll','domain','conclusion','alpha','base'))

all.stuff<-merge(m.models,
                 collapsed.bs[c('domain','syll','value','conclusion')], 
                 by=c('syll','domain','conclusion'))

model.fits<-ddply(all.stuff, .(variable,base,alpha), summarise, cor(value.x, value.y))

names(model.fits)<-c('n','base','alpha','correlation')

model.fits$n<-as.integer(substring(model.fits$n,2,3))

max.loc<-which.max(model.fits$correlation)

plot5<-
  ggplot(model.fits, aes(x=base,y=alpha))+
  geom_tile(aes(fill = correlation), colour = "white") + 
  geom_tile(data=model.fits[max.loc,], aes(x=base,y=alpha, fill=correlation),
            size=1,colour='black')+
  geom_text(data=model.fits[max.loc,], aes(x=base,y=alpha, label=round(correlation,2)),
            size=4,colour='black')+
  scale_fill_gradient(low = "red", high = "yellow")+
#  theme_blackDisplay()+
  #scale_x_continuous(breaks=seq(3,11,2))+
  theme_solarized()+
  facet_wrap(~n)+
  xlab("\n base")+
  ylab("alpha\n")

#ggsave(filename = paste('pragmaticEP',EP,'Alt',alt,'_corrTiles_ExpBoth.png',sep=''),plot5, width=16, height=12)

max.n <-paste('n',model.fits[max.loc,]$n,sep='')
max.alpha<-model.fits[max.loc,]$alpha 
max.base<-model.fits[max.loc,]$base

maxcorr.stuff<-subset(all.stuff,variable==max.n&
                        alpha==max.alpha&
                        base==max.base)
maxcorr.stuff$experiment<-maxcorr.stuff$syll%in%c('AA1','AI1','EA1','EI1')
maxcorr.stuff$experiment<-factor(maxcorr.stuff$experiment,labels=c('experiment 1','experiment 2'))
corrs <- data.frame(correlations=c(with(subset(maxcorr.stuff,experiment=='experiment 1'), cor(value.x,value.y)),
                                   with(subset(maxcorr.stuff,experiment=='experiment 2'), cor(value.x,value.y))
))
corrs$xpos<- 0.75
corrs$ypos<- 15
corrs$experiment <- c('experiment 1','experiment 2')


ggplot(maxcorr.stuff,aes(x=value.x,y=value.y,colour=conclusion))+
  geom_point(size=4)+
  geom_text(data=corrs,aes(x=xpos,y=ypos, label=paste('r =',round(correlations,2))),size=10,colour='black')+
  geom_abline(intercept=0,slope=100,colour='grey50')+
  facet_wrap(~experiment)+
  theme_solarized()+
  coord_fixed(ratio = 0.01,xlim = c(-0.02,1), ylim = c(-2,100))+
  scale_y_continuous(breaks=c(25,50,75))+
  scale_x_continuous(breaks=c(0.25,0.5,0.75))+
  xlab('\n model posterior')+
  ylab('human endorsement\n')+
  #scale_colour_di(guide = guide_legend()) +
  theme(legend.position="bottom",
        legend.direction='horizontal',
        legend.title=element_blank())

ggsave(filename =paste('pragmaticsMW_EP',EP,'alt',alt,max.n,'_alpha',max.alpha,'_base',max.base,'scatter.png',sep=''), plot4, height=14, width=14)

models$syllogism <- factor(models$syll, levels = c('AO2', 'EA3', 'IE1', 'OA1','AA1','AI1','EA1','EI1'),
                           labels=c("Some of the As are not Bs\n All of the Cs are Bs",
                                    "All of the Bs are As\n None of Bs are Cs",
                                    "None of the As are Bs\n Some of the Bs are Cs",
                                    "All of the As are Bs\n Some of the Bs are not Cs",
                                    "All of the As are Bs\n All of the Bs are Cs",
                                    "Some of the As are Bs\n All of the Bs are Cs",
                                    "All of the As are Bs\n None of the Bs are Cs",
                                    "Some of the As are Bs\n None of the Bs are Cs"
                           ))

models$domain <- factor(models$domain, labels = exp_domains)
models$conclusion<-factor(models$conclusion, labels = c('all','none','some','some...not'))

# Faceted grids of model predictions (Syll X Domain)

plot2<-ggplot(subset(models,syll%in%c('AO2', 'EA3', 'IE1', 'OA1') & alpha==max.alpha & base==max.base),
              aes(x=conclusion,y=n5,fill=conclusion))+
  geom_bar(position=position_dodge(.6), 
           width = .6,
           stat='identity')+
  facet_grid(domain~syllogism)+
  theme_solarized()+
  guides(fill=F)+
  theme(
    axis.text.x=element_text(angle=90,hjust=1,vjust=.5,colour='black'),
    strip.text.x = element_text(colour='black'),
    strip.text.y = element_text(angle=0,colour='black')
  )+
  coord_cartesian(ylim=c(0,1)) + 
  scale_y_continuous(breaks=c(.25,.50,.75))+
  xlab("\nconclusion")+
  ylab('posterior probability\n')

ggsave(filename = paste('pragmatics_EP',EP,'alt',alt,'_n5alpha2_exp1.png',sep=''),plot2, width=32, height=16)


plot3<-ggplot(subset(models,syll%in%c('AA1','AI1','EA1','EI1') & alpha==max.alpha & base==max.base),
              aes(x=conclusion,y=n5,fill=conclusion))+
  geom_bar(position=position_dodge(.6), 
           width = .6,
           stat='identity')+
  facet_grid(domain~syllogism)+
  theme_solarized()+
  guides(fill=F)+
  theme(
    axis.text.x=element_text(angle=90,hjust=1,vjust=.5,colour='black'),
    strip.text.x = element_text(colour='black'),
    strip.text.y = element_text(angle=0,colour='black')
  )+
  coord_cartesian(ylim=c(0, 1)) + 
  scale_y_continuous(breaks=c(0.25,0.5,0.75))+
  xlab("\nconclusion")+
  ylab('posterior probability\n')

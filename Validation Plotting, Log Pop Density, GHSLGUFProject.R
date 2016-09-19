library(ggthemes)
library(ggplot2)
library(foreign)
#library(viridis)
library(gridExtra)
library(gtable)
library(MASS)
setwd("D:/Research/WorldPop/GUF vs GHSL Project/ValidationPlots/QGIS Extracted Run/")

##  Define getlevel function to get cotour breaks:
getLevel <- function(x,y,prob=0.95) {
  kk <- MASS::kde2d(x,y)
  dx <- diff(kk$x[1:2])
  dy <- diff(kk$y[1:2])
  sz <- sort(kk$z)
  c1 <- cumsum(sz) * dx * dy
  approx(c1, sz, xout = 1 - prob)$y
}

##### NOTE THIS IS THE ONLY BLOCK YOU SHOULD HAVE TO MODIFY BETWEEN COUNTRY RUNS
##        Unless the data doesn't like your plot limits
country <- "TZA"
adminhighname <- "Village"
adminhighnum <- 5
adminlowname <- paste0("Randomly Aggregated\n",adminhighname)
#####


load(paste0(country,"_PopDeviation.RData"))
popdeviation$AREAKM <- popdeviation$AREA/1000000
##  Determine the appropriate limits after converting area to sq km:
observed <- log10(popdeviation$ADMINPOP / (popdeviation$AREAKM)  + 0.00001)
predicted <- log10(popdeviation$PREDPOP / (popdeviation$AREAKM)+ 0.00001)
##  Remove infinites
observed <- observed[observed!=Inf&predicted!=Inf]
predicted <- predicted[predicted!=Inf&observed!=Inf]
##  Remove NAs
exna <- !is.na(observed)&!is.na(predicted)
observed <- observed[exna]
predicted <- predicted[exna]
##  Remove -5 values
observed <- observed + 0.00001
predicted <- predicted + 0.00001
lim <- c(-1,max(max(observed),max(predicted)))

##  BEGIN:  SUBSETTING BY MODEL
##    ESA
d_E <- popdeviation[popdeviation$MODEL=="ESA",]
observed_E <- log10(d_E$ADMINPOP / d_E$AREAKM + 0.00001)
predicted_E <- log10(d_E$PREDPOP / d_E$AREAKM + 0.00001)
observed_E <- observed_E[observed_E!=Inf&predicted_E!=Inf]
predicted_E <- predicted_E[predicted_E!=Inf&observed_E!=Inf]
exna_E <- !is.na(observed_E)&!is.na(predicted_E)
observed_E <- observed_E[exna_E]
predicted_E <- predicted_E[exna_E]
observed_E <- observed_E + 0.00001
predicted_E <- predicted_E + 0.00001
##    MODIS
d_M <- popdeviation[popdeviation$MODEL=="MODIS",]
observed_M <- log10(d_M$ADMINPOP / d_M$AREAKM  + 0.00001)
predicted_M <- log10(d_M$PREDPOP / d_M$AREAKM + 0.00001)
observed_M <- observed_M[observed_M!=Inf&predicted_M!=Inf]
predicted_M <- predicted_M[predicted_M!=Inf&observed_M!=Inf]
exna_M <- !is.na(observed_M)&!is.na(predicted_M)
observed_M <- observed_M[exna_M]
predicted_M <- predicted_M[exna_M]
observed_M <- observed_M + 0.00001
predicted_M <- predicted_M + 0.00001

##    GHSL
d_H <- popdeviation[popdeviation$MODEL=="GHSL",]
observed_H <- log10(d_H$ADMINPOP / d_H$AREAKM  + 0.00001)
predicted_H <- log10(d_H$PREDPOP / d_H$AREAKM + 0.00001)
observed_H <- observed_H[observed_H!=Inf&predicted_H!=Inf]
predicted_H <- predicted_H[predicted_H!=Inf&observed_H!=Inf]
exna_H <- !is.na(observed_H)&!is.na(predicted_H)
observed_H <- observed_H[exna_H]
predicted_H <- predicted_H[exna_H]
observed_H <- observed_H + 0.00001
predicted_H <- predicted_H + 0.00001
##    GUF
d_G <- popdeviation[popdeviation$MODEL=="GUF",]
observed_G <- log10(d_G$ADMINPOP / d_G$AREAKM + 0.00001)
predicted_G <- log10(d_G$PREDPOP / d_G$AREAKM + 0.00001)
observed_G <- observed_G[observed_G!=Inf&predicted_G!=Inf]
predicted_G <- predicted_G[predicted_G!=Inf&observed_G!=Inf]
exna_G <- !is.na(observed_G)&!is.na(predicted_G)
observed_G <- observed_G[exna_G]
predicted_G <- predicted_G[exna_G]
observed_G <- observed_G + 0.00001
predicted_G <- predicted_G + 0.00001
##    GHSL GUF
d_HG <- popdeviation[popdeviation$MODEL=="GUF GHSL",]
observed_HG <- log10(d_HG$ADMINPOP / d_HG$AREAKM + 0.00001)
predicted_HG <- log10(d_HG$PREDPOP / d_HG$AREAKM + 0.00001)
observed_HG <- observed_HG[observed_HG!=Inf&predicted_HG!=Inf]
predicted_HG <- predicted_HG[predicted_HG!=Inf&observed_HG!=Inf]
exna_HG <- !is.na(observed_HG)&!is.na(predicted_HG)
observed_HG <- observed_HG[exna_HG]
predicted_HG <- predicted_HG[exna_HG]
observed_HG <- observed_HG + 0.00001
predicted_HG <- predicted_HG + 0.00001
##    SBAW GHSL
d_SH <- popdeviation[popdeviation$MODEL=="SBAW GHSL",]
observed_SH <- log10(d_SH$ADMINPOP / d_SH$AREAKM + 0.00001)
predicted_SH <- log10(d_SH$PREDPOP / d_SH$AREAKM + 0.00001)
observed_SH <- observed_SH[observed_SH!=Inf&predicted_SH!=Inf]
predicted_SH <- predicted_SH[predicted_SH!=Inf&observed_SH!=Inf]
exna_SH <- !is.na(observed_SH)&!is.na(predicted_SH)
observed_SH <- observed_SH[exna_SH]
predicted_SH <- predicted_SH[exna_SH]
observed_SH <- observed_SH + 0.00001
predicted_SH <- predicted_SH + 0.00001
##    SBAW GUF
d_SG <- popdeviation[popdeviation$MODEL=="SBAW GUF",]
observed_SG <- log10(d_SG$ADMINPOP / d_SG$AREAKM + 0.00001)
predicted_SG <- log10(d_SG$PREDPOP / d_SG$AREAKM + 0.00001)
observed_SG <- observed_SG[observed_SG!=Inf&predicted_SG!=Inf]
predicted_SG <- predicted_SG[predicted_SG!=Inf&observed_SG!=Inf]
exna_SG <- !is.na(observed_SG)&!is.na(predicted_SG)
observed_SG <- observed_SG[exna_SG]
predicted_SG <- predicted_SG[exna_SG]
observed_SG <- observed_SG + 0.00001
predicted_SG <- predicted_SG + 0.00001
##  END:  SUBSETTING BY MODEL

##  BEGIN:  CREATE LEVELS BY MODEL
##	NOTE: These values don't seem to be hard coded into the saved g90, g00, and g10
##		ggplot2 plots, which means that if they are overwritten they will affect the 
##		final output when plotted for all three plots... So they have to be named
##		uniquely...
##    ESA
L90_E <- getLevel(observed_E,predicted_E, prob=0.9)
L75_E <- getLevel(observed_E,predicted_E, prob=0.75)
L50_E <- getLevel(observed_E,predicted_E, prob=0.50)
L25_E <- getLevel(observed_E,predicted_E, prob=0.25)

##    MODIS
L90_M <- getLevel(observed_M,predicted_M, prob=0.9)
L75_M <- getLevel(observed_M,predicted_M, prob=0.75)
L50_M <- getLevel(observed_M,predicted_M, prob=0.50)
L25_M <- getLevel(observed_M,predicted_M, prob=0.25)

##    GHSL
L90_H <- getLevel(observed_H,predicted_H, prob=0.9)
L75_H <- getLevel(observed_H,predicted_H, prob=0.75)
L50_H <- getLevel(observed_H,predicted_H, prob=0.50)
L25_H <- getLevel(observed_H,predicted_H, prob=0.25)

##    GUF
L90_G <- getLevel(observed_G,predicted_G, prob=0.9)
L75_G <- getLevel(observed_G,predicted_G, prob=0.75)
L50_G <- getLevel(observed_G,predicted_G, prob=0.50)
L25_G <- getLevel(observed_G,predicted_G, prob=0.25)

##    GUF GHSL
L90_HG <- getLevel(observed_HG,predicted_HG, prob=0.9)
L75_HG <- getLevel(observed_HG,predicted_HG, prob=0.75)
L50_HG <- getLevel(observed_HG,predicted_HG, prob=0.50)
L25_HG <- getLevel(observed_HG,predicted_HG, prob=0.25)

##    SBAW GHSL
L90_SH <- getLevel(observed_SH,predicted_SH, prob=0.9)
L75_SH <- getLevel(observed_SH,predicted_SH, prob=0.75)
L50_SH <- getLevel(observed_SH,predicted_SH, prob=0.50)
L25_SH <- getLevel(observed_SH,predicted_SH, prob=0.25)

##    SBAW GUF
L90_SG <- getLevel(observed_SG,predicted_SG, prob=0.9)
L75_SG <- getLevel(observed_SG,predicted_SG, prob=0.75)
L50_SG <- getLevel(observed_SG,predicted_SG, prob=0.50)
L25_SG <- getLevel(observed_SG,predicted_SG, prob=0.25)

#cols <- viridis(4)
cols <- c("#fdae61","#abdda4","#2b83ba","#d7191c")

#pdf(file="1990_validation.pdf", width=5, height=4)
gESA <- ggplot(NULL, aes(x = observed_E, y= predicted_E)) + 
  geom_point(colour="black", alpha=0.125) + 
  theme_bw() + 
  stat_smooth(method="loess", fill="grey", colour="darkred", alpha=0.4) + 
  geom_abline(slope=1, intercept=0, linetype="dashed", colour="#00000066") + 
  stat_density2d(colour=cols[1], linetype="dotted", breaks=L90_E) + 
  stat_density2d(colour=cols[2], linetype="dashed", breaks=L75_E) + 
  stat_density2d(colour=cols[3], linetype="longdash", breaks=L50_E) + 
  stat_density2d(colour=cols[4], linetype="solid", breaks=L25_E) +
  theme(legend.key = element_blank()) + 
  ggtitle(paste0(country," ESA Population")) + 
  ##  Standard Scale
  scale_x_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  scale_y_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) +
  ##CRI ESA Scale
  #scale_x_continuous(breaks=c(-3,-2,-1,0,1), labels=c(0.001,0.01,0.1,0,10), limits=c(-3.5,1)) + 
  #scale_y_continuous(breaks=c(-3,-2,-1,0,1), labels=c(0.001,0.01,0.1,0,10), limits=c(-3.5,1)) + 
  ##NPL Scale
  #scale_x_continuous(breaks=c(-1,0,1,2), labels=c(0.1,0,10,100), limits=c(-1,2)) + 
  #scale_y_continuous(breaks=c(-4,-3,-2,-1,0,1), labels=c(0.0001,0.001,0.01,0.1,0,10), limits=c(-4,2)) + 
  ##ESAVNM Scale
  #scale_x_continuous(breaks=c(-1,0,1), labels=c(0.1,0,10), limits=c(-1,1.5)) + 
  #scale_y_continuous(breaks=c(-4,-3,-2,-1,0,1), labels=c(0.0001,0.001,0.01,0.1,0,10), limits=c(-4,1)) +
  labs(x="Observed (ppp)", y="Predicted (ppp)")



gMODIS <- ggplot(NULL, aes(x = observed_M, y= predicted_M)) + 
  geom_point(colour="black", alpha=0.125) + 
  theme_bw() + 
  stat_smooth(method="loess", fill="grey", colour="darkred", alpha=0.4) + 
  geom_abline(slope=1, intercept=0, linetype="dashed", colour="#00000066") + 
  stat_density2d(colour=cols[1], linetype="dotted", breaks=L90_M) + 
  stat_density2d(colour=cols[2], linetype="dashed", breaks=L75_M) + 
  stat_density2d(colour=cols[3], linetype="longdash", breaks=L50_M) + 
  stat_density2d(colour=cols[4], linetype="solid", breaks=L25_M) +
  theme(legend.key = element_blank()) + 
  ggtitle(paste0(country," MODIS Population")) + 
  scale_x_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  scale_y_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  labs(x="Observed (ppp)", y="Predicted (ppp)")

gGHSL <- ggplot(NULL, aes(x = observed_H, y= predicted_H)) + 
  geom_point(colour="black", alpha=0.125) + 
  theme_bw() + 
  stat_smooth(method="loess", fill="grey", colour="darkred", alpha=0.4) + 
  geom_abline(slope=1, intercept=0, linetype="dashed", colour="#00000066") + 
  stat_density2d(colour=cols[1], linetype="dotted", breaks=L90_H) + 
  stat_density2d(colour=cols[2], linetype="dashed", breaks=L75_H) + 
  stat_density2d(colour=cols[3], linetype="longdash", breaks=L50_H) + 
  stat_density2d(colour=cols[4], linetype="solid", breaks=L25_H) +
  theme(legend.key = element_blank()) + 
  ggtitle(paste0(country," GHSL Population")) + 
  scale_x_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  scale_y_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  labs(x="Observed (ppp)", y="Predicted (ppp)")

gGUF <- ggplot(NULL, aes(x = observed_G, y= predicted_G)) + 
  geom_point(colour="black", alpha=0.125) + 
  theme_bw() + 
  stat_smooth(method="loess", fill="grey", colour="darkred", alpha=0.4) + 
  geom_abline(slope=1, intercept=0, linetype="dashed", colour="#00000066") + 
  stat_density2d(colour=cols[1], linetype="dotted", breaks=L90_G) + 
  stat_density2d(colour=cols[2], linetype="dashed", breaks=L75_G) + 
  stat_density2d(colour=cols[3], linetype="longdash", breaks=L50_G) + 
  stat_density2d(colour=cols[4], linetype="solid", breaks=L25_G) +
  theme(legend.key = element_blank()) + 
  ggtitle(paste0(country," GUF Population")) + 
  scale_x_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  scale_y_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  labs(x="Observed (ppp)", y="Predicted (ppp)")

gGUFGHSL <- ggplot(NULL, aes(x = observed_HG, y= predicted_HG)) + 
  geom_point(colour="black", alpha=0.125) + 
  theme_bw() + 
  stat_smooth(method="loess", fill="grey", colour="darkred", alpha=0.4) + 
  geom_abline(slope=1, intercept=0, linetype="dashed", colour="#00000066") + 
  stat_density2d(colour=cols[1], linetype="dotted", breaks=L90_HG) + 
  stat_density2d(colour=cols[2], linetype="dashed", breaks=L75_HG) + 
  stat_density2d(colour=cols[3], linetype="longdash", breaks=L50_HG) + 
  stat_density2d(colour=cols[4], linetype="solid", breaks=L25_HG) +
  theme(legend.key = element_blank()) + 
  ggtitle(paste0(country," GUF-GHSL Population")) + 
  scale_x_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  scale_y_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  labs(x="Observed (ppp)", y="Predicted (ppp)")

gSBAWGHSL <- ggplot(NULL, aes(x = observed_SH, y= predicted_SH)) + 
  geom_point(colour="black", alpha=0.125) + 
  theme_bw() + 
  stat_smooth(method="loess", fill="grey", colour="darkred", alpha=0.4) + 
  geom_abline(slope=1, intercept=0, linetype="dashed", colour="#00000066") + 
  stat_density2d(colour=cols[1], linetype="dotted", breaks=L90_SH) + 
  stat_density2d(colour=cols[2], linetype="dashed", breaks=L75_SH) + 
  stat_density2d(colour=cols[3], linetype="longdash", breaks=L50_SH) + 
  stat_density2d(colour=cols[4], linetype="solid", breaks=L25_SH) +
  theme(legend.key = element_blank()) + 
  ggtitle(paste0(country," SBAW GHSL Population")) + 
  scale_x_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  scale_y_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  labs(x="Observed (ppp)", y="Predicted (ppp)")

gSBAWGUF <- ggplot(NULL, aes(x = observed_SG, y= predicted_SG)) + 
  geom_point(colour="black", alpha=0.125) + 
  theme_bw() + 
  stat_smooth(method="loess", fill="grey", colour="darkred", alpha=0.4) + 
  geom_abline(slope=1, intercept=0, linetype="dashed", colour="#00000066") + 
  stat_density2d(colour=cols[1], linetype="dotted", breaks=L90_SG) + 
  stat_density2d(colour=cols[2], linetype="dashed", breaks=L75_SG) + 
  stat_density2d(colour=cols[3], linetype="longdash", breaks=L50_SG) + 
  stat_density2d(colour=cols[4], linetype="solid", breaks=L25_SG) +
  theme(legend.key = element_blank()) + 
  ggtitle(paste0(country," SBAW GUF Population")) + 
  scale_x_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  scale_y_continuous(breaks=c(-1,0,1,2,3,4), labels=c(0.1,0,10,100,1000,10000), limits=lim) + 
  labs(x="Observed (ppp)", y="Predicted (ppp)")

pdf(file=paste0(country,"_Validation Plots_Log Population Density.pdf"), width=13, height=13)	
grid.arrange( gESA, gMODIS, gGHSL,gGUF,gGUFGHSL,gSBAWGHSL,gSBAWGUF, 
              widths=unit(c(4,4,4,4,4,4,4,6), "in"), ncol=3, 
              top=textGrob(paste(country,"\n",
                                 adminhighname,
                                 "-Level (",
                                 adminhighnum,
                                 ")\nvs.\n",
                                 adminlowname,
                                 "\nLog Population Density\n(",
                                 expression(log[10]),
                                 "(people/pixel))"),
                           gp=gpar(cex=1.5)))
dev.off()
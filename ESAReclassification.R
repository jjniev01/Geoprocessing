##  TITLE:  ESA RECLASSIFICATION
##  AUTHOR:  JEREMIAH J. NIEVES
##  LAST UPDATE:  2016-05-27
##  NOTES:  
##
##
##
##

#####
##  BEGIN:  GENERAL STATEMENTS AND FUNCTIONS
require(raster)
require(snow)

##  Set the root path:
root <- "C:/Users/jnieves/Desktop/ESA Data/"

##  Set the number of cluster workers:
cluster_workers <- 6

##  END:  GENERAL STAEMENTS AND FUNCTIONS
#####

#####
##  BEGIN:  DATA IMPORT
##  Define in raster:
in_raster <- paste0(root, "ESACCI-LC-L4-LCCS-Map-300m-P5Y-2010-v1.6.1.tif")

##  Load the raster (in memory):
esa_lc <- raster(in_raster)

##  END:  DATA IMPORT
#####

#####
##  BEGIN: LC RECLASSIFICATION
##  Create a reclassifcation raster to convert the ESA LC to our WorldPop 
##    standard; the first two columns define the range and the third column 
##    declares the new value for each range:
from_vec <- c(0,
              10,
              40,
              110,
              130,
              120,
              140,
              160,              
              190,
              200,
              210,
              220
              )


to_vec <- c(0.1,
            30.1,
            100.1,
            110.1,
            130.1,
            122.1,
            153.1,
            180.1,
            190.1,
            202.1,
            210.1,
            220.1
            )
val_vec <- c(230,
             11,
             40,
             140,
             130,
             130,
             150,
             160,
             190,
             200,
             210,
             200
             )
rc_matrix <- matrix(nrow = length(val_vec), ncol = 3)
rc_matrix  <-cbind(rc_matrix, from_vec, to_vec, val_vec)
rc_matrix <- rc_matrix[,4:6]

new_lc <- reclassify(esa_lc, rc_matrix, filename = paste0(root, "ESA_Reclassified_2016_05_30.tif"), include.lowest = TRUE)

##  END:  LC RECLASSIFICATION
#####

#####
##  BEGIN:  NEW LC EXPORT

##  END:  NEW LC EXPORT
#####
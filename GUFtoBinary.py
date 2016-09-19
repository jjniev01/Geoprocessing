##  GHSL to 0 and 1  ##
import os, arcpy, glob

root = "W:/GHSLGUF Project/GUF GHSL Binary WGS84/"

arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
def GUFConvert(inras):
    iso = inras.split("/")[2].split("\\")[1]
    outras = inras.split(os.path.basename(inras))[0]+iso+"_GUF_binary.tif"
    urb = arcpy.Raster(inras)
    binguf = arcpy.sa.Con(urb==255,1,0)
    binguf.save(outras)




f = glob.glob(root+"*\\GUF\\*.tif")
    

for i in f:
   GUFConvert(i)

arcpy.CheckInExtension()

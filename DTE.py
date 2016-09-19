##  Distance to Edge ##
from __future__ import print_function
print("Importing packages...")
import os, arcpy, fnmatch

print("Setting general paths and settings...")
root = "W:/GHSLGUF Project/GUF GHSL Binary WGS84/"

arcpy.env.overwriteOutput = True

print("Defineing Projections...")
##  Define the projection dictionary:
prj_dict = {
    "VNM":"PROJCS['WGS_1984_UTM_Zone_48N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',105.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
    "KEN":"PROJCS['WGS_1984_UTM_Zone_37N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',39.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
    "CRI":"PROJCS['WGS_1984_UTM_Zone_16.5N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-84.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0],AUTHORITY['EPSG',32616]]",
    "HTI":"PROJCS['WGS_1984_UTM_Zone_18.5N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-72.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0],AUTHORITY['EPSG',32618]]",
    "NAM":"PROJCS['WGS_1984_UTM_Zone_33.5S',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',18.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
    "THA":"PROJCS['WGS_1984_UTM_Zone_46.5N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',96.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
    "MMR":"PROJCS['WGS_1984_UTM_Zone_46.5N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',96.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
    "NPL":"PROJCS['WGS_1984_UTM_Zone_44.5N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',84.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
    "MEX":"PROJCS['WGS_1984_UTM_Zone_13.5N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-102.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
    "ECU":"PROJCS['WGS_1984_UTM_Zone_17S',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-81.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]",
    "TZA":"PROJCS['WGS_1984_UTM_Zone_36.5S',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',36.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"}

print("Checking Out Extentsions...")
##  Check out the Spatial Analyst Extension:
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *

##  Define a function that replicates the Con() in Arcmap so I can do Raster Math without the
##  excessive ifelse and the string formatting needed for raster calculator:
##def Conditional(condition, trueValue, falseValue):
##    if condition:
##        foo = 1
##        opp = 0
##    else:
##        foo = 0
##        opp = 1
##        
##    return(foo * trueValue + (opp)*falseValue)
print("Defining Functions...")
##	Create a directory function to check for and create data directories if they don't exist:
def ensure_dir(d):
	if not os.path.isdir(d):
		os.makedirs(d)
	return d

##  Define the function that actually calculates the distance to edge:
def DTE(tiffile):
    
    ##  Retrieve country ISO:
    iso = tiffile.split("/")[3].split("\\")[0]
    print("Working on {0}".format(iso))
    ##  Set the output path:
    outpath = tiffile.split(os.path.basename(tiffile))[0]
    
    print("\tProjecting Data...")
    ##  Project the dataset  ##
    ##    Retrieve projection from dictionary:
    intermediate_prj = prj_dict[iso]
    
    ##    Set the ouput data name:
    outpath = ensure_dir(tiffile.split(".tif")[0]+"tmp/")
    output =  outpath + "_projected.tif"
    
    ##    Project the dataset:
    data_desc = arcpy.Describe(tiffile)
    input_prj = data_desc.SpatialReference.exportToString()
    arcpy.ProjectRaster_management(tiffile, output, intermediate_prj, "NEAREST","100","#","#",input_prj)

    ##  Retrieve the projected dataset:
    prjtif = output

    print("\tPolygonizing...")
    ##  Calculate the DTE  ##
    ##    Raster to Polygon:
    arcpy.RasterToPolygon_conversion(prjtif,"D:/tmp/"+iso+"_polyras.shp","NO_SIMPLIFY","VALUE")
    polyras = "D:/tmp/"+iso+"_polyras.shp"

    ##    Convert the polygon to a feature layer:
    polyfeat = arcpy.MakeFeatureLayer_management(polyras, "polyras")

    print("\tLinizing...")
    ##    Polygon to Line:
    arcpy.PolygonToLine_management(polyfeat, "D:/tmp/"+iso+"_polyline.shp", "IGNORE_NEIGHBORS")
    polyline = "D:/tmp/"+iso+"_polyline.shp"

    print("\tCalculating Distance to Line...")
    ##    Distance to Line:
    output = "D:/tmp/"+iso+"dst.tif"
    dstras = arcpy.sa.EucDistance(polyline, cell_size = 100)
    dstras.save(output)
    

    ##    Convert the internal numbers to negative using rastermath:
    print("\tCalculating negative values...")
    outpath = ensure_dir(tiffile.split(".tif")[0] +"Output/")
    output = outpath + "_projected_DTE.tif"
    urb = arcpy.Raster(tiffile)
    dteras = arcpy.sa.Con(urb == 1,-1,0) * dstras + arcpy.sa.Con(urb == 0,1,0)*dstras
    dteras.save(output)
    
print("Gathering files...")
##  Get a list of all the files:
f = []
for roots, dirnames, filenames in os.walk(root):
    for filename in fnmatch.filter(filenames, '*.tif'):
        f.append(os.path.join(roots, filename))
print(f)

print("Running DTE...")
for i in f:
   DTE(i)

print("Checking In Extension")           
arcpy.CheckInExtension("Spatial")                    
    

    

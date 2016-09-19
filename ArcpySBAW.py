import arcpy, glob, os, sys

root_path = "D:/Users/jnieves/Research/SBAW/"

arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False
arcpy.CheckOutExtension("Spatial")

def ensure_dir(d):
    if not os.path.isdir(d):
        os.makedirs(d)
    return d

clist = ["MEX"]
#clist = ["CRI","HTI","KEN","TZA","NAM","MMR","VNM","THA","NPL","MEX"]

for i in clist:
    try:
        #  Set output paths:
        outpath = ensure_dir(root_path + "Output/" + i+ "/")
        tmp_out = ensure_dir(outpath + "tmp/")
        
        print("Getting Census file...")
        #  Read in the projected census data:
        #    Get the census data path:
        census_path = glob.glob(root_path + "Census Data/Aggregated/"+i+"/*.shp")[0]

        print("Resampling watermask to 0.0008333 degress...")
        #  Resample the watermask to 100m (i.e. 0.0008333 degree):
        if not(os.path.exists(root_path+"Watermasks/"+i+"/landcover_cls210_100m.tif")):
            arcpy.Resample_management(root_path+"Watermasks/"+i+"/landcover_cls210.tif", root_path+"Watermasks/"+i+"/landcover_cls210_100m.tif","0.0008333","NEAREST")
        #  Set a list of the urban dataset folders stored as tifs
        #  in the folder "! UrbanRepo":
        urb_folders = [root_path+"GUF GHSL Binary WGS84/"+i+"/GHSL/", root_path+"GUF GHSL Binary WGS84/"+i+"/GUF/"]

        for urb_folder in urb_folders:
            #    Get the census data as a layer:
            census_layer = arcpy.MakeFeatureLayer_management(census_path,"census_layer")
            print("Retrieving urban datasets...")
            #  Get the urban dataset path:
            urb = arcpy.Raster(glob.glob(urb_folder+"*.tif")[0])
            urbname = urb_folder.split("/")[-2]
            print("\tRetrieved {0}.".format(urbname))
            
            print("Applying watermask to urban data...")
            #  Watermask it:
            watermask = arcpy.Raster(root_path+"Watermasks/"+i+"/landcover_cls210_100m.tif")
            #maskedurb = arcpy.sa.Con(watermask == 1,0,1)*urb
            maskedurb = arcpy.sa.Con(watermask == 0, urb)
            maskedurb.save(tmp_out+urbname+"_masked.tif")
            urb = arcpy.Raster(tmp_out+urbname+"_masked.tif")
            
            #  Get a count of the number of urban pixels in each admin unit,
            #    using ZonalStatisticsAsTable:
            print("Getting count of the number of urban pixels per admin unit...")
            outtbl = tmp_out+"urbansum_"+urbname+".dbf"
            arcpy.sa.ZonalStatisticsAsTable(census_path,"ADMINID",urb,outtbl,"DATA","SUM")

            #  Add URBDENS field:
            print("Calculating urban population density...")
            fieldnames = [f.name for f in arcpy.ListFields(census_layer)]
            popfield = os.path.basename(census_path).split(".")[0]+".ADMINPOP"
            urbfield = "urbansum_"+urbname+".SUM"
            urbdensfield = os.path.basename(census_path).split(".")[0]+".URBDENS"
            print(fieldnames)
            if "URBDENS" in fieldnames:
                print("Field Already Exists; Deleting...")
                census_layer = arcpy.DeleteField_management(census_layer,["URBDENS"])

            #  Join the zonal table to the census layer:
            arcpy.AddJoin_management(census_layer,"ADMINID",outtbl,"ADMINID")

            #  Write the joined census layer with urb density values to the tmp folder:
            joinfeat = tmp_out+urbname+"_urbansum.shp"
            arcpy.CopyFeatures_management(census_layer,joinfeat)
            join_lyr = arcpy.MakeFeatureLayer_management(joinfeat,"join_lyr")

            #  Create new field:
            join_lyr = arcpy.AddField_management(join_lyr,"URBDENS","DOUBLE")
            #  Select records with SUM == 0:
            arcpy.SelectLayerByAttribute_management(join_lyr,"NEW_SELECTION",'SUM = 0')
            arcpy.CalculateField_management(join_lyr,"URBDENS", 0, "PYTHON_9.3")
            #  Calculate new field:
            arcpy.SelectLayerByAttribute_management(join_lyr, "NEW_SELECTION", 'SUM <> 0')
            arcpy.CalculateField_management(join_lyr,"URBDENS", '!ADMINPOP!/!SUM!',"PYTHON_9.3")
            #  Clear selection:
            arcpy.SelectLayerByAttribute_management(join_lyr,"CLEAR_SELECTION")
            #  Write the urb density shapefile to file:
            urbdens = tmp_out+urbname+"_urbdensity.shp"
            arcpy.CopyFeatures_management(join_lyr, urbdens)
            print("\tFinished urban density calculation.")
           
            #    Read it back in as a layer:
            urbdens_lyr = arcpy.MakeFeatureLayer_management(urbdens,"urbdens_lyr")
            print("Rasterizing population density...")
            #  Rasterize the urban density data:
            outras = tmp_out+urbname+"_urbdens_rasterized.tif"
            arcpy.PolygonToRaster_conversion(urbdens_lyr,"URBDENS",outras,"CELL_CENTER","",0.0008333)
            #    Read it back in as a raster:
            urbdens_ras = arcpy.Raster(outras)

            print("Applying urban mask to population density...")
            #    Apply watermask and the urban mask:
            fin_path = tmp_out+i+"_"+urbname+"_SBAW_PPP_unclipped.tif"
            fin_ras = urb*urbdens_ras
            #  Save the final raster:
            fin_ras.save(fin_path)
            print("Clipping to country extents...")
            #  Clip to the extents of the census data:
            arcpy.Clip_management(arcpy.Raster(fin_path), out_raster = outpath+i+"_"+urbname+"_SBAW_PPP.tif",in_template_dataset = census_path, clipping_geometry = "ClippingGeometry")
            print("Successfully processed {0} {1}".format(i, urbname))
            del census_layer,join_lyr,urbdens_lyr
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])


arcpy.CheckInExtension("Spatial")



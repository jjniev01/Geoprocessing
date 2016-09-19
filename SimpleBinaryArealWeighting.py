# TITLE: Simple Binary Areal Weighting
# AUTHOR:  Jeremiah J. Nieves
#  UPDATED: 16 JUNE 2016
#  VERSION: 0.1
#  NOTES:  This script should be written to be used in conjunction
#          with the RF folder structure and other WorldPop src code.
#
#
#

#####
#  BEGIN: GENERAL STATEMENTS AND FUNCTIONS
from __future__ import print_function
import numpy, glob, os
from osgeo import ogr, gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
from rasterstats import zonal_stats
from osgeo import osr, ogr


#  -- DEFINE GLOBALS --  #

#  Provide a list of three-letter ISO definitions to
#  indicate what countries to process:
clist = ["MEX"]#,"VNM","THA","MMR","NPL","NAM","KEN","TZA",
         #"CRI","ECU","HTI"]


#  -- GDAL RELATED ITEMS --  #
#  Enable GDAL exceptions:
gdal.UseExceptions()

#  Define which OGR driver to use for all vector based data:
driver = ogr.GetDriverByName("ESRI Shapefile")
#
# #  Set up the ability to load spatial data into memory
# #    Create the output memory datasource:
# outdriver = ogr.GetDriverByName("MEMORY")
# ram = outdriver.CreateDataSource("tmpRAMData")
# #    Open the ram memory source with write access:
# tmp = outdriver.Open("tmpRAMData", 1)


#  Define a GDAL Error Handler:
def gdal_error_handler(err_class, err_num, err_msg):
    errtype = {
            gdal.CE_None:'None',
            gdal.CE_Debug:'Debug',
            gdal.CE_Warning:'Warning',
            gdal.CE_Failure:'Failure',
            gdal.CE_Fatal:'Fatal'
    }
    err_msg = err_msg.replace('\n',' ')
    err_class = errtype.get(err_class, 'None')
    print('Error Number: {0}'.format(err_num))
    print('Error Type: {0}'.format(err_class))
    print('Error Message: {0}'.format(err_msg))


#  Install the GDAL Error Handler:
gdal.PushErrorHandler(gdal_error_handler)

#  Function to make sure directory exists:
def ensure_dir(d):
    if not os.path.isdir(d):
        os.makedirs(d)
    return d

#  Create a function which will retrieve the
#  field information from a shapefile:
def attributeRetriever(shapefile, fieldname_list, type = "integer"):
    """ The shapefile_layer should be an OGR layer object
        the fid_field should be the name of a unique feature
        identification field, and fieldname_list should be a list
        that contains the string representation of the field
        names that are to be extracted. Return a list, indices of
        the list correspond to the FID of the feature, of
        dictionaries which contain the requested fields"""

    #  Create an empty list:
    feat_attributes = []
    shapefile_layer = shapefile.GetLayer()
    #  For every feature in the layer:
    for f in shapefile_layer:
        #  Create an empty dictionary:
        foo_dict = {}

        #  Put the FID in the dictionary:
        foo_dict["FID"] = f.GetFID()

        #  For every declared field to be extracted:
        for fn in fieldname_list:
            if type == "integer":
                #  Retrieve the field value and put in the dictionary:
                foo_dict[fn] = f.GetFieldAsInteger(fn)
            if type == "double":
                #  Retrieve the field value and put in the dictionary:
                foo_dict[fn] = f.GetFieldAsDouble(fn)

        # Append the dictionary to the list:
        feat_attributes.append(foo_dict)

    return feat_attributes


def polyToRaster(shp_layer, template_raster, output_path, outfile_name):
    """This function will take a polygon vector shapefile and
       convert it to a GeoTiff, assigning cell values based upon
       a single defined Field. This function assumes you are
       feeding it a OGR layer and a gdal raster layer upon
       which to base the spatial characteristics of the output
       raster on.
       NOTE:  The attribute field used is HARDCODED into the
       last line of this function. Couldn't remember how to
       pass it dynamically
       """
    try:
        #  -- Begin by creating the destination raster -- #
        #  Get the extents of the new raster based upon the
        #  template raster:
        tmpras_geom = template_raster.GetGeoTransform()
        # xmin = tmpras_geom[0]
        # xres = tmpras_geom[1]
        # ymax = tmpras_geom[3]
        # yres = tmpras_geom[5]

        #  Set resolutions to that of the template:
        n_x = template_raster.RasterXSize
        n_y = template_raster.RasterYSize

        #  Create the raster:
        out = output_path + outfile_name

        #  If the file already exists:
        if os.path.isfile(out):
            os.remove(out)

        gtiff = gdal.GetDriverByName("GTiff")
        out_ras = gtiff.Create(out,n_x,n_y,1,gdal.GDT_Float32)

        #  Define the spatial references identical to the template:
        out_ras.SetProjection(template_raster.GetProjection())
        out_ras.SetGeoTransform(tmpras_geom)

        #  Retrieve the first raster band and set it to nodata:
        #    NOTE:  Interesting how the counting starts with 1 here.

        rband = out_ras.GetRasterBand(1)
        rband.SetNoDataValue(-999)
        rband.Fill(-999)
        burnatt = "URBDENS"
        #  Rasterize the polygon with the indicated field for new values:
        gdal.RasterizeLayer(out_ras,  #  Where to put it
                            [1],  #  Band to use
                            shp_layer,  # What polygon
                            options = ["ATTRIBUTE=%s"%burnatt])

        out_ras.FlushCache()
        out_ras = None
        shp_layer = None
    except:
        out_ras = None
        shp_layer = None
        del out_ras
        del shp_layer


#  -- BASE PATHS --  #
#  Read in the root path from the configuration script to
#  get the RF folder structure path :
#  NOTE:  If running in pycharm, their stupid projects
# hierarchy messes this up and requires you call the following first
# to directly point to the local directory:
root_path = "D:/Research/WorldPop/GUF vs GHSL Project/SBAW/"

#  --  GEOPROCESSING --  #
#  Define the function which will perform the binary areal weighting:
def binArealWeighting(countries = None):
    """This function yada yada yada. Countries should be a list of
    three-letter country ISO codes.
    """
    #  For each country in the input list:
    for i in clist:
        print("Processing: {0}".format(i))
        #  Define the country data folder path:
        #country_path = root_path + i + "/"
        stats = None
        census_att = None

        #  Set the outpath:
        outpath = ensure_dir(root_path + "Output/" + i+ "/")

        #  Set the temporary outpath:
        tmp_out = ensure_dir(outpath + "tmp/")

        print("Getting Census file...")
        #  Read in the projected census data:
        #    Get the census data path:
        census_path = glob.glob(root_path + "Census Data/Aggregated/"+i+"/*.shp")[0]

        #  Set a list of the urban dataset folders stored as tifs
        #  in the folder "! UrbanRepo":
        urb_folders = [root_path+"GUF GHSL Binary WGS84/"+i+"/GHSL/", root_path+"GUF GHSL Binary WGS84/"+i+"/GUF/"]

        #  Project the census data and return the projected census shapefile:
        # proj_cens_path = projectFeature(census_path, i, urb_path, tmp_out)
        proj_cens_path = census_path
        #  Open the census file; 1 indicates it can be modified:
        census_prj = driver.Open(proj_cens_path, 1)

        #  Get the census layer:
        census_ram = census_prj.GetLayer()

        #  Get the admin population counts referenced by admin pop:
        #  NOTE: See output notes in the function definition of
        #        attributeRetriever.
        print("Retrieving census population attribute...")
        census_att = attributeRetriever(census_prj, ["ADMINPOP"])

        #  Define new field name to be created:
        nfield = "URBDENS"

        for urb_folder in urb_folders:

            #  Mask the urban areas by the watermask and write the
            #    watermasked urban data to be retrieved by the urb glob
            #    glob step below:
            #  Retrieve watermask and read in as an array:
            print("Retireving watermask as array...")
            waterpath = root_path+"Watermasks/"+i+"/landcover_cls210.tif"
            watermask = gdal.Open(waterpath)
            water_arr = watermask.GetRasterBand(1).ReadAsArray()
            #  Invert the 1's and 0's of the water mask:
            water_arr = 1-water_arr
            #  Check to make sure the values are right:
            for i in range(watermask.RasterYSize):
                for j in range(watermask.RasterXSize):
                    if water_arr[i,j] != 0 and water_arr[i,j] !=1:
                        print("Item {0}, {1} has non-binary value of {2}".format(i,j,water_arr[i,j]))

            print("Retrieving urban data from {0} ...".format(urb_folder))
            urb = glob.glob(urb_folder+"*.tif")[0]
            urb_op = gdal.Open(urb)
            if urb_folder.endswith("GUF/"):
                nd = 255
            if urb_folder.endswith("GHSL/"):
                nd = -2147483648
            urb_band = urb_op.GetRasterBand(1)
            urb_band.SetNoDataValue(nd)
            urb_arr = urb_band.ReadAsArray()
            #  Check to make sure the values are right:
            for i in range(urb_op.RasterYSize):
                for j in range(urb_op.RasterXSize):
                    if urb_arr[i,j] != 0 and urb_arr[i,j] !=1 and urb_arr[i,j]== nd:
                        urb_arr[i,j] = 0
                    if urb_arr[i,j] != 0 and urb_arr[i,j] !=1 and urb_arr[i,j]!= nd:
                        print("Item {0}, {1} has non-binary value of {2}".format(i,j,urb_arr[i,j]))

            print("Masking urban areas with water mask...")
            masked_urb = urb_arr * water_arr

            print("Writing water masked urban dataset...")
            newurb = driver.Create(urb_folder+"watermasked_urbandata.tif", urb_op.RasterXSize, urb_op.RasterYSize, 1)
            newurb.GetRasterBand(1).WriteArray(masked_urb)

            prj = urb_op.GetProjection()
            georef = urb_op.GetGeoTransform()
            newurb.SetProjection(prj)
            newurb.SetGeoTransform(georef)
            newurb.FlushCache()
            newurb = None
            del watermask,water_arr,urb_op,urb_arr

            #  Get the urban dataset name:
            urbdataname = i + "_" + urb.split("/")[-1].split("\\")[0]

            try:
                #  Delete the new field if it exists:
                #    If the field name does not equal nonexistant:
                census_ram.ResetReading()
                if census_ram.GetLayerDefn().GetFieldIndex(nfield) != -1:
                    print("Field already exists; deleting field.")
                    #  Delete the field:
                    census_ram.DeleteField(census_ram.FindFieldIndex(nfield,1))

                #  Reset the feature reading to the first feature:
                census_ram.ResetReading()

                print("Reading urban data...")
                #  Read in the urban dataset:
                urban = gdal.Open(urb_folder+"watermasked_urbandata.tif")

                #  Carry out zonal stats to get the count of urban cells
                #  in each feature; will return a list of dictionaries,
                #  one for each feature:
                #  NOTE: Must have the file paths as input, not any
                #        GDAL/OGR objects:
                print("Calculating zonal statistics...")
                stats = zonal_stats(census_path, urb_folder+"watermasked_urbandata.tif", stats = ["sum"],conditional = True)

                #  Create a field definition for the new field containing the
                #  new pop density for each admin unit; OFTReal is a double:
                field_def = ogr.FieldDefn(nfield, ogr.OFTReal)
                #  Create the field:
                census_ram.CreateField(field_def)

                census_ram.ResetReading()

                print("Calculating population density...")
                # For every feature in the census:
                for feature in census_ram:
                    # Get the FID:
                    fid = feature.GetFID()
                    print("FID: {0}".format(fid))
                    if double(stats[fid]["sum"]) == 0.0:
                        popdens = 0.0
                    #  If the sum is none due to no data, pass:
                    elif stats[fid]["sum"] == None:
                        pass
                    else:
                        #  Calculate the new pop density:
                        popdens = double(census_att[fid]["ADMINPOP"])/double(stats[fid]["sum"])

                    print("Pop. Density: {0} people per pixel".format(popdens))

                    #  Set the field value:
                    feature.SetField(nfield, double(popdens))
                    #  Update the feature with the new field value:
                    census_ram.SetFeature(feature)

                census_ram.ResetReading()
                #  Close the census shapefile so changes can be set:
                census_prj = None
                census_ram = None

                #  Reopen the file and layer
                census_prj = ogr.Open(census_path,1)
                census_ram = census_prj.GetLayer()

                print("Rasterizing census data...")
                polyToRaster(census_ram, urban,tmp_out,urbdataname+"_binary_popdens_census_raster.tif")
                #raw_input("Press Enter to continue after you have manually rasterized the\nURBDENS field in QGIS.")
                print("Opening rasterized census data...")
                #  Open the rasterized dataset:
                poprasdens = gdal.Open(tmp_out+urbdataname+"_binary_popdens_census_raster.tif")

                #  --  Raster Math Time  --  #
                print("Setting final output path...")
                #  Set the output path:
                fin_surf_path = outpath+"SBAW_" + urbdataname + "_PPP.tif"
                if os.path.isfile(fin_surf_path): os.remove(fin_surf_path)

                print("Dumping raster data into arrays...")
                #  Dump the datas into arrays:
                pop_ban = poprasdens.GetRasterBand(1)
                urb_ban = urban.GetRasterBand(1)
                pop_arr = BandReadAsArray(pop_ban)
                urb_arr = BandReadAsArray(urb_ban)

                print("Performing Raster Math...")
                #  Carry out calculation:
                fin_surface = pop_arr * urb_arr

                print("Creating output dataset...")
                #  Create the output dataset:
                #    Create the file:
                out_surf = gdal.GetDriverByName("GTiff").Create(fin_surf_path,
                                                                urban.RasterXSize,
                                                                urban.RasterYSize,
                                                                1,
                                                                gdal.GDT_Float32)
#

                rband = out_surf.GetRasterBand(1)
                rband.SetNoDataValue(NAN)
                rband.Fill(NAN)

                print("Writing calculated output to band...")
                #  Get the band from the output raster:
                #bandout = out_surf.GetRasterBand(1)
                #  Write the calculated values:
                rband.WriteArray(fin_surface)

                out_surf.SetProjection(urban.GetProjection())
                out_surf.SetGeoTransform(urban.GetGeoTransform())
                # Release the data to be written
                rband = None
                out_surf = None
                urban = None
                pop_ban = None
                urb_ban = None
                out_surf = None
                stats = None
                poprasdens = None
                print(urbdataname+" Model Complete!")
            except:
                print("Something wrong yo")

            finally:
                #  Close the urban dataset to retrieve memory resources:
                urban = None
                pop_ban = None
                urb_ban = None
                bandout = None
                out_surf = None
                stats = None
                poprasdens = None



#  END:  GENERAL STATMENTS AND FUNCTIONS
#####

# Carry out the map production:
binArealWeighting(clist)
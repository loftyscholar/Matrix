import os,sys,arcpy
import time,math
from geoprocesstools import *
from calculator import *

path_result = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True

def getMinXY(inFeatureClass):
    extentXY = []
    with arcpy.da.SearchCursor(inFeatureClass,['SHAPE@']) as cursor:
        minX = 10000
        minY = 10000
        maxX = -10000
        maxY = -10000
        
        for row in cursor:
            extent = row[0].extent
            if extent.XMin < minX:
                minX = extent.XMin
                
            if extent.YMin <  minY:
                minY =  extent.YMin

            if extent.XMax > maxX:
                maxX = extent.XMax

            if extent.YMax > maxY:
                maxY = extent.YMax
                
        extentXY.append(minX)
        extentXY.append(minY)
        extentXY.append(maxX)
        extentXY.append(maxY)
        
    return extentXY
def checkandrepair3(path_result):
    path_match = sys.path[0] + '/match.config'
    dictionary = read_match(path_match)
    arcpy.env.workspace = path_result
    GDBs_result = arcpy.ListFiles('*.gdb')
    while 1:
        needrepair = 0
        for GDB_result in GDBs_result:
            arcpy.env.workspace = path_result+'\\' + GDB_result
            layers = arcpy.ListFeatureClasses()
            if 'LCA_intersect' not in layers:
                needrepair = 1
        if needrepair == 1:
            for GDB_result in GDBs_result:
                arcpy.env.workspace = path_result+'\\' + GDB_result
                layers = arcpy.ListFeatureClasses()         
                if 'LCA_intersect' not in layers:
                    print GDB_result+':lack of LCA_intersect'
                    f = open(sys.path[0]+'/log/'+GDB_result[0:6]+'.txt','a')
                    start = time.clock()
                    time_start = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
                    
                    AlterField('LCA_old','CC','CC_old','CC_old')

                    #create fishnet
                    extent = getMinXY('LCA_new')
                    fishnet_out = 'grid'
                    originCoordinate = str(extent[0] - 0.025) + " " + str(extent[1] - 0.025)
                    yAxisCoordinate = str(extent[0]) + " " + str(extent[1] + 10)
                    numRows = math.ceil((extent[3] - extent[1])/0.05) + 1
                    numColumns=  math.ceil((extent[2] - extent[0])/0.05) + 1
                    arcpy.CreateFishnet_management(fishnet_out, originCoordinate, yAxisCoordinate, '0.05', '0.05', numRows, numColumns, '#', 'NO_LABELS', 'LCA_new', 'POLYGON')


                    #PAC_old intersect grid
                    intersectOutput = 'LCA_old_grid'
                    intersect(['LCA_old','grid'],intersectOutput)

                    #PAC_old intersect grid
                    intersectOutput = 'LCA_new_grid'
                    intersect(['LCA_new','grid'],intersectOutput)
                    
                    #PAC_old_grid intersect PAC_new_grid           
                    inFeatures = ['LCA_old_grid','LCA_new_grid']
                    intersectOutput ='LCA_intersect'
                    intersect(inFeatures,intersectOutput)
                    print GDB_result+':intersect finished'
                    
                    end = time.clock()
                    time_end = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
                    f.write('R2,'+time_start+','+time_end+','+str(end-start)+'\n')
                    f.close()            
        else:
            break
    print "check3 finished"            
               
    
if __name__ == '__main__':
    checkandrepair3(path_result)

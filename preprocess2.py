# -*- coding: utf-8 -*-
import arcpy,sys,os,time,math
from geoprocesstools import *



#参数

path_result = arcpy.GetParameterAsText(0)    
GDB =arcpy.GetParameterAsText(1)
path_old = arcpy.GetParameterAsText(2)


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



f = open(sys.path[0]+'/log/'+GDB[0:6]+'.txt','a')
start = time.clock()
time_start = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())

arcpy.env.workspace = path_result + "/" + GDB

#创建渔网
extent = getMinXY('LCA_new')
fishnet_out = 'grid'
originCoordinate = str(extent[0] - 0.025) + " " + str(extent[1] - 0.025)
yAxisCoordinate = str(extent[0]) + " " + str(extent[1] + 10)
numRows = math.ceil((extent[3] - extent[1])/0.05) + 1
numColumns=  math.ceil((extent[2] - extent[0])/0.05) + 1
arcpy.CreateFishnet_management(fishnet_out, originCoordinate, yAxisCoordinate, '0.05', '0.05', numRows, numColumns, '#', 'NO_LABELS', 'LCA_new', 'POLYGON')


layers = arcpy.ListFeatureClasses("LCA_old")
for layer in layers:
    #修改CC字段名
    filed = "CC"
    new_field_name = "CC_old"
    new_field_alias = "CC_old"
    input_feature = path_result + "/" + GDB + "/LCA_old"
    AlterField(input_feature,filed,new_field_name,new_field_alias)

    #PAC_old intersect grid
    intersectOutput = 'LCA_old_grid'
    intersect(['LCA_old','grid'],intersectOutput)

    #PAC_old intersect grid
    intersectOutput = 'LCA_new_grid'
    intersect(['LCA_new','grid'],intersectOutput)
    
    #PAC_old_grid intersect PAC_new_grid
    LCA_old = path_result + "/" + GDB + "/LCA_old_grid" 
    LCA_new = path_result + "/" + GDB + "/LCA_new_grid" 
    inFeatures = [LCA_old, LCA_new]
    intersectOutput =path_result + "/" + GDB + "/" + "LCA_intersect"
    intersect(inFeatures,intersectOutput)
    
time_end = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
end = time.clock()
f.write('2,'+time_start+','+time_end+','+str(end-start)+'\n')
f.close()
print GDB[0:6]+':Preprocess3 Finished'

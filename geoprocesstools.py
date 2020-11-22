# -*- coding: utf-8 -*-
import os,sys,arcpy
from multiprocessing import Pool



def mkdir(path):
#定义创建文件夹函数
    path = path.strip()
    path = path.strip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False
def CreateFileGDB(out,out_name):
    try:
        arcpy.CreateFileGDB_management(out, out_name)
        #print 'CreateFileGDB successful' 
    except Exception:
        print arcpy.GetMessages()    
def Copy(inFeatureClass,outFeatureClass):
    try:
        arcpy.CopyFeatures_management(inFeatureClass, outFeatureClass)
        #print 'CopyFeatures successful'
    except Exception:
        print arcpy.GetMessages()

def AddField(inFeatureClass,fieldName,fieldLength,GDB):
    try:
        arcpy.AddField_management(inFeatureClass, fieldName, "TEXT", "", "", fieldLength)
        cursor = arcpy.UpdateCursor(inFeatureClass)
        for row in cursor:
            row.setValue("PAC",GDB[0:6])
            cursor.updateRow(row)
        #print 'AddField successful'
    except Exception:
        print arcpy.GetMessages()
def AlterField(inFeatureClass,filed,new_field_name,new_field_alias):
    try:
        arcpy.AlterField_management(inFeatureClass, filed, new_field_name, new_field_alias)
        #print 'AlterField successful'
    except Exception:
        print arcpy.GetMessages()
def intersect(inFeatures,intersectOutput):
    try:
        arcpy.Intersect_analysis(inFeatures, intersectOutput, "", "", "")
        #print 'Intersect successful'
    except Exception:
        print arcpy.GetMessages()
def Erase(in_features,erase_features,out_feature_class):
    try:
        arcpy.Erase_analysis(in_features,erase_features,out_feature_class,'')
        #print 'Erase_analysis successful'
    except Exception:
        print arcpy.GetMessages()



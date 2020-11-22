# -*- coding: utf-8 -*-
import arcpy
import time,sys,os,time
from geoprocesstools import *

#输入参数
path_result = arcpy.GetParameterAsText(0)     #结果目录
GDB =arcpy.GetParameterAsText(1)              #某县GDB：110102.gdb
path_new = arcpy.GetParameterAsText(2)        #GDB目录

       
       

f = open(sys.path[0]+'/log/'+GDB[0:6]+'.txt','a')
start = time.clock()
time_start = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())

out = path_result
out_name = GDB[0:7] + "gdb"
if not arcpy.Exists(os.path.join(out,out_name)):
    CreateFileGDB(out,out_name)

arcpy.env.workspace = path_new + "/" + GDB
layers = arcpy.ListFeatureClasses("LCA")
for layer in layers:
    #复制LCA
    outFeatureClass = path_result + "/" + GDB + "/LCA_new"
    Copy(layer,outFeatureClass)
    #添加字段
    inFeatureClass = outFeatureClass
    fieldName = "PAC"
    fieldLength = 50   
    AddField(inFeatureClass,fieldName,fieldLength,GDB)
    #修改CC字段名
    inFeatureClass = outFeatureClass
    filed = "CC"
    new_field_name = "CC_new"
    new_field_alias = "CC_new"
    AlterField(inFeatureClass,filed,new_field_name,new_field_alias)
time_end = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
end = time.clock()
f.write('0,'+time_start+','+time_end+','+str(end-start)+'\n')
f.close()
print GDB[0:6]+':Preprocess1 Finished'







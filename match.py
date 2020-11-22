# -*- coding: utf-8 -*-
import os,sys,time,arcpy
from geoprocesstools import *



#arg
# # #
boua5path_old = r'E:\qxl\全国县界2016.gdb\V_BOUA52016'
boua5path_new = r'E:\qxl\V_BOUA20180705.gdb\V_BOUA5_2017'
configLyrName = "Config_2016_2017"
configTextName = "2016_2017.config"

dir_old = os.path.split(boua5path_old)[0]
dir_new = os.path.split(boua5path_new)[0]
name_old = os.path.split(boua5path_old)[1]
name_new = os.path.split(boua5path_new)[1]
print dir_old,name_old,dir_new,name_new

configData = sys.path[0] + "/configData"
mkdir(configData)
arcpy.env.overwriteOutput = True
if not arcpy.Exists(os.path.join(configData,'config.gdb')):
    CreateFileGDB(configData,'config.gdb')

arcpy.env.workspace = os.path.join(configData,'config.gdb')
# # #
Copy(os.path.join(dir_old,name_old),'BOUA5_old')
Copy(os.path.join(dir_new,name_new),'BOUA5_new')

#Erase_analysis

Erase("BOUA5_new","BOUA5_old",configLyrName)

AlterField("BOUA5_old",'PAC','PAC_old','PAC_old')

AlterField("BOUA5_new",'PAC','PAC_new','PAC_new')

AlterField(configLyrName,'PAC','PAC_old','PAC_old')

#AlterFieldValue
try:
    cursor = arcpy.UpdateCursor(configLyrName)
    for row in cursor:
        value = '-'
        row.setValue("PAC_old",value)
        row.setValue("CC",'----')
        cursor.updateRow(row)
    print 'AlterFieldValue successful'
  
except Exception:
    print arcpy.GetMessages()



#append
try:

    arcpy.Append_management(configLyrName, 'BOUA5_old', 'NO_TEST','','')
    print 'Append successful'
except:
    print arcpy.GetMessages()

   
#intersect
inFeatures = ['BOUA5_old','BOUA5_new']
out_intersect = "intersect"
intersect(inFeatures,out_intersect)



list_GDBthisyear=[]
with arcpy.da.SearchCursor(out_intersect,('PAC_new')) as cursor:
    for row in cursor:
        list_GDBthisyear.append(row[0][0:6])

dict_match = dict.fromkeys(list_GDBthisyear,'')

with arcpy.da.SearchCursor(out_intersect,('PAC_new','PAC_old','Shape_Area')) as cursor:
    for row in cursor:
        if float(row[2]) > 10e-10:
            if len(row[1])>=6:
                dict_match[row[0][0:6]]+=row[1][0:6]+','
            else:
                dict_match[row[0][0:6]]+=row[1][0:1]+','
            
f = open(sys.path[0] + "\\" + configTextName,'w+')
                                        
for key,value in dict_match.items():
    tmpstr = key+':'+value
    tmpstr = tmpstr.strip(',')
    value_wrt = str(tmpstr+'\n')    
    f.write(value_wrt)
f.close()
arcpy.Delete_management(out_intersect,"#")
arcpy.Delete_management("BOUA5_old","#")
arcpy.Delete_management("BOUA5_new","#")

print 'finish'

        


        
    
    

import os,sys,arcpy
import time
from geoprocesstools import *
from calculator import *

path_result = arcpy.GetParameterAsText(0)
path_new = arcpy.GetParameterAsText(1)


arcpy.env.overwriteOutput = True 
def checkandrepair1(path_result,path_new):
    arcpy.env.workspace = path_new
    GDBs_new = arcpy.ListFiles('*.gdb')
    
#   print "Checking whether all the data are created"   

    while 1:
        
        arcpy.env.workspace = path_result
        GDBs_result = arcpy.ListFiles('*.gdb')
        needrecreate = 0
        needrecopy = 0
        
        for GDB_new in GDBs_new:
            if GDB_new not in GDBs_result and GDB_new[-6:-4] !='00':
                needrecreate = 1

        if needrecreate == 1:            
            for GDB_new in GDBs_new:
                if GDB_new not in GDBs_result and GDB_new[-6:-4] !='00':
                    print GDB_new+': lack of GDB' 
                    outname = GDB_new
                    CreateFileGDB(path_result,outname)                   
        #print "Checking whether all the layers are copied and modified"           
        for GDB_result in GDBs_result:
            arcpy.env.workspace = path_result+'\\' + GDB_result
            layer = arcpy.ListFeatureClasses()
            if not layer:
                needrecopy = 1
        if needrecopy == 1:
            for GDB_result in GDBs_result:
                arcpy.env.workspace = path_result+'\\' + GDB_result
                layer = arcpy.ListFeatureClasses()
                if not layer:
                    f = open(sys.path[0]+'/log/'+GDB_result[0:6]+'.txt','a')
                    time_start = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
                    start = time.clock()
                    print GDB_result+': Lack of LCA_new'
                    inFeatureClass = path_new + '/'+ GDB_result +'/LCA'
                    outFeatureClass = 'LCA_new'
                    Copy(inFeatureClass,outFeatureClass)           
                    AddField(outFeatureClass,'PAC','50',GDB_result)
                    AlterField(outFeatureClass,'CC','CC_new','CC_new')
                    time_end = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
                    end = time.clock()
                    f.write('R0,'+time_start+','+time_end+','+str(end-start)+'\n')
                    f.close()
        if needrecreate == 0 and needrecopy == 0:
            break
    print 'check1 finished'
#   print "Checking finished!"
if __name__ == '__main__':
    checkandrepair1(path_result,path_new)


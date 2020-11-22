import os,sys,arcpy
import time
from geoprocesstools import *
from calculator import *

path_result = arcpy.GetParameterAsText(0)
def calc_area(path_result):
    
    arcpy.env.workspace = path_result
    GDBs_result = arcpy.ListFiles('*.gdb')
    list_txt = arcpy.ListFiles('*.txt')
    for pac in GDBs_result:
        if pac[0:6]+'.txt' not in list_txt:
            f = open(sys.path[0]+'/log/'+pac[0:6]+'.txt','a')
            start = time.clock()
            time_start = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
            print pac[0:6]+'Lack of area'
            I_path = sys.path[0] + "\\x64\\spatialoperation.exe"
            file_txt = path_result +'/'+ pac[0:6]+'.txt'
            os.system("{0} {1} {2} {3} {4} ".format(I_path,"TRANSITIONMATRIX",path_result+'/'+pac,'LCA_intersect',file_txt))
            time_end = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
            end = time.clock()
            f.write('R3,'+time_start+','+time_end+','+str(end-start)+'\n')
            f.close() 
calc_area(path_result)
print 'check4 Finished'


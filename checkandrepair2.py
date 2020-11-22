import os,sys,arcpy
import time
from geoprocesstools import *
from calculator import *

path_result = arcpy.GetParameterAsText(0)
path_old = arcpy.GetParameterAsText(1)
path_new = arcpy.GetParameterAsText(2)
year_old = arcpy.GetParameterAsText(3)
year_new = arcpy.GetParameterAsText(4)
arcpy.env.overwriteOutput = True
def checkandrepair2(path_result,path_old,path_new,year_old,year_new):
    path_match = sys.path[0] + '/' + year_old + '_' + year_new + '.config'
    appendLyr = sys.path[0] +  '\\configData\\config.gdb\\Config_' + year_old + '_' + year_new
    dictionary = read_match(path_match)
    
    arcpy.env.workspace = path_result
    GDBs_result = arcpy.ListFiles('*.gdb')
    while 1:
        needrepair = 0
        for GDB_result in GDBs_result:
            arcpy.env.workspace = path_result+'\\' + GDB_result
            layers = arcpy.ListFeatureClasses()
            if 'LCA_old' not in layers:
                needrepair = 1
        if needrepair == 1: 
            for GDB_result in GDBs_result:
                arcpy.env.workspace = path_result+'\\' + GDB_result
                clip_feature = path_new + '/' + GDB_result + '/BOUA5'
                out_feature_class = path_result + '/' + GDB_result + '/LCA_old'
                layers = arcpy.ListFeatureClasses()
                if 'LCA_old' not in layers:
                    if len(dictionary[GDB_result[0:6]].split(',')) == 1:
                        f = open(sys.path[0]+'/log/'+GDB_result[0:6]+'.txt','a')
                        start = time.clock()
                        time_start = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
                
                        if dictionary[GDB_result[0:6]].split(',')[0] <> '-':
                            in_feature = path_old + '/' + GDB_result + '/LCA'
                            arcpy.Clip_analysis(in_feature, clip_feature, out_feature_class, '')
                        else:
                            in_feature = appendLyr
                            if arcpy.Exists(in_feature):
                                arcpy.Clip_analysis(in_feature, clip_feature, out_feature_class, '')
                    
                        time_end = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
                        end = time.clock()
                        f.write('R1,'+time_start+','+time_end+','+str(end-start)+'\n')
                        f.close()
                    else:
                        f = open(sys.path[0]+'/log/'+GDB_result[0:6]+'.txt','a')
                        start = time.clock()
                        time_start = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
                        if 'merge' not in layers:
                            list_temp = []
                            for GDB in dictionary[GDB_result[0:6]].split(','):
                                if GDB <> '-':
                                    list_temp.append(os.path.normpath(path_old+'/'+GDB+'.gdb/LCA'))
                                else:
                                    if arcpy.Exists(appendLyr): 
                                        list_temp.append(appendLyr)
                            list_input = list(set(list_temp))
                            print 'Merge'+GDB_result + "start"
                            arcpy.Merge_management(list_input,path_result+'/'+ GDB_result+'/merge','')
                            print 'Merge'+GDB_result + "end"
                            arcpy.Clip_analysis(path_result+'/'+ GDB_result+'/merge', clip_feature, out_feature_class, '')
                        else:
                            arcpy.Clip_analysis(path_result+'/'+ GDB_result+'/merge', clip_feature, out_feature_class, '')
                        end = time.clock()    
                        time_end = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
                        f.write('R1,'+time_start+','+time_end+','+str(end-start)+'\n')
                        f.close()   
        else:
            break
    print 'check2 Finished'
if __name__ == '__main__':
    checkandrepair2(path_result,path_old,path_new,year_old,year_new)
                    

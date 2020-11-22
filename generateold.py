import arcpy,os,sys,time

pac_newyear = arcpy.GetParameterAsText(0)
pac_oldyear = arcpy.GetParameterAsText(1)
path_oldyear = arcpy.GetParameterAsText(2)
path_newyear = arcpy.GetParameterAsText(3)
path_result = arcpy.GetParameterAsText(4)
clip_features = arcpy.GetParameterAsText(5)
out_feature_class = arcpy.GetParameterAsText(6)
year_old = arcpy.GetParameterAsText(7)
year_new = arcpy.GetParameterAsText(8)

appendLyr = sys.path[0] +  '\\configData\\config.gdb\\Config_' + year_old + '_' + year_new
f = open(sys.path[0]+'/log/'+pac_newyear[0:6]+'.txt','a')
start = time.clock()
time_start = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())

if len(pac_oldyear.split(',')) == 1:
    if pac_oldyear.split(',')[0] <> '-':
        in_features = path_oldyear + '/'+ pac_oldyear.split(',')[0]+'.gdb/LCA'
        if arcpy.Exists(in_features):
            arcpy.Clip_analysis(in_features, clip_features, out_feature_class, '')
            print pac_newyear[0:6]+":Preprocess2 Finished"
    else:
        in_features = appendLyr
        if arcpy.Exists(in_features):
            arcpy.Clip_analysis(in_features, clip_features, out_feature_class, '')
            print pac_newyear[0:6]+":Preprocess2 Finished"
else:
    list_temp=[]
    for GDB in pac_oldyear.split(','):
        if GDB <> '-' and arcpy.Exists(os.path.normpath(path_oldyear + '/'+ GDB+'.gdb/LCA')):
            list_temp.append(os.path.normpath(path_oldyear + '/'+ GDB+'.gdb/LCA'))
        else:
            if arcpy.Exists(appendLyr):
                list_temp.append(appendLyr)
            else:
                print "xxxxxxxxxxxx"
    list_input = list(set(list_temp))
    try:
        arcpy.Merge_management(list_input,path_result+'/'+ pac_newyear+'/merge','')
        arcpy.Clip_analysis(path_result+'/'+ pac_newyear+'/merge', clip_features, out_feature_class, '')
        print pac_newyear[0:6]+":Preprocess2 Finished"
    except Exception:
        print arcpy.GetMessages()
        
time_end = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
end = time.clock()
f.write('1,'+time_start+','+time_end+','+str(end-start)+'\n')
f.close()

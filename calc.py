# -*- coding: utf-8 -*-
import arcpy,sys,os,time


result_path = arcpy.GetParameterAsText(0)
GDB = arcpy.GetParameterAsText(1)

f = open(sys.path[0]+'/log/'+GDB[0:6]+'.txt','a')
start = time.clock()
time_start = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())



#calc area
path=result_path + "\\" + GDB

arcpy.env.workspace = os.path.normpath(result_path + "/" + GDB)
file_txt = result_path + "/" + GDB[0:6] + ".txt"
I_path = sys.path[0] + "\\x64\\spatialoperation.exe"
os.popen("{0} {1} {2} {3} {4} ".format(I_path,"TRANSITIONMATRIX",result_path + "/" + GDB,'LCA_intersect',file_txt))
time_end = time.strftime("%Y-%m-%d#%H:%M:%S",time.localtime())
end = time.clock()
f.write('3,'+time_start+','+time_end+','+str(end-start)+'\n')
f.close()

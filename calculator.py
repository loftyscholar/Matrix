# -*- coding: UTF-8 -*-

import Tkinter,os,sys,time,thread,glob
import tkFileDialog,tkMessageBox
from multiprocessing import Pool
from exportMatrix import *



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

def delete_resultandlog(result_path,path_new):
    if path_new[-4:] != '.gdb':
        result_path = os.path.normpath(result_path)
        log_path = os.path.normpath(sys.path[0] + '\\log')
        if os.path.exists(log_path):
            os.system('rd \"{0}\" /s /q'.format(log_path))
            print "log delete"
        if os.path.exists(result_path):
            os.system('rd \"{0}\" /s /q'.format(result_path))
            print "result delete"
    else:
        gdbname = path_new[-10:-4]
        change_path = os.path.join(result_path,gdbname + '.txt')
        result_path = os.path.join(result_path,gdbname + '.gdb')
        log_path = os.path.join(sys.path[0],'log',gdbname + '.txt')
        if os.path.exists(log_path):
            os.remove(log_path)
            print "log delete"
        if os.path.exists(change_path):
            os.remove(change_path)
        if os.path.exists(result_path):
            os.system('rd \"{0}\" /s /q'.format(result_path))
            print "result delete"


def write_pathfile(pathOld,pathNew):
    if "/" in pathOld:
        l_pathOld = pathOld.split('/')
        l_pathOld.pop()
        pathOld = "\\".join(l_pathOld)
    else:
        l_pathOld = pathOld.split('\\')
        l_pathOld.pop()
        pathOld = "\\".join(l_pathOld)

    if pathNew[-4:] != '.gdb':
        if "/" in pathNew:
            l_pathNew = pathNew.split('/')
            l_pathNew.pop()
            pathNew = "\\".join(l_pathNew)
        else:
            l_pathNew = pathNew.split('\\')
            l_pathNew.pop()
            pathNew = "\\".join(l_pathNew)
    else:
        if "/" in pathNew:
            l_pathNew = pathNew.split('/')
            l_pathNew.pop()
            l_pathNew.pop()
            pathNew = "\\".join(l_pathNew)
        else:
            l_pathNew = pathNew.split('\\')
            l_pathNew.pop()
            l_pathNew.pop()
            pathNew = "\\".join(l_pathNew)
     
    list_path = sys.path[0].split("\\")
    list_path.pop()
    path = "/".join(list_path)
    
    f = open(os.path.normpath(path + '\\FilePath.txt'),'r')
    lst_line = []
    for line in f.readlines():
        lst_line.append(line.split(',')[0])
    yearNew = lst_line[0]
    yearOld = lst_line[1]
    f.close()

    str = yearNew + "," + pathNew + '\n' + yearOld + "," + pathOld + '\n'
    
    f = open(os.path.normpath(path + '\\FilePath.txt'),'w')
    f.write(str)
    f.close()


def read_match(path_match):
    f = open(path_match,'r')
    list_key = []
    list_value = []
    dictionary = {}
    for line in f.readlines():
        list_key.append(line.strip('\n').split(':')[0])
        list_value.append(line.strip('\n').split(':')[1])
    dictionary = dict(zip(list_key,list_value))
    return dictionary

def preprocess1(path_result,GDB,path_new):
    #调用preprocess1.py
    path_py = sys.path[0]+"/preprocess1.pyc"        
    os.popen("python {0} {1} {2} {3}".format(path_py,path_result,GDB,path_new))

def generateold(pac_newyear,pac_oldyear,path_oldyear,path_newyear,path_result,clip_features,out_feature_class,year_old,year_new):
    path_py = os.path.normpath(sys.path[0]+ '/generateold.pyc')
    os.popen('python {0} {1} {2} {3} {4} {5} {6} {7} {8} {9}'.format(path_py,pac_newyear,pac_oldyear,path_oldyear,path_newyear,path_result,clip_features,out_feature_class,year_old,year_new))

def preprocess2(path_result,GDB,path_old):
    path_py = sys.path[0]+"/preprocess2.pyc"        
    os.popen("python {0} {1} {2} {3}".format(path_py,path_result,GDB,path_old))

def calc(result_path,GDB):
    path_py = os.path.normpath(sys.path[0]+"/calc.pyc")
    os.popen("python {0} {1} {2}".format(path_py,result_path,GDB))
    

 #本期数据预处理    
def procedure1(path_new,path_result):

    gdbname = ''
    if path_new[-4:] == '.gdb':
        path_new_1 = path_new[0:-10]
        gdbname = path_new[-10:] 
    else:
        path_new_1 = path_new
 
    p1 = Pool()
    if gdbname == '':
        GDBs = os.listdir(path_new_1)
        for GDB in GDBs:
            if GDB[-3:]=='gdb' and GDB[-6:-4] != '00':
                p1.apply_async(preprocess1, args=(path_result,GDB,path_new_1))
    else:
        p1.apply_async(preprocess1, args=(path_result,gdbname,path_new_1))
    p1.close()
    p1.join()

#上期数据预处理
def procedure2(year_old,year_new,path_oldyear,path_newyear,path_result):
    gdbname = ''
    if path_newyear[-4:] == '.gdb':
        path_new_1 = path_newyear[0:-10]
        gdbname = path_newyear[-10:]
    else:
        path_new_1 = path_newyear
        
    p = Pool()
    configName = year_old + "_" + year_new + ".config"
    path_match = sys.path[0] + '/' + configName
    dictionary = read_match(path_match)
#取到新数据集pac列表
    newpaclist = os.listdir(path_result)
    if gdbname == '':
        for key in newpaclist:
            value = dictionary[key[0:6]]
            clip_features = os.path.normpath(path_new_1 + '/' + key +'/BOUA5')
        
            out_feature_class = os.path.normpath(path_result+ '/' + key +'/LCA_old')
            p.apply_async(generateold, args=(key,value,path_oldyear,path_new_1,path_result,clip_features,out_feature_class,year_old,year_new))
    else:
        value = dictionary[gdbname[0:6]]
        clip_features = os.path.normpath(path_new_1 + '/' + gdbname +'/BOUA5')
        
        out_feature_class = os.path.normpath(path_result+ '/' + gdbname +'/LCA_old')
        p.apply_async(generateold, args=(gdbname,value,path_oldyear,path_new_1,path_result,clip_features,out_feature_class,year_old,year_new))
                
    p.close()
    p.join()

        
    
#两期数据联合处理
def procedure3(path_lastyear,path_output,path_thisyear):
    gdbname = ''
    if path_thisyear[-4:] == '.gdb':
        gdbname = path_thisyear[-10:]
    p2 = Pool()
    GDBs = os.listdir(path_output)
    if gdbname == '':
        for GDB in GDBs:
            p2.apply_async(preprocess2, args=(path_output,GDB,path_lastyear))
    else:
        p2.apply_async(preprocess2, args=(path_output,gdbname,path_lastyear))
    p2.close()
    p2.join()

#计算面积
def areacalculator(path_result,path_newyear):
    gdbname = ''
    if path_newyear[-4:] == '.gdb':
        gdbname = path_newyear[-10:]
    p3 = Pool()
    if gdbname == '':
        GDBs = os.listdir(path_result)   
        for GDB in GDBs:
            if GDB[-3:] == "gdb":
                p3.apply_async(calc, args=(path_result,GDB))
    else:
        p3.apply_async(calc, args=(path_result,gdbname))
    p3.close()
    p3.join()




def calculator(year_old,year_new,path_old,path_new,result_path,path_result,window):
    #result_path temp 路径
    #path_result 最终结果路径
    if path_new[-4:] != '.gdb':
        start = time.clock()
        os.popen("reg add \"HKEY_CURRENT_USER\Software\Microsoft\Windows\Windows Error Reporting\" /v DontShowUI /t REG_DWORD /d 1 /f")
        delete_resultandlog(result_path,path_new)
        write_pathfile(path_old,path_new)
        mkdir(result_path)
        mkdir(path_result)
        mkdir(os.path.normpath(sys.path[0]+'/log'))
        procedure1(path_new,result_path)

        print 'Start repairing of procedure1'
        path_check1 = os.path.normpath(sys.path[0]+'/checkandrepair1.pyc')
        os.popen('python {0} {1} {2}'.format(path_check1,result_path,path_new))
        print 'repairing of procedure1 finished'
        
        procedure2(year_old,year_new,path_old,path_new,result_path)
        print 'Start repairing of procedure2'
        path_check2 = os.path.normpath(sys.path[0]+'/checkandrepair2.pyc')
        os.popen('python {0} {1} {2} {3} {4} {5}'.format(path_check2,result_path,path_old,path_new,year_old,year_new))
        print 'repairing of procedure2 finished'
        
        procedure3(path_old,result_path,path_new)
        print 'Start repairing of procedure3'
        path_check3 = os.path.normpath(sys.path[0]+'/checkandrepair3.pyc')
        os.popen('python {0} {1}'.format(path_check3,result_path))
        print 'repairing of procedure3 finished'
        
        areacalculator(result_path,path_new)
        print 'Start repairing of procedure4'
        path_check4 = os.path.normpath(sys.path[0]+'/checkandrepair4.pyc')
        os.popen('python {0} {1}'.format(path_check4,result_path))
        print 'repairing of procedure4 finished'
        out_matrix = path_result + "\\" + year_new + "VS" + year_old
        mkdir(out_matrix)
        collect_province(result_path,out_matrix)
        collect_city(result_path,out_matrix)
        collect_county(result_path,out_matrix)
        window.destroy()
        

        os.popen("reg add \"HKEY_CURRENT_USER\Software\Microsoft\Windows\Windows Error Reporting\" /v DontShowUI /t REG_DWORD /d 0 /f")
        print time.clock()-start
    else:
        start = time.clock()
        os.popen("reg add \"HKEY_CURRENT_USER\Software\Microsoft\Windows\Windows Error Reporting\" /v DontShowUI /t REG_DWORD /d 1 /f")
        delete_resultandlog(result_path,path_new)
        write_pathfile(path_old,path_new)
        mkdir(result_path)
        mkdir(path_result)
        mkdir(os.path.normpath(sys.path[0]+'/log'))
        procedure1(path_new,result_path)
        procedure2(year_old,year_new,path_old,path_new,result_path)
        procedure3(path_old,result_path,path_new)
       
        areacalculator(result_path,path_new)
        out_matrix = path_result + "\\" + year_new + "VS" + year_old
        mkdir(out_matrix)
        collect_province(result_path,out_matrix)
        collect_city(result_path,out_matrix)
        collect_county(result_path,out_matrix)
        window.destroy()
        

        os.popen("reg add \"HKEY_CURRENT_USER\Software\Microsoft\Windows\Windows Error Reporting\" /v DontShowUI /t REG_DWORD /d 0 /f")
        print time.clock()-start

        
    


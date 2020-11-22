# -*- coding: utf-8 -*-


import Tkinter,os,sys,time,glob,sqlite3,ttk
import tkFileDialog,tkMessageBox
from multiprocessing import Pool
from calculator import *


def progressupdate(var_preprocess1,var_preprocess2,var_preprocess3,var_preprocess4,var_new):
    btn_disabledOractive('disabled')
    new_path = var_new.get()
    if new_path[-4:] != '.gdb':
        num_total = len(glob.glob(new_path+'/*.gdb'))
        num_00 = len(glob.glob(new_path+'/*00.gdb'))
        num_total -= num_00
        while True:    
            time.sleep(5)        
            progress_dic = {}
            for key in glob.glob(new_path+'/*.gdb'):
                progress_dic[key[-10:-4]] = [None]*4
            path_log = os.path.normpath(sys.path[0]+'/log')
            if os.path.exists(path_log):
                for txt_log in os.listdir(path_log):
                    f_log = open(os.path.normpath(path_log + '/'+txt_log),'r')
                    for p,l in enumerate(f_log.readlines()):
                        list_l = l.split(',')
                        progress_dic[f_log.name[-10:-4]][p]=list_l[3].strip('\n')
                num_preprocess1 = 0
                num_preprocess2 = 0
                num_preprocess3 = 0
                num_preprocess4 = 0
                for value_list in progress_dic.values():
                    if value_list[0] != None:
                        num_preprocess1 +=1
                    if value_list[1] != None:
                        num_preprocess2 +=1
                    if value_list[2] != None:
                        num_preprocess3 +=1
                    if value_list[3] != None:
                        num_preprocess4 +=1
                var_preprocess1.set('数据创建:'+str(round(num_preprocess1 * 100./num_total,1)) + '%')
                var_preprocess2.set('拼接裁切:'+str(round(num_preprocess2 * 100./num_total,1)) + '%')
                var_preprocess3.set('匹配分析:'+str(round(num_preprocess3 * 100./num_total,1)) + '%')
                var_preprocess4.set('矩阵计算:'+str(round(num_preprocess4 * 100./num_total,1)) + '%')
                if num_preprocess4 == num_total:
                    break
    else:
        gdbname = new_path[-10:-4]
        while True:
            time.sleep(5)
            progress_dic = {}
            progress_dic[gdbname] = [None]*4
            txt_log = os.path.join(sys.path[0],'log',gdbname + '.txt')
            if os.path.exists(txt_log):
                f_log = open(txt_log,'r')
                for p,l in enumerate(f_log.readlines()):
                    list_l = l.split(',')
                    progress_dic[f_log.name[-10:-4]][p] = list_l[3].strip('\n')
                num_preprocess1 = 0
                num_preprocess2 = 0
                num_preprocess3 = 0
                num_preprocess4 = 0
                for value_list in progress_dic.values():
                    if value_list[0] != None:
                        num_preprocess1 +=1
                    if value_list[1] != None:
                        num_preprocess2 +=1
                    if value_list[2] != None:
                        num_preprocess3 +=1
                    if value_list[3] != None:
                        num_preprocess4 +=1
                var_preprocess1.set('数据创建:'+str(round(num_preprocess1 * 100./1,1)) + '%')
                var_preprocess2.set('拼接裁切:'+str(round(num_preprocess2 * 100./1,1)) + '%')
                var_preprocess3.set('匹配分析:'+str(round(num_preprocess3 * 100./1,1)) + '%')
                var_preprocess4.set('矩阵计算:'+str(round(num_preprocess4 * 100./1,1)) + '%')
                if num_preprocess4 == 1:
                    break
                    
    btn_disabledOractive('active')
    
    

#######
def read_pathfile(pathOld,pathNew,pathResult):
    l_path = []
    l_year = []
    list_path = sys.path[0].split("\\")
    list_path.pop()
    path = "/".join(list_path)
    if os.path.exists(os.path.normpath(path + '\\FilePath.txt')):
        f = open(os.path.normpath(path + '\\FilePath.txt'),'r')
        for line in f.readlines():
            line = line.strip('\n')
            l_year.append(line.split(',')[0])
            l_path.append(line.split(',')[1])
        pathOld.set(os.path.normpath(l_path[1] + "\\GDB"))
        pathNew.set(os.path.normpath(l_path[0] + "\\GDB"))
        pathResult.set(sys.path[0])
        f.close()
        return l_year
        
        

def thread_calc(year_old,year_new,var_old,var_new,var_result,var_preprocess1,var_preprocess2,var_preprocess3,var_preprocess4,window):
    path_old = var_old.get()
    path_new = var_new.get()
    result_path = var_result.get() + "/temp"  #temp路径
    path_result = var_result.get() + "/Result" #最终结果路径
    if (not os.path.exists(path_old)) or (not os.path.exists(path_new)):
        tkMessageBox.showwarning(title = "提示",message = "您输入的路径不存在")
    else:
        if (not os.listdir(path_old)) or (not os.listdir(path_new)):
            tkMessageBox.showwarning(title = "提示",message = "您输入的路径为空")
        else:
            thread.start_new_thread(calculator,(year_old,year_new,path_old,path_new,result_path,path_result,window))
            thread.start_new_thread(progressupdate,(var_preprocess1,var_preprocess2,var_preprocess3,var_preprocess4,var_new))   
def select_folder(x):
    #功能：选择文件目录。参数：目录赋值的对象
    global file_path
    file_path=tkFileDialog.askdirectory(title = "选择文件目录")
    if file_path:
        x.set(os.path.normpath(file_path))

def delete_resultandlog(var_result):
    result_path = os.path.normpath(var_result.get() + '\\temp')
    log_path = os.path.normpath(sys.path[0] + '\\log')
    if os.path.exists(result_path):
        os.system('rd \"{0}\" /s /q'.format(result_path))
        print "result delete"
    if os.path.exists(log_path):
        os.system('rd \"{0}\" /s /q'.format(log_path))
        print "log delete" 

    
def btn_disabledOractive(mark):
    if mark == 'disabled':
    #按钮失效
        button_old.config(state='disabled')
        button_new.config(state='disabled')
        button_result.config(state='disabled')
        button_calculator.config(state='disabled')
    #按钮恢复
    elif mark == 'active':
        button_old.config(state='active')
        button_new.config(state='active')
        button_result.config(state='active')
        button_calculator.config(state='active')
def creat_UI():
    global window
    global text_interactive
    
    window = Tkinter.Tk()
    window.title("地理国情地表覆盖转移矩阵计算")
    window.geometry('600x300')
    window.resizable(False,False)
    var_old = Tkinter.StringVar(window)
    fm1 = Tkinter.Frame(window)
    label_old = Tkinter.Label(fm1,font=('Fixdsys',12,'bold'),text="往期数据",fg = 'black')
    label_old.place(relx = 0.02,rely = 0.1,relwidth =0.15,relheight = 0.22)
    entry_old = Tkinter.Entry(fm1,textvariable=var_old)
    entry_old.place(relx = 0.2 ,rely = 0.1 ,relwidth = 0.6 ,relheight = 0.22)
    global button_old
    button_old = Tkinter.Button(fm1,text="...",command=lambda:select_folder(var_old),bd = 4)
    button_old.place(relx = 0.84 ,rely = 0.1 ,relwidth = 0.12 ,relheight = 0.22)

    var_new = Tkinter.StringVar(window)
    label_new = Tkinter.Label(fm1,font=('Fixdsys',12,'bold'),text="本期数据",fg = 'black')
    label_new.place(relx = 0.02 ,rely = 0.38 ,relwidth = 0.15 ,relheight = 0.22)
    entry_new = Tkinter.Entry(fm1,textvariable=var_new)
    entry_new.place(relx = 0.2 ,rely = 0.38 ,relwidth = 0.6 ,relheight = 0.22)
    global button_new
    button_new = Tkinter.Button(fm1,text="...",command=lambda:select_folder(var_new),bd = 4)
    button_new.place(relx = 0.84 ,rely = 0.38 ,relwidth = 0.12 ,relheight = 0.22)

    var_result = Tkinter.StringVar(window)
    label_result = Tkinter.Label(fm1,font=('Fixdsys',12,'bold'),text="结果位置",fg = 'black')
    label_result.place(relx = 0.02 ,rely = 0.66 ,relwidth = 0.15 ,relheight = 0.22)
    entry_result = Tkinter.Entry(fm1,textvariable=var_result)
    entry_result.place(relx = 0.2 ,rely = 0.66 ,relwidth = 0.6 ,relheight = 0.22)
    global button_result
    button_result = Tkinter.Button(fm1,text="...",command=lambda:select_folder(var_result),bd = 4)
    button_result.place(relx = 0.84 ,rely = 0.66 ,relwidth = 0.12 ,relheight = 0.22)

    fm1.place(relx =0 ,rely = 0, relwidth =1 , relheight = 0.55)
    
    fm2 = Tkinter.Frame(window)
    var_preprocess1 = Tkinter.StringVar()
    var_preprocess1.set('数据创建:')
    label_preprocess1 = Tkinter.Label(fm2,font=('Fixdsys',12,'bold'),textvariable = var_preprocess1)
    label_preprocess1.place(relx = 0.02 ,rely = 0.3 )
    
    var_preprocess2 = Tkinter.StringVar()
    var_preprocess2.set('拼接裁切:')
    label_preprocess2 = Tkinter.Label(fm2,font=('Fixdsys',12,'bold'),textvariable = var_preprocess2)
    label_preprocess2.place(relx = 0.27 ,rely = 0.3 ) 

    var_preprocess3 = Tkinter.StringVar()
    var_preprocess3.set('匹配分析:')
    label_preprocess3 = Tkinter.Label(fm2,font=('Fixdsys',12,'bold'),textvariable = var_preprocess3)
    label_preprocess3.place(relx = 0.52 ,rely = 0.3 ) 

    var_preprocess4 = Tkinter.StringVar()
    var_preprocess4.set('矩阵计算:')
    label_preprocess4 = Tkinter.Label(fm2,font=('Fixdsys',12,'bold'),textvariable = var_preprocess4)
    label_preprocess4.place(relx = 0.77 ,rely = 0.3 ) 

    fm2.place(relx = 0,rely = 0.55 , relwidth = 1,relheight = 0.25)

    fm3 = Tkinter.Frame(window)
    global button_calculator
    button_calculator = Tkinter.Button(fm3,text="计算",command=lambda:thread_calc(year_old,year_new,var_old,var_new,var_result,var_preprocess1,var_preprocess2,var_preprocess3,var_preprocess4,window),font = ('MS Sans Serif',12,'bold'),state = 'active',relief = 'ridge',bd = 4)
    button_calculator.place(relx = 0.68,rely = 0.1,relheight = 0.8,relwidth = 0.30)



    fm3.place(relx = 0,rely = 0.8,relwidth = 1 , relheight = 0.2)
    l_year = read_pathfile(var_old,var_new,var_result)
    year_new = l_year[0]
    year_old = l_year[1]
    window.mainloop()
    

##if __name__ == "__main__":
##    creat_UI()
    

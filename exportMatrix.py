# -*- coding: utf-8 -*-


import os,sys,glob,math
from decimal import Decimal
from decimal import getcontext
dict_ccName = {}
dic_cc2015_cc2017 = {}
f = open(os.path.normpath(sys.path[0] +'\ccName.txt'))
for line in f.readlines():
    l_line = line.strip('\n').split(',')
    dict_ccName[l_line[0]] = l_line[1]
f.close()



f = open(os.path.normpath(sys.path[0] +'\cc2015-2017.txt'))
for line in f.readlines():
    l_line = line.strip('\n').split(',')
    dic_cc2015_cc2017[l_line[0]] = l_line[1]
f.close()


def get_dicOneLevelMatrix(pac,var_temp):
    global list_cc
    list_cc = []
    dict_matrixProvince = {}
    for f_matrix in glob.glob(os.path.normpath(var_temp + '\\{}.txt'.format(pac))):
        f = open(f_matrix,'r')
        for line in f.readlines():
            if 'PAC' in line:
                continue
            else:
                list_line = line.strip('\n').split(',')
                cc_2015 = dic_cc2015_cc2017.get(list_line[1][0:4],list_line[1])
                cc_2017 = dic_cc2015_cc2017.get(list_line[2][0:4],list_line[2])
                cc_2015 = cc_2015[0:2] + '00'
                cc_2017 = cc_2017[0:2] + '00'
                if cc_2015 + '_' + cc_2017 in dict_matrixProvince.keys():
                    dict_matrixProvince[cc_2015 +'_'+cc_2017] = Decimal(dict_matrixProvince[cc_2015+'_'+cc_2017]) + Decimal(list_line[3])
                else:
                    dict_matrixProvince[cc_2015+'_'+cc_2017] = Decimal(list_line[3])
                list_cc.append(cc_2015)
                list_cc.append(cc_2017)    
        f.close()
    list_cc = sorted(list(set(list_cc)))
    if '--00' in list_cc:
        list_cc.remove('--00')
        list_cc.append('--00')
    return dict_matrixProvince

def get_dicThreeLevelMatrix(pac,var_temp):
    global list_cc
    list_cc = []
    dict_Matrix = {}
    #dic_cc2015_cc2017 = query('select cc_2015,cc_2017 from match')
    ##
    for f_matrix in glob.glob(os.path.normpath(var_temp + '\\{}.txt'.format(pac))):
        f = open(f_matrix,'r')
        for line in f.readlines():
            if 'PAC' in line:
                continue
            else:
                list_line = line.strip('\n').split(',')
                cc_2015 = dic_cc2015_cc2017.get(list_line[1][0:4],list_line[1])
                cc_2017 = dic_cc2015_cc2017.get(list_line[2][0:4],list_line[2])   
                if cc_2015+'_'+cc_2017 in dict_Matrix.keys():
                    dict_Matrix[cc_2015+'_'+cc_2017] = Decimal(dict_Matrix[cc_2015+'_'+cc_2017]) + Decimal(list_line[3])
                else:
                    dict_Matrix[cc_2015+'_'+cc_2017] = Decimal(list_line[3])
                list_cc.append(cc_2015)
                list_cc.append(cc_2017)         
        f.close()
    list_cc = sorted(list(set(list_cc)))
    if '----' in list_cc:
        list_cc.remove('----')
        list_cc.append('----')
    return dict_Matrix

def write_ToTxt_county_oneLevel(List_CcLevel,pac,out_path,dict_Matrix):
    increment = {}
    total_col = {}
    f = open(out_path+'\\'+pac+'_1'+'.txt','w')
    line_1 = "分类"  
    for cc in List_CcLevel:
        line_1 += "," + dict_ccName.get(cc[0:4],cc)
    line_1 += ",总计,转出量\n"    
    f.write(line_1)
    for v1 in  List_CcLevel:
        decrement = 0
        increment[v1] = 0
        total_row = 0
        total_col[v1] = 0
        f.write(dict_ccName.get(v1[0:4],v1))
        for v2 in  List_CcLevel:
            if v1 +'_'+ v2 in dict_Matrix.keys():
                f.write(',' +str(dict_Matrix[v1 +'_'+ v2]))
            else:
                f.write(',')
            if v1 != v2:
                increment[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
                decrement += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            total_row += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            total_col[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
        f.write(',' + str(total_row) + ',' + str(decrement) + '\n')
    f.write("总计")
    for cc in List_CcLevel:
        f.write(',' + str(total_col[cc]))
    f.write(',' + str(sum(total_col.values())))
    f.write('\n')
    
    f.write("转入量")
    for cc in List_CcLevel:
        f.write(',' + str(increment[cc]))
    f.write('\n')
    f.close()
def write_ToTxt_county_twoLevel(List_CcLevel,pac,out_path,dict_Matrix):
    increment = {}
    total_col = {}
    f = open(out_path+'\\'+pac+'_2'+'.txt','w')
    #dict_ccName = query1('select CcCode,Name from TLayerCode')
    line_1 = "分类"  
    for cc in List_CcLevel:
        line_1 += "," + dict_ccName.get(cc[0:4],cc)
    line_1 += ",总计,转出量\n"
    f.write(line_1)
    for v1 in  List_CcLevel:
        decrement = 0
        increment[v1] = 0
        total_row = 0
        total_col[v1] = 0
        f.write(dict_ccName.get(v1[0:4],v1))
        for v2 in List_CcLevel:
            total_row += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            total_col[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
            if v1 != v2:
                increment[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
                decrement += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            if v1 +'_'+ v2 in dict_Matrix.keys():
                f.write(',' +str(dict_Matrix[v1 +'_'+ v2]))
            else:
                f.write(',')
        f.write(',' + str(total_row) + ',' + str(decrement) + '\n')

    f.write("总计")
    for cc in List_CcLevel:
        f.write(',' + str(total_col[cc]))
    f.write(',' + str(sum(total_col.values())))
    f.write('\n')
    
    f.write("转入量")
    for cc in List_CcLevel:
        f.write(',' + str(increment[cc]))
    f.write('\n')
    f.close()

def write_ToTxt_county_threeLevel(List_CcLevel,pac,out_path,dict_Matrix):
    increment = {}
    total_col = {}
    f = open(out_path+'\\'+pac+'_3'+'.txt','w')
    #dict_ccName = query1('select CcCode,Name from TLayerCode')
    line_1 = "分类"  
    for cc in List_CcLevel:
        line_1 += "," + dict_ccName.get(cc[0:4],cc)
    line_1 += ",总计,转出量\n"
    f.write(line_1)
    for v1 in List_CcLevel:
        decrement = 0
        increment[v1] = 0
        total_row = 0
        total_col[v1] = 0
        f.write(dict_ccName.get(v1[0:4],v1))
        for v2 in List_CcLevel:
            total_row += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            total_col[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
            if v1 != v2:
                increment[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
                decrement += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            if v1 +'_'+ v2 in dict_Matrix.keys():
                f.write(',' +str(dict_Matrix[v1 +'_'+ v2]))
            else:
                f.write(',')
        f.write(',' + str(total_row) + ',' + str(decrement) + '\n')

    f.write("总计")
    for cc in List_CcLevel:
        f.write(',' + str(total_col[cc]))
    f.write(',' + str(sum(total_col.values())))
    f.write('\n')
        
    f.write("转入量")
    for cc in List_CcLevel:
        f.write(',' + str(increment[cc]))
    f.write('\n')
    f.close()
def write_ToTxt_city_oneLevel(List_CcLevel,pac,out_path,dict_Matrix):
    increment = {}
    total_col = {}
    f = open(out_path+'\\'+pac[0:4]+'00_1.txt','w')
    #dict_ccName = query1('select CcCode,Name from TLayerCode')
    line_1 = "分类"  
    for cc in List_CcLevel:
        line_1 += "," + dict_ccName.get(cc[0:4],cc)
    line_1 += ",总计,转出量\n"
    f.write(line_1)
    for v1 in List_CcLevel:
        decrement = 0
        increment[v1] = 0
        total_row = 0
        total_col[v1] = 0
        f.write(dict_ccName.get(v1[0:4],v1))
        for v2 in List_CcLevel:
            total_row += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            total_col[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
            if v1 != v2:
                increment[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
                decrement += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            if v1 +'_'+ v2 in dict_Matrix.keys():
                f.write(',' +str(dict_Matrix[v1 +'_'+ v2]))
            else:
                f.write(',')
        f.write(',' + str(total_row) + ',' + str(decrement) + '\n')

    f.write("总计")
    for cc in List_CcLevel:
        f.write(',' + str(total_col[cc]))
    f.write(',' + str(sum(total_col.values())))
    f.write('\n')
        
    f.write("转入量")
    for cc in List_CcLevel:
        f.write(',' + str(increment[cc]))
    f.write('\n')
    f.close()
def write_ToTxt_city_twoLevel(List_CcLevel,pac,out_path,dict_Matrix):
    increment = {}
    total_col = {}
    f = open(out_path+'\\'+pac[0:4]+'00_2.txt','w')
    #dict_ccName = query1('select CcCode,Name from TLayerCode')
    line_1 = "分类"   
    for cc in List_CcLevel:
        line_1 += "," + dict_ccName.get(cc[0:4],cc)
    line_1 += ",总计,转出量\n"
    f.write(line_1)
    for v1 in List_CcLevel:
        decrement = 0
        increment[v1] = 0
        total_row = 0
        total_col[v1] = 0
        f.write(dict_ccName.get(v1[0:4],v1))
        for v2 in List_CcLevel:
            total_row += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            total_col[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
            if v1 != v2:
                increment[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
                decrement += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            if v1 +'_'+ v2 in dict_Matrix.keys():
                f.write(',' +str(dict_Matrix[v1 +'_'+ v2]))
            else:
                f.write(',')
        f.write(','+ str(total_row) + ',' + str(decrement) + '\n')

    f.write("总计")
    for cc in List_CcLevel:
        f.write(',' + str(total_col[cc]))
    f.write(',' + str(sum(total_col.values())))
    f.write('\n')
        
    f.write("转入量")
    for cc in List_CcLevel:
        f.write(',' + str(increment[cc]))
    f.write('\n')
    f.close()


def write_ToTxt_city_threeLevel(List_CcLevel,pac,out_path,dict_Matrix):
    increment = {}
    total_col = {}
    f = open(out_path+'\\'+pac[0:4]+'00_3.txt','w')
    #dict_ccName = query1('select CcCode,Name from TLayerCode')
    line_1 = "分类" 
    for cc in List_CcLevel:
        line_1 += "," + dict_ccName.get(cc[0:4],cc)
    line_1 += ",总计,转出量\n"
    f.write(line_1)
    for v1 in List_CcLevel:
        decrement = 0
        increment[v1] = 0
        total_row = 0
        total_col[v1] = 0
        f.write(dict_ccName.get(v1[0:4],v1))
        for v2 in List_CcLevel:
            total_row += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            total_col[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
            if v1 != v2:
                increment[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
                decrement += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            if v1 +'_'+ v2 in dict_Matrix.keys():
                f.write(',' +str(dict_Matrix[v1 +'_'+ v2]))
            else:
                f.write(',')
        f.write(',' + str(total_row) + ',' + str(decrement) + '\n')

    f.write("总计")
    for cc in List_CcLevel:
        f.write(',' + str(total_col[cc]))
    f.write(',' + str(sum(total_col.values())))
    f.write('\n')
        
    f.write("转入量")
    for cc in List_CcLevel:
        f.write(',' + str(increment[cc]))
    f.write('\n')
    f.close()

def write_ToTxt_province_oneLevel(List_CcLevel,pac,out_path,dict_Matrix):
    increment = {}
    total_col = {}
    f = open(out_path+'\\'+pac[0:2]+'0000_1.txt','w')
    line_1 = "分类"
    for cc in List_CcLevel:        
        line_1 += "," + dict_ccName.get(cc[0:4],cc)
    line_1 += ",总计,转出量\n"
    f.write(line_1)
    for v1 in List_CcLevel:
        decrement = 0
        increment[v1] = 0
        total_row = 0
        total_col[v1] = 0
        f.write(dict_ccName.get(v1[0:4],v1))
        for v2  in List_CcLevel:
            total_row += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            total_col[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
            if v1 != v2:
                increment[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
                decrement += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            if v1 +'_'+ v2 in dict_Matrix.keys():
                f.write(',' +str(dict_Matrix[v1 +'_'+ v2]))
            else:
                f.write(',')
        f.write(',' + str(total_row) + ',' + str(decrement) + '\n')

    f.write("总计")
    for cc in List_CcLevel:
        f.write(',' + str(total_col[cc]))
    f.write(',' + str(sum(total_col.values())))
    f.write('\n')
        
    f.write("转入量")
    for cc in List_CcLevel:
        f.write(',' + str(increment[cc]))
    f.write('\n')
    f.close()

def write_ToTxt_province_twoLevel(List_CcLevel,pac,out_path,dict_Matrix):
    increment = {}
    total_col = {}
    f = open(out_path+'\\'+pac[0:2]+'0000_2.txt','w')
    line_1 = "分类"
    for cc in List_CcLevel:
        line_1 += "," + dict_ccName.get(cc[0:4],cc)
    line_1 += ",总计,转出量\n"
    f.write(line_1)
    for v1 in List_CcLevel:
        decrement = 0
        increment[v1] = 0
        total_row = 0
        total_col[v1] = 0
        f.write(dict_ccName.get(v1[0:4],v1))
        for v2 in List_CcLevel:
            total_row += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            total_col[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
            if v1 != v2:
                increment[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
                decrement += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            if v1 +'_'+ v2 in dict_Matrix.keys():
                f.write(',' +str(dict_Matrix[v1 +'_'+ v2]))
            else:
                f.write(',')
        f.write(',' + str(total_row) + ',' + str(decrement) + '\n')

    f.write("总计")
    for cc in List_CcLevel:
        f.write(',' + str(total_col[cc]))
    f.write(',' + str(sum(total_col.values())))
    f.write('\n')
        
    f.write("转入量")
    for cc in List_CcLevel:
        f.write(',' + str(increment[cc]))
    f.write('\n')
    f.close()

def write_ToTxt_province_threeLevel(List_CcLevel,pac,out_path,dict_Matrix):
    increment = {}
    total_col = {}
    f = open(out_path+'\\'+pac[0:2]+'0000_3.txt','w')
    line_1 = "分类"
    for cc in List_CcLevel:
        line_1 += "," + dict_ccName.get(cc[0:4],cc)
    line_1 += ",总计,转出量\n"
    f.write(line_1)
    for v1 in List_CcLevel:
        decrement = 0
        increment[v1] = 0
        total_row = 0
        total_col[v1] = 0
        f.write(dict_ccName.get(v1[0:4],v1))
        for v2 in List_CcLevel:
            total_row += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            total_col[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
            if v1 != v2:
                increment[v1] += Decimal(dict_Matrix.get(v2 + '_' + v1,'0'))
                decrement += Decimal(dict_Matrix.get(v1 +'_'+ v2,'0'))
            if v1 +'_'+ v2 in dict_Matrix.keys():
                f.write(',' +str(dict_Matrix[v1 +'_'+ v2]))
            else:
                f.write(',')
        f.write(',' + str(total_row) + ',' + str(decrement) + '\n')

    f.write("总计")
    for cc in List_CcLevel:
        f.write(',' + str(total_col[cc]))
    f.write(',' + str(sum(total_col.values())))
    f.write('\n')

    f.write("转入量")
    for cc in List_CcLevel:
        f.write(',' + str(increment[cc]))
    f.write('\n')
    f.close()
###
def get_dicTwoLevelMatrix(pac,var_temp):
    global list_cc
    list_cc = []
    dict_Matrix = {}
    for f_matrix in glob.glob(os.path.normpath(var_temp + '\\{}.txt'.format(pac))):
        f = open(f_matrix,'r')
        for line in f.readlines():
            if 'PAC' in line:
                continue
            else:
                list_line = line.strip('\n').split(',')

                
                if list_line[1] == '1001' or list_line[1] == '1012' or list_line[1] == '0601':
                    if list_line[2] == '1001' or list_line[2] == '1012' or list_line[2] == '0601':
                        cc_2015 = dic_cc2015_cc2017.get(list_line[1][0:4],list_line[1])
                        cc_2017 = dic_cc2015_cc2017.get(list_line[2][0:4],list_line[2])
                        if cc_2015+'_'+cc_2017 in dict_Matrix.keys():
                            dict_Matrix[cc_2015+'_'+cc_2017] = Decimal(dict_Matrix[cc_2015+'_'+cc_2017]) + Decimal(list_line[3])
                        else:
                            dict_Matrix[cc_2015+'_'+cc_2017] = Decimal(list_line[3])
                        list_cc.append(cc_2015)
                        list_cc.append(cc_2017)
                    else:
                        cc_2015 = dic_cc2015_cc2017.get(list_line[1][0:4],list_line[1])
                        cc_2017 = dic_cc2015_cc2017.get(list_line[2][0:4],list_line[2])
                        if cc_2015+'_'+list_line[2][0:3]+'0' in dict_Matrix.keys():
                            dict_Matrix[cc_2015+'_'+cc_2017[0:3]+'0'] = Decimal(dict_Matrix[cc_2015+'_'+cc_2017[0:3]+'0']) + Decimal(list_line[3])
                        else:
                            dict_Matrix[cc_2015+'_'+cc_2017[0:3]+'0'] = Decimal(list_line[3])
                        list_cc.append(cc_2015)
                        list_cc.append(cc_2017[0:3]+'0')
                else:
                    if list_line[2] == '1001' or list_line[2] == '1012' or list_line[2] == '0601':
                        cc_2015 = dic_cc2015_cc2017.get(list_line[1][0:3]+'0',list_line[1][0:3]+'0')
                        cc_2017 = dic_cc2015_cc2017.get(list_line[2][0:4],list_line[2])
                        if cc_2015 +'_'+cc_2017 in dict_Matrix.keys():
                            dict_Matrix[cc_2015+'_'+cc_2017] = Decimal(dict_Matrix[cc_2015+'_'+cc_2017]) + Decimal(list_line[3])
                        else:
                            dict_Matrix[cc_2015+'_'+cc_2017] = Decimal(list_line[3])
                        list_cc.append(cc_2015)
                        list_cc.append(cc_2017)
                    else:
                        cc_2015 = dic_cc2015_cc2017.get(list_line[1][0:3]+'0',list_line[1][0:3]+'0')
                        cc_2017 = dic_cc2015_cc2017.get(list_line[2][0:4],list_line[2])
                        if cc_2015+'_'+cc_2017[0:3]+'0' in dict_Matrix.keys():
                            dict_Matrix[cc_2015+'_'+cc_2017[0:3]+'0'] = Decimal(dict_Matrix[cc_2015+'_'+cc_2017[0:3]+'0']) + Decimal(list_line[3])
                        else:
                            dict_Matrix[cc_2015+'_'+cc_2017[0:3]+'0'] = Decimal(list_line[3])
                        list_cc.append(cc_2015)
                        list_cc.append(cc_2017[0:3]+'0')                        
        f.close()
    list_cc = sorted(list(set(list_cc)))
    if '---0' in list_cc:
        list_cc.remove('---0')
        list_cc.append('---0')
    return dict_Matrix








def collect_province(var_temp,out_path):
    list_pac_province = []
    for pac in glob.glob(os.path.normpath(var_temp + "\\*.txt")):
        list_pac_province.append(pac[-10:-8])
    list_pac_province = list(set(list_pac_province))
    for pac_province in list_pac_province:
        pac_province = pac_province + '*'
        dict_Matrix_province_one = get_dicOneLevelMatrix(pac_province,var_temp)
        write_ToTxt_province_oneLevel(list_cc,pac_province,out_path,dict_Matrix_province_one)
        dict_Matrix_province_two = get_dicTwoLevelMatrix(pac_province,var_temp)
        write_ToTxt_province_twoLevel(list_cc,pac_province,out_path,dict_Matrix_province_two)
        dict_Matrix_province_three = get_dicThreeLevelMatrix(pac_province,var_temp)
        write_ToTxt_province_threeLevel(list_cc,pac_province,out_path,dict_Matrix_province_three)

def collect_city(var_temp,out_path):
    list_pac_city = []
    for pac in glob.glob(os.path.normpath(var_temp + "\\*.txt")):
        list_pac_city.append(pac[-10:-6])
    list_pac_city = list(set(list_pac_city))
    for pac_city in list_pac_city:
        pac_city = pac_city + '*'
        dict_Matrix_city_one = get_dicOneLevelMatrix(pac_city,var_temp)
        write_ToTxt_city_oneLevel(list_cc,pac_city,out_path,dict_Matrix_city_one)
        dict_Matrix_city_two = get_dicTwoLevelMatrix(pac_city,var_temp)
        write_ToTxt_city_twoLevel(list_cc,pac_city,out_path,dict_Matrix_city_two)
        dict_Matrix_city_three = get_dicThreeLevelMatrix(pac_city,var_temp)
        write_ToTxt_city_threeLevel(list_cc,pac_city,out_path,dict_Matrix_city_three)

def collect_county(var_temp,out_path):
    list_pac_county = []
    for pac in glob.glob(os.path.normpath(var_temp + "\\*.txt")):
        list_pac_county.append(pac[-10:-4])
    list_pac_county = list(set(list_pac_county))
    for pac_county in list_pac_county:
        dict_Matrix_county_one = get_dicOneLevelMatrix(pac_county,var_temp)
        write_ToTxt_county_oneLevel(list_cc,pac_county,out_path,dict_Matrix_county_one)
        dict_Matrix_county_two = get_dicTwoLevelMatrix(pac_county,var_temp)
        write_ToTxt_county_twoLevel(list_cc,pac_county,out_path,dict_Matrix_county_two)
        dict_Matrix_county_three = get_dicThreeLevelMatrix(pac_county,var_temp)
        write_ToTxt_county_threeLevel(list_cc,pac_county,out_path,dict_Matrix_county_three)


def collect_QuanGuo(var_temp,out_path):
    dict_Matrix_county_one = get_dicOneLevelMatrix('*',var_temp)
    write_ToTxt_county_oneLevel(list_cc,'000000',out_path,dict_Matrix_county_one)
    dict_Matrix_county_two = get_dicTwoLevelMatrix('*',var_temp)
    write_ToTxt_county_twoLevel(list_cc,'000000',out_path,dict_Matrix_county_two)
    dict_Matrix_county_three = get_dicThreeLevelMatrix('*',var_temp)
    write_ToTxt_county_threeLevel(list_cc,'000000',out_path,dict_Matrix_county_three)
##if __name__ == '__main__':
##    var_temp = r'G:\2015_2017Matrix\temp'
##    out_path = r'G:\2015_2017Matrix\Result'
##    collect_city(var_temp,out_path)
##    collect_county(var_temp,out_path)
##    collect_QuanGuo(var_temp,out_path)
##    collect_province(var_temp,out_path)

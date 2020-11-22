# -*- coding: cp936 -*-

import sys,os,xlwt,glob
from decimal import Decimal


def len_byte(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length)/2 + length
    return int(length)
def get_dic_codeName(path):
    dic = {}
    f = open(path,'r')
    for line in f.readlines():
        lst = line.strip().split(',')
        dic[lst[0]] = lst[1].decode('utf-8')
        
    return dic
def wrt_excel(txt_dir,out_dir,yearOld,yearNer):
    dic_codeName = get_dic_codeName(sys.path[0] + os.sep + 'CodeName.txt')
    lst_provinceCode = []
    for pac in os.listdir(txt_dir):
        if pac[-3:] == 'txt':
            lst_provinceCode.append(pac[0:2])
    lst_provinceCode = set(lst_provinceCode)

    style_bold = xlwt.XFStyle()
    style_noBold = xlwt.XFStyle()

    font_bold = xlwt.Font()
    font_bold.name = u'宋体'
    font_bold.bold = True
    style_bold.font = font_bold

    font_noBold = xlwt.Font()
    font_noBold.name = u'宋体'
    font_noBold.bold = False
    style_noBold.font = font_noBold

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    style_bold.borders = borders
    style_noBold.borders = borders

    alignment_center = xlwt.Alignment()
    alignment_center.horz = xlwt.Alignment.HORZ_CENTER
    alignment_center.vert = xlwt.Alignment.VERT_CENTER
    style_bold.alignment = alignment_center

    alignment_right = xlwt.Alignment()
    alignment_right.horz = xlwt.Alignment.HORZ_RIGHT
    alignment_right.vert = xlwt.Alignment.VERT_CENTER
    style_noBold.alignment = alignment_right
    style_noBold.num_format_str = '0.00'

    for pac in lst_provinceCode:
        book = xlwt.Workbook(encoding = 'utf-8')
        for txt_path in glob.glob(txt_dir + os.sep + '{0}*.txt'.format(pac)):
            row = 3
            f = open(txt_path,'r')
            num_line = len(f.readlines())
            f.seek(0,0)
            #表头
            if txt_path[-5:-4] == '1':
                sheet = book.add_sheet(dic_codeName.get(txt_path[-12:-6],txt_path[-12:-6]) + u'一级地表覆盖转移矩阵',cell_overwrite_ok = True)
                sheet.write_merge(row,row,2,num_line + 2,dic_codeName.get(txt_path[-12:-6],txt_path[-12:-6]) + u'一级地表覆盖转移矩阵',style_bold)
            elif txt_path[-5:-4] == '2':
                sheet = book.add_sheet(dic_codeName.get(txt_path[-12:-6],txt_path[-12:-6]) + u'二级地表覆盖转移矩阵',cell_overwrite_ok = True)
                sheet.write_merge(row,row,2,num_line + 2,dic_codeName.get(txt_path[-12:-6],txt_path[-12:-6]) + u'二级地表覆盖转移矩阵',style_bold)
            elif txt_path[-5:-4] == '3':
                sheet = book.add_sheet(dic_codeName.get(txt_path[-12:-6],txt_path[-12:-6]) + u'三级地表覆盖转移矩阵',cell_overwrite_ok = True)
                sheet.write_merge(row,row,2,num_line + 2,dic_codeName.get(txt_path[-12:-6],txt_path[-12:-6]) + u'三级地表覆盖转移矩阵',style_bold)
            #第二行
            row += 1
            sheet.write(row,2,u'年份',style_bold)
            sheet.write_merge(row,row,3,num_line,yearNer,style_bold)
            sheet.write_merge(row,row + 1,num_line + 1,num_line + 1,u'总计',style_bold)
            sheet.write_merge(row,row + 1,num_line + 2,num_line + 2,u'减少',style_bold)
            #第一列
            sheet.write_merge(row + 1,row + num_line - 2,2,2,yearOld,style_bold)
            sheet.write_merge(row + num_line - 1,row + num_line - 1,2,3,u'总计',style_bold)
            sheet.write_merge(row + num_line,row + num_line,2,3,u'增加',style_bold)

            column_width_dic = {}
            
            for value_row in f.readlines():
                row += 1
                column = 2
                for value_column in value_row.strip().split(','):
                    column += 1
                    if len_byte(value_column.decode('utf-8')) > column_width_dic.get(column,10):
                        column_width_dic[column] = len_byte(value_column.decode('utf-8'))
                    sheet.col(column).width = 256 * (column_width_dic.get(column,10) + 1)
                    if row == 5 or column == 3:
                        sheet.write(row,column,value_column,style_bold)
                    else:
                        if value_column != '':
                            value_column = Decimal(value_column)
                            sheet.write(row,column,value_column,style_noBold)
                        else:
                            sheet.write(row,column,value_column,style_noBold)
                            
            sheet.write(row - 1,2 + num_line,'',style_noBold)
            sheet.write(row,1 + num_line,'',style_noBold)
            sheet.write(row,2 + num_line,'',style_noBold)
            f.close()
       
        book.save(os.path.join(out_dir,dic_codeName.get(pac + '0000',pac + '0000') + '.xls'))

def wrt_excel_shenji(txt_dir,out_dir):
    dic_codeName = get_dic_codeName(sys.path[0] + os.sep + 'CodeName.txt')
    lst_provinceCode = []
    for pac in os.listdir(txt_dir):
        if pac[-3:] == 'txt':
            lst_provinceCode.append(pac[0:2])
    lst_provinceCode = set(lst_provinceCode)

    style_bold = xlwt.XFStyle()
    style_noBold = xlwt.XFStyle()

    font_bold = xlwt.Font()
    font_bold.name = 'Times New Roman'
    font_bold.bold = True
    style_bold.font = font_bold

    font_noBold = xlwt.Font()
    font_noBold.name = 'Times New Roman'
    font_noBold.bold = False
    style_noBold.font = font_noBold

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    style_bold.borders = borders
    style_noBold.borders = borders

    alignment_center = xlwt.Alignment()
    alignment_center.horz = xlwt.Alignment.HORZ_CENTER
    alignment_center.vert = xlwt.Alignment.VERT_CENTER
    style_bold.alignment = alignment_center

    alignment_right = xlwt.Alignment()
    alignment_right.horz = xlwt.Alignment.HORZ_RIGHT
    alignment_right.vert = xlwt.Alignment.VERT_CENTER
    style_noBold.alignment = alignment_right

    for pac in lst_provinceCode:
        book = xlwt.Workbook(encoding = 'utf-8')
        for txt_path in glob.glob(txt_dir + os.sep + '{0}*.txt'.format(pac)):
            row = 3
            f = open(txt_path,'r')
            #表头
    
            sheet = book.add_sheet(dic_codeName[txt_path[-10:-4]] + u'生态地表转移矩阵',cell_overwrite_ok = True)
            sheet.write_merge(row,row,3,len(f.readlines()) + 2,dic_codeName[txt_path[-10:-4]] + u'生态地表转移矩阵',style_bold)
            f.seek(0,0)
            for value_row in f.readlines():
                row += 1
                column = 2
                for value_column in value_row.strip().split(','):
                    column += 1
                    if row == 4 or column == 3:
                        sheet.write(row,column,value_column,style_bold)
                    else:
                        if value_column != '':
                            value_column = Decimal(value_column).quantize(Decimal('0.00'))
                            sheet.write(row,column,'{:,}'.format(value_column),style_noBold)
                        else:
                            sheet.write(row,column,value_column,style_noBold)
            f.seek(0,0)
            sheet.write(row,2 + len(f.readlines()),'',style_noBold)
            f.close()
        book.save(os.path.join(out_dir,dic_codeName[pac + '0000'] + '.xls'))

if __name__ == '__main__':
##    wrt_excel_shenji(r'G:\qxl\Matrix_new\Matrix',r'G:\qxl\Matrix_new\Matrix')
    wrt_excel(r'G:\qxl\Matrix_new\Matrix',r'G:\qxl\Matrix_new','2015','2017')
    
                            
                
    
    

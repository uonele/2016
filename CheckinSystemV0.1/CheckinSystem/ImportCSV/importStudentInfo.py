# -*- coding: utf-8 -*-
import csv
from AbstractImport import Abstractimport
from BaseCheck import Basecheck

class importStudentInfo(Abstractimport, Basecheck):
    def data_prepare(self, filename, _filename):
        #正确表头
        message0 =['StuID','StuName','ClassID','WechatID']
        #检查列的个数和列名以及数据的完整性
        if self.check_data(filename, message0) :
            #提取待导入文件的数据
            csvfile = open(filename, 'rb')
            reader = csv.reader(csvfile)
            Data = []           #存入待导入信息
            reader.next()       #抛出第一行
            for line in reader :
                Data.append(line)
            csvfile.close()
            self.check_in_out(Data, _filename)  #查重
        else :
            return

if  __name__ == '__main__' :
    #待导入学生信息文件
    filename =['Externalfiles/软件工程1401.csv','Externalfiles/软件工程1402.csv','Externalfiles/软件工程1403.csv','Externalfiles/软件工程1404.csv','Externalfiles/软件工程1405.csv','Externalfiles/计算机科学与技术1401.csv']
    #目标文件
    _filename = 'data/studentInfo.csv'
    #实例化
    StudentInfo = importStudentInfo()

    for _file in filename:
        print _file.split('/')[1][:-4]
        StudentInfo.data_prepare(_file, _filename)

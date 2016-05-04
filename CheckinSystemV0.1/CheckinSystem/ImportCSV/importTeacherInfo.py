# -*- coding: utf-8 -*-
import csv
from AbstractImport import Abstractimport
from BaseCheck import Basecheck

class importTeacherInfo(Abstractimport, Basecheck):
    def data_prepare(self, filename, _filename):
        #正确表头
        message0 =["TeacherID", "TeacherName", "WeChatID"]
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
            self.check_in_out(Data, _filename)
        else :
            return

if  __name__ == '__main__' :

    #待导入教师信息文件
    filename ='Externalfiles/teacherInfo.csv'
    #目标文件
    _filename = 'data/teacherInfo.csv'
    #实例化
    TeacherInfo = importTeacherInfo()
    #调用方法
    TeacherInfo.data_prepare(filename, _filename)




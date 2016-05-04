# -*- coding: utf-8 -*-
import csv
import csvkit
import os
import re
from AbstractImport import Abstractimport
from BaseCheck import Basecheck

class importCourseInfo(Abstractimport, Basecheck):
    def data_prepare(self, filename, _filename):
        #抽取其中有效的数据列并先存入course.csv中,"csvkit"
        cmd = 'csvcut -c CourseID,CourseName,TeacherID,ClassNums ' + filename +' > data/course.csv'
        os.popen(cmd)
        #正确表头
        message0=['CourseID','CourseName','TeacherID','ClassNums']
        _file = 'data/course.csv'
        #检查列的个数和列名以及数据的完整性
        if self.check_data(_file, message0) :
            self.data_integration(_file, _filename)
        else :
            return

    #数据的整合成正确格式
    def data_integration(self, filename, _filename):
        csvfile = open(filename, 'rb')
        reader = csv.reader(csvfile)
        reader.next()
        #存放课程信息
        Data = []
        for line in reader :
            for cl1 in line[-1].split(',') :
                pattern = re.compile(r'\d+') #正则表达式提取班级区间
                clnum = re.findall(pattern, cl1)  #班级区间
                for i in range(int(clnum[0]), int(clnum[-1]) + 1) :
                    #提取专业名称
                    cl2 = cl1.split('-')[0][:-4]
                    line1 = line[:-1]
                    cl2 = cl2 + str(i)
                    line1.append(cl2)
                    Data.append(line1)
        #去除教师信息表不存在的教师or学生表不存在的班级
        self.check_teacher_stu(Data, _filename)

    #检查班级
    def check_class(self, Class) :
        csvfile = open('data/studentInfo.csv', 'rb')
        reader = csv.reader(csvfile)
        for line in reader :
            if line[2] == Class :
                return True
        csvfile.close()
        return False

    #检查教师
    def check_teacher(self, teacherId) :
        csvfile = open('data/teacherInfo.csv', 'rb')
        reader = csv.reader(csvfile)
        for line in reader :
            if line[0] == teacherId :
                return True
        csvfile.close()
        return False

    #去除教师信息表不存在的教师or学生表不存在的班级
    def check_teacher_stu(self, Data, _filename):

        #班级信息列表的索引
        Line = 0
        for classlist in Data :
            #检查教师和班级信息，若有一项不存在，pop()
            if not (self.check_class(classlist[-1])  and  self.check_teacher(classlist[-2]) ):
                Data.pop(Line)
            Line = Line +1
        #查重
        self.check_in_out(Data, _filename)

    #自身的查重(复写)
    def check_dup(self, Data):
        Data1 = []
        Data1.append(Data[0])
        for line1 in Data :
            Dn = False
            for line2 in Data1 :
                if line1 == line2 :
                    Dn = True
                    break
            if not Dn :
                Data1.append(line1)
        return Data1

    #查重(复写)
    def get_unique_line(self,Data, line) :
        for line1 in Data :
            if line[:-2].split(',') == line1 :   #[:-2]去除后两位的换行符
                return False
        return True

if  __name__ == '__main__' :

    #待导入课程信息文件
    filename ='Externalfiles/courseProgress.csv'
    #目标文件
    _filename = 'data/courseInfo.csv'
    #实例化
    CourseInfo = importCourseInfo()
    #调用方法
    CourseInfo.data_prepare(filename, _filename)

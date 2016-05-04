# coding=utf-8

import csv
import os
import time
import random
from Timer import Timer

class Student(Timer):

    #通过微信号生成checkfilename
    def getFileName(self,_stuWecharID):

        #由学生微信号得到学生ID 和 班级ID
        with open('data/studentInfo.csv', 'r') as checkStuFile:
            reader = csv.reader(checkStuFile)
            reader.next()
            for readline in reader:
                if readline[3] == _stuWecharID:

                    Timer.StuID = readline[0]
                    ClassID = readline[2]
                else:
                    print '没这个学生'  # 没有查询到该学生

        #由班级ID生成checkfilename
        #遍历教师队列中教师所带的多个班级
        for line in Timer.List :
            for cline in line[2] :   #line[2]是班级列表
                if cline == ClassID :
                    TID=line[0]      #line[0]是teacherID
                    CID=line[1]      #line[1]是courseID
                    cmd = 'csvcut -c TeacherID,CourseID,SeqID  data/seq.csv' + '> data/seqnew.csv'
                    os.popen(cmd)

                    #记录seqID
                    with open('data/seqnew.csv', 'r') as csvfile:
                        reader = csv.reader(csvfile)
                        reader.next()
                        for line in reader:
                            if (line[0] == TID) & (line[1] == CID):
                                Timer.seqID = line[2]
                            else:
                                pass

                    Timer.checkfileName = 'data/' + str(TID) + '_' + str(CID) + '_' + \
                                        str(Timer.seqID) + '_' + 'checkinDetail.csv'
                    os.remove('data/seqnew.csv')
                    print '你将进行ID为'+TID+'的教师的考勤操作'
                    print '课程ID为'+CID


    #学生正常签到
    def StuCheckIn(self,_stuWecharID,inputStream):

        self.getFileName(_stuWecharID)
        checkinTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ProofPath = inputStream
        checkinType = 'Auto'
        IsSucc = bool(random.randrange(0, 2))
        checkinResult = None
        print Timer.checkfileName
        with open(Timer.checkfileName, 'a') as checkfile:
            writer = csv.writer(checkfile)
            message0 = [Timer.StuID, checkinTime, ProofPath, checkinType, IsSucc, checkinResult]
            writer.writerow(message0)

    #学生请假
    def StuLeave(self,_stuWecharID,inputStream):
        self.getFileName(_stuWecharID)

        checkinTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ProofPath = inputStream
        checkinType = 'Auto'
        IsSucc = ''
        checkinResult = '请假'

        with open(Timer.checkfileName, 'a') as checkfile:
            writer = csv.writer(checkfile)
            message0 = [Timer.StuID, checkinTime, ProofPath, checkinType, IsSucc, checkinResult]
            writer.writerow(message0)
    #学生参与抽点
    def stuRadomCheckIn(self,_stuWechatID, inputStream):

        ISOTIMEFORMAT = '%Y/%m/%d %X'  # 指定时间格式

        #生成文件名
        self.getFileName(_stuWechatID)
        _filename = open(Timer.checkfileName, 'a+')

        #随机生成考勤结果（出勤/缺勤）
        list = ["True", "False"]
        IsSucc = random.choice(list)
        if IsSucc == 'True':
            checkinResult = '出勤'
        else:
            checkinResult = '缺勤'

        #匹配微信号，成功->写入考勤信息
        filename = 'data/studentInfo.csv'
        with open(filename, 'rb') as studentInfo:
            reader = csv.reader(studentInfo)
            reader.next()
            for readline in reader:
                if readline[2] == _stuWechatID:
                    _filename.write(readline[0] + ',Random,' + time.strftime(ISOTIMEFORMAT, time.localtime())
                                + ',' + inputStream + ',' + IsSucc + ',' + checkinResult + ',' + _stuWechatID)

if __name__ == '__main__' :
    _stuWechatID ='wfsf_135'
    inputStream = '正常的考勤路径'
    s=Student()
 #   s.StuCheckIn(_stuWechatID,inputStream)
    s.getFileName('wfsf_138')

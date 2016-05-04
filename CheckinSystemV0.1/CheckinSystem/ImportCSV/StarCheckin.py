# -*- coding: utf-8 -*-

import threading
import random
import time
import csv
'''
by子恒 and Onele
版本号:01
详细设计:
教师类
    1):可打开或者关闭考勤;
    2):打开考勤:def StartCheckin(self,teacherWechatID,CourseID)
        2.1:系统采用遍历'data/teacherInfo.csv'文件的方式匹配教师微信号
            匹配成功则将考勤记录写入'data/seq.csv'中
    3):关闭考勤:stopCheckin(self,teacherID,CourseID)
        3.1:教师如不手动关闭考勤的话,系统将 
'''

class Teacher:

    global Teacher_Queue
    Teacher_Queue = []
    #教师开启考勤
    def StartCheckin(self,teacherWechatID,CourseID):
        filename = open('data/seq.csv','a+')#每次考勤对应一个文件
        csvfile = open('data/teacherInfo.csv', 'a+')
        reader = csv.reader(csvfile)
        reader.next()
        count=1
        for line in reader :
            if teacherWechatID == line[-1]:
                filename.write(line[0]+',' + CourseID +',' + (str)(count) +','+ time.strftime('%Y/%m/%d %X',time.localtime()) + '\n')
                count=count+1
                global TEACHER_ID
                TEACHER_ID = line[0]

                Teacher_Queue.append(line[0])   #入队

                # #定时器,60minutes后关闭考勤
                # timer = threading.Timer(30, self.StopCheckin(teacherWechatID,CourseID))
                # print '系统将在90 minutes后自动关闭'
                # timer.start()

                break

        csvfile.close()
        filename.close()

    #教师关闭考勤,并出队
    def StopCheckin(self,teacherWechatID , CourseID):
        #根据教师微信号,找到该教师的教工号
        with open('data/teacherInfo.csv') as  file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['WeChatID'] == teacherWechatID:
                    teacherID = row['TeacherID']
        #根据教师ID来出队
        for teacherInfo in Teacher_Queue:
            flag = 0
            if (teacherInfo[0] == teacherID) and (teacherInfo[1] == CourseID):
                Teacher_Queue.pop(flag)
                print'出队成功'
            flag = flag + 1

    #学生参与考勤
    def StuCheckin(self, _stuWechatID, inputStream):
        ISOTIMEFORMAT = '%Y/%m/%d %X'  # 指定时间格式

        # 按照相应格式写考勤文件名
        count = '1'  # 考勤序号初始化为1
        TeacherID = '2004633'

        csvfile = open('data/courseInfo.csv', 'r')
        reader = csv.reader(csvfile)
        reader.next()
        for line in reader:
            if TeacherID == line[2]:
                CourseID = line[0]  # line[2]:教工号  line[0]:课程号
                break

        filename = open('data/' + TeacherID + '_' + CourseID + '_' + count + '_' + 'checkinDetail.csv',
                        'a+')  # 每次考勤对应一个文件
        # 生成考勤内容,    输入微信号,如果微信号相同,则记录到文件中,不同则不写
        checkinType = 'Auto'  # checkinType登记为Auto

        csv_file = open('data/studentInfo.csv', 'r')
        _file = csv.reader(csv_file)
        _file.next()

        for line in _file:
            list = ["True", "False"]
            IsSucc = random.choice(list)
            if IsSucc == 'True':
                checkinResult = '出勤'
            else:
                checkinResult = '缺勤'
            if _stuWechatID == line[-1]:
                filename.write(line[0] + ',' + time.strftime(ISOTIMEFORMAT, time.localtime()) + ','
                               + 'D:/Proof/' + line[
                                   0] + '_51610055_1_' + inputStream + '.jpg' + ',' + checkinType + ',' + IsSucc + ',' + checkinResult)
                filename.write('\n')
                print '考勤成功'
            else:
                pass  # 输出考勤失败

        csvfile.close()
        filename.close()
        csv_file.close()

if __name__ =='__main__':
    #教师开启考勤的测试
    StartCheckin =Teacher()
    # teacherWecherID=raw_input('请输入教师微信号：')
    # CourseID=raw_input('请输入课程号：')
    # StartCheckin.StartCheckin(teacherWecherID, CourseID)
    # print '考勤开始，您可以在5分钟内考勤！！！'


    #学生参与考勤的测试
    _stuWechatID = raw_input('_stuWechatID:')   #微信号
    inputStream = raw_input('inputStream:')
    StartCheckin.StuCheckin(_stuWechatID,inputStream)
    #测试时最好分布测试,一个一个的测










#此乃定时器的使用法门
'''
# encoding: UTF-8
import threading
#Timer（定时器）是Thread的派生类，
#用于在指定时间后调用一个方法。
def func():
  print 'hello timer!'
timer = threading.Timer(5, func)
timer.start()
该程序可实现延迟5秒后调用func方法的功能。
'''

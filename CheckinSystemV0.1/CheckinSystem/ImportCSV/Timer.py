# coding=utf-8

import ConfigParser
import time
import re

class Timer(object):

    #学生类中用到的全局变量
    StuID = ''
    seqID =''

    #教师类中用到的全局变量
    teacherID =''
    List =[]
    classlist = []
    checkfileName=''
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S')



    # 需要把seq.ini放在Externalfiles文件夹里面
    Time = []
    config = ConfigParser.ConfigParser()  #
    config.readfp(open('Externalfiles/settings.ini'))  # open里面的参数是文件路径
    # 读取配置文件中的上课时间信息到Time
    Time.append(config.get("Time", "class_One_Start"))
    Time.append(config.get("Time", "class_One_End"))
    Time.append(config.get("Time", "class_Two_Start"))
    Time.append(config.get("Time", "class_TWo_End"))
    Time.append(config.get("Time", "class_Three_Start"))
    Time.append(config.get("Time", "class_Three_End"))
    Time.append(config.get("Time", "class_Four_Start"))
    Time.append(config.get("Time", "class_Four_End"))

    # 设置计时器 传入的时时间差值
    def timeCheck(self, timerInterval):
        if len(self.List) == 1:
            timerInterval = self.cf.get('time', 'timewindow')
        else:
            pass
        time.sleep(timerInterval)
        return False

    # 这里比较l_time 是否在时间区间[start_t, end_t]中
    def compare_time(l_time, start_t, end_t):
        log_time = time.mktime(time.strptime(l_time, '%H:%M'))

        s_time = time.mktime(time.strptime(start_t, '%H:%M'))  # get the seconds for specify date

        e_time = time.mktime(time.strptime(end_t, '%H:%M'))

        if (float(log_time) >= float(s_time)) and (float(log_time) <= float(e_time)):
            return True

        return False

    # cf = ConfigParser.ConfigParser()
    # cf.read('InData/settings.ini')
    #
    # # 第一二节课的时间始末
    # time = re.split('-|:',cf.get('sectime','sec1'))
    # FirstEndTime = str(time[2])+str(time[3])
    # time = re.split('-|:', cf.get('sectime', 'sec2'))
    # SecondStartTime = str(time[0]) + str(time[1])
    #
    # # 第三四节课的时间始末
    # time = re.split('-|:', cf.get('sectime', 'sec3'))
    # ThreeEndtime = str(time[2]) + str(time[3])
    # time = re.split('-|:', cf.get('sectime', 'sec4'))
    # FourStartTime = str(time[0]) + str(time[1])
    # # 第四五节课的时间始末
    # FourEndTime = str(time[2]) + str(time[3])
    # time = re.split('-|:', cf.get('sectime', 'sec5'))
    # FiveStartTime = str(time[0]) + str(time[1])














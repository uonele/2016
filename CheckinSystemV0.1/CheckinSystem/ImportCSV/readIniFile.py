#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
by:onele
功能:读配置文件
'''
def read_ini():

    #需要把seq.ini放在Externalfiles文件夹里面
    import ConfigParser
    Time = []
    config = ConfigParser.ConfigParser()               #
    config.readfp(open('Externalfiles/settings.ini'))  #open里面的参数是文件路径
    #读取配置文件中的上课时间信息到Time
    Time.append(config.get("Time","class_One_Start"))
    Time.append(config.get("Time","class_One_End"))
    Time.append(config.get("Time","class_Two_Start"))
    Time.append(config.get("Time","class_TWo_End"))
    Time.append(config.get("Time","class_Three_Start"))
    Time.append(config.get("Time","class_Three_End"))
    Time.append(config.get("Time","class_Four_Start"))
    Time.append(config.get("Time","class_Four_End"))
#    for str in Time:
 #       print str
#read_ini()



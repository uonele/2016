# -*- coding: utf-8 -*-

import csv
import os
import logging

class Basecheck():
    #检查列的个数和列名以及数据的完整性
    def check_data (self, _filename, message0) :
        csvfile = open(_filename, 'rb')
        reader = csv.reader(csvfile)
        message = reader.next()   #获取文件第一行
        Dict = {}                #存放错误信息

        if message == message0:    #表头信息完整
            count = 2             #控制行数
            for line in reader:
                if len(line) == len(message0):
                    if not (line.count('') == 0):
                        Dict.update({count: '某项信息为空'})
                else:
                    Dict.update({count: '对象信息数量不匹配'})
                count = count + 1       #下一行
        else :
            Dict.update({'error': '表头信息不完整或有错误'})
        if not (len(Dict) == 0) :
            csvfile.close()
            print '导入失败，原因查看错误日志'
            self.write_log(Dict)
            return False
        return True

    #错误写入日志
    def write_log(self, Dict):
        logging.basicConfig(
                level=logging.DEBUG, #日志级别，默认为logging.WARNING
                format='%(levelname)s:   %(message)s     %(asctime)s', #指定内容顺序
                datefmt='%a, %d %b %Y %H:%M:%S', #指定时间格式
                filename='data/importError.log', #日志文件名，没有会自动生成
                filemode='a'  #覆盖之前log
        )
        for key, value in Dict.items():
            Error =  "第" + str(key) + "行数据   "  + value
            logging.error(Error)

    #向系统文件内导入无误外部数据
    def import_data(self, filename, Data):
        csvfile = open(filename, 'a')
        writer = csv.writer(csvfile)
        writer.writerows(Data)
        csvfile.close()
        print '导入成功'

    #比较待导入文件与系统内文件某行的差异
    def get_unique_line(self, Data, line):
        for data in Data :
            if data[0] == line.split(',')[0] :
                return False
        return True

    #自身的查重
    def check_dup(self, Data):
        Data1 = []
        Data1.append(Data[0])
        for line1 in Data :
            Dn = False
            for line2 in Data1 :
                if line1[0] == line2[0] :
                    Dn = True
                    break
            if not Dn :
                Data1.append(line1)
        return Data1

    #外部文件与内部文件的查重,并更新内部文件
    def check_in_out(self, Data, _filename):
        Data = self.check_dup(Data)   #自身查重并更新
        csvfile1 = open(_filename,'r+') #内外部信息的查重
        lines = csvfile1.readlines()
        csvfile1.seek(0)
        for line in lines :
            if self.get_unique_line(Data, line) :
                csvfile1.write(line)
        csvfile1.truncate()       #对系统文件的更新
        csvfile1.close()
        #导入无误信息
        self.import_data(_filename, Data)









# _*_ coding: utf-8 _*_
'''
详细设计:
    1):停止考勤,搜索该教师的个人信息,并驱逐出队
    2):计算考勤结果:
     2.1:打开存放考勤结果的文件
     2.2:动态生成并打开考勤信息汇总文件
     2.3:每次都在文件中追加一列来存放考勤结果
'''
import csv
def readFile(output_filename):
    list = []
    i = 0
    f = open(output_filename,"r")
    lines = f.readlines()               #读取全部内容
    for line in lines:
        list[i] = line
        i = i+1
    f.close()
    return list

def clacSum(teacherID , courseID , seqID):
    #统计对应教师号 课程号 考勤序号的考勤结果汇总

    #根据传入的参数整合成一个文件，该文件就是某个教师该门课的考勤详细情况
    input_filename = '%s_%s_0%s_checkinDetail.csv' % (teacherID , courseID , seqID)
    reader  = open(input_filename , 'r+')

    #打开要写入的文件
    output_filename = '%s_%s_0%s_sum.csv' % (teacherID , courseID , seqID)
    writer = file(output_filename , 'a')

    Data = []           #用来存放带整合的数据
    reader.readline()   #第一行不读

    #判断需要统计的是否是第一次的考勤情况，如果是第一次的就直接将表头写进文件  格式Stu_ID,checkin1
    if seqID == '1':
        #正确表头（第一次考勤）往后自动增加一列
        writer.write('StuID,checkin1')
        i = 0
        for line in reader.readlines():
            Data[i] = line.split(',')[0]+','+line.split(',')[-1] #将第一列的学号取出
            writer.write(Data[i])
            i = i + 1
    #统计的是第一次往后的考勤情况，需要在表头增加列数，并且需要将相应的学号对应的考勤结果写入
    else:
        Data2 = []   #储存要写入的文件中的内容
        Data3 = []   #学号
        Data4 = []   #考勤状态

        Data2 =  readFile(output_filename)

        strTemp = Data2[0]
        Data2[0] = strTemp+'checkin%s' % seqID

        #Data2复制到Data中，并给Data中的每一列增加考勤状态
        i = 0
        for line in reader.readlines():
            Data3[i] = line.split(',')[1]   #将第一列的学号取出并储存在列表中
            Data4[i] = line.split(',')[-1] #将第一列的考勤状态取出，并储存
            i = i + 1

            for line2 in Data2 :             #遍历Data3（也就是学号）
                if Data3[i] == line2.split(',')[0] :
                    Data.append(line2 + Data4[i])
        for i in Data:
            writer.write(i)
            writer.write("\n")

        writer.close()

#停止考勤
'''
def StopCheckin(teacherWechatID,CourseID):
	#根据教师微信号，找到该教师的教工号
	with open('teacherInfo.csv') as csv_Teacher:
		reader = csv.DictReader(csv_Teacher)
		for row in reader:
			if row['WeChatID'] == teacherWechatID:
				TeacherID = row['TeacherID']
	csv_Teacher.close()
	#从全局队列中删除该教师的课程信息
	for teacherInfo in Teacher_Queue:
		flag = 0
		if  (teacherInfo[0] == TeacherID) and (teacherInfo[1]== CourseID):
			Teacher_Queue.pop(flag)
		flag = flag + 1

'''







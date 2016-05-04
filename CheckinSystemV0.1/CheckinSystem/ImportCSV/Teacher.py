#coding=utf-8
import time,string,os,csv
from Timer import Timer

class Teacher(Timer):
    #根据教师微信号找到教师ID
    def findTeacherId(self,teacherWechatID):
        filename = 'data/teacherInfo.csv'
        with open(filename, 'rb') as teacherInfo:  # 从教师信息表里查询教师工号 记录
            reader = csv.reader(teacherInfo)
            reader.next()
            for readline in reader:
                if readline[2] == teacherWechatID:

                    Timer.teacherID = readline[0]
                    checkTeacher = 0
                    break
                else:
                    checkTeacher = 1  # 没有查询到教师工号
            if checkTeacher == 1:
                print '无法在教师的信息表里查询到该教师的信息'

    #根据课程ID和已赋值的全局变量teacherID生成classlist（也是global类型）
    def getList(self,CourseID):
        with open('data/courseInfo.csv', 'rb') as courseInfo:
            reader = csv.reader(courseInfo)
            reader.next()
            for cline in reader:
                if (cline[0] == CourseID) & (cline[2] == Timer.teacherID):
                    Timer.classlist.append(cline[3])
                else:
                    pass

    #将教师的信息加入队列
    def enqueue(self,CourseID):

        testTime = time.strftime('%H:%M',time.localtime())

        messagelist = [Timer.teacherID, CourseID, Timer.classlist, Timer.nowtime]
        if Timer.List != True:  # 判断队列是否为空  空列表即为false
            Timer.List.append(messagelist)  # 将需要加入的信息加入队列
        else:
            for line in Timer.List:
                if (set(Timer.classlist) & set(line[2])):  # 判断当前的的班级是否在队列中已存在
                    RElist = messagelist  # 设置当班级重现重复上课时教师的信息
                    if Timer.compare_time(testTime,Timer.Time[1],Timer.Time[2]) or \
                        Timer.compare_time(testTime,Timer.Time[3],Timer.Time[4]) or \
                            Timer.compare_time(testTime, Timer.Time[5], Timer.Time[6]) :

                        Timer.List.remove(RElist)  # 将该教师信息踢出　其后的向前移动
                        Timer.List.append(messagelist)  # 将后进入的教师的信息加入队列
                else:
                    print '当前班级已经在考勤之中，无法继续开始考勤'
    #生成学生考勤信息表的文件名，并返回考勤次序号
    def checkRecord(self,CourseID):
        # 开始在考勤次序表中记录教师的考勤信息
        cmd = 'csvcut -c TeacherID,CourseID,SeqID  data/seq.csv' + '> data/seqnew.csv'
        os.popen(cmd)
        with open('data/seqnew.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
#            reader.next()
            seqID = '0'
            for line in reader:
                if (line[0] == Timer.teacherID) & (line[1] == CourseID):
                    seqID = line[2]
                else:
                    pass
            seqID = int(seqID) + 1
            Timer.checkfileName = 'data/' + str(Timer.teacherID) + '_' + str(CourseID) + '_' + \
                                  str(seqID) + '_' + 'checkinDetail.csv'  # 换行符　'\'　可以将一行长代码换成多行
            os.remove('data/seqnew.csv')
            return seqID
    #教师开启考勤
    def startcheckin(self, teacherWechatID, CourseID):

        self.findTeacherId(teacherWechatID)

        self.getList(CourseID)

        self.enqueue(CourseID)

        seqID = self.checkRecord(CourseID)

        # 在考勤信息总表（seq.csv）中记录教师本次考勤信息
        with open('data/seq.csv', 'a+') as seq:
            writer = csv.writer(seq)
            seqlist = [Timer.teacherID, CourseID, str(seqID), Timer.nowtime]
            writer.writerow(seqlist)

        # 生成学生考勤信息表,并写入表头
        with open(Timer.checkfileName, 'a') as checkfile:
            writer = csv.writer(checkfile)
            message0 = ['StuID', 'checkTime', 'ProofPath', 'checkinType', 'IsSucc', 'checkinResult']
            writer.writerow(message0)
        print '您已开始考勤！'

    #停止考勤
    def stopCheckin(self):
        timedev = 90 * 60
        if Timer.timeCheck(timedev)==False :
            leaveTime = Timer.List[0][3]   #??
            leaveTimeArray=leaveTime.split('-| | :')

            beginTime = Timer.List[1][3]
            beginTimeArray = beginTime.split('-| | :')

            # 获得时间的差值 并将其赋给计时器
            timedev=(int(beginTimeArray[3])-int(leaveTime[3]))*3600+(int(beginTimeArray[4])-int(leaveTime[4]))*60+ \
                    (int(beginTimeArray[5]) - int(leaveTime[5]))

            Timer.timeCheck(timedev)  #传递一个参数给计时器

            Timer.List.pop(0)  #将教师踢出队列


    #教师开启抽点
    def teaRadomCheckIn(self, CourseID, seq, _stuID=[]):

        # 根据CourseID找到TeacherID
        csvfile = open('data/courseInfo.csv', 'r')
        reader = csv.reader(csvfile)
        reader.next()
        for line in reader:
            if CourseID == line[0]:
                TeacherID = line[2]  # line[2]:教工号  line[0]:课程号
                break
        filename = open('data/' + TeacherID + '_' + CourseID + '_' + seq + '_' + 'checkinDetail.csv', 'a+')  # 每次考勤对应一个文件
        _file = open('data/studentInfo.csv', 'r')

        _file.next()
        checkinType = 'Radom'

        for line in _file:
            Data = line.split(',')
            for i in range(len(_stuID)):
                if _stuID[i] == Data[0]:
                    list = [Data[0] + ',' + checkinType + ',  ' + ',  ' + ',' + Data[-1]]
                    filename.write(list)
        _file.close()
        filename.close()
        #预先动态生成保存本次学生考勤信息的文件
        _filename = open('data/' + TeacherID + '_' + CourseID + '_' + seq + '_' + 'CheckDetial.csv', 'a+')
        _filename.close()

    #让教师选择要抽点的学生学号范围，并返回次范围
    def choseStuID(self):
        stuIDList = []
        wechatIDList = []
        # 输入学号范围，并把该范围内的学号储存
        staStuID = raw_input("请输入想要抽点的学生的起始学号：")
        endStuID = raw_input("请输入想要抽点的学生的终止学号：")
        for id in range(string.atoi(staStuID), string.atoi(endStuID) + 1):
            stuIDList.append(str(id))

        # 根据学号找到微信号，并把微信号入队
        with open('data/studentInfo.csv', 'rb') as studentInfo:
            reader = csv.reader(studentInfo)
            reader.next()
            for readline in reader:
                for id in stuIDList:
                    print readline[0]
                    if readline[0] == id:
                        wechatIDList.append(readline[3])
        # 返回多个微信号
        return wechatIDList

    #判断有没有这个班级
    def weatherClass(self):
        #教师输入想要抽点的班级名称
        classID = raw_input("请输入想要抽点的班级名称（如：软件工程1401）：")

        # 检查是否有这个班级
        flag = 0
        filename = 'data/studentInfo.csv'
        with open(filename, 'rb') as studentInfo:
            reader = csv.reader(studentInfo)
            reader.next()
            for readline in reader:
                if readline[2] == classID:
                    flag = 1
                    print '有这个班级'
                    return True
        if flag == 0:
            print '没有这个班级'
            return False
if __name__ == '__main__' :
    teacherWechatID = 'wonka80'
    CourseID = '51610189'

    t = Teacher()
    t.startcheckin(teacherWechatID,CourseID)
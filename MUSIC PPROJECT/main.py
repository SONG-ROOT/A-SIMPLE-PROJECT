#coding=utf-8
import os,sys,ctypes
from PyQt5.QtWidgets import QMainWindow,QApplication,QDesktopWidget,QTextEdit,QPushButton\
    ,QMessageBox,QLabel,QFileDialog,QTabWidget,QWidget,QCheckBox,QAction
from PyQt5.QtCore import Qt
import json

import ID#私有模块
import URL_1#私有模块
import HEBING#私有模块

if os.name=='nt':
    whnd1 = ctypes.windll.kernel32.GetConsoleWindow()#在 WINDOWS 上隐藏控制台
    ctypes.windll.user32.ShowWindow(whnd1, 0)
    ctypes.windll.kernel32.CloseHandle(whnd1)
elif os.name=='posix':
    print("当前系统：LINUX/UNIX ,NICE!")

################################ MAIN CONTROL ######################################
class Dmain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path=''#要扫描的目录
        self.userid=os.getlogin()#用户名
        self.errid=''#出错的ID记录
        self.SONG_IMFORMATION=''#歌曲信息：包括艺人名，专辑名，歌曲名。用于合成文件名
        self.SONG_WILL_BE_SAVE=''#提取完成的歌词和翻译文本

        self.ID_LIST=''#批列表
        self.error_info=''#批错误

        self.I_WANT_TO_SAY='用Python脚本从网易云抓取带时间戳的歌词并保存成lrc格式的文件\n目的:\
        \n这个脚本的目的是根据ID（网易云音乐每首歌有唯一对应的ID）提取翻译\n我的目标：\
        \n我希望在自己能用的基础上，热爱音乐的人也能用的上。当然要比较懂计算机才能用的好。\n适用人群：\
        \n热爱音乐的网易云中国用户。仅供音乐热爱者个人使用，未经允许拿去做爬虫，商业化，先死个妈\n软件编写：\n使用python PYQT5第三方库构建图形化界面。\
        \n使用requests库联网发送请求。\n使用JSON库数据类型转换。\n使用re库匹配时间戳提取。\
        \n在linux,windows上均可运行.\n\n                                             ---by 宋健 2020.5.31'

        self.initUI()
        

    def initUI(self):
        self.setGeometry(200, 150, 1152,648)
        self.center()#窗口居中
        self.my_ui()#纯UI
        self.SET_UI_EVENT()#BUTTON CLICK EVENT
        self.setWindowTitle('网易云歌词提取')
        self.show()
        
    def SET_UI_EVENT(self):#UI点击事件
        if os.name=='nt':
            self.QTextEdit_1.setText(os.path.join(r'C:\Users',self.userid,'AppData','Local','Netease','CloudMusic','webdata','lyric'))
        elif os.name=='posix':
            self.QTextEdit_1.setText(os.path.join('/home',self.userid,'.cache','netease-cloud-music','TempFiles')) 
        self.button_1.clicked.connect(self.path_choose)        
        self.button_2.clicked.connect(self.ID_GET)  
        self.button_3.clicked.connect(self.URL_R)
        self.button_4.clicked.connect(self.SAVE_1)  
        self.button_5.clicked.connect(self.SAVE_2)
        self.button_6.clicked.connect(self.BATCH_SAVE)
        self.button_7.clicked.connect(self.SAVE_4)

##################################### TEST ONLY ##########################################
    def path_choose(self):
        fname = QFileDialog.getExistingDirectory(self, '选择要扫描的目录', '/home/')
        if fname:
            self.QTextEdit_1.setText(fname)
        else:
            QMessageBox.warning(self,'空路径','至少选择一个路径!    ')
            
    def ID_GET(self):
        if self.DEEP_SCAN.isChecked()==False:
            self.path=self.QTextEdit_1.toPlainText()
            self.IDLIST=ID.ID_GET(self.path)
            self.QTextEdit_2.setText(self.IDLIST)
        else:
            self.path=self.QTextEdit_1.toPlainText()
            self.IDLIST=ID.OPEN_FILE_DEEPIN(self.path)
            self.QTextEdit_2.setText(self.IDLIST)

    def URL_R(self):            #ID提取测试平台
        n=self.QTextEdit_3.toPlainText()#MUSIC ID
        a=URL_1.URL_GET(n)#拿到服务器返回的JSON
        if a=='非法数字':
            self.QTextEdit_4.setText('不要调皮,请传入正确ID')
        elif a=='timeout':
            self.errid=self.errid+','+n
            self.QTextEdit_4.setText('与服务器建立连接失败,网络不通畅？\nERROR ID：'+self.errid)
            self.QTextEdit_5.setText('ERROR ID：'+self.errid)
        elif a!='非法数字' and a!='timeout':
            jss=URL_1.json_wrap(a)#数据筛选
            if jss=='不存在的歌曲ID!':
                self.errid=self.errid+','+n
                self.QTextEdit_4.setText('与服务器建立连接成功，但没有提取到歌曲基本信息，这个ID 没有对应的歌曲？\nERROR ID：'+self.errid)
                self.QTextEdit_5.setText('ERROR ID：'+self.errid)
            else:#拿到歌曲信息并打印,第一步完成
                self.SONG_IMFORMATION=jss
                song_info=jss.split(',',-1)
                self.QTextEdit_7.setText('艺人名：'+song_info[0]+'\n曲名：'+song_info[1]+'\n专辑名：'+song_info[2])

                TRANS=URL_1.URL_GET_translation(n)#获取JSON
                if TRANS=='timeout':
                    self.errid=self.errid+','+n
                    self.QTextEdit_4.setText('已获取歌曲信息，但与服务器建立新连接获取歌词失败，网络不通畅?\nERROR ID：'+self.errid)
                    self.QTextEdit_5.setText('ERROR ID：'+self.errid)
                else:
                    TRANSlation=URL_1.json_wrap_tras(TRANS)#数据清洗
                    #self.QTextEdit_4.setText(str(TRANSlation))
                    if TRANSlation == '无歌词':
                        self.errid=self.errid+','+n
                        self.QTextEdit_4.setText('已获取歌曲信息，与服务器建立新连接获取歌词成功，但歌曲无歌词，\nERROR ID：'+self.errid)
                        self.QTextEdit_5.setText('ERROR ID：'+self.errid)
                    elif TRANSlation == '未收录':
                        self.errid=self.errid+','+n
                        self.QTextEdit_4.setText('已获取歌曲信息，与服务器建立新连接获取歌词成功，但该歌曲未收录，\nERROR ID：'+self.errid)
                        self.QTextEdit_5.setText('ERROR ID：'+self.errid)
                    elif TRANSlation[1]=='无翻译' or self.NO_NEED_TRA.isChecked()==True or TRANSlation[1]=='没有翻译且大概率是无时间戳歌词':
                        ssd=HEBING.SIMPLE_NO_TRA(TRANSlation)
                        self.QTextEdit_4.setText(ssd)
                    else:
                        kklp=self.QTextEdit_6.toPlainText()
                        ssd=HEBING.LIST_BULID(TRANSlation,kklp)
                        self.QTextEdit_4.setText(ssd)
                        self.SONG_WILL_BE_SAVE=ssd

###################################### 批量保存 ################################################
    def BATCH_SAVE(self):
        n=self.QTextEdit_9.toPlainText()
        try:
            self.ID_LIST=n.split(',',-1)
        except Exception as err:
            self.error_info=self.error_info+str(err)
            self.QTextEdit_10.setText(self.error_info)       
            return 0     
        for i in self.ID_LIST:
            print(i)
            a=URL_1.URL_GET(i)#拿到服务器返回的JSON
            if a=='非法数字':
                self.error_info=self.error_info+'不要调皮,请传入正确ID\n'
                self.QTextEdit_10.setText(self.error_info)
            elif a=='timeout':
                self.error_info=self.error_info+'与服务器建立连接失败,网络不通畅？ERROR ID：'+str(i)+'\n'
                self.QTextEdit_10.setText(self.error_info)
            elif a!='非法数字' and a!='timeout':
                jss=URL_1.json_wrap(a)#数据筛选
                if jss=='不存在的歌曲ID!':
                    self.error_info=self.error_info+'与服务器建立连接成功，但没有提取到歌曲基本信息，这个ID 没有对应的歌曲？ERROR ID：'+str(i)+'\n'
                    self.QTextEdit_10.setText(self.error_info)
                else:#第一步完成
                    self.SONG_IMFORMATION=jss
                    TRANS=URL_1.URL_GET_translation(i)#获取JSON
                    if TRANS=='timeout':
                        self.error_info=self.error_info+'已获取歌曲信息，但与服务器建立新连接获取歌词失败，网络不通畅？ERROR ID：'+str(i)+'\n'
                        self.QTextEdit_10.setText(self.error_info)
                    else:
                        TRANSlation=URL_1.json_wrap_tras(TRANS)#数据清洗
                        if TRANSlation == '无歌词':
                            self.error_info=self.error_info+'已获取歌曲信息，与服务器建立新连接获取歌词成功，但歌曲无歌词？ERROR ID：'+str(i)+'\n'
                            self.QTextEdit_10.setText(self.error_info)
                        elif TRANSlation == '未收录':
                            self.error_info=self.error_info+'已获取歌曲信息，与服务器建立新连接获取歌词成功，但该歌曲未收录？ERROR ID：'+str(i)+'\n'
                            self.QTextEdit_10.setText(self.error_info)
                        elif TRANSlation[1]=='无翻译' or self.DO_NOT_TRANSLATE.isChecked()==True  or TRANSlation[1]=='没有翻译且大概率是无时间戳歌词':
                            ssd=HEBING.SIMPLE_NO_TRA(TRANSlation)
                            self.error_info=self.error_info+'DONE!,成功 ID：'+str(i)+'\n'
                            self.QTextEdit_10.setText(self.error_info)
                            self.SONG_WILL_BE_SAVE=ssd
                            self.SAVE_3()
                        else:
                            kklp=self.QTextEdit_12.toPlainText()
                            ssd=HEBING.LIST_BULID(TRANSlation,kklp)
                            self.error_info=self.error_info+'DONE!,成功 ID：'+str(i)+'\n'
                            self.QTextEdit_10.setText(self.error_info)
                            self.SONG_WILL_BE_SAVE=ssd
                            self.SAVE_3()
        QMessageBox.information(self,'NICE','DONE!')
######################################## SAVE #############################################
    def Special_Character_Clean(self,text):
        f=text.replace('<','').replace('>','').replace('|','').replace('*','').replace('"','')
        s=f.replace('?','').replace(':','').replace('/','').replace('‪','').replace('\\','')
        return s
    def SAVE_1(self):
        fname = QFileDialog.getExistingDirectory(self, '选择要扫描的目录', '/home/')
        if fname:
            self.QTextEdit_8.setText(fname)
        else:
            QMessageBox.warning(self,'空路径','至少选择一个路径!    ')

    def SAVE_2(self):
        try:
            name_1=self.SONG_IMFORMATION.split(',',-1)
            name_2=name_1[0]+' - '+name_1[1]+'.lrc'
            name=self.Special_Character_Clean(name_2)
            path_1=self.QTextEdit_8.toPlainText()
            
            path_2=os.path.join(path_1,name)
            PATH=os.path.normpath(path_2)  #规范路径
            with open(PATH,'w',encoding='utf-8') as u:
                u.write(self.SONG_WILL_BE_SAVE)
            QMessageBox.information(self,'nice','保存成功!')
        except Exception as f:
            self.QTextEdit_4.setText(str(f))

    def SAVE_3(self):
        try:
            name_1=self.SONG_IMFORMATION.split(',',-1)
            name_2=name_1[0]+' - '+name_1[1]+'.lrc'
            name=self.Special_Character_Clean(name_2)
            path_1=self.QTextEdit_13.toPlainText()
            
            path_2=os.path.join(path_1,name)
            PATH=os.path.normpath(path_2)  #规范路径
            with open(PATH,'w',encoding='utf-8') as u:
                u.write(self.SONG_WILL_BE_SAVE)
            #QMessageBox.information(self,'nice','保存成功!')
        except Exception as f:
            self.error_info=self.error_info+'文件保存时，处理错误!,失败 ID：'+str(i)
            self.QTextEdit_10.setText(self.error_info)
    def SAVE_4(self):
        fname = QFileDialog.getExistingDirectory(self, '选择要扫描的目录', '/home/')
        if fname:
            self.QTextEdit_13.setText(fname)
        else:
            QMessageBox.warning(self,'空路径','至少选择一个路径!    ')

#################################################  UI  ##################################### 
    def center(self):#窗口对齐
        qr = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center_point)
        self.move(qr.topLeft())
    def my_ui(self):#仅仅画出程序UI
        self.tabWidget_1 = QTabWidget(self);self.tabWidget_1.setGeometry(10,30,1130,600)
        self.tab_1= QWidget();self.tab_2= QWidget();self.tab_3= QWidget()
        self.tabWidget_1.addTab(self.tab_1, "歌曲选取");self.tabWidget_1.addTab(self.tab_2, "歌曲提取测试台");self.tabWidget_1.addTab(self.tab_3, "批量提取")
        
        #################### PAGE 1########################
        self.label_1 = QLabel('输入要扫描的路径：',self.tab_1);self.label_1.setGeometry(10,5,150,30)
        self.QTextEdit_1 = QTextEdit(self.tab_1);self.QTextEdit_1.setGeometry(170,5,850,40)
        self.button_1 = QPushButton("路径选择",self.tab_1);self.button_1.setGeometry(10,60,100,30)
        self.button_2 = QPushButton("开始扫描",self.tab_1);self.button_2.setGeometry(120,60,100,30)
        self.QTextEdit_2 = QTextEdit("提示: 双击选中文字！鼠标右键copy",self.tab_1);self.QTextEdit_2.setGeometry(170,120,850,150)
        self.DEEP_SCAN=QCheckBox('打开文件扫描 for linux', self.tab_1);self.DEEP_SCAN.move(10,350)
        self.DEEP_SCAN.setChecked(False)
        ############################### PAGE 2 ##########################
        self.label_3 = QLabel('MUSIC ID：(测试)',self.tab_2);self.label_3.setGeometry(10,5,150,30)
        self.QTextEdit_3 = QTextEdit(self.tab_2);self.QTextEdit_3.setGeometry(170,5,300,40)
        self.button_3 = QPushButton("发送",self.tab_2);self.button_3.setGeometry(10,60,100,30)
        self.QTextEdit_4 = QTextEdit(self.tab_2);self.QTextEdit_4.setGeometry(170,60,850,400)

        self.label_3= QLabel('失败 ID:',self.tab_2);self.label_3.setGeometry(500,5,170,30)
        self.QTextEdit_5 = QTextEdit(self.tab_2);self.QTextEdit_5.setGeometry(580,5,520,40)

        self.label_4 = QLabel("翻译原文\n连接符",self.tab_2);self.label_4.setGeometry(10,100,100,100)
        self.QTextEdit_6 = QTextEdit(self.tab_2);self.QTextEdit_6.setGeometry(10,180,100,150)
        self.QTextEdit_6.setText('    ')

        self.label_5 = QLabel("歌曲信息",self.tab_2);self.label_5.setGeometry(10,410,100,80)
        self.QTextEdit_7 = QTextEdit(self.tab_2);self.QTextEdit_7.setGeometry(10,465,300,90)
        self.QTextEdit_7.setText('艺人名：曲名：专辑名：')

        self.label_6 = QLabel("保存在哪个目录?",self.tab_2);self.label_6.setGeometry(410,465,150,50)
        self.QTextEdit_8 = QTextEdit(self.tab_2);self.QTextEdit_8.setGeometry(560,465,400,40)
        self.button_4 = QPushButton("路径选择",self.tab_2);self.button_4.setGeometry(1000,465,100,30)
        self.button_5 = QPushButton("点击保存",self.tab_2);self.button_5.setGeometry(1000,500,100,30)

        self.NO_NEED_TRA=QCheckBox('不需要中文翻译', self.tab_2);self.NO_NEED_TRA.move(10,350)
        self.NO_NEED_TRA.setChecked(False)
        ######################## PAGE 3 ##################################
        self.label_7 = QLabel('批量保存',self.tab_3);self.label_7.setGeometry(10,5,150,30)
        self.QTextEdit_9 = QTextEdit(self.tab_3);self.QTextEdit_9.setGeometry(170,5,300,40)
        self.button_6 = QPushButton("开始",self.tab_3);self.button_6.setGeometry(10,60,100,30)
        self.QTextEdit_10 = QTextEdit(self.tab_3);self.QTextEdit_10.setGeometry(170,60,850,200)
        self.label_9 = QLabel("翻译原文\n连接符",self.tab_3);self.label_9.setGeometry(10,100,100,100)
        self.QTextEdit_12 = QTextEdit(self.tab_3);self.QTextEdit_12.setGeometry(10,180,100,150)
        self.QTextEdit_12.setText('    ')
        self.label_10 = QLabel("保存在哪个目录?",self.tab_3);self.label_10.setGeometry(410,465,150,50)
        self.QTextEdit_13 = QTextEdit(self.tab_3);self.QTextEdit_13.setGeometry(560,465,400,40)
        self.button_7 = QPushButton("路径选择",self.tab_3);self.button_7.setGeometry(1000,465,100,30)
        self.QTextEdit_14 = QTextEdit(self.tab_3);self.QTextEdit_14.setGeometry(170,300,850,150)
        self.QTextEdit_14.setText('使用须知：\nID 格式：ID,ID,ID,ID\nID与ID之间由逗号(,)隔开\n注意是英文逗号,不是汉语逗号\nPython脚本WINDOWS，LINUX均可运行')
        self.QTextEdit_14.setTextInteractionFlags(Qt.NoTextInteraction)
        self.DO_NOT_TRANSLATE=QCheckBox('不需要中文翻译', self.tab_3);self.DO_NOT_TRANSLATE.move(10,350)
        self.DO_NOT_TRANSLATE.setChecked(False)
        ######################## 
        exitAction = QAction( '&软件介绍', self)#菜单下拉项 显示内容         
        exitAction.setShortcut('Ctrl+B')# 此操作的快捷方式
        exitAction.setStatusTip('我要说的。balabala')#菜单下拉项 状态栏显示内容

        self.statusBar()#创建一个菜单栏
        fileMenu =self.menuBar().addMenu('&总控制台')#菜单栏中添加主项
        fileMenu.addAction(exitAction)#添加写好的exitAction事件
        exitAction.triggered.connect(self.TELL_ABOUT)
    def TELL_ABOUT(self):
        QMessageBox.about(self,"标题",self.I_WANT_TO_SAY)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dmain()
    sys.exit(app.exec_())
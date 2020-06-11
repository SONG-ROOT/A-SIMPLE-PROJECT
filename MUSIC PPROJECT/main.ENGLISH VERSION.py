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
    print("Current operating system：LINUX/UNIX ,NICE!")

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

        self.I_WANT_TO_SAY='Use Python script to grab time stamped lyrics from Netease cloud and save them as LRC files\nobjective:\
        \nThe purpose of this script is to extract the translation according to the ID (each song of Netease cloud music has a unique corresponding ID)\nMy goal：\
        \nI hope that people who love music can use it on the basis of I can use fisrt. Of course, it"s better to understand computers.\nApplicable population：\
        \nChinese users of Netease cloud who love music. It"s only for music lovers" personal use.Those who use it as Crawler without permission, or commercialize it, you die first\nSoftware writing：\nUse Python pyqt5 third-party library to build graphical interface.\
        \nUse the requests library to send requests online.\nUse JSON library data type conversion.\nUse re library to match timestamp extraction.\
        \nIt can run on Linux and windows. \n\n                                             ---by 宋健 2020.6.1'

        self.initUI()
        

    def initUI(self):
        self.setGeometry(200, 150, 1152,648)
        self.center()#窗口居中
        self.my_ui()#纯UI
        self.SET_UI_EVENT()#BUTTON CLICK EVENT
        self.setWindowTitle('Netease cloud lyrics extraction')
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
        fname = QFileDialog.getExistingDirectory(self, 'Select directory to scan', '/home/')
        if fname:
            self.QTextEdit_1.setText(fname)
        else:
            QMessageBox.warning(self,'Empty path !','Select at least one path!    ')
            
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
            self.QTextEdit_4.setText('Don"t be naughty, please pass in the correct ID\n')
        elif a=='timeout':
            self.errid=self.errid+','+n
            self.QTextEdit_4.setText('Failed to establish a connection with the server, the network is not smooth？\nERROR ID：'+self.errid)
            self.QTextEdit_5.setText('ERROR ID：'+self.errid)
        elif a!='非法数字' and a!='timeout':
            jss=URL_1.json_wrap(a)#数据筛选
            if jss=='不存在的歌曲ID!':
                self.errid=self.errid+','+n
                self.QTextEdit_4.setText('The connection with the server was established successfully, but the basic information of the song was not extracted. There is no corresponding song for this ID？\nERROR ID：'+self.errid)
                self.QTextEdit_5.setText('ERROR ID：'+self.errid)
            else:#拿到歌曲信息并打印,第一步完成
                self.SONG_IMFORMATION=jss
                song_info=jss.split(',',-1)
                self.QTextEdit_7.setText('Artist Name：'+song_info[0]+'\nSong Name：'+song_info[1]+'\nAlbum Name：'+song_info[2])

                TRANS=URL_1.URL_GET_translation(n)#获取JSON
                if TRANS=='timeout':
                    self.errid=self.errid+','+n
                    self.QTextEdit_4.setText('Got song information, but failed to establish a new connection with the server to get lyrics, the network is not smooth?\nERROR ID：'+self.errid)
                    self.QTextEdit_5.setText('ERROR ID：'+self.errid)
                else:
                    TRANSlation=URL_1.json_wrap_tras(TRANS)#数据清洗
                    #self.QTextEdit_4.setText(str(TRANSlation))
                    if TRANSlation == '无歌词':
                        self.errid=self.errid+','+n
                        self.QTextEdit_4.setText('The song information has been obtained. A new connection has been established with the server to obtain the lyrics successfully, but the song has no lyrics，\nERROR ID：'+self.errid)
                        self.QTextEdit_5.setText('ERROR ID：'+self.errid)
                    elif TRANSlation == '未收录':
                        self.errid=self.errid+','+n
                        self.QTextEdit_4.setText('The song information has been obtained, and a new connection with the server has been established to obtain the lyrics successfully, but the song is not included，\nERROR ID：'+self.errid)
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
            a=URL_1.URL_GET(i)#拿到服务器返回的JSON
            if a=='非法数字':
                self.error_info=self.error_info+'Don"t be naughty, please pass in the correct ID\n'
                self.QTextEdit_10.setText(self.error_info)
            elif a=='timeout':
                self.error_info=self.error_info+'Failed to establish a connection with the server, the network is not smooth？\nERROR ID：'+str(i)+'\n'
                self.QTextEdit_10.setText(self.error_info)
            elif a!='非法数字' and a!='timeout':
                jss=URL_1.json_wrap(a)#数据筛选
                if jss=='不存在的歌曲ID!':
                    self.error_info=self.error_info+'The connection with the server was established successfully, but the basic information of the song was not extracted. There is no corresponding song for this ID \nERROR ID：'+str(i)+'\n'
                    self.QTextEdit_10.setText(self.error_info)
                else:#第一步完成
                    self.SONG_IMFORMATION=jss
                    TRANS=URL_1.URL_GET_translation(i)#获取JSON
                    if TRANS=='timeout':
                        self.error_info=self.error_info+'Got song information, but failed to establish a new connection with the server to get lyrics, the network is not smooth？\nERROR ID：'+str(i)+'\n'
                        self.QTextEdit_10.setText(self.error_info)
                    else:
                        TRANSlation=URL_1.json_wrap_tras(TRANS)#数据清洗
                        if TRANSlation == '无歌词':
                            self.error_info=self.error_info+'The song information has been obtained. A new connection has been established with the server to obtain the lyrics successfully, but the song has no lyrics？\nERROR ID：'+str(i)+'\n'
                            self.QTextEdit_10.setText(self.error_info)
                        elif TRANSlation == '未收录':
                            self.error_info=self.error_info+'The song information has been obtained, and a new connection with the server has been established to obtain the lyrics successfully, but the song is not included？\nERROR ID：'+str(i)+'\n'
                            self.QTextEdit_10.setText(self.error_info)
                        elif TRANSlation[1]=='无翻译' or self.DO_NOT_TRANSLATE.isChecked()==True  or TRANSlation[1]=='没有翻译且大概率是无时间戳歌词':
                            ssd=HEBING.SIMPLE_NO_TRA(TRANSlation)
                            self.error_info=self.error_info+'DONE! Success ID：'+str(i)+'\n'
                            self.QTextEdit_10.setText(self.error_info)
                            self.SONG_WILL_BE_SAVE=ssd
                            self.SAVE_3()
                        else:
                            kklp=self.QTextEdit_12.toPlainText()
                            ssd=HEBING.LIST_BULID(TRANSlation,kklp)
                            self.error_info=self.error_info+'DONE!,Success ID：'+str(i)+'\n'
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
        fname = QFileDialog.getExistingDirectory(self, 'Select directory to scan', '/home/')
        if fname:
            self.QTextEdit_8.setText(fname)
        else:
            QMessageBox.warning(self,'Empty path','Select at least one path!    ')

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
            QMessageBox.information(self,'nice','Saved successfully!')
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
            self.error_info=self.error_info+'Processing error while saving file!,error ID：'+str(i)
            self.QTextEdit_10.setText(self.error_info)
    def SAVE_4(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select directory to scan', '/home/')
        if fname:
            self.QTextEdit_13.setText(fname)
        else:
            QMessageBox.warning(self,'Empty path','Select at least one path!    ')

#################################################  UI  ##################################### 
    def center(self):#窗口对齐
        qr = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center_point)
        self.move(qr.topLeft())
    def my_ui(self):#仅仅画出程序UI
        self.tabWidget_1 = QTabWidget(self);self.tabWidget_1.setGeometry(10,30,1130,600)
        self.tab_1= QWidget();self.tab_2= QWidget();self.tab_3= QWidget()
        self.tabWidget_1.addTab(self.tab_1, "Song selection");self.tabWidget_1.addTab(self.tab_2, "SINGLE TEST");self.tabWidget_1.addTab(self.tab_3, "Batch extraction")
        
        #################### PAGE 1########################
        self.label_1 = QLabel('Enter path scan：',self.tab_1);self.label_1.setGeometry(10,5,150,30)
        self.QTextEdit_1 = QTextEdit(self.tab_1);self.QTextEdit_1.setGeometry(170,5,850,40)
        self.button_1 = QPushButton("path choose",self.tab_1);self.button_1.setGeometry(10,60,110,30)
        self.button_2 = QPushButton("start scan",self.tab_1);self.button_2.setGeometry(120,60,100,30)
        self.QTextEdit_2 = QTextEdit("Tip: double click the selected text! Right mouse button to copy",self.tab_1);self.QTextEdit_2.setGeometry(170,120,850,150)
        self.DEEP_SCAN=QCheckBox('Open file scan for linux', self.tab_1);self.DEEP_SCAN.move(10,350)
        self.DEEP_SCAN.setChecked(False)
        ############################### PAGE 2 ##########################
        self.label_3 = QLabel('MUSIC ID：(TEST)',self.tab_2);self.label_3.setGeometry(10,5,150,30)
        self.QTextEdit_3 = QTextEdit(self.tab_2);self.QTextEdit_3.setGeometry(170,5,300,40)
        self.button_3 = QPushButton("submit",self.tab_2);self.button_3.setGeometry(10,60,100,30)
        self.QTextEdit_4 = QTextEdit(self.tab_2);self.QTextEdit_4.setGeometry(170,60,850,400)

        self.label_3= QLabel('error ID:',self.tab_2);self.label_3.setGeometry(500,5,170,30)
        self.QTextEdit_5 = QTextEdit(self.tab_2);self.QTextEdit_5.setGeometry(580,5,520,40)

        self.label_4 = QLabel("how to link \ntranslate",self.tab_2);self.label_4.setGeometry(10,100,100,100)
        self.QTextEdit_6 = QTextEdit(self.tab_2);self.QTextEdit_6.setGeometry(10,180,100,150)
        self.QTextEdit_6.setText('    ')

        self.label_5 = QLabel("Song info",self.tab_2);self.label_5.setGeometry(10,410,100,80)
        self.QTextEdit_7 = QTextEdit(self.tab_2);self.QTextEdit_7.setGeometry(10,465,300,90)
        self.QTextEdit_7.setText('Artist Name：Song Name：Album Name:')

        self.label_6 = QLabel("what path save?",self.tab_2);self.label_6.setGeometry(410,465,150,50)
        self.QTextEdit_8 = QTextEdit(self.tab_2);self.QTextEdit_8.setGeometry(560,465,400,40)
        self.button_4 = QPushButton("path",self.tab_2);self.button_4.setGeometry(1000,465,100,30)
        self.button_5 = QPushButton("click save",self.tab_2);self.button_5.setGeometry(1000,500,100,30)

        self.NO_NEED_TRA=QCheckBox('No Chinese \ntranslation \nrequired', self.tab_2);self.NO_NEED_TRA.move(10,350)
        self.NO_NEED_TRA.setChecked(False)
        ######################## PAGE 3 ##################################
        self.label_7 = QLabel('Batch save',self.tab_3);self.label_7.setGeometry(10,5,150,30)
        self.QTextEdit_9 = QTextEdit(self.tab_3);self.QTextEdit_9.setGeometry(170,5,300,40)
        self.button_6 = QPushButton("start",self.tab_3);self.button_6.setGeometry(10,60,100,30)
        self.QTextEdit_10 = QTextEdit(self.tab_3);self.QTextEdit_10.setGeometry(170,60,850,200)
        self.label_9 = QLabel("how to link \ntranslate",self.tab_3);self.label_9.setGeometry(10,100,100,100)
        self.QTextEdit_12 = QTextEdit(self.tab_3);self.QTextEdit_12.setGeometry(10,180,100,150)
        self.QTextEdit_12.setText('    ')
        self.label_10 = QLabel("what path save?",self.tab_3);self.label_10.setGeometry(410,465,150,50)
        self.QTextEdit_13 = QTextEdit(self.tab_3);self.QTextEdit_13.setGeometry(560,465,400,40)
        self.button_7 = QPushButton("path",self.tab_3);self.button_7.setGeometry(1000,465,100,30)
        self.QTextEdit_14 = QTextEdit(self.tab_3);self.QTextEdit_14.setGeometry(170,300,850,150)
        self.QTextEdit_14.setText('Instructions for use：\nID format：ID,ID,ID,ID\nSeparate ID from ID by ,\nNotice it”s English , not Chinese ，\nPython scripts can run on Windows and on LINUX')
        self.QTextEdit_14.setTextInteractionFlags(Qt.NoTextInteraction)
        self.DO_NOT_TRANSLATE=QCheckBox('No Chinese\n translation\n required', self.tab_3);self.DO_NOT_TRANSLATE.move(10,350)
        self.DO_NOT_TRANSLATE.setChecked(False)
        ######################## 
        exitAction = QAction( '&Software introduction', self)#菜单下拉项 显示内容         
        exitAction.setShortcut('Ctrl+B')# 此操作的快捷方式
        exitAction.setStatusTip('i want to say。balabala')#菜单下拉项 状态栏显示内容

        self.statusBar()#创建一个菜单栏
        fileMenu =self.menuBar().addMenu('&CTRL')#菜单栏中添加主项
        fileMenu.addAction(exitAction)#添加写好的exitAction事件
        exitAction.triggered.connect(self.TELL_ABOUT)
    def TELL_ABOUT(self):
        QMessageBox.about(self,"Tittle",self.I_WANT_TO_SAY)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dmain()
    sys.exit(app.exec_())
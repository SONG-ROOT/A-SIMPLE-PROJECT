#coding=utf-8
import os,sys,ctypes
from PyQt5.QtWidgets import QMainWindow,QApplication,QDesktopWidget,QTextEdit,QPushButton\
    ,QMessageBox,QLabel,QFileDialog,QTabWidget,QWidget,QCheckBox,QAction,QComboBox
from PyQt5.QtCore import Qt
import json
import threading
import time
import re
import webbrowser

from EASY_X import ID#私有模块
from EASY_X import URL_1#私有模块
from EASY_X import HEBING#私有模块
from EASY_X import READ_CONFIG

CONFIG=READ_CONFIG.READ_CONFIG()#读取配置文件
CONFGI_ERROR=READ_CONFIG.CONFIG_CHECK(CONFIG)#检查配置文件

def CONSOLE(AAAA):#在 WINDOWS 上隐藏控制台 1 为显示，0 为隐藏
    whnd1 = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(whnd1, AAAA)
    ctypes.windll.kernel32.CloseHandle(whnd1)

if CONFGI_ERROR=='CONFGI_ERROR':
    if os.name=='nt':
        CONSOLE(1)
    print('请求头不得出现敏感词汇 且 长度需大于18！修复完成\n请重新启动')
    time.sleep(20)
    exit(0)
else:
    if os.name=='nt' and CONFIG['CMD']=='HIDE':
        CONSOLE(0)
    elif os.name=='posix':
        print("当前系统：LINUX/UNIX ,NICE!")

################################ MAIN CONTROL ######################################
class Dmain(QMainWindow):
    def __init__(self,config_import):
        super().__init__()
        self.path=''#要扫描的目录
        self.userid=os.getlogin()#当前用户名
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
        \n在linux,windows上均可运行.\n\n                                             ---by 荒野79 2020.5.31'
        
        self.CONFIG_DIC=config_import#读取的配置文件
        self.initUI()
        

    def initUI(self):
        self.setGeometry(200, 150, 1152,648)
        self.center()#窗口居中
        self.my_ui()#纯UI
        self.SET_UI_EVENT()#按钮点击事件
        self.setWindowTitle('网易云歌词提取 V1.05')
        self.show()
        
    def SET_UI_EVENT(self):#设定UI点击事件
        if os.name=='nt':#初始扫描目录显示
            self.QTextEdit_1.setText(os.path.join(r'C:\Users',self.userid,'AppData','Local','Netease','CloudMusic','webdata','lyric'))
        elif os.name=='posix':
            self.QTextEdit_1.setText(os.path.join('/home',self.userid,'.cache','netease-cloud-music','TempFiles')) 

        if self.CONFIG_DIC['SAVE_PATH']=='.':#初始保存目录设定
            pass
        else:
            self.QTextEdit_8.setText(self.CONFIG_DIC['SAVE_PATH'])
            self.QTextEdit_13.setText(self.CONFIG_DIC['SAVE_PATH'])
        self.button_1.clicked.connect(self.path_choose)        
        self.button_2.clicked.connect(self.ID_GET)  
        self.button_3.clicked.connect(self.URL_R)
        self.button_4.clicked.connect(self.SAVE_1)  
        self.button_5.clicked.connect(self.SAVE_2)
        self.button_6.clicked.connect(self.BATCH_SAVE)
        self.button_7.clicked.connect(self.SAVE_4)
        self.choose()

##################################### PAGE_1 function    ##########################################
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

###############################    PAGE_2   function     ##################################
    def URL_R(self):            #ID提取测试平台
        n=self.QTextEdit_3.toPlainText()#MUSIC ID
        a=URL_1.URL_GET(n,self.CONFIG_DIC['User-Agent'])#拿到服务器返回的JSON
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

                TRANS=URL_1.URL_GET_translation(n,self.CONFIG_DIC['User-Agent'])#获取JSON
                if TRANS=='timeout':
                    self.errid=self.errid+','+n
                    self.QTextEdit_4.setText('已获取歌曲信息，但与服务器建立新连接获取歌词失败，网络不通畅?\nERROR ID：'+self.errid)
                    self.QTextEdit_5.setText('ERROR ID：'+self.errid)
                else:
                    TRANSlation=URL_1.json_wrap_tras(TRANS)#数据清洗
                    #print(TRANSlation)
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
                        self.SONG_WILL_BE_SAVE=ssd
                    else:
                        kklp=self.QTextEdit_6.toPlainText()
                        ssd=HEBING.LIST_BULID(TRANSlation,kklp)
                        self.QTextEdit_4.setText(ssd)
                        self.SONG_WILL_BE_SAVE=ssd

###################################### page_3 function 批量保存 ################################################
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
            a=URL_1.URL_GET(i,self.CONFIG_DIC['User-Agent'])#拿到服务器返回的JSON
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
                    TRANS=URL_1.URL_GET_translation(i,self.CONFIG_DIC['User-Agent'])#获取JSON
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
######################################## page_2&3 SAVE #############################################
    def Special_Character_Clean(self,text):
        f=text.replace('<','').replace('>','').replace('|','').replace('*','').replace('"','')
        s=f.replace('?','').replace(':','').replace('/','').replace('‪','').replace('\\','')
        return s
    def SAVE_1(self):#page_2 path choose
        fname = QFileDialog.getExistingDirectory(self, '选择要扫描的目录', '/home/')
        if fname:
            self.QTextEdit_8.setText(fname)
        else:
            QMessageBox.warning(self,'空路径','至少选择一个路径!    ')

    def SAVE_2(self):#page_2
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

    def SAVE_3(self):#page_3
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
    def SAVE_4(self):#page_3 path choose
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
        self.tab_1= QWidget();self.tab_2= QWidget();self.tab_3= QWidget();self.tab_4= QWidget()
        self.tabWidget_1.addTab(self.tab_1, "歌曲选取");self.tabWidget_1.addTab(self.tab_2, "歌曲提取测试台");self.tabWidget_1.addTab(self.tab_3, "批量提取");self.tabWidget_1.addTab(self.tab_4, "实时链接转ID")
        
        #################### PAGE 1########################
        self.label_1 = QLabel('输入要扫描的路径：',self.tab_1);self.label_1.setGeometry(10,5,150,30)
        self.QTextEdit_1 = QTextEdit(self.tab_1);self.QTextEdit_1.setGeometry(170,5,850,40)
        self.button_1 = QPushButton("路径选择",self.tab_1);self.button_1.setGeometry(10,60,100,30)
        self.button_2 = QPushButton("开始扫描",self.tab_1);self.button_2.setGeometry(120,60,100,30)
        self.QTextEdit_2 = QTextEdit("提示: 双击选中文字，三击全选！鼠标右键copy",self.tab_1);self.QTextEdit_2.setGeometry(170,120,850,150)
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
        ######################## PAGE 4 ##################################
        self.label_8 = QLabel('链接输入框:',self.tab_4);self.label_8.setGeometry(10,5,150,30)
        self.QTextEdit_15 = QTextEdit(self.tab_4);self.QTextEdit_15.setGeometry(10,35,600,40)
        self.label_9 = QLabel('输出ID:',self.tab_4);self.label_9.setGeometry(10,80,150,30)
        self.QTextEdit_16 = QTextEdit(self.tab_4);self.QTextEdit_16.setGeometry(10,110,700,40)
        self.label_10 = QLabel('每过一段时间检测输入框中的内容，进行转化。\n转化前：http://music.163.com/song?id=12345678&userid=9876543210 \n转化后：12345678\n\n链接获取：打开网易云客户端，打开歌单（不管是自己的还是别人的歌单）选中音乐标题一栏中的歌名，\n点击鼠标右键，复制链接,黏贴到这里,就得到ID了\n\n\n建议时间间隔为三秒，防止刷新过快复制不到',self.tab_4)
        self.label_10.setGeometry(10,200,1000,300)

        ######################## 菜单 ####################################
        self.statusBar()#创建一个菜单栏
        fileMenu =self.menuBar().addMenu('&总控制台')#菜单栏中添加主项

        exitAction = QAction( '&软件介绍', self)#菜单下拉项 显示内容         
        exitAction.setShortcut('Ctrl+B')# 此操作的快捷方式
        exitAction.setStatusTip('我要说的。balabala')#菜单下拉项 状态栏显示内容
        exitAction.triggered.connect(self.TELL_ABOUT)
        fileMenu.addAction(exitAction)#添加写好的exitAction事件

        exitAction_1 = QAction( '&修改配置文件', self);exitAction_1.setStatusTip('修改程序的配置文件，重启后生效');fileMenu.addAction(exitAction_1);exitAction_1.triggered.connect(self.OPEN_SHELL)
        exitAction_2 = QAction( '&更新', self);fileMenu.addAction(exitAction_2);exitAction_2.triggered.connect(self.MAY_BE_LAST_VERSION)

        fileMenu_open_webbrowser =self.menuBar().addMenu('&访问')
        exitAction_webbrowser_0=QAction( 'python官网', self);fileMenu_open_webbrowser.addAction(exitAction_webbrowser_0);exitAction_webbrowser_0.triggered.connect(self.webbrower)
        exitAction_webbrowser_1=QAction( 'Github', self);fileMenu_open_webbrowser.addAction(exitAction_webbrowser_1);exitAction_webbrowser_1.triggered.connect(self.webbrower)
        exitAction_webbrowser_2=QAction( 'musicbee', self);fileMenu_open_webbrowser.addAction(exitAction_webbrowser_2);exitAction_webbrowser_2.triggered.connect(self.webbrower)

    def TELL_ABOUT(self):
        QMessageBox.about(self,"标题",self.I_WANT_TO_SAY)
    def OPEN_SHELL(self):
        def run(a):
            if os.name=='nt':
                os.system('notepad.exe config.txt')
            elif os.name=='posix':
                os.system('vi config.txt')
            else:
                pass
            print("执行了线程 ",a)
        b=threading.Thread(target=run,args=("001",))
        b.start()
####################################    PAGE_4 timer and work    ##########################################
    def choose(self):#选择时间间隔
        combo = QComboBox(self.tab_4);combo.addItem('几秒一次');combo.addItem("0.1");combo.addItem("0.5");combo.addItem("1")
        combo.addItem("2");combo.addItem("3");combo.addItem("5");combo.addItem("关闭此功能")
        combo.move(10,160)
        combo.activated[str].connect(self.onActivated)
    def onActivated(self, text):#选择时间间隔后的选项
        if text!='关闭此功能' and text!='几秒一次':
            self.time_inval=float(text)
            self.check_num_word()
        else:
            try:
                self.killTimer(self.timer_id_autodisp)#杀掉残留
                self.QTextEdit_16.setText('已经杀死计数器！')
            except:
                pass
    def check_num_word(self):#开启指定时间间隔的定时器
        try:
            self.killTimer(self.timer_id_autodisp)#新定时器前尝试杀掉残留
        except:
            pass
        self.timer_id_autodisp=self.startTimer(int(self.time_inval*1000))   #ms定时器
        self.timer_id_cnt=6000  #定时器运行次数
    def timerEvent(self, *args, **kwargs):#timer所做的事情
        QApplication.processEvents()

        input_txt=self.QTextEdit_15.toPlainText()#获取文本框内容
        IDS=re.compile(r'id=(.*?)&userid').findall(input_txt)
        if IDS !=[]:
            self.QTextEdit_16.setText(IDS[0])
        else:
            self.QTextEdit_16.setText('没有合适内容')

        self.timer_id_cnt -= 1
        if self.timer_id_cnt == 0:
            self.killTimer(self.timer_id_autodisp)
            self.QTextEdit_16.setText('计数次数已经耗尽！，请重新计数！')
###############################    WEB_OPEN    #################################
    def MAY_BE_LAST_VERSION(self):
        QMessageBox.about(self,"标题",'不出意外的话这该是最后一次功能更新了，功能方面懒得改了。我很早就发现当一首歌有两个歌手时，文件名只会是一个歌手的名字，但大部分歌曲都是一个歌手。碰到这种情况，手动复制黏贴一下另一个歌手的名字就好了。  -- 2020.8.5')
    def webbrower(self):
        sender = self.sender()#sender()方法来判断当前按下的是哪个按钮
        self.statusBar().showMessage(sender.text() + ' was pressed')
        if sender.text() =='python官网':
            webbrowser.open("https://www.python.org")
        elif sender.text() =='Github':
            webbrowser.open("https://github.com/SONG-ROOT/A-SIMPLE-PROJECT")
        elif sender.text() =='musicbee':
            webbrowser.open("https://getmusicbee.com")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dmain(CONFIG)
    sys.exit(app.exec_())
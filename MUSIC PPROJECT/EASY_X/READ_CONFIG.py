import os
import re
def READ_CONFIG():
    try:
        with open('config.txt','r',encoding='utf-8') as h:
            AS=h.readlines()
        
        K=1
        while K<100:
            for i in AS:
                if '#' in i[0]:#去除纯注释行
                    AS.remove(i)
                elif i=='\n':#去空内容行
                    AS.remove(i)
                else:
                    K=K+1
        CONTENT={}
        for f in AS:
            con=f.split('#',1)#去除后面的注释部分
            CON=con[0].split(':',1)#读取配置
            CONTENT[CON[0].replace(' ','').replace('\n','')]=CON[1].strip()
        return CONTENT
        
    except Exception as f:
        print(str(f),'    ,READ_CONFIG.py : 1. Unknow Error')
        return 'Unknow Error'

def FIX_CONFIG():
    a='#警告：如果你不知道你在做什么,你不要动这个文件\n\nCMD  :                              HIDE                      # 改成 HIDE 隐藏控制台，其余情况都会显示控制台。仅WINDOWS系统有效\nSAVE_PATH :                    .                             # 预先设定要保存的目录,避免每次重复设置路径\n\n#下面的内容是User-Agent ，乱改这个可能会出现未知错误。\n\nUser-Agent :                    None                      #默认不设置请求头 即为None\n\n#备用请求头：Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36\n#备用请求头：Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50\n#备用请求头：Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50\n#获取更多请求头，你可以访问这个网站\n#https://blog.csdn.net/chang995196962/article/details/93715295'
    with open('config.txt','w',encoding='utf-8') as h:
        h.write(a)

def CONFIG_CHECK(CONFIG):
    def USER_AGENT_CLEAN():
        rst=re.search('[\u4e00-\u9fa5]',CONFIG['User-Agent'])#中文去除
        if rst is not None:
            return '存在中文'
        ban=['python','java','c\+\+','jvav','php','robot','automaton','arachnid','spider','araneid','JavaScript','VBScript','RUBY','climb','reptile','clamber','creep','crawl']
        for gh in ban:
            rst=re.search(str(gh),CONFIG['User-Agent'],re.I)
            if rst is not None:
                return '非法字符'

    if not 'CMD' in CONFIG  or  not 'SAVE_PATH' in CONFIG or not 'User-Agent' in CONFIG :
        FIX_CONFIG()
        print('错误的配置文件,已自动修复！')
        return 'CONFGI_ERROR'
    CLEAN=USER_AGENT_CLEAN()

    if CLEAN== '存在中文' or CLEAN=='非法字符' or (len(CONFIG['User-Agent']) < 18 and CONFIG['User-Agent']!='None'):
        FIX_CONFIG()
        print('错误的配置文件,已自动修复！')
        return 'CONFGI_ERROR'
    
    
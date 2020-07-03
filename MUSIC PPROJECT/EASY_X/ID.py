import os
import json

def ID_GET(a):#所有要提取的文件，存放到表格
    music_list=[]
    if os.path.exists(a) is True:#检测目录是否存在
        pass
    else:
        print ('ID.py : 1. ID GET ERROR')
        return '路径不存在'

    try:
        file_list=os.listdir(a)
        for i in file_list:
            if str(i).isdigit():
                music_list.append(i) #筛选出符合条件的网易云JSON文件
        nice=''
        for i in music_list:
            nice=nice+i+','
        nicee=nice[0:-1]#最后一个逗号看着不舒服
        return nicee
    except Exception as o:
        print(str(o),'  ,ID.py : 2. File Operation ERROR')

def OPEN_FILE_DEEPIN(a):#所有要提取的文件，存放到表格
    music_list_really=[]
    music_list=[]
    if os.path.exists(a) is True:#检测目录是否存在
        pass
    else:
        return '路径不存在'

    
    file_list=os.listdir(a)
    for i in file_list:
        try:
            path_1=os.path.join(a,str(i))
            with open(path_1,'r',encoding='utf-8') as p:
                deepin=json.loads(p.read())
                idd=deepin['transUser']['id']
                music_list_really.append(path_1)

        except Exception as o:
            pass

    for i in music_list_really:
        with open(i,'r',encoding='utf-8') as p:
            deepin=json.loads(p.read())
            idd=deepin['transUser']['id']
            music_list.append(str(idd)) #筛选出符合条件的网易云JSON文件

    nice=''
    for i in music_list:
        nice=nice+i+','
    nicee=nice[0:-1]#最后一个逗号看着不舒服
    return nicee
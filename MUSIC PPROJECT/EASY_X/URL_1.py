import os
import requests
import json

def URL_GET(A,US):#传入单个ID ,return JSON数据
    if str(A).isdigit():
        pass
    else:
        print('"',str(A),'"','不是合法的数字！')
        return '非法数字'
    if US=='None':
        headers={"ContentType": "application/json","User-Agent":None,"Accept-Encoding":None,\
            "Accept":None,"Connection":None}
    else:
        headers={"ContentType": "application/json","User-Agent":US,"Accept-Encoding":None,\
            "Accept":None,"Connection":None}
    try:
        url="http://music.163.com/api/song/detail/?id="+str(A)+"&ids=["+str(A)+"]"
        aa=requests.get(url,headers=headers,timeout=3).text
        return aa#JSON
    except Exception as r:
        print(str(r),'    ,URL_1.py : 1. connection timeout')
        return 'timeout'#没拿到JSON

def json_wrap(a):#数据清洗 传入JSON ,RETURN歌曲基本信息 
    #jpp=js.keys()#dict_keys(['songs', 'equalizers', 'code'])
    #print(js['songs'][0].keys())
    try:
        js=json.loads(a)
        if str(js['songs']) == '[]':
            return '不存在的歌曲ID!'
        else:
            jp1=js['songs'][0]['artists'][0]['name']#艺人名
            jp2=js['songs'][0]['name']#曲名
            jp3=js['songs'][0]['album']['name']#专辑名

            if jp1 is None or len(jp1)==0 :
                jp1=' '
            if jp2 is None or len(jp2)==0 :
                jp2=' '
            if jp3 is None or len(jp3)==0 :
                jp3=' '
            jpeg=jp1+','+jp2+','+jp3
            return jpeg
    except Exception as r:
        print(str(r),'    ,URL_1.py : 3.json_wrap error')

def URL_GET_translation(S,US):#传入ID ,RETURN JSON
    print('User-Agent : ',US)
    if US=='None':
        headers={"ContentType": "application/json","User-Agent":None,"Accept-Encoding":None,\
        "Accept":None,"Connection":None}
    else:
        headers={"ContentType": "application/json","User-Agent":US,"Accept-Encoding":None,\
        "Accept":None,"Connection":None}
    try:
        url="http://music.163.com/api/song/lyric?os=pc&id="+str(S)+"&lv=-1&kv=-1&tv=-1"
        bb=requests.get(url,headers=headers,timeout=3).text
        return bb#JSON
    except Exception as r:
        print(str(r),'    ,URL_1.py : 4.connection timeout')
        return 'timeout'

def json_wrap_tras(a):#数据清洗 传入JSON ,RETURN 歌词和翻译
    try:
        js=json.loads(a)
        jp1=js['lrc']['lyric']#歌词
        if not 'lyric' in js['tlyric']:
            return [jp1,'没有翻译且大概率是无时间戳歌词']
        jp2=js['tlyric']['lyric']#翻译
        
        if jp2 is None:
            jp2='无翻译'
        jpg=[jp1,jp2]
        #print(jpg)
        return jpg
    except Exception as r:
        if 'nolyric' in js:
            if js['nolyric']== True:
                return '无歌词'
        elif 'uncollected' in js:
            if js['uncollected']== True:
                return '未收录'
        print(str(r),'    ,URL_1.py : 5.json_wrap_tras error')
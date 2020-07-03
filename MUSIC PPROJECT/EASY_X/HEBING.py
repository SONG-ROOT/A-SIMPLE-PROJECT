import re
def LIST_BULID(b,c):#传入歌词列表，return文本（有翻译）
    try:              #[T]歌词/n[T][T][T]歌词/n[T]歌词
        b[0]=b[0]+'\n'
        b[1]=b[1]+'\n'
        ENGLISH=b[0].split('\n')  #可靠的时间线加上未翻译的语言    用\n分割
        CHINESE=b[1].replace('\n','<<><><<>')#匹配不到\n

        unreliable_time_line=[]#临时不可靠的时间线
        K=1
        while K:
            if '' in ENGLISH:
                ENGLISH.remove('')
            else:
                K=0
        for i in range(len(ENGLISH)):
            a=re.compile(r'\[(.*?)\]').findall(ENGLISH[i])
            if a != []:#奇葩的翻译格式,导致我必须额外增加校验
                unreliable_time_line.append(a[0])#只选第一个时间线,后面的不要 
            elif a==[] and i==0:
                ENGLISH[i]='[00:00.88]'+ENGLISH[i]
            else:
                pass
                



        #原文列表理应和临时时间线列表 项数 一致，我根据临时时间线拿取中文翻译
        REAL_CHINESE=[]#提取出的翻译
        for i in range(len(unreliable_time_line)):
            i_get=re.compile(r'\['+unreliable_time_line[i]+r'\](.*?)\<\<\>\<\>\<\<\>').findall(CHINESE)
            REAL_CHINESE.append(i_get)
        
        for GG in range(len(REAL_CHINESE)):
            if REAL_CHINESE[GG] !=[]:#不为[]证明这句话翻译了
                ENGLISH[GG]=ENGLISH[GG]+c+REAL_CHINESE[GG][0]
        
        STRR=''
        for kj in ENGLISH:
            STRR=STRR+kj+'\n'
        return STRR

    except Exception as d:
        print(str(d),'    ,HEBING.py : 1.LIST_BULID Error')

def SIMPLE_NO_TRA(b):#传入歌词列表，return文本（无翻译）
    try:             
        b[0]=b[0]+'\n'
        ENGLISH=b[0].split('\n')
        STRR=''
        for kj in ENGLISH:
            STRR=STRR+kj+'\n'
        return STRR
    except Exception as d:
        print(str(d),'    ,HEBING.py : 2.SIMPLE_NO_TRA Error')

# coding: utf-8
# Writer: Mike_Shine
# Date: 2018-7-11
# 请尊重原创，谢谢。

# 这段代码是输入B站UP主的编号（User_Mid------进入up主的主页 https://space.bilibili.com/91236407/#/video。 其中91236407即为 User_Mid），然后爬取主页内的视频
# 有一点没有做的就是说这段代码只爬100个。如果想要爬所有的视频，你可以加一点点代码做翻页的动作，获取新的包

import json
import re
import os
import requests
import time
import datetime


start_time = datetime.datetime.now()


# 为了替换掉命名时的非法字符，不然下载创建路径时会报错
def sub(s):
    patn_1 = re.compile(r'\?')  
    patn_2 = re.compile(r'\/')
    patn_3 = re.compile(r'\\')
    patn_4 = re.compile(r'\|')
    patn_5 = re.compile(r'\:')
    patn_6 = re.compile(r'\<')
    patn_7 = re.compile(r'\>')
    patn_8 = re.compile(r'\*')
    patn_9 = re.compile(r'\:')

    s = re.sub(patn_1,"",s)
    s = re.sub(patn_2,"",s)
    s = re.sub(patn_3,"",s)
    s = re.sub(patn_4,"",s)
    s = re.sub(patn_5,"",s)
    s = re.sub(patn_6,"",s)
    s = re.sub(patn_7,"",s)
    s = re.sub(patn_8,"",s)
    s = re.sub(patn_9,"",s)
    return s 





# 下载的函数
# 这里拿到URL就下载，因为URL是动态更新的，要注意这个点。
def download(i,Video_List,path):
    pass

# 主函数
def main():
    host = 'upos-hz-mirrorks3u.acgvideo.com'

    # 下面是下载内容
    headers = {
        'Host': host,
        'Connection': 'keep-alive',
        'Origin': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.bilibili.com/video/ava923312/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    if not os.path.exists('tmp.mp4'):
        with open('tmp.mp4', 'wb') as f:
            print("-------------------------STart LINE-------------------------")
            localtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(localtime + "开始下载")
            f.write(requests.get('http://upos-hz-mirrorks3u.acgvideo.com/upgcxcode/15/90/13009015/13009015-1-64.flv?e=ig8euxZM2rNcNbhHhbUVhoMznWNBhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNo8g2ENvNo8i8o859r1qXg8xNEVE5XREto8GuFGv2U7SuxI72X6fTr859r1qXg8gNEVE5XREto8z5JZC2X2gkX5L5F1eTX1jkXlsTXHeux_f2o859IB_&uipk=5&nbs=1&deadline=1575214605&gen=playurl&os=ks3u&oi=1001173206&trid=179082e356714617a4b6aa701d8c0fbcu&platform=pc&upsig=5e4af3118431ea54e90de5a9582cdca5&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=95451953', headers=headers, verify=False).content)

            localtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(localtime + "下载完成")
            print("-------------------------STop LINE-------------------------")
    else:
        print("视频  存在于本地，跳过下载")


if __name__=='__main__':
    main()

end_time = datetime.datetime.now() 
minus = end_time - start_time
consume = minus.total_seconds()
print( "总共用时:"+str(round(consume,1))+"s")


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

def getBaseUrl():
    url = input('请输入视频网址，形如："https://www.bilibili.com/video/av7923312/"\n')
    url = url.strip(' ')
    # url = 'https://www.bilibili.com/video/av7923312/'
    # url = 'https://www.bilibili.com/video/av6477644'

    # url = 'https://www.bilibili.com/video/av75993929'

    # url = 'https://www.bilibili.com/video/av50267413'

    # url = 'https://www.bilibili.com/video/av71422418'

    # url_host = url.match(r'(?<=https://)(.*?)(?=/video)')
    url_host = re.search(r'https://(.*?)/video', url).group(1)
    print('url_host', url_host)
    return url_host, url


def getBaseHtml(base_url_host, base_url):
    # GET /video/av7923312 HTTP/1.1
    # Host: www.bilibili.com
    # Connection: keep-alive
    # Cache-Control: max-age=0
    # Upgrade-Insecure-Requests: 1
    # User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400
    # DNT: 1
    # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
    # Referer: https://www.bilibili.com/
    # Accept-Encoding: gzip, deflate, br
    # Accept-Language: zh-CN,zh;q=0.9
    # Cookie: _uuid=196F43D9-3E0E-956B-1A4B-5F27D11452B390921infoc; buvid3=93A48880-B326-4F26-BF1E-CCE18770B4FF155841infoc; LIVE_BUVID=AUTO7715739825912970; CURRENT_FNVAL=16; laboratory=1-1; hasstrong=1; rpdid=|(u)mml)uYY)0J'ul~Jm)kYu); DedeUserID=95451953; DedeUserID__ckMd5=a23508be4333313f; SESSDATA=95e210d8%2C1576574645%2C69d0abb1; bili_jct=4e26561411ba9527d522880c69f2bd23; CURRENT_QUALITY=64; UM_distinctid=16e7979d6a72a9-03f033b5830b67-34564978-144000-16e7979d6ad18e; stardustvideo=1; bp_t_offset_95451953=327633273712012521; INTVER=1; sid=74shxc33

    url_header = {
        'Host': base_url_host,
        'Connection': 'keep-alive',
        # 'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        # 'Origin': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
        'DNT': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.bilibili.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    html = requests.get(base_url, headers=url_header, verify=False).content.decode('utf-8')

    print('\n\n')
    print(html)
    print('\n\n')

    return html


def checkM4S(base_html):
    result = re.findall(r'\.m4s\?', base_html)
    print(result)
    return result != []
        # (r'\.(.+?)\?', base_html).group(1)


def getInfo(html):
    video_url = re.search(r'"url":"(.*?)","backup_url"', html).group(1)  # 这个是URL
    print('video_url')
    print(video_url)

    host = re.search(r'http://(.*?)/upgcxcode', video_url).group(1)
    print('host')
    print(host)

    title = re.search(r'<title data-vue-meta="true">(.*?)_哔哩哔哩', html).group(1)
    for ch in r'/\:*"<>|?':
        title = title.replace(ch,'_')
    print('title')
    print(title)

    format = re.search(r'\.(.+?)\?', video_url).group(1).split('.')[-1]
    print('format')
    print(format)

    return host, video_url, title, format


def getM4SInfo(html):
    video_url = re.search(r'"video":\[\{"id":\d*,"baseUrl":"(.*?)","base_url"', html).group(1)  # 这个是URL
    print('video_url')
    print(video_url)

    audio_url = re.search(r'"audio":\[\{"id":\d*,"baseUrl":"(.*?)","base_url"', html).group(1)  # 这个是URL
    print('audio_url')
    print(audio_url)

    video_host = re.search(r'http://(.*?)/upgcxcode', video_url).group(1)
    print('video_host')
    print(video_host)

    audio_host = re.search(r'http://(.*?)/upgcxcode', audio_url).group(1)
    print('audio_host')
    print(audio_host)

    title = re.search(r'<title data-vue-meta="true">(.*?)_哔哩哔哩', html).group(1)
    for ch in r'/\:*"<>|?':
        title = title.replace(ch,'_')
    print('title')
    print(title)

    format = re.search(r'\.(.+?)\?', video_url).group(1).split('.')[-1]
    print('format')
    print(format)

    return video_host, video_url, audio_host, audio_url, title, format


def download(base_url, host, video_url, save_path):
    # GET /upgcxcode/15/90/13009015/13009015-1-64.flv?e=ig8euxZM2rNcNbhHhbUVhoMznWNBhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNo8g2ENvNo8i8o859r1qXg8xNEVE5XREto8GuFGv2U7SuxI72X6fTr859r1qXg8gNEVE5XREto8z5JZC2X2gkX5L5F1eTX1jkXlsTXHeux_f2o859IB_&uipk=5&nbs=1&deadline=1575298307&gen=playurl&os=ks3u&oi=3670383011&trid=1e68e83c0d404e039b754dfa1d872c94u&platform=pc&upsig=a2b51986300359e9463f567a03c920c3&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=95451953 HTTP/1.1
    # Host: upos-hz-mirrorks3u.acgvideo.com
    # Connection: keep-alive
    # Origin: https://www.bilibili.com
    # User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400
    # DNT: 1
    # Accept: */*
    # Referer: https://www.bilibili.com/video/av7923312
    # Accept-Encoding: gzip, deflate, br
    # Accept-Language: zh-CN,zh;q=0.9

    # 下面是下载内容
    headers = {
        'Host': host,
        'Connection': 'keep-alive',
        'Origin': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400',
        'DNT': '1',
        'Accept': '*/*',
        'Referer': base_url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    if not os.path.exists(save_path):
        with open(save_path, 'wb') as f:
            print("-------------------------STart LINE-------------------------")
            localtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(localtime + "开始下载")
            f.write(requests.get(video_url, headers=headers, verify=False).content)

            localtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(localtime + "下载完成")
            print("-------------------------STop LINE-------------------------")
    else:
        print("视频  存在于本地，跳过下载")


# 主函数
def main():
    base_url_host, base_url = getBaseUrl()
    base_html = getBaseHtml(base_url_host, base_url)
    if checkM4S(base_html):
        video_host, video_url, audio_host, audio_url, title, format = getM4SInfo(base_html)
        abspath = '\\'.join(os.path.abspath(__file__).split('\\')[0:-1]) + '\\'
        # title = '2019'
        video_path = abspath + title + 'video.' + format
        audio_path = abspath + title + 'audio.' + format
        merge_path = abspath + title + '.mp4'
        print(os.path.abspath(__file__))
        download(base_url, video_host, video_url, video_path)
        download(base_url, audio_host, audio_url, audio_path)
        command = r'FFmpeg -i "' + video_path + r'" -i "' + audio_path + r'" -codec copy "' + merge_path + r'"'
        print(command)
        if os.system(command)==0:
            os.system('del "' + video_path + '"')
            os.system('del "' + audio_path + '"')
            print('合并成功')
        else:
            print('合并失败')
    else:
        host, video_url, title, format = getInfo(base_html)
        download(base_url, host, video_url, title + '.' + format)



    return



if __name__=='__main__':
    main()

end_time = datetime.datetime.now() 
minus = end_time - start_time
consume = minus.total_seconds()
print( "总共用时:"+str(round(consume,1))+"s")


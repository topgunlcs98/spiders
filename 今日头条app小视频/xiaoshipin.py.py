import urllib
import requests
import json
import os
import re
import random

header = {
    'Host': 'is-hl.snssdk.com',
    'Connection': 'keep-alive',
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; VIE-AL10 Build/HUAWEIVIE-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.91 Mobile Safari/537.36 JsSdk/2 NewsArticle/6.8.7 NetType/wifi (NewsLite 6.8.7)',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://is-hl.snssdk.com/feoffline/search/template/tt_search/search/search.html?from=search_tab&keyword=&search_position=search_bar&action_type=input_keyword_search&iid=68391280727&device_id=38812718349&ac=wifi&channel=lite_huawei&aid=35&app_name=news_article_lite&version_code=687&version_name=6.8.7&device_platform=android&ab_version=770575%2C668905%2C567188%2C374097%2C758003%2C794260%2C770502%2C724569%2C644001%2C736978%2C768227%2C661929%2C785656%2C800193%2C668907%2C808414%2C799768%2C821460%2C709445%2C794704%2C766815%2C788039%2C793955%2C819036%2C731484%2C668904%2C668906%2C811292%2C812272%2C824262%2C817851%2C823382%2C783635%2C652981%2C731483%2C770317%2C668903%2C679107%2C775316%2C789001&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_group=z1&ab_feature=z1&abflag=3&device_type=VIE-AL10&device_brand=HUAWEI&language=zh&os_api=24&os_version=7.0&uuid=861962034707256&openudid=6c38d6b3fa6a31ed&manifest_version_code=687&resolution=1080*1794&dpi=480&update_version_code=6873&_rticket=1554691554826&sa_enable=0&fp=crTrc2GWFrXqFlHbLrU1FzmSLl4r&rom_version=emotionui_5.0.3_vie-al10c00b399sp20&plugin=0',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.9',
    'Cookie': 'odin_tt=30456c3835776458354f59493373375a81e15d3c6e6aa2c1ca279f32b270030461739d73fbf464d537e76f0c0d232e08; install_id=68391280727; ttreq=1$7268ff1aba2dc27d7e7dc2a750c82640d2169e6a; qh[360]=1'
}

url_list=[]
dy_list=[]
else_list=[]

def getVideosFromPages(url_set,offset,headers):
    url = 'https://is-hl.snssdk.com/api/search/content/?from=xiaoshipin&keyword=%E9%BB%91%E5%AF%BC%E6%B8%B8&search_position=aladdin_xiaoshipin&action_type=input_keyword_search&iid=68391280727&device_id=38812718349&ac=wifi&channel=lite_huawei&aid=35&app_name=news_article_lite&version_code=687&version_name=6.8.7&device_platform=android&ab_group=z1&abflag=3&device_type=VIE-AL10&device_brand=HUAWEI&language=zh&os_api=24&os_version=7.0&uuid=861962034707256&openudid=6c38d6b3fa6a31ed&manifest_version_code=687&resolution=1080*1794&dpi=480&update_version_code=6873&_rticket=1554691554826&sa_enable=0&fp=crTrc2GWFrXqFlHbLrU1FzmSLl4r&rom_version=emotionui_5.0.3_vie-al10c00b399sp20&plugin=0&count=10&format=json&source=input&pd=xiaoshipin&keyword_type=&from_search_subtab=&offset='+str(offset)+'&search_id=&has_count='+str(offset)+'&qc_query='
    rsp = requests.get(url,headers = header, verify = False)
    data = rsp.json()
    videos = data['data']
    for video in videos:
        addr = video['raw_data']['video']['download_addr']['url_list'][0]
        url_set.append(addr)

def sortLinks(url_list,dy_list,else_list):
    for url in url_list:
        pattern = 'https://aweme.snssdk.com/aweme'
        if re.match(pattern,url):
            dy_list.append(url)
        else: else_list.append(url)

def download_else(urls,header):
    path='F:/小视频/'
    num=0
    for url in urls:
        try:
            fname = '其他平台'+str(num)+'.mp4'
            print(fname)
            dest_dir = os.path.join(path,fname)
            r = requests.get(url,stream = True,headers=header,verify=False)
            f = open(dest_dir,'wb')
            f.write(r.content)
            f.flush()
            num+=1
            print("下载完成")
        except:
            print('erro')

def download_dy(links):
    path="XXXXX"
    headers={
        "User-Agent": "com.ss.android.ugc.aweme/570 (Linux; U; Android 7.0; zh_CN; VIE-AL10; Build/HUAWEIVIE-AL10; Cronet/58.0.2991.0)"
    }
    num=0
    for link in links:
        try:
            fname='抖音'+str(num)+'.mp4'
            dest_dir = os.path.join(path,fname)
            response = requests.get(link,headers=headers)
            content_size=int(response.headers['content-length'])
            f = open(dest_dir,'wb')
            f.write(response.content)
            f.flush()
            print("下载完成！"+"大小："+str(content_size))
            f.close()
            num+=1
        except:
            print('erro')

if __name__ == '__main__':
    for i in range(0,80,10):
        getVideosFromPages(url_list,i,header)
    
    sortLinks(url_list,dy_list,else_list)
    download_dy(dy_list)
    download_else(else_list,header)

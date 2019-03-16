import requests
from urllib.parse import urlencode
import time
import toutiao_save
from bson import ObjectId
#max_behot_time用于模拟分页，初值为0
max_behot_time=['0']

user={}

def get_page(j):
    params = {
        'category':'组图',
        'utm_source':'toutiao',
        'max_behot_time':j,
    }
    headers={
        'cookie':'csrftoken=9bac7d486ba3b65281cfd5122efddc4b; tt_webid=6667417260644681224; UM_distinctid=16971009c9125b-0f1082a5515cb5-b781636-144000-16971009ca73d0; tt_webid=6667417260644681224; WEATHER_CITY=%E5%8C%97%E4%BA%AC; s_v_web_id=781fb7db1a992686eab2ec15f487fd3c; login_flag=5163ce0786b07db2eabb5fefae066fd5; sessionid=01cb325d486a7fb9b2e8d1b28de78c7c; uid_tt=3f07060dc210570593a35c2d688b82d9; sid_tt=01cb325d486a7fb9b2e8d1b28de78c7c; sid_guard="01cb325d486a7fb9b2e8d1b28de78c7c|1552653698|15552000|Wed\054 11-Sep-2019 12:41:38 GMT"; __tasessionId=xry6oxv701552662761868; CNZZDATA1259612802=882188190-1552375846-%7C1552662342',
        'referer':'https://www.toutiao.com/ch/gallery_photograthy/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    base_url = 'https://www.toutiao.com/api/pc/feed/?'
    url = base_url + urlencode(params)
    try:
        resp = requests.get(url,headers=headers)
        if 200 == resp.status_code:
            response=resp.json()
        return response
    except requests.ConnectionError:
        return None

def get_max_behot_time(response):
    try:
        max_behot_time1 = response.get('next')
        max_behot_time2 = max_behot_time1.get('max_behot_time')
        #获取到下一个页面的max_behot_time2，将其加入列表max_behot_time,方便请求下一个页
        max_behot_time.append(max_behot_time2)
    except:
        pass

def to_save(response):
    if response.get('data'):
        data = response.get('data')
        for item in data:
            image_list = []
            title = item.get('title')
            user_url='https://www.toutiao.com'+item.get('media_url')
            user_name=item.get('source')
            source_url='https://www.toutiao.com'+item.get('source_url')
            user['user_name']=user_name
            user['user_url']=user_url
            user['source_url']=source_url
            user['title']=title
            #'_id'是用来处理，存入mongodb报错的情况
            user['_id']=ObjectId()
            images = item.get('image_list')

            if images:
                for image in images:
                    image1=image.get('url_list')
                    if image1:
                        image_list.append(image1[0].get('url'))
                    else:
                        image2 = 'http:'+image.get('url')
                        image_list.append(image2)


            image1_sum=len(image_list)
            for i in range(image1_sum):
                image_name='image'+str(i)
                user[image_name]=image_list[i]
            #print(user)
            time.sleep(1.5)
            #toutiao_save.to_mysql(user)
            #toutiao_save.to_mongodb(user)
            toutiao_save.to_local(user)

if __name__ == '__main__':
    while True:
        i=len(max_behot_time)
        j=max_behot_time[i-1]
        #通过提取max_behot_time列表中的值，逐页发送请求
        response=get_page(j)
        time.sleep(1)
        to_save(response)
        get_max_behot_time(response)



import pymysql
from pymongo import MongoClient
import os
from hashlib import md5
import requests
from requests import codes
import urllib

def to_mysql(user):
    """
    信息写入mysql
    """
    table='toutiao_content'
    keys =', '.join(user.keys())
    values = ', '.join(['%s'] * len(user))

    db = pymysql.connect(host='localhost', user='root', password='自己的数据库密码', port=3306, db='toutiao')
    cursor = db.cursor()
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(user.values())):
            print("Successful")
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()


def to_mongodb(user):
    '''
    写入mongodb
    :param user: 今日头条信息字典
    '''
    client = MongoClient()
    db = client['toutiao']
    collection = db['toutiao_content']
    if collection.insert(user):
        print('Saved to Mongo!')


def to_local(user):
    '''
    写入本地目录
    '''
    #创建名为toutiao_img的主目录、和title内容为目录名的子目录
    table=str.maketrans('.:|','111')
    img_path = 'toutiao_img' + os.path.sep + user['title'].translate(table)
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        #请求图片链接
        #遍历请求image0-image2的链接
        for i in range(0,3):
            image='image'+str(i)
            resp = requests.get(user[image])
            if codes.ok == resp.status_code:
                #图片内容使用其内容的MD5值，避免重复
                file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                    file_name=md5(resp.content).hexdigest(),
                    file_suffix='jpg')
                if not os.path.exists(file_path):
                    '''
                    #也可以用urllib的urlretrieve()方法下载图片
                    for i in range(0,3):
                        image='image'+str(i)
                        urllib.request.urlretrieve(user[image], file_path)
                    '''
                    with open(file_path, 'wb') as f:
                        f.write(resp.content)
                    print('Downloaded image path is %s' % file_path)
                else:
                    print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image，item')

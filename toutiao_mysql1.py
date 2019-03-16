import pymysql

db = pymysql.connect(host='127.0.0.1', user='root', password='自己的数据库密码', port=3306)
cursor = db.cursor()
cursor.execute("CREATE DATABASE toutiao DEFAULT CHARACTER SET utf8mb4")
db.close()
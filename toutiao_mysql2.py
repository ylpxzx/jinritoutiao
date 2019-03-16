import pymysql

db = pymysql.connect(host='127.0.0.1', user='root', password='自己的数据库密码', port=3306, db='toutiao')
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS toutiao_content(title VARCHAR(255) NOT NULL,user_name VARCHAR(255) NOT NULL, user_url VARCHAR(255) NOT NULL, source_url VARCHAR(255) NOT NULL, image0 VARCHAR(255) NOT NULL,image1 VARCHAR(255) NOT NULL,image2 VARCHAR(255) NOT NULL,PRIMARY KEY (title))'
cursor.execute(sql)
db.close()
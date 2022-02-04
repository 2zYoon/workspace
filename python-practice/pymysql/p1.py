import pymysql

db = pymysql.connect(
    host='ec2-3-38-108-28.ap-northeast-2.compute.amazonaws.com',
    port=3306,
    user='root',
    passwd='root',
    db='bbgg',
    charset='utf8'
)

cursor = db.cursor()

sql_to_helloworld = 'select * from Product'
cursor.execute(sql_to_helloworld)
for i in cursor.fetchall():
    print(i)

cursor.close()
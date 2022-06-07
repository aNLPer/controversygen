# coding:utf-8
# 过滤数据库数据

import mysql.connector as conn

# 获取数据库连接
mydb = conn.connect(
    host="localhost",
    user="root",
    password="123456",
    database = "controversyfocus"
)
cursor = mydb.cursor()

insert_sql = "insert into resources_of_first_instance (id, appeal,plea, courtview) values (%s,%s,%s,%s)"
val = []
base = 0
step = 500
max_length = 200
print("开始遍历数据库...")
while 1:
    cursor.execute(f"select * from resources limit {base},{step}")
    results = cursor.fetchall()
    for record in results:
        if "一审" in record[1] or "一审" in record[2]:
            continue
        if record[1] == None or record[1].strip() == "":
            continue
        if record[2] == None or record[2].strip() == "":
            continue
        item = []
        item.append(record[0])
        item.append(record[1])
        item.append(record[2])
        item.append(record[4])
        val.append(item)
        if len(val) == max_length:
            cursor.executemany(insert_sql, val)
            mydb.commit()
            val.clear()
    if len(results) < step:
        break
    base = base+step
cursor.executemany(insert_sql, val)
mydb.commit()
print("处理完成...")
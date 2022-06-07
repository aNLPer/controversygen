# coding=utf-8

import mysql.connector as conn
import configparser
import time

mydb = conn.connect(
    host="localhost",
    user="root",
    password="123456",
    database="controversyfocus"
)

if mydb is not None:
    print("连接数据库成功")

# 读取配置文件
config = configparser.ConfigParser()
config.read("dataAnno.cfg", encoding="utf-8")
currentAnnoIndex = config.getint("dataanno", "currentAnnoIndex")
tableName = config.get("dataanno", "tableName")


update_sql = f"update {tableName} set appeal= %s, plea=%s, focus=%s where id=%s"
cursor = mydb.cursor()
while 1:
    # 选择数据
    select_sql = f'select * from {tableName} limit {currentAnnoIndex}, 1'
    # 获取数据
    cursor.execute(select_sql)
    res = cursor.fetchall()
    item = res[0]
    print("----------------------------------------------------------------诉称-----------------------------------------------------------------\n\n")
    print(item[1])
    print("\n\n")
    print("----------------------------------------------------------------辩称------------------------------------------------------------------\n\n")
    print(item[2])
    print("\n\n")
    print("---------------------------------------------------------------法院观点----------------------------------------------------------------\n\n")
    print(item[4])
    print("\n\n")
    while 1:
        focus = input("请输入争议焦点\n")
        sure = input("请您确认:y or n\n")
        if sure == "y":
            break
        else:
           continue
    while 1:
        appeal = input("请输入诉称\n")
        if appeal == "s":
            appeal = item[1]
        sure = input("请您确认:y or n\n")
        if sure == "y":
            break
        else:
            continue
    while 1:
        plea = input("请输入辩称\n")
        if plea == "s":
            plea = item[2]
        sure = input("请您确认:y or n\n")
        if sure == "y":
            break
        else:
            continue

    sure = input("是否提交标注结果？y or n\n")
    if sure == "y":
        print("插入数据库\n")
        cursor.execute(update_sql, [appeal, plea, focus, item[0]])
        mydb.commit()
        print("标注索引+1\n")
        currentAnnoIndex += 1
        print("修改当前标注索引\n")
        config.set("dataanno", "currentAnnoIndex",str(currentAnnoIndex))
        config.write(open("dataAnno.cfg","w", encoding="utf-8"))
    else:
        print("将重新标注....")
        time.sleep(1.5)
        print()



# read database

import sqlite3
import csv

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

with conn:
    c.execute("""SELECT * FROM myapp_orderpending WHERE user_id=3""")
    data = c.fetchall()
    # data = c.fetchone()
    # data = c.fetchmany(3)
    for d in data:
        print(data)
        print('-------')

    ######## EXPORT TO CSV ########
    with open('allorder_user3.csv','w',newline='',encoding='utf-8') as f:
        #File Writer
        fw = csv.writer(f)
        fw.writerows(data)



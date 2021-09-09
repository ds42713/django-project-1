####### เขียนลงข้อมูล myapp_verifyemail

import sqlite3
import csv
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

def writetodb(token,approved,user_id):
    #write data to verifyemail table
    with conn:
        c.execute("""INSERT INTO myapp_verifyemail (id,token,approved,user_id) VALUES (?,?,?,?)""",
            (None,token,approved,user_id))
        conn.commit() #save to database

# writetodb('asdandlsfkn3',1,11)

########## read csv #####
with open('newtoken.csv',newline='',encoding='utf-8') as f:
    # fr = file reader
    fr = csv.reader(f)
    data = list(fr)

    #print(list(fr))
for t,a,u in data:
    print(t,a,u)
    writetodb(t,int(a),int(u))

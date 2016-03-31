from common import Common
import pymysql.cursors
import pymysql
import pandas as pd

class Insert_db:

    def __init__(self):
        self.com = Common()

    def loadData(self):
        '''
        #usage: Load data form /home/boyang/Documents/furnitures
        #arg: None
        #return: Data stored at path above in json structure
        '''
        src = '/home/boyang/Documents/json'
        datas = []
        furniture_list = self.com.GetFileList(src)
        for furniture in furniture_list:
            data = self.com.readJSON(furniture)
            datas.append(data)
        return datas

    def insertData(self, datas):
        '''
        #usage: Insert data into data base
        #arg: Data you want to insert
        #rerutn: None
        '''
        db = pymysql.connect(host = '127.0.0.1',
                             user = 'root',
                             password = 'Devil123',
                             db = 'FurnitoData',
                             charset = 'utf8',
                             cursorclass = pymysql.cursors.DictCursor)
        cursor = db.cursor()
        for data in datas:
            comments = data['reviews']
            
            for comment in comments:
                sql = 'INSERT INTO comments (furniture_name, comment, vote_up, vote_down) VALUES (%s, %s, %s, %s)'
                cursor.execute(sql, (data['name'].encode('utf-8'),comment.encode('utf-8'),'0','0'))
                db.commit()
        db.close()

    def csvtoDatebase(self):
        db = pymysql.connect(host = '127.0.0.1',
                             user = 'root',
                             password = 'Devil123',
                             db = 'FurnitoData',
                             charset = 'utf8',
                             cursorclass = pymysql.cursors.DictCursor)
        cursor = db.cursor()
        csv_url = '/home/boyang/Documents/data.csv'
        df = pd.read_csv(csv_url, encoding = "utf-8")
        for index, row in df.iterrows():
            gender = row[1]
            age = row[2]
            favoritestyle = row[3]
            for i in range(4,len(row)-3):
                if row.index[i].encode('utf-8').startswith('Please choose and take a good look at the'):
                    furniture_one = row[i]
                else:
                    if not str(row[i]) == 'nan':
                        furniture_two = row[i]
                        sql = 'INSERT INTO clicks (furniture_one, furniture_two, age, favoritestyle, gender) VALUES (%s, %s, %s, %s, %s)'
                        print sql
                        cursor.execute(sql,(furniture_one.encode('utf-8'), furniture_two.encode('utf-8'), age.encode('utf-8'), favoritestyle.encode('utf-8'), gender.encode('utf-8')))
                        db.commit()
                    else:
                        pass
        db.close()

i = Insert_db()
i.csvtoDatebase()

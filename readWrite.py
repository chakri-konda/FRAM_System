import os
import csv
from datetime import datetime, date

def id_check(sid):
    with open('data/student_data.csv') as file:
        data = {}
        rawData = csv.DictReader(file)
        for row in rawData:
            if row['uid'] == sid:
                data['uid'] = row['uid']
                data['name'] = row['name']
                return True
        else:
            return False

def mark_attendence(sid):
    file_name = 'data/Attendence/'+date.today().strftime("%d-%m-%Y")+'.csv'
    if not os.path.isfile(file_name):
        with open(file_name, 'w') as file:
            file.write('uid,time')
    with open(file_name, 'r+') as file:
        rawData = csv.DictReader(file)
        idList = []
        for row in rawData:
            idList.append(row['uid'])
        if sid not in idList:
            now = datetime.now()
            time = now.strftime('%H:%M:%S')
            file.writelines('\n{},{}'.format(sid, time))
            return True
    return False
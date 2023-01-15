import sqlite3
from datetime import datetime

import pandas as pd
from patient import Patient



# "DB data processing" testing
def convert_timestamp(timestamp):
    # Convert the timestamp to a readable format
    if not timestamp:
        return None
    dt_object = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
    return dt_object.date().strftime("%d/%m/%Y")


conn = sqlite3.connect('instance/database.db')
data = pd.read_sql_query("SELECT * from Patient", conn)
conn.close()
data['timestamp'] = data['timestamp'].apply(convert_timestamp)
counters = data['people_counter'].groupby(data['timestamp']).count().tolist()
dates = data['timestamp'].unique()
dates = pd.Series(dates).dropna().tolist()

# "fetching user data from db" testing

conn = sqlite3.connect('testing_database.db', timeout=15)
cur = conn.cursor()
cur.execute("SELECT * FROM user WHERE role = 'User' ORDER BY id DESC")
last_user = cur.fetchone()
conn.close()
pat = Patient(patient_id=last_user[0], name=last_user[3])
pat.load()
# print all the attributes of the patient
print(pat.__dict__)

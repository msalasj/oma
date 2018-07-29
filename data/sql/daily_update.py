from datetime import datetime, date, timedelta

import cx_Oracle
import pandas as pd
import sqlite3


# dbConnection
ip = '10.240.142.101'
port = '2050'
SID = 'PRODVG'
dsnStr = cx_Oracle.makedsn(ip, port, SID)
user = 'pase01'  # 'modf_abar'
password = 'pase02'  # 'm201712a'
conn = cx_Oracle.connect(user=user, password=password, dsn=dsnStr, 
	                     encoding='iso-8859-1')
# get data from open
sql_fname = 'ciclos_itin'
query = open(sql_fname + '.sql').read()
now = datetime.now()
start_date = date.today() - timedelta(1)
sql = query.format(start_date.strftime('%d/%m/%Y'))
data = pd.read_sql(sql, conn)
conn.close()
# put data on oma
conn = sqlite3.connect('../oma.db')
# process data
query = """
    update fechas_itin set
    f_plan = {}, f_real = {}, f_fact = {}
    where cod_unicom = {} 
    and ruta = {} 
    and num_itin = {}
    and periodo = {}
"""
periodo = [int(datetime.strptime(str(x)[:10], "%Y-%m-%d").strftime('%Y%m')) for x in data.F_LTEOR.values]
fplan = [int(datetime.strptime(str(x)[:10], "%Y-%m-%d").timestamp()) for x in data.F_LTEOR.values]
freal = [int(datetime.strptime(str(x)[:10], "%Y-%m-%d").timestamp()) for x in data.F_LREAL.values]
ffact = [int(datetime.strptime(str(x)[:10], "%Y-%m-%d").timestamp()) for x in data.F_FACT.values]
for i in range(data.shape[0]):
    row = data.iloc[i]
    sql = query.format(fplan[i], freal[i], ffact[i], row.COD_UNICOM, 
     				   row.RUTA, row.NUM_ITIN, periodo[i])
    conn.execute(sql)
    conn.commit()
conn.close()
print('Process Finished')

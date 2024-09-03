import json
import sqlite3
import datetime

# import numpy as np
# import math
# # from datetime import timedelta, date
# import MetaTrader5 as mt5
# import pandas as pd

# # date_from = date.today() - timedelta(days=52)

# # print(date_from)

# if not mt5.initialize():
#     print("initialize() failed, error code =",mt5.last_error())
#     quit()
# # shut down connection to the MetaTrader 5 terminal

# rates = mt5.copy_rates_from_pos("ABEV3", mt5.TIMEFRAME_D1, 0, 40)
# rates_frame = pd.DataFrame(rates)

# with open('./json/ativos.json') as f:
#     ativos = json.load(f)

# def SaveVol(codigo,vol):
#     for item in ativos:
#         if (item['ticker'] == codigo):
#           item['sigma'] = vol
#     return

# # for item in ativos:
# # #   data = yf.download(item['ticker'], start=date_from)
# #   # rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_D1, utc_from, 10)
# rates_frame['log_retorno'] = np.log(rates_frame['close'] / rates_frame['close'].shift(1))
# sigma = rates_frame['log_retorno'].std()*math.sqrt(252)
# SaveVol('PETR4',sigma)

# print(rates_frame)
# print(round(sigma,4))
# # mt5.shutdown()
# ik = {'ticker': 'AAPL', 'social': 'Vale do Rio Doce S.A.', 'sigma': 0.2209}
# nome = 'XXX'
# ik = {'ticker': nome, 'social': 'Vale do Rio Doce S.A.', 'sigma': 0.2209}
# print(ativos)
# ativos.append(ik)

# for item in ativos:
#     print(item)
#     if (item['ticker'] == 'AAPL'):
#         item['social'] = 'blablabla'

# print(ativos)

# with open('./json/series.json') as f:
#     series = json.load(f)

# import datetime
# from workadays import workdays

# d1 = datetime.date.today()

# print(d1.strftime("%Y,%m,%d"))

# for item in series:
#     dv = item['data']
#     d = int(dv[:2])
#     m = int(dv[3:5])
#     y = int(dv[6:10])
#     d2 = datetime.date(y,m,d)
#     duteis = workdays.networkdays(d1, d2)
#     item['du'] = duteis

# with open('./json/series.json', "w") as outfile:
#     json.dump(series, outfile)

# with open('./json/parametros.json') as h:
#     parameters = json.load(h)

# print(parameters)

# parameters[0] = ['dsds','qadsad']

# print(parameters)

with open('./json/ativos.json') as f:
    ativos = json.load(f)

try:
    sqliteConnection = sqlite3.connect('C:/Users/procs/OneDrive/DATABASES/BRLMarket.db')
    cursor = sqliteConnection.cursor()
    print("Database successfully Connected to SQLite")
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

for item in ativos:
    data = datetime.date.today().strftime("%Y-%m-%d")
    i_vol = 34.5656
    query  = "INSERT INTO ativos_iv (ticker,data,iv) VALUES ('" + item['ticker'] + "','" + data + "'," + str(round(i_vol,2)) + ");"
    print(query)
    query_run = cursor.execute(query)

sqliteConnection.commit()
sqliteConnection.close()
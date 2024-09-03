import MetaTrader5 as mt5
import numpy as np
import math
import pandas as pd
import json
import datetime
from workadays import workdays

if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()

with open('./json/ativos.json') as f:
    ativos = json.load(f)

def SAVESIGMA(codigo,vol):
    for item in ativos:
        if (item['ticker'] == codigo):
          item['sigma'] = vol
    return

for item in ativos:
  rates = mt5.copy_rates_from_pos(item['ticker'], mt5.TIMEFRAME_D1, 0, 90)
  rates_frame = pd.DataFrame(rates)
  rates_frame['log_retorno'] = np.log(rates_frame['close'] / rates_frame['close'].shift(1))
  sigma = rates_frame['log_retorno'].std()*math.sqrt(252)
  print(item['ticker']," - ",round(sigma,4))
  SAVESIGMA(item['ticker'],round(sigma,4))

with open('./json/ativos.json', "w") as outfile:
    json.dump(ativos, outfile)

mt5.shutdown()

with open('./json/series.json') as f:
    series = json.load(f)

# Dias Uteis para os Vencimentos

d1 = datetime.date.today()

print(d1.strftime("%Y,%m,%d"))

for item in series:
    dv = item['data']
    d = int(dv[:2])
    m = int(dv[3:5])
    y = int(dv[6:10])
    d2 = datetime.date(y,m,d)
    duteis = workdays.networkdays(d1, d2)
    item['du'] = duteis

with open('./json/series.json', "w") as outfile:
    json.dump(series, outfile)
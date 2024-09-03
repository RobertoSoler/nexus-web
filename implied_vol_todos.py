import cotacoes
import sqlite3
from datetime import datetime
from datetime import date
from workadays import workdays
import implied_vol_delta as ivd

r = 0.14
serie_call = 'C'
serie_put = 'O'

#---------------------------------------
try:
    sqliteConnection = sqlite3.connect('C:/Users/procs/OneDrive/DATABASES/BRLMarket.db')
    cursor = sqliteConnection.cursor()
    print("Database successfully Connected to SQLite")
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
#---------------------------------------

def load_ativos():
    query = "SELECT * FROM ativos"
    query_run = cursor.execute(query)
    ativos = cursor.fetchall()
    return ativos

ativos = load_ativos()

def load_series(ativo,serie1,serie2):
    base = ativo[:4]
    query = "SELECT * FROM series WHERE BASE='" + base + "' AND (E_SERIE='" + serie1 + "' OR E_SERIE='" + serie2 + "') ORDER BY STRIKE"
    query_run = cursor.execute(query)
    series = cursor.fetchall()
    return series

def IMPLIED_VOL_ATIVO(ativo,lista,du,r):
    T = du / 252
    book_ativo = cotacoes.book_price(ativo,'LAST')
    valC1 = 0.0
    ivC1 = 0.0
    valC2 = 0.0
    ivC2 = 0.0
    valP1 = 0.0
    ivP1 = 0.0
    valP2 = 0.0
    ivP2 = 0.0
    strikeBase = 0
    size = len(lista)
    i = 0
    while (i < size) and (valC2 == 0.0):
        ticker1 = lista[i][1].strip()
        tip1 = lista[i][5].strip()
        strik1 = lista[i][2]
        if (tip1 == 'COMPRA'):
            if (strik1 >= book_ativo):
                if (valC1 == 0.0):
                        valC1 = cotacoes.book_price(ticker1,'LAST')
                        if (valC1 > 0.0):
                            ivC1 = ivd.I_VOL(valC1, book_ativo, strik1, T, r,type="c")
                            strikeBase = strik1
                else:
                    if (strik1 > strikeBase):
                        if (valC2 == 0.0):
                            valC2 = cotacoes.book_price(ticker1,'LAST')
                            if (valC2 > 0.0):
                                ivC2 = ivd.I_VOL(valC2, book_ativo, strik1, T, r,type="c") 
        i += 1
    strikeBase = book_ativo * 2
    j = i - 1
    while (j > 0) and (valP2 == 0.0):
        ticker2 = lista[j][1].strip()
        tip2 = lista[j][5].strip()
        strik2 = lista[j][2]
        if (tip2 == 'VENDA'):
            if (strik2 <= book_ativo):
                if (valP1 == 0.0):
                        valP1 = cotacoes.book_price(ticker2,'LAST')
                        if (valP1 > 0.0):
                            ivP1 = ivd.I_VOL(valP1, book_ativo, strik2, T, r,type="p")
                            strikeBase = strik2
                else:
                    if (strik2 < strikeBase):
                        if (valP2 == 0.0):
                            valP2 = cotacoes.book_price(ticker2,'LAST')
                            if (valP2 > 0.0):
                                ivP2 = ivd.I_VOL(valP2, book_ativo, strik2, T, r,type="p") 
        j -= 1
    retorno = (ivC1 + ivP1) * 0.25 + (ivC2 + ivP2) * 0.25
    return retorno

d1 = date.today()

for item in ativos:
    dados = load_series(item[0],serie_call,serie_put)
    d = dados[0][3]
    d2 = datetime.strptime(d,'%Y-%m-%d').date()
    du = workdays.networkdays(d1, d2)
    i_vol = IMPLIED_VOL_ATIVO(item[0],dados,du,r)
    data = d1.strftime("%Y-%m-%d")
    query  = "INSERT INTO ativos_iv (ticker,data,iv) VALUES ('" + item[0] + "','" + data + "'," + str(round(i_vol,4)) + ");"
    print(item[0],' ---- ',i_vol)
    # print(query)
    query_run = cursor.execute(query)



sqliteConnection.commit()
sqliteConnection.close()
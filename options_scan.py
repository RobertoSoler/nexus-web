import sqlite3
import setups
import cotacoes
#---------------------------------------
def last_price(ativo):
    return cotacoes.book_price(ativo,'LAST')
#---------------------------------------
def load_series(ativo,serie1,serie2):
    base = ativo[:4]
    try:
        sqliteConnection = sqlite3.connect('C:/Users/procs/OneDrive/DATABASES/BRLMarket.db')
        cursor = sqliteConnection.cursor()
        print("Database successfully Connected to SQLite")
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    query = "SELECT * FROM series WHERE BASE='" + base + "' AND (E_SERIE='" + serie1 + "' OR E_SERIE='" + serie2 + "') ORDER BY STRIKE"
    query_run = cursor.execute(query)
    series = cursor.fetchall()
    #sqliteConnection.close()
    return series
#---------------------------------------
def scan_options(ativos,parameters,px,oper):
    serie_call = parameters['vencimento']['serieCall']
    serie_put = parameters['vencimento']['seriePut']
    du = parameters['vencimento']['du']
    r = parameters['taxa_juros']
    painel = [()]
    for ativo in ativos:
        dados = load_series(ativo,serie_call,serie_put)
        if 'S Strangle' in oper:
            set = setups.S_STRANGLE(ativo,dados,px.loc[0],du,r)
            painel = painel + set
        if 'S Iron Condor' in oper:
            set = setups.S_ICONDOR(ativo,dados,px.loc[1],du,r)
            painel = painel + set
        if 'S Jade Lizard' in oper:
            set = setups.S_JLIZARD(ativo,dados,px.loc[2],du,r)
            painel = painel + set
        if 'S Straddle' in oper:
            set = setups.S_STRADDLE(ativo,dados,px.loc[3],du,r)
            painel = painel + set
        if 'S Call Spread' in oper:
            set = setups.S_CALLSPREAD(ativo,dados,px.loc[4],du,r)
            painel = painel + set
        if 'S Put Spread' in oper:
            set = setups.S_PUTSPREAD(ativo,dados,px.loc[5],du,r)
            painel = painel + set
    painel.pop(0)
    painel.sort(key = lambda x: x[3]/x[1],reverse=True)
    return(painel)

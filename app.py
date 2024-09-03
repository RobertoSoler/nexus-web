from flask import Flask, render_template, request, redirect
import sqlite3
import json
import pandas as pd
import options_scan
# -----------------------------------------------------------------------------------
try:
    sqliteConnection = sqlite3.connect('C:/Users/procs/OneDrive/DATABASES/BRLMarket.db')
    cursor = sqliteConnection.cursor()
    print("Database successfully Connected to SQLite")
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
# -----------------------------------------------------------------------------------
def load_venctos():
    query = "SELECT * FROM vencimentos ORDER BY data"
    query_run = cursor.execute(query)
    series_v = cursor.fetchall()
    return series_v
# -----------------------------------------------------------------------------------
def load_ativos():
    query = "SELECT * FROM ativos ORDER BY ticker"
    query_run = cursor.execute(query)
    ativos = cursor.fetchall()
    return ativos
# -----------------------------------------------------------------------------------
ativos = load_ativos()
series = load_venctos()
px = pd.DataFrame(pd.read_csv("./json/parameters.csv"))
carteira = []
tabela = []
operacoes_escolhidas = []
sqliteConnection.close()
# with open('./json/series.json') as f:
#     series = json.load(f)

# with open('./json/ativos.json') as g:
#     ativos = json.load(g)

# with open('./json/parametros.json') as h:
#     parameters = json.load(h)
# -----------------------------------------------------------------------------------
# def PegaDadosVencto(vencimento):
#     for item in series:
#         if (item['data'] == vencimento):
#             return (item['data'],item['du'],item['serieCall'],item['seriePut'])
# -----------------------------------------------------------------------------------
def AtualizaParametros(vencto,carteira):
    vencimento_dados = PegaDadosVencto(vencto)
    parameters['vencimento']['data'] = vencimento_dados[0]
    parameters['vencimento']['du'] = vencimento_dados[1]
    parameters['vencimento']['serieCall'] = vencimento_dados[2]
    parameters['vencimento']['seriePut'] = vencimento_dados[3]
    with open('./json/parametros.json', "w") as outfile:
        json.dump(parameters, outfile)
# -----------------------------------------------------------------------------------
app = Flask(__name__)

@app.route("/",methods=['POST',"GET"])
def base():
    return render_template("index.html", series=series, ativos=ativos, carteira=carteira,
            tabela=tabela,parameters=parameters,operacoes_disponiveis=px['nome'],
            operacoes_escolhidas=operacoes_escolhidas,px=px)

@app.route("/add",methods=['POST',"GET"])
def add_itens():
    carteira.append(request.form["select_itens"])
    return redirect('/')

@app.route("/remove",methods=['POST',"GET"])
def remove_itens():
    checked_boxes = request.form.getlist("check")

    for item in checked_boxes:
        if item in carteira:
            idx = carteira.index(item)
            carteira.pop(idx)

    return redirect('/')
    # return render_template("index.html", series=series, ativos=ativos, carteira=carteira,
    #         tabela=tabela,parameters=parameters,operacoes_disponiveis=px['nome'],
    #         operacoes_escolhidas=operacoes_escolhidas,px=px)

@app.route("/scan",methods=['POST',"GET"])
def painel():
    if request.method=='POST':
        size = px.shape[0]
        i = 0
        while (i < size):
            px.iat[i,3] = request.form["A_" + str(i)]
            px.iat[i,4] = request.form["B_" + str(i)]
            px.iat[i,5] = request.form["C_" + str(i)]
            if (px.iat[i,2] > 3):
                px.iat[i,6] = request.form["D_" + str(i)]
            if (px.iat[i,2] > 4):
                px.iat[i,7] = request.form["E_" + str(i)] 
            i += 1
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        operacoes_escolhidas = request.form.getlist("check2")
        AtualizaParametros(request.form["selectVencto"],carteira)
        tabela = options_scan.scan_options(carteira,parameters,px,operacoes_escolhidas)
        return render_template("index.html", series=series, ativos=ativos, carteira=carteira,
                tabela=tabela,parameters=parameters,operacoes_disponiveis=px['nome'],
                operacoes_escolhidas=operacoes_escolhidas,px=px)

if __name__ == "__main__":
    app.run(debug=True)

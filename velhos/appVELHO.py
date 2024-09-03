from flask import Flask, render_template, request, redirect
import json
import options_scan
# -----------------------------------------------------------------------------------
with open('./json/series.json') as f:
    series = json.load(f)

with open('./json/ativos.json') as g:
    ativos = json.load(g)

with open('./json/parametros.json') as h:
    parameters = json.load(h)

carteira = []
tabela = []
# -----------------------------------------------------------------------------------
def PegaDadosVencto(vencimento):
    for item in series:
        if (item['data'] == vencimento):
            return (item['data'],item['du'],item['serieCall'],item['seriePut'])
# -----------------------------------------------------------------------------------
def AtualizaParametros(vencto,premioMin):
    vencimento_dados = PegaDadosVencto(vencto)
    parameters[0] = carteira
    parameters[2]['vencimento']['data'] = vencimento_dados[0]
    parameters[2]['vencimento']['du'] = vencimento_dados[1]
    parameters[2]['vencimento']['serieCall'] = vencimento_dados[2]
    parameters[2]['vencimento']['seriePut'] = vencimento_dados[3]
    premio = float(premioMin)
    if (premio > 1.0):
        parameters[3]['premio']['perc_minimo'] = premio
    else:
        parameters[3]['premio']['perc_minimo'] = 1.0
    with open('./json/parametros.json', "w") as outfile:
        json.dump(parameters, outfile)
# -----------------------------------------------------------------------------------
app = Flask(__name__)

@app.route("/",methods=['POST',"GET"])
def base():
    #return render_template("base.html", series=series, ativos=ativos, carteira=carteira,parameters=parameters)
    return render_template("base.html", series=series, ativos=ativos, carteira=carteira,tabela=tabela,parameters=parameters)

@app.route("/add",methods=['POST',"GET"])
def add_itens():
    carteira.append(request.form["select_itens"])
    return redirect('/')
    # return render_template("base.html", series=series, ativos=ativos, carteira=carteira,parameters=parameters)   

@app.route("/remove",methods=['POST',"GET"])
def remove_itens():
    checked_boxes = request.form.getlist("check")

    for item in checked_boxes:
        if item in carteira:
            idx = carteira.index(item)
            carteira.pop(idx)

    return render_template("base.html", series=series, ativos=ativos, carteira=carteira,parameters=parameters) 

@app.route("/scan",methods=['POST',"GET"])
def painel():
    if request.method=='POST':
        AtualizaParametros(request.form["selectVencto"],request.form['premioMin'])
        tabela = options_scan.scan_options(parameters)
        print("tab2 - ",len(tabela))
        return render_template("base.html", series=series, ativos=ativos, carteira=carteira,tabela=tabela,parameters=parameters)

if __name__ == "__main__":
    app.run(debug=True)

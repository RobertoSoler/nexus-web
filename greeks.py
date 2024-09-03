import numpy as np
from scipy.stats import norm
import json

def delta_calc(S, K, T, r, sigma, type="c"):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    try:
        if type == "c":
            delta_calc = norm.cdf(d1, 0, 1)
        elif type == "p":
            delta_calc = -norm.cdf(-d1, 0, 1)
        return delta_calc
    except:
        print("Please confirm option type, either 'c' for Call or 'p' for Put!")


with open('./json/ativos.json') as g:
    ativos = json.load(g)

def DELTA(dados,du,r):

    tabela = []
    codigo_anterior = ''
    sigma = 0.0
    T = du/252
    for line in dados:
        codigo_ativo = line[0]
        if (codigo_ativo != codigo_anterior):
            codigo_anterior = codigo_ativo
            for item in ativos:
                if (item['ticker'] == codigo_ativo):
                    sigma = item['sigma']
        S = line[1]
        if(line[4] != '9999'):
            K = line[5]
            pbdelta = delta_calc(S,K,T,r,sigma,'p')
        else:
            pbdelta = 0.0
        if(line[8] != '9999'):
            K = line[9]
            psdelta = delta_calc(S,K,T,r,sigma,'p')
        else:
            psdelta = 0.0
        if(line[12] != '9999'):
            K = line[13]
            csdelta = delta_calc(S,K,T,r,sigma,'c')
        else:
            csdelta = 0.0
        if(line[16] != '9999'):
            K = line[17]
            cbdelta = delta_calc(S,K,T,r,sigma,'c')
        else:
            cbdelta = 0.0

        k = (line[0],line[1],line[2],line[3],
            line[4],line[5],line[6],round(pbdelta,2),
            line[8],line[9],line[10],round(psdelta,2),
            line[12],line[13],line[14],round(csdelta,2),
            line[16],line[17],line[18],round(cbdelta,2),line[20])

        tabela.append(k)

    return tabela


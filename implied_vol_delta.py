import numpy as np
from scipy.stats import norm

N = norm.cdf

def BS_CALL(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * N(d1) - K * np.exp(-r*T)* N(d2)

def BS_PUT(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma* np.sqrt(T)
    return K*np.exp(-r*T)*N(-d2) - S*N(-d1)

def DELTA_IV(target_value,S, K, T, r, type="c"):
    sigma = I_VOL(target_value, S, K, T, r,type)
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    if type == "c":
        delta_calc = N(d1, 0, 1)
    elif type == "p":
        delta_calc = -N(-d1, 0, 1)
    return delta_calc
  
def BS_VEGA(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)

def I_VOL(target_value, S, K, T, r,type="c"):
    MAX_ITERATIONS = 200
    PRECISION = 1.0e-5
    sigma = 0.5
    for i in range(0, MAX_ITERATIONS):
      if type == "c":
        price = BS_CALL(S, K, T, r, sigma)
      elif type == "p":
        price = BS_PUT(S, K, T, r, sigma)
      vega = BS_VEGA(S, K, T, r, sigma)
      diff = target_value - price  # our root
      if (abs(diff) < PRECISION):
          return sigma
      sigma = sigma + diff/vega # f(x) / f'(x)
    return sigma # value wasn't found, return best guess so far

def DELTA(dados,du,r):
    tabela = []
    T = du/252
    for line in dados:
        S = line[1]
        if(line[4] != '9999'):
            K = line[5]
            price = line[6]
            pbdelta = DELTA_IV(price,S,K,T,r,'p')
        else:
            pbdelta = 0.0
        if(line[8] != '9999'):
            K = line[9]
            price = line[10]
            psdelta = DELTA_IV(price,S,K,T,r,'p')
        else:
            psdelta = 0.0
        if(line[12] != '9999'):
            K = line[13]
            price = line[14]
            csdelta = DELTA_IV(price,S,K,T,r,'c')
        else:
            csdelta = 0.0
        if(line[16] != '9999'):
            K = line[17]
            price = line[18]
            cbdelta = DELTA_IV(price,S,K,T,r,'c')
        else:
            cbdelta = 0.0

        k = (line[0],line[1],line[2],line[3],
            line[4],line[5],line[6],round(pbdelta,2),
            line[8],line[9],line[10],round(psdelta,2),
            line[12],line[13],line[14],round(csdelta,2),
            line[16],line[17],line[18],round(cbdelta,2),line[20])

        tabela.append(k)

    return tabela

# r = 0.14
# S = 95.32
# T = 32/252

# call = 1.09
# Kc = 106.16
# print('delta call - :',DELTA_IV(call, S, Kc, T, r, type="c"))

# put = 1.43
# Kp = 88.66
# print('delta put - :',DELTA_IV(put, S, Kp, T, r, type="p"))

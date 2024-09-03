import cotacoes
import implied_vol_delta as ivd

## PRECISA REVER ...

def EXPECTED_MOVE(book_ativo,lista):
    valC1 = 0.0
    valC2 = 0.0
    valC3 = 0.0
    valP1 = 0.0
    valP2 = 0.0
    valP3 = 0.0
    size = len(lista)
    i = 0
    while (i < size) and (valC1 == 0.0):
        ticker1 = lista[i][1].strip()
        tip1 = lista[i][5].strip()
        strik1 = lista[i][2]
        if (tip1 == 'COMPRA'):
            if (strik1 >= book_ativo):
                if valC2 > 0.0 and valC3 == 0.0:
                    valC3 = cotacoes.book_price(ticker1,'BID')
                if valC1 > 0.0 and valC2 == 0.0:
                    valC2 = cotacoes.book_price(ticker1,'BID')
                if valC1 == 0.0:
                    valC1 = cotacoes.book_price(ticker1,'BID')
        i += 1
    j = size - 1
    while (j > 0) and (valP1 == 0.0):
        ticker2 = lista[j][1].strip()
        tip2 = lista[j][5].strip()
        strik2 = lista[j][2]
        if (tip2 == 'VENDA'):
            if (strik2 <= book_ativo):
                if valP2 > 0.0 and valP3 == 0.0:
                    valP3 = cotacoes.book_price(ticker2,'BID')
                if valP1 > 0.0 and valP2 == 0.0:
                    valP2 = cotacoes.book_price(ticker2,'BID')
                if valP1 == 0.0:
                    valP1 = cotacoes.book_price(ticker2,'BID')
        j -= 1
    retorno = (valC1 + valP1)*0.6 + (valC2 + valP2)*0.3 + (valC3 + valP3)*0.10
    return retorno

def S_STRANGLE(ativo,lista,px,du,r):
    premioMinFin = px[3]
    premioMinPerc = px[4]
    book_ativo = cotacoes.book_price(ativo,'LAST')
    if(px['movto_espe']):
        movto_esperado = EXPECTED_MOVE(book_ativo,lista)
    else:
        movto_esperado = 0.00
    list_strangle = [];
    size = len(lista)
    i = 0
    indice = 0;
    while (i < size):
        ticker1 = lista[i][1].strip()
        tip1 = lista[i][5].strip()
        strik1 = lista[i][2]
        if (tip1 == 'COMPRA'):
            if (strik1 >= book_ativo + movto_esperado):
                preco1 = cotacoes.book_price(ticker1,'BID')
                if (preco1 > 0.01):
                    j = i - 1
                    while (j >= 0):
                        tip2 = lista[j][5].strip()
                        if (tip2 == 'VENDA'):
                            ticker2 = lista[j][1].strip()
                            strik2 = lista[j][2]
                            preco2 = cotacoes.book_price(ticker2,'BID')
                            if(preco2 > 0.01):
                                premio = preco1 + preco2
                                if (strik2 <= book_ativo - movto_esperado):
                                    if (premio >= premioMinPerc/100 * book_ativo) and (premio >= premioMinFin):
                                        list_strangle.append((ativo,book_ativo,indice,preco2+preco1,
                                        '9999',0,0,0,
                                        ticker2,strik2,preco2,0,
                                        ticker1,strik1,preco1,0,
                                        '9999',0,0,0,
                                        'S Stran'
                                        ))
                                        indice += 1
                        j -= 1
        i += 1

    tabela1 = ivd.DELTA(list_strangle,du,r)
    tabela2 = []
    for item in tabela1:
        if(abs(item[11]) <= px['delta_max']):
            if(abs(item[15]) <= px['delta_max']):
                tabela2.append(item)

    return tabela2

def S_JLIZARD(ativo,lista,px,du,r):
    book_ativo = cotacoes.book_price(ativo,'LAST')
    if(px['movto_espe']):
        movto_esperado = EXPECTED_MOVE(book_ativo,lista)
    else:
        movto_esperado = 0.00
    minima_diferenca = min(book_ativo * 0.01,1.00)
    premioMinFin = px[3]
    premioMinPerc = px[4]
    list_JLizard = [];
    size = len(lista)
    i = 0
    indice = 0
    while (i < size):
        ticker1 = lista[i][1].strip()
        tip1 = lista[i][5].strip()
        strik1 = lista[i][2]
        if (tip1 == 'COMPRA'):
            if (strik1 >= book_ativo):
                preco1 = cotacoes.book_price(ticker1,'BID')
                if (preco1 > 0.01):
                    j = i + 1
                    while (j < size):
                        tip2 = lista[j][5].strip()
                        if (tip2 == 'COMPRA'):
                            ticker2 = lista[j][1].strip()
                            strik2 = lista[j][2]
                            preco2 = cotacoes.book_price(ticker2,'BID')
                            difere = (strik2 -strik1)
                            premio = preco1 - preco2
                            if(difere > minima_diferenca):
                                if(preco2 > 0.01):
                                    if (preco1 - preco2) >= difere * premioMinPerc:
                                        k = j - 1
                                        while (k > 0):
                                            tip3 = lista[k][5].strip()
                                            if (tip3 == 'VENDA'):
                                                ticker3 = lista[k][1].strip()
                                                strik3 = lista[k][2]
                                                if (strik3 <= book_ativo - movto_esperado):
                                                    preco3 = cotacoes.book_price(ticker3,'BID')
                                                    if (preco3 > 0.01):
                                                            if (premio + preco3) > difere and (premio + preco3) < premioMinFin:
                                                                if (premio + preco3) > difere * (1 + premioMinPerc):
                                                                    list_JLizard.append((ativo,book_ativo,indice,premio + preco3,
                                                                    '9999',0,0,0,
                                                                    ticker3,strik3,preco3,0,
                                                                    ticker1,strik1,preco1,0,
                                                                    ticker2,strik2,preco2,0,
                                                                    'S Jade Lizard'
                                                                    ))
                                                                    indice += 1
                                            k -= 1
                        j += 1
        i += 1
    
    tabela1 = ivd.DELTA(list_JLizard,du,r)
    tabela2 = []
    for item in tabela1:
        if(abs(item[11]) <= px['delta_max']):
            tabela2.append(item)
    
    return tabela2

def S_ICONDOR(ativo,lista,px,du,r):
    book_ativo = cotacoes.book_price(ativo,'LAST')
    if(px['movto_espe']):
        movto_esperado = EXPECTED_MOVE(book_ativo,lista)
    else:
        movto_esperado = 0.00
    minima_diferenca = min(book_ativo * 0.01,1.00)
    premioMinFin = px[3]
    premioMinPerc = px[4]
    list_ICondor = [];
    size = len(lista)
    i = 0
    indice = 0
    while (i < size):
        ticker1 = lista[i][1].strip()
        tip1 = lista[i][5].strip()
        strik1 = lista[i][2]
        if (tip1 == 'COMPRA'):
            if (strik1 >= book_ativo + movto_esperado):
                preco1 = cotacoes.book_price(ticker1,'BID')
                if (preco1 > 0.01):
                    j = i + 1
                    while (j < size):
                        tip2 = lista[j][5].strip()
                        if (tip2 == 'COMPRA'):
                            ticker2 = lista[j][1].strip()
                            strik2 = lista[j][2]
                            difere1 = (strik2 -strik1)
                            if(difere1 > minima_diferenca):
                                preco2 = cotacoes.book_price(ticker2,'BID')
                                if(preco2 > 0.01):
                                    premio1 = preco1 - preco2
                                    k = j - 1
                                    while (k > 0):
                                        tip3 = lista[k][5].strip()
                                        if (tip3 == 'VENDA'):
                                            ticker3 = lista[k][1].strip()
                                            strik3 = lista[k][2]
                                            if(strik3 <= book_ativo - movto_esperado):
                                                preco3 = cotacoes.book_price(ticker3,'BID')
                                                if (preco3 > 0.01):
                                                    l = k - 1
                                                    while (l > 0):
                                                        tip4 = lista[l][5].strip()
                                                        if (tip4 == 'VENDA'):
                                                            ticker4 = lista[l][1].strip()
                                                            strik4 = lista[l][2]
                                                            if (strik4 < strik3):
                                                                difere2 = strik3 - strik4
                                                                if (difere1 == difere2):
                                                                    preco4 = cotacoes.book_price(ticker4,'BID')
                                                                    if(preco4 > 0.01):
                                                                        premio2 = preco3 - preco4
                                                                        if ((premio1 + premio2) / difere1 > premioMinPerc):
                                                                            if (premio1 + premio2 > premioMinFin):
                                                                                list_ICondor.append((ativo,book_ativo,indice,premio1 + premio2,
                                                                                ticker4,strik4,preco4,0,
                                                                                ticker3,strik3,preco3,0,
                                                                                ticker1,strik1,preco1,0,
                                                                                ticker2,strik2,preco2,0,
                                                                                'S I Condor'
                                                                                ))
                                                        l -= 1
                                        k -= 1
                        j += 1
        i += 1
    
    tabela1 = ivd.DELTA(list_ICondor,du,r)
    tabela2 = []
    for item in tabela1:
        if(abs(item[11]) <= px['delta_max']):
            if(abs(item[15]) <= px['delta_max']):
                tabela2.append(item)

    return tabela2

def S_STRADDLE(ativo,lista,px,du,r):
    book_ativo = cotacoes.book_price(ativo,'LAST')
    premioMinFin = px[3]
    premioMinPerc = px[4]
    list_straddle = [];
    size = len(lista)
    i = 0
    indice = 0;
    while (i < size):
        ticker1 = lista[i][1].strip()
        tip1 = lista[i][5].strip()
        strik1 = lista[i][2]
        if (tip1 == 'COMPRA'):
            if (strik1 >= book_ativo) and (strik1 < book_ativo * (1 + 0.01)):
                preco1 = cotacoes.book_price(ticker1,'BID')
                if (preco1 > 0.01):
                    j = i - 1
                    while (j >= 0):
                        tip2 = lista[j][5].strip()
                        if (tip2 == 'VENDA'):
                            ticker2 = lista[j][1].strip()
                            strik2 = lista[j][2]
                            preco2 = cotacoes.book_price(ticker2,'BID')
                            if(preco2 > 0.01):
                                premio = preco1 + preco2
                                if (strik2 <= book_ativo) and (strik2 >= book_ativo * (1 - 0.01)):
                                    if (premio > premioMinPerc/100 * book_ativo) and (premio >= premioMinFin):
                                        list_straddle.append((ativo,book_ativo,indice,premio,
                                        '9999',0,0,0,
                                        ticker2,strik2,preco2,0,
                                        ticker1,strik1,preco1,0,
                                        '9999',0,0,0,
                                        'S Strad'
                                        ))
                                        indice += 1
                        j -= 1
        i += 1
    
    tabela2 = ivd.DELTA(list_straddle,du,r)

    return tabela2

def S_CALLSPREAD(ativo,lista,px,du,r):
    book_ativo = cotacoes.book_price(ativo,'LAST')
    if(px['movto_espe']):
        movto_esperado = EXPECTED_MOVE(book_ativo,lista)
    else:
        movto_esperado = 0.00
    premioMinFin = px[3]
    premioMinPerc = px[4]
    premioSprePerc = px[7]
    minima_diferenca = min(book_ativo * 0.01,1.00)
    list_Cspread = [];
    size = len(lista)
    i = 0
    indice = 0;
    while (i < size):
        ticker1 = lista[i][1].strip()
        tip1 = lista[i][5].strip()
        strik1 = lista[i][2]
        if (tip1 == 'COMPRA'):
            if (strik1 >= book_ativo):
                preco1 = cotacoes.book_price(ticker1,'BID')
                if (preco1 > 0.01):
                    j = i + 1
                    while (j < size):
                        tip2 = lista[j][5].strip()
                        if (tip2 == 'COMPRA'):
                            ticker2 = lista[j][1].strip()
                            strik2 = lista[j][2]
                            preco2 = cotacoes.book_price(ticker2,'BID')
                            difere = (strik2 -strik1)
                            if(difere > minima_diferenca):
                                if(preco2 > 0.01):
                                    premioLiq = preco1 - preco2
                                    if premioLiq >= difere * premioSprePerc:
                                        if (premioLiq > premioMinFin) and (premioLiq > book_ativo * premioMinPerc):
                                            if (strik2 >= book_ativo + movto_esperado):
                                                list_Cspread.append((ativo,book_ativo,indice,premioLiq,
                                                '9999',0,0,0,
                                                '9999',0,0,0,
                                                ticker1,strik1,preco1,0,
                                                ticker2,strik2,preco2,0,
                                                'S C Spread'
                                                ))
                                                indice += 1
                        j += 1
        i += 1
    
    tabela1 = ivd.DELTA(list_Cspread,du,r)
    tabela2 = []
    for item in tabela1:
        if(abs(item[15]) <= px['delta_max']):
            tabela2.append(item)

    return tabela2

def S_PUTSPREAD(ativo,lista,px,du,r):
    book_ativo = cotacoes.book_price(ativo,'LAST')
    if(px['movto_espe']):
        movto_esperado = EXPECTED_MOVE(book_ativo,lista)
    else:
        movto_esperado = 0.00
    minima_diferenca = min(book_ativo * 0.01,1.00)
    premioMinFin = px[3]
    premioMinPerc = px[4]
    premioSprePerc = px[7]
    list_Pspread = [];
    size = len(lista)
    i = size - 1
    indice = 0
    while (i > 0):
        ticker1 = lista[i][1].strip()
        tip1 = lista[i][5].strip()
        strik1 = lista[i][2]
        if (tip1 == 'VENDA'):
            if (strik1 <= book_ativo):
                preco1 = cotacoes.book_price(ticker1,'BID')
                if (preco1 > 0.01):
                    j = i - 1
                    while (j > 0):
                        tip2 = lista[j][5].strip()
                        if (tip2 == 'VENDA'):
                            ticker2 = lista[j][1].strip()
                            strik2 = lista[j][2]
                            preco2 = cotacoes.book_price(ticker2,'BID')
                            difere = (strik1 -strik2)
                            if(difere > minima_diferenca):
                                if(preco2 > 0.01):
                                    premioLiq = preco1 - preco2
                                    if premioLiq >= difere * premioSprePerc:
                                        if (premioLiq > premioMinFin) and (premioLiq > book_ativo * premioMinPerc):
                                            if (strik2 <= book_ativo - movto_esperado):
                                                list_Pspread.append((ativo,book_ativo,indice,premioLiq,
                                                ticker2,strik2,preco2,0,
                                                ticker1,strik1,preco1,0,
                                                '9999',0,0,0,
                                                '9999',0,0,0,
                                                'S P Spread'
                                                ))
                                                indice += 1
                        j -= 1
        i -= 1
    
    tabela1 = ivd.DELTA(list_Pspread,du,r)
    tabela2 = []
    for item in tabela1:
        if(abs(item[11]) <= px['delta_max']):
            tabela2.append(item)

    return tabela2

#mt5.shutdown()
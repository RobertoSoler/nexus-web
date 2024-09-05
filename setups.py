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
    
    tabela1 = ivd.DELTA(list_Pspread,du,r)
    tabela2 = []
    for item in tabela1:
        if(abs(item[11]) <= px['delta_max']):
            tabela2.append(item)

    return tabela2

#mt5.shutdown()

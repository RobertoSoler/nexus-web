import cotacoes
import blackscholes as bs

def strangle(ativo,lista,premioMin,gap):
    book_ativo = cotacoes.book_price(ativo,'LAST')
    list_strangle = [];
    size = len(lista)
    i = 0
    indice = 0;
    while (i < size):
        ticker1 = lista[i][1].strip()
        tip1 = lista[i][5].strip()
        strik1 = lista[i][2]
        if (tip1 == 'COMPRA'):
            if (strik1 >= book_ativo) and (strik1 < book_ativo * (1 + gap)):
                preco1 = cotacoes.book_price(ticker1,'BID')
                if (preco1 > 0.0):
                    j = i - 1
                    while (j >= 0):
                        tip2 = lista[j][5].strip()
                        if (tip2 == 'VENDA'):
                            ticker2 = lista[j][1].strip()
                            strik2 = lista[j][2]
                            preco2 = cotacoes.book_price(ticker2,'BID')
                            if(preco2 > 0.0):
                                premio = preco1 + preco2
                                if (strik2 <= book_ativo) and (strik2 > book_ativo * (1 - gap)):
                                    if (premio > premioMin/100*book_ativo):
                                        list_strangle.append((ativo,book_ativo,indice,preco2+preco1,
                                        '9999',0,0,0,
                                        ticker2,strik2,preco2,0,
                                        ticker1,strik1,preco1,0,
                                        '9999',0,0,0
                                        ))
                                        indice += 1
                        j -= 1
        i += 1
    #list_strangle.sort(key = lambda x: x[3],reverse=True)
    return list_strangle
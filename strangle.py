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
    #list_strangle.sort(key = lambda x: x[3],reverse=True)
    return list_strangle

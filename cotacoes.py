import MetaTrader5 as mt5
mt5.initialize()

def book_price(ticker,tipo):
    preco = 0.00
    mt5.symbol_select(ticker,True)
    info = mt5.symbol_info_tick(ticker)
    # print(ticker)
    # print(info)
    if info:
        if tipo == 'BID':
            preco = info.bid
        if tipo == 'ASK':
            preco = info.ask
        if tipo == 'LAST':
            preco = info.last
    return preco
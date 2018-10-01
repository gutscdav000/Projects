from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order



def make_contract(symbol, security_type, eschange, primary_exchange, currency):

    Contract.m_symbol = symbol
    Contract.m_secType = security_type
    Contract.m_exchange = exchange
    Contract.m_primaryExch = primary_exchange
    Contract.m_currency = currency

    return Contract


# action: buy/sell, qty: how many, price: at what price 
def make_order(action, quantity, price = None):
    #limit action
    if price is not None:
        order = Order()
        # specifies a limit order
        order.m_orderType = 'LMT'
        order.m_totalQuantity = quantity
        order.m_action = action
        order.m_lmt = price
 
    # market action
    else:
        order = Order()
        # specifies a limit order
        order.m_orderType = 'MKT'
        order.m_totalQuantity = quantity
        order.m_action = action
        
    return order



def main():
    conn = Connection.create(port = 7496, clientId = 999) #you set clientID
    conn.connect()

    # must increment order ID's
    oid = 1

    #contracts  # smart routing IB
    cont = make_contract('TSLA', 'STK', 'SMART', 'SMART', 'USD')
    # 
    offer = make_order('BUY', 1, 200)

    conn.placeOrder(oid, cont, offer)
    conn.disconnect()


# NOTES:
# sometimes order doesn't come through on demo?
# must accept incoming connection in the GUI
# try getting order ID's so you know that it doesn't conflict

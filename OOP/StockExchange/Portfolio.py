class Portfolio:

    stock = list()
    cash_balance = 0

    def __init__(self):
        self.stock = list()
        self.cash_balance = 0

    def add_stock(self,stock):
        self.stock.append(stock)

    def remove_stock(self,stock):
        self.stock.remove(stock)
        
    def get_stock(self):
        return self.stock
    
    def get_cash_balance(self):
        return self.cash_balance
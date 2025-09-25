class Portfolio:

    __stock = list()
    cash_balance = 0
    __holdings = []

    def __init__(self):
        self.stock = list()
        self.cash_balance = 0

    def set_holding(self,holding):
        self.__holdings.append(holding)
    
    def get_holding(self):
        return self.__holdings
    
    def add_stock(self,stock):
        self.stock.append(stock)

    def remove_stock(self,stock):
        self.stock.remove(stock)
        
    def get_stock(self):
        return self.stock
    
    def get_cash_balance(self):
        return self.cash_balance
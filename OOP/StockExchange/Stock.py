class Stock:
    #atributes privates
    __symbol = {'AAPL':150.000,'GOOGL':20.000,'MSFT':32.000,'AMZN':45.000,'TSLA':23.000}

    #Construct
    def __init__(self):
        self.__symbol = input('Enter the ticker: ')

    def update_price(self,symbol,new_price):
        self.set_symbol(symbol,new_price)
        
    def register_ticker(self,symbol, price):
        self.set_symbol(symbol, price)
        
    #Methods
    def get_symbol(self,symbol):
        return self.__symbol[symbol]

    def set_symbol(self,symbol,price):
        self.__symbol[symbol] = price

    # when called, it returns a string representation of the object
    def __str__(self):
        for key in self.__symbol:
            str_dict = f"{key}: {self.__symbol[key]}\n"
        return f"The tickers is:{str_dict}"

from Trader import Trader

class ConservativeTrader(Trader):
    
    def decide_action(self, market):
        # Conservative strategy: Buy only if the stock price has dropped by more than 5% in the last day
        pass
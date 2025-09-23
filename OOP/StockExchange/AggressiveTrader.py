from Trader import Trader

class AggressiveTrader(Trader):
    
    def decide_action(self, market):
        # Aggressive strategy: Buy if the stock price has increased by more than 2% in the last day
        pass
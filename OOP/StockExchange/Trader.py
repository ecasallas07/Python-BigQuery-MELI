from abc import ABC, abstractmethod

class Trader(ABC):
    
    name = ''
    portfolio = list()
    initial_cash = 0.0    
    
    def __init__(self, name, portfolio,initial_cash):
        self.name = name
        self.portfolio = portfolio
        self.initial_cash = initial_cash

    @abstractmethod
    def decide_action(self, market):
        pass
    
    
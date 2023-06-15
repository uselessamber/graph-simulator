from math import *

class function: # f(x)
    func = None
    color = (0, 0, 0)
    def __init__(self, func, color = (0, 0, 0)):
        self.func = func
        self.color = color
    def evaluate(self, input):
        try:
            return self.func(input)
        except:
            return None
    def __str__(self):
        return self.func.__str__()
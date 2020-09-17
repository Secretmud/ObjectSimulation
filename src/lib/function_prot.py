import numpy as np

class function_prot:
    """This class is used to create and store the function for the plots.

    The file itself will be minimal but

    """
    def __init__(self, h, fu):
       self.h = h
       self.fu = fu

    def f(self, x, y):
        return eval(self.fu) 

    def fdx(self, x, y):
        return (self.f(x+self.h,y)-self.f(x-self.h,y))/(2*self.h)

    def fdy(self, x, y):
        return (self.f(x,y+self.h)-self.f(x,y-self.h))/(2*self.h)


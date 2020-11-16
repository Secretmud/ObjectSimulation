"""
    File name: function_prot.py
    Author: Tor Kristian
    Date created: 07/09/2020
    Date last modified: 28/09/2020
    Python Version: 3.8
"""

import numpy as np


class Function_prot:
    """This class is used to create and store the function for the plots.

    The file itself will be minimal but it does the job for now. Might explore better ways of approximating the derivatives later.
    """

    def __init__(self, h, fu):
        self.h = h
        self.fu = fu

    def f(self, x, y):
        """f(x, y) using eval to do a live evaluation of the mathematical function given in the terminal input, and return the output of that function"""
        return eval(self.fu)

    def fdx(self, x, y):
        """fdx(x, y) return the derivative approximate of the function with regards to x"""
        return (self.f(x + self.h, y) - self.f(x - self.h, y)) / (2 * self.h)

    def fdy(self, x, y):
        """fdy(x, y) return the derivative approximate of the function with regards to y"""
        return (self.f(x, y + self.h) - self.f(x, y - self.h)) / (2 * self.h)

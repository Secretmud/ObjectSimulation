"""
    File name: physics.py
    Author: Tor Kristian
    Date created: 07/09/2020
    Date last modified: 28/09/2020
    Python Version: 3.8
"""
from math import atan, sin, cos

class Physics:
    def __init__(self, g, mu, step):
        self.g = g
        self.mu = mu
        self.step = step

        
    # The signum
    def sign(self, x):
        """sign(x) return 1, 0 or -1 depending on size of x"""
        return 1 if (x > 0) else ( 0 if (x == 0) else -1)

    # The angle theta
    def theta(self, x):
        """theta(x) return arctan(x) where x if the derivative of f(x)"""
        return atan(x)

    # The normal force
    def N(self, ang):
        """N(ang) return the normal force at some angle ang"""
        return self.g * cos(ang)

    # The friction force
    def R(self, v, ang):
        """R(v, ang) return the friction depending on speed and angle"""
        if v > 0:
            return self.mu * self.N(ang)
        else:
            return -self.mu * self.N(ang)

    def collider(self, pos, lim):
        """collider(pos, lim) return 1 if the current pos is within the limit, or -1 if the pos is on the edge or outside"""
        return 1 if (min(lim[0], lim[1]) < pos < max(lim[0], lim[1])) else -1

from math import atan, sin, cos

class physics:
    def __init__(self, g, mu, step):
        self.g = g
        self.mu = mu
        self.step = step

        
    # The signum
    def sign(self, x):
        return 1 if (x > 0) else ( 0 if (x == 0) else -1)

    # The angle theta
    def theta(self, x):
        return atan(x)

    # The normal force
    def N(self, ang):
        return self.g*cos(ang)

    # The friction force
    def R(self, v, ang):
        if v > 0:
            return self.mu*self.N(ang)
        elif (v < 0):
            return -self.mu*self.N(ang)
        else:
            return self.sign(v)*min(self.g*sin(ang), self.mu*self.N(ang))

    """
    This function will check if we have a colliosion or not. 
    """
    def collider(self, pos, lim):
        return 1 if (min(lim[0], lim[1]) + self.step < pos < max(lim[0], lim[1]) - self.step) else -1

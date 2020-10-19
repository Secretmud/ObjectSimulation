import math


class InputValidation:

    def validatefunc(self, func):
        x = 1
        y = 1
        try:
            eval(func)
            return True
        except SyntaxError:
            return False

    def validatefloat(self, x):
        return True if (type(x) == float) else False

    def validatesimspeed(self, speed):
        if 0 < speed <= 100:
            return True
        else:
            return False

    def validateN(self, N):
        if type(N) == int:
            if 2 < N < 1e5:
                return True

        return False

    def validatestart(self, pos, lim):
        lower = min(lim[0], lim[1])
        upper = max(lim[0], lim[1])

        return True if (lower <= pos <= upper) else False

    def validatelim(self, lim):
        return True if lim[0] != lim[1] else False
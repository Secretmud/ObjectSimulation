from lib.physics import *
from lib.function_prot import *

class Algo:
    """Euler Cromer  
    

    This method class implements Euler Cromer, and is used to 

    """
    
    def __init__(self, N, mu, ax, v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC):
        self.fun = function_prot(0.0001, func)
        self.dt = dt
        self.N = N
        self.vx = [v_ix] *N
        self.vy = [v_iy] *N
        self.ax = [self.fun.fdx(self.vx[0],self.vy[0])] *N
        self.ay = [self.fun.fdy(self.vx[0],self.vy[0])] *N
        self.posx = [1] *N
        self.posy = [-4] *N
        self.posz = [self.fun.f(self.posx[0], self.posy[0])] *N
        self.p = physics(9.81, mu, self.dt)
        self.i = 0
        self.ax = ax
        self.l = 0
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.USER_PC = USER_PC


    def reset(self):
        if (self.i + 1 == self.N):
            self.i = 0
            self.posx[0] = self.posx[-1]
            self.posy[0] = self.posy[-1]
            self.posz[0] = self.posz[-1]
            self.vx[0] = self.vx[-1]
            self.vy[0] = self.vy[-1]
 

    def ang(self):
        angx = self.p.theta(self.fun.fdx(self.posx[self.i], self.posy[self.i]))
        angy = self.p.theta(self.fun.fdy(self.posx[self.i], self.posy[self.i]))

        return angx, angy

    
    def n(self, angx, angy):
        nx = self.p.N(angx)
        ny = self.p.N(angy)
        
        return nx, ny


    def R(self, angx, angy):
        rx = self.p.R(self.vx[self.i], angx)
        ry = self.p.R(self.vy[self.i], angy)

        return rx, ry
        
    
    def collision(self):
        self.vx[self.i+1] *= self.p.collider(self.posx[self.i+1], self.x_lim)
        self.vy[self.i+1] *= self.p.collider(self.posy[self.i+1], self.y_lim)

    def F(self, ang, n, r):
        return -n*sin(ang)-r*cos(ang)
        
    def euler(self, t):
        self.reset()

        (angx, angy) = self.ang()
        (nx, ny) = self.n(angx, angy)
        (rx, ry) = self.R(angx, angy)

        self.vx[self.i+1] = self.vx[self.i] + (self.F(angx, nx, rx))*self.dt
        self.vy[self.i+1] = self.vy[self.i] + (self.F(angy, ny, ry))*self.dt

        self.posx[self.i+1] = self.posx[self.i] + self.vx[self.i]*self.dt
        self.posy[self.i+1] = self.posy[self.i] + self.vy[self.i]*self.dt
        self.posz[self.i+1] = self.fun.f(self.posx[self.i], self.posy[self.i])

        self.collision()

        if t==0:
            self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")
        if t%self.USER_PC==0:
            self.l.remove()
            self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")

        self.i+=1

    def heuns(self, t):
        self.reset()

        (angx, angy) = self.ang()
        (nx, ny) = self.n(angx, angy)
        (rx, ry) = self.R(angx, angy)

        Vxm = self.vx[self.i] + self.F(angx, nx, rx)*self.dt
        Xm = self.posx[self.i] + self.vx[self.i]*self.dt
        self.posx[self.i+1] = self.posx[self.i] + Vxm*self.dt
        self.vx[self.i+1] = self.vx[self.i] - self.fun.f(Xm, Vxm)*self.dt 
        
        Vym = self.vy[self.i] + self.F(angy, ny, ry)*self.dt
        Ym = self.posy[self.i] + self.vy[self.i]*self.dt
        self.posy[self.i+1] = self.posy[self.i] + Vym*self.dt
        self.vy[self.i+1] = self.vy[self.i] - self.fun.f(Ym, Vym)*self.dt 

        self.posz[self.i+1] = self.fun.f(self.posx[self.i], self.posy[self.i])
        self.collision()
        
        
        
        if t==0:
            self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")
        if t%self.USER_PC==0:
            self.l.remove()
            self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")
            
        self.i+=1

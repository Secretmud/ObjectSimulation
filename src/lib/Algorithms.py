from lib.physics import *
from lib.function_prot import *

class Algo:
    """Algorithms used  
    

    This method class implements different type of algorithms, and is used to create different instances so that we
    can simulate them at the same time.

    """
    
    def __init__(self, N, mu, ax, v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC):
        self.fun = function_prot(0.0001, func)
        self.dt = dt
        self.N = N
        self.vx = [v_ix] *N
        self.vy = [v_iy] *N
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
        self.time = dt
        self.t_s = dt


    def reset(self):
        if (self.i + 1 == self.N):
            self.i = 0
            self.posx[0] = self.posx[-1]
            self.posy[0] = self.posy[-1]
            self.posz[0] = self.posz[-1]
            self.vx[0] = self.vx[-1]
            self.vy[0] = self.vy[-1]
 
        
    def a_x(self, x, y):
        ang = self.p.theta(self.fun.fdx(x, y))
        n = self.p.N(ang)
        r = self.p.R(self.vx[self.i], ang)
        return -n*sin(ang)-r*cos(ang)

    def a_y(self, x, y):
        ang = self.p.theta(self.fun.fdy(x, y))
        n = self.p.N(ang)
        r = self.p.R(self.vy[self.i], ang)
        return -n*sin(ang)-r*cos(ang)

    # Collision 
    def collision(self):
        self.vx[self.i+1] *= self.p.collider(self.posx[self.i+1], self.x_lim)
        self.vy[self.i+1] *= self.p.collider(self.posy[self.i+1], self.y_lim)

    def euler(self, t):
        """Euler's method is implemented below

        Euler's method is a rather simple aproach to this problem, but the overall fault in the calculation is similar to O(dt).
        Which makes it less forgiving when running with poor equipment or 
        """
        self.reset() # Reset if i + 1 == Self.N 

        a1 = self.a_x(self.posx[self.i], self.posy[self.i]) 
        a2 = self.a_y(self.posx[self.i], self.posy[self.i]) 

        self.vx[self.i+1] = self.vx[self.i] + a1*self.dt
        self.vy[self.i+1] = self.vy[self.i] + a2*self.dt

        self.posx[self.i+1] = self.posx[self.i] + self.vx[self.i]*self.dt
        self.posy[self.i+1] = self.posy[self.i] + self.vy[self.i]*self.dt
        self.posz[self.i+1] = self.fun.f(self.posx[self.i], self.posy[self.i])

        # Calling the collision function to have the object bounce of the wall
        self.collision()

        if t==0:
            self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")
        if t%self.USER_PC==0:
            self.l.remove()
            self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")

        self.i+=1
        self.time += self.t_s

        return (np.sqrt(np.power(self.vx[self.i], 2) + np.power(self.vy[self.i], 2)), np.sqrt(np.power(a1, 2) + np.power(a2, 2)))


    def heuns(self, t):
        """Heun's method is implemented below

        The idea of heun's is an improvement of Eulers which is implemented above, the fault. is a lot less. 
        This function should give a better prediction of the path an object would take when going down a slope
        """
        self.reset() # Reset if i + 1 == Self.N
        a1 = self.a_x(self.posx[self.i] + self.vx[self.i]*self.dt/2, self.posy[self.i] + self.vy[self.i]*self.dt/2) 
        a2 = self.a_y(self.posx[self.i] + self.vx[self.i]*self.dt/2, self.posy[self.i] + self.vy[self.i]*self.dt/2)
        self.vx[self.i+1] = self.vx[self.i] + a1*self.dt 
        self.vy[self.i+1] = self.vy[self.i] + a2*self.dt 
        self.posx[self.i+1] = self.posx[self.i] + self.vx[self.i]*self.dt + (np.power(self.dt, 2)/2)*(self.fun.f(self.posx[self.i], self.posy[self.i]))
        self.posy[self.i+1] = self.posy[self.i] + self.vy[self.i]*self.dt + (np.power(self.dt, 2)/2)*(self.fun.f(self.posx[self.i], self.posy[self.i]))
        self.posz[self.i+1] = self.fun.f(self.posx[self.i], self.posy[self.i])

        # Calling the collision function to have the object bounce of the wall
        self.collision()
        
        # Create the scatter object at  t==0, and delete it and create it again for every iteration you've set.
        # This creates a smooth animation.
        if t==0:
            self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")
        if t%self.USER_PC==0:
            self.l.remove()
            self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")
        # Increment i    
        self.i+=1
        self.time += self.t_s

        return (np.sqrt(np.power(self.vx[self.i], 2) + np.power(self.vy[self.i], 2)), np.sqrt(np.power(a1, 2) + np.power(a2, 2)))

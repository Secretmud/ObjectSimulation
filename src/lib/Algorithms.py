"""
    File name: Algorithms.py
    Author: Tor Kristian
    Date created: 07/09/2020
    Date last modified: 28/09/2020
    Python Version: 3.8
"""
from lib.physics import *
from lib.function_prot import *

class Algo:
    """Algorithms used  
    

    This method class implements different type of algorithms, and is used to create different instances so that we
    can simulate them at the same time.
    """
    def __init__(self, N, mu, ax, v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC, plot, x, y):
        self.fun = function_prot(0.0001, func)
        self.dt = dt
        self.N = N
        self.vx = [v_ix] *N
        self.vy = [v_iy] *N
        self.posx = [x] *N
        self.posy = [y] *N
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
        self.plot = plot


    def setdt(self, dt):
            self.dt = dt
        
    def reset(self):
        """reset() checks if i + 1 is equal to the set list size, if it is it copies the last value and inserts it into the start of the list.
        
        it also resets the i to be equal to 0m.
        It takes no arguments and is implemented with reusability in mind.
        """
        if (self.i + 1 == self.N):
            self.i = 0
            self.posx[0] = self.posx[-1]
            self.posy[0] = self.posy[-1]
            self.posz[0] = self.posz[-1]
            self.vx[0] = self.vx[-1]
            self.vy[0] = self.vy[-1]
 
        
    def a_x(self, x, y):
        """a_x(x, y) return the current acceleration with regards to the x velocity vector"""
        ang = self.p.theta(self.fun.fdx(x, y))
        n = self.p.N(ang)
        r = self.p.R(self.vx[self.i], ang)
        return -n*sin(ang)-r*cos(ang)

    def a_y(self, x, y):
        """a_y(x, y) return the current acceleration with regards to the y velocity vector"""
        ang = self.p.theta(self.fun.fdy(x, y))
        n = self.p.N(ang)
        r = self.p.R(self.vy[self.i], ang)
        return -n*sin(ang)-r*cos(ang)

    # Collision 
    def collision(self):
        """collision() utelize the collider function declared in physics.py and modifies the next speed if it's not within the given limits"""
        self.vx[self.i+1] *= self.p.collider(self.posx[self.i+1], self.x_lim)
        self.vy[self.i+1] *= self.p.collider(self.posy[self.i+1], self.y_lim)

    def euler(self, t):
        """euler(t) takes iteration as an argument. 

        Euler's forward method is a simple but kinda inefective with a ΔT < 0.001 and it quickly becomes ugly when you reduce the  ΔT to much, a  ΔT at 0.05 or larger 
        provides a large fault. Seeing that the fault in Forward Euler is approximatly equal to the  ΔT.
         
        returns a tuple (v_vector, a_vector)
        """
        self.reset() # Reset if i + 1 == Self.N 

        a1 = self.a_x(self.posx[self.i], self.posy[self.i]) # Calculate acceleration at the given time for x and y
        a2 = self.a_y(self.posx[self.i], self.posy[self.i]) 

        self.vx[self.i+1] = self.vx[self.i] + a1*self.dt # Caluculate the velocity at the next step
        self.vy[self.i+1] = self.vy[self.i] + a2*self.dt

        self.posx[self.i+1] = self.posx[self.i] + self.vx[self.i]*self.dt # Update the next position for x,y and z. x and y is calculated based on the velocity and z is based on x and y.
        self.posy[self.i+1] = self.posy[self.i] + self.vy[self.i]*self.dt
        self.posz[self.i+1] = self.fun.f(self.posx[self.i+1], self.posy[self.i+1])

        # Calling the collision function to have the object bounce of the wall
        self.collision()

        # Create the scatter object at  t==0, and delete it and create it again for every iteration you've set.
        # This creates a smooth animation.
        if self.plot:
            if t==0:
                self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")
            if t%self.USER_PC==0:
                self.l.remove()
                self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")

        # Increment i    
        self.i+=1

        return (self.posx[self.i-1], self.posy[self.i-1]) 


    def heuns(self, t):
        """heuns(t) takes iteration as an argument. 

        The idea of heun's is an improvement of Eulers which is implemented above, the fault. is a lot less. 
        This function should give a better prediction of the path an object would take when going down a slope.
        The outcome of the this method gives higher accuracy of O(ΔT²) rather than Forward Euler which is O(ΔT). 

        returns a tuple (v_vector, a_vector)
        """
        self.reset() # Reset if i + 1 == Self.N
        a1 = self.a_x(self.posx[self.i] + self.vx[self.i]*self.dt/2, self.posy[self.i] + self.vy[self.i]*self.dt/2) # Calculate the acceleration at the at the current step  
        a2 = self.a_y(self.posx[self.i] + self.vx[self.i]*self.dt/2, self.posy[self.i] + self.vy[self.i]*self.dt/2)
        self.vx[self.i+1] = self.vx[self.i] + a1*self.dt # Update the the velocity for the next step  
        self.vy[self.i+1] = self.vy[self.i] + a2*self.dt 
        # Update the next position for x,y and z. x and y is calculated based on the velocity and z is based on x and y. 
        self.posx[self.i+1] = self.posx[self.i] + self.vx[self.i]*self.dt + (np.power(self.dt, 2)/2)*(self.fun.f(self.posx[self.i], self.posy[self.i]))
        self.posy[self.i+1] = self.posy[self.i] + self.vy[self.i]*self.dt + (np.power(self.dt, 2)/2)*(self.fun.f(self.posx[self.i], self.posy[self.i]))
        self.posz[self.i+1] = self.fun.f(self.posx[self.i+1], self.posy[self.i+1])

        # Calling the collision function to have the object bounce of the wall
        self.collision()
        
        # Create the scatter object at  t==0, and delete it and create it again for every iteration you've set.
        # This creates a smooth animation.
        if self.plot:
            if t==0:
                self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")
            if t%self.USER_PC==0:
                self.l.remove()
                self.l = self.ax.scatter(self.posx, self.posy, self.posz, color="black")

        # Increment i    
        self.i+=1

        return (self.posx[self.i-1], self.posy[self.i-1]) 

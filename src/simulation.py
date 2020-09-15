from math import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from lib.physics import *
from time import sleep

print("Simulating a object sliding down a function")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# The function with plot as a surface and use as a temp Z value for the calculation 
def f(x, y):
    return np.cos(x)+np.sin(y)

def fdx(x,y):
    h = 0.0001
    return (f(x+h,y)-f(x-h,y))/(2*h)

def fdy(x,y):
    h = 0.0001
    return (f(x,y+h)-f(x,y-h))/(2*h)

N = 3 
x_lim = [-5, 1]
y_lim = [2, -5]
vx = [4] *N
vy = [5] *N
posx = [-2] *N
posy = [-3] *N
posz = [f(posx[0], posy[0])] *N
i = 0
m = 1
p = physics(m, 9.81, 0.1)
dt = 0.006

"""
This function is the live simulation, it utilizes matplotlibs.animation.FuncAnimation.
This let's us run the simulation for as long as we want, and have it updated in realtime.  
"""        
def animate(t):
    global i
    # Created 5 lists with the length of 3
    # Using this if-check to reset them all
    if (i + 1 == N):
        i = 0
        posx[0] = posx[-1]
        posy[0] = posy[-1]
        posz[0] = posz[-1]
        vx[0] = vx[-1]
        vy[0] = vy[-1]
        
    angx = p.theta(fdx(posx[i], posy[i]))
    angy = p.theta(fdy(posx[i], posy[i]))
    
    nx = p.N(angx)
    ny = p.N(angy)
    
    rx = p.R(vx[i], angx)
    ry = p.R(vy[i], angy)

    vx[i+1] = vx[i] + ((-nx*sin(angx)-rx*cos(angx))*dt)/m
    vy[i+1] = vy[i] + ((-nx*sin(angx)-rx*cos(angx))*dt)/m

    posx[i+1] = posx[i] + vx[i]*dt
    posy[i+1] = posy[i] + vy[i]*dt
    posz[i+1] = f(posx[i], posy[i])

    vx[i+1] *= p.collider(posx[i+1], x_lim)
    vy[i+1] *= p.collider(posy[i+1], y_lim)

    
    if t%10==0:
        ax.plot(posx, posy, posz, color="black")
        
    print("{:4}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\r".format(t, angx, angy, rx, ry, nx, ny, vx[i], vy[i]), end="")
    
    i += 1


X = np.linspace(x_lim[0], x_lim[1], 50)
Y = np.linspace(y_lim[0], y_lim[1], 50)
X,Y = np.meshgrid(X, Y)

Z = f(X,Y)
    
ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")


sim = FuncAnimation(plt.gcf(), animate,
                    frames=1800,
                    interval=1,
                    blit=False)
    

plt.show()

print("Simulation is finished")

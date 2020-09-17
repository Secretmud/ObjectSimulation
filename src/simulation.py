from math import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from lib.physics import *
from lib.function_prot import *
from time import sleep

print("Simulating a object sliding down a function")

i = 0
dt = float(input("Enter a value for delta t:\t"))
p = physics(9.81, 0.1, dt)
fun = function_prot(0.0001, input("The function you want to evaluate:\t"))

print(fun.f(0, 1))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

USER_PC = int(input("How often do you want to plot? from 1..100(1 requires extreme PC performance, you're adviced to set atleast 10):\t"))
v_ix = float(input("Initial x velocity:\t"))
try:
    v_iy = float(input("Initial y velocity(leave blank if you want the same as x):\t"))
except ValueError:
    v_iy = None
v_iy = v_ix if (v_iy == None) else v_iy

# The function with plot as a surface and use as a temp Z value for the calculation 

N = 10 
x_lim = [-5, 5]
y_lim = [-5, 5]
vx = [v_ix] *N
vy = [v_iy] *N
posx = [-1] *N
posy = [-4] *N
posz = [fun.f(posx[0], posy[0])] *N

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
        posx[:5] = posx[-5:]
        posy[:5] = posy[-5:]
        posz[:5] = posz[-5:]
        vx[0] = vx[-1]
        vy[0] = vy[-1]
        
        
    angx = p.theta(fun.fdx(posx[i], posy[i]))
    angy = p.theta(fun.fdy(posx[i], posy[i]))
    
    nx = p.N(angx)
    ny = p.N(angy)
    
    rx = p.R(vx[i], angx)
    ry = p.R(vy[i], angy)

    vx[i+1] = vx[i] + (-nx*sin(angx)-rx*cos(angx))*dt
    vy[i+1] = vy[i] + (-ny*sin(angy)-ry*cos(angy))*dt

    posx[i+1] = posx[i] + vx[i]*dt
    posy[i+1] = posy[i] + vy[i]*dt
    posz[i+1] = fun.f(posx[i], posy[i])

    vx[i+1] *= p.collider(posx[i+1], x_lim)
    vy[i+1] *= p.collider(posy[i+1], y_lim)

    if t%USER_PC==0:
        ax.scatter(posx[i], posy[i], posz[i], color="black")

    #print("{:4}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\r".format(t, angx, angy, rx, ry, nx, ny, vx[i], vy[i]), end="")
    
    i += 1


X = np.linspace(x_lim[0], x_lim[1], 50)
Y = np.linspace(y_lim[0], y_lim[1], 50)
X,Y = np.meshgrid(X, Y)

Z = fun.f(X,Y)
    
ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")


sim = FuncAnimation(plt.gcf(), animate,
                    frames=1800,
                    interval=20,
                    blit=False)
    

plt.show()

print("Simulation is finished")

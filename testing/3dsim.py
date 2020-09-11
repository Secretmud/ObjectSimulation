from math import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from lib.physics import *

print("Simulating a object sliding down a function")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



save_plot = input("Do you want to save the plot[y/n]?\t")
mu = float(input("Enter a value for mu:\t"))
g = 9.81
m = float(input("Enter the mass:\t"))
dt = float(input("Enter the Δt:\t"))
v_init = float(input("Enter the velocity in km/h:\t"))/3.6
v_x = [v_init]
v_y = [0]
x_sim = [0.1]
i = 0
#func = input("Enter the function to test:\t")
x_vec = [0]
fps_tot = 60
x_tail = []
y_tail = []

p = physics(m, g, mu)

# The function to use
def f(x, y):
    return np.cos(x)
    #return eval(func)

y_sim = [0.1]
z_sim = [f(x_sim[0], y_sim[0])]
# The function derivative 

def fdx(x,y):
    h = 0.0001
    return (f(x+h,y)-f(x-h,y))/(2*h)

def fdy(x,y):
    h = 0.0001
    return (f(x,y+h)-f(x,y-h))/(2*h)

"""
This function is the live simulation, it utilizes matplotlibs.animation.FuncAnimation.
This let's us run the simulation for as long as we want, and have it updated in realtime.  
"""        
def animate(t):
    global i, dt
    angx = p.theta(fdx(x_sim[i], y_sim[i]))
    angy = p.theta(fdy(x_sim[i], y_sim[i]))
    nx = p.N(angx)
    rx = p.R(v_x[i], angx)
    ny = p.N(angy)
    ry = p.R(v_y[i], angy)
    z_sim.append(f(x_sim[i], y_sim[i]))
    v_x.append(v_x[i] + ((-nx*sin(angx)-rx*cos(angx))*dt)/m)
    v_y.append(v_y[i] + ((-ny*sin(angy)-rx*cos(angy))*dt)/m)
    x_sim.append(x_sim[i] + v_x[i]*dt)
    y_sim.append(y_sim[i] + v_y[i]*dt)
    
    plt.cla()
    ax.plot_wireframe(X, Y, Z, rstride=5, cstride=5)
    ax.plot(x_sim, y_sim, z_sim, color="black")
    if i >= 4:
        ax.scatter(x_sim[i], y_sim[i], z_sim[i], color="black")

    
    
    print("{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\t{:4.3f}\r".format(x_sim[i], y_sim[i], z_sim[i], v_x[i], v_y[i]), end="")
    i += 1

X = np.linspace(-7.5, 0, 300)
Y = np.linspace(0, 30, 300)
X,Y = np.meshgrid(X, Y)

Z = f(X, Y)
    
    
sim = FuncAnimation(plt.gcf(), animate,
                    frames=1800,
                    interval=20,
                    blit=False)

if (save_plot.lower() == "y"):
    sim_name = input("Enter the name of the simulation:\t")
    print("Writing the animation to a file...")
    sim.save(sim_name, fps=fps_tot, extra_args=['-vcodec', 'libx264'])
else:
    print("Playing the animation")
    plt.show()
print("\nSimulation was ended")

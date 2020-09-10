from math import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

print("Simulating a object sliding down a function")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

save_plot = input("Do you want to save the plot[y/n]?\t")
mu = float(input("Enter a value for mu:\t"))
g = 9.81
m = float(input("Enter the mass:\t"))
dt = float(input("Enter the Δt:\t"))
v_init = float(input("Enter the velocity in km/h:\t"))/3.6
v = [v_init]
x_sim = [0]
i = 0
#func = input("Enter the function to test:\t")
x_vec = [0]
fps_tot = 60
x_tail = []
y_tail = []

# The function to use
def f(x, y):
    return x+2*y 
    #return eval(func)

y_sim = [f(x_sim[0], 0)]
z_sim = [f(x_sim[0], y_sim[0])]
# The function derivative 
def fd(x):
    h = 0.0001
    return (f(x+h)-f(x-h))/(2*h)

def fdx(x,y):
    h = 0.001
    return (f(x+h,y)-f(x-h,y))/(2*h)

def fdy(x,y):
    h = 0.001
    return (f(x,y+h)-f(x,y-h))/(2*h)

# The signum
def sign(x):
    return 1 if (x > 0) else ( 0 if (x == 0) else -1)

# The angle theta
def theta(x):
    return atan(x)

# The normal force
def N(ang):
    return m*g*cos(ang)

# The friction force
def R(v, ang, x):
    if v[i] > 10e-8:
        return mu*N(ang)
    elif (v[i] < 10e-8):
        return -mu*N(ang)
    elif (abs(v[i]) < 10e-8):
        return sign(x)*min(m*g*sin(ang), mu*N(ang))
    
"""
This function will check if we have a colliosion or not. 
"""
def collision(x, y, xs, ys):
    if (xs > x and ys >= y):
        return True
    return False

"""
This function is the live simulation, it utilizes matplotlibs.animation.FuncAnimation.
This let's us run the simulation for as long as we want, and have it updated in realtime.  
"""        
def animate(t):
    global i, dt
    # some setup
    if (i == 0):
        for ii in range(1, 800):
            pass
            
    plt.title("Braking length: %imeters" %i)
#    ang = theta(fd(x_sim[i]))
    angx = theta(fdx(x_sim[i], y_sim[i]))
    angy = theta(fdy(x_sim[i], y_sim[i]))
    nx = N(angx)
    rx = R(v, angx, x_sim[i])
    ny = N(angy)
    ry = R(v, angy, y_sim[i])
    v_x = v[i] + ((-nx*sin(angx)-rx*cos(angx))*dt)/m
    v_y = v[i] + ((-ny*cos(angy)-rx*sin(angy))*dt)/m
    v.append(v_x-v_y)
    x_sim.append(x_sim[i] + v[i]*dt)
    y_sim.append(y_sim[i] + v[i]*dt)
    z_sim.append(f(x_sim[i], y_sim[i]))
    plt.cla()
    
    print("v(i): {:4.3f}\tx: {:2.3f}\t\r".format(v[i]*3.6, x_sim[i]), end="")
    ax.plot_surface(x_sim[i], y_sim[i], z_sim[i])
    i += 1
    plt.legend(loc="upper right")

    
    
sim = FuncAnimation(plt.gcf(), animate,
                    frames=1800,
                    interval=10,
                    blit=False)

if (save_plot.lower() == "y"):
    sim_name = input("Enter the name of the simulation:\t")
    print("Writing the animation to a file...")
    sim.save(sim_name, fps=fps_tot, extra_args=['-vcodec', 'libx264'])
else:
    print("Playing the animation")
    plt.show()
print("\nSimulation was ended")

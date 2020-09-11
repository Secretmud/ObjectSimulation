from math import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from lib.physics import *

print("Simulating a object sliding down a function")


save_plot = input("Do you want to save the plot[y/n]?\t")
mu = float(input("Enter a value for mu:\t"))
g = 9.81
m = float(input("Enter the mass:\t"))
dt = float(input("Enter the Δt:\t"))
v_init = float(input("Enter the velocity in km/h:\t"))/3.6
v = [v_init]
x_sim = [0]
i = 0
func = input("Enter the function to test:\t")
x_vec = [0]
fps_tot = 60

p = physics(m, g, mu)

# The function to use
def f(x):
    return eval(func)

y_vec = [f(x_vec[0])]
y_sim = [f(x_sim[0])]
# The function derivative 
def fd(x):
    h = 0.0001
    return (f(x+h)-f(x-h))/(2*h)
    
"""
This function is the live simulation, it utilizes matplotlibs.animation.FuncAnimation.
This let's us run the simulation for as long as we want, and have it updated in realtime.  
"""

x_tail = []
y_tail = []

def animate(t):
    global i, dt
    # some setup
    if (i == 0):
        for ii in range(0, 6000):
            x_vec.append(x_vec[ii]+dt)
            y_vec.append(f(x_vec[ii]))
            
    plt.title("Braking length: %imeters" %i)
    y=f(x_sim[i])
    y_sim.append(y)
    fdv = fd(x_sim[i])
    ang = theta(fdv)
    n = N(ang)
    r = R(v, ang, x_sim[i])
    n_v = v[i] + ((-n*sin(ang)-r*cos(ang))*dt)/m 
    v.append(n_v)
    x_sim.append(x_sim[i] + v[i]*dt)
    plt.cla()
    
    print("v(i+1): {:4.3f}\tv(i): {:4.3f}\tx: {:2.3f}\t\r".format(n_v*3.6, v[i]*3.6, x_sim[i]), end="")
    plt.plot(x_sim[i], y_sim[i], marker="*", color="red", label="Simulation")
    if (i >= 1):
        x_tail.append(x_sim[i-1])
        y_tail.append(y_sim[i-1])
        plt.plot(x_tail, y_tail, linestyle="solid", color="black")

    i += 1
    plt.plot(x_vec, y_vec, color="orange", label="Function") 
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

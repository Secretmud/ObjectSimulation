"""
    File name: simulation.py
    Author: Tor Kristian
    Date created: 07/09/2020
    Date last modified: 28/09/2020
    Python Version: 3.8
"""
from math import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from lib.Algorithms import *
from lib.function_prot import *

print("Simulating a object sliding down a function")

i = 0
dt = float(input("Enter a value for delta t:\t"))

# Doing some assignments for matplotlib, fig, ax[2] 
fig = plt.figure()
ax = [0]*2
ax[0] = fig.add_subplot(211, projection='3d')
ax[1] = fig.add_subplot(212, projection='3d')
func = input("Enter the function:\t")
mu = float(input("Enter the friction ceofficient:\t"))

USER_PC = int(input("How often do you want to plot? from 1..100(1 requires extreme PC performance, you're adviced to set atleast 10):\t"))
v_ix = float(input("Initial x velocity:\t"))
try:
    v_iy = float(input("Initial y velocity(leave blank if you want the same as x):\t"))
except ValueError:
    v_iy = None
v_iy = v_ix if (v_iy == None) else v_iy

# N set's the tail size, it can be anything from 1 to whatever you want
try:
    N = int(input("Tail size(3..):\t"))
except ValueError:
    N = 3

if (N < 3):
    N = 3
    print("N has to be three or larger, N is set to 3")

# Setting the x and y limit.
x_lim = [float(input("x, lower:\t")), float(input("x, upper:\t"))]
y_lim = [float(input("y, lower:\t")), float(input("y, upper:\t"))]
# Setting starting x and y. But with default values, x = x_lim[0] + 1 and y = y_lim[0] + 1.
x = ""
y = ""
# Doing a try except for ValueError, and asserting default values if the ValueError is hit
try:
    x = int(input(f"provide a starting value for x(default is {x_lim[0] + 1}):\t"))
except ValueError:
    if x == "":
        x = x_lim[0] + 1
try:    
    y = int(input(f"provide a starting value for y(default is {y_lim[0] + 1}):\t"))
except ValueError:
    if y == "":
        y = y_lim[0] + 1

# Initializing Forward Euler and Heuns with the values they need.
e = Algo(N, mu, ax[0], v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC, x, y)
h = Algo(N, mu, ax[1], v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC, x, y)

# Using linspace with limts to create the X and Y values
X = np.linspace(x_lim[0], x_lim[1], 50)
Y = np.linspace(y_lim[0], y_lim[1], 50)
# Creating a meshgrig with the two linspaces above
X,Y = np.meshgrid(X, Y)
fun = function_prot(0.001, func)
# Creating Z using the given function
Z = fun.f(X,Y)
# Initializing the plot using a for loop and giving them titles
titles = ["Euler Cromer", "Heun's Method"]
for i in range(len(ax)):
    ax[i].plot_wireframe(X, Y, Z, rstride=5, cstride=5)
    ax[i].set_title(titles[i])
    ax[i].set_xlabel("X-axis")
    ax[i].set_ylabel("Y-axis")
    ax[i].set_zlabel("Z-axis")

# Setting a initial value for t and running the while loop forever and plotting every 0.05 seconds
t = 0
while True:
    e.euler(t)
    h.heuns(t)
    t+=1
    plt.pause(0.05)

plt.show()

print("Simulation is finished")

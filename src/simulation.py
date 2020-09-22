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

fig = plt.figure()
ax = [0]*4
ax[0] = fig.add_subplot(221, projection='3d')
ax[1] = fig.add_subplot(222, projection='3d')
ax[2] = fig.add_subplot(223, projection='3d')
ax[3] = fig.add_subplot(224, projection='3d')
#ax1 = fig.add_subplot(212, projection='3d')
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
N = int(input("Tail size(1..):\t")) 
x_lim = [-5, 5]
y_lim = [-5, -1]

e = Algo(N, mu, ax[0], v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC)
h = Algo(N, mu, ax[1], v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC)
r = Algo(N, mu, ax[2], v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC)

X = np.linspace(x_lim[0], x_lim[1], 50)
Y = np.linspace(y_lim[0], y_lim[1], 50)
X,Y = np.meshgrid(X, Y)
fun = function_prot(0.0001, func)
Z = fun.f(X,Y)
titles = ["Euler Cromer", "Heun's Method", "RK4", "Summary"]
for i in range(len(ax)):
    ax[i].plot_wireframe(X, Y, Z, rstride=5, cstride=5)
    ax[i].set_title(titles[i])
    ax[i].set_xlabel("X-axis")
    ax[i].set_ylabel("Y-axis")
    ax[i].set_zlabel("Z-axis")


t = 0

while True:
    e.euler(t)
    h.heuns(t)
    r.rk4(t)
    t+=1
    plt.pause(dt)

plt.show()

print("Simulation is finished")

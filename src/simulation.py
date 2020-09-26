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

x_lim = [-5, 5]
y_lim = [-5, -1]

e = Algo(N, mu, ax[0], v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC)
h = Algo(N, mu, ax[1], v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC)

X = np.linspace(x_lim[0], x_lim[1], 50)
Y = np.linspace(y_lim[0], y_lim[1], 50)
X,Y = np.meshgrid(X, Y)
fun = function_prot(0.001, func)
Z = fun.f(X,Y)
titles = ["Euler Cromer", "Heun's Method"]
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
    t+=1
    plt.pause(0.05)

plt.show()

print("Simulation is finished")

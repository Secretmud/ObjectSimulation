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
from time import sleep


class Simulation:

    def __init__(self, dt, func, mu, update_time, v_ix, v_iy, n, x_lim, y_lim, plot, x, y):
        self.dt = dt
        self.fig = plt.figure()
        self.ax = [0] * 2
        self.ax[0] = self.fig.add_subplot(121, projection='3d')
        self.ax[1] = self.fig.add_subplot(122, projection='3d')
        self.e = Algo(n, mu, self.ax[0], v_ix, v_iy, func, dt, x_lim, y_lim, update_time, plot, x, y)
        self.h = Algo(n, mu, self.ax[1], v_ix, v_iy, func, dt, x_lim, y_lim, update_time, plot, x, y)
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.func = func


    def simulate(self):
        # Using linspace with limts to create the X and Y values
        X = np.linspace(self.x_lim[0], self.x_lim[1], 60)
        Y = np.linspace(self.y_lim[0], self.y_lim[1], 60)
        # Creating a meshgrig with the two linspaces above
        X, Y = np.meshgrid(X, Y)
        fun = function_prot(0.001, self.func)
        # Creating Z using the given function
        Z = fun.f(X, Y)
        # Initializing the plot using a for loop and giving them titles
        titles = ["Forward Euler", "Heun's Method"]
        for i in range(len(self.ax)):
            self.ax[i].plot_wireframe(X, Y, Z, rstride=3, cstride=3)
            self.ax[i].set_title(titles[i])
            self.ax[i].set_xlabel("X-axis")
            self.ax[i].set_ylabel("Y-axis")
            self.ax[i].set_zlabel("Z-axis")

        # Setting a initial value for t and running the while loop forever and plotting every 0.05 seconds
        t = 0
        while True:
            self.e.euler(t)
            self.h.heuns(t)
            t += 1
            plt.pause(0.05)

    def show_function(self):
        check = self.fig.add_subplot(111, projection='3d')
        # Using linspace with limts to create the X and Y values
        X = np.linspace(self.x_lim[0], self.x_lim[1], 60)
        Y = np.linspace(self.y_lim[0], self.y_lim[1], 60)
        # Creating a meshgrig with the two linspaces above
        X, Y = np.meshgrid(X, Y)
        fun = function_prot(0.001, self.func)
        # Creating Z using the given function
        Z = fun.f(X, Y)
        # Initializing the plot using a for loop and giving them titles
        check.plot_wireframe(X, Y, Z, rstride=3, cstride=3)
        check.set_xlabel("X-axis")
        check.set_ylabel("Y-axis")
        check.set_zlabel("Z-axis")
        plt.show()
        print("plotted " + self.func)
        plt.show()


if __name__ == "__main__":
    # Run an example simulation to test different
    s = Simulation(0.01, "np.sin(x)+np.cos(y)", 0.3, 1, 1, 1, 10, [0, 10], [0, 10], True, 1, 1)
    s.simulate()

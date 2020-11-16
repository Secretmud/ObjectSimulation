import matplotlib.pyplot as plt
from matplotlib import cm, rc
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csv


def plot_axes_3d(fname1, fname2, i):
    t = 0
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    X = np.linspace(1, 8, 60)
    Y = np.linspace(1.9, 4.5, 60)
    X, Y = np.meshgrid(X, Y)

    Z = np.sin(X) + np.cos(Y)

    xh = []
    yh = []
    zh = []
    xe = []
    ye = []
    ze = []
    ax.plot_surface(X, Y, Z, zorder=0, alpha=0.5)
    with open(fname1) as f:
        reader = csv.DictReader(f, delimiter=',')
        next(reader)
        for row in reader:
            xe.append(float(row['x']))
            ye.append(float(row['y']))
            ze.append(float(row['z']))

    with open(fname2) as f:
        reader = csv.DictReader(f, delimiter=',')
        next(reader)
        for row in reader:
            xh.append(float(row['x']))
            yh.append(float(row['y']))
            zh.append(float(row['z']))

    ax.annotate("last Euler", (xe[-1], ye[-1]))
    ax.annotate("last Heuns", (xe[-1], ye[-1]))
    ax.set_xlabel("X-axis", fontsize=18)
    ax.set_ylabel("Y-axis", fontsize=18)
    ax.set_zlabel("Z-axis", fontsize=18)
    ax.scatter(xe, ye, ze, color="black", zorder=1)
    ax.scatter(xh, yh, zh, color="orange", zorder=1)
    plt.show()


def plot_axes_2d(fname):
    time = 0
    fig = plt.figure()
    ax = fig.add_subplot(111)

    v = []
    a = []
    t = []
    with open(fname) as f:
        reader = csv.DictReader(f, delimiter=',')
        next(reader)
        for row in reader:
            v.append(np.sqrt(np.power(float(row['vx']), 2) +
                             np.power(float(row['vy']), 2)))
            a.append(np.sqrt(np.power(float(row['ax']), 2) +
                             np.power(float(row['ay']), 2)))
            t.append(time)
            time += 0.06

    ax.plot(t, v, color="black")
    ax.plot(t, a, color="black")
    ax.set_xlabel("Time", fontsize=18)
    ax.set_ylabel("Velocity vector", fontsize=18)
    ax.set_xscale("log")
    plt.show()


plot_axes_3d("data/data_euler.csv", "data/data_heuns.csv", 1)
#plot_axes_2d("data/data_heuns.csv")

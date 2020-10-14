"""
    File name: simulation.py
    Author: Tor Kristian
    Date created: 07/09/2020
    Date last modified: 28/09/2020
    Python Version: 3.8
"""
import csv
from time import time

import matplotlib.pyplot as plt

from lib.Algorithms import *
from lib.function_prot import *

print("Simulating a object sliding down a function")


def write_file(x_cord, y_cord, dt_end, type_write):
    with open("data/data_" + str(dt_end) + ".csv", type_write, newline="") as f:
        fieldnames = ['x', 'y', 'dt']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'x': x_cord, 'y': y_cord, 'dt': dt_end})
        f.close()


dt = 0.1
# Doing some assignments for matplotlib, fig, ax[2] 
fig = plt.figure()
ax = fig.add_subplot(111)
func = "np.sin(x)+np.cos(y)"
mu = 0.1
USER_PC = 1
v_ix = 1
v_iy = 1
N = 3
x_lim = [1, 10]
y_lim = [1, 10]
x = x_lim[0] + 1
y = y_lim[0] + 1
plot = False
# Initializing Forward Euler and Heuns with the values they need.
e = Algo(N, mu, ax, v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC, plot, x, y)
h = Algo(N, mu, ax, v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC, plot, x, y)
# Initializing the plot using a for loop and giving them titles
# Setting a initial value for t and running the while loop forever and plotting every 0.05 seconds
steps = 5
tend = 0.5
time_t = time()
print("calculating perfect val")
for i in range(25):
    dt /= 2
print(dt)
h.set_dt(dt)
try:
    with open("data/data_" + str(dt) + ".csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader)
        result = []
        for row in reader:
            for col in row:
                result.append(col)
        x_end = float(result[0])
        y_end = float(result[1])
        dt = float(result[2])

        csvfile.close()
except IOError:
    print(f"end {steps / dt}")
    t = 0
    while t < tend / dt:
        (x_end, y_end) = h.heuns(t)
        t += 1

    write_file(x_end, y_end, dt)
    print(f"value calculated in {time() - time_t}")
print(f"x {x_end} y {y_end} dt {dt}")

dt = 0.1
end = tend / dt
t = 0
fh = [1] * steps
fe = [1] * steps
dts = [1] * steps
for i in range(0, steps):
    e.re_init(dt, v_ix, v_iy, x, y)
    h.re_init(dt, v_ix, v_iy, x, y)
    while t < end - 1:
        e.euler(t)
        h.heuns(t)
        t += 1
    (xe, ye) = e.euler(t)
    (xh, yh) = h.heuns(t)
    fe[i] = np.sqrt(np.power(x_end - xe, 2) + np.power(y_end - ye, 2))
    fh[i] = np.sqrt(np.power(x_end - xh, 2) + np.power(y_end - yh, 2))
    print(f"FH: {fh[i]}\tFE: {fe[i]} ")
    dts[i] = dt
    dt /= 2
    i += 1
    t = 0
    end = tend / dt

print(f"Simulation is finished. It took {time() - time_t}")
ax.loglog(dts, np.abs(fe), 'bo-', marker="*", linewidth=1, label="Euler")
ax.loglog(dts, np.abs(fh), 'go-', marker="*", linewidth=1, label="Heun's")
ax.set_xlabel("dt")
ax.set_ylabel("Error")
ax.legend()
plt.show()

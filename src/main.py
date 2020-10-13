"""
    File name: simulation.py
    Author: Tor Kristian
    Date created: 07/09/2020
    Date last modified: 28/09/2020
    Python Version: 3.8
"""
from math import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from lib.Algorithms import *
from lib.function_prot import *
from time import time
import csv
from multiprocessing import Process
print("Simulating a object sliding down a function")
def writeFile(xend, yend, dt):
    with open("data_" + str(dt) + ".csv", "w", newline="") as f:
        fieldnames = ['x', 'y', 'dt']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'x': xend, 'y': yend, 'dt': dt})
        f.close()
dt = 0.1
# Doing some assignments for matplotlib, fig, ax[2] 
fig = plt.figure()
ax = [0]*3
ax[0] = fig.add_subplot(121, projection='3d')
ax[1] = fig.add_subplot(122, projection='3d')
ax[2] = fig.add_subplot(111)
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
e = Algo(N, mu, ax[0], v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC, plot, x, y)
h = Algo(N, mu, ax[1], v_ix, v_iy, func, dt, x_lim, y_lim, USER_PC, plot, x, y)
# Initializing the plot using a for loop and giving them titles
# Setting a initial value for t and running the while loop forever and plotting every 0.05 seconds
steps = 5
time_t = time()
print("calculating perfect val")
for i in range(13):
    dt /= 2
print(dt)
h.setdt(dt)
try:
    with open("data_" + str(dt) + ".csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader)
        result = []
        for row in reader:
            for col in row:
                result.append(col)
        xend = float(result[0])
        yend = float(result[1])
        dt = float(result[2])
            
        csvfile.close()
except IOError:
    print(f"end {steps/dt}")
    while t < steps/dt:
        (xend, yend) = h.heuns(t)
        t += 1

    writeFile(xend, yend, dt)
    print(f"value calcualted in {time() - time_t}")
print(f"x {xend} y {yend} dt {dt}")

dt = 0.1
h.setdt(dt)
end = steps/dt
t = 0
end = steps/dt
fh = [1] * steps
fe = [1] * steps
dts = [1] * steps
for i in range(0, steps):
    while t < end:
        (xe, ye) = e.euler(t)
        fe[i] = np.sqrt(np.power(xend-xe, 2) + np.power(yend-ye,2))
        t+=1
        (xh, yh) = h.heuns(t)
        fh[i] = np.sqrt(np.power(xend-xh, 2) + np.power(yend-yh,2))
        t+=1
    print(f"FH: {fh[i]} FE: {fe[i]}")
    dts[i] = dt
    dt /= 2
    i += 1
    h.setdt(dt)
    e.setdt(dt)
    t = 0
    end = steps/dt


print(f"Simulation is finished. It took {time() - time_t}")
ax[2].plot(dts,np.log(fe) + np.log(dts), 'bo-',  marker="*", linewidth=1, label="Euler")
ax[2].plot(dts,np.log(fh) + 2*np.log(dts), 'go-', marker="*", linewidth=1, label="Heun's")
ax[2].set_xlabel("dt")
ax[2].set_ylabel("Error")
plt.show()


  
    

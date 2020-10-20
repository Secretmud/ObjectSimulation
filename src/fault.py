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
from simulation import *

print("Simulating a object sliding down a function")


def write_file(x_cord, y_cord, dt_end, type_write):
    with open("data/data_" + str(dt_end) + ".csv", type_write, newline="") as f:
        fieldnames = ['x', 'y', 'dt']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'x': x_cord, 'y': y_cord, 'dt': dt_end})
        f.close()


def read_file(delta):
    with open("data/data_2.9802322387695314e-09.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader)
        result = []
        for row in reader:
            for col in row:
                result.append(col)
        x_last = float(result[0])
        y_last = float(result[1])
        delta = float(result[2])

        csvfile.close()

    return x_last, y_last, delta


def create_file(time_end):
    iterations = 0
    while iterations < time_end / dt:
        (x_last, y_last) = s.h.heuns(iterations)
        iterations += 1

    write_file(x_last, y_last, dt)
    print(f"value calculated in {time() - time_total}")

    return x_last, y_last, dt


def low_dt(initial_dt, x):
    for i in range(x):
        initial_dt /= 2

    return initial_dt


if __name__ == "__main__":
    s = Simulation(0.1, "np.sin(x)+np.cos(y)", 0.1, 1, 1, 1, 3, [1, 10], [1, 10], False, 2, 2)
    dt = low_dt(0.1, 15)
    try:
        x_end, y_end, dt = read_file(dt)
    except IOError:
        x_end, y_end, dt = create_file(0.5)
    s.plot_fault(0.1, 10, 0.5, x_end, y_end)
    time_total = time()
    print(f"Simulation is finished. It took {time() - time_total}")

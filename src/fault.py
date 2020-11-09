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


class fault:

    def __init__(self, dt, halves, time_end, s):
        self.edt = self.low_dt(dt, halves)
        self.time_end = time_end
        self.halves = halves
        self.s = s

    def write_file(self, x_cord, y_cord, dt_end, type_write):
        with open("data/data_" + str(dt_end) + ".csv", type_write, newline="") as f:
            fieldnames = ['x', 'y', 'dt']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'x': x_cord, 'y': y_cord, 'dt': dt_end})
            f.close()

    def read_file(self):
        with open("data/data_" + str(self.edt) + ".csv", newline="") as csvfile:
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

    def create_file(self):
        iterations = 0
        a = Algo(3, 0.1, [], 1, 1, "np.sin(x)+np.cos(y)", self.edt, [1, 10], [1, 10], 1, False, 2, 2)
        self.s.dt = self.edt
        while iterations < (self.time_end / self.edt) - 1:
            a.heuns(iterations)
            iterations += 1
        (x_last, y_last) = a.heuns(iterations)
        self.write_file(x_last, y_last, self.edt, 'w')
        print(f"value calculated in {time() - time_total}")

        return x_last, y_last, self.edt

    def low_dt(self, initial_dt, x):
        for i in range(x):
            initial_dt /= 2

        return initial_dt


if __name__ == "__main__":
    time_total = time()
    s = Simulation(dt=0.1, func="np.sin(x)+np.cos(y)", mu=0.1, update_time=1,
                   v_ix=1, v_iy=1, n=3, x_lim=[1, 10], y_lim=[1, 10], plot=False, x=2, y=2)
    f = fault(dt=0.1, halves=24, time_end=0.5, s=s)
    try:
        x_end, y_end, dt = f.read_file()
    except IOError:
        x_end, y_end, dt = f.create_file()

    print(x_end, y_end, dt)
    s.plot_fault(0.1, 4, 0.5, x_end, y_end)
    print(f"Simulation is finished. It took {time() - time_total}")

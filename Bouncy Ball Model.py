import matplotlib
matplotlib.use("TkAgg")

import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def bouncyball(mass, restitution, height, gravity):
    g = gravity# strength of gravity
    h = height #maximum drop height
    c = restitution #coeffiecitn of resitution
    m = mass #ball mass/kg
    t_bounce = 0.02 #bounce time/s
    N = 20 # number of bounces
    dt = 0.001 #timestep /s

    #total time to stop bouncing
    Tinf = 2*math.sqrt(2*h/g)*((1/(1-c))-0.5)

    #total distance travelled /m
    D = 2*h*(1/(1-c**2)-0.5)

    x = h #initial displacement
    v = 0 # velocity(downwards)
    t = 0 #time

    tb, f = [], [] #initialise bounce times and bounce force
    bounce = 0

    ts, xs = [],[]

    #increment time by dt, and see if a bounce happens
    while bounce <= N:
        ts.append(t)
        xs.append(x)

        v2 = v + g*dt #constant acceleration motion, v is downwards
        x2 = x - v*dt - 0.5*g*(dt**2) # x measure upwards from surface
        t2 = t + dt #increment time

        if x2 < 0 < v2: # bounce criteria
            bounce += 1
            tb += [t2-0.5*t_bounce, t2, t2+0.5*t_bounce] #bounce time
            f += [0, 2*(1+c)*m*v2/t_bounce, 0] # max bounce force
            v2 = -c*v2
        x, v, t = x2, v2, t2

    fig, ax = plt.subplots()
    ax.set_xlim(0, ts[-1])
    ax.set_ylim(min(xs), max(xs))
    ax.set_xlabel("time (s)")
    ax.set_ylabel("height (m)")
    ax.set_title("Bouncy Ball Animation")

    point, = ax.plot([], [], 'ro', markersize=8)
    trail, = ax.plot([], [], 'b-', linewidth=1)

    def update(frame):
        point.set_data([ts[frame]], [xs[frame]])
        trail.set_data(ts[:frame+1], xs[:frame+1])
        return point, trail

    ani = FuncAnimation(fig, update, frames=len(ts), interval=1, blit=True)
    plt.show()

import tkinter as tk

root = tk.Tk()
root.title("Bouncy Ball Animation")

mass_var = tk.DoubleVar(value=0.5)
rest_var = tk.DoubleVar(value=0.71)
height_var = tk.DoubleVar(value=0.281)
gravity_var = tk.DoubleVar(value=9.81)

tk.Label(root, text="mass (kg)").pack()
tk.Scale(root, from_=0.1, to=5, resolution= 0.1, orient="horizontal", variable=mass_var).pack()

tk.Label(root, text="Restitution (0–1)").pack()
tk.Scale(root, from_=0.0, to=1.0, resolution=0.01, orient="horizontal", variable=rest_var).pack()

tk.Label(root, text="Drop Height (m)").pack()
tk.Scale(root, from_=0.05, to=2.0, resolution=0.01, orient="horizontal", variable=height_var).pack()

tk.Label(root, text="Gravity (m/s²)").pack()
tk.Scale(root, from_=1, to=20, resolution=0.1, orient="horizontal", variable=gravity_var).pack()

def run_sim():
    bouncyball(
        mass_var.get(),
        rest_var.get(),
        height_var.get(),
        gravity_var.get()
    )

tk.Button(root, text="Run Simulation", command=run_sim).pack(pady=10)

root.mainloop()
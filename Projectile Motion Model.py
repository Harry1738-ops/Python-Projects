import matplotlib
matplotlib.use("TkAgg")

import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def projectilemotion(speed, angle_deg, gravity, height, mass, air_resistance):
    #convert angle into radians
    theta = math.radians(angle_deg)
    k = 1

    #initial velocity components
    vx = speed * math.cos(theta)
    vy = speed * math.sin(theta)

    #initial position
    x = 0
    y = height

    dt = 0.01
    xs, ys = [], []

    while y >= 0:
        xs.append(x)
        ys.append(y)

        if air_resistance:
            ax = -(k / mass) * vx
            ay = -gravity - (k / mass) * vy
        else:
            ax = 0
            ay = -gravity

        vx = vx + ax * dt
        vy = vy +ay * dt

        x = x + vx * dt
        y = y + vy * dt

    fig, ax = plt.subplots()
    ax.set_xlim(0, max(xs))
    ax.set_ylim(0, max(ys) * 1.1)
    ax.set_xlabel(" x (m)")
    ax.set_ylabel(" y (m)")
    ax.set_title("Projectile Motion Model")

    point, = ax.plot([], [], 'ro', ms=8)
    trail, = ax.plot([], [], 'bo', lw=1)

    def update(frame):
        point.set_data([xs[frame]], [ys[frame]])
        trail.set_data(xs[:frame+1], ys[:frame+1])
        return point, trail

    ani = FuncAnimation(fig, update, frames=len(xs), interval=1, blit=True)
    plt.show()

import tkinter as tk

root = tk.Tk()
root.title("Projectile Motion Model")

speed_var = tk.DoubleVar(value=10)
angle_deg_var = tk.DoubleVar(value=45)
gravity_var = tk.DoubleVar(value=9.81)
height_var = tk.DoubleVar(value=0)
mass_var = tk.DoubleVar(value=0.5)

air_resistance_var = tk.BooleanVar(value=False)

tk.Label(root, text="Speed (m/s)").pack()
tk.Scale(root, from_=0.1, to=20, resolution=0.1, orient="horizontal", variable=speed_var).pack()

tk.Label(root, text="Angle").pack()
tk.Scale(root, from_=0, to=89, resolution=1, orient="horizontal", variable=angle_deg_var).pack()

tk.Label(root, text="Gravity").pack()
tk.Scale(root, from_=1, to=20, resolution=0.1, orient="horizontal", variable=gravity_var).pack()

tk.Label(root, text="Height").pack()
tk.Scale(root, from_=0, to=100, resolution=1, orient="horizontal", variable=height_var).pack()

tk.Label(root, text="Mass").pack()
tk.Scale(root, from_=0.1, to=5, resolution=0.1, orient="horizontal", variable=mass_var).pack()

tk.Checkbutton(root, text="Air Resistance", variable=air_resistance_var).pack()

def run_sim():
    projectilemotion(
        speed_var.get(),
        angle_deg_var.get(),
        gravity_var.get(),
        height_var.get(),
        mass_var.get(),
        air_resistance_var.get()
    )

tk.Button(root, text="Run Simulation", command=run_sim).pack(pady=10)

root.mainloop()



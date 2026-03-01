import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def Snell_law(theta_incident, n1, n2):

    ax.clear()

    x = [0,2,2,0,0]
    y = [0,0,2,2,0]

    ax.fill(x, y, color="#f0f0f0", zorder=0)

    ax.plot(x, y, 'k-', label="Boundary")
    ax.set_aspect("equal")

    ax.set_xlim(-1, 2)
    ax.set_ylim(0, 2.5)

    critical_angle = None
    if n1 > n2:
        critical_angle = np.degrees(np.arcsin(n2 / n1))

    sin_value = (n1 / n2) * np.sin(np.radians(theta_incident))
    theta_2 = None

    if abs(sin_value) <= 1:
        theta_2 = -np.degrees(np.arcsin(sin_value))

    theta_plot = -theta_incident

    dx = -np.cos(np.radians(theta_plot))
    dy = -np.sin(np.radians(theta_plot))

    x1, y1 = 0, 1
    x2 = x1 + dx * 0.8
    y2 = y1 + dy * 0.8

    ax.plot([x1, x2], [y1, y2], 'k-', label="Incident ray")

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    arrow_length = 0.2
    length = np.sqrt(dx**2 + dy**2)
    ux = dx / length
    uy = dy / length

    ax.annotate(
        "",
        xy=(mx - ux * arrow_length/2, my - uy * arrow_length/2),
        xytext=(mx + ux * arrow_length/2, my + uy * arrow_length/2),
        arrowprops=dict(arrowstyle="->", color="black", mutation_scale=20)
    )

    ax.plot([-0.5, 0.5], [1, 1], '--', color='red', label="Normal")

    angle_radius = 0.3
    angles = np.linspace(0, -theta_incident, 100)

    x_arc = -angle_radius * np.cos(np.radians(angles))
    y_arc = 1 - angle_radius * np.sin(np.radians(angles))

    ax.plot(x_arc, y_arc, linestyle="dotted", color="black", linewidth=2)

    if theta_2 is not None:

        dx_r = np.cos(np.radians(theta_2))
        dy_r = np.sin(np.radians(theta_2))

        x2 = x1 + dx_r * 1
        y2 = y1 + dy_r * 1

        ax.plot([x1, x2], [y1, y2], color="blue", label="Refraction")

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        length = np.sqrt(dx_r**2 + dy_r**2)
        ux = dx_r / length
        uy = dy_r / length

        ax.annotate(
            "",
            xy=(mx + ux * arrow_length/2, my + uy * arrow_length/2),
            xytext=(mx - ux * arrow_length/2, my - uy * arrow_length/2),
            arrowprops=dict(arrowstyle="->", color="blue", mutation_scale=20)
        )

        angles = np.linspace(0, theta_2, 100)

        x_arc2 = angle_radius * np.cos(np.radians(angles))
        y_arc2 = 1 + angle_radius * np.sin(np.radians(angles))

        ax.plot(x_arc2, y_arc2, linestyle="dotted", color="blue", linewidth=2)

    else:

        incident_vector = np.array([dx, dy])
        normal_vector = np.array([0, 1])

        reflected_vector = incident_vector - 2 * np.dot(incident_vector, normal_vector) * normal_vector

        dx_r, dy_r = reflected_vector

        x2 = x1 + dx_r * 1
        y2 = y1 + dy_r * 1

        ax.plot([x1, x2], [y1, y2], color="orange", label="Reflection (TIR)")

        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        length = np.sqrt(dx_r**2 + dy_r**2)
        ux = dx_r / length
        uy = dy_r / length

        ax.annotate(
            "",
            xy=(mx + ux * arrow_length/2, my + uy * arrow_length/2),
            xytext=(mx - ux * arrow_length/2, my - uy * arrow_length/2),
            arrowprops=dict(arrowstyle="->", color="orange", mutation_scale=20)
        )

        angles = np.linspace(0, theta_incident, 100)

        x_arc_tir = -angle_radius * np.cos(np.radians(angles))
        y_arc_tir = 1 - angle_radius * np.sin(np.radians(angles))

        ax.plot(x_arc_tir, y_arc_tir, linestyle="dotted", color="orange", linewidth=2)

    ax.text(-0.5, 1.8, f"θ₁ = {theta_incident:.2f}°", fontsize=14)

    if theta_2 is not None:
        ax.text(0.7, 1.8, f"θ₂ = {-theta_2:.2f}°", fontsize=14, color="blue")
    else:
        ax.text(0.7, 1.8, "Total Internal Reflection", fontsize=12, color="orange")
        ax.text(0.7, 1.65, f"Angle of Reflection = {theta_incident:.2f}°",
                fontsize=12, color="orange")

    ax.text(-0.5, 1.9, f"n₁ = {n1:.2f}", fontsize=14)
    ax.text(0.7, 1.9, f"n₂ = {n2:.2f}", fontsize=14)

    if critical_angle is not None:
        ax.text(-0.5, 2.05,
                f"Critical Angle = {critical_angle:.2f}°",
                fontsize=12,
                color="orange")

    ax.legend(loc="upper right")
    for spine in ax.spines.values():
        spine.set_color("white")
    ax.tick_params(colors='white')
    fig.suptitle("Snell's Law Model", fontsize=20, y=0.835)

    canvas.draw()

root = tk.Tk()

root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, sticky="ns", padx=5)
tk.Label(left_frame, text="").pack(pady=200)

right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, sticky="nsew")

fig, ax = plt.subplots(figsize=(5,5))
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

theta_1_var = tk.DoubleVar(value=30)
n1_var = tk.DoubleVar(value=1.00)
n2_var = tk.DoubleVar(value=1.33)

def update(*args):
    try:
        Snell_law(theta_1_var.get(), n1_var.get(), n2_var.get())
    except:
        pass

theta_1_var.trace_add("write", update)
n1_var.trace_add("write", update)
n2_var.trace_add("write", update)

tk.Label(left_frame, text="Refractive Index (Outside)").pack()
tk.Entry(left_frame, textvariable=n1_var).pack()

tk.Label(left_frame, text="Refractive Index (Inside)").pack()
tk.Entry(left_frame, textvariable=n2_var).pack()

tk.Label(left_frame, text="Angle of Incident (degrees)").pack()
tk.Scale(left_frame, from_=0, to=90,
         orient="horizontal",
         variable=theta_1_var).pack()

update()
root.mainloop()
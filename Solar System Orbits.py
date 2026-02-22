from math import pi
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
matplotlib.use('TkAgg')
import tkinter as tk

def solar_orbits():
    root = tk.Tk()
    root.title("Solar System Simulation")

    # Main layout frames
    left_panel = tk.Frame(root, bg="black")
    left_panel.pack(side="left", fill="y")

    right_panel = tk.Frame(root)
    right_panel.pack(side="right", fill="both", expand=True)

    r = {
        "Mercury" : 0.39,
        "Venus" : 0.72,
        "Earth" : 1,
        "Mars" : 1.523,  # orbital radius in AU
        "Jupiter" : 5.2,
        "Saturn" : 9.54,
        "Uranus" : 19.2,
        "Neptune" : 30.06
    }
    moon_scale = 25
    r_moon = 0.00257 * moon_scale

    saturn_ring_inner = 0.25
    saturn_ring_outer = 0.45

    planet_sizes = {
        "Mercury": 4,
        "Venus": 7,
        "Earth": 7,
        "Mars": 5,
        "Jupiter": 12,
        "Saturn": 11,
        "Uranus": 9,
        "Neptune": 9
    }

    ecc = {
        "Mercury": 0.205,
        "Venus": 0.007,
        "Earth": 0.017,
        "Mars": 0.093,
        "Jupiter": 0.048,
        "Saturn": 0.056,
        "Uranus": 0.047,
        "Neptune": 0.009
    }

    p = {planet: r[planet]**1.5 for planet in r}
    p["Earth"]= 1

    t = np.linspace(0, 5*p["Mars"], 1500)

    outer_speed = 50 # speed multiplier for outer planets

    theta = {}
    for planet in r:
        e = ecc[planet]
        P = p[planet]
        M0 = 2*pi*random.random()

        speed = 50 if planet in ["Jupiter", "Saturn", "Uranus", "Neptune"] else 1

        M = M0 + 2*pi*t/P * speed

        E = M.copy()
        for _ in range(5):
            E = E - (E - e*np.sin(E) -M) /  (1-e * np.cos(E))

        nu = 2*np.arctan2(
            np.sqrt(1+e) * np.sin(E/2),
            np.sqrt(1-e) * np.cos(E/2)
        )

        theta[planet] = nu

    theta_moon = 2*pi*t/0.0748

    theta_ring = np.linspace(0,2*pi, 300)

    x = {}
    y = {}

    for planet in r:
       a = r[planet]
       e = ecc[planet]
       th = theta[planet]

       rad = (a * (1- e**2)) / (1 + e * np.cos(th))

       x[planet] = rad * np.cos(th)
       y[planet] = rad * np.sin(th)

    x_moon = x["Earth"] +r_moon *np.cos(theta_moon)
    y_moon = y["Earth"] +r_moon *np.sin(theta_moon)

    colours = {
        "Mercury": "gray",
        "Venus": "#EEDC82",
        "Earth": "blue",
        "Mars": "red",
        "Jupiter": "tan",
        "Saturn": "#F5DEB3",
        "Uranus": "#AFEEEE",
        "Neptune": "#4169E1"
    }

    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    fig, (ax_inner, ax_outer) = plt.subplots(1, 2, figsize=(12, 6))

    canvas = FigureCanvasTkAgg(fig, master=right_panel)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    camera_mode = tk.StringVar(value="static")

    def set_camera(mode):
        camera_mode.set(mode)

    btn_static = tk.Button(left_panel, text="Static", width=15,
                           command=lambda: set_camera("static"))
    btn_earth = tk.Button(left_panel, text="Follow Earth", width=15,
                          command=lambda: set_camera("Earth"))
    btn_moon = tk.Button(left_panel, text="Follow Moon", width=15,
                         command=lambda: set_camera("Moon"))
    btn_jupiter = tk.Button(left_panel, text="Follow Jupiter", width=15,
                            command=lambda: set_camera("Jupiter"))

    btn_static.pack(pady=10)
    btn_earth.pack(pady=10)
    btn_moon.pack(pady=10)
    btn_jupiter.pack(pady=10)

    fig.patch.set_facecolor("black")
    ax_inner.set_facecolor("black")
    ax_outer.set_facecolor("black")

    for ax in (ax_inner, ax_outer):
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")
        for spine in ax.spines.values():
            spine.set_color("white")

    mw_x = np.linspace(-1, 1, 800)
    mw_y = np.linspace(-1, 1, 800)
    xx, yy = np.meshgrid(mw_x, mw_y)

    milky_way = np.exp(-((yy - 0.2 * xx) ** 2) / 0.02)

    milky_way = milky_way * 0.2

    ax_outer.imshow(
        milky_way,
        extent=[-40, 40, -40, 40],
        cmap="gray",
        alpha=0.15,
        origin="lower",
        zorder=-1
    )

    sun_res = 1500
    gx = np.linspace(-1, 1, sun_res)
    gy = np.linspace(-1, 1, sun_res)
    gxx, gyy = np.meshgrid(gx, gy)
    sun_gauss = np.exp(-(gxx ** 2 + gyy ** 2) / 0.18)

    sun_res = 1000
    gx = np.linspace(-1, 1, sun_res)
    gy = np.linspace(-1, 1, sun_res)
    gxx, gyy = np.meshgrid(gx, gy)

    r2 = gxx ** 2 + gyy ** 2
    sun_gauss = np.exp(-r2 / 0.08)

    sun_rgba = np.zeros((sun_res, sun_res, 4))

    sun_rgba[..., 0] = 1.0
    sun_rgba[..., 1] = 0.6
    sun_rgba[..., 2] = 0.1

    sun_rgba[..., 3] = sun_gauss

    sun_rgba[r2 > 1.0, 3] = 0

    ax_inner.imshow(
        sun_rgba,
        extent=[-0.6, 0.6, -0.6, 0.6],
        origin="lower",
        zorder=0
    )

    ax_outer.imshow(
        sun_rgba,
        extent=[-6, 6, -6, 6],
        origin="lower",
        zorder=0
    )

    num_stars_inner = 150
    star_x_inner = np.random.uniform(-2, 2, num_stars_inner)
    star_y_inner = np.random.uniform(-2, 2, num_stars_inner)

    star_alpha_base_inner = np.random.uniform(0.2, 0.8, num_stars_inner)
    star_twinkle_speed_inner = np.random.uniform(0.5, 2.0, num_stars_inner)

    stars_inner = ax_inner.scatter(star_x_inner, star_y_inner, s=2, color="white", alpha=star_alpha_base_inner)

    num_stars = 300
    star_x = np.random.uniform(-40, 40, num_stars)
    star_y = np.random.uniform(-40, 40, num_stars)

    star_alpha_base = np.random.uniform(0.2, 0.8, num_stars)

    star_twinkle_speed = np.random.uniform(0.5, 2.0, num_stars)

    stars_outer = ax_outer.scatter(star_x, star_y, s=2, color="white", alpha=star_alpha_base)

    inner_planets = ["Mercury", "Venus", "Earth", "Mars"]

    inner_orbit_lines = {}
    for planet in inner_planets:
        line, = ax_inner.plot(x[planet], y[planet], color=colours[planet], alpha=0.1)
        inner_orbit_lines[planet] = line

    moon_dot = ax_inner.plot([], [], 'o', color='cyan', ms=4, label="Moon")[0]
    moon_trail = ax_inner.plot([], [], color='cyan', lw=1)[0]
    moon_trail_x = []
    moon_trail_y = []

    ax_inner.set_title("Inner Planets (Mercury-Mars)")
    ax_inner.set_xlabel("x/AU")
    ax_inner.set_ylabel("y/AU")
    ax_inner.set_xlim(-1.8,1.8)
    ax_inner.set_ylim(-1.8,1.8)
    ax_inner.legend()

    inner_dots = {
        planet: ax_inner.plot([],[],'o', color=colours[planet], ms=planet_sizes[planet])[0]
        for planet in inner_planets
    }

    inner_trails = {}
    for planet in inner_planets:
        lc = LineCollection([], lw=1)
        lc.set_color(colours[planet])
        ax_inner.add_collection(lc)
        inner_trails[planet] = lc

    outer_planets = ["Jupiter", "Saturn", "Uranus", "Neptune"]

    outer_orbit_lines = {}
    for planet in outer_planets:
        line, = ax_outer.plot(x[planet], y[planet], color=colours[planet], alpha=0.1, label=planet)
        outer_orbit_lines[planet] = line

    ax_outer.set_title("Outer Planets (Jupiter-Neptune) "
                       "50x Speed")
    ax_outer.set_xlabel("x/AU")
    ax_outer.set_ylabel("y/AU")
    ax_outer.set_xlim(-35, 35)
    ax_outer.set_ylim(-35, 35)

    inner_default_xlim = (-1.8, 1.8)
    inner_default_ylim = (-1.8, 1.8)

    outer_default_xlim = (-35, 35)
    outer_default_ylim = (-35, 35)

    saturn_ring_inner_line = ax_outer.plot([], [], color='gray', alpha=0.5, lw=1)[0]
    saturn_ring_outer_line = ax_outer.plot([], [], color='gray', alpha=0.5, lw=1)[0]

    leg_inner = ax_inner.legend(frameon=False, handlelength=1.5)
    for text in leg_inner.get_texts():
        text.set_color("white")
    for lh in leg_inner.legend_handles:
        lh.set_alpha(1)

    leg_outer = ax_outer.legend(loc="upper right", frameon=False, handlelength=1.5)
    for text in leg_outer.get_texts():
        text.set_color("white")
    for lh in leg_outer.legend_handles:
        lh.set_alpha(1)

    outer_dots = {
        planet: ax_outer.plot([],[],'o-', color=colours[planet], ms=planet_sizes[planet])[0]
        for planet in outer_planets
    }

    outer_trails = {}
    for planet in outer_planets:
        lc = LineCollection([], lw=1)
        lc.set_color(colours[planet])
        ax_outer.add_collection(lc)
        outer_trails[planet] = lc

    trail_length = 200

    inner_trail_x = {planet: [] for planet in inner_planets}
    inner_trail_y = {planet: [] for planet in inner_planets}

    outer_trail_x = {planet: [] for planet in outer_planets}
    outer_trail_y = {planet: [] for planet in outer_planets}

    def apply_camera(ax, mode, frame, is_inner):
        if mode == "static":
            if is_inner:
                ax.set_xlim(*inner_default_xlim)
                ax.set_ylim(*inner_default_ylim)
            else:
                ax.set_xlim(*outer_default_xlim)
                ax.set_ylim(*outer_default_ylim)
            return

        if is_inner:
            if mode == "Earth":
                cx = x["Earth"][frame]
                cy = y["Earth"][frame]
                ax.set_xlim(cx - 1.8, cx + 1.8)
                ax.set_ylim(cy - 1.8, cy + 1.8)

            elif mode == "Moon":
                cx = x_moon[frame]
                cy = y_moon[frame]
                ax.set_xlim(cx - 1.8, cx + 1.8)
                ax.set_ylim(cy - 1.8, cy + 1.8)

            else:
                ax.set_xlim(*inner_default_xlim)
                ax.set_ylim(*inner_default_ylim)

        else:
            if mode == "Jupiter":
                cx = x["Jupiter"][frame]
                cy = y["Jupiter"][frame]
                ax.set_xlim(cx - 10, cx + 10)
                ax.set_ylim(cy - 10, cy + 10)
            else:
                ax.set_xlim(*outer_default_xlim)
                ax.set_ylim(*outer_default_ylim)

    def update(frame):

        new_alpha = star_alpha_base + 0.15 * np.sin(frame * 0.05 * star_twinkle_speed)
        new_alpha = np.clip(new_alpha, 0.05, 1.0)
        stars_outer.set_alpha(new_alpha)

        new_alpha_inner = star_alpha_base_inner + 0.15 * np.sin(frame * 0.05 * star_twinkle_speed_inner)
        new_alpha_inner = np.clip(new_alpha_inner, 0.05, 1.0)
        stars_inner.set_alpha(new_alpha_inner)

        apply_camera(ax_inner, camera_mode.get(), frame, is_inner=True)
        apply_camera(ax_outer, camera_mode.get(), frame, is_inner=False)

        if camera_mode.get() != "static":
            for planet in inner_planets:
                inner_orbit_lines[planet].set_alpha(0)  # hide
            for planet in outer_planets:
                outer_orbit_lines[planet].set_alpha(0)

        if camera_mode.get() != "static":
            for planet in inner_planets:
                inner_trails[planet].set_segments([])
            for planet in outer_planets:
                outer_trails[planet].set_segments([])

        nonlocal moon_trail_x, moon_trail_y
        for planet in inner_planets:

            inner_dots[planet].set_data([x[planet][frame]], [y[planet][frame]])

            inner_trail_x[planet].append(x[planet][frame])
            inner_trail_y[planet].append(y[planet][frame])

            inner_trail_x[planet] = inner_trail_x[planet][-trail_length:]
            inner_trail_y[planet] = inner_trail_y[planet][-trail_length:]

            pts = np.array([inner_trail_x[planet], inner_trail_y[planet]]).T
            segments = np.array([pts[:-1], pts[1:]]).transpose(1,0,2)

            if len(segments) > 0:
                alphas = np.linspace(0.1, 1.0, len(segments))
                base = matplotlib.colors.to_rgba(colours[planet])
                colors = np.tile(base, (len(segments), 1))
                colors[:, -1] = alphas

                colors[:, -1] = alphas
                inner_trails[planet].set_segments(segments)
                inner_trails[planet].set_color(colors)
            else:
                inner_trails[planet].set_segments([])

            moon_dot.set_data([x_moon[frame]], [y_moon[frame]])

            moon_trail_x.append(x_moon[frame])
            moon_trail_y.append(y_moon[frame])

            moon_trail_x = moon_trail_x[-trail_length:]
            moon_trail_y = moon_trail_y[-trail_length:]

            moon_trail.set_data(moon_trail_x, moon_trail_y)

        for planet in outer_planets:

            if planet == "Saturn":
                sx = x["Saturn"][frame]
                sy = y["Saturn"][frame]

                ring_inner_x = sx + saturn_ring_inner * np.cos(theta_ring)
                ring_inner_y = sy + saturn_ring_inner * np.sin(theta_ring)

                ring_outer_x = sx + saturn_ring_outer * np.cos(theta_ring)
                ring_outer_y = sy + saturn_ring_outer * np.sin(theta_ring)

                saturn_ring_inner_line.set_data(ring_inner_x, ring_inner_y)
                saturn_ring_outer_line.set_data(ring_outer_x, ring_outer_y)

            outer_dots[planet].set_data([x[planet][frame]], [y[planet][frame]])

            outer_trail_x[planet].append(x[planet][frame])
            outer_trail_y[planet].append(y[planet][frame])

            outer_trail_x[planet] = outer_trail_x[planet][-trail_length:]
            outer_trail_y[planet] = outer_trail_y[planet][-trail_length:]

            pts = np.array([outer_trail_x[planet], outer_trail_y[planet]]).T
            segments = np.array([pts[:-1], pts[1:]]).transpose(1, 0, 2)

            if len(segments) > 0:
                alphas = np.linspace(0.1, 1.0, len(segments))
                base = matplotlib.colors.to_rgba(colours[planet])
                colors = np.tile(base, (len(segments), 1))
                colors[:, -1] = alphas

                colors[:, -1] = alphas
                outer_trails[planet].set_segments(segments)
                outer_trails[planet].set_color(colors)
            else:
                outer_trails[planet].set_segments([])

        return (list(inner_dots.values()) +
                list(outer_dots.values()) +
                list(inner_trails.values()) +
                list(outer_trails.values()) +
                [moon_dot, moon_trail,
                 saturn_ring_inner_line, saturn_ring_outer_line,
                 stars_inner, stars_outer
                 ]
                )

    ani = FuncAnimation(fig, update, frames=len(t), interval=30, blit=False)
    root.mainloop()

solar_orbits()
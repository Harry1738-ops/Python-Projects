import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G = 6.67430e-11

masses = {
    "Sun": 1.9885e30,
    "Earth": 5.972e24,
    "Moon": 7.348e22
}

def gravity(pos1, pos2, m2):
    r = pos2 - pos1
    dist = np.linalg.norm(r)
    return G * m2 * r / dist**3

def step(pos, vel, mass, others):
    a= np.zeros(2)
    for (pos_other, mass_other) in others:
        a += gravity(pos, pos_other, mass_other)
    pos_new = pos + vel*dt + 0.5*a*dt**2

    a_new = np.zeros(2)
    for (pos_other, mass_other) in others:
        a_new += gravity(pos_other, pos_new, mass_other)
    vel_new = vel + 0.5*(a + a_new)*dt
    return pos_new, vel_new

AU = 1.496e11
earth_sun_dist = AU
earth_moon_dist = 3.84e8

dt = 2000

v_earth = np.sqrt(G*masses["Sun"] / earth_sun_dist)
v_moon = np.sqrt(G*masses["Earth"] / earth_moon_dist)

pos_sun = np.array([0, 0], dtype=float)
pos_earth =  np.array([earth_sun_dist,0], dtype=float)
pos_moon = pos_earth + np.array([earth_moon_dist,0], dtype=float)
vel_earth = np.array([0, v_earth])
vel_moon = vel_earth + np.array([0, v_moon])

a_earth = gravity(pos_earth, pos_sun, masses["Sun"]) + gravity(pos_earth, pos_moon, masses["Moon"])
a_moon = gravity(pos_moon, pos_earth, masses["Earth"]) + gravity(pos_moon, pos_sun, masses["Sun"])

pos_earth = pos_earth + vel_earth*dt + 0.5*a_earth*dt**2
vel_earth = vel_earth + a_earth*dt

pos_moon = pos_moon + vel_moon*dt + 0.5*a_moon*dt**2
vel_moon = vel_moon + a_moon*dt





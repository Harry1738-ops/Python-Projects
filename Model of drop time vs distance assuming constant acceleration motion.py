import math
import matplotlib.pyplot as plt

_g = 9.8
# in m/s^2
# drop distance is in x (m)
# ignore air resistance

drop_distance = input("What is your desired drop distance: ")
drop_distance = int(drop_distance)

distances = list(range(drop_distance))
times = [math.sqrt((2*x)/_g) for x in distances]

def find_gradient(x1, x2, y1, y2):
    if x2 - x1 == 0:
        return "vertical line"
    else:
        gradient = (y2 - y1) / (x2 - x1)
        return gradient

x1, x2 = 0,1.017
y1, y2 = 0,0.441
slope = find_gradient(x1, x2, y1, y2)
print("gradient slope = ", slope)

plt.scatter(distances, times)
plt.xlabel("Drop distance (m)")
plt.ylabel("Time to fall (s)")
plt.title("Free-fall time vs distance")
plt.grid(True)

plt.show()


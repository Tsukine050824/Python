import numpy as np
import matplotlib.pyplot as plt

radius = 10
num_nodes = 15
steps = 30

positions = np.random.uniform(-radius, radius, num_nodes)

plt.figure()
for t in range(steps):
    plt.clf()
    positions += np.random.uniform(-2, 2, num_nodes)

    for p in positions:
        if abs(p) <= radius:
            plt.scatter(p, 0, color="green")
        else:
            plt.scatter(p, 0, color="red")

    circle = plt.Circle((0, 0), radius, fill=False)
    plt.gca().add_patch(circle)

    plt.xlim(-radius*1.5, radius*1.5)
    plt.ylim(-5, 5)
    plt.title(f"WPAN Node Movement - Step {t}")
    plt.pause(0.3)

plt.show()

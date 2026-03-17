import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# ===============================
# PARAMETERS
# ===============================
NUM_NODES = 20
AREA = 100
RANGE_INFRA = 35
RANGE_ADHOC = 25
RANGE_MESH = 30

PACKET_SPEED = 0.03
TIME_STEPS = 500

np.random.seed(3)

# Initial positions
nodes_inf = np.random.rand(NUM_NODES, 2) * AREA
nodes_adh = nodes_inf.copy()
nodes_mesh = nodes_inf.copy()

vel = (np.random.rand(NUM_NODES, 2) - 0.5) * 2

ap = np.array([AREA/2, AREA/2])
routers = np.array([[20,20],[80,20],[20,80],[80,80]])

# ===============================
# STAT STORAGE
# ===============================
time_history = []
tp_inf_hist, tp_adh_hist, tp_mesh_hist = [], [], []
delay_inf_hist, delay_adh_hist, delay_mesh_hist = [], [], []

# ===============================
# FIGURES
# ===============================
fig_sim, axs = plt.subplots(1,3, figsize=(18,6))
fig_stats, axs_stats = plt.subplots(2,1, figsize=(8,8))

titles = ["Infrastructure","Ad-hoc","Mesh"]

for i in range(3):
    axs[i].set_xlim(0, AREA)
    axs[i].set_ylim(0, AREA)
    axs[i].set_title(titles[i])

sc_inf = axs[0].scatter(nodes_inf[:,0], nodes_inf[:,1])
axs[0].scatter(ap[0], ap[1], marker='^', s=200)

sc_adh = axs[1].scatter(nodes_adh[:,0], nodes_adh[:,1])
sc_mesh = axs[2].scatter(nodes_mesh[:,0], nodes_mesh[:,1])
axs[2].scatter(routers[:,0], routers[:,1], marker='s', s=150)

text_inf = axs[0].text(2,95,"")
text_adh = axs[1].text(2,95,"")
text_mesh = axs[2].text(2,95,"")

lines = [[],[],[]]
packets = []
SIM_TIME = 0

# ===============================
# UPDATE FUNCTION
# ===============================
def update(frame):
    global nodes_inf, nodes_adh, nodes_mesh
    global packets, SIM_TIME

    SIM_TIME += 1
    time_history.append(SIM_TIME)

    for group in lines:
        for l in group:
            l.remove()
        group.clear()

    nodes_inf[:] += vel
    nodes_adh[:] += vel
    nodes_mesh[:] += vel

    nodes_inf[:] = np.clip(nodes_inf,0,AREA)
    nodes_adh[:] = np.clip(nodes_adh,0,AREA)
    nodes_mesh[:] = np.clip(nodes_mesh,0,AREA)

    sc_inf.set_offsets(nodes_inf)
    sc_adh.set_offsets(nodes_adh)
    sc_mesh.set_offsets(nodes_mesh)

    # ================= INFRA =================
    conn_inf = 0
    for node in nodes_inf:
        if np.linalg.norm(node-ap) < RANGE_INFRA:
            line, = axs[0].plot([node[0],ap[0]],[node[1],ap[1]],color="blue")
            lines[0].append(line)
            conn_inf += 1
            if random.random() < 0.05:
                packets.append(["inf", node.copy(), ap.copy(), 0])

    tp_inf = conn_inf * 2
    delay_inf = 1/(conn_inf+1)

    tp_inf_hist.append(tp_inf)
    delay_inf_hist.append(delay_inf)

    text_inf.set_text(f"Links: {conn_inf}\nTP: {tp_inf:.1f}\nDelay: {delay_inf:.2f}")

    # ================= ADHOC =================
    conn_adh = 0
    for i in range(NUM_NODES):
        for j in range(i+1,NUM_NODES):
            if np.linalg.norm(nodes_adh[i]-nodes_adh[j]) < RANGE_ADHOC:
                line, = axs[1].plot([nodes_adh[i][0],nodes_adh[j][0]],
                                    [nodes_adh[i][1],nodes_adh[j][1]],
                                    color="green")
                lines[1].append(line)
                conn_adh += 1
                if random.random() < 0.02:
                    packets.append(["adh", nodes_adh[i].copy(), nodes_adh[j].copy(), 0])

    tp_adh = conn_adh * 1.5
    delay_adh = 2/(conn_adh+1)

    tp_adh_hist.append(tp_adh)
    delay_adh_hist.append(delay_adh)

    text_adh.set_text(f"Links: {conn_adh}\nTP: {tp_adh:.1f}\nDelay: {delay_adh:.2f}")

    # ================= MESH =================
    conn_mesh = 0
    for node in nodes_mesh:
        dists = np.linalg.norm(routers-node,axis=1)
        idx = np.argmin(dists)
        if dists[idx] < RANGE_MESH:
            line, = axs[2].plot([node[0],routers[idx][0]],
                                [node[1],routers[idx][1]],
                                color="red")
            lines[2].append(line)
            conn_mesh += 1
            if random.random() < 0.05:
                packets.append(["mesh", node.copy(), routers[idx].copy(), 0])

    for i in range(len(routers)):
        for j in range(i+1,len(routers)):
            axs[2].plot([routers[i][0],routers[j][0]],
                        [routers[i][1],routers[j][1]],
                        color="orange")

    tp_mesh = conn_mesh * 2.5
    delay_mesh = 1.5/(conn_mesh+1)

    tp_mesh_hist.append(tp_mesh)
    delay_mesh_hist.append(delay_mesh)

    text_mesh.set_text(f"Links: {conn_mesh}\nTP: {tp_mesh:.1f}\nDelay: {delay_mesh:.2f}")

    # ================= PACKETS =================
    for p in packets[:]:
        mode, start, end, progress = p
        progress += PACKET_SPEED
        p[3] = progress
        if progress >= 1:
            packets.remove(p)
            continue
        pos = start + (end-start)*progress
        if mode=="inf":
            axs[0].scatter(pos[0],pos[1],color="black",s=15)
        elif mode=="adh":
            axs[1].scatter(pos[0],pos[1],color="black",s=15)
        else:
            axs[2].scatter(pos[0],pos[1],color="black",s=15)

    # ================= UPDATE STATS PLOTS =================
    axs_stats[0].cla()
    axs_stats[1].cla()

    axs_stats[0].plot(time_history, tp_inf_hist, label="Infra")
    axs_stats[0].plot(time_history, tp_adh_hist, label="Adhoc")
    axs_stats[0].plot(time_history, tp_mesh_hist, label="Mesh")
    axs_stats[0].set_title("Throughput vs Time")
    axs_stats[0].legend()

    axs_stats[1].plot(time_history, delay_inf_hist, label="Infra")
    axs_stats[1].plot(time_history, delay_adh_hist, label="Adhoc")
    axs_stats[1].plot(time_history, delay_mesh_hist, label="Mesh")
    axs_stats[1].set_title("Delay vs Time")
    axs_stats[1].legend()

    return sc_inf, sc_adh, sc_mesh

ani = FuncAnimation(fig_sim, update, frames=TIME_STEPS, interval=100)
plt.show()
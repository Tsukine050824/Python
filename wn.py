import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np
from matplotlib.animation import FuncAnimation

# ==============================
# PARAMETERS
# ==============================

NUM_NODES = 10
SIM_STEPS = 400
PACKET_SIZE = 8000
STEP_TIME_MS = 10

LIGHT_RATE = 0.2
HEAVY_RATE = 0.6

# ==============================
# TOPOLOGY GENERATORS
# ==============================

def create_adhoc():

    nodes = range(1, NUM_NODES+1)
    G = nx.random_geometric_graph(nodes,0.9)
    pos = nx.spring_layout(G,seed=2)

    return G,pos


def create_infrastructure():

    G = nx.Graph()

    G.add_node(1)

    for i in range(2,NUM_NODES+1):
        G.add_edge(1,i)

    pos = {1:(0,0)}

    angle = np.linspace(0,2*np.pi,NUM_NODES)

    idx=2
    for a in angle[1:]:
        pos[idx]=(np.cos(a),np.sin(a))
        idx+=1

    return G,pos


def create_mesh():

    nodes = range(1,NUM_NODES+1)
    G = nx.complete_graph(nodes)

    pos = nx.circular_layout(G)

    return G,pos


# ==============================
# CREATE NETWORKS
# ==============================

G1,pos1 = create_adhoc()
G2,pos2 = create_infrastructure()
G3,pos3 = create_mesh()

G4,pos4 = create_adhoc()
G5,pos5 = create_infrastructure()
G6,pos6 = create_mesh()

graphs=[G1,G2,G3,G4,G5,G6]
positions=[pos1,pos2,pos3,pos4,pos5,pos6]

titles=[
"Adhoc (Light Load)",
"Infrastructure (Light Load)",
"Mesh (Light Load)",
"Adhoc (Heavy Load)",
"Infrastructure (Heavy Load)",
"Mesh (Heavy Load)"
]

colors=["green","royalblue","orange",
        "green","royalblue","orange"]

# ==============================
# METRICS
# ==============================

sent=[0]*6
recv=[0]*6
delay_sum=[0]*6

# ==============================
# PACKET CLASS
# ==============================

class Packet:

    def __init__(self,path,start):

        self.path=path
        self.index=0
        self.progress=0
        self.start=start


packets=[[] for _ in range(6)]

# ==============================
# CREATE PACKET
# ==============================

def create_packet(G,step):

    nodes=list(G.nodes())

    s,d=random.sample(nodes,2)

    try:
        path=nx.shortest_path(G,s,d)
        return Packet(path,step)
    except:
        return None


# ==============================
# MOVE PACKET
# ==============================

def move_packet(packet,pos):

    if packet.index >= len(packet.path)-1:
        return None

    n1=packet.path[packet.index]
    n2=packet.path[packet.index+1]

    x1,y1=pos[n1]
    x2,y2=pos[n2]

    packet.progress+=0.08

    x=x1+(x2-x1)*packet.progress
    y=y1+(y2-y1)*packet.progress

    if packet.progress>=1:

        packet.index+=1
        packet.progress=0

        if packet.index>=len(packet.path)-1:
            return (x2,y2)

    return (x,y)

# ==============================
# FIGURE
# ==============================

fig,axes=plt.subplots(2,3,figsize=(16,9))

fig.suptitle(
"Wireless Network Architecture Simulation\nLight Load vs Heavy Load",
fontsize=16,
fontweight="bold"
)

# ==============================
# DRAW FUNCTION
# ==============================

def draw(ax,G,pos,title,color,packet_pos):

    ax.clear()

    nx.draw_networkx_edges(
        G,pos,ax=ax,
        width=2,
        edge_color=color,
        alpha=0.7
    )

    nx.draw_networkx_nodes(
        G,pos,ax=ax,
        node_color="white",
        edgecolors=color,
        node_size=1100,
        linewidths=2
    )

    nx.draw_networkx_labels(
        G,pos,
        ax=ax,
        font_size=11,
        font_weight="bold"
    )

    for p in packet_pos:
        if p:
            ax.scatter(
                p[0],
                p[1],
                s=120,
                color="red",
                zorder=5
            )

    ax.set_title(title,fontsize=11)
    ax.set_xticks([])
    ax.set_yticks([])


# ==============================
# SIMULATION UPDATE
# ==============================

def update(step):

    packet_positions=[]

    for i,G in enumerate(graphs):

        load = LIGHT_RATE if i<3 else HEAVY_RATE

        # tạo packet
        if random.random()<load:

            p=create_packet(G,step)

            if p:
                packets[i].append(p)
                sent[i]+=1

        pos_list=[]

        for p in packets[i][:]:

            pos=move_packet(p,positions[i])

            if p.index>=len(p.path)-1:

                recv[i]+=1

                delay_steps=step-p.start
                delay_ms=delay_steps*STEP_TIME_MS
                delay_sum[i]+=delay_ms

                packets[i].remove(p)

            else:

                if pos:
                    pos_list.append(pos)

        packet_positions.append(pos_list)

    k=0

    for r in range(2):
        for c in range(3):

            draw(
                axes[r][c],
                graphs[k],
                positions[k],
                titles[k],
                colors[k],
                packet_positions[k]
            )

            k+=1


ani=FuncAnimation(
    fig,
    update,
    frames=SIM_STEPS,
    interval=120
)

plt.subplots_adjust(top=0.88,hspace=0.35,wspace=0.25)

plt.show()

# ==============================
# METRICS CALCULATION
# ==============================

throughput=[]
pdr=[]
delay=[]

for i in range(6):

    th=(recv[i]*PACKET_SIZE*1000)/(SIM_STEPS*STEP_TIME_MS)
    throughput.append(th)

    pdr_val=(recv[i]/sent[i]*100) if sent[i]>0 else 0
    pdr.append(pdr_val)

    delay_val=(delay_sum[i]/recv[i]) if recv[i]>0 else 0
    delay.append(delay_val)

# ==============================
# DASHBOARD
# ==============================

plt.style.use("seaborn-v0_8-whitegrid")

arch=["Adhoc","Infrastructure","Mesh"]

light_th=throughput[:3]
heavy_th=throughput[3:]

light_pdr=pdr[:3]
heavy_pdr=pdr[3:]

light_delay=delay[:3]
heavy_delay=delay[3:]

x=np.arange(len(arch))
w=0.35

fig2=plt.figure(figsize=(16,10))

fig2.suptitle(
"Wireless Network Architecture Performance",
fontsize=18,
fontweight="bold"
)

# Throughput

ax1=fig2.add_subplot(2,2,1)

bars1=ax1.bar(x-w/2,light_th,w,label="Light Load")
bars2=ax1.bar(x+w/2,heavy_th,w,label="Heavy Load")

ax1.set_title("Throughput (Kbps)")
ax1.set_xticks(x)
ax1.set_xticklabels(arch)
ax1.legend()

# PDR

ax2=fig2.add_subplot(2,2,2)

bars3=ax2.bar(x-w/2,light_pdr,w,label="Light Load")
bars4=ax2.bar(x+w/2,heavy_pdr,w,label="Heavy Load")

ax2.set_title("Packet Delivery Ratio (%)")
ax2.set_xticks(x)
ax2.set_xticklabels(arch)

# Delay

ax3=fig2.add_subplot(2,2,3)

bars5=ax3.bar(x-w/2,light_delay,w,label="Light Load")
bars6=ax3.bar(x+w/2,heavy_delay,w,label="Heavy Load")

ax3.set_title("Delay (ms)")
ax3.set_xticks(x)
ax3.set_xticklabels(arch)

# TABLE

ax4=fig2.add_subplot(2,2,4)
ax4.axis("off")

table_data=[
["Adhoc",light_th[0],heavy_th[0],light_pdr[0],heavy_pdr[0],light_delay[0],heavy_delay[0]],
["Infrastructure",light_th[1],heavy_th[1],light_pdr[1],heavy_pdr[1],light_delay[1],heavy_delay[1]],
["Mesh",light_th[2],heavy_th[2],light_pdr[2],heavy_pdr[2],light_delay[2],heavy_delay[2]],
]

columns=[
"Architecture",
"Th Light","Th Heavy",
"PDR Light","PDR Heavy",
"Delay Light","Delay Heavy"
]

table_text=[]
for row in table_data:
    formatted=[row[0]]+[f"{v:.2f}" for v in row[1:]]
    table_text.append(formatted)

table=ax4.table(
cellText=table_text,
colLabels=columns,
loc="center",
cellLoc="center"
)

table.scale(1,2)

plt.tight_layout(rect=[0,0,1,0.95])
plt.show()
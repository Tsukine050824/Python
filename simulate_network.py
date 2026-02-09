import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

np.random.seed(42)
SPEED_OF_LIGHT = 3e8  # m/s

class WirelessNetwork:
    def __init__(self, name, radius, bandwidth, base_delay):
        self.name = name
        self.radius = radius
        self.bandwidth = bandwidth
        self.base_delay = base_delay

    def simulate(self, sim_time, num_nodes, packet_rate,
                 mobility_speed, packet_size=1024, log_packets=0):

        delivered = 0
        lost = 0
        total_delay = 0
        total_bits = 0

        positions = np.random.uniform(-self.radius, self.radius, (num_nodes, 2))

        for t in range(sim_time):
            positions += np.random.uniform(
                -mobility_speed, mobility_speed, (num_nodes, 2)
            )

            for _ in range(num_nodes * packet_rate):
                src = np.random.randint(0, num_nodes)
                dst = np.random.randint(0, num_nodes)
                while dst == src:
                    dst = np.random.randint(0, num_nodes)

                dist = np.linalg.norm(positions[src] - positions[dst])
                # Scale loss coefficient by network radius so larger-range
                # technologies (WMAN) don't suffer near-100% loss from large
                # absolute distances. This keeps the physical intuition but
                # avoids making long-range networks unusable in the toy model.
                alpha = 0.02 * (10.0 / max(1.0, self.radius))
                loss_prob = 1 - np.exp(-alpha * dist)
                loss_prob = min(loss_prob, 1.0)

                if np.random.rand() < loss_prob:
                    lost += 1
                else:
                    tx_delay = packet_size * 8 / self.bandwidth
                    prop_delay = dist / SPEED_OF_LIGHT
                    queue_delay = np.random.exponential(0.001)

                    delay = self.base_delay + tx_delay + prop_delay + queue_delay

                    delivered += 1
                    total_delay += delay
                    total_bits += packet_size * 8

        throughput = total_bits / sim_time
        avg_delay = total_delay / delivered if delivered > 0 else 0
        packet_loss = lost / (lost + delivered)

        return throughput, avg_delay, packet_loss


# ===== Khai báo mạng =====
networks = [
    WirelessNetwork("WPAN", 10, 250_000, 0.01),
    WirelessNetwork("WLAN", 100, 54_000_000, 0.005),
    # Reduce radius so WMAN nodes are within useful range (avoid near-100% loss)
    WirelessNetwork("WMAN", 1000, 70_000_000, 0.02)
]

# ===== Kịch bản =====
scenarios = [
    {"name": "KB1_PA1", "nodes": 20, "mobility": 8},
    {"name": "KB1_PA2", "nodes": 20, "mobility": 2},
    {"name": "KB2_PA1", "nodes": 40, "mobility": 10},
    {"name": "KB2_PA2", "nodes": 40, "mobility": 3},
]


results = []

for sc in scenarios:
    for net in networks:
        tp, d, loss = net.simulate(
            sim_time=10,
            num_nodes=sc["nodes"],
            packet_rate=5,
            mobility_speed=sc["mobility"]
        )

        results.append({
            "Scenario": sc["name"],
            "Network": net.name,
            "Throughput_Mbps": tp / 1e6,
            "Delay_ms": d * 1000,
            "Packet_Loss_%": loss * 100
        })

df = pd.DataFrame(results)
print(df)
print("\nCÁC NETWORK CÓ TRONG DF:")
print(df["Network"].unique())

# ===== VẼ BIỂU ĐỒ =====
throughput_pivot = df.pivot(index="Scenario", columns="Network", values="Throughput_Mbps")
delay_pivot = df.pivot(index="Scenario", columns="Network", values="Delay_ms")
loss_pivot = df.pivot(index="Scenario", columns="Network", values="Packet_Loss_%")

fig1, ax1 = plt.subplots()
throughput_pivot.plot(kind="bar", ax=ax1)
ax1.set_title("Throughput Comparison (Mbps)")
ax1.set_xlabel("Scenario")
ax1.set_ylabel("Throughput (Mbps)")
ax1.tick_params(axis='x', rotation=0)
fig1.tight_layout()

fig2, ax2 = plt.subplots()
delay_pivot.plot(kind="bar", ax=ax2)
ax2.set_title("Average Delay Comparison (ms)")
ax2.set_xlabel("Scenario")
ax2.set_ylabel("Delay (ms)")
ax2.tick_params(axis='x', rotation=0)
fig2.tight_layout()

fig3, ax3 = plt.subplots()
loss_pivot.plot(kind="bar", ax=ax3)
ax3.set_title("Packet Loss Comparison (%)")
ax3.set_xlabel("Scenario")
ax3.set_ylabel("Packet Loss (%)")
ax3.tick_params(axis='x', rotation=0)
fig3.tight_layout()

# Allow skipping the (slow) animation for automated runs / debugging
if os.environ.get("SKIP_ANIMATION") != "1":
    plt.show()

# ================== ANIMATION NODE ==================

def animate_packets(network: WirelessNetwork, scenario: dict,
                    steps=15):

    radius = network.radius
    num_nodes = scenario["nodes"]
    mobility = scenario["mobility"]

    positions = np.random.uniform(-radius, radius, (num_nodes, 2))

    plt.figure()

    for step in range(steps):
        plt.clf()

        # node di chuyển nhẹ
        positions += np.random.uniform(-mobility*0.3, mobility*0.3, (num_nodes, 2))

        plt.scatter(positions[:, 0], positions[:, 1], color="green", s=40)

        circle = plt.Circle((0, 0), radius, fill=False)
        plt.gca().add_patch(circle)

        # chọn src và dst
        src = np.random.randint(0, num_nodes)
        dst = np.random.randint(0, num_nodes)
        while dst == src:
            dst = np.random.randint(0, num_nodes)

        src_pos = positions[src]
        dst_pos = positions[dst]

        # vẽ đường nét đứt cố định
        plt.plot([src_pos[0], dst_pos[0]],
                 [src_pos[1], dst_pos[1]],
                 linestyle="--")

        dist = np.linalg.norm(src_pos - dst_pos)

        alpha_loss = 0.02
        loss_prob = 1 - np.exp(-alpha_loss * dist)
        is_lost = np.random.rand() < loss_prob

        delivered = False

        # packet di chuyển
        for alpha_move in np.linspace(0, 1, 25):

            plt.clf()
            plt.scatter(positions[:, 0], positions[:, 1], color="green", s=40)

            circle = plt.Circle((0, 0), radius, fill=False)
            plt.gca().add_patch(circle)

            # vẽ lại đường nét đứt
            plt.plot([src_pos[0], dst_pos[0]],
                     [src_pos[1], dst_pos[1]],
                     linestyle="--")

            pkt_x = src_pos[0] + alpha_move * (dst_pos[0] - src_pos[0])
            pkt_y = src_pos[1] + alpha_move * (dst_pos[1] - src_pos[1])

            # 🎨 đổi màu khi gần đến đích
            if alpha_move > 0.8:
                color = "orange"
            else:
                color = "red"

            # ❌ nếu mất gói → dừng giữa đường
            if is_lost and alpha_move > 0.5:
                plt.scatter(pkt_x, pkt_y, color="black", s=80)
                plt.text(0, radius*1.05, "LOST ", ha="center")
                break

            # vẽ packet (chỉ 1 chấm di chuyển)
            plt.scatter(pkt_x, pkt_y, color=color, s=120)

            plt.xlim(-radius*1.2, radius*1.2)
            plt.ylim(-radius*1.2, radius*1.2)
            plt.gca().set_aspect("equal", adjustable="box")

            plt.title(f"Packet Animation - {network.name} - {scenario['name']}")
            plt.pause(0.03)

            if alpha_move >= 1.0:
                delivered = True

        # 🎉 nếu thành công
        if delivered and not is_lost:
            plt.text(0, radius*1.05, "DELIVERED ", ha="center")
            plt.pause(0.5)

    plt.show()





# ===== CHẠY ANIMATION THEO SCENARIO =====
for sc in scenarios:
    for net in networks:
        animate_packets(net, sc, steps=20)






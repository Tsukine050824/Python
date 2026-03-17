import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

np.random.seed(42)
SPEED_OF_LIGHT = 3e8  # m/s


# ===============================
# CLASS MÔ PHỎNG MẠNG KHÔNG DÂY
# ===============================
class WirelessNetwork:
    def __init__(self, name, radius, bandwidth, base_delay):
        self.name = name
        self.radius = radius          # phạm vi phủ sóng
        self.bandwidth = bandwidth    # băng thông (tốc độ lý thuyết)
        self.base_delay = base_delay  # độ trễ nền

    def simulate(self, sim_time, num_nodes, packet_rate,
                 mobility_speed, packet_size=1024):

        delivered = 0
        total_delay = 0
        total_bits = 0

        # khởi tạo vị trí node
        positions = np.random.uniform(
            -self.radius, self.radius, (num_nodes, 2)
        )

        for _ in range(sim_time):

            # node di chuyển (mobility)
            positions += np.random.uniform(
                -mobility_speed, mobility_speed, (num_nodes, 2)
            )

            for _ in range(num_nodes * packet_rate):

                src = np.random.randint(0, num_nodes)
                dst = np.random.randint(0, num_nodes)
                while dst == src:
                    dst = np.random.randint(0, num_nodes)

                dist = np.linalg.norm(positions[src] - positions[dst])

                # xác suất mất gói phụ thuộc khoảng cách / phạm vi
                loss_prob = min(dist / self.radius, 1.0)

                if np.random.rand() > loss_prob:

                    tx_delay = packet_size * 8 / self.bandwidth
                    prop_delay = dist / SPEED_OF_LIGHT

                    delay = self.base_delay + tx_delay + prop_delay

                    delivered += 1
                    total_delay += delay
                    total_bits += packet_size * 8

        throughput = total_bits / sim_time
        avg_delay = total_delay / delivered if delivered > 0 else 0

        return throughput, avg_delay


# ===============================
# KHAI BÁO 3 LOẠI MẠNG
# ===============================
networks = [
    WirelessNetwork("WPAN", 10, 250_000, 0.01),
    WirelessNetwork("WLAN", 100, 54_000_000, 0.005),
    WirelessNetwork("WMAN", 1000, 70_000_000, 0.02)
]


# ===============================
# KỊCH BẢN MÔ PHỎNG
# ===============================
scenarios = [
    {"name": "KB1_PA1", "nodes": 20, "mobility": 8},
    {"name": "KB1_PA2", "nodes": 20, "mobility": 2},
    {"name": "KB2_PA1", "nodes": 40, "mobility": 10},
    {"name": "KB2_PA2", "nodes": 40, "mobility": 3},
]


# ===============================
# CHẠY MÔ PHỎNG
# ===============================
results = []

for sc in scenarios:
    for net in networks:

        tp, d = net.simulate(
            sim_time=10,
            num_nodes=sc["nodes"],
            packet_rate=5,
            mobility_speed=sc["mobility"]
        )

        results.append({
            "Scenario": sc["name"],
            "Network": net.name,
            "Throughput_Mbps": tp / 1e6,
            "Delay_ms": d * 1000
        })

df = pd.DataFrame(results)
print(df)


# ===============================
# VẼ BIỂU ĐỒ
# ===============================
throughput_pivot = df.pivot(
    index="Scenario",
    columns="Network",
    values="Throughput_Mbps"
)

delay_pivot = df.pivot(
    index="Scenario",
    columns="Network",
    values="Delay_ms"
)

# đảm bảo thứ tự đúng
order = ["WPAN", "WLAN", "WMAN"]
throughput_pivot = throughput_pivot[order]
delay_pivot = delay_pivot[order]

# Biểu đồ Throughput
fig1, ax1 = plt.subplots()
throughput_pivot.plot(kind="bar", ax=ax1)
ax1.set_title("Throughput Comparison (Mbps)")
ax1.set_ylabel("Throughput (Mbps)")
ax1.tick_params(axis='x', rotation=0)
fig1.tight_layout()

# Biểu đồ Delay
fig2, ax2 = plt.subplots()
delay_pivot.plot(kind="bar", ax=ax2)
ax2.set_title("Average Delay Comparison (ms)")
ax2.set_ylabel("Delay (ms)")
ax2.tick_params(axis='x', rotation=0)
fig2.tight_layout()

plt.show()


# ===============================
# ANIMATION MÔ PHỎNG GÓI TIN
# ===============================
def animate_packets(network: WirelessNetwork, scenario: dict, steps=10):

    radius = network.radius
    num_nodes = scenario["nodes"]
    mobility = scenario["mobility"]

    positions = np.random.uniform(-radius, radius, (num_nodes, 2))

    plt.figure()

    for _ in range(steps):

        positions += np.random.uniform(
            -mobility*0.3, mobility*0.3, (num_nodes, 2)
        )

        src = np.random.randint(0, num_nodes)
        dst = np.random.randint(0, num_nodes)
        while dst == src:
            dst = np.random.randint(0, num_nodes)

        src_pos = positions[src]
        dst_pos = positions[dst]

        dist = np.linalg.norm(src_pos - dst_pos)
        loss_prob = min(dist / radius, 1.0)
        is_lost = np.random.rand() < loss_prob

        for alpha in np.linspace(0, 1, 25):

            plt.clf()

            plt.scatter(positions[:, 0], positions[:, 1],
                        color="green", s=40)

            circle = plt.Circle((0, 0), radius, fill=False)
            plt.gca().add_patch(circle)

            plt.plot([src_pos[0], dst_pos[0]],
                     [src_pos[1], dst_pos[1]],
                     linestyle="--")

            pkt_x = src_pos[0] + alpha * (dst_pos[0] - src_pos[0])
            pkt_y = src_pos[1] + alpha * (dst_pos[1] - src_pos[1])

            if is_lost and alpha > 0.5:
                plt.scatter(pkt_x, pkt_y, color="black", s=100)
                plt.text(0, radius*1.1, "LOST", ha="center")
                break

            color = "orange" if alpha > 0.8 else "red"
            plt.scatter(pkt_x, pkt_y, color=color, s=120)

            plt.xlim(-radius*1.2, radius*1.2)
            plt.ylim(-radius*1.2, radius*1.2)
            plt.gca().set_aspect("equal")

            plt.title(f"{network.name} - {scenario['name']}")
            plt.pause(0.03)

        if not is_lost:
            plt.text(0, radius*1.1, "DELIVERED", ha="center")
            plt.pause(0.5)

    plt.show()


# ===============================
# CHẠY ANIMATION
# ===============================
for sc in scenarios:
    for net in networks:
        animate_packets(net, sc, steps=5)

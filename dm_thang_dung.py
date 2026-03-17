import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3


class Packet:
    def __init__(self, source, target, color, speed):
        self.source = np.array(source, dtype=float)
        self.target = np.array(target, dtype=float)
        self.position = np.array(source, dtype=float)
        self.color = color
        self.speed = speed
        self.alive = True
        self.progress = 0
        self.direction = self.target - self.source
        self.distance = np.linalg.norm(self.direction)
        if self.distance > 0:
            self.direction = self.direction / self.distance

    def update(self):
        self.progress += self.speed / self.distance if self.distance > 0 else 1
        if self.progress >= 1:
            self.alive = False
            self.position = self.target.copy()
        else:
            self.position = self.source + self.direction * self.distance * self.progress


class NetworkSimulation:
    NETWORKS = {
        'WPAN': {'color': '#E74C3C', 'radius': 50, 'real_radius': '1-10m', 
                 'speed': 3, 'packet_rate': 0.15, 'label': 'WPAN\n(Bluetooth/Zigbee)\n1-10m', 'clients': 6},
        'WLAN': {'color': '#27AE60', 'radius': 150, 'real_radius': '10-100m',
                 'speed': 6, 'packet_rate': 0.2, 'label': 'WLAN\n(Wi-Fi)\n10-100m', 'clients': 8},
        'WMAN': {'color': '#3498DB', 'radius': 300, 'real_radius': '1-50km',
                 'speed': 5, 'packet_rate': 0.15, 'label': 'WMAN\n(WiMAX)\n1-50km', 'clients': 10}
    }
    CENTERS = {'WPAN': (-400, 0), 'WLAN': (0, 0), 'WMAN': (500, 0)}

    def __init__(self):
        self.nodes = {}
        self.all_packets = []
        self.stats = {k: {'sent': 0, 'received': 0} for k in self.NETWORKS}
        self.frame_count = 0
        self._create_nodes()
        self._setup_figure()

    def _create_nodes(self):
        for net_type, center in self.CENTERS.items():
            net = self.NETWORKS[net_type]
            self.nodes[net_type] = [{'x': center[0], 'y': center[1], 'type': 'router'}]
            for i in range(net['clients']):
                angle = 2 * np.pi * i / net['clients']
                r = net['radius'] * 0.7 * (0.5 + 0.5 * random.random())
                self.nodes[net_type].append({
                    'x': center[0] + r * np.cos(angle),
                    'y': center[1] + r * np.sin(angle),
                    'type': 'client'
                })

    def _setup_figure(self):
        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        self.fig.patch.set_facecolor('white')
        self.ax.set_facecolor('white')
        self.ax.set_xlim(-850, 900)
        self.ax.set_ylim(-400, 400)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.4)
        self.ax.set_xlabel('Distance (scaled)', fontsize=10)
        self.ax.set_ylabel('Distance (scaled)', fontsize=10)
        self.ax.set_title('MO PHONG REAL-TIME: PACKET TRANSMISSION - WLAN/WPAN/WMAN',
                          fontsize=14, fontweight='bold', color='#2C3E50', pad=15)

        self.pulse_circles = {}
        for net_type, center in self.CENTERS.items():
            net = self.NETWORKS[net_type]
            self.ax.add_patch(plt.Circle(center, net['radius'], fill=True, alpha=0.2,
                                         facecolor=net['color'], edgecolor=net['color'], linewidth=2.5))
            pulse = plt.Circle(center, net['radius'] * 0.5, fill=False, alpha=0.6,
                               edgecolor=net['color'], linewidth=1.5)
            self.ax.add_patch(pulse)
            self.pulse_circles[net_type] = pulse
            self.ax.text(center[0], center[1] + net['radius'] + 25, net['label'],
                         ha='center', va='bottom', fontsize=10, fontweight='bold', color=net['color'])

        for net_type, nodes in self.nodes.items():
            color = self.NETWORKS[net_type]['color']
            for node in nodes:
                marker, size = ('s', 12) if node['type'] == 'router' else ('o', 7)
                self.ax.plot(node['x'], node['y'], marker, markersize=size, color=color,
                             markeredgecolor='black', markeredgewidth=1.5 if node['type'] == 'router' else 1)

        self.packet_scatter = self.ax.scatter([], [], s=40, c=[], edgecolors='black', linewidth=0.5, zorder=10)
        self.stats_text = self.ax.text(-830, 380, '', fontsize=9, color='#2C3E50', verticalalignment='top',
                                        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='#ECF0F1', alpha=0.8))

        for i, (net_type, net) in enumerate(self.NETWORKS.items()):
            x_pos = -550 + i * 400
            self.ax.add_patch(plt.Circle((x_pos, -370), 12, color=net['color'], ec='black'))
            self.ax.text(x_pos + 25, -370, f"{net_type}: Ban kinh thuc {net['real_radius']}",
                         color='#2C3E50', fontsize=9, va='center', fontweight='bold')

    def _generate_packet(self, net_type):
        nodes = self.nodes[net_type]
        net = self.NETWORKS[net_type]
        if len(nodes) < 2:
            return
        if random.random() < 0.5:
            source, target = nodes[0], random.choice(nodes[1:])
        else:
            source = random.choice(nodes[1:])
            target = random.choice([n for n in nodes if n != source])
        self.all_packets.append({
            'packet': Packet((source['x'], source['y']), (target['x'], target['y']), net['color'], net['speed']),
            'type': net_type
        })
        self.stats[net_type]['sent'] += 1

    def update(self, frame):
        self.frame_count += 1

        for net_type, net in self.NETWORKS.items():
            if random.random() < net['packet_rate']:
                self._generate_packet(net_type)

        alive_packets, positions, colors = [], [], []
        for pdata in self.all_packets:
            packet, net_type = pdata['packet'], pdata['type']
            if packet.alive:
                packet.update()
                positions.append(packet.position)
                colors.append(packet.color)
                alive_packets.append(pdata)
            else:
                self.stats[net_type]['received'] += 1
        self.all_packets = alive_packets

        if positions:
            self.packet_scatter.set_offsets(np.array(positions))
            self.packet_scatter.set_facecolors(colors)
        else:
            self.packet_scatter.set_offsets(np.empty((0, 2)))

        for net_type, pulse in self.pulse_circles.items():
            radius = self.NETWORKS[net_type]['radius']
            phase = (self.frame_count % 40) / 40
            pulse.set_radius(radius * (0.3 + 0.7 * phase))
            pulse.set_alpha(0.6 * (1 - phase))

        total_sent = sum(s['sent'] for s in self.stats.values())
        total_recv = sum(s['received'] for s in self.stats.values())
        stats_str = "THONG KE PACKETS:\n" + "-" * 22 + "\n"
        for net_type, stat in self.stats.items():
            stats_str += f"{net_type}: Gui={stat['sent']:3d} | Nhan={stat['received']:3d}\n"
        stats_str += "-" * 22 + f"\nTONG: Gui={total_sent:3d} | Nhan={total_recv:3d}\nDang truyen: {len(self.all_packets)}"
        self.stats_text.set_text(stats_str)

        return [self.packet_scatter, self.stats_text] + list(self.pulse_circles.values())

    def run(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=None, interval=33, blit=True, cache_frame_data=False)
        plt.tight_layout()
        plt.show()


def main():
    print("\n" + "=" * 55)
    print("  MO PHONG REAL-TIME PACKET TRANSMISSION")
    print("     So sanh ban kinh WLAN / WPAN / WMAN")
    print("=" * 55)
    print("\n[DO]   WPAN : Bluetooth/Zigbee - Ban kinh 1-10m")
    print("[XANH] WLAN : Wi-Fi - Ban kinh 10-100m")
    print("[LAM]  WMAN : WiMAX - Ban kinh 1-50km")
    print("\n* Packets di chuyen giua cac nodes trong vung phu song")
    print("* Dong cua so de ket thuc mo phong\n")
    NetworkSimulation().run()


if __name__ == "__main__":
    main()

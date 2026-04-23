import matplotlib 
# chức năng là hiển thị đồ họa, tạo biểu đồ và hoạt hình. 
matplotlib.use('TkAgg')
# TkAgg là một backend của Matplotlib cho phép hiển thị đồ họa trong các ứng dụng Tkinter.
import matplotlib.pyplot as plt
# pyplot là một module của Matplotlib cung cấp một giao diện giống như MATLAB để tạo biểu đồ và đồ họa.
import matplotlib.animation as animation
# animation là một module của Matplotlib cho phép tạo các hoạt hình bằng cách cập nhật các khung hình liên tục.
import numpy as np
# NumPy là một thư viện Python mạnh mẽ cho tính toán khoa học, cung cấp các cấu trúc dữ liệu và hàm toán học hiệu quả để làm việc với mảng và ma trận.
import random
# random là một module tích hợp của Python cung cấp các hàm để tạo số ngẫu nhiên và thực hiện các phép toán liên quan đến ngẫu nhiên.
import tkinter as tk
# Tkinter là một thư viện GUI tích hợp của Python, cho phép tạo các ứng dụng đồ họa với giao diện người dùng.
from tkinter import ttk
# ttk là một module của Tkinter cung cấp các widget có kiểu dáng hiện đại và cải tiến, như nút, hộp văn bản, và bảng.
from collections import defaultdict
# defaultdict là một lớp trong module collections của Python, cung cấp một từ điển mặc định cho phép tự động tạo giá trị mặc định khi truy cập vào các khóa chưa tồn tại.

# ════════════════ FONT CONFIG (fix loi font tieng Viet) ════════════════
FONT_SANS = 'DejaVu Sans'
FONT_MONO = 'DejaVu Sans Mono'

plt.style.use('default')
plt.rcParams['font.family'] = FONT_SANS
plt.rcParams['font.sans-serif'] = [FONT_SANS, 'Arial', 'Liberation Sans']
plt.rcParams['font.monospace'] = [FONT_MONO, 'Liberation Mono', 'Courier New']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = '#1a1a2e'
plt.rcParams['axes.facecolor'] = '#16213e'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.15
plt.rcParams['grid.color'] = '#e0e0e0'
plt.rcParams['text.color'] = '#e0e0e0'
plt.rcParams['axes.labelcolor'] = '#e0e0e0'
plt.rcParams['xtick.color'] = '#e0e0e0'
plt.rcParams['ytick.color'] = '#e0e0e0'

# ════════════════════ CONSTANTS ════════════════════
SCENARIO_DURATION_FRAMES = 500
FPS_INTERVAL = 33
CENTERS = {'WPAN': (-400, 0), 'WLAN': (0, 0), 'WMAN': (500, 0)}


# ════════════════════ SCENARIO CONFIGS ════════════════════
SCENARIOS = {
    'light': {
        'name': 'KICH BAN 1: TAI NHE',
        'desc': 'It nut - Kenh tot - Mobility thap',
        'short': 'KB1-Nhe',
        'banner_color': '#00b894',
        'networks': {
            'WPAN': {
                'color': '#ff6b6b', 'radius': 55, 'real_radius': '1-10m',
                'speed': 3.5, 'packet_rate': 0.08, 'clients': 4,
                'loss_prob': 0.02, 'collision_prob': 0.03, 'mobility': 0.3,
                'label': 'WPAN\n(Bluetooth/Zigbee)\n1-10m',
            },
            'WLAN': {
                'color': '#51cf66', 'radius': 150, 'real_radius': '10-100m',
                'speed': 7.0, 'packet_rate': 0.10, 'clients': 5,
                'loss_prob': 0.03, 'collision_prob': 0.04, 'mobility': 0.5,
                'label': 'WLAN\n(Wi-Fi)\n10-100m',
            },
            'WMAN': {
                'color': '#339af0', 'radius': 300, 'real_radius': '1-50km',
                'speed': 5.5, 'packet_rate': 0.07, 'clients': 6,
                'loss_prob': 0.04, 'collision_prob': 0.05, 'mobility': 0.2,
                'label': 'WMAN\n(WiMAX)\n1-50km',
            },
        },
    },
    'heavy': {
        'name': 'KICH BAN 2: TAI NANG',
        'desc': 'Nhieu nut - Kenh xau - Mobility cao',
        'short': 'KB2-Nang',
        'banner_color': '#e17055',
        'networks': {
            'WPAN': {
                'color': '#ff6b6b', 'radius': 55, 'real_radius': '1-10m',
                'speed': 2.5, 'packet_rate': 0.25, 'clients': 10,
                'loss_prob': 0.12, 'collision_prob': 0.18, 'mobility': 2.0,
                'label': 'WPAN\n(Bluetooth/Zigbee)\n1-10m',
            },
            'WLAN': {
                'color': '#51cf66', 'radius': 150, 'real_radius': '10-100m',
                'speed': 5.0, 'packet_rate': 0.30, 'clients': 14,
                'loss_prob': 0.10, 'collision_prob': 0.15, 'mobility': 3.0,
                'label': 'WLAN\n(Wi-Fi)\n10-100m',
            },
            'WMAN': {
                'color': '#339af0', 'radius': 300, 'real_radius': '1-50km',
                'speed': 4.0, 'packet_rate': 0.22, 'clients': 16,
                'loss_prob': 0.15, 'collision_prob': 0.20, 'mobility': 1.5,
                'label': 'WMAN\n(WiMAX)\n1-50km',
            },
        },
    },
}


# ════════════════════ PACKET ════════════════════
class Packet:
    _id_counter = 0

    def __init__(self, source, target, color, speed, net_type, created_frame):
        Packet._id_counter += 1
        self.id = Packet._id_counter
        self.source = np.array(source, dtype=float)
        self.target = np.array(target, dtype=float)
        self.position = np.array(source, dtype=float)
        self.color = color
        self.speed = speed
        self.net_type = net_type
        self.alive = True
        self.progress = 0.0
        self.created_frame = created_frame
        self.collided = False
        self.target_node_id = 0

        self.direction = self.target - self.source
        self.distance = np.linalg.norm(self.direction)
        if self.distance > 0:
            self.direction /= self.distance

    def update(self):
        if not self.alive:
            return
        self.progress += self.speed / max(self.distance, 1e-6)
        if self.progress >= 1.0:
            self.alive = False
            self.position = self.target.copy()
        else:
            self.position = self.source + self.direction * self.distance * self.progress


# ════════════════════ METRIC TRACKER ════════════════════
class MetricTracker:
    def __init__(self):
        self.reset()

    def reset(self):
        self.packets_sent = defaultdict(int)
        self.packets_received = defaultdict(int)
        self.packets_lost = defaultdict(int)
        self.packets_collided = defaultdict(int)
        self.delays = defaultdict(list)
        self.throughput_history = defaultdict(list)
        self.per_node_received = defaultdict(lambda: defaultdict(int))
        self._win_recv = defaultdict(int)
        self._win_start = 0

    def record_sent(self, nt):
        self.packets_sent[nt] += 1

    def record_received(self, nt, delay_frames, node_id=0):
        self.packets_received[nt] += 1
        self.delays[nt].append(delay_frames * FPS_INTERVAL)
        self.per_node_received[nt][node_id] += 1
        self._win_recv[nt] += 1

    def record_lost(self, nt):
        self.packets_lost[nt] += 1

    def record_collision(self, nt):
        self.packets_collided[nt] += 1

    def snapshot_throughput(self, elapsed):
        w = max(elapsed - self._win_start, 1)
        for nt in ['WPAN', 'WLAN', 'WMAN']:
            tp = self._win_recv[nt] / (w * FPS_INTERVAL / 1000.0)
            self.throughput_history[nt].append(tp)
            self._win_recv[nt] = 0
        self._win_start = elapsed

    def throughput(self, nt, total_frames):
        t = max(total_frames * FPS_INTERVAL / 1000.0, 0.001)
        return self.packets_received[nt] / t

    def avg_delay(self, nt):
        d = self.delays[nt]
        return float(np.mean(d)) if d else 0.0

    def jitter(self, nt):
        d = self.delays[nt]
        if len(d) < 2:
            return 0.0
        return float(np.mean([abs(d[i] - d[i-1]) for i in range(1, len(d))]))

    def pdr(self, nt):
        s = self.packets_sent[nt]
        return (self.packets_received[nt] / s * 100) if s else 0.0

    def collision_rate(self, nt):
        s = self.packets_sent[nt]
        return (self.packets_collided[nt] / s * 100) if s else 0.0

    def jain_fairness(self, nt):
        c = list(self.per_node_received[nt].values())
        if not c:
            return 1.0
        n, s, ss = len(c), sum(c), sum(x**2 for x in c)
        return (s**2) / (n * ss) if ss else 1.0

    def summary(self, total_frames):
        r = {}
        for nt in ['WPAN', 'WLAN', 'WMAN']:
            r[nt] = {
                'throughput': self.throughput(nt, total_frames),
                'delay': self.avg_delay(nt),
                'pdr': self.pdr(nt),
                'jitter': self.jitter(nt),
                'collision_rate': self.collision_rate(nt),
                'fairness': self.jain_fairness(nt),
                'sent': self.packets_sent[nt],
                'received': self.packets_received[nt],
                'lost': self.packets_lost[nt],
                'collided': self.packets_collided[nt],
                'throughput_history': list(self.throughput_history[nt]),
            }
        return r


# ════════════════════ SINGLE SCENARIO ANIMATION ════════════════════
class ScenarioAnimation:
    """Chay animation rieng cho 1 kich ban, tra ve ket qua metric."""

    def __init__(self, scenario_key):
        self.scenario_key = scenario_key
        self.scenario = SCENARIOS[scenario_key]
        self.networks = self.scenario['networks']
        self.tracker = MetricTracker()
        self.packets = []
        self.nodes = {}
        self.frame_count = 0
        self.finished = False
        Packet._id_counter = 0

        self._create_nodes()
        self._setup_figure()

    def _create_nodes(self):
        for nt, center in CENTERS.items():
            net = self.networks[nt]
            nodes = [{'x': center[0], 'y': center[1], 'type': 'router',
                      'vx': 0, 'vy': 0, 'id': 0}]
            for i in range(net['clients']):
                a = 2 * np.pi * i / net['clients']
                r = net['radius'] * 0.65 * (0.4 + 0.6 * random.random())
                nodes.append({
                    'x': center[0] + r * np.cos(a),
                    'y': center[1] + r * np.sin(a),
                    'vx': random.uniform(-1, 1) * net['mobility'],
                    'vy': random.uniform(-1, 1) * net['mobility'],
                    'type': 'client', 'id': i + 1,
                })
            self.nodes[nt] = nodes

    def _move_nodes(self):
        for nt, center in CENTERS.items():
            net = self.networks[nt]
            cx, cy = center
            for n in self.nodes[nt]:
                if n['type'] == 'router':
                    continue
                n['x'] += n['vx']
                n['y'] += n['vy']
                dx, dy = n['x'] - cx, n['y'] - cy
                if np.sqrt(dx**2 + dy**2) > net['radius'] * 0.85:
                    n['vx'] *= -1; n['vy'] *= -1
                    n['x'] += n['vx'] * 2; n['y'] += n['vy'] * 2
                if random.random() < 0.05:
                    n['vx'] = random.uniform(-1, 1) * net['mobility']
                    n['vy'] = random.uniform(-1, 1) * net['mobility']

    def _setup_figure(self):
        self.fig = plt.figure(figsize=(17, 9.5))
        self.fig.patch.set_facecolor('#1a1a2e')

        # Main animation axis (left)
        self.ax = self.fig.add_axes([0.02, 0.10, 0.58, 0.78])
        self.ax.set_facecolor('#16213e')
        self.ax.set_xlim(-850, 950)
        self.ax.set_ylim(-450, 450)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.12, color='#e0e0e0')
        self.ax.tick_params(colors='#888', labelsize=7)
        for spine in self.ax.spines.values():
            spine.set_color('#333')

        # Metrics panel (right top)
        self.ax_metrics = self.fig.add_axes([0.62, 0.40, 0.36, 0.48])
        self.ax_metrics.set_facecolor('#0f3460')
        self.ax_metrics.set_xlim(0, 10)
        self.ax_metrics.set_ylim(0, 10)
        self.ax_metrics.axis('off')

        # Stats panel (right bottom)
        self.ax_stats = self.fig.add_axes([0.62, 0.10, 0.36, 0.28])
        self.ax_stats.set_facecolor('#0f3460')
        self.ax_stats.set_xlim(0, 10)
        self.ax_stats.set_ylim(0, 10)
        self.ax_stats.axis('off')

        # Banner title
        bc = self.scenario['banner_color']
        self.fig.text(
            0.50, 0.97,
            f"  >>  {self.scenario['name']}  <<  ",
            ha='center', va='top', fontsize=18, fontweight='bold',
            color='white', family=FONT_SANS,
            bbox=dict(boxstyle='round,pad=0.6', facecolor=bc,
                      edgecolor='white', linewidth=2.5)
        )
        self.fig.text(
            0.50, 0.925,
            f"-- {self.scenario['desc']} --",
            ha='center', va='top', fontsize=12, color='#ddd',
            family=FONT_SANS, style='italic'
        )

        self._draw_network()
        self._init_text_elements()

    def _draw_network(self):
        ax = self.ax

        # Coverage areas
        self.pulse_circles = {}
        for nt, center in CENTERS.items():
            net = self.networks[nt]
            ax.add_patch(plt.Circle(center, net['radius'], fill=True, alpha=0.08,
                                    facecolor=net['color'], edgecolor=net['color'],
                                    linewidth=2, linestyle='--'))
            p = plt.Circle(center, net['radius'] * 0.5, fill=False, alpha=0.3,
                           edgecolor=net['color'], linewidth=1.5)
            ax.add_patch(p)
            self.pulse_circles[nt] = p
            ax.text(center[0], center[1] + net['radius'] + 18, net['label'],
                    ha='center', va='bottom', fontsize=8, fontweight='bold',
                    color=net['color'], alpha=0.9, family=FONT_SANS)

        # Nodes
        self.node_plots = {}
        for nt, nodes in self.nodes.items():
            c = self.networks[nt]['color']
            for n in nodes:
                if n['type'] == 'router':
                    ax.plot(n['x'], n['y'], 's', ms=12, color=c,
                            mec='white', mew=1.5, zorder=5)
            xs = [n['x'] for n in nodes if n['type'] == 'client']
            ys = [n['y'] for n in nodes if n['type'] == 'client']
            line, = ax.plot(xs, ys, 'o', ms=5, color=c, mec='white', mew=0.4,
                            alpha=0.85, zorder=5)
            self.node_plots[nt] = line

        # Legend
        for i, nt in enumerate(['WPAN', 'WLAN', 'WMAN']):
            net = self.networks[nt]
            xp = -700 + i * 500
            ax.add_patch(plt.Circle((xp, -425), 8, color=net['color'], ec='white'))
            ax.text(xp + 18, -425,
                    f"{nt}: {net['real_radius']} | {net['clients']} nodes | "
                    f"loss={net['loss_prob']*100:.0f}% | coll={net['collision_prob']*100:.0f}%",
                    color='#bbb', fontsize=6.5, va='center', family=FONT_SANS)

        # Scatter plots
        self.pkt_scatter = ax.scatter([], [], s=28, c=[], edgecolors='white',
                                      linewidth=0.3, zorder=10)
        self.col_scatter = ax.scatter([], [], s=90, c='#ffeaa7', marker='X',
                                      linewidth=1.5, zorder=11, alpha=0)

        # Progress
        self.progress_text = ax.text(
            50, -390, '', fontsize=9, ha='center', va='center',
            color='white', fontweight='bold', family=FONT_SANS,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#e94560',
                      alpha=0.9, edgecolor='white', linewidth=1)
        )

    def _init_text_elements(self):
        # Metrics panel header
        self.ax_metrics.text(5, 9.7, 'METRICS REAL-TIME', ha='center', va='top',
                             fontsize=11, fontweight='bold', color='#ffeaa7',
                             family=FONT_MONO)
        self.ax_metrics.axhline(y=9.3, color='#339af0', linewidth=0.8, alpha=0.5)

        self.metrics_text = self.ax_metrics.text(
            0.3, 9.0, '', fontsize=8.5, color='#f8f8f2', va='top',
            family=FONT_MONO, linespacing=1.35
        )

        # Stats panel header
        self.ax_stats.text(5, 9.7, 'THONG KE GOI TIN', ha='center', va='top',
                           fontsize=11, fontweight='bold', color='#ffeaa7',
                           family=FONT_MONO)
        self.ax_stats.axhline(y=9.3, color='#339af0', linewidth=0.8, alpha=0.5)

        self.stats_text = self.ax_stats.text(
            0.3, 9.0, '', fontsize=8.5, color='#f8f8f2', va='top',
            family=FONT_MONO, linespacing=1.35
        )

    def _gen_packets(self):
        for nt in ['WPAN', 'WLAN', 'WMAN']:
            net = self.networks[nt]
            nodes = self.nodes[nt]
            if random.random() >= net['packet_rate'] or len(nodes) < 2:
                continue
            if random.random() < 0.5:
                src, tgt = nodes[0], random.choice(nodes[1:])
            else:
                src = random.choice(nodes[1:])
                tgt = random.choice([n for n in nodes if n['id'] != src['id']])

            pkt = Packet((src['x'], src['y']), (tgt['x'], tgt['y']),
                         net['color'], net['speed'] * (0.8 + 0.4 * random.random()),
                         nt, self.frame_count)
            pkt.target_node_id = tgt['id']

            if random.random() < net['collision_prob']:
                pkt.collided = True
                self.tracker.record_collision(nt)

            if random.random() < net['loss_prob']:
                self.tracker.record_sent(nt)
                self.tracker.record_lost(nt)
                return

            self.packets.append(pkt)
            self.tracker.record_sent(nt)

    def _update(self, frame):
        if self.finished:
            return []

        self.frame_count += 1
        if self.frame_count >= SCENARIO_DURATION_FRAMES:
            self.finished = True
            self.tracker.snapshot_throughput(self.frame_count)
            plt.close(self.fig)
            return []

        self._move_nodes()
        self._gen_packets()

        for nt in ['WPAN', 'WLAN', 'WMAN']:
            xs = [n['x'] for n in self.nodes[nt] if n['type'] == 'client']
            ys = [n['y'] for n in self.nodes[nt] if n['type'] == 'client']
            self.node_plots[nt].set_data(xs, ys)

        alive, positions, colors, col_pos = [], [], [], []
        for pkt in self.packets:
            if not pkt.alive:
                continue
            pkt.update()
            if pkt.alive:
                positions.append(pkt.position)
                colors.append('#ffeaa7' if pkt.collided else pkt.color)
                alive.append(pkt)
            else:
                if not pkt.collided:
                    delay = self.frame_count - pkt.created_frame
                    self.tracker.record_received(pkt.net_type, delay, pkt.target_node_id)
                else:
                    self.tracker.record_lost(pkt.net_type)
                    col_pos.append(pkt.position)
        self.packets = alive

        if self.frame_count % 30 == 0:
            self.tracker.snapshot_throughput(self.frame_count)

        if positions:
            self.pkt_scatter.set_offsets(np.array(positions))
            self.pkt_scatter.set_facecolors(colors)
        else:
            self.pkt_scatter.set_offsets(np.empty((0, 2)))

        if col_pos:
            self.col_scatter.set_offsets(np.array(col_pos))
            self.col_scatter.set_alpha(0.8)
        else:
            a = self.col_scatter.get_alpha()
            if a and a > 0:
                self.col_scatter.set_alpha(max(0, a - 0.08))

        for nt, pulse in self.pulse_circles.items():
            rad = self.networks[nt]['radius']
            ph = (self.frame_count % 50) / 50
            pulse.set_radius(rad * (0.3 + 0.7 * ph))
            pulse.set_alpha(0.35 * (1 - ph))

        # Stats text
        s = ""
        for nt in ['WPAN', 'WLAN', 'WMAN']:
            sent = self.tracker.packets_sent[nt]
            recv = self.tracker.packets_received[nt]
            lost = self.tracker.packets_lost[nt]
            coll = self.tracker.packets_collided[nt]
            s += f"[{nt}]\n"
            s += f"  Gui={sent:4d}  Nhan={recv:4d}\n"
            s += f"  Mat={lost:4d}  Collision={coll:3d}\n"
        total_s = sum(self.tracker.packets_sent[x] for x in ['WPAN','WLAN','WMAN'])
        total_r = sum(self.tracker.packets_received[x] for x in ['WPAN','WLAN','WMAN'])
        s += f"--------------------\n"
        s += f"TONG: Gui={total_s}  Nhan={total_r}\n"
        s += f"Dang truyen: {len(self.packets)}"
        self.stats_text.set_text(s)

        # Metrics text
        m = ""
        for nt in ['WPAN', 'WLAN', 'WMAN']:
            tp = self.tracker.throughput(nt, self.frame_count)
            dl = self.tracker.avg_delay(nt)
            pd = self.tracker.pdr(nt)
            jt = self.tracker.jitter(nt)
            cr = self.tracker.collision_rate(nt)
            fj = self.tracker.jain_fairness(nt)
            m += f"-- {nt} -------------\n"
            m += f"  Throughput : {tp:7.2f} pkt/s\n"
            m += f"  Delay TB   : {dl:7.1f} ms\n"
            m += f"  PDR        : {pd:7.1f} %\n"
            m += f"  Jitter     : {jt:7.1f} ms\n"
            m += f"  Collision  : {cr:7.1f} %\n"
            m += f"  Fairness   : {fj:7.3f}\n"
        self.metrics_text.set_text(m)

        pct = self.frame_count / SCENARIO_DURATION_FRAMES * 100
        self.progress_text.set_text(f"  Tien do: {pct:.0f}%  ")

        return []

    def run(self):
        self.ani = animation.FuncAnimation(
            self.fig, self._update, frames=None,
            interval=FPS_INTERVAL, blit=False, cache_frame_data=False
        )
        plt.show()
        return self.tracker.summary(SCENARIO_DURATION_FRAMES)


# ════════════════════ METRIC CHARTS ════════════════════
def show_scenario_metrics(scenario_key, results):
    sc = SCENARIOS[scenario_key]
    fig, axes = plt.subplots(2, 3, figsize=(17, 10))
    fig.patch.set_facecolor('#1a1a2e')

    bc = sc['banner_color']
    fig.suptitle(
        f"  KET QUA: {sc['name']}  \n{sc['desc']}",
        fontsize=16, fontweight='bold', color='white', y=0.98,
        family=FONT_SANS,
        bbox=dict(boxstyle='round,pad=0.5', facecolor=bc,
                  edgecolor='white', linewidth=2)
    )

    net_types = ['WPAN', 'WLAN', 'WMAN']
    net_colors = ['#ff6b6b', '#51cf66', '#339af0']
    metrics = [
        ('throughput',     'Throughput (pkt/s)', 'Throughput'),
        ('delay',          'Delay TB (ms)',      'Delay Trung Binh'),
        ('pdr',            'PDR (%)',            'Packet Delivery Ratio'),
        ('jitter',         'Jitter (ms)',        'Jitter'),
        ('collision_rate', 'Collision (%)',      'Collision Rate'),
        ('fairness',       "Jain's Index",       "Jain's Fairness Index"),
    ]

    for idx, (key, ylabel, title) in enumerate(metrics):
        r, c = idx // 3, idx % 3
        ax = axes[r][c]
        ax.set_facecolor('#16213e')
        for sp in ax.spines.values():
            sp.set_color('#444')
        ax.tick_params(colors='#ccc')

        vals = [results[nt][key] for nt in net_types]
        bars = ax.bar(net_types, vals, color=net_colors, edgecolor='white',
                      linewidth=1, alpha=0.9, width=0.5)

        max_val = max(vals) if vals else 1
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max_val * 0.03,
                    f'{v:.2f}', ha='center', va='bottom',
                    fontsize=10, fontweight='bold', color='#ffeaa7',
                    family=FONT_SANS)

        ax.set_ylabel(ylabel, fontsize=9, color='#aaa', family=FONT_SANS)
        ax.set_title(title, fontsize=12, fontweight='bold', color='#f8f8f2',
                     family=FONT_SANS)
        ax.grid(axis='y', alpha=0.15, color='#e0e0e0')

    # Table text
    tbl = _build_single_table(scenario_key, results)
    fig.text(0.5, 0.01, tbl, ha='center', va='bottom', fontsize=8,
             family=FONT_MONO, color='#f8f8f2',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f3460',
                       alpha=0.95, edgecolor=bc, linewidth=1.5))

    plt.tight_layout(rect=[0, 0.12, 1, 0.90])
    plt.show()


def _build_single_table(scenario_key, results):
    sc = SCENARIOS[scenario_key]
    h = (f"  {sc['name']} -- {sc['desc']}\n"
         f"+--------+------------+----------+--------+---------+------------+----------+------+------+------+\n"
         f"| Mang   | Throughput | Delay(ms)| PDR(%) | Jitter  | Collision% | Fairness | Gui  | Nhan | Mat  |\n"
         f"+--------+------------+----------+--------+---------+------------+----------+------+------+------+\n")
    rows = ""
    for nt in ['WPAN', 'WLAN', 'WMAN']:
        r = results[nt]
        rows += (f"| {nt:<6} | {r['throughput']:>9.2f}  | {r['delay']:>7.1f}  | "
                 f"{r['pdr']:>5.1f}  | {r['jitter']:>6.1f}  | {r['collision_rate']:>9.1f}  | "
                 f"{r['fairness']:>7.3f}  | {r['sent']:>4}  | {r['received']:>4}  | {r['lost']:>4}  |\n")
    footer = "+--------+------------+----------+--------+---------+------------+----------+------+------+------+"
    return h + rows + footer


def show_comparison(all_results):
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.patch.set_facecolor('#1a1a2e')
    fig.suptitle(
        '  SO SANH TONG HOP 2 KICH BAN  \n'
        'KB1: Tai nhe (it nut, kenh tot)  vs  KB2: Tai nang (nhieu nut, kenh xau)',
        fontsize=15, fontweight='bold', color='white', y=0.98,
        family=FONT_SANS,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#6c5ce7',
                  edgecolor='white', linewidth=2)
    )

    net_types = ['WPAN', 'WLAN', 'WMAN']
    bar_colors = {'light': '#74b9ff', 'heavy': '#fd79a8'}
    x = np.arange(len(net_types))
    w = 0.32

    metrics = [
        ('throughput',     'Throughput (pkt/s)',  'Throughput'),
        ('delay',          'Delay TB (ms)',       'Delay Trung Binh'),
        ('pdr',            'PDR (%)',             'Packet Delivery Ratio'),
        ('jitter',         'Jitter (ms)',         'Jitter'),
        ('collision_rate', 'Collision (%)',       'Collision Rate'),
        ('fairness',       "Jain's Index",        "Jain's Fairness Index"),
    ]

    for idx, (key, ylabel, title) in enumerate(metrics):
        r, c = idx // 3, idx % 3
        ax = axes[r][c]
        ax.set_facecolor('#16213e')
        for sp in ax.spines.values():
            sp.set_color('#444')
        ax.tick_params(colors='#ccc')

        v1 = [all_results['light'][nt][key] for nt in net_types]
        v2 = [all_results['heavy'][nt][key] for nt in net_types]

        b1 = ax.bar(x - w/2, v1, w, label='KB1: Tai nhe',
                     color=bar_colors['light'], edgecolor='white', linewidth=0.8, alpha=0.9)
        b2 = ax.bar(x + w/2, v2, w, label='KB2: Tai nang',
                     color=bar_colors['heavy'], edgecolor='white', linewidth=0.8, alpha=0.9)

        max_v = max(max(v1) if v1 else 0, max(v2) if v2 else 0, 0.01)
        for bar in b1:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + max_v*0.02,
                    f'{h:.2f}', ha='center', va='bottom', fontsize=7.5,
                    color='#74b9ff', fontweight='bold', family=FONT_SANS)
        for bar in b2:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + max_v*0.02,
                    f'{h:.2f}', ha='center', va='bottom', fontsize=7.5,
                    color='#fd79a8', fontweight='bold', family=FONT_SANS)

        ax.set_ylabel(ylabel, fontsize=9, color='#aaa', family=FONT_SANS)
        ax.set_title(title, fontsize=12, fontweight='bold', color='#f8f8f2',
                     family=FONT_SANS)
        ax.set_xticks(x)
        ax.set_xticklabels(net_types, fontsize=10, color='#e0e0e0')
        ax.legend(fontsize=8, loc='best', facecolor='#16213e',
                  edgecolor='#444', labelcolor='#e0e0e0')
        ax.grid(axis='y', alpha=0.15, color='#e0e0e0')

    tbl = _build_comparison_table(all_results)
    fig.text(0.5, 0.01, tbl, ha='center', va='bottom', fontsize=7.5,
             family=FONT_MONO, color='#f8f8f2',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f3460',
                       alpha=0.95, edgecolor='#6c5ce7', linewidth=1.5))

    plt.tight_layout(rect=[0, 0.11, 1, 0.90])
    plt.show()


def show_throughput_over_time(all_results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor('#1a1a2e')
    fig.suptitle('  THROUGHPUT THEO THOI GIAN  ', fontsize=14,
                 fontweight='bold', color='white', family=FONT_SANS,
                 bbox=dict(boxstyle='round,pad=0.4', facecolor='#00b894',
                           edgecolor='white', linewidth=1.5))

    net_colors = {'WPAN': '#ff6b6b', 'WLAN': '#51cf66', 'WMAN': '#339af0'}
    panels = [
        (ax1, 'light', 'KICH BAN 1: TAI NHE\n(it nut - kenh tot - mobility thap)'),
        (ax2, 'heavy', 'KICH BAN 2: TAI NANG\n(nhieu nut - kenh xau - mobility cao)'),
    ]
    for ax, skey, title in panels:
        ax.set_facecolor('#16213e')
        for sp in ax.spines.values():
            sp.set_color('#444')
        ax.tick_params(colors='#ccc')
        for nt in ['WPAN', 'WLAN', 'WMAN']:
            h = all_results[skey][nt]['throughput_history']
            if h:
                t = np.arange(len(h))
                ax.plot(t, h, '-o', color=net_colors[nt], label=nt,
                        ms=4, lw=2, alpha=0.85)
                ax.fill_between(t, h, alpha=0.08, color=net_colors[nt])
        ax.set_xlabel('Time interval (snapshot)', fontsize=10, color='#aaa',
                      family=FONT_SANS)
        ax.set_ylabel('Throughput (pkt/s)', fontsize=10, color='#aaa',
                      family=FONT_SANS)
        ax.set_title(title, fontsize=11, fontweight='bold', color='#f8f8f2',
                     family=FONT_SANS)
        ax.legend(fontsize=9, facecolor='#16213e', edgecolor='#444',
                  labelcolor='#e0e0e0')
        ax.grid(True, alpha=0.15, color='#e0e0e0')

    plt.tight_layout()
    plt.show()


def _build_comparison_table(all_results):
    h = ("  SO SANH 2 KICH BAN: KB1 (Tai nhe)  vs  KB2 (Tai nang)\n"
         "+--------+-----------+------------+----------+--------+---------+------------+----------+\n"
         "| Mang   | Kich ban  | Throughput | Delay(ms)| PDR(%) | Jitter  | Collision% | Fairness |\n"
         "+--------+-----------+------------+----------+--------+---------+------------+----------+\n")
    rows = ""
    for nt in ['WPAN', 'WLAN', 'WMAN']:
        for sk, sn in [('light', 'KB1-Nhe'), ('heavy', 'KB2-Nang')]:
            r = all_results[sk][nt]
            rows += (f"| {nt:<6} | {sn:<9} | {r['throughput']:>9.2f}  | "
                     f"{r['delay']:>7.1f}  | {r['pdr']:>5.1f}  | {r['jitter']:>6.1f}  | "
                     f"{r['collision_rate']:>9.1f}  | {r['fairness']:>7.3f}  |\n")
        rows += "+--------+-----------+------------+----------+--------+---------+------------+----------+\n"
    rows = rows.rsplit('\n', 2)[0] + '\n'
    footer = "+--------+-----------+------------+----------+--------+---------+------------+----------+"
    return h + rows + footer


# ════════════════════ MAIN MENU (Tkinter) ════════════════════
class MainMenu:
    """Cua so menu chinh de chon kich ban mo phong."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mo Phong Mang Khong Day - WPAN / WLAN / WMAN")
        self.root.geometry("700x680")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')

        self.all_results = {}
        self._build_ui()

    def _build_ui(self):
        root = self.root

        # Title
        title_frame = tk.Frame(root, bg='#0f3460', padx=20, pady=15)
        title_frame.pack(fill='x', padx=10, pady=(10, 5))

        tk.Label(title_frame,
                 text="MO PHONG SO SANH MANG KHONG DAY",
                 font=('Helvetica', 18, 'bold'), fg='#ffeaa7', bg='#0f3460'
        ).pack()
        tk.Label(title_frame,
                 text="WPAN / WLAN / WMAN",
                 font=('Helvetica', 14, 'bold'), fg='#74b9ff', bg='#0f3460'
        ).pack()
        tk.Label(title_frame,
                 text="Danh gia dinh luong  |  2 Kich ban  |  6 Metrics",
                 font=('Helvetica', 10), fg='#ddd', bg='#0f3460'
        ).pack(pady=(5, 0))

        # Scenario info
        info_frame = tk.Frame(root, bg='#1a1a2e')
        info_frame.pack(fill='x', padx=10, pady=5)

        # KB1
        kb1_frame = tk.LabelFrame(info_frame, text=" KICH BAN 1: TAI NHE ",
                                   font=('Helvetica', 11, 'bold'),
                                   fg='#00b894', bg='#16213e',
                                   padx=15, pady=10)
        kb1_frame.pack(fill='x', pady=3)
        for line in [
            "- It nut:    WPAN=4, WLAN=5, WMAN=6 clients",
            "- Kenh tot:  loss 2-4%, collision 3-5%",
            "- Mobility:  thap (0.2 - 0.5)",
        ]:
            tk.Label(kb1_frame, text=line, font=('Consolas', 10),
                     fg='#ddd', bg='#16213e', anchor='w').pack(fill='x')

        # KB2
        kb2_frame = tk.LabelFrame(info_frame, text=" KICH BAN 2: TAI NANG ",
                                   font=('Helvetica', 11, 'bold'),
                                   fg='#e17055', bg='#16213e',
                                   padx=15, pady=10)
        kb2_frame.pack(fill='x', pady=3)
        for line in [
            "- Nhieu nut: WPAN=10, WLAN=14, WMAN=16 clients",
            "- Kenh xau:  loss 10-15%, collision 15-20%",
            "- Mobility:  cao (1.5 - 3.0)",
        ]:
            tk.Label(kb2_frame, text=line, font=('Consolas', 10),
                     fg='#ddd', bg='#16213e', anchor='w').pack(fill='x')

        # Metrics info
        met_frame = tk.LabelFrame(info_frame, text=" 6 METRICS DANH GIA ",
                                   font=('Helvetica', 11, 'bold'),
                                   fg='#ffeaa7', bg='#16213e',
                                   padx=15, pady=8)
        met_frame.pack(fill='x', pady=3)
        tk.Label(met_frame,
                 text="Throughput | Delay | PDR | Jitter | Collision Rate | Jain's Fairness",
                 font=('Consolas', 10), fg='#74b9ff', bg='#16213e').pack()

        # Buttons
        btn_frame = tk.Frame(root, bg='#1a1a2e')
        btn_frame.pack(fill='x', padx=20, pady=10)

        btn_style = {
            'font': ('Helvetica', 12, 'bold'),
            'width': 40, 'height': 2,
            'relief': 'raised', 'bd': 2,
            'cursor': 'hand2',
        }

        btn1 = tk.Button(btn_frame,
                         text="[1]  Chay KICH BAN 1: TAI NHE",
                         bg='#00b894', fg='white', activebackground='#00a381',
                         command=self._run_scenario1, **btn_style)
        btn1.pack(pady=4, fill='x')

        btn2 = tk.Button(btn_frame,
                         text="[2]  Chay KICH BAN 2: TAI NANG",
                         bg='#e17055', fg='white', activebackground='#c0392b',
                         command=self._run_scenario2, **btn_style)
        btn2.pack(pady=4, fill='x')

        btn3 = tk.Button(btn_frame,
                         text="[3]  Chay CA 2 KICH BAN + So sanh",
                         bg='#6c5ce7', fg='white', activebackground='#5b4cdb',
                         command=self._run_both, **btn_style)
        btn3.pack(pady=4, fill='x')

        btn4 = tk.Button(btn_frame,
                         text="[4]  Thoat",
                         bg='#636e72', fg='white', activebackground='#555',
                         command=self.root.destroy,
                         font=('Helvetica', 11), width=40, height=1,
                         relief='raised', bd=2, cursor='hand2')
        btn4.pack(pady=(8, 4), fill='x')

        # Status
        self.status_var = tk.StringVar(value="San sang. Chon kich ban de bat dau.")
        self.status_label = tk.Label(root, textvariable=self.status_var,
                                      font=('Consolas', 10), fg='#ffeaa7',
                                      bg='#0f3460', padx=10, pady=6, anchor='w')
        self.status_label.pack(fill='x', padx=10, pady=(0, 10))

    def _set_status(self, text):
        self.status_var.set(text)
        self.root.update()

    def _run_scenario1(self):
        self._set_status("Dang chay Kich ban 1: Tai nhe ...")
        self.root.update()
        sim = ScenarioAnimation('light')
        self.all_results['light'] = sim.run()
        self._set_status("Kich ban 1 hoan thanh! Hien thi ket qua ...")
        self.root.update()
        show_scenario_metrics('light', self.all_results['light'])
        self._set_status("Kich ban 1: Da xong. Chon tiep hoac thoat.")

    def _run_scenario2(self):
        self._set_status("Dang chay Kich ban 2: Tai nang ...")
        self.root.update()
        sim = ScenarioAnimation('heavy')
        self.all_results['heavy'] = sim.run()
        self._set_status("Kich ban 2 hoan thanh! Hien thi ket qua ...")
        self.root.update()
        show_scenario_metrics('heavy', self.all_results['heavy'])
        self._set_status("Kich ban 2: Da xong. Chon tiep hoac thoat.")

    def _run_both(self):
        # KB1
        self._set_status("Dang chay Kich ban 1: Tai nhe ...")
        self.root.update()
        sim1 = ScenarioAnimation('light')
        self.all_results['light'] = sim1.run()
        self._set_status("KB1 xong! Hien thi metric KB1 ...")
        self.root.update()
        show_scenario_metrics('light', self.all_results['light'])

        # KB2
        self._set_status("Dang chay Kich ban 2: Tai nang ...")
        self.root.update()
        sim2 = ScenarioAnimation('heavy')
        self.all_results['heavy'] = sim2.run()
        self._set_status("KB2 xong! Hien thi metric KB2 ...")
        self.root.update()
        show_scenario_metrics('heavy', self.all_results['heavy'])

        # Comparison
        self._set_status("Hien thi bieu do so sanh tong hop ...")
        self.root.update()
        show_comparison(self.all_results)
        show_throughput_over_time(self.all_results)

        self._set_status("Da xong ca 2 kich ban + so sanh! Chon tiep hoac thoat.")

    def run(self):
        self.root.mainloop()


# ════════════════════ MAIN ════════════════════
def main():
    print()
    print("=" * 55)
    print("  MO PHONG MANG KHONG DAY: WPAN / WLAN / WMAN")
    print("  2 Kich ban  |  6 Metrics  |  Menu chon")
    print("=" * 55)
    print()

    menu = MainMenu()
    menu.run()

    print()
    print("=" * 55)
    print("  MO PHONG HOAN TAT!")
    print("=" * 55)
    print()


if __name__ == "__main__":
    main()

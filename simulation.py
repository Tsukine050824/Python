import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np
import random
import collections
import warnings

warnings.filterwarnings('ignore')

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor':   '#F8F9FA',
    'axes.grid':        True,
    'grid.alpha':       0.4,
    'font.family':      'DejaVu Sans',
})

NETWORKS = {
    'WPAN': {'color': '#E74C3C', 'radius': 50,  'speed': 3, 'bw_mbps': 2,  'clients': 6,  'label': 'WPAN\n(Bluetooth/Zigbee)'},
    'WLAN': {'color': '#27AE60', 'radius': 150, 'speed': 6, 'bw_mbps': 54, 'clients': 8,  'label': 'WLAN\n(Wi-Fi 802.11n)'},
    'WMAN': {'color': '#3498DB', 'radius': 300, 'speed': 5, 'bw_mbps': 20, 'clients': 10, 'label': 'WMAN\n(WiMAX)'},
}

CENTERS = {'WPAN': (-400, 0), 'WLAN': (0, 0), 'WMAN': (500, 0)}

SCENARIOS = {
    'light_good': {
        'short':       'S1: Tải nhẹ / Kênh tốt',
        'packet_rate': {'WPAN': 0.10, 'WLAN': 0.12, 'WMAN': 0.08},
        'loss_prob':   {'WPAN': 0.02, 'WLAN': 0.02, 'WMAN': 0.03},
        'speed_scale': 1.0,
        'color':       '#27AE60',
    },
    'heavy_bad': {
        'short':       'S2: Tải nặng / Kênh xấu',
        'packet_rate': {'WPAN': 0.45, 'WLAN': 0.50, 'WMAN': 0.35},
        'loss_prob':   {'WPAN': 0.25, 'WLAN': 0.20, 'WMAN': 0.30},
        'speed_scale': 0.4,
        'color':       '#E74C3C',
    },
}

TOTAL_FRAMES   = 400
HISTORY_WINDOW = 40


class Packet:
    _id = 0

    def __init__(self, source, target, net_type, speed, loss_prob, created_at):
        Packet._id += 1
        self.pid        = Packet._id
        self.source     = np.array(source, dtype=float)
        self.target     = np.array(target, dtype=float)
        self.position   = np.array(source, dtype=float)
        self.net_type   = net_type
        self.speed      = speed
        self.loss_prob  = loss_prob
        self.created_at = created_at
        self.alive      = True
        self.lost       = False
        self.progress   = 0.0
        diff            = self.target - self.source
        self.distance   = max(np.linalg.norm(diff), 1e-9)
        self.direction  = diff / self.distance

    def update(self, speed_scale=1.0):
        if random.random() < self.loss_prob * 0.02:
            self.alive = False
            self.lost  = True
            return
        self.progress += (self.speed * speed_scale) / self.distance
        if self.progress >= 1:
            self.alive    = False
            self.position = self.target.copy()
        else:
            self.position = self.source + self.direction * self.distance * self.progress


def build_nodes():
    nodes = {}
    for net_type, center in CENTERS.items():
        net = NETWORKS[net_type]
        nodes[net_type] = [{'x': center[0], 'y': center[1], 'type': 'router'}]
        for i in range(net['clients']):
            angle = 2 * np.pi * i / net['clients']
            r = net['radius'] * 0.7 * (0.5 + 0.5 * random.random())
            nodes[net_type].append({
                'x': center[0] + r * np.cos(angle),
                'y': center[1] + r * np.sin(angle),
                'type': 'client',
            })
    return nodes


def _make_packet(nodes, net_type, sc, frame):
    nlist = nodes[net_type]
    if len(nlist) < 2:
        return None
    if random.random() < 0.5:
        src, dst = nlist[0], random.choice(nlist[1:])
    else:
        src = random.choice(nlist[1:])
        dst = random.choice([n for n in nlist if n != src])
    return Packet(
        (src['x'], src['y']), (dst['x'], dst['y']),
        net_type, NETWORKS[net_type]['speed'],
        sc['loss_prob'][net_type], frame,
    )


def _init_frame_stats():
    return {nt: {
        'sent': 0, 'recv': 0, 'lost': 0,
        'delays': collections.deque(maxlen=HISTORY_WINDOW),
    } for nt in NETWORKS}


def _record_history(history, cumulative, frame_stats):
    for nt in NETWORKS:
        fs     = frame_stats[nt]
        bw     = NETWORKS[nt]['bw_mbps']
        delays = list(fs['delays'])
        tput   = min((fs['recv'] / max(HISTORY_WINDOW / 30, 1 / 30)) * 1500 * 8 / 1e6, bw)

        history[nt]['sent'].append(cumulative[nt]['sent'])
        history[nt]['recv'].append(cumulative[nt]['recv'])
        history[nt]['lost'].append(cumulative[nt]['lost'])
        history[nt]['delay'].append(np.mean(delays) if delays else 0)
        history[nt]['jitter'].append(np.std(delays) if len(delays) > 1 else 0)
        history[nt]['throughput'].append(tput)

        fs['sent'] = fs['recv'] = fs['lost'] = 0


def run_scenario(scenario_key, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    Packet._id = 0

    sc          = SCENARIOS[scenario_key]
    nodes       = build_nodes()
    history     = {nt: {'sent': [], 'recv': [], 'lost': [], 'delay': [], 'jitter': [], 'throughput': []} for nt in NETWORKS}
    frame_stats = _init_frame_stats()
    cumulative  = {nt: {'sent': 0, 'recv': 0, 'lost': 0} for nt in NETWORKS}
    all_packets = []

    for frame in range(TOTAL_FRAMES):
        for net_type in NETWORKS:
            for _ in range(np.random.poisson(sc['packet_rate'][net_type])):
                p = _make_packet(nodes, net_type, sc, frame)
                if p:
                    all_packets.append(p)
                    frame_stats[net_type]['sent'] += 1
                    cumulative[net_type]['sent']   += 1

        alive = []
        for p in all_packets:
            if not p.alive:
                continue
            p.update(sc['speed_scale'])
            if p.alive:
                alive.append(p)
            else:
                nt = p.net_type
                if p.lost:
                    frame_stats[nt]['lost'] += 1
                    cumulative[nt]['lost']   += 1
                else:
                    frame_stats[nt]['delays'].append((frame - p.created_at + 1) / 30)
                    frame_stats[nt]['recv']  += 1
                    cumulative[nt]['recv']    += 1
        all_packets = alive

        _record_history(history, cumulative, frame_stats)

    return history, cumulative


def compute_summary(history, cumulative):
    result = {}
    for nt in NETWORKS:
        sent    = cumulative[nt]['sent']
        recv    = cumulative[nt]['recv']
        lost    = cumulative[nt]['lost']
        delays  = [d for d in history[nt]['delay']      if d > 0]
        jitters = [j for j in history[nt]['jitter']     if j > 0]
        tputs   = [t for t in history[nt]['throughput'] if t > 0]
        result[nt] = {
            'PDR':           recv / max(sent, 1) * 100,
            'Avg Delay(s)':  np.mean(delays)  if delays  else 0,
            'Jitter(s)':     np.mean(jitters) if jitters else 0,
            'Throughput':    np.mean(tputs)   if tputs   else 0,
            'CollisionRate': lost / max(sent, 1) * 100,
            'Sent': sent, 'Recv': recv, 'Lost': lost,
        }
    return result


def _plot_timeseries(fig, gs, results, sc_keys, nt_colors, time_s):
    metric_rows = [
        ('throughput', 'Throughput (Mbps)'),
        ('delay',      'Avg Delay (giây)'),
        ('jitter',     'Jitter (giây)'),
    ]
    kernel = np.ones(15) / 15
    for col_i, nt in enumerate(NETWORKS):
        for row_i, (metric, ylabel) in enumerate(metric_rows):
            ax = fig.add_subplot(gs[row_i, col_i])
            for sk in sc_keys:
                data   = results[sk][0][nt][metric]
                smooth = np.convolve(data, kernel, mode='same')
                ax.plot(time_s, smooth, color=SCENARIOS[sk]['color'],
                        linewidth=2, label=SCENARIOS[sk]['short'], alpha=0.9)
                ax.fill_between(time_s, 0, smooth, color=SCENARIOS[sk]['color'], alpha=0.08)
            ax.set_title(f'{NETWORKS[nt]["label"].replace(chr(10), " ")} – {ylabel}',
                         fontsize=9, fontweight='bold', color=nt_colors[nt])
            ax.set_xlabel('Thời gian (s)', fontsize=8)
            ax.set_ylabel(ylabel, fontsize=8)
            ax.tick_params(labelsize=7)
            if row_i == 0:
                ax.legend(fontsize=7, loc='upper right')


def _plot_pdr_bar(fig, gs, results, sc_keys, nt_list):
    ax    = fig.add_subplot(gs[3, :])
    x     = np.arange(len(nt_list))
    width = 0.32
    for i, sk in enumerate(sc_keys):
        vals = [results[sk][2][nt]['PDR'] for nt in nt_list]
        bars = ax.bar(x + i * width, vals, width, label=SCENARIOS[sk]['short'],
                      color=SCENARIOS[sk]['color'], alpha=0.85, edgecolor='black', linewidth=0.7)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f'{v:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels([f'{nt}\n{NETWORKS[nt]["label"].split(chr(10))[1]}' for nt in nt_list], fontsize=10)
    ax.set_ylabel('PDR – Tỷ lệ nhận gói (%)', fontsize=11)
    ax.set_title('Tỷ lệ nhận gói (PDR) – So sánh 2 kịch bản', fontsize=13, fontweight='bold', color='#2C3E50')
    ax.set_ylim(0, 115)
    ax.axhline(100, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.legend(fontsize=10)


def _plot_metric_bars(fig, gs, results, sc_keys, nt_list):
    metrics_bar = [
        ('Avg Delay(s)',  'Avg Delay (s)',          'Thời gian trễ trung bình'),
        ('Jitter(s)',     'Jitter (s)',              'Jitter'),
        ('CollisionRate', 'Collision/Loss Rate (%)', 'Collision / Loss Rate'),
    ]
    for col_i, (mk, unit_label, title) in enumerate(metrics_bar):
        ax = fig.add_subplot(gs[4, col_i])
        x  = np.arange(len(nt_list))
        for i, sk in enumerate(sc_keys):
            vals = [results[sk][2][nt][mk] for nt in nt_list]
            bars = ax.bar(x + i * 0.32, vals, 0.32, label=SCENARIOS[sk]['short'],
                          color=SCENARIOS[sk]['color'], alpha=0.85, edgecolor='black', linewidth=0.7)
            for bar, v in zip(bars, vals):
                label = f'{v:.1f}%' if 'Rate' in mk else f'{v:.3f}'
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.02,
                        label, ha='center', va='bottom', fontsize=7.5)
        ax.set_xticks(x + 0.16)
        ax.set_xticklabels(nt_list, fontsize=9)
        ax.set_ylabel(unit_label, fontsize=9)
        ax.set_title(title, fontsize=10, fontweight='bold', color='#2C3E50')
        ax.legend(fontsize=7)


def _plot_table(fig, gs, results, sc_keys, nt_list):
    ax = fig.add_subplot(gs[5, :])
    ax.axis('off')

    col_labels = ['Kịch bản', 'Mạng', 'PDR (%)', 'Avg Delay (s)', 'Jitter (s)',
                  'Throughput (Mbps)', 'Collision Rate (%)', 'Gói gửi', 'Gói nhận', 'Gói mất']
    sc_names = {'light_good': 'S1: Tải nhẹ / Kênh tốt', 'heavy_bad': 'S2: Tải nặng / Kênh xấu'}
    sc_bg    = {'light_good': '#D5F5E3',                 'heavy_bad': '#FADBD8'}

    rows_data, row_colors = [], []
    for sk in sc_keys:
        summ = results[sk][2]
        for j, nt in enumerate(nt_list):
            s = summ[nt]
            rows_data.append([
                sc_names[sk] if j == 0 else '',
                f'{nt}\n({NETWORKS[nt]["label"].split(chr(10))[1]})',
                f'{s["PDR"]:.1f}',
                f'{s["Avg Delay(s)"]:.4f}',
                f'{s["Jitter(s)"]:.4f}',
                f'{s["Throughput"]:.3f}',
                f'{s["CollisionRate"]:.1f}',
                f'{s["Sent"]}', f'{s["Recv"]}', f'{s["Lost"]}',
            ])
            alt = '#F0F0F0' if j % 2 == 0 else 'white'
            row_colors.append([sc_bg[sk]] + [alt] * (len(col_labels) - 1))

    tbl = ax.table(cellText=rows_data, colLabels=col_labels, cellLoc='center',
                   loc='center', cellColours=row_colors)
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1.0, 1.55)
    for (r, c), cell in tbl.get_celld().items():
        if r == 0:
            cell.set_facecolor('#2C3E50')
            cell.set_text_props(color='white', fontweight='bold')
        cell.set_edgecolor('#BDC3C7')
    ax.set_title('BẢNG TỔNG HỢP CÁC CHỈ SỐ HIỆU SUẤT – 2 KỊCH BẢN × 3 MẠNG',
                 fontsize=12, fontweight='bold', color='#2C3E50', pad=12)


def plot_all(results):
    sc_keys   = list(SCENARIOS.keys())
    nt_list   = list(NETWORKS.keys())
    nt_colors = {nt: NETWORKS[nt]['color'] for nt in NETWORKS}
    time_s    = np.arange(TOTAL_FRAMES) / 30

    fig = plt.figure(figsize=(22, 26))
    fig.suptitle(
        'ĐÁNH GIÁ ĐỊNH LƯỢNG – SO SÁNH HAI KỊCH BẢN\nTruyền Gói Tin: WPAN / WLAN / WMAN',
        fontsize=17, fontweight='bold', color='#2C3E50', y=0.98,
    )
    gs = gridspec.GridSpec(6, 3, figure=fig, hspace=0.68, wspace=0.38,
                           top=0.94, bottom=0.04, left=0.07, right=0.97)

    _plot_timeseries(fig, gs, results, sc_keys, nt_colors, time_s)
    _plot_pdr_bar(fig, gs, results, sc_keys, nt_list)
    _plot_metric_bars(fig, gs, results, sc_keys, nt_list)
    _plot_table(fig, gs, results, sc_keys, nt_list)

    patches = [
        mpatches.Patch(color=SCENARIOS[sk]['color'], label=SCENARIOS[sk]['short']) for sk in sc_keys
    ] + [
        mpatches.Patch(color=NETWORKS[nt]['color'], label=nt) for nt in NETWORKS
    ]
    fig.legend(handles=patches, loc='upper right', bbox_to_anchor=(0.98, 0.97),
               fontsize=9, framealpha=0.9)

    out_path = 'network_quantitative_evaluation.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    return out_path


def print_summary(results):
    print("\n=== TÓM TẮT KẾT QUẢ ===")
    for sk, (_, _, summ) in results.items():
        print(f"\n{SCENARIOS[sk]['short']}")
        print(f"{'Mạng':<8} {'PDR%':>7} {'Delay':>9} {'Jitter':>8} {'Tput':>10} {'Loss%':>7}")
        print("-" * 55)
        for nt, s in summ.items():
            print(f"{nt:<8} {s['PDR']:>6.1f}% {s['Avg Delay(s)']:>9.4f} "
                  f"{s['Jitter(s)']:>8.4f} {s['Throughput']:>9.3f}Mbps {s['CollisionRate']:>6.1f}%")


def main():
    scenarios_to_run = {
        'light_good': ('Tải NHẸ – Kênh TỐT', 10),
        'heavy_bad':  ('Tải NẶNG – Kênh XẤU', 10),
    }
    results = {}
    for key, (label, seed) in scenarios_to_run.items():
        print(f"Chạy kịch bản: {label} ...")
        h, c = run_scenario(key, seed=seed)
        results[key] = (h, c, compute_summary(h, c))

    print_summary(results)

    out = plot_all(results)
    print(f"\nBiểu đồ đã lưu: {out}")


if __name__ == '__main__':
    main()
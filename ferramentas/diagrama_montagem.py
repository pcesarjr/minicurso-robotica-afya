import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import matplotlib.patheffects as pe

# ---------- cores por função ----------
C5V, CGND = "#D62728", "#222222"
CSEG, CSR, CSERVO = "#7B3FA0", "#1F77B4", "#FF7F0E"
CBUZ, CLED, CBTN = "#D6619E", "#2CA02C", "#8C564B"
CLDR, CREL = "#13A3B5", "#6B6B6B"

ROWS = {"a": 12, "b": 11, "c": 10, "d": 9, "e": 8, "f": 5, "g": 4, "h": 3, "i": 2, "j": 1,
        "T+": 15, "T-": 14, "B-": -1, "B+": -2}

def H(col, row):
    return (col, ROWS[row])

fig, ax = plt.subplots(figsize=(17, 15.8))
ax.set_xlim(-4, 47.5)
ax.set_ylim(-21.5, 26)
ax.set_aspect("equal")
ax.axis("off")

def wire(pts, color, lw=3.2, z=6):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color="white", lw=lw + 2.6, solid_capstyle="round", solid_joinstyle="round", zorder=z)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", solid_joinstyle="round", zorder=z + 0.1)
    for p in (pts[0], pts[-1]):
        ax.add_patch(Circle(p, 0.17, fc=color, ec="white", lw=0.8, zorder=z + 0.2))

def tag(hole, tpos, label, color, z=8):
    wire([hole, tpos], color, lw=2.6, z=z - 1)
    w = 0.42 * len(label) + 0.5
    ax.add_patch(FancyBboxPatch((tpos[0] - w / 2, tpos[1] - 0.32), w, 0.64,
                                boxstyle="round,pad=0.02,rounding_size=0.25", fc=color, ec="white", lw=1.2, zorder=z))
    ax.text(tpos[0], tpos[1] - 0.02, label, ha="center", va="center", fontsize=10.5, color="white",
            weight="bold", zorder=z + 0.1)

def resistor(p1, p2, valor, z=5, lbl_off=(0, 0.42)):
    (x1, y1), (x2, y2) = p1, p2
    ax.plot([x1, x2], [y1, y2], color="#8A8A8A", lw=2, zorder=z)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    horiz = abs(x2 - x1) >= abs(y2 - y1)
    L = min(1.5, 0.55 * max(abs(x2 - x1), abs(y2 - y1)))
    if horiz:
        ax.add_patch(FancyBboxPatch((mx - L / 2, my - 0.2), L, 0.4, boxstyle="round,pad=0.02,rounding_size=0.18",
                                    fc="#E8D3A8", ec="#9C8456", lw=1, zorder=z + 0.1))
        for k, c in enumerate(["#3B6FD8", "#C9222B", "#7A4A1C"] if valor == "620" else
                                ["#2E8B57", "#3B6FD8", "#7A4A1C"] if valor == "560" else
                                ["#7A4A1C", "#111111", "#C9222B"]):
            ax.add_patch(Rectangle((mx - L / 2 + 0.22 + k * 0.22, my - 0.2), 0.09, 0.4, fc=c, zorder=z + 0.2))
    else:
        ax.add_patch(FancyBboxPatch((mx - 0.2, my - L / 2), 0.4, L, boxstyle="round,pad=0.02,rounding_size=0.18",
                                    fc="#E8D3A8", ec="#9C8456", lw=1, zorder=z + 0.1))
        for k, c in enumerate(["#2E8B57", "#3B6FD8", "#7A4A1C"] if valor == "560" else
                                ["#7A4A1C", "#111111", "#C9222B"]):
            ax.add_patch(Rectangle((mx - 0.2, my + L / 2 - 0.3 - k * 0.22), 0.4, 0.09, fc=c, zorder=z + 0.2))
    ax.text(mx + lbl_off[0], my + lbl_off[1], valor + " Ω", ha="center", va="center", fontsize=7.5,
            color="#5A4A2A", zorder=z + 0.3, path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])

# ================= PROTOBOARD =================
ax.add_patch(FancyBboxPatch((0.15, -2.9), 30.7, 18.8, boxstyle="round,pad=0.05,rounding_size=0.5",
                            fc="#F4F1EA", ec="#BDB6A6", lw=1.5, zorder=1))
ax.add_patch(Rectangle((0.15, 6.15), 30.7, 0.7, fc="#E1DCCF", ec="none", zorder=1.1))
# trilhos
for y, c in [(15.5, C5V), (13.5, "#2A5DB0"), (-0.5, "#2A5DB0"), (-2.5, C5V)]:
    ax.plot([0.7, 30.3], [y, y], color=c, lw=1.6, zorder=1.2)
for y, s, c in [(15, "+", C5V), (14, "−", "#2A5DB0"), (-1, "−", "#2A5DB0"), (-2, "+", C5V)]:
    ax.text(0.45, y, s, ha="center", va="center", fontsize=12, weight="bold", color=c, zorder=1.3)
    ax.text(30.55, y, s, ha="center", va="center", fontsize=12, weight="bold", color=c, zorder=1.3)
# furos
for col in range(1, 31):
    for r, y in ROWS.items():
        ax.add_patch(Rectangle((col - 0.16, y - 0.16), 0.32, 0.32, fc="#9E978A", ec="none", zorder=1.4))
for col in (1, 5, 15, 20, 30):
    ax.text(col, 0.3, str(col), ha="center", va="center", fontsize=7.5, color="#8A8273", zorder=1.5)
for r in "abcdefghij":
    ax.text(0.45 if r not in "ae" else 0.45, ROWS[r], r, ha="center", va="center", fontsize=7.5, color="#8A8273", zorder=1.5)

# ---------- display 7 segmentos (cols 12–16, pinos nas linhas d e h) ----------
ax.add_patch(FancyBboxPatch((11.45, 2.45), 5.1, 7.1, boxstyle="round,pad=0.02,rounding_size=0.2",
                            fc="#2B2B2B", ec="#111111", lw=1.2, zorder=4))
seg = dict(color="#E24A3B", lw=6, solid_capstyle="round", zorder=4.2)
cx, top, mid, bot, L, R = 14, 7.85, 6.0, 4.15, 13.0, 15.0
ax.plot([L + .25, R - .25], [top, top], **seg); ax.plot([L + .25, R - .25], [mid, mid], **seg)
ax.plot([L + .25, R - .25], [bot, bot], **seg)
for x in (L, R):
    ax.plot([x, x], [top - .25, mid + .25], **seg); ax.plot([x, x], [mid - .25, bot + .25], **seg)
ax.add_patch(Circle((15.75, 3.75), 0.18, fc="#E24A3B", zorder=4.2))
for i, (lab, col) in enumerate(zip(["g", "f", "C", "a", "b"], range(12, 17))):
    ax.add_patch(Circle((col, 9), 0.17, fc="#C8C8C8", zorder=4.3))
    ax.text(col, 8.65, lab, ha="center", va="top", fontsize=8.5, color="#FFFFFF", weight="bold", zorder=4.4)
for lab, col in zip(["e", "d", "C", "c", "dp"], range(12, 17)):
    ax.add_patch(Circle((col, 3), 0.17, fc="#C8C8C8", zorder=4.3))
    ax.text(col, 3.35, lab, ha="center", va="bottom", fontsize=8.5, color="#FFFFFF", weight="bold", zorder=4.4)

# resistores 620 Ω do display
resistor(H(12, "a"), H(8, "a"), "620")
resistor(H(13, "b"), H(10, "b"), "620", lbl_off=(0, -0.42))
resistor(H(15, "b"), H(18, "b"), "620", lbl_off=(0, -0.42))
resistor(H(16, "a"), H(20, "a"), "620")
resistor(H(12, "j"), H(8, "j"), "620", lbl_off=(0, 0.45))
resistor(H(13, "i"), H(10, "i"), "620")
resistor(H(15, "i"), H(18, "i"), "620")
# comuns no GND
wire([H(14, "a"), H(14, "T-")], CGND)
wire([H(14, "j"), H(14, "B-")], CGND)
# etiquetas dos segmentos
for col, lab in [(8, "A5"), (10, "A4"), (18, "D3"), (20, "D4")]:
    tag(H(col, "e"), (col, 7.0), lab, CSEG)
for col, lab in [(8, "A3"), (10, "D6"), (18, "D5")]:
    tag(H(col, "f"), (col, 6.0), lab, CSEG)

# ---------- LEDs (anodo col k, catodo col k+1, linha c) ----------
for k, cor, lab in [(22, "#E03131", "D11"), (25, "#2FA84F", "D12"), (28, "#2F6FE0", "D13")]:
    ax.plot([k, k], [10, 10.75], color="#9A9A9A", lw=2, zorder=4)
    ax.plot([k + 1, k + 1], [10, 10.75], color="#9A9A9A", lw=2, zorder=4)
    ax.add_patch(Circle((k + 0.5, 11.15), 0.62, fc=cor, ec="#333333", lw=1, alpha=0.95, zorder=4.2))
    ax.text(k - 0.42, 10.45, "+", ha="center", va="center", fontsize=10, weight="bold", color="#333333", zorder=4.3)
    resistor(H(k + 1, "a"), H(k + 1, "T-"), "560", lbl_off=(0.95, 0))
    tag(H(k, "e"), (k, 7.0), lab, CLED)

# ---------- botão (diagonal: col1 em cima, col3 embaixo) ----------
ax.add_patch(FancyBboxPatch((0.7, 5.25), 2.6, 2.5, boxstyle="round,pad=0.02,rounding_size=0.15",
                            fc="#3A3A3A", ec="#111111", lw=1, zorder=4))
ax.add_patch(Circle((2, 6.5), 0.75, fc="#202020", ec="#5A5A5A", lw=1.2, zorder=4.1))
for p in [H(1, "e"), H(3, "e"), H(1, "f"), H(3, "f")]:
    ax.add_patch(Circle(p, 0.15, fc="#C8C8C8", zorder=4.2))
wire([H(1, "c"), (-1.6, 10)], CBTN, lw=2.6, z=7)
ax.add_patch(FancyBboxPatch((-2.55, 9.68), 1.3, 0.64, boxstyle="round,pad=0.02,rounding_size=0.25",
                            fc=CBTN, ec="white", lw=1.2, zorder=8))
ax.text(-1.9, 9.98, "D2", ha="center", va="center", fontsize=10.5, color="white", weight="bold", zorder=8.1)
wire([H(3, "j"), H(3, "B-")], CGND)

# ---------- LDR (cols 5 e 6, linha g) + divisor 1 kΩ ----------
ax.plot([5, 5.3], [4, 4.6], color="#9A9A9A", lw=2, zorder=4); ax.plot([6, 5.7], [4, 4.6], color="#9A9A9A", lw=2, zorder=4)
ax.add_patch(Circle((5.5, 4.75), 0.45, fc="#E9C46A", ec="#8A6414", lw=1.2, zorder=4.2))
ax.plot([5.2, 5.35, 5.5, 5.65, 5.8], [4.75, 4.95, 4.55, 4.95, 4.75], color="#B5452F", lw=1.3, zorder=4.3)
wire([H(5, "i"), (5, -2)], C5V, lw=2.6)
resistor(H(6, "h"), (6, -1), "1k", lbl_off=(1.0, 0.5))
tag(H(6, "f"), (6, 6.0), "A0", CLDR)

# ---------- buzzer (+ col 22, − col 25, linha g) ----------
ax.plot([22, 22.6], [4, 3.6], color="#9A9A9A", lw=2, zorder=4); ax.plot([25, 24.4], [4, 3.6], color="#9A9A9A", lw=2, zorder=4)
ax.add_patch(Circle((23.5, 3.1), 1.25, fc="#1E1E1E", ec="#000000", lw=1, zorder=4.2))
ax.add_patch(Circle((23.5, 3.1), 0.25, fc="#444444", zorder=4.3))
ax.text(22.55, 4.35, "+", ha="center", va="center", fontsize=10, weight="bold", color="#333333", zorder=4.4)
tag(H(22, "f"), (22, 6.0), "D10", CBUZ)
wire([H(25, "j"), H(25, "B-")], CGND)

# ---------- capacitor 100 µF nos trilhos de cima ----------
ax.plot([2, 2], [15, 16.3], color="#9A9A9A", lw=2, zorder=4)
ax.plot([3, 3], [14, 16.3], color="#9A9A9A", lw=2, zorder=4)
ax.add_patch(FancyBboxPatch((1.55, 16.3), 1.9, 1.7, boxstyle="round,pad=0.02,rounding_size=0.3",
                            fc="#1F3A93", ec="#0F1F55", lw=1, zorder=4.2))
ax.add_patch(Rectangle((2.85, 16.3), 0.6, 1.7, fc="#B8C4E6", zorder=4.3))
ax.text(3.15, 17.15, "−", ha="center", va="center", fontsize=12, weight="bold", color="#0F1F55", zorder=4.4)
ax.text(2.2, 17.15, "100µF", ha="center", va="center", fontsize=6.5, color="white", rotation=90, zorder=4.4)

# ---------- pontes entre trilhos (direita) ----------
wire([H(30, "T+"), (31.9, 15), (31.9, -2), H(30, "B+")], C5V, lw=2.8, z=3)
wire([H(29, "T-"), (31.3, 14), (31.3, -1), H(29, "B-")], CGND, lw=2.8, z=3)

# ================= FORA DA PROTOBOARD =================
# HC-SR04
ax.add_patch(FancyBboxPatch((4.2, 20.6), 7.2, 3.0, boxstyle="round,pad=0.02,rounding_size=0.2",
                            fc="#2D6CB3", ec="#173E6B", lw=1.2, zorder=4))
for cxx in (5.9, 9.7):
    ax.add_patch(Circle((cxx, 22.3), 1.15, fc="#C9CDD2", ec="#7D838A", lw=1.5, zorder=4.1))
    ax.add_patch(Circle((cxx, 22.3), 0.75, fc="#5E646B", zorder=4.2))
ax.text(7.8, 23.25, "HC-SR04", ha="center", va="center", fontsize=9, color="white", weight="bold", zorder=4.3)
hc = {"VCC": 6.3, "Trig": 7.3, "Echo": 8.3, "GND": 9.3}
for lab, x in hc.items():
    ax.text(x, 21.05, lab, ha="center", va="center", fontsize=6.5, color="white", zorder=4.3)
    ax.add_patch(Rectangle((x - 0.13, 20.1), 0.26, 0.5, fc="#C8A84B", zorder=4.3))
wire([(6.3, 20.1), (6.3, 17.6), (5, 17.6), H(5, "T+")], C5V, lw=2.6)
tag((7.3, 20.1), (7.3, 18.9), "D7", CSR)
tag((8.3, 20.1), (8.3, 17.7), "D8", CSR)
wire([(9.3, 20.1), (9.3, 16.6), (8, 16.6), H(8, "T-")], CGND, lw=2.6)

# servo SG90
ax.add_patch(FancyBboxPatch((12.6, 17.0), 5.6, 3.3, boxstyle="round,pad=0.02,rounding_size=0.2",
                            fc="#3C78C9", ec="#1D4580", lw=1.2, zorder=4))
ax.add_patch(Circle((16.6, 20.3), 0.7, fc="#F2F2F2", ec="#9A9A9A", lw=1.2, zorder=4.2))
ax.add_patch(FancyBboxPatch((14.0, 20.05), 5.2, 0.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                            fc="#F2F2F2", ec="#9A9A9A", lw=1, zorder=4.1))
ax.text(15.4, 18.4, "Servo SG90", ha="center", va="center", fontsize=9, color="white", weight="bold", zorder=4.3)
ax.text(16.6, 21.35, "braço", ha="center", va="center", fontsize=7.5, color="#555555", zorder=4.3)
for x, c in [(13.2, "#7A4A1C"), (13.6, C5V), (14.0, CSERVO)]:
    ax.plot([x, x], [17.0, 16.4], color=c, lw=3, zorder=4.1)
wire([(13.2, 16.4), (13.2, 16.0), (11, 16.0), H(11, "T-")], "#7A4A1C", lw=2.6)
wire([(13.6, 16.4), (13.6, 15.75), (12, 15.75), H(12, "T+")], C5V, lw=2.6)
tag((14.0, 16.4), (14.9, 16.4), "D9", CSERVO)
ax.annotate("", xy=(11.2, 21.6), xytext=(14.6, 20.6),
            arrowprops=dict(arrowstyle="->", color="#7A8394", lw=1.5, connectionstyle="arc3,rad=0.3"), zorder=4)
ax.text(14.3, 23.0, "colar o sensor\nno braço do servo", ha="center", va="center", fontsize=8, color="#5B6576", style="italic")

# módulo relé
ax.add_patch(FancyBboxPatch((20.2, 17.0), 6.4, 4.2, boxstyle="round,pad=0.02,rounding_size=0.2",
                            fc="#2D6CB3", ec="#173E6B", lw=1.2, zorder=4))
ax.add_patch(Rectangle((22.4, 18.0), 2.6, 2.4, fc="#1B1B1B", zorder=4.1))
ax.text(23.7, 19.2, "RELÉ", ha="center", va="center", fontsize=8, color="white", weight="bold", zorder=4.2)
ax.add_patch(Rectangle((25.4, 17.6), 1.0, 3.0, fc="#2F8F4E", zorder=4.1))
ax.text(25.9, 21.6, "carga", ha="center", va="center", fontsize=7.5, color="#5B6576", zorder=4.2)
rel = {"VCC": 20.8, "GND": 21.5, "IN": 22.2}
for lab, x in rel.items():
    ax.text(x, 17.5, lab, ha="center", va="center", fontsize=6.3, color="white", rotation=90, zorder=4.3)
    ax.add_patch(Rectangle((x - 0.13, 16.55), 0.26, 0.45, fc="#C8A84B", zorder=4.3))
wire([(20.8, 16.55), (20.8, 16.1), (19, 16.1), H(19, "T+")], C5V, lw=2.6)
wire([(21.5, 16.55), (21.5, 15.75), (21, 15.75), H(21, "T-")], CGND, lw=2.6)
tag((22.2, 16.55), (23.4, 16.2), "A2", CREL)

# ================= ARDUINO UNO =================
AX0, AX1, AY0, AY1 = 4.5, 22.5, -19.0, -5.8
ax.add_patch(FancyBboxPatch((AX0, AY0), AX1 - AX0, AY1 - AY0, boxstyle="round,pad=0.02,rounding_size=0.4",
                            fc="#00878F", ec="#005A60", lw=1.5, zorder=2))
ax.add_patch(Rectangle((AX0 - 1.0, -9.6), 3.0, 2.4, fc="#BFC3C7", ec="#7D838A", lw=1, zorder=2.1))
ax.text(AX0 + 0.5, -8.4, "USB", ha="center", va="center", fontsize=8, color="#333333", zorder=2.2)
ax.add_patch(Rectangle((AX0 - 0.6, -17.3), 2.6, 2.6, fc="#1B1B1B", zorder=2.1))
ax.add_patch(Rectangle((14.5, -15.6), 6.6, 1.6, fc="#1B1B1B", zorder=2.1))
ax.text(10.8, -12.2, "ARDUINO  UNO", ha="center", va="center", fontsize=15, color="white", weight="bold", zorder=2.2)

usados = {"D2": CBTN, "D3": CSEG, "D4": CSEG, "D5": CSEG, "D6": CSEG, "D7": CSR, "D8": CSR, "D9": CSERVO,
          "D10": CBUZ, "D11": CLED, "D12": CLED, "D13": CLED, "A0": CLDR, "A2": CREL, "A3": CSEG,
          "A4": CSEG, "A5": CSEG, "5V": C5V, "GND": CGND}
P = 0.6
top_pins = ["SCL", "SDA", "AREF", "GND", "D13", "D12", "D11", "D10", "D9", "D8"]
top_pins2 = ["D7", "D6", "D5", "D4", "D3", "D2", "D1", "D0"]
xs_top = [8.0 + i * P for i in range(10)] + [8.0 + 10 * P + 0.5 + i * P for i in range(8)]
bot_pins = ["NC", "IOREF", "RST", "3V3", "5V", "GND", "GND", "VIN"]
bot_pins2 = ["A0", "A1", "A2", "A3", "A4", "A5"]
xs_bot = [10.0 + i * P for i in range(8)] + [10.0 + 8 * P + 0.8 + i * P for i in range(6)]
pin_xy = {}
for lab, x in zip(top_pins + top_pins2, xs_top):
    c = usados.get(lab)
    ax.add_patch(Rectangle((x - 0.24, -6.75), 0.48, 0.6, fc=c if c else "#1B1B1B", ec="#000000", lw=0.6, zorder=2.3))
    ax.text(x, -7.0, lab, ha="center", va="top", fontsize=7.5, rotation=90, color="white",
            weight="bold" if c else "normal", zorder=2.4)
for lab, x in zip(bot_pins + bot_pins2, xs_bot):
    c = usados.get(lab) if not (lab == "GND" and x != xs_bot[5]) else None
    ax.add_patch(Rectangle((x - 0.24, -18.6), 0.48, 0.6, fc=c if c else "#1B1B1B", ec="#000000", lw=0.6, zorder=2.3))
    ax.text(x, -17.75, lab, ha="center", va="bottom", fontsize=7.5, rotation=90, color="white",
            weight="bold" if c else "normal", zorder=2.4)
    pin_xy[lab] = pin_xy.get(lab, (x, -18.3))
# 5V e GND do Arduino para os trilhos de baixo
x5, xg = xs_bot[4], xs_bot[5]
wire([(x5, -18.3), (x5, -20.0), (-1.4, -20.0), (-1.4, -2), H(1, "B+")], C5V, lw=3.2, z=3)
wire([(xg, -18.3), (xg, -20.8), (-2.2, -20.8), (-2.2, -1), H(1, "B-")], CGND, lw=3.2, z=3)

ax.text(13.6, -4.6, "Pinos coloridos = usados no robô  ·  as etiquetas na protoboard (D3, A5…) indicam o pino de destino",
        ha="center", va="center", fontsize=8.5, color="#3A4456")

# ================= TÍTULO =================
ax.text(-3.5, 25.2, "Robô Sentinela — diagrama de montagem", ha="left", va="center", fontsize=20,
        weight="bold", color="#14213D")
ax.text(-3.5, 24.1, "Protoboard de 400 pontos · vista de cima · mesma pinagem para os sketches 01 a 04",
        ha="left", va="center", fontsize=11, color="#5B6576")

# ================= LEGENDA =================
LX = 34.0
ax.add_patch(FancyBboxPatch((LX - 0.6, -20.6), 13.9, 43.7, boxstyle="round,pad=0.02,rounding_size=0.4",
                            fc="#FBF9F4", ec="#D8D2C4", lw=1, zorder=1))
y = 22.2
ax.text(LX, y, "Fios por função", fontsize=12.5, weight="bold", color="#14213D", va="center")
itens = [(C5V, "5 V"), (CGND, "GND"), (CSEG, "Display: a→D3  b→D4  c→D5  d→D6\n                e→A3  f→A4  g→A5"),
         (CSR, "HC-SR04: Trig→D7  Echo→D8"), (CSERVO, "Servo (sinal)→D9"), (CBUZ, "Buzzer (+)→D10"),
         (CLED, "LEDs: verm.→D11  verde→D12  azul→D13"), (CBTN, "Botão→D2"), (CLDR, "LDR→A0"), (CREL, "Relé (IN)→A2")]
y -= 1.4
for c, t in itens:
    ax.plot([LX, LX + 1.1], [y, y], color=c, lw=4, solid_capstyle="round")
    ax.text(LX + 1.5, y, t, fontsize=9.3, va="center" if "\n" not in t else "top", color="#3A4456",
            linespacing=1.5) if "\n" not in t else ax.text(LX + 1.5, y + 0.3, t, fontsize=9.3, va="top",
                                                          color="#3A4456", linespacing=1.5)
    y -= 1.85 if "\n" in t else 1.05

y -= 0.6
ax.text(LX, y, "Resistores", fontsize=12.5, weight="bold", color="#14213D", va="center")
for t in ["620 Ω: um por segmento do display (7)", "560 Ω: um por LED, no lado do GND (3)", "1 kΩ: divisor do LDR (1)"]:
    y -= 1.0
    ax.text(LX + 0.2, y, "• " + t, fontsize=9.3, va="center", color="#3A4456")

y -= 1.7
ax.text(LX, y, "Display 7 segmentos (ex.: 5161)", fontsize=12.5, weight="bold", color="#14213D", va="center")
y -= 0.9
dx, dy = LX + 2.0, y - 7.0
ax.add_patch(FancyBboxPatch((dx - 1.4, dy), 6.0, 5.4, boxstyle="round,pad=0.02,rounding_size=0.2", fc="#2B2B2B", zorder=2))
s2 = dict(color="#E24A3B", lw=5, solid_capstyle="round", zorder=2.2)
l2, r2, t2, m2, b2 = dx + 0.6, dx + 2.6, dy + 4.3, dy + 2.7, dy + 1.1
ax.plot([l2 + .2, r2 - .2], [t2, t2], **s2); ax.plot([l2 + .2, r2 - .2], [m2, m2], **s2); ax.plot([l2 + .2, r2 - .2], [b2, b2], **s2)
for x in (l2, r2):
    ax.plot([x, x], [t2 - .2, m2 + .2], **s2); ax.plot([x, x], [m2 - .2, b2 + .2], **s2)
for t, (px, py) in {"a": (1.6, 4.65), "b": (2.95, 3.5), "c": (2.95, 1.9), "d": (1.6, 0.6), "e": (0.25, 1.9),
                     "f": (0.25, 3.5), "g": (1.6, 3.05)}.items():
    ax.text(dx + px, dy + py, t, ha="center", va="center", fontsize=9, color="white", weight="bold", zorder=2.3)
ax.add_patch(Circle((r2 + 0.55, b2 - 0.05), 0.15, fc="#E24A3B", zorder=2.2))
for i, t in enumerate(["g", "f", "C", "a", "b"]):
    ax.text(dx - 1.0 + i * 1.2, dy + 5.85, t, ha="center", va="center", fontsize=9.5, weight="bold", color="#14213D")
for i, t in enumerate(["e", "d", "C", "c", "dp"]):
    ax.text(dx - 1.0 + i * 1.2, dy - 0.45, t, ha="center", va="center", fontsize=9.5, weight="bold", color="#14213D")
ax.text(dx + 5.3, dy + 5.85, "pinos\nde cima", fontsize=8, va="center", color="#5B6576")
ax.text(dx + 5.3, dy - 0.45, "pinos\nde baixo", fontsize=8, va="center", color="#5B6576")
y = dy - 1.6
for t in ["C = comum. Cátodo comum: C no GND.", "Ânodo comum: C no 5V e no código",
          "DISPLAY_ANODO_COMUM = true.", "Confirme os pinos antes (passo 3)."]:
    ax.text(LX + 0.2, y, t, fontsize=9, va="center", color="#3A4456")
    y -= 0.85

y -= 0.7
ax.text(LX, y, "Atenção", fontsize=12.5, weight="bold", color="#B5452F", va="center")
for t in ["Monte tudo com a USB desligada.", "Trilho de dentro (azul) = GND;", "de fora (vermelho) = 5 V.",
          "Capacitor: faixa − no GND.", "LED: perna longa (+) na etiqueta.", "Botão: use pinos em diagonal.",
          "Os jumpers da direita ligam os", "trilhos de cima aos de baixo."]:
    y -= 0.85
    ax.text(LX + 0.2, y, t, fontsize=9, va="center", color="#3A4456")

plt.savefig("img_montagem.png", dpi=170, bbox_inches="tight", facecolor="white")
print("ok")

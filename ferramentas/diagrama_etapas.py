"""Diagramas progressivos da montagem (Parte 1), placa da protoboard e Arduino comentado."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import matplotlib.patheffects as pe
import os

C5V, CGND = "#D62728", "#222222"
CSEG, CSR, CSERVO = "#7B3FA0", "#1F77B4", "#FF7F0E"
CBUZ, CLED, CBTN = "#D6619E", "#2CA02C", "#8C564B"
CLDR, CREL = "#13A3B5", "#6B6B6B"
ROWS = {"a": 12, "b": 11, "c": 10, "d": 9, "e": 8, "f": 5, "g": 4, "h": 3, "i": 2, "j": 1,
        "T+": 15, "T-": 14, "B-": -1, "B+": -2}
OUT = "etapas"
os.makedirs(OUT, exist_ok=True)

ax = None
ZB = 0

def H(col, row):
    return (col, ROWS[row])

def z(v):
    return v + ZB

def wire(pts, color, lw=3.2, zz=6):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color="white", lw=lw + 2.6, solid_capstyle="round", solid_joinstyle="round", zorder=z(zz))
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", solid_joinstyle="round", zorder=z(zz + 0.1))
    for p in (pts[0], pts[-1]):
        ax.add_patch(Circle(p, 0.17, fc=color, ec="white", lw=0.8, zorder=z(zz + 0.2)))

def tag(hole, tpos, label, color, zz=8):
    wire([hole, tpos], color, lw=2.6, zz=zz - 1)
    w = 0.42 * len(label) + 0.5
    ax.add_patch(FancyBboxPatch((tpos[0] - w / 2, tpos[1] - 0.32), w, 0.64,
                                boxstyle="round,pad=0.02,rounding_size=0.25", fc=color, ec="white", lw=1.2, zorder=z(zz)))
    ax.text(tpos[0], tpos[1] - 0.02, label, ha="center", va="center", fontsize=10.5, color="white",
            weight="bold", zorder=z(zz + 0.1))

def tag_at(x, y, label, color, zz=8):
    w = 0.42 * len(label) + 0.5
    ax.add_patch(FancyBboxPatch((x - w / 2, y - 0.32), w, 0.64, boxstyle="round,pad=0.02,rounding_size=0.25",
                                fc=color, ec="white", lw=1.2, zorder=z(zz)))
    ax.text(x, y - 0.02, label, ha="center", va="center", fontsize=10.5, color="white", weight="bold", zorder=z(zz + 0.1))

BANDS = {"620": ["#3B6FD8", "#C9222B", "#7A4A1C"], "560": ["#2E8B57", "#3B6FD8", "#7A4A1C"],
         "1k": ["#7A4A1C", "#111111", "#C9222B"]}

def resistor(p1, p2, valor, lbl_off=(0, 0.42), zz=5):
    (x1, y1), (x2, y2) = p1, p2
    ax.plot([x1, x2], [y1, y2], color="#8A8A8A", lw=2, zorder=z(zz))
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    horiz = abs(x2 - x1) >= abs(y2 - y1)
    L = min(1.5, 0.55 * max(abs(x2 - x1), abs(y2 - y1)))
    if horiz:
        ax.add_patch(FancyBboxPatch((mx - L / 2, my - 0.2), L, 0.4, boxstyle="round,pad=0.02,rounding_size=0.18",
                                    fc="#E8D3A8", ec="#9C8456", lw=1, zorder=z(zz + 0.1)))
        for k, c in enumerate(BANDS[valor]):
            ax.add_patch(Rectangle((mx - L / 2 + 0.22 + k * 0.22, my - 0.2), 0.09, 0.4, fc=c, zorder=z(zz + 0.2)))
    else:
        ax.add_patch(FancyBboxPatch((mx - 0.2, my - L / 2), 0.4, L, boxstyle="round,pad=0.02,rounding_size=0.18",
                                    fc="#E8D3A8", ec="#9C8456", lw=1, zorder=z(zz + 0.1)))
        for k, c in enumerate(BANDS[valor]):
            ax.add_patch(Rectangle((mx - 0.2, my + L / 2 - 0.3 - k * 0.22), 0.4, 0.09, fc=c, zorder=z(zz + 0.2)))
    ax.text(mx + lbl_off[0], my + lbl_off[1], valor + " Ω", ha="center", va="center", fontsize=7.5,
            color="#5A4A2A", zorder=z(zz + 0.3), path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])

# ---------------- base: protoboard ----------------
def protoboard(numeros=True):
    ax.add_patch(FancyBboxPatch((0.15, -2.9), 30.7, 18.8, boxstyle="round,pad=0.05,rounding_size=0.5",
                                fc="#F4F1EA", ec="#BDB6A6", lw=1.5, zorder=1))
    ax.add_patch(Rectangle((0.15, 6.15), 30.7, 0.7, fc="#E1DCCF", ec="none", zorder=1.1))
    for y, c in [(15.5, C5V), (13.5, "#2A5DB0"), (-0.5, "#2A5DB0"), (-2.5, C5V)]:
        ax.plot([0.7, 30.3], [y, y], color=c, lw=1.6, zorder=1.2)
    for y, s, c in [(15, "+", C5V), (14, "−", "#2A5DB0"), (-1, "−", "#2A5DB0"), (-2, "+", C5V)]:
        ax.text(0.45, y, s, ha="center", va="center", fontsize=12, weight="bold", color=c, zorder=1.3)
        ax.text(30.55, y, s, ha="center", va="center", fontsize=12, weight="bold", color=c, zorder=1.3)
    for col in range(1, 31):
        for r, y in ROWS.items():
            ax.add_patch(Rectangle((col - 0.16, y - 0.16), 0.32, 0.32, fc="#9E978A", ec="none", zorder=1.4))
    if numeros:
        for col in (1, 5, 10, 15, 20, 25, 30):
            ax.text(col, 0.3, str(col), ha="center", va="center", fontsize=7.5, color="#8A8273", zorder=1.5)
        for r in "abcdefghij":
            ax.text(0.45, ROWS[r], r, ha="center", va="center", fontsize=7.5, color="#8A8273", zorder=1.5)

# ---------------- grupos de componentes ----------------
def g_alimentacao():
    wire([H(30, "T+"), (31.9, 15), (31.9, -2), H(30, "B+")], C5V, lw=2.8, zz=3)
    wire([H(29, "T-"), (31.3, 14), (31.3, -1), H(29, "B-")], CGND, lw=2.8, zz=3)
    wire([H(1, "B+"), (-0.6, -2), (-0.6, -3.4)], C5V, lw=3.0, zz=6)
    wire([H(1, "B-"), (-1.6, -1), (-1.6, -3.4)], CGND, lw=3.0, zz=6)
    tag_at(-0.3, -4.1, "5V", C5V)
    tag_at(-2.1, -4.1, "GND", CGND)
    ax.text(-1.2, -5.0, "do Arduino", ha="center", va="center", fontsize=8.5, color="#5B6576", zorder=z(8))

def led(k, cor, lab):
    ax.plot([k, k], [10, 10.75], color="#9A9A9A", lw=2, zorder=z(4))
    ax.plot([k + 1, k + 1], [10, 10.75], color="#9A9A9A", lw=2, zorder=z(4))
    ax.add_patch(Circle((k + 0.5, 11.15), 0.62, fc=cor, ec="#333333", lw=1, zorder=z(4.2)))
    ax.text(k - 0.42, 10.45, "+", ha="center", va="center", fontsize=10, weight="bold", color="#333333", zorder=z(4.3))
    resistor(H(k + 1, "a"), H(k + 1, "T-"), "560", lbl_off=(0.95, 0))
    tag(H(k, "e"), (k, 7.0), lab, CLED)

def g_led_verm():
    led(22, "#E03131", "D11")

def g_leds_va():
    led(25, "#2FA84F", "D12")
    led(28, "#2F6FE0", "D13")

def g_botao():
    ax.add_patch(FancyBboxPatch((0.7, 5.25), 2.6, 2.5, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc="#3A3A3A", ec="#111111", lw=1, zorder=z(4)))
    ax.add_patch(Circle((2, 6.5), 0.75, fc="#202020", ec="#5A5A5A", lw=1.2, zorder=z(4.1)))
    for p in [H(1, "e"), H(3, "e"), H(1, "f"), H(3, "f")]:
        ax.add_patch(Circle(p, 0.15, fc="#C8C8C8", zorder=z(4.2)))
    wire([H(1, "c"), (-1.6, 10)], CBTN, lw=2.6, zz=7)
    tag_at(-1.9, 10, "D2", CBTN)
    wire([H(3, "j"), H(3, "B-")], CGND)

def g_buzzer():
    ax.plot([22, 22.6], [4, 3.6], color="#9A9A9A", lw=2, zorder=z(4))
    ax.plot([25, 24.4], [4, 3.6], color="#9A9A9A", lw=2, zorder=z(4))
    ax.add_patch(Circle((23.5, 3.1), 1.25, fc="#1E1E1E", ec="#000000", lw=1, zorder=z(4.2)))
    ax.add_patch(Circle((23.5, 3.1), 0.25, fc="#444444", zorder=z(4.3)))
    ax.text(22.55, 4.35, "+", ha="center", va="center", fontsize=10, weight="bold", color="#333333", zorder=z(4.4))
    tag(H(22, "f"), (22, 6.0), "D10", CBUZ)
    wire([H(25, "j"), H(25, "B-")], CGND)

def g_ldr():
    ax.plot([5, 5.3], [4, 4.6], color="#9A9A9A", lw=2, zorder=z(4))
    ax.plot([6, 5.7], [4, 4.6], color="#9A9A9A", lw=2, zorder=z(4))
    ax.add_patch(Circle((5.5, 4.75), 0.45, fc="#E9C46A", ec="#8A6414", lw=1.2, zorder=z(4.2)))
    ax.plot([5.2, 5.35, 5.5, 5.65, 5.8], [4.75, 4.95, 4.55, 4.95, 4.75], color="#B5452F", lw=1.3, zorder=z(4.3))
    wire([H(5, "i"), (5, -2)], C5V, lw=2.6)
    resistor(H(6, "h"), (6, -1), "1k", lbl_off=(1.0, 0.5))
    tag(H(6, "f"), (6, 6.0), "A0", CLDR)

def g_display():
    ax.add_patch(FancyBboxPatch((11.45, 2.45), 5.1, 7.1, boxstyle="round,pad=0.02,rounding_size=0.2",
                                fc="#2B2B2B", ec="#111111", lw=1.2, zorder=z(4)))
    seg = dict(color="#E24A3B", lw=6, solid_capstyle="round", zorder=z(4.2))
    top, mid, bot, L, R = 7.85, 6.0, 4.15, 13.0, 15.0
    for yy in (top, mid, bot):
        ax.plot([L + .25, R - .25], [yy, yy], **seg)
    for x in (L, R):
        ax.plot([x, x], [top - .25, mid + .25], **seg); ax.plot([x, x], [mid - .25, bot + .25], **seg)
    ax.add_patch(Circle((15.75, 3.75), 0.18, fc="#E24A3B", zorder=z(4.2)))
    for lab, col in zip(["g", "f", "C", "a", "b"], range(12, 17)):
        ax.add_patch(Circle((col, 9), 0.17, fc="#C8C8C8", zorder=z(4.3)))
        ax.text(col, 8.65, lab, ha="center", va="top", fontsize=8.5, color="#FFFFFF", weight="bold", zorder=z(4.4))
    for lab, col in zip(["e", "d", "C", "c", "dp"], range(12, 17)):
        ax.add_patch(Circle((col, 3), 0.17, fc="#C8C8C8", zorder=z(4.3)))
        ax.text(col, 3.35, lab, ha="center", va="bottom", fontsize=8.5, color="#FFFFFF", weight="bold", zorder=z(4.4))
    resistor(H(12, "a"), H(8, "a"), "620")
    resistor(H(13, "b"), H(10, "b"), "620", lbl_off=(0, -0.42))
    resistor(H(15, "b"), H(18, "b"), "620", lbl_off=(0, -0.42))
    resistor(H(16, "a"), H(20, "a"), "620")
    resistor(H(12, "j"), H(8, "j"), "620", lbl_off=(0, 0.45))
    resistor(H(13, "i"), H(10, "i"), "620")
    resistor(H(15, "i"), H(18, "i"), "620")
    wire([H(14, "a"), H(14, "T-")], CGND)
    wire([H(14, "j"), H(14, "B-")], CGND)
    for col, lab in [(8, "A5"), (10, "A4"), (18, "D3"), (20, "D4")]:
        tag(H(col, "e"), (col, 7.0), lab, CSEG)
    for col, lab in [(8, "A3"), (10, "D6"), (18, "D5")]:
        tag(H(col, "f"), (col, 6.0), lab, CSEG)

def g_hcsr04():
    ax.add_patch(FancyBboxPatch((4.2, 20.6), 7.2, 3.0, boxstyle="round,pad=0.02,rounding_size=0.2",
                                fc="#2D6CB3", ec="#173E6B", lw=1.2, zorder=z(4)))
    for cxx in (5.9, 9.7):
        ax.add_patch(Circle((cxx, 22.3), 1.15, fc="#C9CDD2", ec="#7D838A", lw=1.5, zorder=z(4.1)))
        ax.add_patch(Circle((cxx, 22.3), 0.75, fc="#5E646B", zorder=z(4.2)))
    ax.text(7.8, 23.25, "HC-SR04", ha="center", va="center", fontsize=9, color="white", weight="bold", zorder=z(4.3))
    for lab, x in {"VCC": 6.3, "Trig": 7.3, "Echo": 8.3, "GND": 9.3}.items():
        ax.text(x, 21.05, lab, ha="center", va="center", fontsize=6.5, color="white", zorder=z(4.3))
        ax.add_patch(Rectangle((x - 0.13, 20.1), 0.26, 0.5, fc="#C8A84B", zorder=z(4.3)))
    wire([(6.3, 20.1), (6.3, 17.6), (5, 17.6), H(5, "T+")], C5V, lw=2.6)
    tag((7.3, 20.1), (7.3, 18.9), "D7", CSR)
    tag((8.3, 20.1), (8.3, 17.7), "D8", CSR)
    wire([(9.3, 20.1), (9.3, 16.6), (8, 16.6), H(8, "T-")], CGND, lw=2.6)

def g_servo():
    ax.add_patch(FancyBboxPatch((12.6, 17.0), 5.6, 3.3, boxstyle="round,pad=0.02,rounding_size=0.2",
                                fc="#3C78C9", ec="#1D4580", lw=1.2, zorder=z(4)))
    ax.add_patch(Circle((16.6, 20.3), 0.7, fc="#F2F2F2", ec="#9A9A9A", lw=1.2, zorder=z(4.2)))
    ax.add_patch(FancyBboxPatch((14.0, 20.05), 5.2, 0.5, boxstyle="round,pad=0.02,rounding_size=0.2",
                                fc="#F2F2F2", ec="#9A9A9A", lw=1, zorder=z(4.1)))
    ax.text(15.4, 18.4, "Servo SG90", ha="center", va="center", fontsize=9, color="white", weight="bold", zorder=z(4.3))
    for x, c in [(13.2, "#7A4A1C"), (13.6, C5V), (14.0, CSERVO)]:
        ax.plot([x, x], [17.0, 16.4], color=c, lw=3, zorder=z(4.1))
    wire([(13.2, 16.4), (13.2, 16.0), (11, 16.0), H(11, "T-")], "#7A4A1C", lw=2.6)
    wire([(13.6, 16.4), (13.6, 15.75), (12, 15.75), H(12, "T+")], C5V, lw=2.6)
    tag((14.0, 16.4), (14.9, 16.4), "D9", CSERVO)
    ax.annotate("", xy=(11.2, 21.6), xytext=(14.6, 20.6), zorder=z(4),
                arrowprops=dict(arrowstyle="->", color="#7A8394", lw=1.5, connectionstyle="arc3,rad=0.3"))
    ax.text(14.3, 23.0, "colar o sensor\nno braço do servo", ha="center", va="center", fontsize=8,
            color="#5B6576", style="italic", zorder=z(4))
    # capacitor 100 µF
    ax.plot([2, 2], [15, 16.3], color="#9A9A9A", lw=2, zorder=z(4))
    ax.plot([3, 3], [14, 16.3], color="#9A9A9A", lw=2, zorder=z(4))
    ax.add_patch(FancyBboxPatch((1.55, 16.3), 1.9, 1.7, boxstyle="round,pad=0.02,rounding_size=0.3",
                                fc="#1F3A93", ec="#0F1F55", lw=1, zorder=z(4.2)))
    ax.add_patch(Rectangle((2.85, 16.3), 0.6, 1.7, fc="#B8C4E6", zorder=z(4.3)))
    ax.text(3.15, 17.15, "−", ha="center", va="center", fontsize=12, weight="bold", color="#0F1F55", zorder=z(4.4))
    ax.text(2.2, 17.15, "100µF", ha="center", va="center", fontsize=6.5, color="white", rotation=90, zorder=z(4.4))

def g_rele():
    ax.add_patch(FancyBboxPatch((20.2, 17.0), 6.4, 4.2, boxstyle="round,pad=0.02,rounding_size=0.2",
                                fc="#2D6CB3", ec="#173E6B", lw=1.2, zorder=z(4)))
    ax.add_patch(Rectangle((22.4, 18.0), 2.6, 2.4, fc="#1B1B1B", zorder=z(4.1)))
    ax.text(23.7, 19.2, "RELÉ", ha="center", va="center", fontsize=8, color="white", weight="bold", zorder=z(4.2))
    ax.add_patch(Rectangle((25.4, 17.6), 1.0, 3.0, fc="#2F8F4E", zorder=z(4.1)))
    ax.text(25.9, 21.6, "carga", ha="center", va="center", fontsize=7.5, color="#5B6576", zorder=z(4.2))
    for lab, x in {"VCC": 20.8, "GND": 21.5, "IN": 22.2}.items():
        ax.text(x, 17.5, lab, ha="center", va="center", fontsize=6.3, color="white", rotation=90, zorder=z(4.3))
        ax.add_patch(Rectangle((x - 0.13, 16.55), 0.26, 0.45, fc="#C8A84B", zorder=z(4.3)))
    wire([(20.8, 16.55), (20.8, 16.1), (19, 16.1), H(19, "T+")], C5V, lw=2.6)
    wire([(21.5, 16.55), (21.5, 15.75), (21, 15.75), H(21, "T-")], CGND, lw=2.6)
    tag((22.2, 16.55), (23.4, 16.2), "A2", CREL)

ETAPAS = [
    ("e0_alimentacao", [g_alimentacao]),
    ("e1_led", [g_led_verm]),
    ("e2_leds", [g_leds_va]),
    ("e3_botao", [g_botao]),
    ("e4_buzzer", [g_buzzer]),
    ("e5_ldr", [g_ldr]),
    ("e6_display", [g_display]),
    ("e7_hcsr04", [g_hcsr04]),
    ("e8_servo", [g_servo]),
    ("e9_rele", [g_rele]),
]

def nova_fig(alto=True):
    global ax
    fig, ax = plt.subplots(figsize=(14.5, 11.6 if alto else 8.6))
    ax.set_xlim(-3.6, 33.0)
    ax.set_ylim(-5.6, 24.3 if alto else 16.4)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig

def render(nome, antigos, novos):
    global ZB
    alto = any(g in (g_hcsr04, g_servo, g_rele) for g in antigos + novos)
    fig = nova_fig(alto)
    protoboard()
    ZB = 0
    for g in antigos:
        g()
    if novos and antigos:
        ax.add_patch(Rectangle((-4, -6), 38, 31, fc="white", alpha=0.5, ec="none", zorder=9.5))
    ZB = 10 if antigos else 0
    for g in novos:
        g()
    ZB = 0
    fig.savefig(f"{OUT}/{nome}.png", dpi=150, bbox_inches="tight", facecolor="white", pad_inches=0.15)
    plt.close(fig)

feitos = []
for nome, grupos in ETAPAS:
    render(nome, feitos, grupos)
    feitos = feitos + grupos
render("e10_completo", feitos, [])

# ---------------- protoboard explicada ----------------
fig = nova_fig()
ax.set_ylim(-4.2, 17.6)
protoboard()
def faixa(x0, y0, w, h, cor, alpha=0.28):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.02,rounding_size=0.3", fc=cor, ec=cor,
                                lw=2, alpha=alpha, zorder=2))
faixa(0.6, 14.6, 29.8, 0.8, C5V)
faixa(0.6, 13.6, 29.8, 0.8, "#2A5DB0")
faixa(0.6, -1.4, 29.8, 0.8, "#2A5DB0")
faixa(0.6, -2.4, 29.8, 0.8, C5V)
for col, cor in [(6, "#E8A33D"), (7, "#7B3FA0")]:
    faixa(col - 0.4, 7.6, 0.8, 4.8, cor, 0.4)
    faixa(col - 0.4, 0.6, 0.8, 4.8, cor, 0.4)
def nota(x, y, t, cor="#14213D", ha="left"):
    ax.text(x, y, t, ha=ha, va="center", fontsize=11, color=cor, weight="bold", zorder=12,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#D8D2C4"))
nota(9.5, 16.6, "Trilho + (5 V): a linha inteira é um só ponto", C5V)
nota(9.5, 12.5, "← cada coluna de 5 furos (a–e) é um ponto", "#8A5A00")
nota(9.5, 6.5, "Vão central: separa a metade de cima da de baixo", "#5B6576")
nota(9.5, 3.0, "← a–e e f–j da mesma coluna NÃO se ligam", "#7B3FA0")
nota(9.5, -3.4, "Trilhos − (GND) e + (5 V) de baixo", "#2A5DB0")
fig.savefig(f"{OUT}/protoboard.png", dpi=150, bbox_inches="tight", facecolor="white", pad_inches=0.15)
plt.close(fig)

# ---------------- Arduino comentado ----------------
fig, ax = plt.subplots(figsize=(14, 9.5))
ax.set_xlim(-9, 33); ax.set_ylim(-3, 25.5); ax.set_aspect("equal"); ax.axis("off")
X0, X1, Y0, Y1 = 4, 26, 2, 19
ax.add_patch(FancyBboxPatch((X0, Y0), X1 - X0, Y1 - Y0, boxstyle="round,pad=0.02,rounding_size=0.6",
                            fc="#00878F", ec="#005A60", lw=2))
ax.add_patch(Rectangle((X0 - 1.5, 13.0), 4.0, 3.4, fc="#BFC3C7", ec="#7D838A", lw=1.2))
ax.text(X0 + 0.5, 14.7, "USB", ha="center", va="center", fontsize=11, color="#333333", weight="bold")
ax.add_patch(Rectangle((X0 - 1.0, 3.5), 3.6, 3.6, fc="#1B1B1B"))
ax.add_patch(Circle((X0 + 0.8, 5.3), 0.9, fc="#444444"))
ax.add_patch(Rectangle((14.5, 5.2), 9.6, 2.4, fc="#1B1B1B"))
ax.text(19.3, 6.4, "ATmega328P", ha="center", va="center", fontsize=11, color="#DDDDDD", weight="bold")
ax.add_patch(Rectangle((6.8, 16.3), 1.4, 1.4, fc="#C9CDD2", ec="#7D838A"))
ax.add_patch(Circle((7.5, 17.0), 0.45, fc="#C9222B"))
ax.add_patch(Rectangle((12.5, 14.6), 0.8, 0.5, fc="#F2C94C"))
ax.text(13.6, 14.85, "L", fontsize=9, color="white", va="center", weight="bold")
ax.text(12.5, 11.0, "ARDUINO  UNO", fontsize=20, color="white", weight="bold", ha="left", va="center")
P = 0.75
top = ["SCL", "SDA", "AREF", "GND", "13", "12", "~11", "~10", "~9", "8"]
top2 = ["7", "~6", "~5", "4", "~3", "2", "TX 1", "RX 0"]
xt = [9.0 + i * P for i in range(10)] + [9.0 + 10 * P + 0.6 + i * P for i in range(8)]
for lab, x in zip(top + top2, xt):
    ax.add_patch(Rectangle((x - 0.3, 18.0), 0.6, 0.7, fc="#1B1B1B", ec="black", lw=0.6))
    ax.text(x, 17.7, lab, ha="center", va="top", fontsize=8.5, color="white", rotation=90)
bot = ["IOREF", "RST", "3V3", "5V", "GND", "GND", "VIN"]
bot2 = ["A0", "A1", "A2", "A3", "A4", "A5"]
xb = [10.4 + i * P for i in range(7)] + [10.4 + 7 * P + 1.0 + i * P for i in range(6)]
for lab, x in zip(bot + bot2, xb):
    ax.add_patch(Rectangle((x - 0.3, 2.3), 0.6, 0.7, fc="#1B1B1B", ec="black", lw=0.6))
    ax.text(x, 3.3, lab, ha="center", va="bottom", fontsize=8.5, color="white", rotation=90)

def callout(xy, txy, t, cor="#14213D", ha="left"):
    ax.annotate(t, xy=xy, xytext=txy, fontsize=11.5, color=cor, ha=ha, va="center", weight="bold",
                arrowprops=dict(arrowstyle="-", color="#7A8394", lw=1.4),
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#D8D2C4"))
callout((12.0, 18.9), (2.5, 23.4), "Pinos digitais 0–13 (entrada ou saída, 0 V / 5 V)", ha="left")
callout((15.0, 18.9), (17.5, 22.2), "~ = também faz PWM", "#8A5A00", ha="left")
callout((21.4, 18.9), (25.3, 21.0), "0 e 1: serial da USB\n(deixe livres)", "#B5452F", ha="left")
callout((X0 - 1.5, 14.7), (-8.6, 14.7), "USB: energia +\nprogramação + Serial", ha="left")
callout((X0 - 1.0, 5.3), (-8.6, 5.3), "Fonte externa\n7 a 12 V", ha="left")
callout((7.5, 17.0), (-0.5, 20.6), "Reset", ha="left")
callout((12.9, 14.6), (13.5, 12.9), "LED interno (pino 13)", "#8A5A00", ha="left")
callout((12.6, 2.3), (6.0, -1.7), "Alimentação: 5V, 3V3 e GND", C5V, ha="left")
callout((19.6, 2.3), (19.0, -1.7), "Analógicos A0–A5 (0 a 1023)\ntambém servem como digitais", CLDR, ha="left")
callout((24.1, 6.4), (27.2, 9.6), "Microcontrolador\n16 MHz · 32 KB · 2 KB", ha="left")
fig.savefig(f"{OUT}/arduino.png", dpi=150, bbox_inches="tight", facecolor="white", pad_inches=0.15)
plt.close(fig)
print("ok", sorted(os.listdir(OUT)))

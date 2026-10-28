import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

NAVY, GOLD, CINZA = "#1F3864", "#B58B2C", "#F2F2F2"

def caixa(ax, x, y, w, h, titulo, sub="", cor=NAVY, fundo="white"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fundo, ec=cor, lw=2))
    ax.text(x, y + (0.3 if "\n" in sub else 0.15) if sub else y, titulo, ha="center", va="center", fontsize=11, weight="bold", color=cor)
    if sub:
        ax.text(x, y - 0.2, sub, ha="center", va="center", fontsize=8.5, color="#333333")

def seta(ax, a, b, texto="", cor="#444444", rad=0.0, dy=0.12):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16, lw=1.6, color=cor,
                                 connectionstyle=f"arc3,rad={rad}"))
    if texto:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + dy, texto, ha="center", va="center", fontsize=8.5,
                color=cor, bbox=dict(fc="white", ec="none", pad=1))

# ---------- 1. Pipeline de ML ----------
fig, ax = plt.subplots(figsize=(12.5, 2.6)); ax.set_xlim(0, 12.5); ax.set_ylim(0, 2.2); ax.axis("off")
etapas = [("HC-SR04", "lê distância\na cada 50 ms"), ("Janela", "20 leituras\n(1 segundo)"),
          ("6 features", "média, desvio,\nmín, máx,\ninclinação, trocas"),
          ("Modelo", "árvore de decisão\nif/else em C\n(modelo.h)"), ("Classe 0–3", "parado, aproximar,\nafastar, acenar"),
          ("Reação", "servo, buzzer,\nLEDs, relé")]
xs = [1.0 + i * 2.1 for i in range(6)]
for i, (t, s) in enumerate(etapas):
    caixa(ax, xs[i], 1.1, 1.8, 1.35, t, s, cor=GOLD if i == 3 else NAVY, fundo="#FFF4DE" if i == 3 else "white")
    if i: seta(ax, (xs[i - 1] + 0.92, 1.1), (xs[i] - 0.92, 1.1))
ax.text(xs[3], 0.25, "treinada no Colab, executada no Arduino", ha="center", fontsize=8.5, color=GOLD, style="italic")
plt.savefig("img_pipeline.png", dpi=200, bbox_inches="tight"); plt.close()

# ---------- 2. Máquina de estados ----------
fig, ax = plt.subplots(figsize=(10.5, 4.6)); ax.set_xlim(0, 10.6); ax.set_ylim(0, 4.6); ax.axis("off")
caixa(ax, 1.55, 2.4, 2.2, 1.1, "PATRULHA", "display P · LED verde\nservo varre 20°–160°")
caixa(ax, 5.8, 2.4, 2.4, 1.1, "ATENÇÃO", "display A · LED vermelho\nclassifica a cada 1 s",
      cor=GOLD, fundo="#FFF4DE")
caixa(ax, 9.1, 4.0, 2.1, 0.85, "ALARME", "sirene + relé")
caixa(ax, 9.1, 2.4, 2.1, 0.85, "AMIGO", "cabeça acena\n+ melodia")
caixa(ax, 9.1, 0.8, 2.1, 0.85, "TCHAU", "bip descendente")
seta(ax, (2.7, 2.6), (4.55, 2.6), "alvo < 40 cm", dy=0.18)
seta(ax, (4.55, 2.15), (2.7, 2.15), "ninguém por 3 janelas", dy=-0.25)
seta(ax, (7.05, 2.8), (8.0, 3.85), "1 APROXIMAR", rad=-0.2, dy=0.05)
seta(ax, (7.05, 2.4), (8.0, 2.4), "3 ACENAR", dy=0.17)
seta(ax, (7.05, 2.0), (8.0, 0.95), "2 AFASTAR", rad=0.2, dy=-0.05)
seta(ax, (8.0, 4.25), (5.3, 2.97), "volta à atenção", rad=0.3, dy=0.75)
seta(ax, (8.0, 0.6), (1.55, 1.84), "volta a patrulhar", rad=-0.25, dy=-0.35)
ax.text(10.25, 2.4, "→ patrulha", ha="left", va="center", fontsize=8.5, color="#444444")
ax.text(5.8, 1.6, "0 PARADO: continua vigiando", ha="center", fontsize=8.5, color="#444444")
plt.savefig("img_estados.png", dpi=200, bbox_inches="tight"); plt.close()
print("ok")

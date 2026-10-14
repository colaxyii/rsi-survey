"""Schematic of the chronological near/far protocol in "Prediction Is Not Memory"."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch, Rectangle

mpl.rcParams["font.sans-serif"] = ["Hiragino Sans GB", "Heiti SC", "DejaVu Sans"]
mpl.rcParams["axes.unicode_minus"] = False

GREY, ORANGE, GREEN, PURPLE, BLUE, RED = (
    "#b9b7ae", "#BD6245", "#437426", "#725299", "#3266AD", "#A73D39")

fig, ax = plt.subplots(figsize=(11.0, 3.5))
ax.set_xlim(-0.4, 10.6)
ax.set_ylim(-1.5, 2.1)
ax.axis("off")

blocks = [
    (0.2, 3.4, GREY, "历史 $H_u$", "决策时可作特征"),
    (3.8, 1.0, ORANGE, "$c_u$", "待决策"),
    (5.0, 1.6, GREEN, "近未来 $N_u$", "弱监督标签"),
    (6.8, 3.0, PURPLE, "远未来 $F_u$", "只用于评估"),
]
for x, w, col, name, sub in blocks:
    ax.add_patch(FancyBboxPatch((x, 0.15), w, 0.9, boxstyle="round,pad=0.06",
                                fc=col, ec="none", alpha=.92))
    ax.text(x + w / 2, 0.72, name, ha="center", va="center", color="white", fontsize=13)
    ax.text(x + w / 2, -0.12, sub, ha="center", va="top", color="#3d3d3a", fontsize=10.5)
    ax.text(x + w / 2, -0.55, "", ha="center")

for x0, x1 in [(3.6, 3.8), (4.8, 5.0), (6.6, 6.8)]:
    ax.annotate("", xy=(x1, 0.6), xytext=(x0, 0.6),
                arrowprops=dict(arrowstyle="-|>", color="#73726c", lw=1.4))

ax.annotate("", xy=(9.9, 1.55), xytext=(0.2, 1.55),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6))
ax.text(0.2, 1.68, "决策时可用的信息（写入闸门的特征只能来自这里）", color=BLUE, fontsize=10.5)

ax.plot([6.7, 6.7], [0.05, 0.95], color=RED, lw=1.6, ls="--")
ax.text(6.78, 1.0, "远未来不参与模型选择", color=RED, fontsize=10.5, ha="left", va="bottom")

ax.annotate("", xy=(9.9, -1.05), xytext=(5.0, -1.05),
            arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1.6))
ax.text(5.0, -1.35, "评估：写入 $c_u$ 之后，$A(p'(w),F_u)$ 是否低于 $A(p(H_u),F_u)$",
        color=PURPLE, fontsize=10.5)

ax.text(0.2, -1.35, "监督：$y^{near}_u=1[A(p'(1),N_u)< A(p(H_u),N_u)]$",
        color=GREEN, fontsize=10.5)

fig.tight_layout()
fig.savefig("fig-protocol.png", dpi=190)
print("saved fig-protocol.png")

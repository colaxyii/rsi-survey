"""Two-dimensional sketch of one profile write (Paper: Prediction Is Not Memory, Fig. 1 context).

Uses the paper's update rule
    p'(w) = norm( (|H| * ebar(H) + w * e(c)) / (|H| + w) )
on a constructed 2-D example so every number in the figure can be recomputed by hand.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl

RED, ORANGE, GREEN, PURPLE, BLUE, CYAN = (
    "#A73D39", "#BD6245", "#437426", "#725299", "#3266AD", "#327A7D")

mpl.rcParams["font.sans-serif"] = ["Hiragino Sans GB", "Heiti SC", "DejaVu Sans"]
mpl.rcParams["axes.unicode_minus"] = False


def unit(deg):
    r = np.deg2rad(deg)
    return np.array([np.cos(r), np.sin(r)])


def mean_dir(degs):
    v = np.mean([unit(d) for d in degs], axis=0)
    return v / np.linalg.norm(v), np.linalg.norm(v)


def write(hist_degs, cand_deg, w=1.0):
    """Return unnormalized mean history, normalized base profile, updated profile, and |H|."""
    h = np.mean([unit(d) for d in hist_degs], axis=0)
    n = len(hist_degs)
    base = h / np.linalg.norm(h)
    upd = (n * h + w * unit(cand_deg)) / (n + w)
    return h, base, upd / np.linalg.norm(upd)


def align(p, degs):
    m, _ = mean_dir(degs)
    return float(np.dot(p, m))


HIST = [0, 10, -10, 5, -5, 15]          # durable history, |H| = 6
FAR = [40, 45, 35, 50]                   # far-future window F_u
CASES = [                                # (candidate, near window, panel title)
    (45, [15, 20, 10], "(a) 安全写入：候选与长期画像同向"),
    (-70, [-55, -65, -70], "(b) 有害写入：候选只被近期情境支持"),
]

fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.0))

for ax, (cand, NEAR, title) in zip(axes, CASES):
    h, base, upd = write(HIST, cand)
    H = np.array([unit(d) for d in HIST])
    N, _ = mean_dir(NEAR)
    F, _ = mean_dir(FAR)
    c = unit(cand)

    ax.scatter(H[:, 0], H[:, 1], s=42, c="#b9b7ae", zorder=3, label="历史交互 $H_u$")
    ax.scatter(*N, s=150, marker="s", c=GREEN, zorder=4, label="近未来质心 $p(N_u)$")
    ax.scatter(*F, s=150, marker="D", c=PURPLE, zorder=4, label="远未来质心 $p(F_u)$")
    ax.scatter(*c, s=150, marker="*", c=ORANGE, zorder=5, label="候选交互 $e(c_u)$")
    ax.scatter(*base, s=170, c=BLUE, zorder=5, label="写入前画像 $p(H_u)$")
    ax.scatter(*upd, s=170, facecolors="none", edgecolors=CYAN, linewidths=2.4,
               zorder=5, label="写入后画像 $p'(1)$")
    ax.annotate("", xy=upd, xytext=base,
                arrowprops=dict(arrowstyle="-|>", color=CYAN, lw=2.0))

    for p, col, ls in ((base, BLUE, "-"), (upd, CYAN, "--")):
        ax.plot([p[0], F[0]], [p[1], F[1]], color=col, ls=ls, lw=1.2, alpha=.75)

    a0, a1 = align(base, FAR), align(upd, FAR)
    ax.set_title(title, fontsize=12)
    ax.text(0.03, 0.03,
            f"$A(p(H_u),F_u)$ = {a0:.3f}\n$A(p'(1),F_u)$ = {a1:.3f}\n"
            f"远未来对齐 {'上升' if a1 > a0 else '下降'} {abs(a1-a0):.3f}",
            transform=ax.transAxes, fontsize=10.5, va="bottom",
            color=GREEN if a1 > a0 else RED,
            bbox=dict(fc="white", ec="#deddd8", boxstyle="round,pad=0.45"))
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(t), np.sin(t), color="#deddd8", lw=1, zorder=1)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.set_aspect("equal")
    ax.set_xlabel("维度 1")
    ax.set_ylabel("维度 2")
    ax.grid(alpha=.25, lw=.6)

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=6, fontsize=10, frameon=False)
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig("fig-write-geometry.png", dpi=190)

print("near label check (y_near = 1 iff writing hurts near alignment)")
for cand, NEAR, name in ((45, [15, 20, 10], "safe"), (-70, [-55, -65, -70], "risk")):
    _, base, upd = write(HIST, cand)
    an0, an1 = align(base, NEAR), align(upd, NEAR)
    af0, af1 = align(base, FAR), align(upd, FAR)
    print(f"  {name:5s} cand={cand:4d}  near {an0:.3f}->{an1:.3f} (label={int(an1<an0)})"
          f"   far {af0:.3f}->{af1:.3f} (hurt={int(af1<af0)})")
    c = unit(cand)
    long_s = float(np.dot(c, base))
    short_s = float(np.dot(c, mean_dir(NEAR)[0]))
    print(f"        cand-long={long_s:.3f}  cand-short={short_s:.3f}  gap={short_s-long_s:+.3f}")

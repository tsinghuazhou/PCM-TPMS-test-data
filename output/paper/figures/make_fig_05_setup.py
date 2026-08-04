import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "stix"

OUT = "output/paper/figures/fig_05_setup"


def ring_points(n, r, jitter=0.0):
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False) + np.pi / n
    pts = np.stack([r * np.cos(ang), r * np.sin(ang)], axis=1)
    if jitter:
        pts += np.random.default_rng(7).normal(0, jitter, pts.shape)
    return pts


fig, ax = plt.subplots(figsize=(3.4, 3.4))

R = 1.0
outer = plt.Circle((0, 0), R, fill=False, lw=1.5, ec="#333333")
ax.add_patch(outer)
ax.annotate(
    "",
    xy=(0, 0.72),
    xytext=(0, -0.72),
    arrowprops=dict(arrowstyle="<->", lw=0.8, color="#333333"),
)
ax.text(0.14, 0.0, r"$r_{\mathrm{out}}$", fontsize=9, va="center")

ax.add_patch(plt.Circle((0, 0), 0.20, fc="#C44E52", ec="k", lw=1.0))
ax.text(0, 0.16, "heater", ha="center", va="bottom", fontsize=8)

rA, rB, rC = 0.32, 0.52, 0.72
ptsA = ring_points(1, rA)
ptsB = ring_points(4, rB, jitter=0.02)
ptsC = ring_points(4, rC, jitter=0.02)

for pts, lab, col in [(ptsA, "A", "#1F77B4"), (ptsB, "B", "#2CA02C"), (ptsC, "C", "#9467BD")]:
    for i, (x, y) in enumerate(pts):
        ax.plot(x, y, "o", ms=5, mfc=col, mec="k", mew=0.4, zorder=3)
        ax.annotate(
            r"$T_%d$" % (["A", "B", "C"].index(lab) * 4 + 1 + (0 if lab == "A" else i)),
            (x, y),
            textcoords="offset points",
            xytext=(4, 4),
            fontsize=7,
        )

for r, lab in [(rA, "Group A"), (rB, "Group B"), (rC, "Group C")]:
    ax.add_patch(plt.Circle((0, 0), r, fill=False, ls="--", lw=0.7, ec="#666666"))
    ax.text(0, -r, lab, ha="center", va="top", fontsize=8, color="#555555")

ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect("equal")
ax.set_axis_off()
ax.set_title("Cross-section: sensor groups", fontsize=10)

fig.savefig(OUT + ".png", dpi=300)
fig.savefig(OUT + ".pdf")
print("saved", OUT)

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from skimage import measure

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "stix"

OUT = "output/paper/figures/fig_04_tpms_setup"


def level_set(name, x, y, z):
    if name == "gyroid":
        return (
            np.sin(x) * np.cos(y)
            + np.sin(y) * np.cos(z)
            + np.sin(z) * np.cos(x)
        )
    if name == "primitive":
        return np.cos(x) + np.cos(y) + np.cos(z)
    if name == "iwp":
        c = np.cos
        return (
            2 * (c(x) * c(y) + c(y) * c(z) + c(z) * c(x))
            - (c(2 * x) + c(2 * y) + c(2 * z))
        )
    raise ValueError(name)


def tpms_mesh(name, n=80, iso=0.0, span=2 * np.pi):
    t = np.linspace(0, span, n)
    x, y, z = np.meshgrid(t, t, t, indexing="ij")
    v = level_set(name, x, y, z)
    verts, faces, _, _ = measure.marching_cubes(v, iso, spacing=(span / n,) * 3)
    return verts, faces


def plot_tpms(ax, name, color="#C44E52"):
    verts, faces = tpms_mesh(name)
    ax.add_collection3d(
        Poly3DCollection(
            verts[faces],
            facecolor=color,
            edgecolor="none",
            alpha=0.85,
            linewidths=0,
        )
    )
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(0, 2 * np.pi)
    ax.set_zlim(0, 2 * np.pi)
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=25, azim=-60)


fig = plt.figure(figsize=(7.0, 3.4))
fig.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.02, wspace=0.05)

names = [("gyroid", "Gyroid"), ("primitive", "Primitive (P)"), ("iwp", "IWP")]
for i, (key, label) in enumerate(names):
    ax = fig.add_subplot(1, 3, i + 1, projection="3d")
    plot_tpms(ax, key)
    ax.set_title(label, fontsize=11)

fig.savefig(OUT + ".png", dpi=300)
fig.savefig(OUT + ".pdf")
print("saved", OUT)

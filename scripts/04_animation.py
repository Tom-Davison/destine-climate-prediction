"""Animate 24 hours of a heatwave day over the Rome region."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib

matplotlib.use("Agg")
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.animation as manim
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation

from destine_risk import config, polytope

OUT = Path(__file__).resolve().parents[1] / "figures" / "diurnal_heat.gif"
OUTLINE = [pe.withStroke(linewidth=2.5, foreground="black")]

lon, lat, tc = polytope.region("future", "20450825", "0000/to/2300")  # (24, points)
tri = Triangulation(lon, lat)
levels = np.arange(8, 47, 1.0)

fig = plt.figure(figsize=(7.6, 5.0))
ax = fig.add_axes([0.01, 0.01, 0.85, 0.98], projection=ccrs.PlateCarree())
ax.set_extent(config.REGION_EXTENT, crs=ccrs.PlateCarree())
cax = fig.add_axes([0.88, 0.06, 0.025, 0.88])

ocean = cfeature.OCEAN.with_scale("10m")
coast = cfeature.COASTLINE.with_scale("10m")
ax.plot(config.LON, config.LAT, "*", ms=16, mfc="#7CFC00", mec="black", zorder=6)

seed = ax.tricontourf(tri, tc[0], levels=levels, cmap="inferno", extend="both")
cb = fig.colorbar(seed, cax=cax)
cb.set_label("2 m temperature (°C)")
clock = ax.text(0.03, 0.05, "", transform=ax.transAxes, color="white",
                fontsize=13, fontweight="bold", zorder=7, path_effects=OUTLINE)
state = {"cf": seed}


def draw(i):
    state["cf"].remove()
    state["cf"] = ax.tricontourf(tri, tc[i], levels=levels, cmap="inferno",
                                 extend="both", zorder=1)
    ax.add_feature(ocean, facecolor="#0b132b", zorder=2)
    ax.add_feature(coast, lw=1.0, edgecolor="white", zorder=3)
    clock.set_text(f"{(i + 2) % 24:02d}:00")
    return []


anim = manim.FuncAnimation(fig, draw, frames=tc.shape[0], interval=200)
OUT.parent.mkdir(exist_ok=True)
anim.save(OUT, writer=manim.PillowWriter(fps=5), dpi=110)
print("Wrote", OUT)

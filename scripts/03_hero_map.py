"""High-res temperature map of the Rome region at the hottest modelled hour."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib

matplotlib.use("Agg")
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation

from destine_risk import config, polytope

OUT = Path(__file__).resolve().parents[1] / "figures" / "hero_map.png"
OUTLINE = [pe.withStroke(linewidth=2.5, foreground="black")]

lon, lat, tc = polytope.region("future", "20450825", "1200")  # 14:00 local
tri = Triangulation(lon, lat)

fig = plt.figure(figsize=(8.5, 5.6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent(config.REGION_EXTENT, crs=ccrs.PlateCarree())

levels = np.arange(np.floor(tc.min()), np.ceil(tc.max()) + 1, 0.5)
cf = ax.tricontourf(tri, tc, levels=levels, cmap="inferno", extend="both")
ax.add_feature(cfeature.OCEAN.with_scale("10m"), facecolor="#0b132b", zorder=2)
ax.coastlines("10m", lw=1.1, color="white", zorder=3)

ax.plot(config.LON, config.LAT, "*", ms=18, mfc="#7CFC00", mec="black", mew=1.1,
        zorder=5)
ax.text(config.LON + 0.07, config.LAT + 0.04, "vineyard", color="white",
        fontsize=11, fontweight="bold", zorder=5, path_effects=OUTLINE)
ax.plot(12.50, 41.90, "o", ms=6, mfc="white", mec="black", zorder=5)
ax.text(12.44, 41.95, "ROME", color="white", fontsize=11, ha="right",
        fontweight="bold", zorder=5, path_effects=OUTLINE)

cb = fig.colorbar(cf, ax=ax, shrink=0.85, pad=0.02)
cb.set_label("2 m temperature (°C)")

OUT.parent.mkdir(exist_ok=True)
fig.savefig(OUT, dpi=170, bbox_inches="tight", pad_inches=0.05)
print("Wrote", OUT)

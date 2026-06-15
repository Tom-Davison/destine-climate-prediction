"""Count hot days per year, baseline vs future, and plot the comparison."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from destine_risk import analysis, config, polytope

FIGURES = Path(__file__).resolve().parents[1] / "figures"
BASE = config.WINDOWS["baseline"]["label"]
FUT = config.WINDOWS["future"]["label"]
COOL, HOT = "#2c7fb8", "#e6320f"

plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold"})


def kde(samples, grid, bw=1.2):
    u = (grid[None, :] - samples[:, None]) / bw
    return np.exp(-0.5 * u ** 2).sum(0) / (len(samples) * bw * np.sqrt(2 * np.pi))


def plot_counts(base, fut):
    cols = base.columns.tolist()
    x = np.arange(len(cols))
    fig, ax = plt.subplots(figsize=(8.5, 5.4))
    b1 = ax.bar(x - 0.19, base.mean(), 0.38, yerr=base.std(), capsize=4,
                label=BASE, color=COOL, edgecolor="white", zorder=3)
    b2 = ax.bar(x + 0.19, fut.mean(), 0.38, yerr=fut.std(), capsize=4,
                label=FUT, color=HOT, edgecolor="white", zorder=3)
    ax.bar_label(b1, fmt="%.0f", padding=3, color="0.3")
    ax.bar_label(b2, fmt="%.0f", padding=3, color="0.3")
    for xi, col in zip(x, cols):
        if base[col].mean() > 0:
            ax.annotate(f"×{fut[col].mean() / base[col].mean():.1f}",
                        (xi + 0.19, fut[col].mean() + fut[col].std()),
                        textcoords="offset points", xytext=(0, 16), ha="center",
                        fontsize=12, fontweight="bold", color=HOT)
    ax.set_xticks(x, [f"above {c[1:]}" for c in cols])
    ax.set_ylabel("Days per year")
    ax.legend(title="Period", frameon=False, loc="upper right")
    ax.grid(axis="y", color="0.9", zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.margins(y=0.22)
    fig.savefig(FIGURES / "hot_days_comparison.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def plot_distribution(base_daily, fut_daily):
    b, f = base_daily.values, fut_daily.values
    grid = np.linspace(np.floor(min(b.min(), f.min())), np.ceil(max(b.max(), f.max())), 400)
    kb, kf = kde(b, grid), kde(f, grid)
    fig, ax = plt.subplots(figsize=(8.5, 5.4))
    ax.fill_between(grid, kb, color=COOL, alpha=0.35)
    ax.fill_between(grid, kf, color=HOT, alpha=0.35)
    ax.fill_between(grid[grid >= 35], kf[grid >= 35], color=HOT, alpha=0.55)
    ax.plot(grid, kb, color=COOL, lw=2, label=BASE)
    ax.plot(grid, kf, color=HOT, lw=2, label=FUT)
    top = max(kb.max(), kf.max())
    for thr in config.THRESHOLDS:
        ax.axvline(thr, color="0.45", ls="--", lw=1)
        ax.text(thr, top * 1.02, f"{thr}°C", ha="center", color="0.35")
    ax.set_ylim(0, top * 1.12)
    ax.set_xlabel("Daily maximum 2 m temperature (°C)")
    ax.set_ylabel("Probability density")
    ax.legend(title="Period", frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(FIGURES / "distribution_shift.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


base_daily = analysis.daily_max(polytope.window_series("baseline"))
fut_daily = analysis.daily_max(polytope.window_series("future"))
base_counts = analysis.hot_day_counts(base_daily, config.THRESHOLDS)
fut_counts = analysis.hot_day_counts(fut_daily, config.THRESHOLDS)

print(f"\n{BASE} baseline:\n{base_counts}")
print(f"\n{FUT} future:\n{fut_counts}")
print("\nmean days/year:")
for col in base_counts.columns:
    bm, fm = base_counts[col].mean(), fut_counts[col].mean()
    print(f"  {col}: {bm:.1f} -> {fm:.1f}")

FIGURES.mkdir(exist_ok=True)
plot_counts(base_counts, fut_counts)
plot_distribution(base_daily, fut_daily)
print("\nWrote figures/hot_days_comparison.png and figures/distribution_shift.png")

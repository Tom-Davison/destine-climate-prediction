import pandas as pd


def daily_max(hourly_c):
    return hourly_c.resample(time="1D").max()


def hot_day_counts(daily_c, thresholds=(30, 35, 40)):
    """Days per year above each threshold. Rows are years, columns thresholds."""
    years = daily_c["time"].dt.year
    counts = {f">{t}C": (daily_c > t).groupby(years).sum().to_series()
              for t in thresholds}
    df = pd.DataFrame(counts)
    df.index.name = "year"
    return df

"""Climate DT retrieval via Polytope (server-side extraction, so no global downloads)."""

import warnings
from pathlib import Path

import numpy as np
import xarray as xr

from . import config
from .polytope_auth import ensure_key

ADDRESS = "polytope.lumi.apps.dte.destination-earth.eu"
DATA = Path(__file__).resolve().parents[2] / "data"

BASE = {"class": "d1", "dataset": "climate-dt", "generation": "2", "model": "ICON",
        "expver": "0001", "realization": "1", "levtype": "sfc", "stream": "clte",
        "type": "fc", "param": "167", "resolution": "high"}


def _fetch(window, extra):
    ensure_key()
    import earthkit.data
    w = config.WINDOWS[window]
    request = {**BASE, "activity": w["activity"], "experiment": w["experiment"], **extra}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        src = earthkit.data.from_source(
            "polytope", "destination-earth", request, address=ADDRESS, stream=False)
        return src.to_xarray()


def point_series(window, year):
    """Hourly 2 m temperature (°C) at the vineyard for one year, cached to NetCDF."""
    cache = DATA / f"{window}_{year}.nc"
    if cache.exists():
        return xr.open_dataarray(cache)

    ds = _fetch(window, {
        "date": f"{year}0101/to/{year}1231", "time": "0000/to/2300",
        "feature": {"type": "timeseries", "points": [[config.LAT, config.LON]],
                    "time_axis": "date"}})
    da = ds["2t"].squeeze(drop=True).rename({"t": "time"}) - 273.15
    if da.size < 8000:
        raise ValueError(f"{window} {year}: only {da.size} hours returned; "
                         "the data is incomplete for this year.")
    da = da.rename("tmax_c")
    cache.parent.mkdir(exist_ok=True)
    da.to_netcdf(cache)
    return da


def window_series(window):
    years = config.WINDOWS[window]["years"]
    return xr.concat([point_series(window, y) for y in years], "time").sortby("time")


def region(window, date, time):
    """2 m temperature (°C) over the map region. Returns (lon, lat, values)."""
    ds = _fetch(window, {"date": date, "time": time,
                         "feature": {"type": "boundingbox", "points": config.REGION_BBOX}})
    lon = np.asarray(ds["longitude"].values).ravel()
    lat = np.asarray(ds["latitude"].values).ravel()
    values = np.asarray(ds["2t"].squeeze().values) - 273.15
    return lon, lat, values

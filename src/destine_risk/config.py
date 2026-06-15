import os

from dotenv import load_dotenv

load_dotenv()

DESP_USERNAME = os.environ.get("DESP_USERNAME")
DESP_PASSWORD = os.environ.get("DESP_PASSWORD")

STAC_URL = "https://hda.data.destination-earth.eu/stac/v2"

# Vineyard near Frascati.
LAT, LON = 41.80, 12.68
THRESHOLDS = (30, 35, 40)

# Baseline comes from the historical run (ends 2014); the future from the SSP3-7.0
# projection. The projection is advertised to 2049 but high-res ICON data actually
# stops in early 2047, so the window ends at 2046.
WINDOWS = {
    "baseline": {"activity": "baseline", "experiment": "hist",
                 "years": range(2010, 2015), "label": "2010–2014"},
    "future": {"activity": "projections", "experiment": "SSP3-7.0",
               "years": range(2042, 2047), "label": "2042–2046"},
}

# Map region for the hero image and animation.
REGION_BBOX = [[42.7, 11.1], [40.5, 14.4]]   # [[N, W], [S, E]]
REGION_EXTENT = [11.1, 14.4, 40.5, 42.7]      # lon_min, lon_max, lat_min, lat_max

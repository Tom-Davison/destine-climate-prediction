# Frascati hot-day risk from the DestinE Climate DT

How many days a year cross 30/35/40 °C at a vineyard near Frascati, now versus
mid-century, using the Destination Earth Climate Change Adaptation Digital Twin.

It pulls hourly 2 m temperature at ~5 km for the cell over the vineyard, takes the
daily maximum, and compares a 2010–2014 baseline against a 2042–2046 SSP3-7.0
projection. It also renders a temperature map of the Rome region and a 24-hour
animation of a heatwave day.

You need a Destination Earth Platform account with Climate DT access (the
`DPAD_Direct_Access` role). Without it the requests authenticate but return nothing.

## Setup

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add your DESP username and password
```

## Run

```
python scripts/01_discover.py     # list the Climate DT collections
python scripts/02_hot_days.py     # hot-day counts + the two charts
python scripts/03_hero_map.py     # temperature map of the Rome region
python scripts/04_animation.py    # 24-hour animation of a heatwave day
```

Scripts 03 and 04 use cartopy, which downloads coastlines. On a python.org build you
may first need:

```
export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
```

Figures are written to `figures/`.

## Caveats

One grid cell, one model (ICON), one scenario; the baseline is the model's own
historical run, not observations. Contains modified Destination Earth data (CC-BY-4.0).

"""Authenticate, check Climate DT access, and list the digital-twin collections."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import destinelab
import pystac_client

from destine_risk import config

auth = destinelab.AuthHandler(config.DESP_USERNAME, config.DESP_PASSWORD)
token = auth.get_token()
print("Authenticated.")
print("Climate DT access:", auth.is_DTaccess_allowed(token))

catalog = pystac_client.Client.open(config.STAC_URL,
                                    headers={"Authorization": f"Bearer {token}"})

for collection in catalog.get_collections():
    blob = f"{collection.id} {collection.title or ''}".lower()
    if "climate" in blob or "dt_" in blob:
        print(collection.id)

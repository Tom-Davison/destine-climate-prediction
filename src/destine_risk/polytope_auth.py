"""Get a Polytope API key into ~/.polytopeapirc using DESP credentials."""

import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from lxml import html

from . import config

IAM = "https://auth.destine.eu/realms/desp/protocol/openid-connect"
CLIENT_ID = "polytope-api-public"
SERVICE = "https://polytope.lumi.apps.dte.destination-earth.eu/"
RC = Path.home() / ".polytopeapirc"


def ensure_key(force=False):
    if RC.exists() and not force:
        return RC
    if not config.DESP_USERNAME or not config.DESP_PASSWORD:
        raise RuntimeError("Set DESP_USERNAME and DESP_PASSWORD in .env")

    with requests.Session() as s:
        page = s.get(f"{IAM}/auth", params={
            "client_id": CLIENT_ID, "redirect_uri": SERVICE,
            "scope": "openid offline_access", "response_type": "code"})
        form_action = html.fromstring(page.content).forms[0].action
        login = s.post(form_action, allow_redirects=False, data={
            "username": config.DESP_USERNAME, "password": config.DESP_PASSWORD})
        if login.status_code != 302:
            raise RuntimeError("Polytope login failed; check DESP credentials.")
        code = parse_qs(urlparse(login.headers["Location"]).query)["code"][0]

    token = requests.post(f"{IAM}/token", data={
        "client_id": CLIENT_ID, "redirect_uri": SERVICE, "code": code,
        "grant_type": "authorization_code", "scope": ""})
    token.raise_for_status()
    RC.write_text(json.dumps({"user_key": token.json()["refresh_token"]}))
    return RC

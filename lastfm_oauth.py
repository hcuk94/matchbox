#!/usr/bin/env python3

import hashlib
import importlib.util
from pathlib import Path
import sys
import urllib.parse
import webbrowser

import requests


API_URL = "https://ws.audioscrobbler.com/2.0/"
AUTH_URL = "https://www.last.fm/api/auth/"


def load_config():
    config_path = Path(__file__).resolve().with_name("config.py")
    spec = importlib.util.spec_from_file_location("config", config_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load config.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_api_sig(params, api_secret):
    payload = "".join(
        "{}{}".format(key, value)
        for key, value in sorted(params.items())
        if key not in ("format", "callback")
    )
    return hashlib.md5((payload + api_secret).encode("utf-8")).hexdigest()


def call_lastfm_api(method, api_key, api_secret, extra_params=None):
    params = {
        "method": method,
        "api_key": api_key,
        "format": "json",
    }
    if extra_params:
        params.update(extra_params)

    params["api_sig"] = build_api_sig(params, api_secret)
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    payload = response.json()
    if "error" in payload:
        raise RuntimeError(
            "Last.fm API error {}: {}".format(
                payload["error"], payload.get("message", "Unknown error")
            )
        )
    return payload


def main():
    try:
        config = load_config()
        lastfm_config = config.providers_notify["LastFM"]["config"]
        api_key = lastfm_config["api_key"]
        api_secret = lastfm_config["api_secret"]
    except FileNotFoundError:
        print("config.py was not found. Copy config_sample.py to config.py first.", file=sys.stderr)
        return 1
    except KeyError as exc:
        print("Missing LastFM config value: {}".format(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        print("Failed to load config.py: {}".format(exc), file=sys.stderr)
        return 1

    if not api_key or not api_secret:
        print("Set providers_notify['LastFM']['config']['api_key'] and ['api_secret'] in config.py first.", file=sys.stderr)
        return 1

    try:
        token_payload = call_lastfm_api("auth.getToken", api_key, api_secret)
        token = token_payload["token"]
    except Exception as exc:
        print("Failed to get request token: {}".format(exc), file=sys.stderr)
        return 1

    auth_url = "{}?{}".format(
        AUTH_URL,
        urllib.parse.urlencode({"api_key": api_key, "token": token}),
    )

    print("Open this URL and authorize MatchBox with Last.fm:")
    print(auth_url)
    print("")

    try:
        opened = webbrowser.open(auth_url)
    except Exception:
        opened = False

    if opened:
        print("A browser window was opened for authorization.")
    else:
        print("A browser window could not be opened automatically.")

    try:
        input("Press Enter after you have approved access in the browser...")
    except EOFError:
        print("No interactive input available. Re-run this script in a terminal after approving access.", file=sys.stderr)
        return 1

    try:
        session_payload = call_lastfm_api(
            "auth.getSession",
            api_key,
            api_secret,
            {"token": token},
        )
    except Exception as exc:
        print("Failed to exchange token for a session key: {}".format(exc), file=sys.stderr)
        return 1

    session = session_payload["session"]
    print("")
    print("Authorization complete.")
    print("Last.fm user: {}".format(session["name"]))
    print("Session key: {}".format(session["key"]))
    print("")
    print("Set providers_notify['LastFM']['config']['session_key'] in config.py to:")
    print("'{}'".format(session["key"]))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pathlib
import requests

BASE = "https://termine.staedteregion-aachen.de"
STEP2_URL = BASE + "/auslaenderamt/select2?md=1"
SUGGEST_URL = BASE + "/auslaenderamt/suggest"

LOCATION_URL = (
    BASE
    + "/auslaenderamt/location"
    + "?mdt=95&select_cnc=1"
    + "&cnc-354=0&cnc-355=0&cnc-351=0&cnc-356=0&cnc-343=0&cnc-353=0&cnc-349=0"
    + "&cnc-359=0&cnc-341=0&cnc-361=0&cnc-367=0&cnc-342=0&cnc-358=0&cnc-368=0"
    + "&cnc-340=0&cnc-345=0&cnc-344=1&cnc-347=0&cnc-350=0&cnc-346=0&cnc-338=0"
    + "&cnc-339=0&cnc-348=0&cnc-360=0&cnc-352=0"
)

NO_APPOINTMENT_NEEDLE = "Für die aktuelle Anliegenauswahl ist leider kein Termin verfügbar"

STATE_PATH = pathlib.Path(".state/last_status.txt")

def make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    })
    s.cookies.set("tvo_language", "de_DE", domain="termine.staedteregion-aachen.de", path="/")
    s.cookies.set("tvo_cookie_accept", "1", domain="termine.staedteregion-aachen.de", path="/")
    return s

def classify(html: str) -> str:
    if "Kein freier Termin verfügbar" in html or NO_APPOINTMENT_NEEDLE in html:
        return "NO_APPOINTMENT"
    if "Terminvorschläge" in html or "suggestion_form" in html or "calendar" in html:
        return "APPOINTMENT_FLOW"
    return "UNKNOWN"

def check() -> tuple[bool, str]:
    """
    returns: (has_appointment, class)
    """
    s = make_session()

    r = s.get(STEP2_URL, timeout=30)
    r.raise_for_status()

    r = s.get(LOCATION_URL, timeout=30, headers={"Referer": STEP2_URL})
    r.raise_for_status()

    form = {"loc": "50", "gps_lat": "50.77858", "gps_long": "6.07867", "select_location": "Weiter"}
    r = s.post(
        LOCATION_URL,
        data=form,
        timeout=30,
        allow_redirects=False,
        headers={"Referer": LOCATION_URL, "Origin": BASE},
    )
    print("POST status =", r.status_code, "Location =", r.headers.get("Location", ""))

    r = s.get(SUGGEST_URL, timeout=30, headers={"Referer": LOCATION_URL})
    r.raise_for_status()

    html = r.text
    cls = classify(html)
    has_appointment = (cls != "NO_APPOINTMENT")
    return has_appointment, cls

def telegram_send(text: str) -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=20)
    resp.raise_for_status()

def read_last() -> str:
    if STATE_PATH.exists():
        return STATE_PATH.read_text(encoding="utf-8").strip()
    return "UNKNOWN"

def write_last(value: str) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(value, encoding="utf-8")

def main() -> int:
    try:
        has_appointment, cls = check()
    except Exception as e:
        print("[error]", repr(e))
        # istersen burada Telegram'a hata mesajı da atarız (şimdilik sadece log)
        return 2

    current = "APPOINTMENT_POSSIBLE" if has_appointment else "NO_APPOINTMENT"
    last = read_last()

    print("class =", cls)
    print("last =", last)
    print("current =", current)

    # sadece durum değişince mesaj
    if current != last and has_appointment:
        telegram_send(
            "🟢 Termin olabilir!\n"
            "Hemen kontrol et:\n"
            "https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1"
        )

    write_last(current)
    print("has_appointment =", has_appointment)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

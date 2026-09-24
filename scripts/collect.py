#!/usr/bin/env python3
"""
Collecteur d'affluence — Calicéo Versailles Saint-Cyr-l'École.

Rôle unique de ce script : lire le pourcentage "Affluence en direct" affiché
sur https://saintcyrlecole.caliceo.com/ et l'ajouter à data/readings.csv,
UNIQUEMENT pendant les heures d'ouverture des Bains. En dehors de ces
heures, il ne fait rien et l'affiche clairement ("Aucune action nécessaire.").

Il n'invente jamais de valeur : en cas d'échec de lecture, il enregistre une
ligne de statut "error" (avec le pourcentage vide) plutôt que de deviner.
"""

import csv
import re
import sys
from datetime import datetime, time as dtime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

URL = "https://saintcyrlecole.caliceo.com/"
PARIS = ZoneInfo("Europe/Paris")
CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "readings.csv"
CSV_HEADER = ["timestamp_paris", "date", "jour", "heure", "type_jour", "pourcentage", "statut"]

JOURS_FR = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

# Fenêtre de collecte : de 10h30 jusqu'à 30 min avant l'évacuation des Bains
# (fermeture 22h dimanche->jeudi, 23h vendredi/samedi ; évacuation 15 min
# avant la fermeture). Marge de sécurité supplémentaire de 15 min.
WINDOW_START = dtime(10, 30)
WINDOW_END_NORMAL = dtime(21, 30)   # dimanche, lundi, mardi, mercredi, jeudi
WINDOW_END_LATE = dtime(22, 30)     # vendredi, samedi


def collection_window(now: datetime) -> tuple[dtime, dtime]:
    weekday = now.weekday()  # 0 = lundi ... 6 = dimanche
    is_late_night = weekday in (4, 5)  # vendredi, samedi
    end = WINDOW_END_LATE if is_late_night else WINDOW_END_NORMAL
    return WINDOW_START, end


def in_window(now: datetime) -> bool:
    start, end = collection_window(now)
    return start <= now.time() <= end


def read_affluence() -> tuple[str | None, str]:
    """Retourne (pourcentage_ou_None, statut)."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(URL, wait_until="domcontentloaded", timeout=45000)

            pattern = re.compile(r"Affluence en direct\s*:\s*(\d{1,3})\s*%")

            last_value = None
            stable_count = 0
            value = None
            for _ in range(12):  # jusqu'à ~12s d'attente/lecture stabilisée
                page.wait_for_timeout(1000)
                content = page.content()
                match = pattern.search(content)
                if not match:
                    continue
                current = match.group(1)
                if current == last_value:
                    stable_count += 1
                    if stable_count >= 2:
                        value = current
                        break
                else:
                    stable_count = 0
                last_value = current

            browser.close()

            if value is None:
                if last_value is not None:
                    # On n'a jamais eu deux lectures identiques d'affilée,
                    # mais on a au moins une lecture : on la garde, en la
                    # signalant comme non confirmée par stabilité.
                    return last_value, "non_stabilise"
                return None, "erreur_lecture"

            pct = int(value)
            if not (0 <= pct <= 100):
                return None, "erreur_valeur_hors_limites"

            if pct == 0:
                return str(pct), "suspect_zero"

            return str(pct), "ok"

    except Exception as exc:  # noqa: BLE001
        print(f"Erreur lors de la lecture du site : {exc}", file=sys.stderr)
        return None, "erreur_technique"


def append_row(now: datetime, pct: str | None, statut: str) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    is_new = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(CSV_HEADER)
        writer.writerow([
            now.strftime("%Y-%m-%d %H:%M"),
            now.strftime("%Y-%m-%d"),
            JOURS_FR[now.weekday()],
            now.strftime("%H:%M"),
            "week-end" if now.weekday() in (5, 6) else "semaine",
            pct if pct is not None else "",
            statut,
        ])


def main() -> None:
    now = datetime.now(PARIS)

    if not in_window(now):
        print(f"Hors des heures de collecte ({now.strftime('%A %H:%M')} Paris). "
              f"Aucune action nécessaire.")
        return

    pct, statut = read_affluence()
    append_row(now, pct, statut)
    print(f"Relevé enregistré : {now.strftime('%Y-%m-%d %H:%M')} Paris -> "
          f"{pct if pct is not None else 'N/A'}% (statut: {statut})")


if __name__ == "__main__":
    main()

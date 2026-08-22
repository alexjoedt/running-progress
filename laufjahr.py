#!/usr/bin/env python3
"""Laufjahr-Dashboard aus einem Garmin-CSV-Export erzeugen.

Aufruf: python3 laufjahr.py running.csv [-o laufjahr.html] [--no-open]
"""
import argparse
import csv
import json
import re
import sys
import webbrowser
from pathlib import Path


def _num(s):
    s = (s or '').strip("' ")
    if s in ('', '--'):
        return None
    try:
        return float(s.replace(',', ''))
    except ValueError:
        return None


def _pace(s):
    m = re.fullmatch(r'(\d+):(\d{2})', (s or '').strip())
    return int(m[1]) * 60 + int(m[2]) if m else None


def _dur(s):
    parts = (s or '').split(':')
    if len(parts) != 3:
        return None
    try:
        h, m, sec = (float(p) for p in parts)
    except ValueError:
        return None
    return h * 3600 + m * 60 + sec


TYPES = [
    ('Basis', 'Basis'),
    ('Schwelle', 'Schwelle'),
    ('Sprint|Anaerob|Tempo', 'Intervall'),
    ('Lang|Long', 'Lang'),
    ('Erholung|Recovery', 'Erholung'),
]


def parse(path):
    rows = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            km = _num(r.get('Distanz'))
            if km is None:
                continue
            if km > 100:  # Bahnläufe stehen in Metern ("6,810")
                km /= 1000
            title = r.get('Titel', '')
            typ = next((t for pat, t in TYPES if re.search(pat, title)), 'Sonstige')
            tm = 1 if 'Laufband' in r.get('Aktivitätstyp', '') else 0
            time_s = _dur(r.get('Zeit'))
            hr = _num(r.get('Ø Herzfrequenz'))
            ef = None
            if not tm and time_s and hr:
                ef = round(km * 1000 / (time_s / 60) / hr, 3)
            rows.append([
                r.get('Datum', '')[:10], typ, tm, round(km, 2), time_s, hr,
                _pace(r.get('Ø Pace')), _num(r.get('Ø Leistung')),
                _num(r.get('Ø Schrittfrequenz (Laufen)')), _num(r.get('Ø Schrittlänge')),
                _num(r.get('Ø Bodenkontaktzeit')), ef, title,
            ])
    rows.sort(key=lambda x: x[0])
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('csv', help='Garmin-Export (Aktivitäten-CSV)')
    ap.add_argument('-o', '--out', default='laufjahr.html', help='Ziel-HTML (Standard: laufjahr.html)')
    ap.add_argument('--no-open', action='store_true', help='Browser nicht öffnen')
    a = ap.parse_args()

    rows = parse(a.csv)
    if not rows:
        sys.exit('Keine Läufe in der CSV gefunden.')

    tpl = Path(__file__).with_name('template.html').read_text(encoding='utf-8')
    out = Path(a.out)
    out.write_text(tpl.replace('/*DATA*/[]', json.dumps(rows, ensure_ascii=False)), encoding='utf-8')
    print(f'{len(rows)} Läufe → {out}')
    if not a.no_open:
        webbrowser.open(out.resolve().as_uri())


if __name__ == '__main__':
    main()

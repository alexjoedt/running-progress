# Laufjahr

Dashboard aus einem Garmin CSV Export. Zeigt Pace, Laufeffizienz, Leistung, Wochenvolumen, Schrittlänge und Bodenkontaktzeit.

## Nutzung

```
python3 laufjahr.py running.csv
```

Erzeugt `laufjahr.html` und öffnet sie im Browser.

Optionen:

```
-o pfad.html    anderes Ziel
--no-open       Browser nicht öffnen
```

## Dateien

- `laufjahr.py` parst die CSV, nur Python Stdlib
- `template.html` enthält die Ansicht, das Skript setzt die Daten ein
- `running.csv` Garmin Export (Aktivitäten als CSV exportieren)

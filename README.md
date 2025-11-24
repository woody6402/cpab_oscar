# CPAP → OSCAR → Home Assistant Workflow

## 1. OSCAR installieren
OSCAR ist ein Open-Source-Tool zur Auswertung von CPAP-Daten.

Download: https://www.sleepfiles.com/OSCAR/

Nach der Installation:
- Benutzer anlegen
- Gerätetyp „ResMed AirSense“ auswählen

## 2. Daten vom AirSense 10 einlesen
1. Gerät ausschalten  
2. SD-Karte entnehmen  
3. In PC stecken  
4. in OSCAR importieren

## 3. CSV aus OSCAR exportieren
OSCAR → Daten → Export → CSV  
Datei z. B. `oscar_export.csv` speichern.

## 4. Importdatei für Home Assistant erzeugen
Script `genHAimport.py` nutzen.  
(Auszug siehe Repository.)

Ausführen:
```
python3 genHAimport.py
```

Output:
`oscar_import_sleep_ahi_6m.tsv`

## 5. Import Statistics (HACS)
1. GITHUB   
2. „Import Statistics“ suchen 
3. In HomeAssistant installieren & neu starten

## 6. Home Assistant Template-Sensoren
In deinem `cpap.yaml` package (Erstellen der Sensoren und Vorbelegen mit 0, Werte werden über import nachgespielt)
```
template:
  - sensor:
      - name: "Sleep Total Time"
        unique_id: sleep_total_time
        unit_of_measurement: "h"
        device_class: duration
        state_class: measurement
        state: 0

      - name: "Sleep AHI"
        unique_id: sleep_ahi
        unit_of_measurement: "events/h"
        state_class: measurement
        state: 0
```

## 7. Daten importieren
In HA → Entwicklerwerkzeuge → Dienste  
Service: `import_statistics.import_from_file`

Beispiel:
```
timezone_identifier: Europe/Vienna
delimiter: "\t"
decimal: false
filename: /config/oscar_import_sleep_ahi_6m.tsv
```

## 8. Statistik löschen (optional)
```
statistics.delete:
  statistic_id: sensor.sleep_total_time
```

## Fertig!
Der komplette Workflow ist nun eingerichtet.

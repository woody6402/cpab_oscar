📘 CPAP → OSCAR → Home Assistant
Vollständige Anleitung zur Installation, Auswertung und Datenübernahme
Diese Anleitung beschreibt den kompletten Workflow, um Daten aus einem ResMed AirSense 10 über OSCAR auszulesen, daraus eine Home-Assistant-kompatible Statistikdatei zu erzeugen und diese anschließend mittels Import Statistics in HA zu übernehmen.

📦 1. OSCAR installieren
OSCAR ist ein Open-Source-Tool zur Auswertung von CPAP-Daten.
Download:
https://www.sleepfiles.com/OSCAR/
Installieren für:


Windows


macOS


Linux (AppImage)


Nach dem Start:


Neuen Benutzer anlegen (z. B. Andreas).


Gerätetyp „ResMed AirSense“ auswählen.



💾 2. Daten vom ResMed AirSense 10 auslesen
Der AirSense 10 speichert alle Rohdaten auf einer SD-Karte.


Gerät ausschalten.


SD-Karte entnehmen.


In PC/Laptop stecken.


OSCAR öffnet automatisch einen Importdialog:
„Neue Daten gefunden – Importieren?“


Import bestätigen.


Die Daten werden nun vollständig eingelesen.

📤 3. CSV-Export aus OSCAR erzeugen
Für Home Assistant brauchen wir eine CSV-Zusammenfassung.
In OSCAR:


Menü Daten → Übersicht speichern / Export


Format: CSV Export


Datei speichern (z. B. oscar_export.csv)


Diese Datei enthält u. a.:


Startzeit pro Session


komplette Schlafdauer


AHI & Apnoe-Arten


Druckstatistiken



🛠️ 4. Home-Assistant-Importdatei erzeugen (TSV)
Im Repository liegt ein Python-Script genHAimport.py, das aus der OSCAR-CSV eine TSV-Datei für Import Statistics erzeugt.
(Auszug aus deinem Script: genHAimport)
Ausführen:
python3 genHAimport.py

Erwartet wird:
oscar_export.csv    (Input)
oscar_import_sleep_ahi_6m.tsv (Output)

Die Datei enthält für jeden Tag zwei Statistikzeilen:


sensor.sleep_total_time – Gesamtschlafzeit (gerundet auf 2 Nachkommastellen)


sensor.sleep_ahi – AHI-Wert dieser Nacht


Die Datei ist TAB-getrennt und im Format:
statistic_id	unit	start	min	max	mean
sensor.sleep_total_time	h	22.05.2025 23:00	8.18	8.18	8.18
sensor.sleep_ahi	events/h	22.05.2025 23:00	1.833	1.833	1.833


📥 5. Import Statistics installieren (HACS)


HACS öffnen


„Integration hinzufügen“


Nach Import Statistics suchen


Installieren & HA neu starten


Der Code im Repo kann genutzt werden, um diese Datei in HA einzuspielen.

📊 6. Statistik-Sensoren in Home Assistant anlegen
Damit die importierten Daten sichtbar werden, müssen die Ziel-Entitäten existieren.
Dazu liegt die Datei cpap.yaml bereit — dein Template-Sensor-Set für die Werte:
(Auszug: cpap)
##############################
#   CPAP / OSCAR PACKAGE     #
##############################

template:
  - sensor:

      # Platzhalter für importierte Schlafdauer (TSV via Import Statistics)
      - name: "Sleep Total Time"
        unique_id: sleep_total_time
        unit_of_measurement: "h"
        device_class: duration
        state_class: measurement
        state: 0

      # Platzhalter für importierte AHI-Werte (TSV via Import Statistics)
      - name: "Sleep AHI"
        unique_id: sleep_ahi
        unit_of_measurement: "events/h"
        state_class: measurement
        state: 0

Nach einem Neustart existieren die Entitäten:


sensor.sleep_total_time


sensor.sleep_ahi



📡 7. TSV-Datei in Home Assistant importieren
Unter Entwicklerwerkzeuge → Aktionen/Dienste:


Dienst auswählen:
import_statistics.import_from_file


Parameter setzen:


timezone_identifier: Europe/Vienna
delimiter: "\t"
decimal: false
filename: /config/oscar_import_sleep_ahi_6m.tsv



Ausführen


Nach Sekunden erscheinen die Daten:


im Diagramm


im Energie-/Statistikbereich


in History-Charts



🧹 8. Alte Testdaten löschen (optional)
Falls du frühere Tests entfernen willst:
Dienst statistics.delete:
statistic_id: sensor.sleep_total_time

Für AHI:
statistic_id: sensor.sleep_ahi


✔️ Fertig!
Du hast jetzt einen vollständigen Workflow:


AirSense-SD einlesen


OSCAR-CSV exportieren


Script → TSV für HA


Statistik-Sensoren erzeugen


Import Statistics → Daten einspielen


Wenn du möchtest, kann ich dir auch eine fertige grafische Lovelace-Card bauen (mit Verlaufsdiagramm für AHI und Schlafdauer).Quellen

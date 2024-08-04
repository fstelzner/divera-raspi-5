# divera-raspi-5
Divera Setup für den Raspberry Pi 5

Vor Jahren haben wir bei uns in der Wache der [Freiwilligen Feuerwehr Brokstedt](https://www.feuerwehr-brokstedt.de) einen Divera-Wachenmonitor
auf dem Raspberry Pi 4 aufgesetzt. Dazu haben wir im Wesentlichen [diese](https://help.divera247.com/pages/viewpage.action?pageId=44171296) Anleitung verwendet und für unsere Zwecke angepasst. 

Auf dem Raspberry Pi 5 kann diese Anleitung nicht mehr verwendet werden, da sie mit dem xscreensaver arbeitet, der unter Wayland nicht funktioniert.
Mein Setup-Prozess habe ich hier dokumentiert, damit Du es einfacher hast. Fragen? Gerne jederzeit an f.stelzner@feuerwehr-brokstedt.de

## Anforderungen:
- [ ] Automatischer Start nach Reboot, um auch bei Stromausfall schnell wieder einsatzfähig zu sein
- [ ] Monitor-Ausgabe nur bei Alarm
- [ ] Auf Basis der Divera-Daten soll eine PDF-Alarmdepesche erstellt werden, die direkt an den Drucker gesendet wird, da die Leitstelle demnächst den Fax-Versand der Depechen einstellen wird

### Step 1 - Frische SD Karte installieren
Mit billigen NoName-Karten habe ich sehr schlechte Erfahrungen gemacht.
Tu Dir selbst einen gefallen und gönne Dir eine hochwertige SD-Karte.
Ich habe mich für [diese hier entschieden](https://amzn.to/3WQP0c6).

1. https://www.raspberrypi.com/software/ herunterladen und installieren
2. In der Software das Pi Model 5 auswählen, die empfohlene Desktop-Variante in 64 BIT und die richtige SD Karte
3. Du sparst Zeit, wenn Du schon jetzt Wifi, Sprache, Tastaturlayout, Username + Password sowie SSH aktivierst
4. SD Karte in den Pi einstecken und starten

### Step 2 (optional) - VNC aktivieren
Da der Pi bei uns in der Wache ohne Tastatur und Maus gut versteckt und gesichert angebracht wird, ergibt es Sinn VNC zu aktivieren.

```
ssh pi@192.168.10.111
sudo apt-get update
sudo raspi-config
```

Unter Punkt 3 - Interface Options kannst Du dann den VNC Dienst einfach aktivieren und kannst dann zum Beispiel mit dem [VNC Viewer](https://www.realvnc.com/de/connect/download/viewer/)
darauf zugreifen.

### Step 3 Divera-Scripte per SSH ins Benutzerverzeichnis schreiben (z.B. /home/pi/ )

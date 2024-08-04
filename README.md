# divera-raspi-5
Divera Setup für den Raspberry Pi 5

Vor Jahren haben wir bei uns in der Wache der [Freiwilligen Feuerwehr Brokstedt](https://www.feuerwehr-brokstedt.de) einen Divera-Wachenmonitor
auf dem Raspberry Pi 4 aufgesetzt. Dazu haben wir im Wesentlichen [diese]([https://help.divera247.com/pages/viewpage.action?pageId=44171296](https://help.divera247.com/display/FAQ/RaspberryPi+-+Bildschirmschoner+automatisch+deaktivieren)) Anleitung verwendet und für unsere Zwecke angepasst. 

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

### Step 4 Verzeichnisse anlegen
Passe die Verzeichnisse gerne an, wie Du möchtest. Achte bei jeder Änderung auf die Referenzen in den Scripten und Befehlen.
So habe ich die Verzeichnisse angelegt:

1. divera -> hier sind alle benötigten Scripte
2. divera/depechen -> hier wird die die aktuelle Alarm-Depeche generiert, bevor sie an den Drucker gesendet und archiviert wird
3. depechen/archive -> hier werden die ausgedruckten Depechen gelagert -> je nach Speicherkapazität solltest Du hier ggf. ab und zu aufräumen

```
mkdir /home/pi/divera
mkdir /home/pi/divera/depechen
mkdir /home/pi/divera/depechen/archive
```

### Step 3 Divera-Scripte per SSH ins Divera-Verzeichnis schreiben (z.B. /home/pi/divera )
Nutze einen Command Line Editor Deiner Wahl, um die Dateien anzulegen. Die meisten verwenden wohl Nano, die coolen Kids eher VI(m) und wer sich da ganz unsicher fühlt, der kann
sich ja glücklicherweise mit VNC verbinden und die Dateien einfach mit dem grafischen Texteditor anlegen. Uncool, aber wenn es hilft ;-) 

```
vi /home/pi/divera/divera-alarm.sh
vi /home/pi/divera/divera-print.py
```

Beide Scripte müssen nun noch ausführbar gemacht werden:

```
chmod +x /home/pi/divera/divera-alarm.sh
chmod +x /home/pi/divera/divera-print.py
```


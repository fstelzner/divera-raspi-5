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

### Step 2 (optional) - VNC aktivieren & Default-Printer bestimmen
Da der Pi bei uns in der Wache ohne Tastatur und Maus gut versteckt und gesichert angebracht wird, ergibt es Sinn VNC zu aktivieren.

```
ssh pi@192.168.10.111
sudo apt-get update
sudo raspi-config
```

Unter Punkt 3 - Interface Options kannst Du dann den VNC Dienst einfach aktivieren und kannst dann zum Beispiel mit dem [VNC Viewer](https://www.realvnc.com/de/connect/download/viewer/)
darauf zugreifen.

Während Du nun die Funktionsfähigkeit des VNCs testest, kannst Du das gleich mit etwas Nützlichem verbinden.
Nämlich der Einstellung des Standard Druckers. 
Unter *PI > Preferences > Print Settings* kannst Du mit Rechtsklick "Set as Default" Deinen Lieblingsdrucker küren.

### Step 4 Verzeichnisse anlegen
Passe die Verzeichnisse gerne an, wie Du möchtest. Achte bei jeder Änderung auf die Referenzen in den Scripten und Befehlen.
So habe ich die Verzeichnisse angelegt:

1. divera -> hier sind alle benötigten Scripte
2. divera/depechen -> hier wird die die aktuelle Alarm-Depeche generiert, bevor sie an den Drucker gesendet und archiviert wird
3. depechen/archive -> hier werden die ausgedruckten Depechen gelagert -> je nach Speicherkapazität solltest Du hier ggf. ab und zu aufräumen
4. depechen/archive/depeche.log -> ein Logfile, um doppeltes Ausdrucken zu verhindern

```
mkdir /home/pi/divera
mkdir /home/pi/divera/depechen
mkdir /home/pi/divera/depechen/archive
touch /home/pi/divera/depechen/archive/depeche.log
```

### Step 3 Divera-Scripte per SSH ins Divera-Verzeichnis schreiben (z.B. /home/pi/divera )
Nutze einen Command Line Editor Deiner Wahl, um die Dateien anzulegen. Die meisten verwenden wohl Nano, die coolen Kids eher VI(m) und wer sich da ganz unsicher fühlt, der kann
sich ja glücklicherweise mit VNC verbinden und die Dateien einfach mit dem grafischen Texteditor anlegen. Uncool, aber wenn es hilft ;-) 

```
vi /home/pi/divera/start-chromium.sh
vi /home/pi/divera/divera-alarm.sh
vi /home/pi/divera/divera-print.py
vi /home/pi/divera/depechen-druck.sh
```

Die Scripte müssen nun noch ausführbar gemacht werden:

```
chmod +x /home/pi/divera/start-chromium.sh
chmod +x /home/pi/divera/divera-alarm.sh
chmod +x /home/pi/divera/divera-print.py
chmod +x /home/pi/divera/depechen-druck.sh
```

### Step 4 Notwendige Programme installieren & Python-Environment einrichten
Für das divera-alarm.sh Script benötigen wir [jq]()

```
sudo apt-get install jq
```

#### Für die Druckfunktion:
Mit Wayland auf dem Raspberry Pi 5 braucht man ein Environment, um _pip install_ nutzen zu können.
Idealerweise gewöhnt man sich an, für jedes Projekt ein eigenes Environment anzulegen. Details und wieso, weshalb, warum gibt es [hier](https://www.raspberrypi.com/documentation/computers/os.html#python-on-raspberry-pi).
In diesem Fall legen wir _divera_ an und aktivieren es:

```
cd /home/pi/divera/
python -m venv --system-site-packages divera
source divera/bin/activate
```

Der Prompt sollte sich nun geändet haben, sodass Du Dich im Environment befindest.
Jetzt können wir _pip install_ benutzen:

```
pip3 install fpdf2
```

Um das Environment wieder zu verlassen:

```
deactivate
```
Das Environment wurde nun im Ordner /home/pi/divera/ im gleichnamigen Unterordner divera angelegt. 

### Step 5 Divera-Monitor-URL mit Chromium automatisch starten
In Wayland ist auch hier der Autostart anders, da wir nicht mehr mit X arbeiten. -.config/lxsession/LXDE-pi/autostart- führt Euch also auf die falsche Fährte.
Die _/home/pi/.config/wayfire.ini_ muss am Ende um folgenden Eintrag ergänzt werden. Die URL zu Deinem Divera-Wachmonitor muss Du natürlich noch anpassen.

```
[autostart]
autostart_wf_shell = false
chromium = /home/pi/divera/start-chromium.sh
divera = /home/pi/divera/divera-alarm.sh
```
### Crontab für die Überprüfung und den Ausdruck der Depechen anlegen

```
crontab -e
```

dort dann die neue Zeile für Ausführung zu jeder Minute durchführen und etwaigen Output (kann nur Fehler-Output sein, da das Script selbst keine Ausgaben macht) zur Sicherheit in ein Logfile schreiben:
```
* * * * * /usr/bin/python3 /home/pi/divera/depechen-druck.sh >> /home/pi/divera/cron.log 2>&1
```

Hier kommt die Lösung - mit dem
Pr0-Videoübersetzer

Benötigt wird:
- eine Grafikkarte
- FFMPEG (https://ffmpeg.org/)
- Git

Installieren:
- aktuelles Python installieren (mind. 3.10)
- git-repo klonen
- Konsole öffnen
- ins geklonte Verzeichnis wechseln
- "pip install -r requirements.txt" eingeben

Benutzen:
- Konsole öffnen und ins Verzeichnis wechseln
- "python transcriber.py" eingeben
- Videolink(Rechtsklick auf Video -> "Video-Adresse kopieren") ins URL-Feld
- Auswählen, ob Whisper-Übersetzer (nur Englisch) oder Deepl (derzeit Deutsch)
- Modellgröße auswählen (größer = besser, aber langsamer)
- "Process" drücken (beim ersten Mal etwas Geduld)

Todo:
- Pr0-Links akzeptieren
- Youtube-Links akzeptieren?
- Übersetzung als Volltext statt Segmente für bessere Zusammenhänge
- einfachere Installation
- bessere GUI (Ich bin halt kein Softwareentwickler)

Geschichte:
Im Rahmen von OSINT-Recherchen im Ukrainekrieg stieß ich immer wieder auf
russische Quellen. Mein Russisch beschränkt sich auf wenige Sätze - "cyka blyat".
Für Text habe ich daher immer Deepl benutzt, jedoch für das gesprochende Wort fand
ich keine gute Lösung, daher habe ich meine eigene geskriptet.
Einige User fragten immer wieder nach dem Quelltext, da der aber Scheiße war(ist) 
und keine GUI hatte, habe ich ein wenig programmiert und das hier ist das Ergebnis.

Vermutlich werde ich daran noch etwas weiterarbeiten und die Todo-Liste abarbeiten.
Wenn jemand daran mitarbeiten will, ist er herzlich willkommen.
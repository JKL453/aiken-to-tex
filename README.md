# Leitfaden zur Erstellung von Antestat-Fragen mit ChatGPT und Export ins Aiken-Format

## Wichtig zu Beginn
Jeder Praktikumsversuch besteht aus **fünf festgelegten Fragen-Kategorien**. Für das Antestat wird aus **jeder Kategorie genau eine Frage** ausgewählt, sodass jede Prüfung fünf Fragen umfasst.

Für jede dieser Kategorien existiert **eine eigene `.txt`-Datei pro Versuch** im Aiken-Format. Diese Dateien enthalten jeweils mehrere Fragen zu einer Kategorie und bilden den Fragenpool.

Die so erstellten Fragen werden einem zentralen **Fragen-Pool** hinzugefügt. Die spätere **Erstellung zufälliger Antestate im LaTeX-Format** erfolgt automatisiert.

**Wichtig: von Anfang an LaTeX-Syntax** für Einheiten und Formeln, damit der automatische Tex-Export korrekt funktioniert.


## Themenfelder (Beispiel: Versuch G - Geometrische Optik)

1. Brechkraft
2. Brennweite
3. Fehlsichtigkeit
4. Sammellinse
5. Strahlenbündel

## Fragen erstellen

Die Fragen können selbst oder mit Hilfe von ChatGPT erstellt werden. Dabei ist es wichtig, dass die Fragen im **Aiken-Format** vorliegen.

Beispiel-Prompt für ChatGPT:

```
Erstelle eine Multiple-Choice-Frage zum Thema 
"Lichtbrechung bei Übergang zwischen Medien" für ein Physik-Antestat 
für Medizinstudierende. Gib fünf Antwortmöglichkeiten (A–E) und 
markiere die richtige Antwort. Formatiere die Ausgabe im Aiken-Format.

Formatiere Einheiten, Formeln etc. in TeX. 
Die Aufgaben sollen ohne Verwendung eines Taschenrechners lösbar sein. 
Verwende eine Klammer statt Punkt bei den Antwortmöglichkeiten, 
Beispiel: A) Antworttext.
```

### Beispielausgabe (korrektes Aiken-Format):

```
Welche Aussage beschreibt korrekt, warum ein Lichtstrahl beim 
Übergang von Luft ($ n = 1,0 $) in Hornhautgewebe ($ n \approx 1,38 $) 
seine Richtung ändert?

A) Weil sich die Frequenz des Lichts beim Übergang erhöht.  
B) Weil die Lichtgeschwindigkeit im dichteren Medium zunimmt.  
C) Weil die Lichtgeschwindigkeit im dichteren Medium abnimmt.  
D) Weil das Licht eine höhere Energie im Gewebe hat.  
E) Weil die Richtung des Lichtstrahls ausschließlich vom Lot abhängt.

ANSWER: C
```

Bei Verwendung von ChatGPT ist es wichtig, die **Fragen zu überprüfen** und ggf. anzupassen. Achte darauf, dass die Fragen klar formuliert sind und keine Missverständnisse aufkommen können.


## Dateien thematisch speichern

Fragen thematisch sortiert in einzelne `.txt`-Dateien sortieren. Zum Beispiel so:

- `fragen_01_lichtbrechung.txt`
- `fragen_02_brennpunkt.txt`
- `fragen_03_strahlenbuendel.txt`
- `fragen_04_brechungsindex.txt`
- `fragen_05_misc.txt`



Launch notebook in JupyterHub: 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JKL453/aiken-to-tex.git/HEAD?labpath=%2Fpython%2Faiken-parsing.ipynb)

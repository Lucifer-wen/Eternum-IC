# Eternum-IC — Übersetzungen

Alles, was zur Mod-Übersetzung gehört, liegt in diesem Ordner. Eine
Basisspiel-Übersetzung in `game/tl/<sprache>/` bleibt davon unberührt und
übernimmt weiterhin den Originaltext.

```
Eternum-IC/tl/
    im_translation.rpy      Loader — trägt die JSON-Dateien in Ren'Pys String-Tabelle ein
    im_tl_convert.rpy       Konverter — macht Fremdübersetzungen mod-kompatibel
    im_tl_extract.rpy       Extraktor — erzeugt die JSON-Vorlage (Dev-Tool)
    im_tl_selftest.rpy      Selbsttest — `Eternum.exe . imtl` (Dev-Tool)
    im_tl_txt_merge.py      Schreibt eine ausgefüllte UNTRANSLATED.txt zurück in die JSON
    German/
        dialogue.json       Mod-Dialoge
        ui.json             Mod-Menüs
        UNTRANSLATED.txt    Was noch offen ist, zum Ausfüllen
```

## Warum JSON und keine `translate ... strings:` Blöcke?

Ren'Py hält **eine** String-Tabelle pro Sprache für das ganze Spiel.
`StringTranslator.add()` wirft eine Exception, sobald dieselbe Zeile ein
zweites Mal registriert wird. `IncestLables.rpy` übernimmt ganze Szenen
wortgleich aus dem Basisspiel — eine Mod-Übersetzung und eine
Basis-Übersetzung würden also kollidieren und das Spiel beim Start abstürzen
lassen. Der Loader schreibt stattdessen selbst in die Tabelle und entscheidet
bei Konflikten, statt abzubrechen.

## Warum nicht `translate <sprache> <id>:`?

Reihenfolge. Translate-Blöcke tauschen den Text auf AST-Ebene aus, also
**bevor** `config.say_menu_text_filter` läuft. Der Mod würde dann deutschen
Text gegen seine englische Map prüfen und nichts ersetzen. String-Übersetzungen
greifen in `renpy.substitute()`, also **danach**:

```
Englisch  ->  Mod ersetzt (Incest-Englisch)  ->  String-Tabelle  ->  Deutsch
```

Deshalb sind die Schlüssel in den JSON-Dateien **die bereits vom Mod
ersetzten** englischen Zeilen, nicht die Originalzeilen.

## Neue Sprache anlegen

1. Ordner erstellen, benannt **exakt** wie die Ren'Py-Sprache — die
   Schreibweise zählt. Die Basis-Übersetzung dieses Spiels heißt `German`
   (groß), also muss der Mod-Ordner auch `German` heißen, nicht `german`.
   Ren'Py hält pro Schreibweise eine eigene String-Tabelle.
2. Vorlage erzeugen — Konsole im Spiel öffnen (`Shift+O`):
   ```python
   im_tl_extract("french")
   ```
   Das schreibt `french/dialogue.json` mit allen Mod-Strings und leeren Werten.
3. Werte ausfüllen. Leerer Wert = noch nicht übersetzt, die englische Zeile
   bleibt stehen.
4. Spiel neu starten (oder `_im_tl_reload()` in der Konsole).

Erneutes Ausführen von `im_tl_extract` behält vorhandene Übersetzungen und
ergänzt nur neue Zeilen — nach einem Spiel- oder Mod-Update also einfach
nochmal laufen lassen.

## Offene Zeilen ausfüllen

`German/UNTRANSLATED.txt` listet alles, was noch keine Übersetzung hat,
gruppiert nach Grund. Format:

```
[0385]
EN: I'll suck your cock, {i}brother{/i}.
DE: 
```

Übersetzung hinter `DE:` schreiben, leer lassen heißt „bleibt englisch". Dann:

```
cd Eternum-IC/tl
python im_tl_txt_merge.py German/UNTRANSLATED.txt
```

Das Skript ordnet über den englischen Text zu, nicht über die Nummer — die
Datei bleibt also gültig, auch wenn `im_tl_extract` die Reihenfolge ändert.
Vor dem Übernehmen prüft es jede Zeile darauf, dass Text-Tags und
`[mc]`/`[lastname]` in Quelle und Übersetzung gleich vorkommen; Abweichungen
werden gemeldet und **nicht** übernommen, weil fehlende Tags sonst das Markup
im Spiel zerlegen.

Die Datei wird von `gen_txt.py` neu erzeugt und ist danach wieder aktuell.

## Regeln für die Schlüssel

- **Exakter Match.** `That's` mit typografischem Apostroph (`’`) ist ein
  anderer Schlüssel als mit ASCII-Apostroph. Schlüssel nie von Hand tippen —
  immer aus der Extraktor-Vorlage übernehmen.
- **`[mc]` und `[lastname]` stehen lassen**, in Schlüssel *und* Übersetzung.
  Ren'Py setzt den Spielernamen erst nach der Übersetzung ein; dadurch ist die
  Datei namensunabhängig.
- **Text-Tags erhalten**: `{i}`, `{size=...}`, `{w}` müssen in der Übersetzung
  genauso vorkommen.
- Schlüssel, die mit `_` beginnen, ignoriert der Loader — praktisch für
  Kommentare wie `_comment`.

## Konfliktregel

Standardmäßig gewinnt die Basis-Übersetzung: existiert eine Zeile bereits in
`game/tl/<sprache>/`, überspringt der Loader den Mod-Eintrag. Umdrehen lässt
sich das in `im_translation.rpy`:

```python
_im_tl_override_base = True
```

Der Extraktor lässt Zeilen, die wortgleich im Basisspiel vorkommen, ohnehin
weg — die gehören der Basis-Übersetzung.

## Ohne Basis-Übersetzung

Wer ein eigenständiges Sprachpaket bauen will, das auch den Originaltext
abdeckt:

```python
im_tl_extract("German", include_base=True)   # -> German/base_dialogue.json
```

Für die UI des Basisspiels zusätzlich Ren'Pys eigenen Generator benutzen:

```
Eternum.exe . translate German --strings-only
```

Der schreibt nach `game/tl/German/` und arbeitet mit `old`/`new`-Paaren, die
mit diesem System zusammenpassen.

## Selbsttest

```
Eternum.exe . imtl
```

Läuft ohne Fenster und prüft: Loader-Registrierung, Lookup über
`translate_string()`, dass die Mod-Ersetzung `[mc]` intakt lässt, und die
komplette Kette Englisch → Mod → Deutsch.

## Fremdübersetzungen mit Translate-Blöcken

`im_tl_convert.rpy` löst das Grundproblem, dass eine normale Ren'Py-Übersetzung
ihre Dialoge als `translate <sprache> <id>:` Blöcke liefert. Die greifen auf
AST-Ebene, also **vor** `config.say_menu_text_filter` — der Mod bekäme
deutschen Text und würde nichts mehr ersetzen.

Der Konverter schreibt beim Sprachwechsel jeden Block in ein String-Paar
`englisches Original -> Übersetzung` um und entfernt den Block.
`lookup_translate()` fällt dann auf das englische Original zurück, der Filter
sieht wieder Englisch, und die Übersetzung greift danach:

```
Englisch  ->  Mod ersetzt  ->  String-Tabelle  ->  Deutsch
```

`game/tl/<sprache>/` wird dabei **nicht angefasst** — die Umschreibung
passiert nur im Arbeitsspeicher.

### Gemessen an der German-Übersetzung von Eternum 0.9.5

```
71793 Blöcke konvertiert in 0,20s
  54347  Strings neu registriert
  10711  bereits vorhanden (Dubletten mit gleicher Übersetzung)
   5705  unübersetzt (Original == "Übersetzung")
   1030  mehrdeutig — erste Fassung gewinnt
```

Die 1030 mehrdeutigen Blöcke betreffen 571 englische Zeilen, die im
Original mehrere deutsche Fassungen haben. Sie zeigen jetzt die erste davon.
In der Stichprobe waren das fast ausschließlich Groß-/Kleinschreibungs-
Varianten desselben Satzes:

```
'Okay... let's do it.'  ->  'Okay... Lass es uns tun.' / 'Okay... lass es uns tun.'
'Good girl...'          ->  'Braves Mädchen...'        / 'Gutes Mädchen...'
```

219 Blöcke bleiben stehen: deren Identifier existiert im aktuellen Script
nicht mehr (Reste einer älteren Spielversion). Sie könnten ohnehin nie feuern
und werden deshalb bewusst in Ruhe gelassen.

### Abschalten

In `im_tl_convert.rpy`:

```python
_im_tl_convert_enabled = False
```

Ohne Konverter ist der Mod bei aktiver Fremdübersetzung für
Basisspiel-Dialoge praktisch abgeschaltet.

### Was danach noch zu tun ist

Zeilen, die der Mod **ersetzt**, sind danach nicht mehr von der
Basis-Übersetzung abgedeckt — ihr Text ist ja ein anderer. Genau dafür ist
`German/dialogue.json` da: die 2126 Strings aus dem Extraktor müssen übersetzt
werden, sonst erscheinen die vom Mod geänderten Zeilen auf Englisch, während
der Rest deutsch ist.

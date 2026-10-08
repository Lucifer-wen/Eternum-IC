"""
Schreibt die in UNTRANSLATED.txt ausgefuellten DE:-Zeilen zurueck nach
<sprache>/dialogue.json.

    cd Eternum-IC/tl
    python im_tl_txt_merge.py German/UNTRANSLATED.txt

Die Zuordnung laeuft ueber den englischen Text in der EN:-Zeile, nicht ueber
die Nummer -- die Nummer ist nur zum Nachschlagen da. Damit bleibt die Datei
auch dann gueltig, wenn im_tl_extract die Reihenfolge aendert.

Geprueft wird pro Zeile, ob Text-Tags ({i}, {color=...}) und die Platzhalter
[mc]/[lastname] in Quelle und Uebersetzung gleich vorkommen. Abweichungen
werden gemeldet und NICHT uebernommen -- fehlende Tags zerlegen sonst das
Markup im Spiel.
"""
import io
import json
import os
import re
import sys

TAG = re.compile(r"\{[^{}]*\}")
PLACEHOLDERS = ("[mc]", "[lastname]")


def parse(path):
    """Liest die txt und liefert [(nummer, englisch, deutsch), ...]."""
    entries = []
    num = en = None

    with io.open(path, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.rstrip("\r\n")

            m = re.match(r"^\[(\d+)\]\s*$", line)
            if m:
                num, en = int(m.group(1)), None
                continue

            if line.startswith("EN: "):
                en = line[4:]
                continue

            if line.startswith("DE:"):
                de = line[3:].strip()
                if en is None:
                    print("  Zeile %d: DE: ohne vorangehendes EN: -- uebersprungen" % lineno)
                elif de:
                    entries.append((num, en, de))
                num = en = None

    return entries


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    txt = sys.argv[1]
    if not os.path.exists(txt):
        print("Datei nicht gefunden: %s" % txt)
        return 1

    langdir = os.path.dirname(os.path.abspath(txt))
    dlg_path = os.path.join(langdir, "dialogue.json")
    if not os.path.exists(dlg_path):
        print("dialogue.json nicht gefunden neben %s" % txt)
        return 1

    with io.open(dlg_path, encoding="utf-8") as f:
        dlg = json.load(f)

    entries = parse(txt)
    applied = skipped = unknown = 0

    for num, en, de in entries:
        if en not in dlg:
            print("  [%04d] unbekannter Quelltext -- steht so nicht in dialogue.json" % (num or 0))
            unknown += 1
            continue

        problems = []
        if sorted(TAG.findall(en)) != sorted(TAG.findall(de)):
            problems.append("Text-Tags weichen ab: %r vs %r"
                            % (TAG.findall(en), TAG.findall(de)))
        for ph in PLACEHOLDERS:
            if (ph in en) != (ph in de):
                problems.append("%s fehlt oder ist zuviel" % ph)

        if problems:
            print("  [%04d] NICHT uebernommen: %s" % (num or 0, "; ".join(problems)))
            skipped += 1
            continue

        dlg[en] = de
        applied += 1

    if applied:
        with io.open(dlg_path, "w", encoding="utf-8") as f:
            json.dump(dlg, f, ensure_ascii=False, indent=2)
            f.write("\n")

    done = sum(1 for k, v in dlg.items() if not k.startswith("_") and v)
    total = sum(1 for k in dlg if not k.startswith("_"))
    print("uebernommen %d | abgelehnt %d | unbekannt %d" % (applied, skipped, unknown))
    print("dialogue.json: %d/%d uebersetzt (%.1f%%)" % (done, total, 100.0 * done / max(total, 1)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Eternum-IC map check (dev tool, not loaded by the game).

Compares the replacement maps in IncestMod.rpy with the scripts of the game
this copy of the mod is installed in and reports:

  * duplicate keys      - the same original line twice in one map (Python
                          silently keeps only the last one)
  * dead keys           - original lines that do not exist in the game
  * unmatched entries   - entries where no alternative's line number or
                          {"after": ...} context fits this install, so the
                          replacement / injection can never fire here
  * bad "after" specs   - a context specifier that matches nowhere (these are
                          the same in every variant, so this is always a bug)
  * bad injections      - injection strings the mod cannot parse

Line numbers differ between the base game, Bonus Mod and Multi-Mod, so run it
once per variant you support (or after a game update):

    python tools/im_map_check.py            # from the mod folder
    python tools/im_map_check.py -v         # also list per-variant misses
    python tools/im_map_check.py --game "D:/path/to/game"

Needs Python 3.7+ only. Exit code is 1 if problems were found.
"""

import argparse
import ast
import io
import os
import re
import sys
import textwrap
from collections import defaultdict

MAP_FILE = "IncestMod.rpy"
SKIP_DIRS = {"tl", ".git", "cache", "saves", "tools", ".vscode", ".vs"}
BS = chr(92)

# --- text normalisation: keep in sync with IncestMod.rpy ---------------------
# (_in_normalize_equiv_text, _in_strip_tags, _im_strip_multimod_tags,
#  _im_strip_bonusmod_tags)
CHAR_TABLE = {
    0x2018: "'", 0x2019: "'", 0x201A: "'",
    0x201C: '"', 0x201D: '"', 0x201E: '"',
    0x2013: "-", 0x2014: "-", 0x2212: "-",
    0x00A0: " ", 0x2026: "...",
}
MULTIMOD_RE = re.compile(
    r"\[(?:gr|mm|red|blue|green|pink|mt|nova_pts|nancy_pts|dalia_pts|annie_pts"
    r"|alex_pts|penelope_pts|luna_pts|calypso_pts)\]"
    r"(?:(?:\{[^{}]+\})?\([^()]+\)(?:\{/[^{}]+\})?)?"
)
BONUS_RE = re.compile(r"\{color=\[\w+\]\}")
TAG_RE = re.compile(r"\{/?[^{}]+\}")
WS_RE = re.compile(r"\s+")


def norm(text):
    text = text.replace("[red](Insist)", "(Insist)").replace("(attack afterward)", "")
    text = MULTIMOD_RE.sub("", text)
    text = BONUS_RE.sub("", text)
    text = TAG_RE.sub("", text)
    text = text.translate(CHAR_TABLE)
    return WS_RE.sub(" ", text.strip())


# --- map parsing --------------------------------------------------------------
def extract_entry(value):
    """Port of _im_extract_entry: -> (text, spec, injections) or None."""
    if isinstance(value, str):
        return (value, None, [])
    if isinstance(value, (list, tuple)):
        items = list(value)
        if not items or not isinstance(items[0], str):
            return None
        spec = None
        injections = []
        for item in items[1:]:
            if isinstance(item, bool):
                continue
            if isinstance(item, int):
                if spec is None:
                    spec = item
            elif isinstance(item, dict):
                if spec is None:
                    spec = item
            elif isinstance(item, str):
                if spec is None and ":" in item:
                    spec = item
                else:
                    injections.append(item)
            elif isinstance(item, (list, tuple)):
                injections.extend(x for x in item if isinstance(x, str))
        return (items[0], spec, injections)
    return None


def alternatives(value):
    if isinstance(value, (list, tuple)) and value and isinstance(value[0], (list, tuple)):
        alts = value
    else:
        alts = (value,)
    return [e for e in (extract_entry(a) for a in alts) if e is not None]


def load_maps(path):
    """-> {map_name: [(key, lineno, value), ...]} for every text map."""
    with io.open(path, encoding="utf-8-sig") as f:
        lines = f.read().split("\n")
    maps = {}
    start_re = re.compile(r"^    (\w+_map)\s*=\s*\{\s*$")
    i = 0
    while i < len(lines):
        m = start_re.match(lines[i])
        if not m or m.group(1).startswith("im_label_map"):
            i += 1
            continue
        end = i
        while end < len(lines) and lines[end].rstrip() != "    }":
            end += 1
        code = textwrap.dedent("\n".join(lines[i:end + 1]))
        node = ast.parse(code).body[0].value
        entries = []
        for k, v in zip(node.keys, node.values):
            try:
                entries.append((ast.literal_eval(k), k.lineno + i, ast.literal_eval(v)))
            except Exception as e:
                print("  ! %s line %d: cannot evaluate entry (%s)" % (m.group(1), k.lineno + i, e))
        maps[m.group(1)] = entries
        i = end + 1
    return maps


# --- game script scan ---------------------------------------------------------
STRING_RE = re.compile('"((?:[^"' + BS * 2 + "]|" + BS * 2 + '.)*)"')
SAY_RE = re.compile(r'^\s*(?:([A-Za-z_]\w*)\s+)?"((?:[^"' + BS * 2 + "]|" + BS * 2 + r'.)*)"\s*(.*)$')
NOT_SPEAKERS = {
    "show", "scene", "hide", "play", "queue", "stop", "voice", "define",
    "default", "image", "call", "jump", "with", "text", "add", "textbutton",
    "label", "key", "style", "use", "imagebutton", "action", "tooltip", "old",
    "new", "return", "if", "elif", "while", "font", "background", "idle",
    "hover", "import", "from", "python", "init",
}


def unescape(text):
    return (text.replace(BS + '"', '"').replace(BS + "'", "'")
            .replace(BS + "n", "\n").replace("%%", "%"))


def scan_game(game_dir, mod_dir):
    """
    -> (occurrences, prev_say)
       occurrences: norm text -> [(short_file, line), ...]  (any string literal)
       prev_say:    (short_file, line) -> norm text of the previous dialogue line
    """
    occurrences = defaultdict(list)
    prev_say = {}
    map_file = os.path.normcase(os.path.join(mod_dir, MAP_FILE))
    for root, dirs, files in os.walk(game_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(files):
            if not fn.endswith(".rpy"):
                continue
            path = os.path.join(root, fn)
            if os.path.normcase(path) == map_file:
                continue
            try:
                with io.open(path, encoding="utf-8-sig") as f:
                    lines = f.read().split("\n")
            except Exception as e:
                print("  ! cannot read %s (%s)" % (path, e))
                continue
            short = os.path.splitext(fn)[0]
            prev = None
            last_code = ""
            for lineno, line in enumerate(lines, 1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                for m in STRING_RE.finditer(line):
                    n = norm(unescape(m.group(1)))
                    if n:
                        occurrences[n].append((short, lineno))
                m = SAY_RE.match(line)
                if m and m.group(1) not in NOT_SPEAKERS and not m.group(3).startswith(":"):
                    in_menu = last_code.startswith("menu") and last_code.endswith(":")
                    if not in_menu:
                        prev_say[(short, lineno)] = prev
                        prev = norm(unescape(m.group(2)))
                last_code = stripped
    return occurrences, prev_say


# --- checks -------------------------------------------------------------------
INJECTION_KEYWORDS = ("show ", "hide ", "scene ", "play ", "queue ", "stop ")
INJECTION_SAY_RE = re.compile(r"^(\w+)\s+[\"'](.+)[\"']$", re.DOTALL)


def injection_ok(text):
    s = re.sub(r"\s+with\s+\w+\s*$", "", text.strip(), flags=re.IGNORECASE).strip()
    return s.lower().startswith(INJECTION_KEYWORDS) or bool(INJECTION_SAY_RE.match(s))


def spec_matches(spec, occ, prev_say):
    if spec is None:
        return True
    if isinstance(spec, dict):
        after = spec.get("after")
        if after is None:
            return False
        if isinstance(after, str):
            after = (after,)
        wanted = {norm(a) for a in after if isinstance(a, str)}
        return any(prev_say.get(loc) in wanted for loc in occ)
    if isinstance(spec, int):
        return any(line == spec for _, line in occ)
    s = str(spec).strip()
    if ":" in s:
        file_hint, _, line = s.partition(":")
        return (file_hint.strip(), line.strip()) in {(f, str(l)) for f, l in occ}
    return any(str(line) == s for _, line in occ)


def short_text(text, width=110):
    text = text.replace("\n", " ")
    return text if len(text) <= width else text[:width - 3] + "..."


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    mod_dir = os.path.dirname(here)
    ap = argparse.ArgumentParser(description="Check the Eternum-IC replacement maps against the installed game.")
    ap.add_argument("--game", default=os.path.dirname(mod_dir), help="path to the game/ folder (default: parent of the mod folder)")
    ap.add_argument("-v", "--verbose", action="store_true", help="also list alternatives that do not match this install")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    game_dir = os.path.abspath(args.game)
    variant = "base game"
    if os.path.exists(os.path.join(game_dir, "mod_additions", "mod_options.rpy")):
        variant = "Multi-Mod"
    elif os.path.exists(os.path.join(game_dir, "achievements", "achievements.rpy")):
        variant = "Bonus Mod"
    print("Game folder : %s" % game_dir)
    print("Variant     : %s" % variant)

    maps = load_maps(os.path.join(mod_dir, MAP_FILE))
    occurrences, prev_say = scan_game(game_dir, mod_dir)
    print("Scanned     : %d distinct strings, %d dialogue lines\n" % (len(occurrences), len(prev_say)))

    problems = 0
    for name, entries in maps.items():
        found = defaultdict(list)
        seen = {}
        for key, lineno, value in entries:
            if not isinstance(key, str):
                continue
            nkey = norm(key)
            if nkey in seen:
                found["duplicate keys"].append("line %d (first at line %d): %s" % (lineno, seen[nkey], short_text(key)))
            seen[nkey] = lineno

            occ = occurrences.get(nkey, [])
            alts = alternatives(value)
            if not alts:
                found["unreadable entries"].append("line %d: %s" % (lineno, short_text(key)))
                continue
            if not occ:
                found["dead keys (line not in this game)"].append("line %d: %s" % (lineno, short_text(key)))
            else:
                hits = [spec_matches(spec, occ, prev_say) for _, spec, _ in alts]
                where = ", ".join("%s:%d" % loc for loc in occ[:4])
                if not any(hits):
                    specs = ", ".join(repr(spec) for _, spec, _ in alts)
                    found["unmatched entries (never fire here)"].append(
                        "line %d: %s\n        specs: %s\n        game : %s" % (lineno, short_text(key), short_text(specs, 160), where))
                for (_, spec, _), hit in zip(alts, hits):
                    if hit:
                        continue
                    if isinstance(spec, dict):
                        found['bad "after" specs'].append(
                            "line %d: %s\n        after: %s" % (lineno, short_text(key), short_text(repr(spec.get("after")), 160)))
                    elif args.verbose:
                        found["alternatives for other variants (info)"].append("line %d: %r  (game: %s)" % (lineno, spec, where))
            for _, _, injections in alts:
                for inj in injections:
                    if not injection_ok(inj):
                        found["bad injections"].append("line %d: %s" % (lineno, short_text(inj)))

        real = sum(len(v) for k, v in found.items() if not k.endswith("(info)"))
        problems += real
        print("%s: %d entries, %d problem(s)" % (name, len(entries), real))
        for title, items in found.items():
            print("  %s: %d" % (title, len(items)))
            for item in items:
                print("    - " + item)
        print()

    print("OK - no problems found." if not problems else "%d problem(s) found." % problems)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

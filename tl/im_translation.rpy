################################################################################
# Eternum-IC translation loader
#
# Loads the mod's translations from  <mod>/tl/<language>/*.json  and registers
# them as Ren'Py *string* translations.
#
# Why not plain `translate <lang> strings:` blocks?
#   Ren'Py keeps one string table per language for the whole game
#   (renpy.game.script.translator.strings[lang]) and StringTranslator.add()
#   raises as soon as the same `old` line is registered twice. IncestLables.rpy
#   re-uses whole scenes from the base game verbatim, so a mod translation and
#   a base-game translation WILL collide and crash the game on startup.
#   Writing into the table ourselves lets us define the conflict policy instead.
#
# Why string translations and not `translate <lang> <id>:` blocks?
#   Translate blocks swap the say text at AST level, i.e. BEFORE
#   config.say_menu_text_filter runs -- the mod would then try to match
#   translated text against its English map and silently replace nothing. String
#   translations are applied inside renpy.substitute(), which runs AFTER the
#   filter. Order becomes:
#       English -> mod makes incest-English -> string table translates
################################################################################

init -900 python:
    import json as _im_tl_json
    import os as _im_tl_os

    # Ren'Py maps dict/list/set/str in the store namespace onto its own
    # revertable types. A plain dict handed back by json.load() is NOT an
    # instance of store `dict`, so isinstance() checks against the store names
    # silently reject valid data. Always test against the real builtins --
    # Ren'Py's revertable types subclass them, so both forms pass.
    import builtins as _im_bi

    # If True, mod translations overwrite entries a base-game translation has
    # already registered. Default False: the base translation owns any line
    # that exists in the original script.
    _im_tl_override_base = False

    # Filled in by _im_tl_load_all() for the dev overlay / console.
    _im_tl_stats = {}

    def _im_tl_log(msg):
        """
        renpy.log() is a no-op unless config.log is set, which this game does
        not do -- write to log.txt the way Ren'Py's own startup code does.
        """
        try:
            renpy.display.log.write("%s", msg)
        except Exception:
            try:
                print(msg)
            except Exception:
                pass

    def _im_tl_dir():
        """Absolute path of <mod>/tl, or None if the mod root is unknown."""
        try:
            root = getattr(renpy.store, "_ICMOD_ROOT", None) or "Eternum-IC"
            path = _im_tl_os.path.join(renpy.config.gamedir, root, "tl")
            return path if _im_tl_os.path.isdir(path) else None
        except Exception:
            return None

    def _im_tl_languages():
        """Names of the language folders shipped with the mod."""
        base = _im_tl_dir()
        if base is None:
            return []
        out = []
        try:
            for entry in sorted(_im_tl_os.listdir(base)):
                if entry.startswith((".", "_")):
                    continue
                if _im_tl_os.path.isdir(_im_tl_os.path.join(base, entry)):
                    out.append(entry)
        except Exception:
            pass
        return out

    def _im_tl_read_file(path):
        """Reads one translation file. Returns {old: new}, never raises."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = _im_tl_json.load(f)
        except Exception as e:
            _im_tl_log("Eternum-IC tl: could not read %s: %r" % (path, e))
            return {}

        if not isinstance(data, _im_bi.dict):
            _im_tl_log("Eternum-IC tl: %s is not a JSON object, ignored." % path)
            return {}

        out = {}
        for old, new in data.items():
            # Keys starting with '_' are metadata/comments, not translations.
            if not isinstance(old, _im_bi.str) or old.startswith("_"):
                continue
            # An empty value means "not translated yet" -- leave the original.
            if not isinstance(new, _im_bi.str) or not new:
                continue
            out[old] = new
        return out

    def _im_tl_load(language, override=None):
        """
        Registers every translation for `language`.
        Returns (added, skipped_existing, untranslated).
        """
        if override is None:
            override = _im_tl_override_base

        base = _im_tl_dir()
        if base is None:
            return (0, 0, 0)

        langdir = _im_tl_os.path.join(base, language)
        if not _im_tl_os.path.isdir(langdir):
            return (0, 0, 0)

        tl = renpy.game.script.translator
        stl = tl.strings[language]        # defaultdict, creates on access
        table = stl.translations

        added = 0
        skipped = 0
        total = 0

        try:
            files = sorted(f for f in _im_tl_os.listdir(langdir) if f.endswith(".json"))
        except Exception:
            files = []

        for fn in files:
            entries = _im_tl_read_file(_im_tl_os.path.join(langdir, fn))
            for old, new in entries.items():
                total += 1
                if (old in table) and not override:
                    # A base-game translation already covers this line.
                    skipped += 1
                    continue
                # Bypass StringTranslator.add() on purpose: its duplicate check
                # would abort the game instead of letting us pick a winner.
                table[old] = new
                added += 1

        if added:
            # Make the language selectable even when the mod is the only
            # provider -- the folder scan in renpy/translation only looks at
            # game/tl/, not at our directory.
            tl.languages.add(language)

        return (added, skipped, total)

    def _im_tl_load_all(override=None):
        """Loads every language the mod ships. Safe to call more than once."""
        global _im_tl_stats
        stats = {}
        for lang in _im_tl_languages():
            stats[lang] = _im_tl_load(lang, override=override)
        _im_tl_stats = stats
        return stats

    def _im_tl_reload():
        """
        Re-reads the JSON files at runtime (for translators).
        Overwrites whatever the mod registered before, but still respects
        entries owned by a base-game translation unless override is on.
        """
        return _im_tl_load_all()


# init 950 puts us behind the base-game translation: `translate <lang> strings:`
# parses into an ast.Init at the file's init offset, which is 0 in practice.
init 950 python:
    try:
        _im_tl_stats = _im_tl_load_all()
        for _im_tl_lang, (_a, _s, _t) in sorted(_im_tl_stats.items()):
            _im_tl_log(
                "Eternum-IC tl [%s]: %d registered, %d left to the base "
                "translation, %d in file." % (_im_tl_lang, _a, _s, _t)
            )
        del _im_tl_lang
    except Exception as e:
        _im_tl_log("Eternum-IC tl: load failed: %r" % e)

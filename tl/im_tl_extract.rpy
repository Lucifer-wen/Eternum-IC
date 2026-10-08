################################################################################
# Eternum-IC translation extractor  (developer tool)
#
# Collects every string the mod can put on screen and writes a JSON template to
#     <mod>/tl/<language>/dialogue.json
#
# Run it from the console (Shift+O):
#     im_tl_extract("german")                     # mod strings only
#     im_tl_extract("german", include_base=True)  # + the whole base game
#
# The extractor deliberately produces the string AS THE PLAYER SEES IT, i.e.
# after the mod's replacement map, after multi-mod tag stripping and after
# renpy.filter_text_tags() -- because that is exactly the form
# renpy.substitute() will look up in the string table. [mc] and [lastname] stay
# unresolved: Ren'Py interpolates them after the lookup, which keeps the
# translation independent of the player's name.
################################################################################

init -900 python:
    import json as _im_tlx_json
    import os as _im_tlx_os

    # Ren'Py maps dict/list/set/str in the store namespace onto its own
    # revertable types. A plain dict handed back by json.load() is NOT an
    # instance of store `dict`, so isinstance() checks against the store names
    # silently reject valid data. Always test against the real builtins --
    # Ren'Py's revertable types subclass them, so both forms pass.
    import builtins as _im_bi

    def _im_tlx_is_mod_file(filename):
        """True if an AST node comes from the mod rather than the base game."""
        if not filename:
            return False
        try:
            root = getattr(renpy.store, "_ICMOD_ROOT", None) or "Eternum-IC"
            root = root.replace("\\", "/").strip("/")
            norm = filename.replace("\\", "/")
            return ("/%s/" % root) in norm or norm.startswith("%s/" % root)
        except Exception:
            return False

    def _im_tlx_is_engine_file(filename):
        """Ren'Py's own common/ files -- handled by `translate --strings-only`."""
        if not filename:
            return True
        norm = filename.replace("\\", "/")
        return "renpy/common/" in norm or norm.startswith("common/")

    def _im_tlx_is_translation_file(filename):
        """
        A node from game/tl/<language>/ is somebody else's translation, not a
        source string. Counting those as base-game lines would let a German
        line shadow an identical mod output and drop it from the template.
        """
        if not filename:
            return False
        norm = filename.replace("\\", "/")
        return "/tl/" in norm or norm.startswith("tl/")

    def _im_tlx_final_form(s):
        """
        Returns every form of `s` that could reach the string table.

        The say/menu filter strips multi-mod tags before matching and applies
        filter_text_tags() to its result -- but whether the tags are stripped
        depends on which other mods are installed. Emitting both forms costs a
        few bytes and makes the file work either way.
        """
        if not isinstance(s, _im_bi.str) or not s.strip():
            return []

        forms = [s]
        for variant in (
            lambda t: _im_strip_multimod_tags(t, force=True),
            lambda t: _im_strip_bonusmod_tags(t),
        ):
            for existing in list(forms):
                try:
                    v = variant(existing)
                except Exception:
                    continue
                if v and v not in forms:
                    forms.append(v)

        out = []
        for f in forms:
            try:
                f = renpy.filter_text_tags(f, allow=_in_allowed_say_tags)
            except Exception:
                pass
            if f and f.strip() and f not in out:
                out.append(f)
        return out

    def _im_tlx_nancy_variant(s):
        """The Nancy -> Mom rewrite that _in_transform_text applies to MC lines."""
        if "Nancy" not in s:
            return None
        try:
            t = _in_nancy_possessive_re.sub("Mom's", s)
            t = _in_nancy_re.sub("Mom", t)
        except Exception:
            return None
        return t if t != s else None

    def _im_tlx_scan_script():
        """
        Walks the loaded AST once. Returns (base_strings, mod_strings,
        base_mc_strings) as ordered lists -- works on the compiled .rpyc, no
        sources needed. The third list is required because the speaker-aware
        Nancy -> Mom fallback also runs on MC lines from the base game.
        """
        base = []
        mod = []
        base_mc = []
        seen_base = set()
        seen_mod = set()
        seen_base_mc = set()

        Say = renpy.ast.Say          # TranslateSay subclasses Say
        Menu = renpy.ast.Menu

        for n in renpy.game.script.all_stmts:
            cls = n.__class__
            if not (issubclass(cls, Say) or cls is Menu):
                continue

            filename = getattr(n, "filename", "") or ""
            if _im_tlx_is_engine_file(filename):
                continue
            # Skip translated nodes: TranslateSay carries the target language,
            # and translation files live under game/tl/.
            if getattr(n, "language", None) is not None:
                continue
            if _im_tlx_is_translation_file(filename):
                continue

            if issubclass(cls, Say):
                texts = [getattr(n, "what", None)]
            else:
                # Menu items are (label, condition, block); label can be None
                # for the caption-less form.
                texts = [i[0] for i in getattr(n, "items", ())]

            is_mod = _im_tlx_is_mod_file(filename)
            bucket, seen = (mod, seen_mod) if is_mod else (base, seen_base)
            is_base_mc = (
                (not is_mod)
                and issubclass(cls, Say)
                and getattr(n, "who", None) in ("mc", "mct", "mcd", "mcsc")
            )

            for t in texts:
                if not isinstance(t, _im_bi.str):
                    continue
                for form in _im_tlx_final_form(t):
                    if form not in seen:
                        seen.add(form)
                        bucket.append(form)
                    if is_base_mc and form not in seen_base_mc:
                        seen_base_mc.add(form)
                        base_mc.append(form)

        return base, mod, base_mc

    def _im_tlx_map_outputs():
        """Every replacement the mod's maps can produce, in map order."""
        out = []
        seen = set()
        map_names = (
            "mom_map",
            "annie_sister_map",
            "annie_only_sister_map",
            "annie_half_sister_map",
            "annie_aunt_map",
        )

        for name in map_names:
            mapping = getattr(renpy.store, name, None)
            if not isinstance(mapping, _im_bi.dict):
                continue

            for old, new in mapping.items():
                if not old:
                    continue

                # A value is either one replacement or a list of alternatives.
                if isinstance(new, (_im_bi.list, _im_bi.tuple)) and new and isinstance(new[0], (_im_bi.list, _im_bi.tuple)):
                    alternatives = new
                else:
                    alternatives = (new,)

                for alt in alternatives:
                    extracted = _im_extract_entry(alt)
                    if extracted is None:
                        continue
                    rep = extracted[0]
                    for form in _im_tlx_final_form(rep):
                        if form not in seen:
                            seen.add(form)
                            out.append(form)

        return out

    def _im_tlx_collect(include_base=False):
        """Builds the ordered list of strings that belong in the mod's file."""
        base_strings, mod_strings, base_mc_strings = _im_tlx_scan_script()
        base_set = set(base_strings)

        ordered = []
        seen = set()

        def add(s):
            if s in seen:
                return
            # Anything that exists verbatim in the base game is the base
            # translation's job -- IncestLables.rpy copies whole scenes.
            if (not include_base) and (s in base_set):
                return
            seen.add(s)
            ordered.append(s)

        for s in mod_strings:
            add(s)
        for s in _im_tlx_map_outputs():
            add(s)

        # The Nancy->Mom rewrite runs after the map, so its output is a
        # separate string that needs its own translation.
        nancy_sources = list(ordered)
        nancy_sources += base_mc_strings
        for s in nancy_sources:
            variant = _im_tlx_nancy_variant(s)
            if variant:
                for form in _im_tlx_final_form(variant):
                    add(form)

        if include_base:
            for s in base_strings:
                add(s)

        return ordered, base_strings

    def im_tl_extract(language="german", include_base=False, filename=None):
        """
        Writes <mod>/tl/<language>/dialogue.json, keeping translations that are
        already in the file. Returns a short summary string.
        """
        base_dir = _im_tl_dir()
        if base_dir is None:
            return "Eternum-IC tl: mod tl/ directory not found."

        langdir = _im_tlx_os.path.join(base_dir, language)
        try:
            _im_tlx_os.makedirs(langdir, exist_ok=True)
        except Exception as e:
            return "Eternum-IC tl: cannot create %s: %r" % (langdir, e)

        if filename is None:
            filename = "base_dialogue.json" if include_base else "dialogue.json"
        path = _im_tlx_os.path.join(langdir, filename)

        # Keep whatever has been translated already.
        existing = {}
        if _im_tlx_os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    existing = _im_tlx_json.load(f) or {}
            except Exception as e:
                return ("Eternum-IC tl: %s exists but is unreadable (%r) -- "
                        "refusing to overwrite." % (path, e))

        ordered, base_strings = _im_tlx_collect(include_base=include_base)

        out = {}
        translated = 0
        for s in ordered:
            old = existing.get(s, "")
            if not isinstance(old, _im_bi.str):
                old = ""
            if old:
                translated += 1
            out[s] = old

        stale = [
            k for k in existing
            if not k.startswith("_") and k not in out and existing.get(k)
        ]

        try:
            with open(path, "w", encoding="utf-8") as f:
                _im_tlx_json.dump(out, f, ensure_ascii=False, indent=2)
                f.write("\n")
        except Exception as e:
            return "Eternum-IC tl: cannot write %s: %r" % (path, e)

        msg = (
            "Eternum-IC tl: wrote %d strings to %s (%d already translated, "
            "%d base-game lines skipped, %d stale entries dropped)."
            % (len(out), path, translated, len(base_strings), len(stale))
        )
        _im_tl_log(msg)
        if stale:
            _im_tl_log("Eternum-IC tl: dropped translations for: %r" % (stale[:10],))
        return msg

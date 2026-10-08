################################################################################
# Eternum-IC translate-block converter
#
# Makes a third-party base-game translation compatible with the mod.
#
# The problem
#   A normal Ren'Py translation ships its dialogue as `translate <lang> <id>:`
#   blocks. Those swap the say text at AST level -- BEFORE
#   config.say_menu_text_filter runs. The mod then matches German text against
#   its English map, hits nothing, and silently stops replacing anything.
#
# The fix
#   For every translate block, register the pair
#       english original -> translated text
#   as a *string* translation and drop the block. lookup_translate() then falls
#   back to default_translates[identifier] (translation/__init__.py:236), which
#   for a TranslateSay is the node itself -- so Say.execute() says the English
#   original, the mod's filter sees English and replaces normally, and the
#   string table translates the result inside renpy.substitute().
#
#       English -> mod replaces -> string table -> German
#
#   game/tl/<language>/ is never touched; the rewrite happens in memory only.
#
# The price
#   Translate blocks are keyed by position, string translations by text. Where
#   one English line has several different translations, only the first
#   survives. Measured against the German translation of Eternum 0.9.5:
#   571 of 55955 distinct lines were ambiguous, costing 677 of 71793
#   translations (0.94%), nearly all of them capitalisation variants of the
#   same sentence. The exact numbers for the installed translation are logged
#   at startup and available via _im_tl_convert_stats.
#
# Turn it off with  _im_tl_convert_enabled = False  below.
################################################################################

init -900 python:
    import time as _im_tl_time

    # This file sorts before im_translation.rpy, so at the same init priority
    # its names are not defined yet. Only function bodies use them (at runtime,
    # long after init), but _im_bi is cheap enough to keep local.
    import builtins as _im_bi

    _im_tl_convert_enabled = True

    # Languages already converted, so the callback is idempotent when the
    # player switches back and forth.
    _im_tl_converted_languages = set()

    # {language: dict of counters} -- see _im_tl_convert_language().
    _im_tl_convert_stats = {}

    def _im_tl_node_text(node):
        """
        The say text of a Translate/TranslateSay node.

        Ren'Py 8.2+ folds `Translate` + single `Say` + `EndTranslate` into one
        TranslateSay that carries `.what` directly; older blocks keep the Say
        inside `.block`. Handle both.
        """
        what = getattr(node, "what", None)
        if what is not None:
            return what

        for b in (getattr(node, "block", None) or ()):
            if isinstance(b, renpy.ast.Say):
                return getattr(b, "what", None)

        return None

    def _im_tl_key_forms(s):
        """
        The forms of `s` that can actually reach the string table.

        The lookup happens on whatever say_menu_text_filter returned, and the
        mod's filter strips multi-mod tags and runs filter_text_tags() before
        handing the line on. A line without braces or brackets passes through
        both untouched, which is the overwhelming majority -- checking for that
        first keeps the conversion of ~72k blocks fast.
        """
        if ("{" not in s) and ("[" not in s):
            return (s,)

        f = globals().get("_im_tlx_final_form")
        if callable(f):
            try:
                forms = f(s)
                if forms:
                    return forms
            except Exception:
                pass
        return (s,)

    def _im_tl_convert_language(language):
        """
        Converts every translate block for `language` into string translations
        and removes the blocks. Returns a stats dict, or None if there was
        nothing to do.
        """
        if not language:
            return None
        if language in _im_tl_converted_languages:
            return None

        tl = renpy.game.script.translator
        table = tl.strings[language].translations

        started = _im_tl_time.time()

        lines = 0          # translate blocks consumed
        added = 0          # source lines that gained a string translation
        identical = 0      # blocks whose translation equals the original
        conflicts = 0      # source lines that already had a different value
        kept_existing = 0  # entries owned by the mod or a strings block

        for (ident, lang), node in _im_bi.list(tl.language_translates.items()):
            if lang != language:
                continue

            src = tl.default_translates.get(ident)
            if src is None:
                # An orphan translation -- lookup_translate() would raise a
                # KeyError on the fallback, so leave this one alone.
                continue

            english = _im_tl_node_text(src)
            translated = _im_tl_node_text(node)

            if not english or not translated:
                continue

            lines += 1

            if english != translated:
                first = True
                for key in _im_tl_key_forms(english):
                    current = table.get(key)
                    if current is None:
                        table[key] = translated
                        if first:
                            added += 1
                    elif current != translated:
                        if first:
                            # Either an earlier block translated the same
                            # sentence differently, or the mod owns this line.
                            conflicts += 1
                    else:
                        if first:
                            kept_existing += 1
                    first = False
            else:
                identical += 1

            # Drop the block so the English original executes and the mod's
            # filter gets a line it can match.
            tl.language_translates.pop((ident, language), None)

        if not lines:
            return None

        _im_tl_converted_languages.add(language)

        stats = {
            "blocks": lines,
            "added": added,
            "identical": identical,
            "conflicts": conflicts,
            "already_translated": kept_existing,
            "seconds": round(_im_tl_time.time() - started, 2),
        }
        _im_tl_convert_stats[language] = stats

        _im_tl_log(
            "Eternum-IC tl: converted %d translate blocks for %r in %.2fs "
            "-- %d strings added, %d untranslated, %d ambiguous (kept first), "
            "%d already present."
            % (stats["blocks"], language, stats["seconds"], stats["added"],
               stats["identical"], stats["conflicts"],
               stats["already_translated"])
        )

        return stats

    def _im_tl_convert_callback():
        """Runs on every language change, including the one during startup."""
        if not _im_tl_convert_enabled:
            return
        try:
            _im_tl_convert_language(renpy.game.preferences.language)
        except Exception as e:
            _im_tl_log("Eternum-IC tl: translate-block conversion failed: %r" % e)


init -899 python:
    # change_language() sets preferences.language before running these
    # (translation/__init__.py:800), and _init_language() calls it during
    # startup -- so this fires before the first say statement either way.
    if _im_tl_convert_callback not in renpy.config.change_language_callbacks:
        renpy.config.change_language_callbacks.append(_im_tl_convert_callback)

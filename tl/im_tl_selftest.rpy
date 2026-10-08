################################################################################
# Eternum-IC translation self-test  (developer tool)
#
#     Eternum.exe . imtl
#
# Runs headless (no window, dummy audio) and checks the whole chain:
#   1. did the loader register the mod's strings?
#   2. does renpy.translation.translate_string() return the translation?
#   3. does the extractor produce a usable template?
################################################################################

init -1 python:

    def _im_tl_selftest():
        renpy.arguments.takes_no_arguments()

        out = []

        def say(msg):
            out.append(msg)
            # Eternum.exe is a windowed Python build, so stdout may silently
            # discard output without raising. Always write the diagnostic log.
            _im_tl_log(msg)
            try:
                print(msg)
            except Exception:
                pass

        say("=" * 72)
        say("Eternum-IC translation self-test")
        say("=" * 72)

        say("mod tl dir      : %s" % _im_tl_dir())
        langs = _im_tl_languages()
        say("languages found : %r" % (langs,))
        lang = langs[0] if langs else "German"
        say("testing language: %r" % lang)

        tl = renpy.game.script.translator
        table = tl.strings[lang].translations
        say("strings in table: %d" % len(table))
        say("stats from init  : %r" % (getattr(store, "_im_tl_stats", "MISSING"),))
        say("language known  : %s" % (lang in tl.languages))

        say("runtime menu hooks:")
        for _im_hook_name, _im_hook in (
            ("store.menu", getattr(store, "menu", None)),
            ("exports.menu", getattr(renpy.exports, "menu", None)),
            ("exports.display_menu", getattr(renpy.exports, "display_menu", None)),
        ):
            _im_hook_code = getattr(_im_hook, "__code__", None)
            say("  %s: %r (%s:%s)" % (
                _im_hook_name,
                _im_hook,
                getattr(_im_hook_code, "co_filename", "?"),
                getattr(_im_hook_code, "co_firstlineno", "?"),
            ))
        _im_choice_screen = renpy.display.screen.get_screen_variant("choice")
        say("  choice screen: %r location=%r ast=%r" % (
            _im_choice_screen,
            getattr(_im_choice_screen, "location", None),
            getattr(_im_choice_screen, "ast", None),
        ))

        # Force the language on so translate_string() resolves against it.
        renpy.game.preferences.language = lang

        say("-" * 72)
        say("Lookup test (what renpy.substitute() will do):")
        probes = [
            "Full Incest (Nancy as Mom and Annie as sister)",
            "I only want Nancy as Mom",
            "*Laughs* I'm sure she will. She is your mother after all.",
            "My name is [mc] [lastname]. I was born into a family of five in the "
            "city of Kredon, a relatively small town on the west coast of the "
            "United States.",
            "This line is not in any translation file.",
        ]
        hits = 0
        for p in probes:
            got = renpy.translation.translate_string(p, lang)
            ok = got != p
            hits += 1 if ok else 0
            say("  [%s] %s" % ("HIT " if ok else "miss", got[:96]))

        say("-" * 72)
        say("Filter test (mod replacement must keep [mc] intact):")

        # Turn the mod on the way the opt-in menu would.
        store.annie_incest = True
        store.annie_mom = True
        store.annie_sister = True
        try:
            _im_sync_adad_alias()
        except Exception:
            pass

        original = ("My name is [mc] [lastname]. I was born in the city of Kredon, "
                    "a relatively small town on the west coast of the United States.")
        replaced = _in_transform_text(original, resolve_names=False)
        say("  original : %s" % original[:96])
        say("  replaced : %s" % replaced[:96])
        say("  keeps [mc]/[lastname] : %s" % ("[mc]" in replaced and "[lastname]" in replaced))
        say("  changed by mod        : %s" % (replaced != original))
        translated = renpy.translation.translate_string(replaced, lang)
        say("  translated            : %s" % translated[:96])
        say("  full chain works      : %s" % (translated != replaced))

        say("-" * 72)
        say("Multi-Mod compatibility (translate before decoration/substitution):")
        filtered = renpy.config.say_menu_text_filter(original)
        say("  filtered dialogue     : %s" % filtered[:96])
        say("  placeholders preserved: %s" % ("[mc]" in filtered and "[lastname]" in filtered))
        say("  translated in filter  : %s" % (filtered != replaced))
        early_substituted = renpy.substitute(
            filtered,
            scope={"mc": "Sebastian", "lastname": "Wendt"},
            translate=False,
        )
        say("  after early names     : %s" % early_substituted[:96])
        say("  stays translated      : %s" % (early_substituted != replaced))

        reported = "Hey [mc], I can't wait to hear all about what happened to you and Annie!"
        filtered_reported = renpy.config.say_menu_text_filter(reported)
        shown_reported = renpy.substitute(
            filtered_reported,
            scope={"mc": "Sebastian"},
            translate=False,
        )
        say("  reported screenshot   : %s" % shown_reported)
        say("  screenshot translated : %s" % (filtered_reported != reported))

        choice = "Full Incest (Nancy as Mom and Annie as sister)"
        filtered_choice = renpy.config.say_menu_text_filter(choice)
        decorated_choice = "1. " + filtered_choice
        say("  decorated choice      : %s" % decorated_choice)
        say("  choice translated     : %s" % (filtered_choice != choice))
        numbered_choice = "1. " + choice
        filtered_numbered = renpy.config.say_menu_text_filter(numbered_choice)
        say("  pre-numbered choice   : %s" % filtered_numbered)
        say("  numbered translated   : %s" % (filtered_numbered != numbered_choice))

        points_choice = "There's no need for that [pink][mt](Mom +1)"
        filtered_points = renpy.config.say_menu_text_filter(points_choice)
        say("  relationship points  : %s" % filtered_points)
        say("  points translated     : %s" % (
            filtered_points != points_choice and "(Mom +1)" in filtered_points
        ))

        numbered_points = "3. " + points_choice
        filtered_numbered_points = renpy.config.say_menu_text_filter(numbered_points)
        say("  numbered points      : %s" % filtered_numbered_points)
        say("  numbered points OK   : %s" % (
            filtered_numbered_points != numbered_points
            and "(Mom +1)" in filtered_numbered_points
        ))
        say("-" * 72)
        say("Base-game line via the converter:")
        say("  converter stats : %r" % (_im_tl_convert_stats.get(lang),))

        tl2 = renpy.game.script.translator
        shown = 0
        for ident, node in tl2.default_translates.items():
            what = getattr(node, "what", None)
            if not what or len(what) < 40:
                continue
            # What the Say node will hand to say_menu_text_filter now.
            resolved = tl2.lookup_translate(ident, getattr(node, "alternate", None))
            if getattr(resolved, "what", None) != what:
                continue                      # still shadowed by a block
            after_mod = _in_transform_text(what, resolve_names=False)
            translated = renpy.translation.translate_string(after_mod, lang)
            if translated == after_mod:
                continue                      # no translation for this one
            say("  EN : %s" % what[:86])
            say("  TL : %s" % translated[:86])
            shown += 1
            if shown >= 3:
                break
        say("  blocks still shadowing base lines : %d"
            % sum(1 for (i, l) in tl2.language_translates if l == lang))
        say("  end-to-end samples that worked    : %d" % shown)

        say("-" * 72)
        say("Extractor:")
        say("  " + im_tl_extract(lang, filename="selftest_out.json"))

        say("=" * 72)
        say("lookup hits: %d/%d (the last probe is expected to miss)" % (hits, len(probes)))
        say("=" * 72)

        return False   # do not start the game

    renpy.arguments.register_command("imtl", _im_tl_selftest)

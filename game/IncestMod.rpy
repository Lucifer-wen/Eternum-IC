# ==========================
# Incest Mod Translation Version (EXPERIMENTAL)
# - Most features have been replaced by Translations
# - Incest Mod Updates are planned
# ==========================

default persistent.text_offset = 1
# Mod update metadata (Step 1)
define im_mod_version = "1.4.1.2"
default persistent.im_current_version = im_mod_version
default persistent.im_update_info_url = "https://github.com/Lucifer-wen/Eternum-IC/releases/download/mod/version.json"
default persistent.im_update_zip_url = "https://github.com/Lucifer-wen/Eternum-IC/releases/download/mod/IncestMod.zip"
default persistent.im_update_pending = False
default persistent.im_update_enabled = False
default persistent.im_update_zip_path = None
default persistent.im_update_target_version = None
default persistent.im_update_debug_hotkey = True
default persistent.im_reload_hotkey_enabled = True
default _im_reloading_scripts = False

# -----------------------------------------
# Update check (Step 2: check + prompt)
# -----------------------------------------
init python:
    try:
        import json as _im_json
        try:
            import urllib.request as _im_urlreq
        except Exception:
            import urllib2 as _im_urlreq
        import os as _im_os
        import hashlib as _im_hashlib
    except Exception:
        _im_json = None
        _im_urlreq = None

    if not hasattr(store, "_im_update_checked"):
        store._im_update_checked = False
    if not hasattr(store, "_im_update_prompted"):
        store._im_update_prompted = False
    if not hasattr(store, "im_update_info"):
        store.im_update_info = None
    if not hasattr(store, "_im_modlog_path"):
        store._im_modlog_path = None

    def _im_get_basedir():
        try:
            return renpy.config.basedir
        except Exception:
            return None

    def _im_log(msg):
        try:
            if store._im_modlog_path is None:
                basedir = _im_get_basedir()
                if basedir:
                    store._im_modlog_path = _im_os.path.join(basedir, "ModLog.txt")
            with open(store._im_modlog_path, "a") as f:
                f.write(str(msg) + "\n")
        except Exception:
            pass

    def _im_parse_version(v):
        if not v:
            return ()
        parts = str(v).strip().split(".")
        out = []
        for p in parts:
            try:
                out.append(int(p))
            except Exception:
                out.append(0)
        return tuple(out)

    def _im_fetch_update_info():
        if _im_urlreq is None or _im_json is None:
            _im_log("update check: missing urllib/json")
            return None
        url = getattr(persistent, "im_update_info_url", None)
        if not url:
            _im_log("update check: no info URL")
            return None
        try:
            _im_log("update check: fetch url=%s" % url)
            resp = _im_urlreq.urlopen(url, timeout=5)
            data = resp.read()
            try:
                text = data.decode("utf-8")
            except Exception:
                text = data
            try:
                _im_log("update check: body bytes=%d" % (len(data) if data else 0))
                _im_log("update check: body head: %s" % str(text)[:200])
            except Exception:
                pass
            try:
                return _im_json.loads(text)
            except Exception as e:
                _im_log("update check: json parse failed: %r" % e)
                _im_log("update check: body head: %s" % str(text)[:200])
                return None
        except Exception as e:
            _im_log("update check: fetch failed: %r" % e)
            try:
                import ssl as _im_ssl
                _im_log("update check: retry without SSL verification")
                ctx = _im_ssl._create_unverified_context()
                resp = _im_urlreq.urlopen(url, timeout=5, context=ctx)
                data = resp.read()
                try:
                    text = data.decode("utf-8")
                except Exception:
                    text = data
                try:
                    _im_log("update check: body bytes (no-verify)=%d" % (len(data) if data else 0))
                    _im_log("update check: body head (no-verify): %s" % str(text)[:200])
                except Exception:
                    pass
                try:
                    return _im_json.loads(text)
                except Exception as e2:
                    _im_log("update check: json parse failed (no-verify): %r" % e2)
                    _im_log("update check: body head (no-verify): %s" % str(text)[:200])
                    return None
            except Exception as e2:
                _im_log("update check: fetch failed (no-verify): %r" % e2)
            return None

    def _im_check_for_update():
        if store._im_update_checked:
            _im_log("update check: already checked")
            return
        store._im_update_checked = True
        _im_log("update check: start")
        info = _im_fetch_update_info()
        if info is None or not hasattr(info, "get"):
            try:
                _im_log("update check: invalid info type=%s repr=%r" % (type(info), info))
            except Exception:
                _im_log("update check: invalid info")
            return
        try:
            _im_log("update check: info keys=%s" % ",".join(sorted([str(k) for k in info.keys()])))
        except Exception:
            pass
        remote_ver = info.get("version", None)
        remote_url = info.get("url", None) or getattr(persistent, "im_update_zip_url", None)
        remote_hash = info.get("sha256", None)
        local_ver = getattr(persistent, "im_current_version", None)
        _im_log("update check: local=%s remote=%s" % (local_ver, remote_ver))
        if _im_parse_version(remote_ver) > _im_parse_version(local_ver):
            store.im_update_info = {
                "version": remote_ver,
                "url": remote_url,
                "sha256": remote_hash,
            }
            if not store._im_update_prompted:
                store._im_update_prompted = True
                _im_log("update check: prompt")
                try:
                    _im_trigger_update_prompt()
                except Exception:
                    pass
        else:
            _im_log("update check: no update")

    def _im_trigger_update_prompt():
        try:
            # Ensure no lingering UI widgets before opening a menu in a new context.
            _stack = getattr(renpy.ui, "stack", None)
            if _stack:
                while len(_stack) > 1:
                    try:
                        renpy.ui.close()
                    except Exception:
                        break
        except Exception:
            pass
        renpy.call_in_new_context("im_update_prompt")

    def _im_start_update_check():
        if not getattr(persistent, "im_update_enabled", False):
            _im_log("update check: disabled")
            return
        _im_check_for_update()

    def _im_prepare_mods_dir():
        try:
            basedir = _im_get_basedir()
        except Exception:
            basedir = None
        if not basedir:
            _im_log("update apply: no basedir")
            return None
        game_dir = _im_os.path.join(basedir, "game")
        mods_dir = _im_os.path.join(game_dir, "mods")
        try:
            if not _im_os.path.isdir(mods_dir):
                _im_os.makedirs(mods_dir)
        except Exception:
            _im_log("update apply: cannot create mods dir")
            return None
        expected = ("IncestMod.rpy", "IncestLables.rpy", "IncestMod.rpyc", "IncestLables.rpyc")
        found = {name: False for name in expected}
        try:
            for root, _dirs, files in _im_os.walk(game_dir):
                for name in expected:
                    if name in files:
                        found[name] = True
        except Exception:
            _im_log("update apply: walk failed")
            return None
        missing = [name for name, ok in found.items() if not ok]
        if missing:
            try:
                renpy.notify("Missing in game tree: " + ", ".join(missing))
                _im_log("update apply: missing in game tree: %s" % ", ".join(missing))
            except Exception:
                pass
        return mods_dir

    def _im_download_update():
        if _im_urlreq is None:
            _im_log("update download: missing urllib")
            return False
        info = getattr(store, "im_update_info", None) or {}
        url = info.get("url", None) or getattr(persistent, "im_update_zip_url", None)
        target_ver = info.get("version", None)
        if not url:
            _im_log("update download: no url")
            return False
        if _im_prepare_mods_dir() is None:
            _im_log("update download: mods dir failed")
            return False
        basedir = _im_get_basedir()
        if not basedir:
            _im_log("update download: no basedir")
            return False
        zip_path = _im_os.path.join(basedir, "IncestMod_update.zip")
        marker_path = _im_os.path.join(basedir, "ModUpdate.pending")
        try:
            _im_log("update download: start %s" % url)
            resp = _im_urlreq.urlopen(url, timeout=15)
            with open(zip_path, "wb") as f:
                while True:
                    chunk = resp.read(1024 * 64)
                    if not chunk:
                        break
                    f.write(chunk)
        except Exception as e:
            _im_log("update download: failed: %r" % e)
            try:
                import ssl as _im_ssl
                _im_log("update download: retry without SSL verification")
                ctx = _im_ssl._create_unverified_context()
                resp = _im_urlreq.urlopen(url, timeout=15, context=ctx)
                with open(zip_path, "wb") as f:
                    while True:
                        chunk = resp.read(1024 * 64)
                        if not chunk:
                            break
                        f.write(chunk)
            except Exception as e2:
                _im_log("update download: failed (no-verify): %r" % e2)
                return False
        expected = info.get("sha256", None)
        if expected and str(expected).strip() not in ("", "<optional>", "optional"):
            try:
                h = _im_hashlib.sha256()
                with open(zip_path, "rb") as f:
                    for b in iter(lambda: f.read(1024 * 64), b""):
                        h.update(b)
                if h.hexdigest().lower() != str(expected).strip().lower():
                    try:
                        _im_os.remove(zip_path)
                    except Exception:
                        pass
                    _im_log("update download: hash mismatch")
                    return False
            except Exception:
                _im_log("update download: hash check failed")
                return False
        else:
            _im_log("update download: hash check skipped")
        try:
            with open(marker_path, "w") as f:
                f.write(str(target_ver or ""))
        except Exception:
            _im_log("update download: marker write failed")
        persistent.im_update_zip_path = zip_path
        persistent.im_update_pending = True
        persistent.im_update_target_version = target_ver
        _im_log("update download: ok")
        return True

    def _im_apply_update_if_pending():
        basedir = _im_get_basedir()
        marker_path = _im_os.path.join(basedir, "ModUpdate.pending") if basedir else None
        zip_path = getattr(persistent, "im_update_zip_path", None)
        if (not getattr(persistent, "im_update_pending", False)) and marker_path and _im_os.path.isfile(marker_path):
            _im_log("update apply: marker found")
            try:
                with open(marker_path, "r") as f:
                    persistent.im_update_target_version = f.read().strip()
            except Exception:
                pass
            if basedir:
                zip_path = _im_os.path.join(basedir, "IncestMod_update.zip")
                persistent.im_update_zip_path = zip_path
            persistent.im_update_pending = True
        if not getattr(persistent, "im_update_pending", False):
            _im_log("update apply: no pending flag")
            return False
        if not zip_path or not _im_os.path.isfile(zip_path):
            _im_log("update apply: missing zip path")
            return False
        mods_dir = _im_prepare_mods_dir()
        if not mods_dir:
            _im_log("update apply: no mods dir")
            return False
        if not basedir:
            _im_log("update apply: no basedir")
            return False
        game_dir = _im_os.path.join(basedir, "game")
        expected = ("IncestMod.rpy", "IncestLables.rpy", "IncestMod.rpyc", "IncestLables.rpyc")
        try:
            import zipfile as _im_zipfile
        except Exception:
            _im_log("update apply: no zipfile module")
            return False
        extracted = []
        payload = {}
        try:
            zf = _im_zipfile.ZipFile(zip_path, "r")
            names = zf.namelist()
            for name in ("IncestMod.rpy", "IncestLables.rpy"):
                for member in names:
                    if _im_os.path.basename(member) == name:
                        payload[name] = zf.read(member)
                        extracted.append(name)
                        break
        except Exception:
            try:
                renpy.log("update apply failed: zip read/extract error")
            except Exception:
                pass
            _im_log("update apply: zip read/extract error")
            return False
        finally:
            try:
                zf.close()
            except Exception:
                pass
        missing = [n for n in ("IncestMod.rpy", "IncestLables.rpy") if n not in extracted]
        if missing:
            try:
                renpy.notify("Update ZIP missing: " + ", ".join(missing))
                renpy.log("update apply failed: missing in zip: %s" % ", ".join(missing))
            except Exception:
                pass
            _im_log("update apply: missing in zip: %s" % ", ".join(missing))
            return False
        try:
            for root, _dirs, files in _im_os.walk(game_dir):
                for name in expected:
                    if name in files:
                        try:
                            _im_os.remove(_im_os.path.join(root, name))
                        except Exception:
                            pass
        except Exception:
            try:
                renpy.log("update apply failed: could not remove old files")
            except Exception:
                pass
            _im_log("update apply: remove old files failed")
            return False
        try:
            for name, data in payload.items():
                with open(_im_os.path.join(mods_dir, name), "wb") as f:
                    f.write(data)
        except Exception:
            try:
                renpy.log("update apply failed: write new files failed")
            except Exception:
                pass
            _im_log("update apply: write new files failed")
            return False
        try:
            _im_os.remove(zip_path)
        except Exception:
            pass
        try:
            if marker_path and _im_os.path.isfile(marker_path):
                _im_os.remove(marker_path)
        except Exception:
            pass
        target_ver = getattr(persistent, "im_update_target_version", None)
        if target_ver:
            persistent.im_current_version = target_ver
        persistent.im_update_pending = False
        persistent.im_update_zip_path = None
        persistent.im_update_target_version = None
        _im_log("update apply: done version=%s" % (target_ver or "unknown"))
        try:
            _im_reload_scripts()
            return True
        except Exception:
            pass
        try:
            renpy.notify("Mod update applied: %s. Please reload scripts manually (F10)." % (target_ver or "unknown"))
        except Exception:
            pass
        return False

screen _im_update_autocall():
    if (
        (renpy.get_screen('choice') is None)
        and (not renpy.context()._main_menu)
        and (not _im_reloading_scripts)
    ):
        timer 0.1 action Function(_im_start_update_check)

init python:
    def _im_reload_scripts():
        """
        Reload Ren'Py scripts without restarting the entire client.
        """
        global _im_reloading_scripts
        if _im_reloading_scripts:
            try:
                renpy.notify("Script reload already running.")
            except Exception:
                pass
            return
        try:
            renpy.notify("Reloading scripts...")
        except Exception:
            pass
        _im_reloading_scripts = True
        try:
            if not hasattr(renpy, "reload_script"):
                _im_reloading_scripts = False
                renpy.notify("Script reload not supported on this build.")
                return
            renpy.reload_script()
        except (renpy.game.UtterRestartException, renpy.game.RestartTopContext):
            # Expected during successful reloads; let Ren'Py handle them.
            raise
        except Exception as e:
            _im_reloading_scripts = False
            msg = "Script reload failed: %s" % (e or e.__class__.__name__)
            try:
                renpy.notify(msg)
            except Exception:
                pass
            try:
                _im_log(msg)
            except Exception:
                pass

init python:
    try:
        if "_im_update_autocall" not in config.overlay_screens:
            config.overlay_screens.append("_im_update_autocall")
    except Exception:
        pass

screen _im_update_debug_hotkey():
    if persistent.im_update_debug_hotkey:
        key "K_F9" action Function(renpy.call_in_new_context, "im_debug_set_version")

screen _im_reload_scripts_hotkey():
    if persistent.im_reload_hotkey_enabled:
        key "K_F10" action Function(_im_reload_scripts)

init python:
    try:
        if "_im_update_debug_hotkey" not in config.overlay_screens:
            config.overlay_screens.append("_im_update_debug_hotkey")
        if "_im_reload_scripts_hotkey" not in config.overlay_screens:
            config.overlay_screens.append("_im_reload_scripts_hotkey")
    except Exception:
        pass

label im_debug_set_version:
    $ _curr = getattr(persistent, "im_current_version", "unknown")
    $ _new = renpy.input("Set mod version:", default=_curr, length=32)
    $ _new = _new.strip()
    if _new:
        $ persistent.im_current_version = _new
        $ renpy.save_persistent()
        $ _im_update_checked = False
        $ renpy.notify("Mod version set to " + _new)
    return

init 5 python:
    try:
        _im_apply_update_if_pending()
    except Exception:
        pass

label im_update_prompt:
    $ _info = getattr(store, "im_update_info", None)
    $ _ver = _info.get("version", None) if _info else None
    $ _curr = getattr(persistent, "im_current_version", None)
    menu:
        "Incest Mod update available (current [_curr], latest [_ver]). Download and install now?"
        "Yes":
            $ _ok = _im_download_update()
            if _ok:
                $ _applied = _im_apply_update_if_pending()
                if not _applied:
                    $ renpy.notify("Update applied. Press F10 to reload scripts manually.")
            else:
                $ renpy.notify("Update download failed.")
        "No":
            $ persistent.im_update_pending = False
    return



# -----------------------------------------
# Preferences screen override with toggle
# -----------------------------------------
init 1000:
    screen preferences():

        tag menu

        key 'game_menu' action Return()

        add "gui/msp5/pref_bg.png"
        label _("{color=#f1f1f1}{size=100}PREFERENCES") xpos 110 ypos 25

        default edit_mode   = False

        viewport:
            xsize 1060
            ysize 721
            xpos 140
            ypos 219
            scrollbars "vertical"
            mousewheel True
            draggable True
            pagekeys True
            vbox:
                hbox:
                    style_prefix "slider"
                    box_wrap True

                    vbox:

                        label _("Text Speed")

                        bar value Preference("text speed")

                        label _("Auto-Forward Time")

                        bar value Preference("auto-forward time")
                null height (4 * gui.pref_spacing)
                hbox:
                    style_prefix "slider"
                    vbox:

                        if config.has_music:
                            label _("Music Volume")

                            hbox:
                                bar value Preference("music volume")

                        if config.has_sound:

                            label _("Sound Volume")

                            hbox:
                                bar value Preference("sound volume")

                                if config.sample_sound:
                                    textbutton _("Test") action Play("sound", config.sample_sound)


                        #if config.has_voice:
                            #label _("Voice Volume")
                            #hbox:
                            #    bar value Preference("voice volume")
                            #    if config.sample_voice:
                            #        textbutton _("Test") action Play("voice", config.sample_voice)

                        if config.has_music or config.has_sound or config.has_voice:
                            null height gui.pref_spacing

                            textbutton _("Mute All"):
                                action Preference("all mute", "toggle")
                                style "mute_all_button"

                null height (4 * gui.pref_spacing)

                hbox:
                    style_prefix "slider"
                    box_wrap True

                    vbox:
                        label _("Text Size ([persistent.text_size]/50)")
                        bar:
                            value FieldValue(persistent, "text_size", offset=20, range=30, style="slider")
                        textbutton _("Set to default") action InvertSelected(SetVariable("persistent.text_size", gui.text_size))


                        label _("Text Outline ([persistent.text_outline]/4)")
                        bar:
                            value FieldValue(persistent, "text_outline", range=4, style="slider")
                        textbutton _("Set to default") action InvertSelected(SetVariable("persistent.text_outline", 2))

                        label _("Text Outline Offset ([persistent.text_offset]/4)")
                        bar:
                            value FieldValue(persistent, "text_offset", range=4, style="slider")
                        textbutton _("Set to default") action InvertSelected(SetVariable("persistent.text_offset", 1))

                null height (4 * gui.pref_spacing)
                hbox:
                    style_prefix "slider"
                    vbox:
                        $ percent_value = int(persistent.textbox_opacity * 100)
                        label _("Textbox Opacity ([percent_value]%)")
                        bar:
                            value FieldValue(persistent, "textbox_opacity", range=1.0, style="slider")
                        textbutton _("Set to default") action InvertSelected(SetVariable("persistent.textbox_opacity", 0.0))


                        label _("Textbox Width ([persistent.textbox_width]/1646)")
                        bar:
                            value FieldValue(persistent, "textbox_width", offset=1116, range=530, style="slider")
                        textbutton _("Set to default") action InvertSelected(SetVariable("persistent.textbox_width", gui.dialogue_width))

                        label _("Textbox Height ([persistent.textbox_height]/350)")
                        bar:
                            value FieldValue(persistent, "textbox_height", offset=100, range=250, style="slider")
                        textbutton _("Set to default") action InvertSelected(SetVariable("persistent.textbox_height", gui.textbox_height))
                null height (4 * gui.pref_spacing)
        viewport:
            xsize 480
            ysize 633
            xpos 1300
            ypos 219
            scrollbars "vertical"
            mousewheel True
            draggable True
            pagekeys True
            vbox:
                xalign 0.5
                yalign 0.5

                if not main_menu and not _in_replay and nicknameunlock:
                    vbox:
                        label _("Edit Nickname")
                        if not edit_mode:
                            textbutton '[nickname]' action SetScreenVariable('edit_mode', True)
                        else:
                            key 'dismiss' action SetScreenVariable('edit_mode', False)
                            key 'input_enter' action SetScreenVariable('edit_mode', False)
                            input:
                                value FieldInputValue(store, 'nickname', returnable=True)
                if renpy.variant("pc"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                # Note to translators: This preference menu appears automatically
                # when more than one language is available. By default, it will use
                # the internal language name of your translation. If you want to
                # provide a better title for your language, add a snippet like this
                # to the top of your screens.rpy translation file (but outside any
                # "translate strings" block):
                #
                # init python:
                #     language_titles["chinese"] = "„÷đ‘-Î"
                #     language_title_fonts["chinese"] = "tl/chinese/font/Thin.ttf"
                #
                # You can omit setting a different font if you don't need it, but if
                # you do set one, you of course need to provide that font with your
                # translation files.
                $ other_lang = False
                for lang in renpy.known_languages():
                    if "incest_" not in lang:
                        $ other_lang = True
                        break
                if other_lang:
                    vbox:
                        style_prefix "radio"
                        label _("Language")
                        textbutton _("English{#prefs}"):
                            action Language(None)
                        for lang in renpy.known_languages():
                            if "incest_" not in lang:
                                $ option_title = language_titles.get(lang, lang)
                                $ option_font = language_title_fonts.get(lang, None)
                                textbutton option_title:
                                    action Language(lang)
                                    if option_font is not None:
                                        text_font option_font

                if renpy.loadable("achievements/achievements.rpy"):
                    vbox:
                        style_prefix "radio"
                        label _("Walkthrough")
                        textbutton _("Enabled") action [SetVariable("walk_points", "45E3C2"), SetVariable("walk_path", "FF073A"), SetVariable("walk_points_chat", "45E3C2"), SetVariable("walk_path_chat", "FF073A")]
                        textbutton _("Disabled") action [SetVariable("walk_points", "CCCCCC"), SetVariable("walk_path", "CCCCCC"), SetVariable("walk_points_chat", "000000"), SetVariable("walk_path_chat", "000000")]

                    vbox:
                        style_prefix "radio"
                        label _("Music popups")
                        textbutton _("Enabled") action [SetVariable("music_popup_enabled", True)]
                        textbutton _("Disabled") action [SetVariable("music_popup_enabled", False)]

                vbox:
                    style_prefix "radio"
                    label _("Rollback Side")
                    textbutton _("Disable") action Preference("rollback side", "disable")
                    textbutton _("Left") action Preference("rollback side", "left")
                    textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    #textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                vbox:
                    style_prefix "radio"
                    label _("Quick Menu")
                    textbutton _("Enabled") action SetField(persistent,"quick_menu", True)
                    textbutton _("Disabled") action SetField(persistent,"quick_menu", False)

                vbox:
                    style_prefix "radio"
                    label _("Interface Motion")
                    textbutton _("Enabled") action SetField(persistent,"motion", 1.0)
                    textbutton _("Disabled") action SetField(persistent,"motion", .0)

                    ## Additional vboxes of type "radio_pref" or "check_pref" can be
                    ## added here, to add additional creator-defined preferences.

                vbox:
                    style_prefix "radio"
                    label _("Incest Mod Updates")
                    textbutton _("Enabled"):
                        action [
                            SetField(persistent, "im_update_enabled", True),
                            SetVariable("_im_update_checked", False),
                            Function(_im_check_for_update),
                        ]
                        selected persistent.im_update_enabled
                    textbutton _("Disabled"):
                        action SetField(persistent, "im_update_enabled", False)
                        selected (not persistent.im_update_enabled)

                vbox:
                    style_prefix "radio"
                    label _("Incest Mode")
                    for lang in ["incest_full", "incest_mom", "incest_only_sister", "incest_half_sister", "incest_aunt"]:
                        if lang in renpy.known_languages():
                            $ option_title = language_titles.get(lang, lang)
                            $ option_font = language_title_fonts.get(lang, None)
                            textbutton option_title:
                                action Language(lang)
                                if option_font is not None:
                                    text_font option_font
                    textbutton _("Disabled"):
                        action Language(None)

                null height (4 * gui.pref_spacing)


        # textbutton "Return" action Return()    xpos 91    yalign 0.93    yoffset -45
        default return_h = None
        button:
            action Return()
            focus_mask True
            image "gui/msp5/return.png"
            image im.MatrixColor("gui/msp5/return.png", im.matrix.colorize('#f1f1f180', '#f1f1f180')):
                if return_h == 1:
                    at transform:
                        easein_quint (0.5 * persistent.motion) alpha 1.0 blur 0
                elif return_h == 0:
                    at transform:
                        easein_quint (0.5 * persistent.motion) alpha 0.0 blur 5
                else:
                    at transform:
                        alpha 0.0
            hovered [ SetLocalVariable("return_h", 1) ]
            unhovered [ SetLocalVariable("return_h", 0) ]

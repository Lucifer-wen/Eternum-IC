# ==========================
# Annie Opt-In (FIXED SKELETON)
# - Replacement order fixed
# - Handles [mc] placeholder vs. resolved name
# - Speaker-aware "Nancy" -> "Mom" only for MC lines
# ==========================

default annie_incest = False
default annie_sister = False
default annie_mom = False
default annie_half_sister = False
default annie_aunt = False
# default im_cousin_override = False
default _in_incest_prompted = False
default im_redirect_enabled = True
default im_label_overrides = {}
default im_debug_redirect = False
default persistent.im_incest_mode = None
default persistent.text_offset = 1
# Mod update metadata (Step 1)
default persistent.im_mod_version = "1.4.1.2"
default persistent.im_update_info_url = "https://github.com/Lucifer-wen/Eternum-IC/releases/download/mod/version.json"
default persistent.im_update_zip_url = "https://github.com/Lucifer-wen/Eternum-IC/releases/download/mod/IncestMod.zip"
default persistent.im_update_pending = False
default persistent.im_update_enabled = False
default persistent.im_update_zip_path = None
default persistent.im_update_target_version = None
default persistent.im_update_debug_hotkey = True
default persistent.im_reload_hotkey_enabled = True
default _im_reloading_scripts = False
# default persistent.im_cousin_override = None

init python:
    def _im_strip_multimod_tags(text):
        """
        Remove unsupported multi-mod tags (e.g. [gr]) when
        MultiMod is not installed. Prevents NameError crashes if the tag
        isn't defined in the current environment.
        """
        try:
            if renpy.loadable("mod_additions/mod_options.rpy"):
                return text
        except Exception:
            pass
        try:
            import re
            t = text
            t = re.sub(r'\[red\]\(Insist\)', '(Insist)', t)
            t = re.sub(r'\(attack afterward\)', '', t)
            t = re.sub(r'\[(?:gr|mm|red|blue|green|pink|mt|nova_pts|nancy_pts|dalia_pts|annie_pts|alex_pts|penelope_pts|luna_pts|calypso_pts)\](?:(?:\{[^{}]+\})?\([^()]+\)(?:\{\/[^{}]+\})?)?', '', t)
            return t.strip()
        except Exception:
            return text

    def _im_define_multimod_tags():
        try:
            if renpy.loadable("mod_additions/mod_options.rpy"):
                return
        except Exception:
            pass
        for _tag in ("gr", "mm", "red", "blue", "green", "pink", "mt", "nova_pts", "nancy_pts", "dalia_pts", "annie_pts", "alex_pts", "penelope_pts", "luna_pts", "calypso_pts"):
            if not hasattr(store, _tag):
                setattr(store, _tag, "")

    _im_define_multimod_tags()

    def _im_strip_bonusmod_tags(text):
        """
        Remove unsupported Bonus Mod tags (e.g. {color=[walk_points]}) when
        Bonus Mod is not installed. Prevents NameError crashes if the tag
        isn't defined in the current environment.
        """
        try:
            if renpy.loadable("achievements/achievements.rpy"):
                return text
        except Exception:
            pass
        try:
            import re
            t = text
            t = re.sub(r'\{color=\[(?:walk_points|walk_path|walk_points_chat|walk_path_chat|computer_color|birthday_color|reception_color|read_this_color|leave_color|stand_up_color|right_elevator_color|left_elevator_color)\]\}', '', t)
            return t.strip()
        except Exception:
            return text

    def _im_define_bonusmod_tags():
        try:
            if renpy.loadable("achievements/achievements.rpy"):
                return
        except Exception:
            pass
        for _tag in ("walk_points", "walk_path", "computer_color", "birthday_color", "reception_color", "read_this_color", "leave_color", "stand_up_color", "right_elevator_color", "left_elevator_color"):
            if not hasattr(store, _tag):
                setattr(store, _tag, "CCCCCC")
        for _tag in ("walk_points_chat", "walk_path_chat"):
            if not hasattr(store, _tag):
                setattr(store, _tag, "000000")

    _im_define_bonusmod_tags()

    def _im_apply_persistent_mode():
        mode = getattr(persistent, "im_incest_mode", None)
        # store.im_cousin_override = bool(getattr(persistent, "im_cousin_override", False))
        if mode == "incest":
            store.annie_incest = True
            store.annie_sister = True
            store.annie_mom = True
            store.annie_half_sister = False
            store.annie_aunt = False
            store._in_incest_prompted = True
        elif mode == "mom":
            store.annie_incest = False
            store.annie_sister = False
            store.annie_mom = True
            store.annie_half_sister = False
            store.annie_aunt = False
            store._in_incest_prompted = True
        elif mode == "sister":
            store.annie_incest = False
            store.annie_sister = True
            store.annie_mom = False
            store.annie_half_sister = False
            store.annie_aunt = False
            store._in_incest_prompted = True
        elif mode == "half":
            store.annie_incest = False
            store.annie_sister = False
            store.annie_mom = True
            store.annie_half_sister = True
            store.annie_aunt = False
            store._in_incest_prompted = True
        elif mode == "aunt":
            store.annie_incest = False
            store.annie_sister = False
            store.annie_mom = False
            store.annie_half_sister = False
            store.annie_aunt = True
            store._in_incest_prompted = True
        elif mode == "off":
            store.annie_incest = False
            store.annie_sister = False
            store.annie_mom = False
            store.annie_half_sister = False
            store.annie_aunt = False
            store._in_incest_prompted = True

    try:
        _im_apply_persistent_mode()
    except Exception:
        pass

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
        local_ver = getattr(persistent, "im_mod_version", None)
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
            persistent.im_mod_version = target_ver
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
    $ _curr = getattr(persistent, "im_mod_version", "unknown")
    $ _new = renpy.input("Set mod version:", default=_curr, length=32)
    $ _new = _new.strip()
    if _new:
        $ persistent.im_mod_version = _new
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
    $ _curr = getattr(persistent, "im_mod_version", None)
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
# Label redirect map (edit like the text maps)
# - Add entries as "old_label": "new_label",
# - New labels can live in IncestLables.rpy
# -----------------------------------------
init python:
    # Flat map (backwards compatible). Behaves like base profile.
    im_label_map = {

        
    }

    # Conditional maps. Only angewendet, wenn der jeweilige Modus aktiv ist.
    # - Base: nur wenn `annie_mom` True (zusätzlich zu `im_label_map`)
    # - Incest: nur wenn `annie_incest` True
    # - Sister: nur wenn `annie_sister` True (eigene Map)
    # - Full Incest: nutzt `im_label_map_sister`
    im_label_map_base = {
        "daliacove": "daliacove_mod",
    }
    im_label_map_incest = {
        # Beispiel: "some_label": "some_label_incest_mod",
    }
    im_label_map_sister = {
        "welcome": "welcome_mod",
        "_call_chat_21":"mod_call_chat_21",        
    }
    im_label_map_only_sister = {
        # Beispiel: "some_label": "some_label_sister_mod",
    }
    # - Half-Sister: nur wenn `annie_half_sister` True
    im_label_map_half = {
        # Beispiel: "some_label": "some_label_half_mod",
    }
    # - Aunt Mode: nur wenn `annie_aunt` True
    im_label_map_aunt = {
        # Beispiel: "some_label": "some_label_aunt_mod",
    }
    # - Disabled/Off: greift, wenn kein anderer Modus aktiv ist
    im_label_map_off = {
        # Beispiel: "some_label": "some_label_disabled_mod",
    }

# (Optional) You can still push maps into Ren'Py's config manually via
# `im_apply_label_map()`, but dynamic routing below no longer relies on it.

# -----------------------------------------
# Dynamic label intercept (runtime reroute)
# - Catches labels on entry, not upfront
# - Uses explicit map (`im_label_map`) or runtime overrides
# -----------------------------------------
init python early hide:
    from renpy import exports as rpy
    from renpy import config as rconfig
    import store

    _im_label_chain = []

    if not hasattr(store, "_im_redirecting"):
        store._im_redirecting = False
    if not hasattr(store, "_im_prev_flags"):
        store._im_prev_flags = (bool(getattr(store, 'annie_incest', False)), bool(getattr(store, 'annie_sister', False)), bool(getattr(store, 'annie_mom', False)), bool(getattr(store, 'annie_half', False)), bool(getattr(store, 'annie_aunt', False)))

    def _im_collect_maps():
        def _map(name):
            data = getattr(store, name, None)
            return data if isinstance(data, dict) else {}

        # Basis: alte Flat-Map (immer aktiv)
        newmap = {}
        newmap.update(_map("im_label_map"))

        def _merge(name):
            data = _map(name)
            if data:
                newmap.update(data)

        incest_active = bool(getattr(store, "annie_incest", False))
        sister_active = bool(getattr(store, "annie_sister", False))
        mom_active = bool(getattr(store, "annie_mom", False))
        half_active = bool(getattr(store, "annie_half_sister", False))
        aunt_active = bool(getattr(store, "annie_aunt", False))

        # Mom/Base profile (gilt auch für Half-Sis, da gleiche Mom-Ersatz-Logik)
        if mom_active:
            _merge("im_label_map_base")

        # Mode-specific maps
        if incest_active:
            _merge("im_label_map_incest")
            _merge("im_label_map_sister")
        elif sister_active:
            _merge("im_label_map_only_sister")

        if half_active:
            _merge("im_label_map_half")

        if aunt_active:
            _merge("im_label_map_aunt")

        if not any((incest_active, sister_active, mom_active, half_active, aunt_active)):
            _merge("im_label_map_off")

        runtime = dict(getattr(store, "im_label_overrides", {}))
        newmap.update(runtime)

        # Alle Schlüssel, die von unseren Profilen/Overrides verwaltet werden
        keys_all = set()
        for name in (
            "im_label_map",
            "im_label_map_base",
            "im_label_map_incest",
            "im_label_map_sister",
            "im_label_map_only_sister",
            "im_label_map_half",
            "im_label_map_aunt",
            "im_label_map_off",
        ):
            keys_all.update(_map(name).keys())
        keys_all.update(runtime.keys())
        return newmap, keys_all

    def _im_apply_map_to_config():
        # Keep function for manual/compat usage, but dynamic routing
        # now happens in the callback; we avoid mutating config by default.
        try:
            if getattr(rconfig, "label_overrides", None) is None:
                rconfig.label_overrides = {}
            newmap, keys_all = _im_collect_maps()
            for k in list(keys_all):
                rconfig.label_overrides.pop(k, None)
            rconfig.label_overrides.update(newmap)
        except Exception:
            pass

    def _im_refresh_if_flags_changed():
        curr = (bool(getattr(store, 'annie_incest', False)), bool(getattr(store, 'annie_sister', False)), bool(getattr(store, 'annie_mom', False)), bool(getattr(store, 'annie_half', False)), bool(getattr(store, 'annie_aunt', False)))
        store._im_prev_flags = curr

    def _im_set_override(src, dst):
        # set runtime override; callback will honor it immediately on next entry
        store.im_label_overrides[src] = dst

    def _im_clear_override(src=None):
        if src is None:
            store.im_label_overrides.clear()
        else:
            store.im_label_overrides.pop(src, None)

    def _im_toggle_redirect(on=None):
        if on is None:
            store.im_redirect_enabled = not store.im_redirect_enabled
        else:
            store.im_redirect_enabled = bool(on)

    def _im_get_override(target):
        # Build current effective map and resolve
        effective, _ = _im_collect_maps()
        ov = effective.get(target, None)
        if ov and rpy.has_label(ov):
            return ov
        return None

    def _im_label_cb(label, *a, **kw):
        # Keep mapping in sync with mode switches
        try:
            _im_refresh_if_flags_changed()
        except Exception:
            pass
        for cb in list(_im_label_chain):
            try:
                cb(label, *a, **kw)
            except Exception:
                pass

        if not getattr(store, "im_redirect_enabled", True):
            return
        if getattr(store, "_im_redirecting", False):
            return

        try:
            if not label:
                return
            alt = _im_get_override(label)
            if getattr(store, 'im_debug_redirect', False):
                try:
                    rpy.notify("IM check: {} -> {}".format(label, alt or '-'))
                except Exception:
                    pass
            if alt and alt != label:
                store._im_redirecting = True
                try:
                    if getattr(store, 'im_debug_redirect', False):
                        try:
                            rpy.notify("IM redirect: {} -> {}".format(label, alt))
                        except Exception:
                            pass
                    rpy.jump(alt)
                finally:
                    store._im_redirecting = False
        except Exception:
            store._im_redirecting = False
            return

    def _im_register_prev_label_cb(cb):
        if cb and cb is not _im_label_cb and cb not in _im_label_chain:
            _im_label_chain.append(cb)

    def _im_ensure_label_callback():
        curr = getattr(rconfig, "label_callback", None)
        if curr is not _im_label_cb:
            _im_register_prev_label_cb(curr)
            rconfig.label_callback = _im_label_cb

    _im_ensure_label_callback()

    # Keep overrides in sync before each statement executes
    def _im_stmt_cb(loc):
        try:
            _im_refresh_if_flags_changed()
            _im_apply_map_to_config()
            _im_ensure_label_callback()
        except Exception:
            pass

    try:
        if getattr(rconfig, "statement_callbacks", None) is None:
            rconfig.statement_callbacks = []
        rconfig.statement_callbacks.append(_im_stmt_cb)
    except Exception:
        pass

    # export helpers to store API (without leaking renpy into store)
    store.im_set_override = _im_set_override
    store.im_clear_override = _im_clear_override
    store.im_toggle_redirect = _im_toggle_redirect
    store.im_apply_label_map = _im_apply_map_to_config

# -----------------------------------------
# Replacement maps (CONTENT OMITTED)
# -----------------------------------------
init python:
    mom_map = {
        # -----------------------------------------
        # Nancy as Mom, Penny and Dalia as older sisters
        # They have the same last name as MC
        # -----------------------------------------
        # Proofreader's notes signed with ~BA
        # BM 0000 = Base Map, Line Number
        # Line numbers based on compiled script from v0.9.0, subject to change in future updates
        #    (which already happened in v0.9.4 fml, too lazy to redo all the numbers)
        # -----------------------------------------

    # -----------------------------------------
    # v0.1 script.rpy  Lines 1-9769

        # BM 826
        "My mother left shortly after I was born and my dad was never around much because he was always so focused on his job.":
            "My mother always cared for me, but my dad was never around much. He was always so focused on his job and never made time for our family. This left my mom as the only parent, taking care of three young kids while juggling school.",

        # BM 827
        "That’s actually why we ended up moving to the UK; Dad needed to relocate there to keep his position.":
            "Frustrated, this led to tension between my mom and dad, which boiled over to the point where the two were constantly fighting. My dad's performance at his job started suffering as a result. That's why we ended up moving to the UK.",

        # BM 828
        "I know, I know, this all sounds pretty gloomy... but don't worry! This is not about to be one long sob story.":
            "Dad relocated to keep his job and his sanity. He and Mom agreed he'd take me, while she stayed with my two older sisters. I know it sounds a bit bleak, but don't worry - this isn't a sob story.",

        # BM 952
        "I was saying that I spoke with Nancy.":
            "I was saying that I spoke with your mom.",

        # BM 958
        "*Laughs* I'm sure she will.":
            "*Laughs* I'm sure she will. She is your mother after all.",

        # BM 961 FIXED: Handle both "Nancy" and "Mom" versions
        "(Nancy used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(My mom used to look after me and my sisters in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)",

        # BM 961
        "(Mom used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(My mom used to look after me and my sisters in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)",

        # BM 962 FIXED: Handle both versions
        "(I used to spend the entire afternoon playing with Nancy and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend the entire afternoon playing with Mom and my sister Dalia, but then we had to move and ended up losing touch.)",

        # BM 962
        "(I used to spend the entire afternoon playing with Mom and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend the entire afternoon playing with Mom and my sister Dalia, but then we had to move and ended up losing touch.)",

        # BM 964 FIXED: Handle both versions
        "(Living with them will be much cheaper than renting a student residence, and it’ll surely be nice to see Nancy and Dalia again.)":
            "Living with them will be much cheaper than renting a student residence, and it'll surely be nice to see my mom, Dalia, and Penelope again.",

        # BM 964
        "(Living with them will be much cheaper than renting a student residence, and it’ll surely be nice to see Mom and Dalia again.)":
            "Living with them will be much cheaper than renting a student residence, and it'll surely be nice to see my mom, Dalia, and Penelope again.",

        # BM 1230
        "Anyway, do you know where Nancy is?":
            "Anyway, do you know where your mom is?",

        # BM 1587
        "How could I forget you?":
            "How could I forget my own mom?",

        # BM 1643 mildly pointless change? ~BA
        "It’s me, Nancy! Even though we’ve only been speaking on the phone for the past few days, I feel like we’ve been becoming good friends already! Isn't that right, Annie?":
            "It's me, Nancy! Even though we've only been speaking on the phone for the past few days, I feel like we're becoming good friends already! Isn't that right, Annie?",

        # BM 1655 lines are identical? ~BA
        "I hope so! And please, just call me Nancy!":
            "I hope so! And please, just call me Nancy!",

        # BM 1657 lines are identical? ~BA
        "Okay! Thank you, Nancy!":
            "Okay! Thank you, Nancy!",

        # BM 1662
        "And of his babysitter!":
            "And of his mother!",

        # BM 1666
        "Yeah, since my Dad was constantly working, I've always said you were like a parent to me.":
            "Yeah!",

        # BM 1669
        "Now I work in a laboratory, but back then I was still finishing my thesis. Thankfully [mc]'s father came along and offered me the babysitting gig.":
            "Now I work in a laboratory, but back then I was still finishing my thesis. Luckily, [mc]'s father made enough money.",

        # BM 1670
        "It was not only well-paid, but also allowed me the flexibility to take care of my daughters at the same time. And for me, being a single mother, that was essential.":
            "I was able to focus on my thesis and take care of our three children.",

        # BM 1674
        "Yes, Dalia and Penelope. Penny was a little older when I was [mc]'s nanny, so she used to play on her own, but Dalia got very close to him!":
            "Yes, Dalia and Penelope. Penny is a little older than [mc], so she used to play on her own, but Dalia was always very close to him!",

        # BM 1687
        "(I guess you don't notice that stuff when you're 8 years old...)":
            "(I guess you don't notice that stuff when you're a kid...)",

        # BM 1689
        "(Okay, now I sound like some old perv.)":
            "(Okay, now I sound like an old pervert. Especially since she's my mother.)",

        # BM 1719
        "(Each day I would spend the afternoon playing with her and Dalia. We had dinner every night at eight, and then Nancy drove me home once it got late.)":
            "(Each day I would spend the afternoon playing with her and Dalia. We had dinner every night at eight, and then went to bed.)",

        # BM 1740
        "Although he left before she was born, so I was left paying the mortgage all by myself...":
            "Although when he left, I had to pay the rest of the mortgage all by myself.",

        # BM 1792
        "I wasn't expecting you to be so excited to meet [mc] again!":
            "I wasn't expecting you to be so excited to meet your brother again!",

        # BM 1808
        "Oh, y-yeah, so excited! Hi [mc]!":
            "Oh, y-yeah, so excited! Hi bro!",

        # BM 1838
        "Both of those things can wait! You didn't even welcome [mc] and Annie properly!":
            "Both of those things can wait! You didn't even welcome your brother and Annie properly!",

        # BM 1843
        "[mc]! I can't wait to properly meet you!":
            "Hey, bro, I can't wait to hear all about what happened to you!",

        # BM 1852
        "Damn [mc], you look... tall!":
            "Damn, bro, you look... tall!",

        # BM 1853
        "Thanks, Dalia. You look... tall too.":
            "Thanks, sis. You look... tall too.",

        # BM 1991
        "Your room will be on the second floor—the last one on the right.":
            "I cleaned up your old room. I hope you still remember it?",

        # BM 2015 FIXED: Handle both "Nancy" and "Mom" versions
        "(There wasn't a bed here before. I guess Nancy fitted it out to serve as a bedroom.)":
            "(My bed is bigger than before. I guess Mom replaced my old furniture.)",

        # BM 2015
        "(There wasn't a bed here before. I guess Mom fitted it out to serve as a bedroom.)":
            "(My bed is bigger than before. I guess Mom replaced my old furniture.)",

        # BM 2081
        "N-Nancy?":
            "M-Mom?",

        # BM 2087
        "N-Nancy? W-Who is this kid?":
            "M-Mom? W-Who is this kid?",

        # BM 2241
        "N-Nancy! You almost gave me a heart attack!":
            "M-Mom! You almost gave me a heart attack!",

        # BM 2252
        "I'm used to only living with my daughters, and...":
            "I'm used to only living with your sisters, and...",

        # BM 2271
        "It's like we're family now. I'm not bothered by you at all!":
            "It's alright, we're family after all. I'm not bothered by you at all!",

        # BM 2306
        "(Jesus, look at me. Fantasizing about the dick of the kid I used to care for.)":
            "(Jesus, look at me. Fantasizing about the dick of my own son.)",

        # BM 2307 lines are identical? ~BA
        "(You're 20 years older than he is, Nancy, for fuck's sake.)":
            "(You're 20 years older than he is, Nancy, for fuck's sake.)",

        # BM 2327
        "Hey Dalia! Good morning!":
            "Hey sis! Good morning!",

        # BM 2328, may also affect 66534, 83881 (not really a problem tho)
        "Hey [mc]!":
            "Hey bro!",

        # BM 2371
        "No problem Dalia. I don’t like being the center of attention anyway.":
            "No problem, sis. I don't like being the center of attention anyway.",

        # BM 2449
        "Good morning...":
            "Good morning, sis...",

        # BM 2461
        "(I mean, I know they’re pretty much like family, so I don't mean it that way, but...)":
            "(I mean, I know they’re family, so I don't mean it that way, but...)",

        # BM 2519
        "W-What the fuck, [mc]?!":
            "W-What the fuck, bro?!",

        # BM 3076
        "*Turning around* Dalia!":
            "*Turning around* Sis!",

        # BM 3301
        "(It's just Dalia. You two grew up together! She's practically your sister...)":
            "(It's just Dalia. You two grew up together! She's your sister...)",

        # BM 3318
        "Dalia, the girl you live with?":
            "Dalia, your sister?",

        # BM 3680
        "(Oh shit, full-on chub incoming...)":
            "(Oh shit, full-on chub incoming... Oh god, snap out of it, [mc]. This is your sister.)",

        # BM 3704
        "(And that's... wrong! Bad [mc]! Get a hold of yourself.)":
            "(And that's... wrong! Bad [mc]! This is your sister! Get a hold of yourself.)",

        # BM 3773
        "You're a fucking rapist!":
            "You're a fucking pervert!",

        # BM 3775
        "You were hiding in the bathtub so you could attack me from behind and then rape me!":
            "You were hiding in the bathtub so you could see me naked! I'm your sister, you pig!",
        
        # BM 3777
        "So what then? You're just a perverted creep?!":
            "So what then? You're just \"{i}curious{/i}\"?!",

        # BM 3825
        "Hi Penelope.":
            "Hi, sis.",

        # BM 3888
        "I can't be seen there... I have a reputation to uphold, [mc].":
            "I can't be seen there... I have a reputation to uphold, bro.",

        # BM 3903
        "She was going with my mom to do some shopping, or at least that’s what I was told. They should be back in time for supper.":
            "She was going with Mom to do some shopping, or at least that's what I was told. They should be back in time for supper.",

        # BM 3917
        "Alright [mc], you convinced me!":
            "Alright bro, you convinced me!",

        # BM 3931
        "Thanks, Penelope!":
            "Thanks, sis!",

        # BM 4076
        "*Laughs* Yeah, if you say so... Thanks, [mc].":
            "*Laughs* Yeah, if you say so... Thanks, bro.",

        # BM 4107
        "(Wow, he's treating Penelope like a celebrity. Is she really that popular?)":
            "(Wow, he's treating sis like a celebrity. Is she really that popular?)",

        # BM 4720
        "Well, I definitely do not share that opinion at all.":
            "Well, I definitely do not share that opinion at all. You are my sister after all.",

        # BM 4722
        "Thanks for trusting me, [mc]. It means a lot.":
            "Thanks for trusting me, bro. It means a lot.",

        # BM 5016
        "Alright, let's go home, [mc]!":
            "Alright, let's go home, bro!",

        # BM 5054
        "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal when I was living with my dad.":
            "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal when I was living with Dad.",

        # BM 5083 lines are identical? ~BA
        "We're only missing Nancy and Penelope, then our group would be complete!":
            "We're only missing Nancy and Penelope, then our group would be complete!",

        # BM 5094
        "It was a nice breath of fresh air. Thank you for pushing me out of my comfort zone, [mc].":
            "It was a nice breath of fresh air. Thank you for pushing me out of my comfort zone, bro.",

        # BM 5096
        "No problem, Penelope.":
            "No problem, sis.",

        # BM 5213
        "(But I'm not gonna find one in this house! I need to start thinking with the head above my shoulders and not the one between my legs.)":
            "(I need to start thinking with the head above my shoulders and not the one between my legs.)",

        # BM 5246
        "I put a little extra elbow grease into it. After all, you're graciously letting me and Annie stay here and you’re sharing your food with us too!":
            "I put a little extra elbow grease into it. After all, I wanted to make you happy, Mom!",

        # BM 5247
        "I know it doesn't come close to making up for it, but I'll try to help you out as much as I can.":
            "It's been way too long since we've seen each other.",

        # BM 5290
        "First, neither of my daughters gets kissed by fire and inherits my lovely red hair, and now they can’t seem to keep tabs on any of their belongings!":
            "First, none of my kids get kissed by fire and inherit my lovely red hair, and now they can't seem to keep tabs on any of their belongings!",

        # BM 5417
        "(Who would’ve known he was hiding such a monster...)":
            "(Who would've known he was hiding such a monster... and where did he get it from? I know his father didn't have one this size...)",

        # BM 5435
        "(Oh Jesus, one man comes into my house and suddenly I turn into a nymphomaniac. What the hell is wrong with me?)":
            "(Oh Jesus, one man comes into my house and suddenly I turn into a nymphomaniac. What the hell is wrong with me? He is my son!)",

        # BM 5459
        "(I mean... If Dalia and Penelope never found out, then would it really be so bad? It’d be our little secret...)":
            "(I mean... If Dalia and Penelope never found out, then would it really be so bad...? {w} Of course it would be! He's my son...)",

        # BM 5478 lines are identical? ~BA
        "(Come on, Nancy... get a hold of yourself. You should be leaving for work already...)":
            "(Come on, Nancy... get a hold of yourself. You should be leaving for work already...)",

        # BM 5523
        "Hey Dalia!":
            "Hey sis!",

        # BM 5545
        "I'm sorry about that, Dalia.":
            "I'm sorry about that, sis.",

        # BM 5921
        "You said you were Dalia's friend?":
            "You said you were Dalia's brother?",

        # BM 5923
        "Yeah, we've known each other since we were little.":
            "Yeah, we were separated as kids when our parents divorced.",

        # BM 8339
        "I heard that promise, Penny! Too late to back out now!":
            "I heard that promise, sis! Too late to back out now!",

        # BM 8413
        "Anyway, I'll go to bed too. Goodnight, [mc].":
            "Anyway, I'll go to bed too. Goodnight, bro.",

        # BM 8428
        "(You're not a horny teenager. Show her you're a man now.)":
            "(You're not a horny teenager. Show her you're a man now. And remember, she is your mother.)",

        # BM 8522
        "What?! Come on, Dalia!":
            "What?! Come on, sis!",

        # BM 8536
        "Please, Dalia! Please!":
            "Please, sis! Please!",

        # BM 9493
        "Thanks Dalia, it means a lot coming from you.":
            "Thanks sis, it means a lot coming from you.",


    # -----------------------------------------
    # v0.2 script2.rpy Lines 9770-19471

        # BM 13783
        "*Knocks* [mc]? Are you up?":
            "*Knocks* Honey? Are you up?",

        # BM 14051
        "Dalia? Are you up?":
            "Sis? Are you up?",

        # BM 14084
        "I gotta say, those were some damn good pancakes. Thank you, [mc].":
            "I gotta say, those were some damn good pancakes. Thank you, bro.",

        # BM 14108
        "Hmmm... I'm not so sure about that, Dalia. I've seen broom sticks thicker than your biceps.":
            "Hmmm... I'm not so sure about that, sis. I've seen broom sticks thicker than your biceps.",

        # BM 14144
        "A-Are you okay, Dalia?":
            "A-Are you okay, sis?",

        # BM 14344
        "*Laughs* It's not that. [mc] is staying with us for a year until he finishes school. He’s part of the student exchange program.":
            "*Laughs* It's not that. He's my son I told you about. [mc] is staying with us for a year until he finishes school. He’s part of the student exchange program.",

        # BM 14350
        "Well, well, well, [mc]!":
            "Well, well, well, the fabled lost son is here!",

        # BM 14610
        "What? I'm not Dalia. My name is [mc].":
            "What? I'm not Dalia. My name is [mc]. Dalia is my sister.",

        # BM 14627 lines are identical? ~BA
        "You know, maybe Nancy would also hear more compliments if she ever left her lab!":
            "You know, maybe Nancy would also hear more compliments if she ever left her lab!",

        # BM 14659 lines are identical? ~BA
        "And of course... my beautiful little dove, Nancy.":
            "And of course... my beautiful little dove, Nancy.",

        # BM 14661 lines are identical? ~BA
        "Flattery...? No, my Nancy. I am only speaking my truth. And truth should never be told to someone who is not worthy of it.":
            "Flattery...? No, my Nancy. I am only speaking my truth. And truth should never be told to someone who is not worthy of it.",

        # BM 14680 Handle both versions
        "No, I came with Nancy.":
            "No, I came with Nancy, my mother.",

        # BM 14680
        "No, I came with Mom.":
            "No, I came with Nancy, my mother.",

        # BM 14682
        "Oh, really? You two know each other? Well I'm glad to meet you, because I'm positive you're going to be seeing a lot more of me soon...":
            "Oh, really? You are her son? Well I'm glad to meet you, because I'm positive you're going to be seeing a lot more of me soon...",

        # BM 14864
        "Look at that perfectly toned stomach... And to think she's had 2 daughters! Unbelievable.":
            "Look at that perfectly toned stomach... And to think she's had 3 children! Unbelievable.",

        # BM 14969
        "*Giggles* Just like when I was your babysitter.":
            "*Giggles* Just like when you were still living with us.",

        # BM 14704 lines are identical? ~BA
        "Perfect, Nancy... your graceful movements are simply unmatched...":
            "Perfect, Nancy... your graceful movements are simply unmatched...",

        # BM 14723 lines are identical? ~BA
        "Our last movement will be an Acro pose and must be done in pairs. So... Raul should go with Noah, [mc] with Gertrude, and... oh! I guess that leaves me with you, Nancy.":
            "Our last movement will be an Acro pose and must be done in pairs. So... Raul should go with Noah, [mc] with Gertrude, and... oh! I guess that leaves me with you, Nancy.",

        # BM 14733
        "I mean, obviously Kai would've asked me out if I wasn't already married, but since I'm happily taken... Nancy will be a very good fit for him.":
            "I mean, obviously Kai would've asked me out if I wasn't already married, but since I'm happily taken... your mom will be a very good fit for him.",

        # BM 15027 lines are identical? ~BA
        "*Breathing heavily* I'm... so relieved... you didn't leave yet, Nancy.":
            "*Breathing heavily* I'm... so relieved... you didn't leave yet, Nancy.",

        # BM 15067 lines are identical? ~BA
        "What? That's absurd! You're a goddess, Nancy! You're a modern day Aphrodite!":
            "What? That's absurd! You're a goddess, Nancy! You're a modern day Aphrodite!",

        # BM 15098 lines are identical? ~BA
        "Nancy, sex is a beautiful part of life. If you have needs, you need to be taken care of. You deserve to be pampered... desired... lusted after. Even more so with you being such a beautiful woman.":
            "Nancy, sex is a beautiful part of life. If you have needs, you need to be taken care of. You deserve to be pampered... desired... lusted after. Even more so with you being such a beautiful woman.",

        # BM 15133, better match
        "(I can't just barge in and be like, \"Hi [mc], did you know you make me feel so horny all the time? Do you wanna fuck your old babysitter?\")":
            "(I can't just barge in and be like, \"Hi [mc], did you know you make me feel so horny all the time? Do you wanna fuck your mother?\")",

        # BM 15134
        "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out.)":
            "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out. And fucking my son, is that even legal?)",

        # BM 15873
        "I never met my mother and my father was always absent in my life. He was constantly too occupied with his work.":
            "I was separated from my mother at a young age and my father was always absent in my life. He was always too occupied with his work.",

        # BM 16858
        "Is that a hint of jealousy, I'm sensing?":
            "Is that a hint of overprotectiveness I'm sensing?",

        # BM 16898
        "(It's not like I was expecting her to wait for me like a nun, but... just imagining some guy banging her... ugh.)":
            "(It's not like I was expecting her to wait for marriage like a nun, but... just imagining some guy banging her... ugh.)",

        # BM 16904
        "(Way out of your league.)":
            "(I am her brother.)",

        # BM 16922
        "[mc] here is gonna be my photographer this time.":
            "My brother here is gonna be my photographer this time.",

        # BM 16926
        "Ahhh... yeah, that's right. [mc]...":
            "Ahhh... yeah, that's right. Your brother, [mc]...",

        # BM 17104
        "(Wake up [mc], we're talking about Penelope here. Still not gonna happen.)":
            "(Wake up [mc], we're talking about your sister here. Still not gonna happen.)",

        # BM 17174
        "But that's why I'm glad to have you here, [mc].":
            "But that's why I'm glad to have you here, bro.",

        # BM 17475
        "I don't mind you seeing me like this, because... I don't know, I just feel comfortable around you.":
            "I don't mind you seeing me like this, because you're my little brother.",

        # BM 17478
        "And besides, what would my mom say if she saw me posting those pictures? She'd probably think it was an introductory photoshoot to a porno or something...":
            "And besides, what would Mom say if she saw me posting those pictures? She'd probably think it was an introductory photoshoot to a porno or something...",

        # BM 17743
        "That Valentino guy made me realize that I'll never feel comfortable doing something like this with a stranger. But you're no stranger, [mc], and since I have you here...":
            "That Valentino guy made me realize that I'll never feel comfortable doing something like this with a stranger. But you're no stranger, you're my brother, [mc], and since I have you here...",

        # BM 17762
        "(Oh my god, am I about to see Penelope naked?)":
            "(Oh my god, am I about to see my older sister naked?)",

        # BM 17877
        "(Or how her breasts are slightly paler than the rest of her body... because she probably never sunbathes topless... meaning you're likely the first man who's gotten to see her breasts in who knows how long... and...)":
            "(Or how her breasts are slightly paler than the rest of her body... because she probably never sunbathes topless... meaning you're likely the first man who's gotten to see your sister's breasts in who knows how long...{p} Shit... Why does it feel so good knowing this?)",

        # BM 17885
        "Oh, come on, [mc]!":
            "Oh, come on, bro!",

        # BM 17910
        "(Is this huge thing I'm feeling... his...)":
            "(Is this huge thing I'm feeling... my brother's...)",

        # BM 17950
        "Um... Hey Penny, do you have all of your belongings?":
            "Um... Hey sis, do you have all of your belongings?",

        # BM 17970
        "Me too, Penelope.":
            "Me too, sis.",

        # BM 18085
        "I was wondering why Nancy and her shared the same last name on your followers list. Nancy is her mom!":
            "I was wondering why Nancy, you, and her shared the same last name on your followers list. Nancy is your mom!",

        # BM 18180, swiped from half-sis map lol ~BA
        "(Nah, I'm probably imagining things... just like Chang does all the time.)":
            "(Nah, I'm probably imagining things... after all, she's my sister. There's no way she's actually flirting with me... right?)",

        # BM 18190
        "And now I’ve come to learn that you’re friends with Penelope too?!":
            "And now I’ve come to learn that you’re Penelope’s brother too?!",


    # -----------------------------------------
    # v0.3 script3.rpy Lines 19472-30120

        # BM 22280
        "Especially the youngest daughter. She's extremely naive and easily manipulated.":
            "Especially the middle daughter. She's extremely naive and easily manipulated.",

        # BM 22368
        "H-Holy shit, [mc]!":
            "H-Holy shit, bro!",

        # BM 22382
        "Take that back, moron. Your problem is with me, not her.":
            "Take that back, moron. Your problem is with me, not my sister.",

        # BM 22384
        "Don't worry, I'm not going to waste time on your whore anymore.":
            "Don't worry, I'm not going to waste time on your whore of a sister anymore.",

        # BM 22516
        "Yeah, Roman style. We're playing with my mom. It's gonna be her first time.":
            "Yeah, Roman style. We're playing with our mom. It's gonna be her first time.",

        # BM 23386
        "Alright, so... we need Penelope and Nancy, right?":
            "Alright, so... we need Penelope and your mom, right?",

        # BM 23408
        "I thought [mc] called me.":
            "I thought my brother called me.",

        # BM 23768
        "Don’t worry Penny, you'll feel better soon. It only gets better from here on out! Come on, let me give you a hand before you get soaked!":
            "Don’t worry sis, you'll feel better soon. It only gets better from here on out! Come on, let me give you a hand before you get soaked!",

        # BM 24318
        "Oh yeah! Thank you [mc]!":
            "Oh yeah! Thank you bro!",

        # BM 24386 lines are identical? ~BA
        "(This is the opportunity you've been waiting for, Nancy. All you gotta do is nail this job interview.)":
            "(This is the opportunity you've been waiting for, Nancy. All you gotta do is nail this job interview.)",

        # BM 24388
        "(This nanny gig just isn't enough to pay the bills, and between paying the girls' tuition and the mortgage...)":
            "(We have enough money at the moment but between paying the kids' tuition and the mortgage, it's only going to increase...)",

        # BM 24390
        "(I'm not gonna be able to hold out much longer. They'll take the house from me if I don't get some sort of extra income this month. I can only fend off the bank for so long...)":
            "*sigh*",

        # BM 24391
        "([mc]'s father is already generously paying me more than he should for taking care of his son. But even with that extra money, it's only delaying the inevitable.)":
            "Also, things with my husband aren't going well... the divorce was costly too.",

        # BM 24396
        "(What if I don't get this job either? What if I have to take the girls out of school and transfer them? What if we don't have enough money to...)":
            "(What if I don't get this job either? What if I have to take the kids out of school and transfer them? What if we don't have enough money to...)",

        # BM 24438
        "I need you to stay and take care of Dalia and [mc].":
            "I need you to stay and take care of your siblings.",

        # BM 24479
        "Do you have any idea how much I've sacrificed so that you and Dalia would never be left wanting?!":
            "Do you have any idea how much I've sacrificed so that you three would never be left wanting?!",

        # BM 24552
        "*Clears throat* Hello, this is Nancy Carter.":
            "*Clears throat* Hello, this is Nancy [lastname].",

        # BM 24559
        "Um... I'm afraid I must cancel the interview. I couldn't find anyone to watch my daughter tonight, so...":
            "Um... I'm afraid I must cancel the interview. I couldn't find anyone to watch my kids tonight, so...",

        # BM 24577
        "Nothing... I’m just sad because in a couple of weeks, my dad will be bringing me with him to Europe.":
            "Nothing... I'm just sad because in a couple of weeks, Dad will be bringing me with him to Europe.",

        # BM 24643
        "Absolutely! Don't worry sis, I'll protect you, [mc], and Mom!":
            "Absolutely! Don't worry, sis, I'll protect you, bro, and Mom!",

        # BM 24682
        "[mc] ate it all in one sitting!":
            "Bro ate it all in one sitting!",

        # BM 24691
        "Quickly, quickly! Pick up everything, [mc]!":
            "Quickly, quickly! Pick up everything, bro!",

        # BM 25442
        "We're just friends. I've only seen her half-naked once... during a photoshoot.":
            "She is my sister. I've only seen her half-naked once... during a photoshoot.",

        # BM 25463
        "So tell me... don't you wanna see a bit more? If I had a \"friend\" who looked like this, I’d be dying to find out what’s underneath all those clothes...":
            "So tell me... don't you wanna see a bit more? If I had a \"sister\" who looked like this, I’d be dying to find out what’s underneath all those clothes...",

        # BM 25954
        "This morning, in the bathroom. Right after [mc] used the shower.":
            "This morning, in the bathroom. Right after my brother, [mc], used the shower.",

        # BM 26036
        "A friend!":
            "Someone I like!",

        # BM 26047
        "Was he [mc]?":
            "Could it be... your brother?",

        # BM 26118
        "Your BDSM-lover friend said you've all been to the Emporium already, right?":
            "Your BDSM-lover sister said you've all been to the Emporium already, right?",

        # BM 27379
        "Don't worry [mc], I'm in good hands!":
            "Don't worry bro, I'm in good hands!",

        # BM 28264
        "O-Of course not! I'd only agree to that in the first place because you'll never beat me in a fight! Like, ever!":
            "O-Of course not! You're my brother! I'd only agree to that in the first place because you'll never beat me in a fight! Like, ever!",

        # BM 28266
        "Well if that’s the case, then why does it matter what I want? Getting naked, testing out your... “skills”, or any other thing. You’re so positive you’re gonna win anyways!":
            "Well if that's the case, then why does it matter what I want? Getting naked, testing out your... “skills”, or any other thing. If you're so positive you're gonna win anyways, it shouldn't even matter that I'm your brother!",

        # BM 29082
        "N-Nancy...":
            "M-Mom...",

        # BM 29096
        "We bathed together countless times when you were younger, remember? Your father left for business trips frequently so you stayed over all the time.":
            "We bathed together countless times when you were younger, remember? Your father left for business trips frequently so I took care of you three on my own.",

        # BM 29135
        "(Keep it together! She’s been like a mother to you. Focus, [mc]! This is strictly a bath!)":
            "(Keep it together! She's your mother. Focus, [mc]! This is strictly a bath!)",

        # BM 29166 should rewrite
        "And I saw you! Back when you were my babysitter. I was too young to remember most of that time, but you looked exactly like you did in our old pictures!":
            "And I saw you! I was too young to remember most of that time, but you looked exactly like you did in our old pictures!",

        # BM 29178
        "I owe it to my mother. It seems like once she reached 25, she stopped aging. She died shortly after Dalia was born, but she was always so full of life.":
            "I owe it to your grandma. It seems like once she reached 25, she stopped aging. She died shortly after Dalia was born. It's a shame she never met you, she was always so full of life.",

        # BM 29186
        "Girlfriend. No doubt about it at all.":
            "Girlfriend. No doubt about it at all. No one would believe me if I said you're my mother.",

        # BM 29201
        "Not at all. Fire away, my Empress.":
            "Not at all. Fire away, Mom.",

        # BM 29208
        "I see... my young [mc] has a little experience under his belt. Very interesting...":
            "I see... my son has a little experience under his belt. Very interesting...",

        # BM 29239
        "Um... I... I'm not...":
            "W-What? T-They're my sisters!",

        # BM 29242
        "Why not? I wouldn’t mind having you as my son-in-law...":
            "Why not? I wouldn't mind.",

        # BM 29246
        "Let’s say one of my daughters came in here right now and asked you to have sex with them. No tricks or schemes... they just desired you. Would you say yes?":
            "Let's say one of your sisters came in here right now and asked you to have sex with them. No tricks or schemes... they just desired you. Would you say yes?",

        # BM 29274
        "I couldn't. I don't know... I just see them as family.":
            "I couldn't! They're my family...",

        # BM 29268 might want to rewrite lines around this one ~BA
        "All areas, huh? How will you determine that?":
            "All areas, huh? How will you determine that? Besides, you're my mother, so shouldn't you know?",

        # BM 29314
        "Hmph. I invite a commoner to my private baths and he can’t even contain himself. What a shame.":
            "Hmph. I invite someone to my private baths and he can’t even contain himself. What a shame.",

        # BM 29337
        "(I’d hate myself if I didn’t at least try...)":
            "(I'd hate myself if I didn't at least try... I guess there's no more denying it; I like my mom.)",

        # BM 29338
        "I think this goes without saying, but let’s not mention this to anyone. My daughters especially... heaven knows what they’d think if they learned we bathed together.":
            "I think this goes without saying, but let's not mention this to anyone. Your sisters especially... heaven knows what they'd think if they learned we bathed together.",

        # BM 29372
        "(I can tell she was looking forward to this.)":
            "(I can tell she was looking forward to this... And you know what? Fuck the taboo! If I want to fuck my mom, I'm gonna do it.)",

        # BM 29382
        "I guess I never paid attention back then, since I was only five and had no interest in them...":
            "I guess I never paid attention back then, since I was just a kid and had no interest in them...",

        # BM 29386 might need tweaking ~BA
        "After having taken care of you for so long back then... I never thought we’d be in this position now...":
            "As your mother who gave birth to you, and having raised you so long ago... I never would've thought we'd be in this position now...",

        # BM 29419
        "But I think we’ve broken enough rules today...":
            "But I think that is a rule we can ignore since you are my son and thus, royalty... but other rules have been broken no doubt.",

        # BM 29572
        "I'll fulfill them all...":
            "Like having sex with your son?",

        # BM 29575
        "And now...":
            "Yes, and now...",

        # BM 29578
        "This time though... I want you to lie back and let your babysitter do all the work...":
            "This time though... I want you to lie back and let your mother do all the work...",

        # BM 29605
        "*Whispering* What for? It's only a guard!":
            "*Whispering* What for? It's only a guard! He doesn't know I'm your son.",

        # BM 29649
        "(Why does God hate me?)":
            "(Why does God hate me? Is this karma?)",

        # BM 29717
        "*From downstairs* [mc]? Is that you? Finally!":
            "*From downstairs* Bro? Is that you? Finally!",

        # BM 29854
        "Yeah, I took [mc] on a tour of the palace afterward. We visited the atrium for awhile and he showed me a few of the skills he’s learned.":
            "Yeah, I took your brother on a tour of the palace afterward. We visited the atrium for awhile and he showed me a few of the skills he’s learned.",

        # BM 29914
        "Hah! I don't think you know us as well as you believe. After all, you've only been living with us for a short while. And the others, you only met them a few weeks ago!":
            "Hah! I don't think you know us as well as you believe. After all, you've only been living with us again for a short while. We've changed in the years you were gone. And the others, you only met them a few weeks ago!",


    # -----------------------------------------
    # v0.4 script4.rpy Lines 30121-39683

        # BM 32396
        "I'm not Nancy's daughter. I mean, I'm not even a girl! Do I have to spell it out or what?":
            "I'm her son! I mean, I'm not even a girl! Do I have to spell it out or what?",

        # BM 32485
        "What the hell, Dalia?!":
            "What the hell, sis?!",

        # BM 32634
        "I'll go as fast as I can. Thank you, [mc].":
            "I'll go as fast as I can. Thank you, bro.",

        # BM 32779
        "Show them what you got, Dalia!":
            "Show them what you got, sis!",

        # BM 33051
        "And on my right, weighing in at 125 lbs... Dalia Carter!":
            "And on my right, weighing in at 125 lbs... Dalia [lastname]!",

        # BM 33109
        "[mc]! I won!":
            "Bro! I won!",

        # BM 33123
        "Congrats, Dalia.":
            "Congrats, sis.",

        # BM 33152 tbh a few more lines here could use work ~BA
        "I didn't know you were dating!":
            "I didn't know you were dating! Aren't you his sister?",

        # BM 33171
        "We're just old friends!":
            "We're just siblings!",

        # BM 33172
        "And d-don't tell my mom":
            "And d-don't tell Mom.",

        # BM 33177
        "It doesn't mean anything!":
            "It doesn't mean anything! A-And I heard in Europe, siblings do this all the time!!",

        # BM 33233
        "*Imitating Dalia* [mc]! I won! I won! Did you see it!? Muah Muah *imitates kissing noises*":
            "*Imitating Dalia* Bro! I won! I won! Did you see it!? Muah Muah *imitates kissing noises*",

        # BM 33647
        "Thank you [mc].":
            "Thank you bro.",

        # BM 33704
        "What are you concocting in that pervy little brain of yours?":
            "What are you concocting in that pervy little brain of yours, brother?",

        # BM 33716
        "This bikini looks good on you, Dalia.":
            "This bikini looks good on you, sis.",

        # BM 33769
        "I loved spending some time with you in your server, Dalia. Thanks for letting me visit.":
            "I loved spending some time with you in your server, sis. Thanks for letting me visit.",

        # BM 33837
        "You made me so fucking horny, Dalia. Do you see how hard you made me?":
            "You made me so fucking horny, sis. Do you see how hard you made me?",

        # BM 33868
        "You're in denial today, Dalia...":
            "You're in denial today, sis...",

        # BM 33881
        "You're driving me insane, Dalia...":
            "You're driving me insane, sis...",

        # BM 33896
        "(Oh my god, Dalia's sucking my cock...)":
            "(Oh my god, my sister is sucking my cock...)",

        # BM 37436
        "Good luck, [mc]!":
            "Good luck, bro!",

        # BM 37438
        "Hey! Thanks, Penny!":
            "Hey! Thanks, sis!",

        # BM 37479
        "Heeeey! Good luck with the fat cats, [mc]!":
            "Heeeey! Good luck with the fat cats, bro!",

        # BM 37480
        "Thanks Dalia!":
            "Thanks sis!",

        # BM 37504, bro kinda weird here ~BA
        "“We” have a party? Who’s “we”? You and [mc]?":
            "“We” have a party? Who’s “we”? You and bro?",

        # BM 37507, bro kinda weird here ~BA
        "Yeah, Nova, [mc], and I are going to a party on campus. I could have sworn I told you about it...":
            "Yeah, Nova, bro, and I are going to a party on campus. I could have sworn I told you about it...",

        # BM 37522
        "What other people? You? Mom? Annie? I'm sure [mc] doesn't mind either. He's like... family. Like a little brother, almost.":
            "What other people? You? Mom? Annie? I'm sure [mc] doesn't mind either. He's... family. Our little brother...",

        # BM 37525
        "Yeah... like a little brother...":
            "Yeah... our little brother...",

        # BM 37528 rewrite ~BA
        "With [mc]? Pffft, please, my bar is WAY higher. You've seen my Instagram DMs: models, actors, influencers... did you know that that Gigachad meme guy from a few years ago tried sliding into my DMs?":
            "With our brother? Pffft, please, my bar is WAY higher. You've seen my Instagram DMs: models, actors, influencers... did you know that that Gigachad meme guy from a few years ago tried sliding into my DMs? Also, that would be incest...",


    # -----------------------------------------
    # v0.5 script5.rpy Lines 39684-55297

        # BM 40313
        "Oh, that is very likely, actually, Ms. Carter. It would be poetic and, at the same time, easy to make it look like an accident.":
            "Oh, that is very likely, actually, Ms. [lastname]. It would be poetic and, at the same time, easy to make it look like an accident.",

        # BM 40711
        "Could you help me with it, [mc]? I've gotta go before leaving.":
            "Could you help me with it, honey? I've gotta go before leaving.",

        # BM 40733
        "It's been quite a challenge trying to find you alone this past week, [mc]...":
            "It's been quite a challenge trying to find you alone this past week, son...",

        # BM 40751
        "I want you to fuck me, [mc]. Hard. And filthy.":
            "I want you to fuck me, my son. Hard. And filthy.",

        # BM 44122 phone chat (nova_chat3)
        "You don't live with the Carters anymore?":
            "You don't live with your family anymore?",

        # BM 44476
        "*Knocks on the door* [mc]? Is that you?":
            "*Knocks on the door* Bro? Is that you?",

        # BM 44549
        "Anyway, now that we’ve both seen each other naked, there's really no reason to make a big deal about this in the future.":
            "Anyway, now that we’ve both seen each other naked again, there's really no reason to make a big deal about this in the future.",

        # BM 44586
        "Penelope Carter... you’re gonna drive me mad.":
            "Penelope [lastname]... you’re gonna drive me mad.",

        # BM 44645
        "Penny? I'm ready!":
            "Sis? I'm ready!",

        # BM 44670
        "You look spectacular, Penny. Really hit it out of the park!":
            "You look spectacular, sis. Really hit it out of the park!",

        # BM 44763
        "*Chuckles* Don’t be silly! You're staying with us until we say so. No escaping the Carters!":
            "*Chuckles* Don’t be silly! You're staying with us until we say so. No escaping the [lastname]s!",

        # BM 44869
        "Can you take a pic of us before going in, [mc]?":
            "Can you take a pic of us before going in, bro?",

        # BM 44894
        "*Chuckles* You're too excited, [mc].":
            "*Chuckles* You're too excited, bro.",

        # BM 44968
        "U-Uh... a-are you sure?":
            "U-Uh... a-are you sure? I-Isn't he your brother?",

        # BM 44999
        "(But holy shit, did she say she has a crush on [mc] too?!)":
            "(But holy shit, did she say she has a crush on her brother too?!)",

        # BM 45892
        "Penelope? Penelope Carter? That IG model in the journalism program?":
            "Penelope? Penelope [lastname]? That IG model in the journalism program?",

        # BM 47667
        "And you thought of asking your big titty blonde bimbo friend to lend you hers, right?":
            "And you thought of asking your big titty blonde bimbo sister to lend you hers, right?",

        # BM 47818
        "No, not really. We're just friends. I've been in Kredon just for a couple of months, actually.":
            "No, not really. I'm her brother. I moved back to Kredon just few months ago, actually.",

        # BM 47861
        "Actually, yeah! I'm looking for Penelope. Penelope Carter. Do you know her?":
            "Actually, yeah! I'm looking for Penelope. Penelope [lastname]. Do you know her?",

        # BM 47881
        "Um... no, not really. We're just friends. I've been in Kredon just for a couple of months.":
            "Um... no, not really. I'm her brother. I moved back to Kredon just few months ago.",

        # BM 47952
        "Hi, [mc]! Sorry for the wait.":
            "Hi, bro! Sorry for the wait.",

        # BM 47958
        "Goddamn, this dress looks GREAT on you, Penny.":
            "Goddamn, this dress looks GREAT on you, sis.",

        # BM 47994
        "I came with Penelope. I live with her, as part of the Student Exchange Program.":
            "I came with Penelope. She's my sister, I live with her as part of the Student Exchange Program.",

        # BM 48022
        "*Chuckles* I'd say the Carters played a big role in that, yeah...":
            "*Chuckles* I'd say my family played a big role in that, yeah...",

        # BM 48138
        "Uhh... I-I mean...":
            "Uhh... I-I meant ever! 'Cus he's my brother...",

        # BM 48149
        "Ohh... this is the kind of dare I like.":
            "You want me to kiss my sister?",

        # BM 48151
        "*Giggles* I bet you do.":
            "*Giggles* Is [mc] scared of a little dare?",

        # BM 48153
        "It's my time to shine.":
            "Not at all! It's my time to shine.",

        # BM 48156
        "*Grabbing her by the waist* I love this dress, Penny.":
            "*Grabbing her by the waist* I love this dress, sis.",

        # Entire truth and dare needs more work imo but I dont have any good ideas ~BA

        # BM 48273
        "*Chuckles* I swear if you don't say my name, I'm gonna grab my things and go home.":
            "*Chuckles* Are you about say what I think you're about to say?",

        # BM 48275
        "*Snorts* Okay, okay, I'm gonna say [mc].":
            "*Snorts* Yeah, okay, I'm gonna say [mc].",

        # BM 48278
        "Penelope Carter just said that she'd like to have a threesome with me. It's difficult not to be enthusiastic.":
            "Penelope [lastname] just said she'd like to have a threesome with her brother. How scandalous!",

        # BM 48280
        "I had to say someone. It's just a game.":
            "I had to say someone, better you than someone I barely know. It's just a game, anyway.",

        # BM 48282
        "*Chuckles* Hey, don't ruin my mood!":
            "*Chuckles* I'm definitely going to remember this.",

        # BM 48383
        "Do you want a glass of water, [mc]?":
            "Do you want a glass of water, bro?",

        # BM 48446
        "Are you okay, [mc]?":
            "Are you okay, bro?",

        # BM 48526
        "I'm not gonna get naked in front of everyone, [mc].":
            "I'm not gonna get naked in front of everyone, bro.",

        # BM 48930
        "To send them to Penelope.":
            "To send them to your sister.",

        # BM 49182
        "*Whispering* I'm sorry I dragged you into this, [mc].":
            "*Whispering* I'm sorry I dragged you into this, bro.",

        # BM 49206
        "Finally! I think she left, [mc]!":
            "Finally! I think she left, bro!",

        # BM 49254
        "My fucking god, [mc], you're hung like a fucking horse. That cock is a weapon!":
            "My fucking god, bro, you're hung like a fucking horse. That cock is a weapon!",

        # BM 49296
        "*Giggles* Oh my, I had no idea you were suffering this much, baby!":
            "*Giggles* Oh my, I had no idea you were suffering this much, bro!",

        # BM 49301
        "*Chuckles* Pretty please... [mc]?":
            "*Chuckles* Pretty please... brother?",

        # BM 49307
        "I'm {i}so{/i} very sorry for flaunting my lewd body in front of you, [mc]. I had no idea it would cause you so much stress...":
            "I'm {i}so{/i} very sorry for flaunting my lewd body in front of you, brother. I had no idea it would cause you so much stress...",

        # BM 49310 Disabled, interferes with other lines, also doesn't work if not on other paths
        # "I like where this is going...":
        #    "I like where this is going... and I am too drunk and horny to care that she is my sister... as if I had cared with Mom and Dalia...",

        # BM 49347
        "Okay, take a good look, [mc].":
            "Okay, take a good look, bro.",

        # BM 49354
        "I'd forgotten how perfect they were, Penny.":
            "I'd forgotten how perfect they were, sis.",

        # BM 49359
        "Not quite yet, Miss Carter...":
            "Not quite yet, Miss [lastname]...",

        # BM 49376
        "Penny... you're a fucking goddess.":
            "Sis... you're a fucking goddess.",

        # BM 49384
        "Admit it. You like being my personal little model, Penny.":
            "Admit it. You like being my personal little model, sis.",

        # BM 49424
        "*Giggles* You're crazy, [mc]...":
            "*Giggles* You're crazy, bro...",

        # BM 49428
        "Damn, [mc]...":
            "Damn, bro...",

        # BM 49442
        "She's mine... For at least tonight, Penelope Carter is all mine...":
            "She's mine... For at least tonight, Penelope [lastname] is all mine...",

        # BM 49454
        "Not my fault. Your tits are literally making me lose my mind, Penny.":
            "Not my fault. Your tits are literally making me lose my mind, sis.",

        # BM 49474
        "*Giggles* Jesus, [mc], how long can you keep up an erection like that?":
            "*Giggles* Jesus, bro, how long can you keep up an erection like that?",

        # BM 49477
        "I mean... holy fuck, Penny.":
            "I mean... holy fuck, sis.",

        # BM 49507
        "My god, Penny, please don't stop...":
            "My god, sis, please don't stop...",

        # BM 49526
        "I think it’s time for me to take the lead, Penny...":
            "I think it’s time for me to take the lead, sis...",

        # BM 49559
        "Your lips are literally dripping over my cock, Penelope...":
            "Your lips are literally dripping over my cock, sis...",

        # BM 49563
        "Don’t even think about it, [mc].":
            "Don’t even think about it, bro.",

        # BM 49590
        "You want it faster? Tell me, Penny...":
            "You want it faster? Tell me, sis...",

        # BM 49606
        "Ohhh Penny...":
            "Ohhh sis...",

        # BM 49610
        "K-Keep up that pace, [mc]...":
            "K-Keep up that pace, bro...",

        # BM 49622
        "You want everyone to treat you like a princess, but deep down you’re a kinky little girl, aren’t you, Penny...?":
            "You want everyone to treat you like a princess, but deep down you’re a kinky little girl, aren’t you, sis...?",

        # BM 49629
        "Ohh... f-fuck me, Penny...":
            "Ohh... f-fuck me, sis...",

        # BM 49631
        "*Choking* Y-Yeagh... u-use me as your fucking toy, [mc]...":
            "*Choking* Y-Yeagh... u-use me as your fucking toy, bro...",

        # BM 49632
        "I wanna make your body writhe in pleasure, Penny...":
            "I wanna make your body writhe in pleasure, sis...",

        # BM 49647
        "*Choking* F-Fuck... I'm gonna cum, [mc]...":
            "*Choking* F-Fuck... I'm gonna cum, bro...",

        # BM 49649
        "F-Fuck, [mc]... I'm gonna cum...":
            "F-Fuck, bro... I'm gonna cum...",

        # BM 49679
        "You're something else, Penny...":
            "You're something else, sis...",

        # BM 49687
        "I'm gonna have to ask you to come to all the parties I'm invited to from now on, [mc].":
            "I'm gonna have to ask you to come to all the parties I'm invited to from now on, bro.",

        # BM 49820
        "What are your plans, [mc]?":
            "What are your plans, bro?",

        # BM 49959
        "I had a lot of fun tonight, [mc]. Thank you.":
            "I had a lot of fun tonight, bro. Thank you.",

        # BM 50081
        "That's the [mc] I know!":
            "That's my son!",

        # BM 50090
        "Thanks for sacrificing your sleep for the mission, [mc].":
            "Thanks for sacrificing your sleep for the mission, honey.",

        # BM 50160
        "After all these years, you're still taking care of me like a babysitter, eh Nancy?":
            "After all these years, you're still taking care of me, eh Mom?",

        # BM 50164
        "Aww, you're too sweet, [mc]! Of course I’ve gotta take care of you.":
            "Aww, sweetie! No matter how old you get, Mommy will always care for you.",

        # BM 50179
        "Don't worry, it's Sunday, so the office will be empty.":
            "Don't worry, it's Sunday, so the office will be empty. And you are my son, I'll just say you came with me to see where I work.",

        # BM 50242
        "Roleplay as Nancy's child":
            "Roleplay as Dalia",

        # BM 50245
        "I've been looking forward to seeing where my... mom works, so she invited me to come with her today.":
            "I've been looking forward to seeing where my mom works, so she invited me to come with her today.",

        # BM 50276
        "I'm not a girl, and I'm not Nancy's child.":
            "I'm not a girl.",

        # BM 50407
        "And you, dear [mc]... are going to retrieve that information.":
            "And you, dear son... are going to retrieve that information.",

        # BM 51008
        "And that's not even taking into account our age difference or my background as your old nanny.":
            "And that's not even taking into account the fact we're mother and son.",

        # BM 51051
        "Our age difference, my daughters, the Student Exchange Program, my history as your former nanny...":
            "The fact we're mother and son, your sisters, the Student Exchange Program...",

        # BM 51185
        "What do they feed you boys nowadays?":
            "What do they feed you boys nowadays? You certainly didn't get that from your father...",

        # BM 51389
        "Can you handle me going faster, sweetie? I'll start slowly... and it'll make your old babysitter feel so much better...":
            "Can you handle me going faster, sweetie? I'll start slowly... and it'll make your mother feel so much better...",

        # BM 51493
        "What a naughty mommy... what if your daughters could see you being fucked like this?":
            "What a naughty mommy... what if my sisters could see you being fucked like this?",

        # BM 52082
        "I kept a mask on because I was afraid that it would scare or hurt my daughters.":
            "I kept a mask on because I was afraid that it would scare or hurt Penny and Dalia.",

        # BM 51640
        "I can't be fired, [mc], I have a family to feed!":
            "I can't be fired, [mc], I have our family to feed!",

        # BM 51781
        "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters would take the news.":
            "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how your sisters would take the news.",

        # BM 52153
        "Of course not! I swear on my daughters!":
            "Of course not! I swear on my children!",

        # BM 52161
        "I have two girls, Dalia and Penelope.":
            "I have two girls and one son, Dalia, Penelope, and [mc].",

        # BM 52162
        "The younger one will start college next fall, and the older one will graduate in a couple of years.":
            "The younger ones will start college next fall, and the oldest one will graduate in a couple of years.",

        # BM 52176
        "I... Whatever you do, you need to hang onto your daughters for as long as you can.":
            "I... Whatever you do, you need to hang onto your kids for as long as you can.",


    # -----------------------------------------
    # v0.6 script6.rpy Lines 52298-66773

        # BM 53852
        "Goddammit, nice job, [mc]!":
            "Goddammit, nice job, bro!",

        # BM 53999
        "No worries [mc], there's nothing important to do tonight.":
            "No worries bro, there's nothing important to do tonight.",

        # BM 54106
        "*Snorts* Of course you’d say that! I'm afraid I'll have to shower alone today, my insatiable stud.":
            "*Snorts* Of course you'd say that! I'm afraid I'll have to shower alone today, my insatiable son.",

        # BM 60104
        "Wow, I love your hair. You look absolutely stunning.":
            "Wow, I love your hair, sis. You look absolutely stunning.",

        # BM 61818
        "Handling the loss like a true sportswoman, Miss Carter.":
            "Handling the loss like a true sportswoman, sis.",

        # BM 62197
        "*Pushing you inside* Goddammit [mc], shut up and get the fuck in!":
            "*Pushing you inside* Goddammit bro, shut up and get the fuck in!",

        # feel like Fuck Marry Kill game could use some rewrites but not really sure what to do for it ~BA

        # BM 62674
        "You always leave me speechless...":
            "You always leave me speechless, sis...",

        # BM 62749
        "*Taking her shirt off* We know each other pretty well already, [mc].":
            "*Taking her shirt off* We know each other pretty well already, bro.",

        # BM 62781
        "(I can't believe I really asked him to go down on me. Alex is such a bad influence, I shouldn't listen to her.)":
            "(I can't believe I really asked my brother to go down on me. Alex is such a bad influence, I shouldn't listen to her.)",

        # BM 62835
        "I want you to get carried away so bad, Dalia...":
            "I want you to get carried away so bad, sis...",

        # BM 62838
        "We're in a cabin in the middle of nowhere, who cares?":
            "We're in a cabin in the middle of nowhere, who cares? And no one will know.",

        # BM 62857
        "Is it weird?":
            "Is it too weird? I mean, we're already siblings as it is...",

        # BM 62867
        "Fuck, you have no fucking idea of how much you're turning me on right now, Dalia.":
            "Fuck, you have no fucking idea of how much you're turning me on right now, sis.",

        # BM 62896
        "(With [mc].)":
            "(With my brother.)",

        # BM 62964
        "F-FUCK, [mc!u]...":
            "F-FUCK, BRO...",

        # BM 62965
        "Oh, Dalia...":
            "Oh, sis...",

        # BM 63046
        "H-H-Holy fuck, [mc]...":
            "H-H-Holy fuck, bro...",

        # BM 63146
        "Fuck, this feels so good, Dalia...":
            "Fuck, this feels so good, sis...",

        # BM 63183
        "(Do I really want [mc] to... fuck me?)":
            "(Do I really want my brother to... fuck me?)",

        # BM 63274
        "I'm g-gonna cum, Dalia...":
            "I'm g-gonna cum, sis...",

        # BM 63280
        "Fuck, Dalia, you're not gonna leave me hanging now, right...?":
            "Fuck, sis, you're not gonna leave me hanging now, right...?",

        # BM 63316
        "Oh Lord, Dalia...":
            "Oh Lord, sis...",

        # BM 63345
        "*Giggles* You're a terrible liar, [mc].":
            "*Giggles* You're a terrible liar, bro.",

        # BM 66449
        "Although... not as much as when you went to Wyatt's house with Nancy Carter, that's for sure.":
            "Although... not as much as when you went to Wyatt's house with Nancy [lastname], that's for sure.",


    # -----------------------------------------
    # v0.7 script7.rpy Lines 66774-80425

        # BM 67196
        "*Snorts* Don't worry, I'm kidding, I'm kidding!":
            "*Snorts* Don't worry, I'm kidding, I'm kidding! I mean, he {i}is{/i} your brother.",

        # BM 67679
        "Penelope Carter plays Eternum!":
            "Penelope [lastname] plays Eternum!",

        # BM 67805
        "*Hyperventilating* I left my drawing utensils at the Carter house last time I was there!":
            "*Hyperventilating* I left my drawing utensils at the [lastname] house last time I was there!",

        # BM 69705
        "She's not my wife":
            "She's my sister",

        # BM 69706
        "Uhh... well, she's my not my wife, but... alright, let's do it.":
            "Uhh... well, she's my sister, not my wife, but... alright, let's do it.",

        # l9453394 note: Changed to be fully compatible with and without either walkthrough
        # BM 69710
        "She's not my wife, yet":
            "{color=[walk_points]}She's my sister... [penelope_pts]",

        # BM 69711, Disabled, think it's better like that ~BA
        # "Well, she's not my wife {i}yet{/i}, but... alright, let's do it.":
        #     "Well, she's my sister and not my wife {i}yet{/i}, but... alright, let's do it.",

        # BM 70960
        "Come on, Dalia!":
            "Come on, sis!",

        # BM 74638
        "(You know that all this teasing with him isn't right.)":
            "(You know that all this teasing with your brother isn't right.)",

        # BM 74736
        "Oh... you mean if I still have a crush on [mc]?":
            "Oh... you mean if I still have a crush on my brother?",

        # BM 74792
        "Penelope Carter is my bestie.":
            "Penelope [lastname] is my bestie.",

        # BM 74912
        "What are you talking about, he's not my step-anything.":
            "What are you talking about? He's not my step-brother, he's my biological brother.",

        # BM 74914 should rework ~BA
        "Well, I know, but didn't you practically grow up around him?":
            "Oh really? I didn't know that.",

        # BM 74915 ditto ~BA
        "You even mentioned babysitting him when your mom had to work.":
            "But didn't you mention babysitting him when your mom had to work?",

        # BM 74917
        "That literally only happened once, and... yeah, so what?":
            "Isn't that a normal thing to do as a big sister?",

        # BM 74918
        "That was ages ago.":
            "And besides, that was ages ago.",

        # BM 75031
        "(We're just two friends goofing around.)":
            "(We're just two siblings goofing around.)",

        # BM 75113
        "{sc=2}PENELOPE{w=.5} P. {w=.5}CARTER.{/sc}":
            "{sc=2}PENELOPE{w=.5} P. {w=.5}[lastname!u].{/sc}",

        # BM 75153
        "Ohh... you brought your photographer friend!":
            "Ohh... you brought your brother!",

        # BM 75229
        "I'm [mc] [lastname] – Penelope Carter's representative.":
            "I'm [mc] [lastname] – Penelope [lastname]'s representative.",

        # BM 75511
        "P-Penelope Paige Carter.":
            "P-Penelope Paige [lastname].",

        # BM 75615
        "Penelope Paige Carter.":
            "Penelope Paige [lastname].",

        # BM 76032
        "I'm glad I have a friend who I trust and with whom I can do these kinds of things, [mc].":
            "I'm glad I have someone who I trust and with whom I can do these kinds of things, bro.",

        # BM 76094
        "*Sitting on the car* Are you okay? Your mind seems to be elsewhere, [mc].":
            "*Sitting on the car* Are you okay? Your mind seems to be elsewhere, bro.",

        # BM 76154
        "C-Can I be frank with you, [mc]?":
            "C-Can I be frank with you, bro?",

        # BM 76244
        "S-Shit... this is crazy, [mc].":
            "S-Shit... this is crazy, bro.",

        # BM 76266
        "Holy fuck, [mc], that feels...":
            "Holy fuck, bro, that feels...",

        # BM 76272
        "Ooh PENNY....":
            "Ooh SIS....",

        # BM 76277
        "I'm having sex with her. I'm fucking Penelope Carter.":
            "I'm having sex with her. I'm fucking my big sister.",

        # BM 76280
        "*Moaning* Aaaghhh, [mc]...":
            "*Moaning* Aaaghhh, bro...",

        # BM 76282
        "*Giggles* Oh y-yeah? You thought about this...? Thought about fucking little old me?":
            "*Giggles* Oh y-yeah? You thought about this...? Thought about fucking your big sister?",

        # BM 76293
        "Jesus Christ, that feels good, Penny...":
            "Jesus Christ, that feels good, sis...",

        # BM 76301
        "*Groaning* F-Fuck, you're so fucking big, [mc]...":
            "*Groaning* F-Fuck, you're so fucking big, bro...",

        # BM 76307
        "Try it for me, baby girl...":
            "Try it for me, sis...",

        # BM 76330
        "You're asking for a lot there, Penny...":
            "You're asking for a lot there, sis...",

        # BM 76343
        "O-Oh my god, [mc], you're stretching me out so much...":
            "O-Oh my god, bro, you're stretching me out so much...",

        # BM 76344
        "Y-You're taking it like a pro, Penny...":
            "Y-You're taking it like a pro, sis...",

        # BM 76353
        "*Panting* F-Fuck, I'm getting tired, [mc]...":
            "*Panting* F-Fuck, I'm getting tired, bro...",

        # BM 76371
        "Fuck me hard, [mc]...":
            "Fuck me hard, bro...",

        # BM 76375
        "*Panting* I-I'm gonna cum so hard, [mc]...":
            "*Panting* I-I'm gonna cum so hard, bro...",

        # BM 76449
        "C’mon... you were talking such a big game earlier, [mc]...":
            "C’mon... you were talking such a big game earlier, brother...",

        # BM 76464
        "*Panting* I just can't stop, Penny...":
            "*Panting* I just can't stop, sis...",

        # BM 76469
        "{sc=2}SWEET LORD, [mc!u]...{/sc}":
            "{sc=2}SWEET LORD, BROTHER...{/sc}",

        # BM 76548
        "*Panting* Fuck, [mc]... don't you ever run out of stamina?":
            "*Panting* Fuck, bro... don't you ever run out of stamina?",

        # BM 76601
        "Crush me against this car, [mc]...":
            "Crush me against this car, bro...",

        # BM 76603
        "Oh yeah, Penny...":
            "Oh yeah, sis...",

        # BM 76645
        "I-I'm at my limit, Penny...":
            "I-I'm at my limit, sis...",

        # BM 76664
        "*Whispering* S-Shit, Penny, keep it down! We need to leave!":
            "*Whispering* S-Shit, sis, keep it down! We need to leave!",

        # BM 76673
        "G-G-Ggggghhhh... P-Pennyyy s-stay quieeeeet...":
            "G-G-Ggggghhhh... S-Siiiiiiissssss s-stay quieeeeet...",

        # BM 77058 phone chat (penelope_chat4)
        "I'm proud of my hot sissy":
            "I'm proud of our hot sissy",

        # BM 76766
        "*Whispering* Oh, Penny...":
            "*Whispering* Oh, sis...",

        # BM 77086
        "*Turning around* Ah, good morning Na-":
            "*Turning around* Ah, good morning Mo-",

        # BM 77089
        "*Gulps* N-Nancy.":
            "*Gulps* M-Mom.",

        # BM 77146
        "Yeah, we're all {i}really{/i} lucky to have you as our friend.":
            "Yeah, they're all {i}really{/i} lucky to have you as their friend.",

        # BM 77184
        "I can see where Penny inherited her love for teasing me.":
            "I can see where Penny and I got our love for teasing.",


    # -----------------------------------------
    # v0.8 script8.rpy Lines 80426-97360

        # BM 83884
        "{i}Listen, I was just calling to see if you've heard anything about my mom. I haven't heard from her in a few months.":
            "{i}Listen, I was just calling to see if you've heard anything about Mom. I haven't heard from her in a few months.",

        # BM 83886
        "What...? There's no power in this world strong enough to stop Nancy from talking to her daughters.":
            "What...? There's no power in this world strong enough to stop Nancy from talking to her kids.",

        # BM 83896
        "Was that Penelope Carter?!":
            "Was that Penelope [lastname]?!",

        # BM 84213
        "The one and only... PENELOPE CARTER!":
            "The one and only... PENELOPE [lastname!u]!",

        # BM 84337
        "Dalia?! Is that you?!":
            "Sis?! Is that you?!",

        # BM 84407
        "{cps=16}However...{cps=1.5} {cps=16}the call from Dalia Carter sparked a glimmer of hope within him, so he decided to head to the coffee area and wait for her.{cps=1} {cps=16}This...{cps=1.4} {cps=16}was his chance.":
            "{cps=16}However...{cps=1.5} {cps=16}the call from Dalia [lastname] sparked a glimmer of hope within him, so he decided to head to the coffee area and wait for her.{cps=1} {cps=16}This...{cps=1.4} {cps=16}was his chance.",

        # BM 84513
        "{cps=17}Our hero was unable to resist the sight of his old friend's ample bosom and alluring figure.{cps=0.6} {cps=16}Overwhelmed by desire, he accepted her offer and surrendered himself to her embrace.":
            "{cps=17}Our hero was unable to resist the sight of his sister's ample bosom and alluring figure.{cps=0.6} {cps=16}Overwhelmed by desire, he accepted her offer and surrendered himself to her embrace.",

        # BM 85311
        "And how about you, Nancy? Have you ever caught Dalia or Penny... you know, giving in to their impulses?":
            "And how about you, Nancy? Have you ever caught Dalia or Penny... you know, giving in to their impulses? Oh, and the one time you burst into MY room doesn't count, I was just getting dressed.",

        # BM 85442
        "And honestly, I had some reservations at first, but now I don't regret it one bit.":
            "And honestly, I had a lot of reservations at first, but now I don't regret it one bit.",

        # BM 85444
        "N-Nancy...?":
            "M-Mom...?",
        
        # BM 85451
        "WHEN?":
            "AREN'T YOU HIS MOM?!",

        # BM 85453
        "A few weeks ago.":
            "Indeed. It happened a few weeks ago.",

        # BM 85457
        "Holy shit, I-I really didn't expect that.":
            "Holy shit, that-that's insane. I-I really didn't expect that.",

        # BM 85984
        "How are you still tight after giving birth to two children...?":
            "How are you still tight after giving birth to three children...?",

        # BM 86121
        "Come here, Nan...":
            "Come here, Mom...",

        # BM 88504
        "My... nanny. She got it for my birthday.":
            "She got it for my birthday.",

        # BM 90558
        "Where'd you find yourself a man like that?":
            "Why didn't I get to know your bro until this late?",

        # BM 92680
        "*Giggles* You get carried away too easily, [mc].":
            "*Giggles* You get carried away too easily, bro.",

        # BM 92687
        "In the end I’m gonna start thinking you’re actually into me, Dalia...":
            "In the end I’m gonna start thinking you’re actually into me, sis...",

        # BM 92734 Added bc relation was never mentioned around Jerry, if I missed it than need to redo this line ~BA
        "That's... a little embarrassing.":
            "That's... a little embarrassing. Shit, does Jerry know we're related?",

        # BM 92789
        "Damn... that took a sad turn all of a sudden.":
            "Doesn't seem like he knows we're related at least, but damn... that took a sad turn all of a sudden.",

        # BM 93284
        "My dad left before I was even born, you fucking idiot.":
            "My dad left when I was a kid, you fucking idiot.",

        # BM 93863
        "You think Nancy wants to play the role of some sort of intermediary? Because she wants it too?":
            "You think your... {i}mom{/i} wants to play the role of some sort of intermediary? Because she wants it too?",

        # BM 95332
        "Thank you for... humoring me with my ramblings, [mc].":
            "Thank you for... humoring me with my ramblings, bro.",

        # BM 95336
        "I also love spending time with you, Dalia.":
            "I also love spending time with you, sis.",

        # BM 95339
        "Do you like me, [mc]?":
            "Do you like me, bro?",

        # BM 95397
        "You mean... love me... like a good friend? Or like a sister?":
            "You mean... love me... as your sister?",

        # BM 95433
        "Yeah, you're smoking hot, but no, I didn't come looking for you because of your “butt”.":
            "Yeah, you're smoking hot, but no, I didn't come looking for you because of your “butt”. It doesn't matter that you're my sister.",

        # BM 95563
        "I know you love it, Dalia, you can't fool me...":
            "I know you love it, sis, you can't fool me...",

        # BM 95564
        "Me? You've been watching too much porn, [mc].":
            "Me? You've been watching too much porn, bro.",

        # BM 95575
        "How is a cute little kiss not enough? You're getting so greedy, [mc]...":
            "How is a cute little kiss not enough? You're getting so greedy, brother...",

        # BM 95671
        "Aghh... you're the best, Dalia...":
            "Aghh... you're the best, sis...",

        # BM 95740
        "*Panting* O-OOH D-D-DALIA, HANG IN RIGHT THERE...":
            "*Panting* O-OOH S-S-SIS, HANG IN RIGHT THERE...",

        # BM 95783
        "You're a horny dog, [mc]. Don't you ever run out of fuel?":
            "You're a horny dog, bro. Don't you ever run out of fuel?",

        # BM 95800
        "You're underestimating the amount of “energy” you just unloaded a minute ago, [mc].":
            "You're underestimating the amount of “energy” you just unloaded a minute ago, brother.",

        # BM 95861
        "*Whispers* Do you want to {i}fuck{/i} me, [mc]...?":
            "*Whispers* Do you want to {i}fuck{/i} your sister, brother...?",

        # BM 95862
        "My god, Dalia, I do...":
            "My god, sis, I do...",

        # BM 95893
        "OH, BABE, YES...":
            "OH, SIS, YES...",

        # BM 96097
        "*Panting* That the childhood friend I used to p-play with would end up ramming her p-perfect, huge ass down on my cock...":
            "*Panting* That my sister would end up ramming her p-perfect, huge ass down on my cock...",

        # BM 95932
        "O-Oh Dalia, I've been waiting for this forever...":
            "O-Oh sis, I've been waiting for this forever...",

        # BM 95947
        "Agghhh... oh [mc]...":
            "Agghhh... oh bro...",

        # BM 95951
        "You have no idea how good your pussy is making me feel right now, Dalia...":
            "You have no idea how good your pussy is making me feel right now, sis...",

        # BM 95953
        "*Moans* AAAAAhhh... [mc]...":
            "*Moans* AAAAAhhh... bro...",

        # BM 95977
        "[mc], I'm gonna cum...":
            "Brother, I'm gonna cum...",

        # BM 95981
        "[mc], I'm cumming...":
            "Bro, I'm cumming...",

        # BM 95984
        "You d-don't have to hold back, Dalia.":
            "You d-don't have to hold back, sis.",

        # BM 96016
        "*Panting* I-I want you to make me cum again, [mc]...":
            "*Panting* I-I want you to make me cum again, bro...",

        # BM 96030
        "*Moans* I-I want you to be the only one t-to ever have me, [mc]...":
            "*Moans* I-I want you to be the only one t-to ever have me, bro...",

        # BM 96089
        "O-Ohh, fuck, Dalia...":
            "O-Ohh, fuck, sis...",

        # BM 96099
        "*Giggling breathlessly* That the idiot who m-moved back in with us w-would...":
            "*Giggling breathlessly* That my idiot brother who m-moved back in with us w-would...",

        # BM 96101
        "Oh fuck, I'm cumming again, [mc]...":
            "Oh fuck, I'm cumming again, bro...",

        # BM 96120
        "Fuck, we can't stop now, Dal...":
            "Fuck, we can't stop now, sis...",

        # BM 96137
        "*Panting* Oh sweet L-Lord, [mc]...":
            "*Panting* Oh sweet L-Lord, bro...",

        # BM 96191
        "F-F-FUCK ME, [mc]...":
            "F-F-FUCK ME, BRO...",

        # BM 96194
        "*Panting* Y-Your pussy's pure fucking magic, Dalia...":
            "*Panting* Y-Your pussy's pure fucking magic, sis...",

        # BM 96260
        "You sound exhausted, Dalia.":
            "You sound exhausted, sis.",

        # BM 96729
        "(Hmm, yeah.)":
            "(Imagine her face if I tell her it was with my brother.)",

        # BM 96732
        "(Or maybe Sissy too...?)":
            "(Sissy would freak out if she knew...)",


    # -----------------------------------------
    # v0.9 script9.rpy Lines 97361-118348

        # still haven't gone over v0.9 yet aaahhhhhhhh ~BA

        # BM 97630
        "I-I don't...":
            "What!? I-I don't... I mean he is our...",

        # BM 97647
        "YOU'RE IN LOVE WITH [mc!u]?!":
            "YOU'RE IN LOVE WITH OUR BROTHER?!",

        # BM 97806
        "I’D STILL HAVE APPRECIATED IT IF MY SISTER HAD TOLD ME SHE WAS SCREWING MY FUCKING BOYFRIEND!":
            "I’D STILL HAVE APPRECIATED IT IF MY SISTER HAD TOLD ME SHE WAS SCREWING MY FUCKING BROTHER!",

        # BM 97808
        "Oh, so he's {i}your{/i} boyfriend now.":
            "Oh, so he's {i}only your{/i} brother now.",

        # BM 97870
        "{sc=3}[mc!u]!!{/sc}":
            "{sc=3}BRO!!{/sc}",

        # BM 97871, Disabled, interferes with other lines
        # "{sc=3}[mc!u]!!!{/sc}":
        #     "{sc=3}BRO!!!{/sc}",

        # BM 99697
        "Last thing [mc] would want is for you to get hurt looking for him.":
            "Last thing your brother would want is for you to get hurt looking for him.",

        # BM 107462
        "Last Christmas, I had a cold kebab in the kitchen while my dad passed out on the couch in the middle of his tenth beer.":
            "Last Christmas, I had a cold kebab in the kitchen while Dad passed out on the couch in the middle of his tenth beer.",

        # BM 107768
        "Honestly, I’d probably feel the same if I hadn’t grown up with my dad.":
            "Honestly, I’d probably feel the same if I hadn’t grown up with Dad.",

        # BM 107843
        "*Starts reading* {i}Dear Ms. Carter, thank you for booking my humble property for this year’s Christmas Eve.":
            "*Starts reading* {i}Dear Ms. [lastname], thank you for booking my humble property for this year’s Christmas Eve.",

        # BM 108222,
        "I don't remember you being one when I still lived in Kredon.":
            "I don't remember you being one when I still lived with you.",

        # BM 108651
        "But I fucking swear to you, Penelope — I love you.":
            "But I fucking swear to you, Penelope — I love you. And I mean not as a sister... as a woman!",

        # BM 108957
        "I mean, it’s 2034. This probably isn’t the freakiest thing you’ll see on the street nowadays.":
            "I mean, it’s 2034. This probably isn’t the freakiest thing you’ll see on the street nowadays. And we are way past the whole incest thing so...",

        # BM 109047
        "Haven't you seen my mom? She’s almost twenty years older than me, and hers are still as firm as a twenty-year-old’s.":
            "Haven't you seen Mom? She’s almost twenty years older than me, and hers are still as firm as a twenty-year-old’s.",

        # BM 109048
        "Genetics are on my side, [mc].":
            "Genetics are on my side, bro.",

        # BM 109288
        "Mmm, I don't know, Penny...":
            "Mmm, I don't know, sis...",

        # BM 109350
        "W-When are you gonna... take that picture, [mc]...?":
            "W-When are you gonna... take that picture, bro...?",

        # BM 109375
        "*Squeezing her breasts together* O-Oh, Penny...":
            "*Squeezing her breasts together* O-Oh, sis...",

        # BM 109431
        "You should learn to savor the moment, [mc]...":
            "You should learn to savor the moment, bro...",

        # BM 109451, but also 76147, 109701 (no negative effect?)
        "Oh, Penny...":
            "Oh, sis...",

        # BM 109459
        "*Giggles* You’re not secretly recording me, right? Taking advantage of little old blind Penny...?":
            "*Giggles* You’re not secretly recording me, right? Taking advantage of your big blind sister...?",

        # BM 109502
        "Your moans are turning shameless, Penny...":
            "Your moans are turning shameless, sis...",

        # BM 109554
        "Finally got too horny, eh, Penny? Or maybe... you just love being on the submissive side?":
            "Finally got too horny, eh, sis? Or maybe... you just love being on the submissive side?",

        # BM 109557
        "Please... [mc]...":
            "Please... bro...",

        # BM 109582
        "It doesn't matter how many times I see you like this, Penny... you still leave me breathless.":
            "It doesn't matter how many times I see you like this, sis... you still leave me breathless.",

        # BM 109641
        "I've said it before, and I'll say it again, Penny — your ass is criminally underrated...":
            "I've said it before, and I'll say it again, sis — your ass is criminally underrated...",

        # BM 109679
        "You're choking my cock, Penny...":
            "You're choking my cock, sis...",

        # BM 109764
        "You're just too much, Penny...":
            "You're just too much, sis...",

        # BM 109797
        "Hey... can I... a-ask you something, [mc]?":
            "Hey... can I... a-ask you something, bro?",

        # BM 109857
        "Have anal sex with Penny":
            "Have anal sex with your sister",

        # BM 109908
        "Last chance to back out, Penny...":
            "Last chance to back out, sis...",

        # BM 109952
        "Oh... fuck Penny, this gets dry so quickly...":
            "Oh... fuck sis, this gets dry so quickly...",

        # BM 109976
        "Ohhh Penny... you’re gonna make me lose my f-fucking mind...":
            "Ohhh sis... you’re gonna make me lose my f-fucking mind...",

        # BM 110202
        "I’ve never had a Christmas dinner like this before, Nan.":
            "I’ve never had a Christmas dinner like this before, Mom.",

        # BM 110413
        "*Chuckles* (Penelope Paige Carter...)":
            "*Chuckles* (Penelope Paige [lastname]...)",

        # BM 111908
        "Like... three of us are literally family here, so...":
            "Like... four of us are literally family here, so...",

        # BM 111909
        "I guess we can just skip ahead and give the points to [mc] and Alex.":
                "I guess we can just skip ahead and give the points to Alex.",

        # BM 111917
        "F-Fine, fine... let's give [mc] his ego boost.":
            "F-Fine, fine... let's give [mc] his perverted ego boost.",

        # BM 111918
        "If I {i}had to{/i} have a threesome with anyone here, I’d pick... [mc] and Alex.":
            "If I {i}had to{/i} have a threesome with anyone here, I’d pick... Alex and as the only male here [mc].",

        # BM 112544
        "This went from zero to nuclear real quick.":
            "This went from zero to nuclear real quick. Your brother...",

        # BM 113157
        "I-I mean... it’s a little weird with [mc] here too, but... whatever." :
            "I-I mean... it’s a little weird with my brother here too, but... whatever." ,

        # BM 113233
        "J-Jesus Christ, [mc].":
            "J-Jesus Christ, bro.",

        # BM 113311
        "Oh, sweet heavens, Dalia...":
            "Oh, sweet heavens, sis...",

        # BM 113364
        "Just... don't get any weird ideas.":
            "Just... don't get any weird ideas. I am [mc]'s sister after all...",

        # BM 113569
        "O-Ohh Dalia, that feels so fucking good...":
            "O-Ohh sis, that feels so fucking good...",

        # BM 113656
        "I-I need you to fuck me, [mc]...":
            "I-I need you to fuck me, bro...",

        # BM 113678
        "C-Christ, you're so fucking tight, Dalia...":
            "C-Christ, you're so fucking tight, sis...",

        # BM 113689
        "*Panting* Yeah... f-fuck me hard, [mc]...":
            "*Panting* Yeah... f-fuck me hard, bro...",

        # BM 113693
        "You're taking it balls-deep f-from the start, Dalia...":
            "You're taking it balls-deep f-from the start, sis...",

        # BM 113702
        "S-S-Slow down, [mc]...":
            "S-S-Slow down, bro...",

        # BM 113732
        "*Groaning* Oh D-Dalia...":
            "*Groaning* Oh s-sis...",

        # BM 113786
        "Oh, Dalia... I-I'm getting close too...":
            "Oh, sis... I-I'm getting close too...",

        # BM 113838
        "I should warn you, though... I'm not as easy as Dalia.":
            "I should warn you, though... I'm not as easy as your sister.",

        # BM 113919
        "*Choked laugh* Y-You're one t-to talk...":
            "*Choked laugh* Y-You're one t-to talk... I-If he's your daddy, am I your a-auntie...?",

        # BM 114015
        "*Grinning* You'll be fine, Dal...":
            "*Grinning* You'll be fine, sis...",

        # BM 114030
        "T-That's because [mc] broke me! A-And all because of you!":
            "T-That's because my brother broke me! A-And all because of you!",

        # BM 114155
        "It’s insane to think about, but... this woman right here is really the reason all of this is even working somehow.":
            "It’s insane to think about, but... my mom is really the reason all of this is even working somehow.",

        # BM 114274
        "Dalia Carter apologizing? This truly is a Christmas miracle.":
            "Dalia [lastname] apologizing? This truly is a Christmas miracle.",
    }


    # cousin_map = {
    # }

    annie_sister_map = {
        # -----------------------------------------
        # Annie as twin sister and Nancy’s child. Add on to base map.
        # Annie has same last name as MC
        # Annie’s father converted to paternal grandparents
        # -----------------------------------------
        # Proofreader's notes signed with ~BA
        # half sis map based on this, if edits are made here check if they can be applied there too.
        # AS 0000 = Annie Sister map, Line number
        # Line numbers based on compiled script from v0.9.0, subject to change in future updates
        #    (which already happened in v0.9.4 fml, too lazy to redo all the numbers)
        # -----------------------------------------

    # -----------------------------------------
    # v0.1 script.rpy  Lines 1-9769

        # AS 826
        "My mother left shortly after I was born and my dad was never around much because he was always so focused on his job.":
            "My mother always cared for me, but my dad was never around much. He was always so focused on his job and never made time for our family. This left Mom to be the only parent taking care of four young kids all while juggling school.",

        # AS 828
        "I know, I know, this all sounds pretty gloomy... but don't worry! This is not about to be one long sob story.":
            "Dad relocated to keep his job and his sanity. He and Mom agreed he'd take me and my twin sister, while she stayed with my two older sisters. I know it sounds a bit bleak, but don't worry—this isn't a sob story.",

        # AS 833
        "He had to work to support us both. Heaven knows where I'd be without him.":
            "He had to work to support the three of us. Heaven knows where we'd be without him.",

        # AS 922
        "(Annie is a close friend from my childhood.)":
            "(Annie is my younger twin sister.)",

        # AS 923
        "(When I moved from Kredon, she was my next-door neighbor and the first person I met, along with Chang.)":
            "(When we moved from Kredon, she was the only familiar person I knew, until I met Chang.)",

        # AS 924
        "(We quickly bonded after discovering we both had something in common... the absence of our parents.)":
            "(Naturally we became really close.)",

        # AS 925
        "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them.)":
            "(It was a chaotic time and we gave each other stability.)",

        # AS 929
        "(Because of how close we were, people always believed we were dating... but the truth is, we're just friends.)":
            "(Because of how close we were, people always joked we would make a great couple... but the truth is, we're just siblings.)",

        # AS 930
        "(I mean… she's cute, and we love spending time with each other, but I've never tried to make a move on her.)":
            "(...)",

        # AS 931
        "(I could never do it.)":
            "(Well you know... I mean if...)",

        # AS 932
        "(She'd probably freak out if I did.)":
            "(NO. Stop it. She'd probably freak out if I did.)",

        # AS 936
        "(It's just not the kind of relationship we have.)":
            "(Why am I even thinking about that!?)",

        # AS 952
        "I was saying that I spoke with Nancy.":
            "I was saying that I spoke with Mom.",

        # AS 956
        "I can't wait to see her. I hope she recognizes me.":
            "I can't wait to see her. I hope she recognizes us.",

        # AS 958
        "*Laughs* I'm sure she will.":
            "*Laughs* I'm sure she will. She is our mother after all.",

        # AS 962 FIXED: Handle both versions
        "(I used to spend the entire afternoon playing with Nancy and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend the entire afternoon playing with Mom and my sisters Dalia and Annie, but then we had to move and ended up losing touch.)",
        
        # AS 962
        "(I used to spend the entire afternoon playing with Mom and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend the entire afternoon playing with Mom and my sisters Dalia and Annie, but then we had to move and ended up losing touch.)",

        # AS 965
        "(Come to find out, she actually had 2 rooms available, so Annie will have a place to stay as well!)":
            "(Come to find out, she actually had our old rooms available!)",

        # AS 966
        "(She’s actually been the one who’s been coordinating with Nancy over the phone, even though they didn’t know each other beforehand.)":
            "(She’s actually been the one who’s been coordinating with Nancy over the phone, I didn't have to do anything.)",

        # AS 969
        "Do you think she will like me?":
            "I'm really excited, do you think everything will go well?",

        # AS 971
        "Nancy? Of course!":
            "Don't worry sis, it'll be alright.",

        # AS 972
        "Don't worry about it, Annie. I haven't seen her in over 10 years, so it’ll probably feel like I’m meeting her for the first time too!":
            "And anyways, it's not like it's a stranger we're meeting, it's our family.",

        # AS 988
        "What's the first thing you're going to do when we get to our new home?":
            "What's the first thing you're going to do when we get to our old home?",

        # AS 1033
        "You should go to sleep too, Annie. We have to wake up early tomorrow.":
            "You should go to sleep too, sis. We have to wake up early tomorrow.",

        # AS 1116
        "We've been through too much together, Annie.":
            "We've literally been together since birth, Annie.",

        # AS 1215
        "Hello everyone! Annie is here!":
            "Hello everyone! Annie is back!",

        # AS 1220
        "I know you're excited Annie, but I'd appreciate it if you could at least carry your hand baggage!":
            "I know you're excited sis, but I'd appreciate it if you could at least carry your hand baggage!",

        # AS 1223
        "It's just that I'm excited to discover the town where you grew up!":
            "It's just that I'm excited to be home again!",

        # AS 1224
        "Well, I left this place when I was 8, so I don’t really remember anything.":
            "Well, I understand, but we left this place when we were 8, so I don't really remember anything.",

        # AS 1225
        "I’ve never had a chance to come back ‘til now, so I'm excited to relive all my childhood memories!":
            "We’ve never had a chance to come back ‘til now, so I'm excited to relive all our childhood memories!",

        # AS 1230
        "Anyway, do you know where Nancy is?":
            "Anyway, do you know where Mom is?",

        # AS 1633
        "Mission failed, [mc]...":
            "Mission failed, bro...",

        # AS 1638
        "You must be Annie!":
            "Annie!",

        # AS 1639
        "Is that right?!":
            "I missed you so much!",

        # AS 1640, Disabled, interferes with other lines
        # "Y-Yeah.":
        #     "Y-Yeah me too.",

        # AS 1641
        "You're even cuter than I imagined! Your voice matches your appearance so much!":
            "You're even cuter than when I last saw you. You've grown so much!",

        # AS 1642
        "T-Thank you, miss.":
            "T-Thank you, Mom.",

        # AS 1643
            "It’s me, Nancy! Even though we’ve only been speaking on the phone for the past few days, I feel like we’ve been becoming good friends already! Isn't that right, Annie?":
                "God, you can't imagine how much I missed you two!",

        # AS 1645
        "Definitely! I’d say we’ve been hitting it off pretty well!":
            "We missed you too, Mom...",

        # AS 1646
        "It's so nice to finally meet you!":
            "It's so nice to finally see you again!",

        # AS 1651
        "I've prepared a room for each of you, though I must warn you – don't expect anything fancy. The bedrooms are pretty small.":
            "I've prepared your old rooms for each of you, though I must warn you – don't expect anything fancy.",

        # AS 1653
        "No worries, miss! I'm sure it'll be more than enough!":
            "No worries, Mom! I'm sure it'll be more than enough!",

        # AS 1655
        "I hope so! And please, just call me Nancy!":
            "I hope so!",

        # AS 1657
        "Okay! Thank you, Nancy!":
            "If they didn't shrink since last time, it'll be alright.",

        # AS 1659
        "Have you ever been to the USA before, Annie?":
            "Do you remember your time in the USA, Annie?",

        # AS 1661
        "Never! But I’ve always wanted to visit. [mc] has always spoken very well of his time in Kredon.":
            "Kind of, but it is all really hard to remember.",

        # AS 1662
        "And of his babysitter!":
            "But I do remember the fun we had playing together!",

        # AS 1669
        "Now I work in a laboratory, but back then I was still finishing my thesis. Thankfully [mc]'s father came along and offered me the babysitting gig.":
            "I work in a laboratory now thanks to my thesis.",

        # AS 1670
        "It was not only well-paid, but also allowed me the flexibility to take care of my daughters at the same time. And for me, being a single mother, that was essential.":
            "It pays some good money.",

        # AS 1672
        "You have 2 daughters, right?":
            "That's good... so how are our sisters?",

        # AS 1674
        "Yes, Dalia and Penelope. Penny was a little older when I was [mc]'s nanny, so she used to play on her own, but Dalia got very close to him!":
            "They're doing well, they've grown up wonderfully like you.",

        # AS 1676
        "*Laughs* I remember she was always stealing my games!":
            "*Laughs* Then they must be doing great!",

        # AS 1678
        "But then, after my daughters grew up, I was able to start a better job within a local company.":
            "Yes... in the beginning I worked a lower-paying job but now that those two are older, I was able to start a better job within a local company.",

        # AS 1683
        "Ahh, aren't you cute!":
            "Ahh, thank you, honey!",

        # AS 1697
        "Alright then! Let's go to the car! Dalia and Penelope are dying to see you again!":
            "Alright then! Let's go to the car! Dalia and Penelope are dying to see you two again!",

        # AS 1719
        "(Each day I would spend the afternoon playing with her and Dalia. We had dinner every night at eight, and then Nancy drove me home once it got late.)":
            "(Each day I would spend the afternoon playing with her, Dalia, and Annie. We had dinner every night at eight, and then went to bed.)",

        # AS 1735
        "Do you like it, Annie?":
            "Do you remember it, Annie?",

        # AS 1736
        "This place looks awesome! Are you rich?!":
            "Yes, this place looks just like I remember!",

        # AS 1737
        "*Laughs* No, I wish. Houses in Kredon are not that expensive.":
            "*Laughs* That's nice, it never felt whole without you two.",

        # AS 1739
        "My husband and I bought it when I was pregnant with Dalia.":
            "Yes it is a good home.",

        # AS 1740
        "Although he left before she was born, so I was left paying the mortgage all by myself...":
            "It's served us well the past years.",

        # AS 1741
        "*Clears throat* But that's a story for another day!":
            "*Clears throat* Let's not get sentimental...",

        # AS 1752
        "That's cool! I love rainy days!":
            "Yes, I remember too! I love rainy days!",

        # AS 1764
        "Did you paint that?!":
            "Do you still paint?",

        # AS 1765
        "Yeah, I used to paint in my free time, but I haven't done anything in years.":
            "No, I haven't done anything in years.",

        # AS 1792
        "I wasn't expecting you to be so excited to meet [mc] again!":
            "I wasn't expecting you to be so excited to meet your brother and sister again!",

        # AS 1808
        "Oh, y-yeah, so excited! Hi [mc]!":
            "Oh, y-yeah, so excited! Hi Annie!",

        # AS 1838
        "Both of those things can wait! You didn't even welcome [mc] and Annie properly!":
            "Both of those things can wait! You didn't even welcome your brother and sister properly!",

        # AS 1839
        "They're gonna live with us for a whole year. You know that, right?":
            "They were away from home for a long time, you know!",

        # AS 1843
        "[mc]! I can't wait to properly meet you!":
            "Hey, bro, I can't wait to hear all about what happened to you and sis!",

        # AS 1846
        "Oh, and you must be Annie! Nice to see you again!":
            "Oh, and Annie! Nice to see you again, sis!",

        # AS 1848
        "Welcome to the family!":
            "Welcome back, you two!",

        # AS 1849
        "By the way, I love your haircut!":
            "By the way, I love your haircut, sis!",

        # AS 1859
        "Of course he doesn't mind!":
            "Of course they don't mind!",

        # AS 1954
        "Annie, you must have gotten the wrong impression of my daughters...":
            "... *looks at Annie*",

        # AS 1956
        "Not at all! They both seem really nice!":
            "Don't worry, Mom!",

        # AS 1957
        "For tonight, I’d rather just unpack all my things and freshen up a bit. We have plenty of time to get to know each other in the days to come!":
            "For tonight, I’d rather just unpack all my things and freshen up a bit. We have plenty of time to catch up in the days to come!",

        # AS 1959
        "You're so nice, Annie. Is there anything I can do for you?":
            "That's nice of you to say, honey. Is there anything I can do for you?",

        # AS 1995
        "Well, since [mc] seems to remember where everything is already... Do you want a tour of the house, Annie?":
            "Well, since [mc] doesn't want a supper... Do you want something, Annie?",

        # AS 2638
        "Oh yeah, that sounds like Annie. I guess she already told you she also plays Eternum?":
            "Oh yeah, that sounds like sis. I guess she already told you she also plays Eternum?",

        # AS 2674
        "(Annie was always good at making friends.)":
            "(Sis was always good at making friends.)",

        # AS 2675
        "(I guess I should let them walk to school on their own, since I don't wanna look like a jealous boyfriend or something.)":
            "(I guess I should let them walk to school on their own, since I don't wanna look like the cliche, overprotective brother.)",

        # AS 2786
        "The lady said no, buddy.":
            "Hands off my sister, you jerk.",

        # AS 2828, 34924
        "Are you okay, Annie?":
            "Are you okay, sis?",

        # AS 2872
        "Will you be alright, Annie?":
            "Will you be alright, sis?",

        # AS 2882
        "And... thank you again for helping me out back there, [mc].":
            "And... thank you again for helping me out back there, bro.",

        # AS 5054
        "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal when I was living with my dad.":
            "I don't know, it felt pretty special to me. Annie and I never really had a nice, home-cooked meal when we were living with Dad.",

        # AS 5076
        "Tomorrow you'll finally be connected to Eternum, [mc]! After waiting for so many years!":
            "Tomorrow you'll finally be connected to Eternum, bro! After waiting for so many years!",

        # AS 5083
        "We’re only missing Nancy and Penelope, then our group would be complete!":
            "We’re only missing Mom and Penelope, then our group would be complete!",

        # AS 5085
        "*Laughs* I wouldn't count on it, Annie, sorry.":
            "*Laughs* I wouldn't count on it, sis, sorry.",

        # AS 5185
        "Nah, don't worry Annie, it's my turn today. But thank you!":
            "Nah, don't worry, sis, it's my turn today. But thank you!",

        # AS 5207
        "Goodnight [mc]!!":
            "Goodnight, bro!!",

        # AS 5459
        "(I mean... If Dalia and Penelope never found out, then would it really be so bad? It’d be our little secret...)":
            "(I mean... If the girls never found out, then would it really be so bad? It’d be our little secret...{w}Of course it would be! He's my son...)",

        # AS 6387
        "(Dammit, Annie didn't tell me about any of this...)":
            "(Dammit, sis didn't tell me about any of this...)",

        # AS 6571
        "No, he's not! He's [mc]! He's tough!":
            "No, he's not! He's my brother! He's tough!",

        # AS 6573
        "So this is the [mc] you're always talking about?":
            "So this is your brother you're always talking about?",

        # AS 6686
        "Thank god I have you, Annie... I’d probably be lost in a ditch somewhere without you!":
            "Thank god I have you, sis... I’d probably be lost in a ditch somewhere without you!",

        # AS 7052
        "(Jeez, I've always tried to not think of Annie in \"that\" way because I don't want to ruin our friendship, but now...)":
            "(Jeez, I really need to stop this... but...)",

        # AS 7062
        "(Damn... I guess she’s not the skinny kid she used to be...)":
            "(Damn... Stop looking at your sister, [mc]...)",

        # AS 7853
        "Oh... Come on Annie, it doesn't matter!":
            "Oh... Come on sis, it doesn't matter!",

        # AS 7978
        "Erm... Y-You're the best friend ever!":
            "Erm... Y-You're the best brother ever!",

        # AS 8343
        "Thank you so much for playing with me, [mc]. It means a lot.":
            "Thank you so much for playing with me, bro. It means a lot.",

        # AS 8344
        "The pleasure was all mine, Annie. Eternum is awesome. I’m so grateful I had you by my side.":
            "The pleasure was all mine, sis. Eternum is awesome. I’m so grateful I had you by my side.",

        # AS 8401
        "You know, I'm not gonna lie, when Mom told me that you and Annie were gonna live with us for a while, I got a little annoyed.":
            "You know, I'm not gonna lie, when Mom told me that you and sis were gonna come back for a while, I didn't know what to think.",


    # -----------------------------------------
    # v0.2 script2.rpy Lines 9770-19471

        # AS 9810
        "I have a feeling this shit is much bigger than we think, Annie.":
            "I have a feeling this shit is much bigger than we think, sis.",

        # AS 9852
        "I don't know, Annie... him having a stroke? I'm not buying it.":
            "I don't know, sis... him having a stroke? I'm not buying it.",

        # AS 9876
        "*Laughs* Don't mind him...":
            "*Laughs* Don't mind my brother...",

        # AS 9883
        "I heard [mc] managed to win a neural implant at your cafe!":
            "I heard my brother managed to win a neural implant at your cafe!",

        # AS 9896
        "Can I play with you guys, [mc]?!":
            "Can I play with you guys, bro?!",

        # AS 9903
        "Horror? Okay... maybe it'd be better if you didn't join us, Annie.":
            "Horror? Okay... maybe it'd be better if you didn't join us, sis.",

        # AS 9937
        "But you're not allowed to complain if you’re scared, Annie!":
            "But you're not allowed to complain if you’re scared, sis!",

        # AS 10580
        "(Maybe his girlfriend...?)":
            "(Maybe his sister...?)",

        # AS 10784
        "Annie should be waiting for us already.":
            "Your sister should be waiting for us already.",

        # AS 10887
        "I love your outfit, Annie!":
            "I love your outfit, sis!",

        # AS 11159
        "Y-You're scaring me, [mc].":
            "Y-You're scaring me, bro.",

        # AS 11735
        "It's okay Annie, I know you’re not one for spooky things, but you’ve been doing good! I’m proud of you!":
            "It's okay sis, I know you’re not one for spooky things, but you’ve been doing good! I’m proud of you!",

        # AS 12675
        "What about you, Annie?":
            "What about you, sis?",

        # AS 13178
        "Oh, [mc]! I wasn’t sure if you were asleep already!":
            "Oh, hey bro! I wasn’t sure if you were asleep already!",

        # AS 13188
        "I told you! You shouldn't have played in Luna's server, Annie! You can't handle that scary stuff! Remember when we played Dead Space?":
            "I told you! You shouldn't have played in Luna's server, sis! You can't handle that scary stuff! Remember when we played Dead Space?",

        # AS 13244
        "You can sleep here as many times as you want. You don’t even have to ask, alright?":
            "You can sleep here as many times as you want. You don’t even have to ask, alright? Just like when we were little.",

        # AS 13249
        "Anytime, Annie.":
            "Anytime, sis.",

        # AS 13274
        "G-Goodnight, [mc].":
            "G-Goodnight, bro.",

        # AS 13276
        "Goodnight Annie.":
            "Goodnight sis.",

        # AS 13288
        "(Oh yeah... I forgot that Annie came to sleep in my room.)":
            "(Oh yeah... I forgot that sis came to sleep in my room.)",

        # AS 13296
        "(She's probably used to hugging a pillow while she sleeps, or something.)":
            "(She's used to hugging a pillow or stuffed animal while she sleeps.)",

        # AS 13300
        "(We're in quite an... intimate position... I don't want her to think I'm trying to take advantage of her while she sleeps.)":
            "(We're in quite an... intimate position... I don't want her to think her brother is trying to take advantage of her while she sleeps.)",

        # AS 13315
        "A-Are you awake, Annie?":
            "A-Are you awake, sis?",

        # AS 13327
        "Baloo?":
            "Baloo? The teddy bear Mom gave you when you were 5?",

        # AS 13329
        "Oh... Well... It's a stuffed bear that my mother gave me when I was 5, and...":
            "Yes, that Baloo...",

        # AS 13334
        "Oh... I didn't know about Baloo.":
            "Oh... I didn't know you still had him.",

        # AS 13364
        "(He probably just sees me as the little girl who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)":
            "(He probably just sees me as his little sister who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)",

        # AS 13365
        "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack.)":
            "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack. And not blood-related ones... he is not a weirdo like me who has feelings for their twin.)",

        # AS 13366
        "(I'll always just be Annie, the \"best friend\".)":
            "(I'll always just be Annie, the \"little sister\".)",

        # AS 13371
        "(I'm a fucking mess. She needs someone more mature.)":
            "(I'm a fucking mess. She needs someone more mature... And someone not blood-related... she is not a weirdo like me who has feelings for their twin.)",

        # AS 13372
        "(This is why I'll always just be [mc], the \"best friend\"...)":
            "(This is why I'll always just be [mc], the \"big brother\"...)",

        # AS 13373
        "It’s just a shirt after all, right...?":
            "It’s just a shirt after all, right... you've seen me without it before...?",

        # AS 13403
        "I mean, yeah, as long as you don't mind...":
            "I mean, yeah, as long as you don't mind... (Even though the last time I saw you topless was when we were 9 and bathing together...)",

        # AS 13412
        "(This doesn't seem like the Annie I’ve known since I was young... Is she trying to prove something?)":
            "(This doesn't seem like the sister I know... Is she trying to prove something?)",

        # AS 13414
        "(...No. You’re a woman now, Annie. It’s time to prove it to yourself... and prove it to [mc].) ":
            "(...No. You’re a woman now, Annie. It’s time to prove it to yourself... and prove it to your brother.)",

        # AS 13417
        "(Holy shit, I’ve never seen her in such an... intimate way...)":
            "(Holy shit, I never noticed know how much she grew over the past years...)",

        # AS 13422
        "(This is really Annie... {i}my{/i} Annie.)":
            "(This is really Annie... {i}my{/i} sister.)",

        # AS 13428
        "We're just... friends getting a little more comfortable.":
            "We're just... siblings getting a little more comfortable.",

        # AS 13442
        "(My precious Annie...)":
            "(My precious sister...)",

        # AS 13445
        "Um, [mc]...? Oh man, I must look weird or someth—":
            "Um, bro...? Oh man, I must look weird or someth—",

        # AS 13447
        "Annie... you are so... beautiful...":
            "Sis... you are so... beautiful...",

        # AS 13473
        "Your skin feels so soft, Annie. It feels... really nice holding you...":
            "Your skin feels so soft, sis. It feels... really nice holding you...",

        # AS 13481
        "(Oh my god, am I the only one feeling all this tension in the air? I want to make a move, but... I don’t want to overstep my bounds...)":
            "(Oh my god, am I the only one feeling all this tension in the air? I kind of want to make a move, but... I don’t want to overstep my bounds... I'm her brother, after all.)",

        # AS 13488
        "(But it’s not just any guy. It’s [mc].)":
            "(But it’s not just any guy. It’s [mc]. My twin brother!)",

        # AS 13489
        "(You've had a crush on him since you were nine years old. You’ve been fantasizing about this moment for so long. Now it’s finally here... what are you going to do about it?)":
            "(You've had a crush on him since you were nine years old, even though he's your brother. You’ve been fantasizing about this moment for so long. Now it’s finally here... what are you going to do about it?)",

        # AS 13498
        "(I better not risk it. This is the closest we’ve ever gotten and I shouldn’t push my luck.)":
            "(I better not risk it. This is the closest we’ve ever gotten and I shouldn’t push my luck. A-And she's still your sister! It's just not right!)",

        # AS 13510
        "Um... Annie...?":
            "Um... sis...?",

        # AS 13533
        "I’m sorry, Annie... I can’t help it... you’re driving me insane...":
            "I’m sorry, sis... I can’t help it... you’re driving me insane...",

        # AS 13546
        "Oh god, Annie...":
            "Oh god, sis...",

        # AS 13562
        "[mc]... Um, I don’t know if I’m ready to go all the way toni-":
            "Bro... Um, I don’t know if I’m ready to go all the way toni-",

        # AS 13567
        "I’m sorry. I’m just a little nervous because no one has ever touched me there before, or even seen it, for that matter.":
            "I’m sorry. I’m just a little nervous because no one has ever touched me there before.",

        # AS 13570
        "[mc]. I said I’m nervous, but that doesn’t mean I... don’t want to...":
            "Bro. I said I’m nervous, but that doesn’t mean I... don’t want to...",

        # AS 13593
        "I’ve never been more sure, Annie.":
            "I’ve never been more sure, sis.",

        # AS 13596
        "I thought you weren’t interested in me...":
            "I thought, as your little sister, you weren’t interested in me...",

        # AS 13598
        "Where did you get that idea from?":
            "That... I-I just, well, you know...",

        # AS 13600
        "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our friendship.":
            "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our relationship as brother and sister.",

        # AS 13637
        "(Holy shit, this is really happening! I'm fucking Annie's thighs!)":
            "(Holy shit, this is really happening! I'm fucking my sister's thighs!)",

        # AS 13642
        "Jesus, Annie...":
            "Jesus, sis...",

        # AS 13694
        "Oh shit, I'm sorry, Annie...":
            "Oh shit, I'm sorry, sis...",

        # AS 13701
        "Did I do something wrong, Annie? I’m sorry! I didn’t know it was going to be that much!":
            "Did I do something wrong, sis? I’m sorry! I didn’t know it was going to be that much!",

        # AS 13712
        "I only came here t-to sleep and then... next thing I know I’m doing that...":
            "I only came here t-to sleep and then... next thing I know I’m doing that... and with my brother...",

        # AS 13715
        "No, no! It's okay! You’re good! I like you, Annie! We can...":
            "No, no! It's okay! You’re good! I like you, sis! We can...",

        # AS 13722
        "We skipped like 14 steps! In one night!":
            "We skipped like 14 steps and broke a dozen rules! In one night!",

        # AS 13734
        "I'm gonna... go... think! Good night [mc]!":
            "I'm gonna... go... think! Good night, bro!",

        # AS 13751
        "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing Annie’s secret kinky side... and I loved every moment of it!)":
            "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing my sister's secret kinky side... and I loved every moment of it!)",

        # AS 14244
        "Annie! Do you have a minute? I wanted to talk to you!":
            "Sis! Do you have a minute? I wanted to talk to you!",

        # AS 14864
        "Look at that perfectly toned stomach... And to think she's had 2 daughters! Unbelievable.":
            "Look at that perfectly toned stomach... And to think she's had 4 children! Unbelievable.",

        # AS 15707
        "And on the first day of school, I saw him harassing a close friend of mine.":
            "And on the first day of school, I saw him harassing my sister.",

        # AS 15134
        "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out.)":
            "(Even if, somehow, he wanted me too... and we ended up... doing it, the girls would be furious if they ever found out. And fucking my son, is that even legal?)",

        # AS 15183
        "(I bet if I tried to do anything at home, Dalia or Penny would surely notice.)":
            "(I bet if I tried to do anything at home, the girls would surely notice.)",


    # -----------------------------------------
    # v0.3 script3.rpy Lines 19472-30120

        # AS 22834
        "Good morning, Annie!":
            "Good morning, sis!",

        # AS 22840
        "Um... Oh! [mc]! Good morning!":
            "Um... Oh! Bro! Good morning!",

        # AS 22892
        "*Taking a deep breath* (Well [mc], it's now or never. Time to grow a pair and man up!)":
            "*Taking a deep breath* (Well [mc], it's now or never. Time to grow a pair and man up! Oh, and fuck the fact that she is your sister, you're well past that point.)",

        # AS 22895
        "I like you, Annie.":
            "I like you, sis.",

        # AS 22903
        "You're my best friend.":
            "You're my twin sister.",

        # AS 22906
        "And in my heart I know, I want us to be so much more than that, too...":
            "But you know what, fuck it I say. I want us to be so much more than that.",

        # AS 22918
        "I don't want to lose our friendship, Annie. I’d be miserable without you in my life.":
            "I don't want to lose you, sis. I’d be miserable without you in my life.",

        # AS 22921
        "I just want us to stay friends forever!":
            "I just want us to stay together forever!",

        # AS 22939
        "That sounds great! Just spending some time together as good friends. Like how we’ve always done it!":
            "That sounds great! Just spending some time together as siblings. Like how we’ve always done it!",

        # AS 22955
        "Like... a fun date between friends?":
            "Like... a fun date with your sister?",

        # AS 22956
        "Hmmm... no, more like a date with a girl that I like. And I just happen to be so lucky in that, she’s also my best friend too. As for what the future holds? Who knows...":
            "Hmmm... no, more like a date with a girl that I like. As for what the future holds? Who knows...",

        # AS 22977
        "Look, [mc], I know we’re going on a {i}date{/i} date, but I really do want to take it slow too. I don’t want you to assume that–":
            "Look, bro, I know we’re going on a {i}date{/i} date, but I really do want to take it slow too. I don’t want you to assume that–",

        # AS 22990
        "T-Thank you, [mc]. I needed this talk.":
            "T-Thank you, bro. I needed this talk.",

        # AS 23033
        "That was quite the goodbye for just a couple of... friends.":
            "That was quite the goodbye for just... twins.",

        # AS 24454
        "I... I know honey, but I don't have anyone else I can call on such short notice to take care of Dalia and [mc].":
            "I... I know honey, but I don't have anyone else I can call on such short notice to take care of your younger siblings.",

        # AS 24479
        "Do you have any idea how much I've sacrificed so that you and Dalia would never be left wanting?!":
            "Do you have any idea how much I've sacrificed so that you four would never be left wanting?!",

        # AS 24518
        "And... what about Dalia and [mc]?":
            "And... what about Dalia, Annie, and [mc]?",

        # AS 24577
        "Nothing... I’m just sad because in a couple of weeks, my dad will be bringing me with him to Europe.":
            "Nothing... I'm just sad because in a couple of weeks, Dad will be taking me and Annie with him to Europe.",

        # AS 24643
        "Absolutely! Don't worry sis, I'll protect you, [mc], and Mom!":
            "Absolutely! Don't worry sis, I'll protect you, [mc], Annie, and Mom too!",

        # AS 24700
        "But you got to bathe first!":
            "But you got to bathe first! I can see the stains on your clothes!",

        # AS 24701 no change, delete or save for the future
        # "Aww! Well okay, I’ll do it for Dory!!":
        #     "Aww! Well okay, I’ll do it for Dory!!",

        # AS 24702
        "Come on [mc], let's go to the bathroom.":
            "Where's Annie? She was playing with you outside earlier.",

        # AS 24703
        "Me too?!":
            "She said she was tired and went to bed.",

        # AS 24704
        "Yeah, let's go! We're all gonna bathe together!":
            "Already? Wake her up, she needs to bathe too.",

        # AS 24705
        "But I'm not dirty!":
            "Okay!",

        # AS 24706
        "I can see the mud stains from here, mister!":
            "After that, we can all watch movies together!",

        # AS 29096
        "We bathed together countless times when you were younger, remember? Your father left for business trips frequently so you stayed over all the time.":
            "We bathed together countless times when you were younger, remember? Your father left for business trips frequently so I took care of you four on my own.",

        # AS 29178
        "I owe it to my mother. It seems like once she reached 25, she stopped aging. She died shortly after Dalia was born, but she was always so full of life.":
            "I owe it to your grandma. It seems like once she reached 25, she stopped aging. She died shortly after Dalia was born. It's a shame she never met you and Annie, she was always so full of life.",

        # AS 29181
        "Dalia and Penelope are gonna be very blessed when they get older too.":
            "Dalia, Penelope, and Annie are gonna be very blessed when they get older too.",

        # AS 29233
        "What about Dalia and Penelope?":
            "What about Dalia, Penelope, and Annie?",


    # -----------------------------------------
    # v0.4 script4.rpy Lines 30121-39683

        # AS 34407
        "(I'm going on a date with [mc]!)":
            "(I'm going on a date with my brother!)",

        # AS 34460
        "*Chuckles* I think you're getting too excited about this, Annie. You need to relax. You'll enjoy it more if you take it less seriously!":
            "*Chuckles* I think you're getting too excited about this, sis. You need to relax. You'll enjoy it more if you take it less seriously!",

        # AS 34470
        "Gonna play some Eternum with ma' homie...":
            "Gonna play some Eternum with ma' bro...",

        # AS 34518
        "Send invitation... to... Annie Winters.":
            "Send invitation... to... Annie [lastname].",

        # AS 34532
        "Annie? Is that you?":
            "Sis? Is that you?",

        # AS 34742
        "Quick, [mc], make a wish!":
            "Quick, bro, make a wish!",

        # AS 35046
        "*Chuckles* A likely story, Ms. Winters... I'll believe you, for now...":
            "*Chuckles* A likely story, Ms. [lastname]... I'll believe you, for now...",

        # AS 35097
        "Come here, [mc]! Jump!":
            "Come here, bro! Jump!",

        # AS 35117
        "Annie, you awake? I can go call the Astrocorp employee if we’re ready to wrap this up.":
            "Sis, you awake? I can go call the Astrocorp employee if we’re ready to wrap this up.",

        # AS 35124
        "You and Chang have always been my best friends, and neither of you played Eternum until recently, so... I've always felt kind of alone here.":
            "You and Chang have always been by my side, and neither of you played Eternum until recently, so... I've always felt kind of alone here.",

        # AS 35128
        "You’re the one who’s really made these first few weeks in Eternum worthwhile, Annie. I couldn't have asked for anyone better to spend time with.":
            "You’re the one who’s really made these first few weeks in Eternum worthwhile, sis. I couldn't have asked for anyone better to spend time with.",

        # AS 35228
        "How's life in Kredon so far?":
            "How's life back in Kredon so far?",

        # AS 35231
        "You were right, it's a rather small town, but there's everything you need!":
            "It's still a rather small town, but there's everything we need!",

        # AS 35232
        "And I felt super welcome in our new home!":
            "And it really feels like we never left!",

        # AS 35233
        "Nancy, Penelope, and Dalia are all very nice to me. They treat me as one of the family. You know I’ve always wanted sisters, so I really feel like they’re giving me that experience!":
            "Mom, Penelope, and Dalia are still so nice to me. You know I’ve always wanted to see our sisters again, so I really feel suuuuuper happy!",

        # AS 35249
        "Assets.":
            "Assets... Why didn't I also get Mom's genes?!",

        # AS 35251
        "Oh! Come on, Annie! You can't be serious!":
            "Oh! Come on, sis! You can't be serious!",

        # AS 35336
        "*Jumps on the bed* Oh my god, [mc]! Look at this!":
            "*Jumps on the bed* Oh my god, bro! Look at this!",

        # l9453394 note: Changed to be fully compatible with and without either walkthrough
        # AS 35431
        "Decline and stay as friends":
            "{color=[walk_path]}Decline and stay as siblings [red][mt](Closes Annie's path)",

        # AS 35434
        "I like you, and you're my best friend, you already know that.":
            "I like you, and you're my sister, you already know that.",

        # AS 35435
        "But... I also feel like we're not meant to be more than that. Things would get awkward if we tried to get together, and our friendship is too important to risk, for me at least.":
            "But... I also feel like we're not meant to be more than that. Things would get awkward if we tried to get together, and our relationship is too important to risk, for me at least.",

        # AS 35437
        "I... I think we're meant to be friends. Best friends!":
            "I... I think we're only meant to be siblings!",

        # AS 35489
        "Y-Yeah... It's been like... 10 years since we first met?":
            "Y-Yeah...",

        # AS 35491
        "That’s quite a while... No big deal.":
            "No big deal.",

        # AS 35502
        "You're so pretty, Annie...":
            "You're so pretty, sis...",

        # AS 35515
        "[mc]! What are you doing?!":
            "Bro! What are you doing?!",

        # AS 35525
        "Seeing you undressing just for me was hot as fuck, Annie.":
            "Seeing you undressing just for me was hot as fuck, sis.",

        # AS 35562
        "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay friends!":
            "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay siblings!",

        # AS 35563
        "It’ll be a little awkward at first, but our friendship is strong, and I know we’d be back to normal in no time.":
            "It’ll be a little awkward at first, but our relationship is strong, and I know we’d be back to normal in no time.",

        # AS 35591
        "*Caressing her cheek* I feel like I could never get enough of you, Annie...":
            "*Caressing her cheek* I feel like I could never get enough of you, sis...",

        # AS 35614
        "Is that so? What have you been thinking about, exactly, Ms. Winters?":
            "Is that so? What have you been thinking about, exactly, Ms. [lastname]?",

        # AS 35646
        "God, there are so many things I want to do to Annie right now... but it's still Annie. I don't wanna cross any line too fast.":
            "God, there are so many things I want to do to Annie right now... but she is still my sister. I don't wanna cross any line too fast.",

        # AS 35648
        "You're making me so horny, Annie...":
            "You're making me so horny, sis...",

        # AS 35724
        "*Panting* K-Keep going, [mc]! Y-You’re hitting just the... r-right spot!":
            "*Panting* K-Keep going, bro! Y-You’re hitting just the... r-right spot!",

        # AS 35741
        "Y-You have to stop! S-STOP! [mc]!":
            "Y-You have to stop! S-STOP! Bro!",

        # AS 35795
        "You turn me on so much, Annie... I'd be lying if I said I wasn’t rock-hard the whole time...":
            "You turn me on so much, sis... I'd be lying if I said I wasn’t rock-hard the whole time...",

        # AS 35844
        "You’re such a good girl, Annie...":
            "You’re such a good girl, sis...",

        # AS 35873
        "D-Do you like beating off my cock, Annie?":
            "D-Do you like beating off my cock, sis?",

        # AS 35885
        "*Panting* F-Fuck, I won't last much longer, Annie...":
            "*Panting* F-Fuck, I won't last much longer, sis...",

        # AS 35887
        "I want to make you cum, [mc]... You were so kind to me...":
            "I want to make you cum, bro... You were so kind to me...",

        # AS 35943
        "I want you so bad, Annie... I can’t wait ‘til the day you can finally take this dick... But not yet...":
            "I want you so bad, sis... I can’t wait ‘til the day you can finally take this dick... But not yet...",

        # AS 35945
        "W-We’ve g-gotta do some practicing b-beforehand, [mc]...":
            "W-We’ve g-gotta do some practicing b-beforehand, bro...",

        # AS 37044
        "Oh Annie... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?":
            "Oh sis... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?",

        # AS 37062
        "Look, Annie! A teleporter! We can get out of here!":
            "Look, sis! A teleporter! We can get out of here!",

        # AS 37106
        "D-Don't look at him, Annie.":
            "D-Don't look at him, sis.",

        # AS 37172
        "*Sobbing* [mc]?":
            "*Sobbing* Bro?",

        # AS 37174
        "D-Don't worry, Annie...":
            "D-Don't worry, sis...",

        # AS 37370
        "Thank you for an amazing day, [mc].":
            "Thank you for an amazing day, bro.",

        # AS 37372
        "I'm glad you enjoyed it, Annie. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.":
            "I'm glad you enjoyed it, sis. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.",

        # AS 37549
        "Oh, already?! Good luck, [mc]! Be sure to get plenty of information!":
            "Oh, already?! Good luck, bro! Be sure to get plenty of information!",

        # AS 37587
        "I can help you out if you want, ma'am.":
            "I can help you out if you want, Mom.",

        # AS 37588
        "I don't know Aunt Cordelia, but I'm good at making collages.":
            "I'm good at making collages.",

        # AS 37593
        "Thank you Annie!":
            "Thank you, sweetie—good to see your father raised you somewhat properly!",


    # -----------------------------------------
    # v0.5 script5.rpy Lines 39684-55297

        # AS 40587
        "We won’t fail you, Nancy! No stone will be left unturned!":
            "We won’t fail you, Mom! No stone will be left unturned!",

        # AS 40689
        "B-Bye, [mc]! I'll see you at home!":
            "B-Bye, bro! I'll see you at home!",

        # AS 44139 phone chats (annie_chat)
        "I've been shopping all day with Nancy and I had no signal!":
            "I've been shopping all day with Mom and I had no signal!",

        "Shopping with Nancy":
            "Shopping with Mom",

        "Shopping with Nancy 😊":
            "Shopping with Mom 😊",

        "Nancy's gonna wonder what's taking me so long":
            "Mom's gonna wonder what's taking me so long",

        # AS 49310 Disabled, interferes with other lines, also doesn't work if not on other paths
        # "I like where this is going...":
        #     "I like where this is going... and I am too horny to care that she is my sister... as if I had cared with Mom, Dalia, or Annie...",

        # AS 52161
        "I have two girls, Dalia and Penelope.":
            "I have three girls and one son, Dalia, Penelope, Annie, and [mc].",


    # -----------------------------------------
    # v0.6 script6.rpy Lines 52298-66773

        # AS 52541
        "Private Annie Winters reports!":
            "Private Annie [lastname] reports!",

        # AS 53976
        "How was your father?":
            "How was Dad?",

        # AS 54065
        "Wow, how come you don’t get this excited when you're playing with your beloved sister?":
            "Wow, how come you don’t get this excited when you're playing with your beloved older sister?",

        # AS 54302
        "It's just... that... well, I was shocked at first since we had {i}never{/i} seen each other naked, and all that.":
            "It's just... that... well, I was shocked at first since the last time I saw you naked was {i}so long{/i} ago.",

        # AS 54273
        "[mc]...? What are you doing here?!":
            "Bro...? What are you doing here?!",

        # AS 57802
        "Oh, thanks for the reassurance, [mc]! I feel much, much better now!":
            "Oh, thanks for the reassurance, brother! I feel much, much better now!",

        # AS 58268
        "*Knocking on the door* Annie?":
            "*Knocking on the door* Sis?",

        # AS 58331
        "And how was your dad?":
            "And how was Dad?",

        # AS 58333
        "My dad...?":
            "Dad...?",

        # AS 58361
        "So... yeah, you know how my father is.":
            "So... yeah, you know how Dad is. He didn't even tell me to say hello to you...",

        # AS 58363
        "Awh, I'm so sorry, [mc]...":
            "Awh, I'm so sorry, bro...",

        # AS 58385
        "You know dads can be real assholes":
            "You know Dad can be a real asshole",

        # AS 58386
        "You know as well as I do that dads can be real assholes.":
            "You know as well as I do that Dad can be a real asshole.",

        # AS 58388
        "W-Well... it's true that my dad has been working a lot all his life and he's been a bit absent, but... he's always cared about me.":
            "W-Well... it's true that Dad's always working and he's been pretty absent, but...",

        # AS 58389
        "And he thinks highly of you!":
            "We still had our grandparents over there!",

        # AS 58391
        "Well... yeah, I guess that's different.":
            "Well... yeah. At least we had some family to care for us.",

        # AS 58392
        "That came out wrong, I'm sorry.":
            "I wish they were able to come over more often.",

        # AS 58394
        "No worries! I know you didn't mean it in a bad way.":
            "I do miss them sometimes.",

        # AS 58697
        "I... I'm n-not sure I'm ready, [mc].":
            "I... I'm n-not sure I'm ready, bro.",

        # AS 58784
        "AAaahh... oh god [mc]... I think I'm gonna... C-CUM...":
            "AAaahh... oh god bro... I think I'm gonna... C-CUM...",

        # AS 58786
        "[mc]! You’re gonna make me...":
            "Bro! You’re gonna make me...",

        # AS 58955
        "The sweet, innocent, little girl I've known for years...":
            "The sweet, innocent, little girl I've known my entire life...",

        # AS 58985
        "You better take care of my little girl while you're in the USA, [mc].":
            "You better take care of your sister while you're in the USA, [mc].",
        
        # AS 58986
        "Rest assured Mr. Winters, I won’t let anything happen to her!":
            "Rest assured Grandpa, I won’t let anything happen to her!",

        # AS 58987
        "I'll take care of Annie as if she was my sister!":
            "I'll take care of Annie!",

        # AS 58998
        "Oh GOD, Annie, I'm gonna fucking cum!":
            "Oh GOD, sis, I'm gonna fucking cum!",

        # AS 59016
        "*Panting* Do it... empty y-yourself all over me, [mc]...":
            "*Panting* Do it... empty y-yourself all over me, bro...",

        # AS 59017
        "Oh god Annie, I'm...":
            "Oh god sis, I'm...",

        # AS 59048
        "Goddammit Annie... that was mind-blowing.":
            "Goddammit sis... that was mind-blowing.",

        # AS 59060
        "Imagine if Nancy had caught us... she'd kick us out of the house!":
            "Imagine if Mom had caught us... she'd go feral!",

        # AS 59064
        "Why would she? We weren't doing anything wrong.":
            "...",


    # -----------------------------------------
    # v0.7 script7.rpy Lines 66774-80425

        # AS 68235
        "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, Annie.":
            "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, sis.",

        # AS 68276
        "Are you sure you don't want to join us, Annie?":
            "Are you sure you don't want to join us, sis?",

        # AS 74971
        "(How would we even explain this to Mom or Dalia?)":
            "(How would we even explain this to Mom, Dalia, or Annie?)",


    # -----------------------------------------
    # v0.8 script8.rpy Lines 80426-97360

        # AS 84648
        "Come on, [mc], I need you to catch on quickly! We're running out of time.":
            "Come on, bro, I need you to catch on quickly! We're running out of time.",

        # AS 84704
        "There's no time to hesitate, [mc]!":
            "There's no time to hesitate, bro!",

        # AS 85984
        "How are you still tight after giving birth to two children...?":
            "How are you still tight after giving birth to four children...?",

        # AS 86947
        "If you ever hurt Nova, Annie, Luna, or Alex... I'll be seriously mad at you, young man.":
            "If you ever hurt Nova, Luna, or Alex... I'll be seriously mad at you, young man.",

        # AS 86949
        "Oh, and if you EVER hurt Penny or Dalia...":
            "Oh, and if you EVER hurt Penny, Dalia, or Annie...",

        # AS 87336
        "Oh, no, no, no. Penny, Dalia, and Nancy were not an option.":
            "Oh, no, no, no. Penny, Dalia, and Mom were not an option.",

        # AS 87518
        "It's straightforward yet stylish, giving off a confident vibe. It shows you're not desperate but also considerate enough to dress well for a date with someone who's been your second-best friend for so many years.":
            "It's straightforward yet stylish, giving off a confident vibe. It shows you're not desperate but also considerate enough to dress well for a date with someone who's been your second-best friend your entire life.",

        # AS 87524
        "Hey, don’t sweat it. I already told you, it gives you a mysterious, sexy vibe.":
            "Hey, don’t sweat it. I already told you, it gives you a mysterious, sexy vibe. And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.",

        # AS 87525
        "And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.":
            "Which is still strange to think about siblings dating, but I just want to tell you again that I support you two. I know how much you mean to each other.",

        # AS 87527
        "*Chuckles* If you say so...":
            "*Chuckles* Thanks, man. I appreciate it a lot.",

        # AS 87824
        "Annie Winters and Luna Hernandez travel to the super scary Red Herring server and complete–":
            "Annie [lastname] and Luna Hernandez travel to the super scary Red Herring server and complete–",

        # AS 87958
        "I'll show them to Nancy later so I can–":
            "I'll show them to Mom later so I can–",

        # AS 88122
        "No one ever thought you were useless, Annie. But after this? D-Damn, even less so.":
            "No one ever thought you were useless, sis. But after this? D-Damn, even less so.",

        # AS 88204
        "Why...? Come on, [mc], you've met up with Annie solo a hundred times, why the jitters now?!":
            "Why...? Come on, [mc], you always have dinners with Annie, why the jitters now?!",

        # The following section is intended to be entirely replaced by new label, this is a backup in case it doesn't work.
        # Needs proofreading tho, hasn't been touched since implementing the label mod lol ~BA

        # AS 88551
        "I live here too! My parents have a hotpot restaurant just around the corner! You and Annie should totally come someday!":
            "I live here too! My parents have a hotpot restaurant just around the corner! You should totally come someday! Hey, you wanna come too?",

        # AS 88553
        "Who's Annie?":
            "Who are you talking to?",

        # AS 88555
        "Annie from school!":
            "The girl!",

        # AS 88557
        "Oh... I don't know her. I just arrived here.":
            "Which girl?",

        # AS 88559
        "Oh... really? And then why is she here?":
            "The one behind you?",

        # AS 88566
        "Hi.":
            "There you are, Annie. I was wondering where you'd gone.",

        # AS 88567
        "Are you Annie?":
            "Is everything alright?",

        # AS 88570
        "*Whispering* Why isn't she talking...?":
            "Annie?",

        # AS 88572
        "*Whispering* I know her from school, but she never talks there either.":
            "Do you know each other?",

        # AS 88573
        "*Whispering* I think she's mute.":
            "*Whispering* Is she mute?",

        # AS 88581
        "I go to school with Chang. I'm Annie.":
            "I'm Annie, [mc]'s sister.",

        # AS 88583
        "Hi Annie. I'm [mc].":
            "This is Chang, Annie",

        # AS 88586
        "D-Did you...":
            "W-We moved here...",

        # AS 88587
        "Did you move here?":
            "Did [mc] already tell you?",

        # AS 88589
        "Yep! From the US, with my dad.":
            "Yep! From the US, with our dad.",

        # AS 88593
        "You shouldn't be out here alone either, Annie.":
            "Nice to meet you, Annie.",

        # AS 88594
        "You could be kidnapped. Or kidnapped and then sold.":
            "Do you want to be my friend, too?.",

        # AS 88596
        "I'm not alone, my dad's over there.":
            "S-Sure Chang.",

        # AS 88598
        "He's a businessman. He's doing business calls now.":
            "I would like to be your friend.",

        # AS 88600
        "We were gonna see the pandas at the zoo, but... he got a call. So I guess we’re not going anymore.":
            "B-But I still like [mc] more then you.",

        # AS 88603
        "I like your... h-hair, American boy.":
            "I like your... h-hair, Chang... And your shirt",

        # AS 88604
        "And your shirt.":
            "But you look better with it, [mc]!",

        # AS 88690
        "Yeah, I should go before my dad gets mad too.":
            "Hmm, then let's wait for Dad.",

        # AS 88691
        "Will you... will you be at school tomorrow?":
            "I wonder if we'll manage... will you help me with school and stuff?",

        # AS 88699
        "You won't ignore me there...?":
            "You won't abandon me...?",

        # AS 88705
        "Promise me we'll be friends!":
            "Promise me we'll be together forever!",

        # AS 88709
        "Friends.":
            "Forever.",

        # AS 88710
        "Friends forever!":
            "Together forever!",

        # AS 88713
        "I'll leave now!":
            "I'll go look for Dad!",

        # AS 88714
        "See you tomorrow... [mc]!":
            "Wait here!",

        # AS 88825
        "Actually, just before you got here, I was reminiscing about the day I met you and Chang.":
            "Actually, just before you got here, I was reminiscing about the day we arrived in Europe and we met Chang.",

        # AS 88829
        "By all means! When I moved to London, I felt like my life was falling apart. You and Chang turned everything around for me.":
            "By all means! When we moved to London, I felt like my life was falling apart. You and Chang turned everything around for me.",

        # AS 88844
        "And where was I going that day with my dad?":
            "And what were we waiting for?",

        # AS 88848
        "To the movie theater":
            "For Chang",

        # l9453394 note: Changed to be fully compatible with and without either walkthrough
        # AS 88850
        # "To see the pandas at the zoo":
        #     "{color=[walk_points]}For dad to finish the registration. [annie_pts]",

        # AS 88852
        "Although... you had to cancel those plans.":
            "You bugged him over and over until he was done.",

        # End label backup section

        # AS 88879
        "Alright, tell me about the first birthday we celebrated together, a couple of years after that.":
            "Alright, tell me what happened on our tenth birthday.",

        # AS 88881
        "We couldn’t celebrate your birthday because you were sick, so we decided to do a joint birthday celebration three weeks later at Chang’s parents' restaurant.":
            "Dad tried to be considerate for once and give us separate birthday parties, but he didn't have the time to plan two parties. So we had a late birthday celebration three weeks later at Chang’s parents’ restaurant.",

        # AS 88923
        "D-Darn it, [mc].":
            "D-Darn it, bro.",

        # AS 89043
        "Your answer could shape how the rest of tonight goes and... maybe even your relationship with Annie.":
            "Your answer could shape how the rest of tonight goes and... maybe even your relationship with your sister.",

        # AS 89217
        "Nancy, Penny, Dalia, Luna, Alex, Nova...":
            "Mom, Penny, Dalia, Luna, Alex, Nova...",

        # AS 89271
        "I'm so impressed, Annie.":
            "I'm so impressed, sis.",

        # AS 89364
        "Dalia, Penny, Nancy, Luna, Nova, Alex...":
            "Dalia, Penny, Mom, Luna, Nova, Alex...",

        # AS 89510
        "Annie Winters.":
            "Annie [lastname].",

        # AS 89581
        "The way you’re tracing your finger on my chest is kind of turning me on more than it should, Annie...":
            "The way you’re tracing your finger on my chest is kind of turning me on more than it should, sis...",

        # AS 89626
        "After so many years thinking I’d never be more than friends with Annie... it's finally happening.":
            "After so many years thinking we’d never be more than siblings... it's finally happening.",

        # AS 89651
        "Phew... you sure know how to drive me crazy, Annie.":
            "Phew... you sure know how to drive me crazy, sis.",

        # AS 89739
        "*Moans* Ohh mmmm-y-yes, [mc]...":
            "*Moans* Ohh mmmm-y-yes, bro...",

        # AS 89808
        "*Tracing Annie's figure* Oh, babe...":
            "*Tracing Annie's figure* Oh, sis...",

        # AS 89941
        "*Panting* Ohh, [mc]...":
            "*Panting* Ohh, bro...",

        # AS 89966
        "Oh, trust me, you've seen nothing yet, my love...":
            "Oh, trust me, you've seen nothing yet, sis...",

        # AS 90370
        "My perfect, beautiful, innocent little Miss Winters...":
            "My perfect, beautiful, innocent little twin sister...",

        # AS 90495
        "B-But I've liked you since the day I met you!":
            "B-But I've always liked you!",


    # -----------------------------------------
    # v0.9 script9.rpy Lines 97361-118348

        # AS 97887
        "*Yawns* Agh, what's with all this noise so early in the morning, girls? You're gonna wake up Annie.":
            "*Yawns* Agh, what's with all this noise so early in the morning, girls? You're gonna wake up your sister.",

        # AS 97913
        "Luckily, I don't have any more sisters he can be with at the moment.":
            "Luckily, I only have one more sister who would never be with her twin brother.",

        # AS 100365
        "Our...":
            "My...",

        # AS 100366
        "Our friend disappeared.":
            "My brother disappeared.",

        # AS 100371
        "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit some family for a few days!":
            "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit your family for a few days!",

        # AS 100373
        "His only family is a drunk skunk of a father living an ocean away.":
            "His only other family is a drunk skunk of a father living an ocean away.",

        # AS 100624
        "*Standing up* No! Didn't you hear Nancy?!":
            "*Standing up* No! Didn't you hear your mom?!",

        # AS 107263
        "Annie flew back to the UK a few days ago to spend Christmas with her family and all, but she’s gonna be back before New Year’s Eve.":
            "Annie flew back to the UK a few days ago to spend Christmas with Grandpa and all, but she’s gonna be back before New Year’s Eve.",

        # AS 107462
        "Last Christmas, I had a cold kebab in the kitchen while my dad passed out on the couch in the middle of his tenth beer.":
            "Last Christmas, Annie and I had cold kebabs in the kitchen while Dad passed out on the couch in the middle of his tenth beer.",

        # AS 107769 new line to rewrite
        "Christmas never felt special to me.":
            "Christmas never felt special to me.",

        # AS 108051 phone chat (annie_chat3)
        "I thought Nancy said you had no signal??":
            "I thought Mom said you had no signal??",

        "But I really gotta go now or my dad will get mad {image=images/MENUS/e_tongue2.png}":
            "But I really gotta go now or Grandpa will get mad",

        # AS 110202 new line to rewrite
        "I’ve never had a Christmas dinner like this before, Nan.":
            "I’ve never had a Christmas dinner like this before, Mom.",
    }

    annie_only_sister_map = {
        # -----------------------------------------
        # Annie is MC’s sister (still twin?), no incest with Nancy, Penny, Dalia.
        # still incomplete
        # -----------------------------------------
        # Proofreader's notes signed with ~BA
        # OS 0000 = Only Sister map, Line number
        # Line numbers based on compiled script from v0.9.0, subject to change in future updates
        #    (which already happened in v0.9.4 fml, too lazy to redo all the numbers)
        # -----------------------------------------

    # -----------------------------------------
    # v0.1 script.rpy  Lines     1-9769

        # OS 833
        "He had to work to support us both. Heaven knows where I'd be without him.":
            "He had to work to support us. Heaven knows where we'd be without him.",

        # OS 922
        "(Annie is a close friend from my childhood.)":
            "(Annie is my sister.)",

        # OS 923
        "(When I moved from Kredon, she was my next-door neighbor and the first person I met, along with Chang.)":
            "(When we moved from Kredon, she was the only familiar person I knew, until I met Chang.)",
        
        # OS 924
        "(We quickly bonded after discovering we both had something in common... the absence of our parents.)":
            "(Naturally we became really close.)",

        # OS 925
        "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them.)":
            "(It was a chaotic time and we gave each other stability.)",

        # OS 929
        "(Because of how close we were, people always believed we were dating... but the truth is, we're just friends.)":
            "(Because of how close we were, people always joked we would make a great couple... but the truth is, we're just siblings.)",

        # OS 930
        "(I mean… she's cute, and we love spending time with each other, but I've never tried to make a move on her.)":
            "(...)",

        # OS 931
        "(I could never do it.)":
            "(Well you know... I mean if...)",

        # OS 932
        "(She'd probably freak out if I did.)":
            "(NO stop it she'd probably freak out if I did.)",

        # OS 936
        "(It's just not the kind of relationship we have.)":
            "(Why am I even thinking about that!?)",

        # OS 961
        "(Nancy used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(Nancy used to be our babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)",

        # OS 962
        "(I used to spend the entire afternoon playing with Nancy and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend the entire afternoon playing with Nancy, her daughter Dalia, and Annie, but then we had to move and ended up losing touch.)",

        # OS 969
        "Do you think she will like me?":
            "I'm really excited, do you think everything will go well?",

        # OS 971
        "Nancy? Of course!":
            "Don't worry sis, it will be alright.",

        # OS 972
        "Don't worry about it, Annie. I haven't seen her in over 10 years, so it’ll probably feel like I’m meeting her for the first time too!":
            "And anyways, it's not like it's a stranger we're meeting, it's our old babysitter.",

        # OS 1109
        "I guess it would be you, Annie.":
            "I guess it would be you, sis.",

        # OS 1116
        "We've been through too much together, Annie.":
            "We've literally been together since birth, Annie.",

        # OS 1223
        "It's just that I'm excited to discover the town where you grew up!":
            "It's just that I'm excited to be home again!",

        # OS 1224
        "Well, I left this place when I was 8, so I don’t really remember anything.":
            "Well, I understand, but we left this place when we were 8, so I don't really remember anything.",

        # OS 1225
        "I’ve never had a chance to come back ‘til now, so I'm excited to relive all my childhood memories!":
            "We’ve never had a chance to come back ‘til now, so I'm excited to relive all our childhood memories!",


    # -----------------------------------------
    # v0.2 script2.rpy Lines  9770-19471


    # -----------------------------------------
    # v0.3 script3.rpy Lines 19472-30120


    # -----------------------------------------
    # v0.4 script4.rpy Lines 30121-39683


    # -----------------------------------------
    # v0.5 script5.rpy Lines 39684-55297


    # -----------------------------------------
    # v0.6 script6.rpy Lines 52298-66773


    # -----------------------------------------
    # v0.7 script7.rpy Lines 66774-80425


    # -----------------------------------------
    # v0.8 script8.rpy Lines 80426-97360


    # -----------------------------------------
    # v0.9 script9.rpy Lines 97361-118348


    }

    annie_half_sister_map = {
        # -----------------------------------------
        # Annie as half-sister, result of Dad cheating while on business trips to the UK. Add on to base map.
        # No last name changes as Nancy and Annie's mom keep their maiden names
        # Editor for this section here: Sorry but I am too lazy to write an entire new map, so I decided to copy the twin sister map and do edits to make it fit the half sister setting
        # -----------------------------------------
        # Proofreader's notes signed with ~BA
        # HS 0000 = Half Sister map, Line number
        # Line numbers based on compiled script from v0.9.0, subject to change in future updates
        #    (which already happened in v0.9.4 fml, too lazy to redo all the numbers)
        # -----------------------------------------

    # -----------------------------------------
    # v0.1 script.rpy  Lines 1-9769

        # HS 826
        "My mother left shortly after I was born and my dad was never around much because he was always so focused on his job.":
            "My mother always cared for me, but my dad was never around much. He was always so focused on his job and never made time for our family. This left Mom to be the only parent taking care of three young kids all while juggling school.",

        # HS 827
        "That’s actually why we ended up moving to the UK; Dad needed to relocate there to keep his position.":
            "Things went south when Mom discovered that many of the so-called \"work\" related \"trips\", were his other wife and family. This led to a huge quarrel and an ugly divorce, and that's why we ended up moving to the UK.",

        # HS 828
        "I know, I know, this all sounds pretty gloomy... but don't worry! This is not about to be one long sob story.":
            "Dad relocated to live with his other family. Apart from that, he also managed to get the custody of me, while Mom stayed with my two older sisters. I know it sounds a bit bleak, but don't worry—this isn't a sob story.",

        # HS 832
        "Even after moving, my father continued to work all day. I could never really blame him, though.":
            "The same can't be said of my dad's second marriage, though. It never really worked out, so they soon divorced once again, leaving my father with only me under his care.",

        # HS 833
        "He had to work to support us both. Heaven knows where I'd be without him.":
            "Despite his other problems, at least he didn't fail to support us both economically. Heaven knows where I'd be without him.",

        # HS 922
        "(Annie is a close friend from my childhood.)":
            "(Annie is my half-sister.)",

        # HS 923
        "(When I moved from Kredon, she was my next-door neighbor and the first person I met, along with Chang.)":
            "(When we moved from Kredon, she was the first person I met, along with Chang.)",

        # HS 924
        "(We quickly bonded after discovering we both had something in common... the absence of our parents.)":
            "(Living in the same semi-functional family, albeit not for long, naturally made us really close.)",

        # HS 925
        "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them.)":
            "(It was a chaotic time and we gave each other stability.)",

        # HS 929
        "(Because of how close we were, people always believed we were dating... but the truth is, we're just friends.)":
            "(Because of how close we were, people always joked we would make a great couple... but the truth is, we're just siblings.)",

        # HS 930
        "(I mean… she's cute, and we love spending time with each other, but I've never tried to make a move on her.)":
            "(...)",

        # HS 931
        "(I could never do it.)":
            "(Well you know... I mean if...)",

        # HS 932
        "(She'd probably freak out if I did.)":
            "(NO. Stop it. She'd probably freak out if I did.)",

        # HS 936
        "(It's just not the kind of relationship we have.)":
            "(Why am I even thinking about that!?)",

        # HS 958
        "*Laughs* I'm sure she will.":
            "*Laughs* I'm sure she will. She is your mother after all.",

        # HS 965
        "(Come to find out, she actually had 2 rooms available, so Annie will have a place to stay as well!)":
            "(Come to find out, she actually had not only my old room, but also an extra room available, so Annie will have a place to stay as well!)",

        # HS 966
        "(She’s actually been the one who’s been coordinating with Nancy over the phone, even though they didn’t know each other beforehand.)":
            "(She’s actually been the one who’s been coordinating with Nancy over the phone, and things seem to be well despite the complicated family matter.)",

        # HS 969
        "Do you think she will like me?":
            "Do you think she will like me? I mean, considering all those things between them...",

        # HS 971
        "Nancy? Of course!":
            "Mom? Of course she's going to like you! You don't have to burden yourself with Dad's mistake.",

        # HS 972
        "Don't worry about it, Annie. I haven't seen her in over 10 years, so it’ll probably feel like I’m meeting her for the first time too!":
            "Mom was never a petty person, and despite not seeing her in over 10 years, I'm sure she hasn't changed in that aspect.",

        # HS 988
        "What's the first thing you're going to do when we get to our new home?":
            "What's the first thing you're going to do when we get to your old home?",

        # HS 1033
        "You should go to sleep too, Annie. We have to wake up early tomorrow.":
            "You should go to sleep too, sis. We have to wake up early tomorrow.",

        # HS 1055
        "You're nothing but a big ball of envy because your best friend can play Eternum and you can't since you didn't save any money.":
            "You're nothing but a big ball of envy because your favorite sister can play Eternum and you can't since you didn't save any money.",

        # HS 1060
        "B-Best friend?":
            "F-Favorite?",

        # HS 1061
        "I thought I was your best friend, [mc]!":
            "I thought I was your favorite, [mc]!",

        # HS 1067
        "I'm not your best friend?":
            "I'm not your favorite?",

        # HS 1068
        "Um... well, yeah, of course you’re my best friend Annie!":
            "Um... well, yeah, of course you’re my favorite Annie!",

        # HS 1071
        "You're both my best friends!":
            "You're both my favorite!",

        # HS 1075
        "Yeah, who's your {i}bestest{/i} friend, me or Chang?":
            "Yeah, who's your {i}favorite{/i}, me or Chang?",

        # HS 1076
        "T-They're different kinds of friendship!":
            "T-They're different kinds of favorite!",

        # HS 1078
        "Who is the {b}ONE TRUE{/b} best friend?!":
            "Who is the {b}ONE TRUE{/b} favorite?!",

        # HS 1096
        "But that doesn't mean you aren’t also my best friend, Annie!":
            "But that doesn't mean you aren’t also my favorite {i}sister{/i}, Annie!",

        # HS 1116
        "We've been through too much together, Annie.":
            "We've literally lived under the same roof, Annie.",

        # HS 1120
        "But that doesn't mean you aren’t also my best friend, Chang!":
            "But that doesn't mean you aren’t also my favorite, Chang. You are my best friend!",

        # HS 1130
        "You're my best... male friend!":
            "You're my favorite... non-family!",

        # HS 1220
        "I know you're excited Annie, but I'd appreciate it if you could at least carry your hand baggage!":
            "I know you're excited sis, but I'd appreciate it if you could at least carry your hand baggage!",

        # HS 1633
        "Mission failed, [mc]...":
            "Mission failed, bro...",

        # HS 1651
        "I've prepared a room for each of you, though I must warn you – don't expect anything fancy. The bedrooms are pretty small.":
            "I've prepared a room for each of you, though I must warn you – don't expect anything fancy. Remember your old room, [mc]?",

        # HS 1843
        "[mc]! I can't wait to properly meet you!":
            "Hey bro, can't wait to hear all about what happened to you!",

        # HS 1846
        "Oh, and you must be Annie! Nice to meet you too!":
            "Oh, and you must be Annie! Nice to meet you!",

        # HS 2638
        "Oh yeah, that sounds like Annie. I guess she already told you she also plays Eternum?":
            "Oh yeah, that sounds like sis. I guess she already told you she also plays Eternum?",

        # HS 2674
        "(Annie was always good at making friends.)":
            "(Sis was always good at making friends.)",

        # HS 2675
        "(I guess I should let them walk to school on their own, since I don't wanna look like a jealous boyfriend or something.)":
            "(I guess I should let them walk to school on their own, since I don't wanna look like the cliche overprotective brother.)",

        # HS 2786
        "The lady said no, buddy.":
            "Hands off my sister, you jerk.",

        # HS 2828, 34924
        "Are you okay, Annie?":
            "Are you okay, sis?",

        # HS 2872
        "Will you be alright, Annie?":
            "Will you be alright, sis?",

        # HS 2882
        "And... thank you again for helping me out back there, [mc].":
            "And... thank you again for helping me out back there, bro.",

        # HS 5076
        "Tomorrow you'll finally be connected to Eternum, [mc]! After waiting for so many years!":
            "Tomorrow you'll finally be connected to Eternum, bro! After waiting for so many years!",

        # HS 5185
        "Nah, don't worry Annie, it's my turn today. But thank you!":
            "Nah, don't worry, sis, it's my turn today. But thank you!",

        # HS 5207
        "Goodnight [mc]!!":
            "Goodnight, bro!!",

        # HS 5459
        "(I mean... If Dalia and Penelope never found out, then would it really be so bad? It’d be our little secret...)":
            "(I mean... If the girls never found out, then would it really be so bad? It’d be our little secret...{w}Of course it would be! He's my son...)",

        # HS 6387
        "(Dammit, Annie didn't tell me about any of this...)":
            "(Dammit, sis didn't tell me about any of this...)",

        # HS 6571
        "No, he's not! He's [mc]! He's tough!":
            "No, he's not! He's my brother! He's tough!",

        # HS 6573
        "So this is the [mc] you're always talking about?":
            "So this is your brother you're always talking about?",

        # HS 6686
        "Thank god I have you, Annie... I’d probably be lost in a ditch somewhere without you!":
            "Thank god I have you, sis... I’d probably be lost in a ditch somewhere without you!",

        # HS 7052
        "(Jeez, I've always tried to not think of Annie in \"that\" way because I don't want to ruin our friendship, but now...)":
            "(Jeez, I really need to stop this... but...)",

        # HS 7062
        "(Damn... I guess she’s not the skinny kid she used to be...)":
            "(Damn... Stop looking at your sister [mc]...)",

        # HS 7853
        "Oh... Come on Annie, it doesn't matter!":
            "Oh... Come on sis, it doesn't matter!",

        # HS 7978
        "Erm... Y-You're the best friend ever!":
            "Erm... Y-You're the best brother ever!",

        # HS 8343
        "Thank you so much for playing with me, [mc]. It means a lot.":
            "Thank you so much for playing with me, bro. It means a lot.",

        # HS 8344
        "The pleasure was all mine, Annie. Eternum is awesome. I’m so grateful I had you by my side.":
            "The pleasure was all mine, sis. Eternum is awesome. I’m so grateful I had you by my side.",


    # -----------------------------------------
    # v0.2 script2.rpy Lines 9770-19471

        # HS 9810
        "I have a feeling this shit is much bigger than we think, Annie.":
            "I have a feeling this shit is much bigger than we think, sis.",

        # HS 9852
        "I don't know, Annie... him having a stroke? I'm not buying it.":
            "I don't know, sis... him having a stroke? I'm not buying it.",

        # HS 9876
        "*Laughs* Don't mind him...":
            "*Laughs* Don't mind my brother...",

        # HS 9883
        "I heard [mc] managed to win a neural implant at your cafe!":
            "I heard my brother managed to win a neural implant at your cafe!",

        # HS 9896
        "Can I play with you guys, [mc]?!":
            "Can I play with you guys, bro?!",

        # HS 9903
        "Horror? Okay... maybe it'd be better if you didn't join us, Annie.":
            "Horror? Okay... maybe it'd be better if you didn't join us, sis.",

        # HS 9937
        "But you're not allowed to complain if you’re scared, Annie!":
            "But you're not allowed to complain if you’re scared, sis!",

        # HS 10784
        "Annie should be waiting for us already.":
            "Your sister should be waiting for us already.",

        # HS 10887
        "I love your outfit, Annie!":
            "I love your outfit, sis!",

        # HS 11159
        "Y-You're scaring me, [mc].":
            "Y-You're scaring me, bro.",

        # HS 11735
        "It's okay Annie, I know you’re not one for spooky things, but you’ve been doing good! I’m proud of you!":
            "It's okay sis, I know you’re not one for spooky things, but you’ve been doing good! I’m proud of you!",

        # HS 12675
        "What about you, Annie?":
            "What about you, sis?",

        # HS 13178
        "Oh, [mc]! I wasn’t sure if you were asleep already!":
            "Oh, hey bro! I wasn’t sure if you were asleep already!",

        # HS 13188
        "I told you! You shouldn't have played in Luna's server, Annie! You can't handle that scary stuff! Remember when we played Dead Space?":
            "I told you! You shouldn't have played in Luna's server, sis! You can't handle that scary stuff! Remember when we played Dead Space?",

        # HS 13244
        "You can sleep here as many times as you want. You don’t even have to ask, alright?":
            "You can sleep here as many times as you want. You don’t even have to ask, alright? Just like when we were little.",

        # HS 13249
        "Anytime, Annie.":
            "Anytime, sis.",

        # HS 13274
        "G-Goodnight, [mc].":
            "G-Goodnight, bro.",

        # HS 13276
        "Goodnight Annie.":
            "Goodnight sis.",

        # HS 13288
        "(Oh yeah... I forgot that Annie came to sleep in my room.)":
            "(Oh yeah... I forgot that sis came to sleep in my room.)",

        # HS 13296
        "(She's probably used to hugging a pillow while she sleeps, or something.)":
            "(I remember seeing her hugging a teddy bear at night when we still lived together, so that's probably why she grabbed me.)",

        # HS 13300
        "(We're in quite an... intimate position... I don't want her to think I'm trying to take advantage of her while she sleeps.)":
            "(We're in quite an... intimate position... I don't want her to think I'm trying to take advantage of her while she sleeps, especially since I'm her brother for Christ's sake.)",

        # HS 13315
        "A-Are you awake, Annie?":
            "A-Are you awake, sis?",

        # HS 13334
        "Oh... I didn't know about Baloo.":
            "Oh him... I didn't know his name is Baloo.",

        # HS 13364
        "(He probably just sees me as the little girl who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)":
            "(He probably just sees me as his little sister who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)",

        # HS 13365
        "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack.)":
            "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack. And not blood-related ones... he is not a weirdo like me who has feelings for their sibling.)",

        # HS 13366
        "(I'll always just be Annie, the \"best friend\".)":
            "(I'll always just be Annie, the \"little sister\".)",

        # HS 13371
        "(I'm a fucking mess. She needs someone more mature.)":
            "(I'm a fucking mess. She needs someone more mature... And someone not blood-related... she is not a weirdo like me who has feelings for their sibling.)",

        # HS 13372
        "(This is why I'll always just be [mc], the \"best friend\"...)":
            "(This is why I'll always just be [mc], the \"big brother\"...)",

        # HS 13373
        "It’s just a shirt after all, right...?":
            "It’s just a shirt after all, right... you've seen me without it before...?",

        # HS 13403
        "I mean, yeah, as long as you don't mind...":
            "I mean, yeah, as long as you don't mind... (Even though the last time I saw you topless was when we were 9 and bathing together...)",

        # HS 13412
        "(This doesn't seem like the Annie I’ve known since I was young... Is she trying to prove something?)":
            "(This doesn't seem like the sister I know... Is she trying to prove something?)",

        # HS 13414
        "(...No. You’re a woman now, Annie. It’s time to prove it to yourself... and prove it to [mc].) ":
            "(...No. You’re a woman now, Annie. It’s time to prove it to yourself... and prove it to your brother.)",

        # HS 13417
        "(Holy shit, I’ve never seen her in such an... intimate way...)":
            "(Holy shit, I never noticed know how much she grew over the past years...)",

        # HS 13422
        "(This is really Annie... {i}my{/i} Annie.)":
            "(This is really sis... {i}my{/i} sister.)",

        # HS 13428
        "We're just... friends getting a little more comfortable.":
            "We're just... siblings getting a little more comfortable.",

        # HS 13442
        "(My precious Annie...)":
            "(My precious sister...)",

        # HS 13445
        "Um, [mc]...? Oh man, I must look weird or someth—":
            "Um, bro...? Oh man, I must look weird or someth—",

        # HS 13447
        "Annie... you are so... beautiful...":
            "Sis... you are so... beautiful...",

        # HS 13473
        "Your skin feels so soft, Annie. It feels... really nice holding you...":
            "Your skin feels so soft, sis. It feels... really nice holding you...",

        # HS 13481
        "(Oh my god, am I the only one feeling all this tension in the air? I want to make a move, but... I don’t want to overstep my bounds...)":
            "(Oh my god, am I the only one feeling all this tension in the air? I kind of want to make a move, but... I don’t want to overstep my bounds... I AM her brother after all)",

        # HS 13488
        "(But it’s not just any guy. It’s [mc].)":
            "(But it’s not just any guy. It’s [mc]. My brother!)",

        # HS 13489
        "(You've had a crush on him since you were nine years old. You’ve been fantasizing about this moment for so long. Now it’s finally here... what are you going to do about it?)":
            "(You've had a crush on him since you were nine years old, even though he's your brother. You’ve been fantasizing about this moment for so long. Now it’s finally here... what are you going to do about it?)",

        # HS 13498
        "(I better not risk it. This is the closest we’ve ever gotten and I shouldn’t push my luck.)":
            "(I better not risk it. This is the closest we’ve ever gotten and I shouldn’t push my luck. A-And she's still your sister! It's just not right!)",

        # HS 13510
        "Um... Annie...?":
            "Um... Sis...?",

        # HS 13533
        "I’m sorry, Annie... I can’t help it... you’re driving me insane...":
            "I’m sorry, sis... I can’t help it... you’re driving me insane...",

        # HS 13546
        "Oh god, Annie...":
            "Oh god, sis...",

        # HS 13562
        "[mc]... Um, I don’t know if I’m ready to go all the way toni-":
            "Bro... Um, I don’t know if I’m ready to go all the way toni-",

        # HS 13567
        "I’m sorry. I’m just a little nervous because no one has ever touched me there before, or even seen it, for that matter.":
            "I’m sorry. I’m just a little nervous because no one has ever touched me there before.",

        # HS 13570
        "[mc]. I said I’m nervous, but that doesn’t mean I... don’t want to...":
            "Bro. I said I’m nervous, but that doesn’t mean I... don’t want to...",

        # HS 13593
        "I’ve never been more sure, Annie.":
            "I’ve never been more sure, sis.",

        # HS 13596
        "I thought you weren’t interested in me...":
            "I thought, as your little sister, you weren’t interested in me...",

        # HS 13598
        "Where did you get that idea from?":
            "That... I-I just well you know...",

        # HS 13600
        "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our friendship.":
            "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our relationship as brother and sister.",

        # HS 13637
        "(Holy shit, this is really happening! I'm fucking Annie's thighs!)":
            "(Holy shit, this is really happening! I'm fucking my sister's thighs!)",

        # HS 13642
        "Jesus, Annie...":
            "Jesus, sis...",

        # HS 13694
        "Oh shit, I'm sorry, Annie...":
            "Oh shit, I'm sorry, sis...",

        # HS 13701
        "Did I do something wrong, Annie? I’m sorry! I didn’t know it was going to be that much!":
            "Did I do something wrong, sis? I’m sorry! I didn’t know it was going to be that much!",

        # HS 13712
        "I only came here t-to sleep and then... next thing I know I’m doing that...":
            "I only came here t-to sleep and then... next thing I know I’m doing that... and with my brother...",

        # HS 13715
        "No, no! It's okay! You’re good! I like you, Annie! We can...":
            "No, no! It's okay! You’re good! I like you, sis! We can...",

        # HS 13722
        "We skipped like 14 steps! In one night!":
            "We skipped like 14 steps and broke a dozen rules! In one night!",

        # HS 13751
        "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing Annie’s secret kinky side... and I loved every moment of it!)":
            "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing my sister's secret kinky side... and I loved every moment of it!)",

        # HS 13734
        "I'm gonna... go... think! Good night [mc]!":
            "I'm gonna... go... think! Good night bro!",

        # HS 14244
        "Annie! Do you have a minute? I wanted to talk to you!":
            "Sis! Do you have a minute? I wanted to talk to you!",

        # HS 15134
        "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out.)":
            "(Even if, somehow, he wanted me too... and we ended up... doing it, the girls would be furious if they ever found out. And fucking my son, is that even legal?)",

        # HS 15183
        "(I bet if I tried to do anything at home, Dalia or Penny would surely notice.)":
            "(I bet if I tried to do anything at home, the girls would surely notice.)",

        # HS 15707
        "And on the first day of school, I saw him harassing a close friend of mine.":
            "And on the first day of school, I saw him harassing my sister.",

        # HS 18085 last name override
        "I was wondering why Nancy and her shared the same last name on your followers list. Nancy is her mom!":
            "I was wondering why Nancy and her shared the same last name on your followers list. Nancy is her mom!",

        # HS 18088
        "Never mind...":
            "Well, actually she's also my sister, but never mind...",

        # HS 18090
        "Can I go say hi?":
            "That's even better then, you can introduce me! Can I go say hi?",

    # -----------------------------------------
    # v0.3 script3.rpy Lines 19472-30120

        # HS 22834
        "Good morning, Annie!":
            "Good morning, sis!",

        # HS 22840
        "Um... Oh! [mc]! Good morning!":
            "Um... Oh! Bro! Good morning!",

        # HS 22892
        "*Taking a deep breath* (Well [mc], it's now or never. Time to grow a pair and man up!)":
            "*Taking a deep breath* (Well [mc], it's now or never. Time to grow a pair and man up! Oh, and fuck the fact that she is your sister, you're well past that point.)",

        # HS 22895
        "I like you, Annie.":
            "I like you, sis.",

        # HS 22903
        "You're my best friend.":
            "You're my sister.",

        # HS 22906
        "And in my heart I know, I want us to be so much more than that, too...":
            "But you know what, fuck it I say. I want us to be so much more than that.",

        # HS 22918
        "I don't want to lose our friendship, Annie. I’d be miserable without you in my life.":
            "I don't want to lose you, sis. I’d be miserable without you in my life.",

        # HS 22921
        "I just want us to stay friends forever!":
            "I just want us to stay together forever!",

        # HS 22939
        "That sounds great! Just spending some time together as good friends. Like how we’ve always done it!":
            "That sounds great! Just spending some time together as siblings. Like how we’ve always done it!",

        # HS 22955
        "Like... a fun date between friends?":
            "Like... a fun date with your sister?",

        # HS 22956
        "Hmmm... no, more like a date with a girl that I like. And I just happen to be so lucky in that, she’s also my best friend too. As for what the future holds? Who knows...":
            "Hmmm... no, more like a date with a girl that I like. As for what the future holds? Who knows...",

        # HS 22977
        "Look, [mc], I know we’re going on a {i}date{/i} date, but I really do want to take it slow too. I don’t want you to assume that–":
            "Look, bro, I know we’re going on a {i}date{/i} date, but I really do want to take it slow too. I don’t want you to assume that–",

        # HS 22990
        "T-Thank you, [mc]. I needed this talk.":
            "T-Thank you, bro. I needed this talk.",

        # HS 23033
        "That was quite the goodbye for just a couple of... friends.":
            "That was quite the goodbye for just... siblings.",

        # HS 24552 last name override
        "*Clears throat* Hello, this is Nancy Carter.":
            "*Clears throat* Hello, this is Nancy Carter.",

        # HS 29233 Umm... offering up your own daughters is one thing, but offering up someone else's is a bit much ~QA
        "What about Dalia and Penelope?":
            "What about Dalia, Penelope, and Annie?",

        # HS 29242 Ditto ~BA
        "Why not? I wouldn’t mind having you as my son-in-law...":
            "Why not? I wouldn't mind. I'm sure Annie's mom wouldn't mind as well...",


    # -----------------------------------------
    # v0.4 script4.rpy Lines 30121-39683

        # HS 33051 last name override
        "And on my right, weighing in at 125 lbs... Dalia Carter!":
            "And on my right, weighing in at 125 lbs... Dalia Carter!",

        # HS 34407
        "(I'm going on a date with [mc]!)":
            "(I'm going on a date with my brother!)",

        # HS 34460
        "*Chuckles* I think you're getting too excited about this, Annie. You need to relax. You'll enjoy it more if you take it less seriously!":
            "*Chuckles* I think you're getting too excited about this, sis. You need to relax. You'll enjoy it more if you take it less seriously!",

        # HS 34470
        "Gonna play some Eternum with ma' homie...":
            "Gonna play some Eternum with ma' bro...",

        # HS 34532
        "Annie? Is that you?":
            "Sis? Is that you?",

        # HS 34742
        "Quick, [mc], make a wish!":
            "Quick, bro, make a wish!",

        # HS 35035
        "(I mean... of course we're not. We haven't even...)":
            "(I mean... of course we're not. We are siblings, after all...)",

        # HS 35097
        "Come here, [mc]! Jump!":
            "Come here, bro! Jump!",

        # HS 35117
        "Annie, you awake? I can go call the Astrocorp employee if we’re ready to wrap this up.":
            "Sis, you awake? I can go call the Astrocorp employee if we’re ready to wrap this up.",

        # HS 35124
        "You and Chang have always been my best friends, and neither of you played Eternum until recently, so... I've always felt kind of alone here.":
            "You and Chang have always been by my side, and neither of you played Eternum until recently, so... I've always felt kind of alone here.",

        # HS 35128
        "You’re the one who’s really made these first few weeks in Eternum worthwhile, Annie. I couldn't have asked for anyone better to spend time with.":
            "You’re the one who’s really made these first few weeks in Eternum worthwhile, sis. I couldn't have asked for anyone better to spend time with.",

        # HS 35232
        "And I felt super welcome in our new home!":
            "And I felt super welcome in your old home!",

        # HS 35233
        "Nancy, Penelope, and Dalia are all very nice to me. They treat me as one of the family. You know I’ve always wanted sisters, so I really feel like they’re giving me that experience!":
            "Nancy, Penelope, and Dalia are all very nice to me. I was worried they would hold a grudge against me or my mom, but nothing like that ever happened. They treat me as one of the family!",

        # HS 35235
        "Happy to hear that!":
            "I told you that you were thinking too much on the train, didn't I? I'm so happy that you're able to get along with them.",

        # HS 35251
        "Oh! Come on, Annie! You can't be serious!":
            "Oh! Come on, sis! You can't be serious!",

        # HS 35336
        "*Jumps on the bed* Oh my god, [mc]! Look at this!":
            "*Jumps on the bed* Oh my god, bro! Look at this!",

        # l9453394 note: Changed to be fully compatible with and without either walkthrough
        # HS 35431
        "Decline and stay as friends":
            "{color=[walk_path]}Decline and stay as siblings [red][mt](Closes Annie's path)",

        # HS 35434
        "I like you, and you're my best friend, you already know that.":
            "I like you, and you're my sister, you already know that.",

        # HS 35435
        "But... I also feel like we're not meant to be more than that. Things would get awkward if we tried to get together, and our friendship is too important to risk, for me at least.":
            "But... I also feel like we're not meant to be more than that. Things would get awkward if we tried to get together, and our relationship is too important to risk, for me at least.",

        # HS 35437
        "I... I think we're meant to be friends. Best friends!":
            "I... I think we're only meant to be siblings!",

        # HS 35489 hmmm original 10 years line works for half sis ~BA
        "Y-Yeah... It's been like... 10 years since we first met?":
            "Y-Yeah...",

        # HS 35491
        "That’s quite a while... No big deal.":
            "No big deal.",

        # HS 35502
        "You're so pretty, Annie...":
            "You're so pretty, sis...",

        # HS 35515
        "[mc]! What are you doing?!":
            "Bro! What are you doing?!",

        # HS 35525
        "Seeing you undressing just for me was hot as fuck, Annie.":
            "Seeing you undressing just for me was hot as fuck, sis.",

        # HS 35562
        "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay friends!":
            "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay siblings!",

        # HS 35563
        "It’ll be a little awkward at first, but our friendship is strong, and I know we’d be back to normal in no time.":
            "It’ll be a little awkward at first, but our relationship is strong, and I know we’d be back to normal in no time.",

        # HS 35591
        "*Caressing her cheek* I feel like I could never get enough of you, Annie...":
            "*Caressing her cheek* I feel like I could never get enough of you, sis...",

        # HS 35646
        "God, there are so many things I want to do to Annie right now... but it's still Annie. I don't wanna cross any line too fast.":
            "God, there are so many things I want to do to Annie right now... but she is still my sister. I don't wanna cross any line too fast.",

        # HS 35648
        "You're making me so horny, Annie...":
            "You're making me so horny, sis...",

        # HS 35724
        "*Panting* K-Keep going, [mc]! Y-You’re hitting just the... r-right spot!":
            "*Panting* K-Keep going, bro! Y-You’re hitting just the... r-right spot!",

        # HS 35741
        "Y-You have to stop! S-STOP! [mc]!":
            "Y-You have to stop! S-STOP! bro!",

        # HS 35795
        "You turn me on so much, Annie... I'd be lying if I said I wasn’t rock-hard the whole time...":
            "You turn me on so much, sis... I'd be lying if I said I wasn’t rock-hard the whole time...",

        # HS 35844
        "You’re such a good girl, Annie...":
            "You’re such a good girl, sis...",

        # HS 35873
        "D-Do you like beating off my cock, Annie?":
            "D-Do you like beating off my cock, sis?",

        # HS 35885
        "*Panting* F-Fuck, I won't last much longer, Annie...":
            "*Panting* F-Fuck, I won't last much longer, sis...",

        # HS 35887
        "I want to make you cum, [mc]... You were so kind to me...":
            "I want to make you cum, bro... You were so kind to me...",

        # HS 35943
        "I want you so bad, Annie... I can’t wait ‘til the day you can finally take this dick... But not yet...":
            "I want you so bad, sis... I can’t wait ‘til the day you can finally take this dick... But not yet...",

        # HS 35945
        "W-We’ve g-gotta do some practicing b-beforehand, [mc]...":
            "W-We’ve g-gotta do some practicing b-beforehand, bro...",

        # HS 37044
        "Oh Annie... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?":
            "Oh sis... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?",

        # HS 37062
        "Look, Annie! A teleporter! We can get out of here!":
            "Look, sis! A teleporter! We can get out of here!",

        # HS 37106
        "D-Don't look at him, Annie.":
            "D-Don't look at him, sis.",

        # HS 37172
        "*Sobbing* [mc]?":
            "*Sobbing* bro?",

        # HS 37174
        "D-Don't worry, Annie...":
            "D-Don't worry, sis...",

        # HS 37370
        "Thank you for an amazing day, [mc].":
            "Thank you for an amazing day, bro.",

        # HS 37372
        "I'm glad you enjoyed it, Annie. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.":
            "I'm glad you enjoyed it, sis. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.",

        # HS 37549
        "Oh, already?! Good luck, [mc]! Be sure to get plenty of information!":
            "Oh, already?! Good luck, bro! Be sure to get plenty of information!",

        # HS 37588 original line would work here ~BA
        "I don't know Aunt Cordelia, but I'm good at making collages.":
            "I'm good at making collages.",


    # -----------------------------------------
    # v0.5 script5.rpy Lines 39684-55297

        # HS 40313 last name override
        "Oh, that is very likely, actually, Ms. Carter. It would be poetic and, at the same time, easy to make it look like an accident.":
            "Oh, that is very likely, actually, Ms. Carter. It would be poetic and, at the same time, easy to make it look like an accident.",

        # HS 40493
        "The scholarship that was granted to [mc] and his best friends is the best thing that has happened to me in a very long time.":
            "The scholarship that was granted to [mc] and his favorite people is the best thing that has happened to me in a very long time.",

        # HS 40495
        "*Clears throat* I think it's best not to dig too deep into the \"best friend\" subject.":
            "*Clears throat* I think it's best not to dig too deep into the \"favorite\" subject.",

        # HS 40501
        "I don't really care about the \"best friend\" status anymore, now that [mc] and I are...":
            "I don't really care about the \"favorite\" status anymore, now that [mc] and I are...",

        # HS 40510
        "N-Now that we are {b}SUPER{/b} best friends!":
            "N-Now that I am his {b}SUPER{/b} favorite!",

        # HS 40513
        "Super-duper best friends!":
            "Super-duper favorite!",

        # HS 40514
        "Wait... did [mc] say Chang is his best friend?! And not me?!":
            "Wait... did [mc] say Chang is his favorite?! And not me?!",

        # HS 40587
        "We won’t fail you, Nancy! No stone will be left unturned!":
            "We won’t fail you, Nancy! No stone will be left unturned!",

        # HS 40689
        "B-Bye, [mc]! I'll see you at home!":
            "B-Bye, bro! I'll see you at home!",

        # HS 49310 Disabled, interferes with other lines, also doesn't work if not on other paths
        # "I like where this is going...":
        #    "I like where this is going... and I am too horny to care that she is my sister... as if I had cared with Mom, Dalia, or Annie...",

        # HS 44586 last name override
        "(Penelope Carter... you’re gonna drive me mad.)":
            "(Penelope Carter... you’re gonna drive me mad.)",

        # HS 44763 last name override
        "*Chuckles* Don’t be silly! You're staying with us until we say so. No escaping the Carters!":
            "*Chuckles* Don’t be silly! You're staying with us until we say so. No escaping this family!",

        # HS 45892 last name override
        "Penelope? Penelope Carter? That IG model in the journalism program?":
            "Penelope? Penelope Carter? That IG model in the journalism program?",

        # HS 47861 last name override
        "Actually, yeah! I'm looking for Penelope. Penelope Carter. Do you know her?":
            "Actually, yeah! I'm looking for Penelope. Penelope Carter. Do you know her?",

        # HS 48278 last name override
        "Penelope Carter just said that she'd like to have a threesome with me. It's difficult not to be enthusiastic.":
            "Penelope Carter just said she'd like to have a threesome with her brother. How scandalous!",

        # HS 49359 last name override
        "Not quite yet, Miss Carter...":
            "Not quite yet, Miss Carter...",

        # HS 49442 last name override
        "She's mine... For at least tonight, Penelope Carter is all mine...":
            "She's mine... For at least tonight, Penelope Carter is all mine...",


    # -----------------------------------------
    # v0.6 script6.rpy Lines 52298-66773

        # HS 53976
        "How was your father?":
            "How was Dad?",

        # HS 54302
        "It's just... that... well, I was shocked at first since we had {i}never{/i} seen each other naked, and all that.":
            "It's just... that... well, I was shocked at first since the last time I saw you naked was {i}so long{/i} ago.",

        # HS 54573
        "[mc]...? What are you doing here?!":
            "Bro...? What are you doing here?!",

        # HS 57802
        "Oh, thanks for the reassurance, [mc]! I feel much, much better now!":
            "Oh, thanks for the reassurance, brother! I feel much, much better now!",

        # HS 58268
        "*Knocking on the door* Annie?":
            "*Knocking on the door* Sis?",

        # HS 58331
        "And how was your dad?":
            "And how was Dad?",

        # HS 58333
        "My dad...?":
            "Dad...?",

        # HS 58361
        "So... yeah, you know how my father is.":
            "So... yeah, you know how Dad is. He didn't even tell me to say hello to you...",

        # HS 58363
        "Awh, I'm so sorry, [mc]...":
            "Awh, I'm so sorry, bro...",

        # HS 58385
        "You know dads can be real assholes":
            "You know Dad can be a real asshole",

        # HS 58386
        "You know as well as I do that dads can be real assholes.":
            "You know as well as I do that Dad can be a real asshole.",

        # HS 58388
        "W-Well... it's true that my dad has been working a lot all his life and he's been a bit absent, but... he's always cared about me.":
            "W-Well... it's true that Dad's kind of an asshole, but...",

        # HS 58389 switch to annie's mom for half sis? ~BA
        "And he thinks highly of you!":
            "We still had our grandparents over there!",

        # HS 58391
        "Well... yeah, I guess that's different.":
            "Well... yeah. At least we had some family to care for us.",

        # HS 58392
        "That came out wrong, I'm sorry.":
            "I wish they were able to come over more often.",

        # HS 58394
        "No worries! I know you didn't mean it in a bad way.":
            "I do miss them sometimes.",

        # HS 58697
        "I... I'm n-not sure I'm ready, [mc].":
            "I... I'm n-not sure I'm ready, bro.",

        # HS 58784
        "AAaahh... oh god [mc]... I think I'm gonna... C-CUM...":
            "AAaahh... oh god bro... I think I'm gonna... C-CUM...",

        # HS 58786
        "[mc]! You’re gonna make me...":
            "Bro! You’re gonna make me...",

        # HS 58955 Disabled, does not apply to half route ~BA
        # "The sweet, innocent, little girl I've known for years...":
        #    "The sweet, innocent, little girl I've known my entire life...",

        # HS 58985
        "You better take care of my little girl while you're in the USA, [mc].":
            "You better take care of your sister while you're in the USA, [mc].",

        # HS 58986
        "Rest assured Mr. Winters, I won’t let anything happen to her!":
            "Rest assured Grandpa, I won’t let anything happen to her!",

        # HS 58987
        "I'll take care of Annie as if she was my sister!":
            "I'll take care of Annie!",

        # HS 58998
        "Oh GOD, Annie, I'm gonna fucking cum!":
            "Oh GOD, sis, I'm gonna fucking cum!",

        # HS 59016
        "*Panting* Do it... empty y-yourself all over me, [mc]...":
            "*Panting* Do it... empty y-yourself all over me, bro...",

        # HS 59017
        "Oh god Annie, I'm...":
            "Oh god sis, I'm...",

        # HS 59048
        "Goddammit Annie... that was mind-blowing.":
            "Goddammit sis... that was mind-blowing.",

        # HS 59060
        "Imagine if Nancy had caught us... she'd kick us out of the house!":
            "Imagine if Nancy had caught us... she'd kick us, or at least me, out of the house!",

        # HS 59064
        "Why would she? We weren't doing anything wrong.":
            "...",

        # HS 66449 last name override
        "Although... not as much as when you went to Wyatt's house with Nancy Carter, that's for sure.":
            "Although... not as much as when you went to Wyatt's house with Nancy Carter, that's for sure.",


    # -----------------------------------------
    # v0.7 script7.rpy Lines 66774-80425

        # HS 67679 last name override
        "Penelope Carter plays Eternum!":
            "Penelope Carter plays Eternum!",

        # HS 67805 last name override
        "*Hyperventilating* I left my drawing utensils at the Carter house last time I was there!":
            "*Hyperventilating* I left my drawing utensils at the Carter house last time I was there!",

        # HS 68235
        "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, Annie.":
            "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, sis.",

        # HS 68276
        "Are you sure you don't want to join us, Annie?":
            "Are you sure you don't want to join us, sis?",

        # HS 74792 last name override
        "Penelope Carter is my bestie.":
            "Penelope Carter is my bestie.",

        # HS 74971
        "(How would we even explain this to Mom or Dalia?)":
            "(How would we even explain this to Mom, Dalia, or Annie?)",

        # HS 75113 last name override
        "{sc=2}PENELOPE{w=.5} P. {w=.5}CARTER.{/sc}":
            "{sc=2}PENELOPE{w=.5} P. {w=.5}CARTER.{/sc}",

        # HS 75229 last name override
        "I'm [mc] [lastname] – Penelope Carter's representative.":
            "I'm [mc] [lastname] – Penelope Carter's representative.",

        # HS 75511 last name override
        "P-Penelope Paige Carter.":
            "P-Penelope Paige Carter.",

        # HS 75615 last name override
        "Penelope Paige Carter.":
            "Penelope Paige Carter.",

        # HS 76277 last name override
        "I'm having sex with her. I’m fucking Penelope Carter.":
            "I'm having sex with her. I’m fucking Penelope Carter.",


    # -----------------------------------------
    # v0.8 script8.rpy Lines 80426-97360

        # HS 83896 last name override
        "Was that Penelope Carter?!":
            "Was that Penelope Carter?!",

        # HS 84213 last name override
        "The one and only... PENELOPE CARTER!":
            "The one and only... PENELOPE CARTER!",

        # HS 84407 last name override
        "{cps=16}However...{cps=1.5} {cps=16}the call from Dalia Carter sparked a glimmer of hope within him, so he decided to head to the coffee area and wait for her.{cps=1} {cps=16}This...{cps=1.4} {cps=16}was his chance.":
            "{cps=16}However...{cps=1.5} {cps=16}the call from Dalia Carter sparked a glimmer of hope within him, so he decided to head to the coffee area and wait for her.{cps=1} {cps=16}This...{cps=1.4} {cps=16}was his chance.",

        # HS 84648
        "Come on, [mc], I need you to catch on quickly! We're running out of time.":
            "Come on, bro, I need you to catch on quickly! We're running out of time.",

        # HS 84704
        "There's no time to hesitate, [mc]!":
            "There's no time to hesitate, bro!",

        # HS 88122
        "No one ever thought you were useless, Annie. But after this? D-Damn, even less so.":
            "No one ever thought you were useless, sis. But after this? D-Damn, even less so.",

        # does not use label mod

        # HS 88596
        "I'm not alone, my dad's over there.":
            "I'm not alone, my uncle's over there.",

        # HS 88598
        "He's a businessman. He's doing business calls now.":
            "He is talking to Mom to confirm who we are picking up.",

        # HS 88600 wait shouldn't annie know dad already because of the "business trips"? ~BA
        "We were gonna see the pandas at the zoo, but... he got a call. So I guess we’re not going anymore.":
            "We were looking for my new dad and brother who just moved over here from the USA, but... I think I just found one of them.",

        # HS 88603
        "I like your... h-hair, American boy.":
            "I like your... h-hair, brother.",

        # HS 88690
        "Yeah, I should go before my dad gets mad too.":
            "We should wait out here for Dad then.",

        # HS 88691
        "Will you... will you be at school tomorrow?":
            "Nice to... Nice to meet you, brother. Will you be at school tomorrow?",

        # HS 88705
        "Promise me we'll be friends!":
            "Promise me I'll always be your favorite!",

        # HS 88709
        "Friends.":
            "Favorite.",

        # HS 88710
        "Friends forever!":
            "Favorite forever!",

        # HS 88713
        "I'll leave now!":
            "I'll go tell uncle I found you!",

        # HS 88714
        "See you tomorrow... [mc]!":
            "Wait here!",

        # HS 88844
        "And where was I going that day with my dad?":
            "And what where we waiting for?",

        # Editor note: With and without walkthrough mod should both be supported (I'm not sure I never checked without walkthrough mod)
        # l9453394 note: Changed to be fully compatible with and without either walkthrough
        # HS 88850
        "To see the pandas at the zoo":
            "{color=[walk_points]}For Dad to finish the registration [annie_pts]",

        # HS 88851
        "To see the pandas at the zoo.":
            "For Dad to finish the registration.",

        # HS 88852
        "Although... you had to cancel those plans.":
            "You bugged your uncle over and over until Dad was done.",

        # HS 88923
        "D-Darn it, [mc].":
            "D-Darn it, bro.",

        # HS 89043
        "Your answer could shape how the rest of tonight goes and... maybe even your relationship with Annie.":
            "Your answer could shape how the rest of tonight goes and... maybe even your relationship with your sister.",

        # HS 89271
        "I'm so impressed, Annie.":
            "I'm so impressed, sis.",

        # HS 89581
        "The way you’re tracing your finger on my chest is kind of turning me on more than it should, Annie...":
            "The way you’re tracing your finger on my chest is kind of turning me on more than it should, sis...",

        # HS 89626
        "After so many years thinking I’d never be more than friends with Annie... it's finally happening.":
            "After so many years thinking we’d never be more than siblings... it's finally happening.",

        # HS 89651
        "Phew... you sure know how to drive me crazy, Annie.":
            "Phew... you sure know how to drive me crazy, sis.",

        # HS 89739
        "*Moans* Ohh mmmm-y-yes, [mc]...":
            "*Moans* Ohh mmmm-y-yes, bro...",

        # HS 89808
        "*Tracing Annie's figure* Oh, babe...":
            "*Tracing Annie's figure* Oh, sis...",

        # HS 89941
        "*Panting* Ohh, [mc]...":
            "*Panting* Ohh, bro...",

        # HS 89966
        "Oh, trust me, you've seen nothing yet, my love...":
            "Oh, trust me, you've seen nothing yet, sis...",

        # HS 90495
        "B-But I've liked you since the day I met you!":
            "B-But I've liked you since the first day!",

        # HS 93863
        "You think Nancy wants to play the role of some sort of intermediary? Because she wants it too?":
            "\"Mom\" huh? Kinky. So, you think \"Mom\" wants to play the role of some sort of intermediary? Because she wants it too?",

        # HS 93865
        "Exactly! That's what she implied.":
            "It's not... never mind. But yes, that's exactly what she implied.",


    # -----------------------------------------
    # v0.9 script9.rpy Lines 97361-118348

        # HS 97913
        "Luckily, I don't have any more sisters he can be with at the moment.":
            "Luckily, I only have one more half sister who would never be with her brother.",

        # HS 100365
        "Our...":
            "My...",

        # HS 100366
        "Our friend disappeared.":
            "My brother disappeared.",

        # HS 100371
        "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit some family for a few days!":
            "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit your family for a few days!",

        # HS 100373
        "His only family is a drunk skunk of a father living an ocean away.":
            "His only other family is a drunk skunk of a father living an ocean away.",

        # HS 107843 last name override
        "*Starts reading* {i}Dear Ms. Carter, thank you for booking my humble property for this year’s Christmas Eve.":
            "*Starts reading* {i}Dear Ms. Carter, thank you for booking my humble property for this year’s Christmas Eve.",

        # HS 108051 phone chat (annie_chat3)
        # change to mom? ~BA
        "But I really gotta go now or my dad will get mad {image=images/MENUS/e_tongue2.png}":
            "But I really gotta go now or grandpa will get mad",

        # HS 110413 last name override
        "*Chuckles* (Penelope Paige Carter...)":
            "*Chuckles* (Penelope Paige Carter...)",

        # HS 114274 last name override
        "Dalia Carter apologizing? This truly is a Christmas miracle.":
            "Dalia Carter apologizing? This truly is a Christmas miracle.",
    }

    annie_aunt_map = {

        # -----------------------------------------
        # Nancy as aunt (mother's sister), Penelope and Dalia as cousins
        # Combined with Annie as stepsister in annie_aunt_map
        # No name changes
        # Original map
        # (Probably) incompatible with other maps
        # -----------------------------------------
        # Nancy aunt/Penelope & Dalia cousin character notes
        # 
        # - Nancy: MC used to call her "Auntie Nancy" as a kid. She only sees him as an irresistible young man. The mother-son incest roleplay is only there to make it hotter for her, despite the fact that it's genuinely blood-related incest either way. She's the horniest character (other than MC) and embraces her desires the earliest.
        # - Penelope: Use diminutive nickname "little cousin/little cuz/cuz/(rarely) cuzzy" for MC when Penelope is confidently joking/flirting or asserting herself. She has the strongest/clearest boundaries, and knows what she wants. After she starts becoming submissive to MC, make it a pet name. Don't go overboard with the nickname, though. It should just add a little "older sister" kick to flirty lines.
        # - Dalia: They're the same age, so never use diminutive nicknames. They should be just like childhood friends reuniting. Before she realizes it, she develops a crush on MC, and she doesn't pull very hard against it. Neither does MC. This path is much more innocent than Annie, despite the fact that it's (legally) more incestuous than Annie. It also has the fewest edits by far.
        # -----------------------------------------
        # AU = Nancy aunt/Penelope & Dalia cousin lines in annie_aunt_map
        # game/script.rpy:0000 = path/file name:line number
        # (menu) = Choice menu line
        # (chat) = Phone chat line
        # (n) = Nancy line
        # (p) = Penelope line
        # (d) = Dalia line
        # (a) = Annie line
        # (other) = Other line (Any/all main)
        # (misc) = Miscellaneous line (Extras/side characters)
        # These tags aren't based on who's speaking, but who the line and scene are about.
        # ED/N = Editor's notes
        # -----------------------------------------


    # -----------------------------------------
    # 0.1 game/script.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU game/script.rpy:1085 (other)
        "(Nancy used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(Nancy is my aunt on my mother's side. She used to look after me in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)",

        # AU game/script.rpy:1086 (other)
        "(I used to spend the entire afternoon playing with Nancy and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend the entire afternoon playing with Auntie Nancy and my cousin Dalia, but then we had to move and ended up losing touch.)",

        # AU game/script.rpy:1089 (other)
        "(Come to find out, she actually had 2 rooms available, so Annie will have a place to stay as well!)":
            "(When she heard Annie was coming, she offered us a second room, so I can finally introduce her to my family back in Kredon!)",

        # AU game/script.rpy:1098 (other)
        "I know, but I can't help feeling a little bit nervous.":
            "I know, but I can't help feeling a little bit nervous to meet your family.",

        # AU game/script.rpy:1711 (n)
        "How could I forget you?":
            "How could I forget my Auntie Nancy?",

        # AU game/script.rpy:1749 (n)
        "You clearly need a strong female influence in your life. Seems like I have my work cut out for me, young man!":
            "You clearly need a strong female influence in your life. Seems like your aunt has her work cut out for her, young man!",

        # AU game/script.rpy:1767 (n)
        "It’s me, Nancy! Even though we’ve only been speaking on the phone for the past few days, I feel like we’ve been becoming good friends already! Isn't that right, Annie?":
            "It’s me, Nancy! Even though we’ve only been speaking on the phone for the past few days, I feel like we’re becoming family already! Isn't that right, Annie?",

        # AU game/script.rpy:1786 (n)
        "And of his babysitter!":
            "And of his aunt!",

        # AU game/script.rpy:1790 (n)
        "Yeah, since my Dad was constantly working, I've always said you were like a parent to me.":
            "Yeah, since my Dad was constantly working, I've always said you were like a mother to me.",

        # AU game/script.rpy:1793 (n)
        "Now I work in a laboratory, but back then I was still finishing my thesis. Thankfully [mc]'s father came along and offered me the babysitting gig.":
            "Now I work in a laboratory, but back then I was still finishing my thesis. Thankfully [mc]'s father came to me and offered me a babysitting gig taking care of [mc] while he was at work.",

        # AU game/script.rpy:1794 (n)
        "It was not only well-paid, but also allowed me the flexibility to take care of my daughters at the same time. And for me, being a single mother, that was essential.":
            "It was not only well-paid, but also allowed me the flexibility to take care of my daughters at the same time. And for both of us, being a single mother and a single father, that was essential.",

        # AU game/script.rpy:1798 (n)
        "Yes, Dalia and Penelope. Penny was a little older when I was [mc]'s nanny, so she used to play on her own, but Dalia got very close to him!":
            "Yes, Dalia and Penelope. Penny is a little older than [mc], so she used to play on her own, but Dalia got very close to him! They were like twins.",

        # AU game/script.rpy:1811 (n)
        "(I guess you don't notice that stuff when you're 8 years old...)":
            "(I guess you don't notice stuff like that about your aunt when you're 8 years old...)",

        # AU game/script.rpy:1916 (n)
        "I wasn't expecting you to be so excited to meet [mc] again!":
            "I wasn't expecting you to be so excited to meet your cousin again!",

        # AU game/script.rpy:1931 (p)
        "Oh... O-Of course! [mc]!":
            "Oh... O-Of course! Little [mc]!",

        # AU game/script.rpy:2395 (n)
        "It's like we're family now. I’m not bothered by you at all!":
            "It's like we're family again. I’m not bothered by you at all!",

        # AU game/script.rpy:2430 (n)
        "(Jesus, look at me. Fantasizing about the dick of the kid I used to care for.)":
            "(Jesus, look at me. Fantasizing about the dick of the kid I used to raise like my own son.)",

        # AU game/script.rpy:2431 (n)
        "(You're 20 years older than he is, Nancy, for fuck's sake.)":
            "(You're his aunt, Nancy, for fuck's sake.)",

        # AU game/script.rpy:2585 (other)
        "(I mean, I know they’re pretty much like family, so I don't mean it that way, but...)":
            "(I mean, I know they’re my family, so I don't mean it that way, but...)",

        # AU game/script.rpy:2657 (p)
        "Is that supposed to be a joke?":
            "Is that supposed to be a joke? You're my cousin.",

        # AU game/script.rpy:2678 (p)
        "Thanks, [mc].":
            "Thanks, little cousin.",

        # AU game/script.rpy:2697 (p)
        "Oh, I'm sorry I bored you, sir.":
            "Oh, I'm sorry I bored you, little cousin.",

        # AU game/script.rpy:3425 (d)
        "(It's just Dalia. You two grew up together! She's practically your sister...)":
            "(It's just Dalia. You two grew up together! She's literally your cousin...)",

        # AU game/script.rpy:3442 (d)
        "Dalia, the girl you live with?":
            "Dalia, your cousin?",

        # AU game/script.rpy:3591 (n)
        "And there's nothing like being on chore duty to strengthen a household bond!":
            "And there's nothing like being on chore duty to strengthen a family bond!",

        # AU game/script.rpy:3668 (p)
        "*Imitating Penelope's voice* {i}Wow, [mc]!":
            "*Imitating Penelope's voice* {i}Wow, little cuz!",

        # AU game/script.rpy:3828 (d)
        "(And that's... wrong! Bad [mc]! Get a hold of yourself.)":
            "(And that's... wrong! Bad [mc]! She is your cousin! Get a hold of yourself.)",

        # AU game/script.rpy:4041 (p)
        "Alright [mc], you convinced me!":
            "Alright little cuz, you convinced me!",

        # AU game/script.rpy:4844 (p)
        "Well, I definitely do not share that opinion at all.":
            "Well, I definitely do not share that opinion. You're my family, Penny.",

        # AU game/script.rpy:4846 (p)
        "Thanks for trusting me, [mc]. It means a lot.":
            "Thanks for trusting me, little cuz. It means a lot.",

        # AU game/script.rpy:5479 (p)
        "(Looking at hot pics of Penelope, yeah, great idea, [mc]. Way to not have even more fantasies of all these girls around me...)":
            "(Looking at hot pics of Penelope, yeah, great idea, [mc]. Way to not have even more fantasies of all the girls in my family...)",

        # AU game/script.rpy:5541 (n)
        "(Who would’ve known he was hiding such a monster...)":
            "(Who would’ve known my nephew was hiding such a monster...)",

        # AU game/script.rpy:5559 (n)
        "(Oh Jesus, one man comes into my house and suddenly I turn into a nymphomaniac. What the hell is wrong with me?)":
            "(Oh Jesus, one man comes into my house and suddenly I turn into a nymphomaniac. What the hell is wrong with me? He's my family!)",

        # AU game/script.rpy:5583 (n)
        "(I mean... If Dalia and Penelope never found out, then would it really be so bad? It’d be our little secret...)":
            "(I mean... If the girls never found out, then would it really be so bad? It’d be our little secret... my big boy...)",

        # AU game/script.rpy:6045 (d)
        "You said you were Dalia's friend?":
            "You said you were Dalia's cousin?",

        # AU game/script.rpy:6047 (d)
        "Yeah, we’ve known each other since we were little.":
            "Yeah, I used to stay at her house all the time when we were little.",

        # AU game/script.rpy:8503 (p)
        "Thanks for supporting me, I appreciate it.":
            "Thanks for supporting me, little cuz. I appreciate it.",

        # AU game/script.rpy:8552 (n)
        "(You're not a horny teenager. Show her you're a man now.)":
            "(You're not a horny teenager. Show her you're a man now. She's just your aunt.)",


    # -----------------------------------------
    # 0.2 game/script2.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU game/script2.rpy:4574 (n)
        "*Laughs* It's not that. [mc] is staying with us for a year until he finishes school. He’s part of the student exchange program.":
            "*Laughs* It's not that. [mc] is my nephew. He's staying with us for a year until he finishes school as part of the student exchange program.",

        # AU game/script2.rpy:4840 (n)
        "What? I'm not Dalia. My name is [mc].":
            "What? I'm not Dalia. My name is [mc]. Dalia is my cousin.",

        # AU game/script2.rpy:4910 (n)
        "No, I came with Nancy.":
            "No, I came with Nancy. I'm her nephew.",

        # AU game/script2.rpy:4912 (n)
        "Oh, really? You two know each other? Well I’m glad to meet you, because I’m positive you’re going to be seeing a lot more of me soon...":
            "Oh, really? You two are related? Well I'm glad to meet you, because I'm positive you're going to be seeing a lot more of me soon...",

        # AU game/script2.rpy:4977 (n)
        "(Or can I? I mean... Why am I so jealous in the first place? It's not like anything could happen between Nancy and I anyways...)":
            "(Or can I? I mean... Why am I so jealous in the first place? It's not like anything could happen between Nancy and I anyways. She's my aunt...)",

        # AU game/script2.rpy:5014 (n)
        "Y-Yeah, I know Nancy very well, and honestly she’s been in quite a heightened emotional state lately. I can’t bear the thought of that guy taking advantage of her.":
            "Y-Yeah, Nancy's my aunt, and honestly she’s been in quite a heightened emotional state lately. I can’t bear the thought of that guy taking advantage of her.",

        # AU game/script2.rpy:5199 (n)
        "*Giggles* Just like when I was your babysitter.":
            "*Giggles* Just like when you were a kid.",

        # AU game/script2.rpy:5294 (n)
        "I can't be with him. It would be... weird. We’re not supposed to be together... like {i}that{/i}.":
            "I can't be with him. It would be... wrong. We’re not supposed to be together... like {i}that{/i}.",

        # AU game/script2.rpy:5321 (n)
        "*Giggles* Um, maybe. No... But, I mean... could you imagine?!":
            "*Giggles* Um, maybe. No, that would be so wrong... But, I mean... could you imagine?!",

        # AU game/script2.rpy:5363 (n)
        "(I can't just barge in and be like, \"Hi [mc], did you know you make me feel so horny all the time? Do you wanna fuck your old babysitter?\")":
            "(I can't just barge in and be like, \"Hi [mc], did you know you make me feel so horny all the time? Do you wanna fuck your old aunt?\")",

        # AU game/script2.rpy:5364 (n)
        "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out.)":
            "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out... {w}And fucking my nephew, is that even legal?)",

        # AU game/script2.rpy:7088 (p)
        "Is that a hint of jealousy, I’m sensing?":
            "Is that a hint of jealousy I’m sensing, little cousin?",

        # AU game/script2.rpy:7117 (p)
        "(I mean... not that I care... or even had any chance, but still...)":
            "(I mean... not that I should care... or even had any chance, but still...)",

        # AU game/script2.rpy:7128 (p)
        "(It's not like I was expecting her to wait for me like a nun, but... just imagining some guy banging her... ugh.)":
            "(It's not like I was expecting her to keep her chastity like a nun, but... just imagining some guy banging her... ugh.)",

        # AU game/script2.rpy:7134 (p)
        "(Way out of your league.)":
            "(Way out of your league, and also, your cousin.)",

        # AU game/script2.rpy:7156 (p)
        "Ahhh... yeah, that’s right. [mc]...":
            "Ahhh... yeah, that’s right. Your cousin, [mc]...",

        # AU game/script2.rpy:7306 (p)
        "Someone is a good listener... thank you for remembering!":
            "My little cousin is a good listener... thank you for remembering!",

        # AU game/script2.rpy:7334 (p)
        "(Wake up [mc], we're talking about Penelope here. Still not gonna happen.)":
            "(Wake up [mc], we're talking about your cousin Penelope here. Still not gonna happen.)",

        # AU game/script2.rpy:7404 (p)
        "But that’s why I’m glad to have you here, [mc].":
            "But that’s why I’m glad to have you here, little cuz.",

        # AU game/script2.rpy:7534 (p)
        "I might need you to be my photographer more often, [mc]!":
            "I might need you to be my photographer more often, little cuz!",

        # AU game/script2.rpy:7679 (p)
        "Well, you sure do know how to push a button, [mc].":
            "Well, you sure do know how to push a button, cuz!",

        # AU game/script2.rpy:7705 (p)
        "I don't mind you seeing me like this, because... I don't know, I just feel comfortable around you.":
            "I don't mind you seeing me like this... You're my little cousin, I feel comfortable around you.",

        # AU game/script2.rpy:7819 (p)
        "Come on, you know you can trust me. I wouldn’t do you wrong.":
            "Come on, cuz, you know you can trust me. I wouldn’t do you wrong.",

        # AU game/script2.rpy:7961 (p)
        "You know... this whole thing got me thinking...":
            "You know, little cuz... this whole thing got me thinking...",

        # AU game/script2.rpy:7973 (p)
        "That Valentino guy made me realize that I'll never feel comfortable doing something like this with a stranger. But you’re no stranger, [mc], and since I have you here...":
            "That Valentino guy made me realize that I'll never feel comfortable doing something like this with a stranger. But you’re family, [mc], and since I have you here...",

        # AU game/script2.rpy:7992 (p)
        "(Oh my god, am I about to see Penelope naked?)":
            "(Oh my god, am I about to see my cousin naked?)",

        # AU game/script2.rpy:8076 (p)
        "Oh don’t be like that! It'll be fun!":
            "Oh don’t be like that, cuz! It'll be fun!",

        # AU game/script2.rpy:8115 (p)
        "Oh, come on, [mc]!":
            "Oh, come on, little cuz!",

        # AU game/script2.rpy:8140 (p)
        "(Is this huge thing I’m feeling... his...)":
            "(Is this huge thing I’m feeling... my little cousin's...)",

        # AU game/script2.rpy:8198 (p)
        "I don't know what it is about you, but... I always have so much fun when you’re around.":
            "I don't know what it is about you, little cuz, but... I always have so much fun when you’re around.",

        # AU game/script2.rpy:8315 (p)
        "I was wondering why Nancy and her shared the same last name on your followers list. Nancy is her mom!":
            "I was wondering why Nancy and her shared the same last name on your followers list. She must be your cousin!",

        # AU game/script2.rpy:8409 (p)
        "(I’ve never been good at taking a hint.)":
            "(She's always been like a big sister to me.)",

        # AU game/script2.rpy:8420 (p)
        "And now I’ve come to learn that you’re friends with Penelope too?!":
            "And now I’ve come to learn that you’re cousins with Penelope too?!",

        # AU game/script2.rpy:8624 (p)
        "Have fun playing.":
            "Have fun playing, little cuz.",


    # -----------------------------------------
    # 0.3 game/script3.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU game/script3.rpy:1248 (misc)
        "We will not leave until every lustful desire of yours is satisfied. Use us as your personal toys, as we surrender ourselves to every inch of you... or lay back and let us take the lead... and do all of the work.":
            "We will not leave until every lustful desire of yours is satisfied. Use us sisters as your personal toys, as we surrender ourselves to every inch of you... or lay back and let us take the lead... and do all of the work.",

        # AU game/script3.rpy:2803 (d)
        "Nah... I don’t need to sleep out here. I tricked a Kredon family into letting me live in their house for a whole year. They set me up with a bed to sleep in, too, so no park benches for me!":
            "Nah... I don’t need to sleep out here. I tricked some relatives in Kredon into letting me live in their house for a whole year. They set me up with a bed to sleep in, too, so no park benches for me!",

        # AU game/script3.rpy:2808 (d)
        "Especially the youngest daughter. She's extremely naive and easily manipulated.":
            "Especially my youngest cousin. She's extremely naive and easily manipulated.",

        # AU game/script3.rpy:2912 (d)
        "Don't worry, I’m not going to waste time on your whore anymore.":
            "Don't worry, I’m not going to waste time on your whore cousin anymore.",

        # AU game/script3.rpy:3941 (p)
        "Penelope and I know each other from college, [mc].":
            "Penelope and I know each other from college, [mc]. I don't know why you never told me you were her cousin!",

        # AU game/script3.rpy:4615 (p)
        "And this here is Penelope, and next to her...":
            "And this here is my cousin Penelope, and next to her...",

        # AU game/script3.rpy:4852 (n)
        "If Nancy asks, I ate it all!":
            "If Auntie Nancy asks, I ate it all!",

        # AU game/script3.rpy:4916 (n)
        "(This nanny gig just isn't enough to pay the bills, and between paying the girls’ tuition and the mortgage...)":
            "(This nanny gig with [mc] just isn't enough to pay the bills, and between paying the girls’ tuition and the mortgage...)",

        # AU game/script3.rpy:4919 (n)
        "([mc]'s father is already generously paying me more than he should for taking care of his son. But even with that extra money, it’s only delaying the inevitable.)":
            "([mc]'s father is already generously paying me more than he should for taking care of his son. I don't know what we'd do without his support. But even with that extra money, it’s only delaying the inevitable.)",

        # AU game/script3.rpy:5200 (p)
        "Has [mc] finished his dinner?":
            "Has little [mc] finished his dinner?",

        # AU game/script3.rpy:5234 (p)
        "I can see the mud stains from here, mister!":
            "I can see the mud stains from here, little cousin!",

        # AU game/script3.rpy:5286 (p)
        "*Giggles* That's a bold move!":
            "*Giggles* That's a bold move, little cuz!",

        # AU game/script3.rpy:5970 (p)
        "We're just friends. I've only seen her half-naked once... during a photoshoot.":
            "She's my cousin. I've only seen her half-naked once... during a photoshoot.",

        # AU game/script3.rpy:5991 (p)
        "So tell me... don't you wanna see a bit more? If I had a \"friend\" who looked like this, I’d be dying to find out what’s underneath all those clothes...":
            "So tell me... don't you wanna see a bit more? If I had a cousin who looked like this, I’d be secretly dying to find out what’s underneath all those clothes...",

        # AU game/script3.rpy:6005 (p)
        "She's perfect...":
            "She's... my cousin is... perfect...",

        # AU game/script3.rpy:6044 (p)
        "Or if you prefer, you can feel this huge, gorgeous ass right here...":
            "Or if you prefer, you can feel your cousin's huge, gorgeous ass right here...",

        # AU game/script3.rpy:6291 (p)
        "Sometimes I forget I'm friends with a celebrity.":
            "Sometimes I forget I'm related to a celebrity.",

        # AU game/script3.rpy:6296 (p)
        "That makes me very uncomfortable, to be honest. I’m gonna need a little more fanfare from you, [mc].":
            "That makes me very uncomfortable, to be honest. I’m gonna need a little more fanfare from you, little cousin.",

        # AU game/script3.rpy:6316 (p)
        "I couldn't care less about your social network pages or how many followers you have... I only care about the person behind it. You became a special person to me just because of who you are.":
            "I couldn't care less about your social network pages or how many followers you have... I only care about the person behind it. You're my one and only big cousin, and you always looked after me. You're special to me just because of the person you are.",

        # AU game/script3.rpy:6374 (p)
        "Nice to meet you. I’m [mc], and this is Penelope and Luna.":
            "Nice to meet you. I’m [mc], and this is Luna and my cousin Penelope.",

        # AU game/script3.rpy:6564 (p)
        "A friend!":
            "Someone I like!",

        # AU game/script3.rpy:6583 (p)
        "(That's too bad...)":
            "(Well yeah, she's my cousin...)",

        # AU game/script3.rpy:6646 (p)
        "Your BDSM-lover friend said you’ve all been to the Emporium already, right?":
            "Your BDSM-lover cousin said you’ve all been to the Emporium already, right?",

        # AU game/script3.rpy:6984 (p)
        "[mc]... can I confess something to you...? ":
            "Little cousin... can I confess something to you...? ",

        # AU game/script3.rpy:6991 (p)
        "Are you gonna fuck me, daddy?":
            "Are you gonna fuck me, little cuz?",

        # AU game/script3.rpy:7664 (p)
        "These are my friends, Penelope and Luna.":
            "This is my cousin, Penelope, and my friend Luna.",

        # AU game/script3.rpy:7688 (misc)
        "She's my cousin. Totally loves to roleplay as an elf.":
            "She's my... second cousin. Totally loves to roleplay as an elf.",

        # AU game/script3.rpy:7907 (p)
        "Don't worry [mc], I'm in good hands!":
            "Don't worry little cuz, I'm in good hands!",

        # AU game/script3.rpy:8172 (d)
        "Actually, I am! I'm looking for a friend of mine. She’s the one who invited me to the server.":
            "Actually, I am! I'm looking for my cousin. She’s the one who invited me to the server.",

        # AU game/script3.rpy:8330 (d)
        "I was just looking for her! Her name is Dalia.":
            "I was just looking for her! Her name is Dalia. She's my cousin.",

        # AU game/script3.rpy:8780 (d)
        "S-Seriously? You're a fucking pig!":
            "S-Seriously? You're a fucking pig! We're cousins!",

        # AU game/script3.rpy:8790 (d)
        "Oh damn, so you'd do all that too?!":
            "Oh, so it's fine to do all that with your cousin?!",

        # AU game/script3.rpy:9576 (n)
        "*Laughs* Oh, don’t you dare! You’re too much!":
            "*Laughs* Oh, don’t you dare! You’re my nephew, so that makes you a Prince too!",

        # AU game/script3.rpy:9585 (n)
        "Well, enough about her. I want to hear more from my esteemed Champion. Did you know this Royal Bathhouse is open only to the Emperor and the Emperor’s special guests?":
            "Well, enough about her. I want to hear more from my noble Prince. Did you know this Royal Bathhouse is open only to chosen members of the imperial family and the Emperor’s special guests?",

        # AU game/script3.rpy:9587 (n)
        "I had no idea! I feel so honored now. Does that make me your special guest?":
            "I had no idea! I feel so honored now. Does that make me your chosen family, or your special guest?",

        # AU game/script3.rpy:9588 (n)
        "Indeed... I don’t see anyone else around here...":
            "Well... No one said you couldn’t be both...",

        # AU game/script3.rpy:9648 (n)
        "You, my Champion. Will you be joining me, or do you have to get going?":
            "You, my Prince. Will you be joining me, or do you have to get going?",

        # AU game/script3.rpy:9663 (n)
        "(Keep it together! She’s been like a mother to you. Focus, [mc]! This is strictly a bath!)":
            "(Keep it together! She’s your aunt, and she's like a mother to you. Focus, [mc]! This is strictly a bath!)",

        # AU game/script3.rpy:9694 (n)
        "And I saw you! Back when you were my babysitter. I was too young to remember most of that time, but you looked exactly like you did in our old pictures!":
            "And I saw you! Back when you took care of me. I was too young to remember most of that time, but you looked exactly like you did in our old family pictures!",

        # AU game/script3.rpy:9706 (n)
        "I owe it to my mother. It seems like once she reached 25, she stopped aging. She died shortly after Dalia was born, but she was always so full of life.":
            "I owe it to your grandmother. It seems like once she reached 25, she stopped aging. She died shortly after you and Dalia were born, but she was always so full of life.",

        # AU game/script3.rpy:9714 (n)
        "Girlfriend. No doubt about it at all.":
            "Girlfriend. No doubt about it at all. No one would believe me if I said you're my aunt.",

        # AU game/script3.rpy:9736 (n)
        "I see... my young [mc] has a little experience under his belt. Very interesting...":
            "I see... my young nephew has a little experience under his belt. Very interesting...",

        # AU game/script3.rpy:9768 (n)
        "I mean... I'd never dare.":
            "I mean... th-they're my cousins. I'd never dare.",

        # AU game/script3.rpy:9770 (n)
        "Why not? I wouldn’t mind having you as my son-in-law...":
            "Just forget about that for a moment, [mc]. I know it’s taboo, but I... wouldn’t mind having you as my son-in-law...",

        # AU game/script3.rpy:9780 (n)
        "I'd be lying if I said that doesn’t sound like a dream come true.":
            "I know it would be incest, but... I'd be lying if I said that doesn’t sound like a dream come true.",

        # AU game/script3.rpy:9791 (n)
        "*Chuckles* Is someone hinting that I might be good enough...?":
            "*Chuckles* Aren't you forgetting something important...?",

        # AU game/script3.rpy:9793 (n)
        "*Giggles* I'm not sure yet. You definitely have most of the desirable qualities in a man, but still... there’s some areas of you I don’t know much about.":
            "*Giggles* You're their family, [mc]. I’ve watched you grow up together, and I know you’d treat them right. You definitely have most of the desirable qualities in a man, but still... there’s some areas of you I don’t know much about.",

        # AU game/script3.rpy:9802 (n)
        "I couldn't. I don't know... I just see them as family.":
            "I couldn't. I don't know... they're my family.",

        # AU game/script3.rpy:9804 (n)
        "Ah, I see. I guess it does make sense.":
            "Ah, I see. I guess you're probably right.",

        # AU game/script3.rpy:9820 (n)
        "Your energy is infectious. Your charm is invigorating. When I’m with you, I feel like I can take on the world. And then you awaken so many other feelings within me that I thought were long gone...":
            "Your energy is infectious. Your charm is invigorating. When I’m with you, I feel like I can take on the world. And then you awaken so many other feelings within me that I thought were long gone... feelings that I know I shouldn’t have...",

        # AU game/script3.rpy:9822 (n)
        "Wow... I had no idea, Nancy.":
            "Wow, I... I had no idea, Nancy.",

        # AU game/script3.rpy:9827 (n)
        "No, really Nancy... it honestly feels so nice to hear that coming from you. I consider you to be someone very important in my life, so it’s truly appreciated.":
            "No, really Nancy... it honestly feels so nice to hear that coming from you. You're my family and one of the most important women in my life, so it’s truly appreciated.",

        # AU game/script3.rpy:9832 (n)
        "*Chuckles* Very much. I’m honored to be your special guest... and feel so privileged to witness such a rare and honestly breathtaking sight.":
            "*Chuckles* Very much. I’m honored to be your chosen family and special guest... and feel so privileged to witness such a rare and honestly breathtaking sight.",

        # AU game/script3.rpy:9842 (n)
        "Hmph. I invite a commoner to my private baths and he can’t even contain himself. What a shame.":
            "Hmph. I invite my own nephew to our private baths and he can’t even contain himself. What a shame.",

        # AU game/script3.rpy:9865 (n)
        "(I’d hate myself if I didn’t at least try...)":
            "(She’s irresistible... even if it’s wrong, I can’t deny it...)",

        # AU game/script3.rpy:9900 (n)
        "(I can tell she was looking forward to this.)":
            "(I can tell she was looking forward to this... my Auntie Nancy...)",

        # AU game/script3.rpy:9942 (n)
        "Does the Champion truly want to serve his Empress?":
            "Does the Prince truly wish to serve his Empress?",

        # AU game/script3.rpy:9946 (n)
        "You know... I remember from my history classes that it was always taboo for royalty to intermingle with common folk...":
            "You know... I remember from my history classes that it was common for royal families to \"intermingle\" with one another...",

        # AU game/script3.rpy:9947 (n)
        "But I think we’ve broken enough rules today...":
            "As they say... {i}\"When in Rome, do as the Romans do...\"{/i}",

        # AU game/script3.rpy:9949 (n)
        "I need to feel my Champion... taste the forbidden fruit...":
            "I need to feel my Prince... taste the forbidden fruit...",

        # AU game/script3.rpy:9970 (n)
        "Oh, my C-Champion feels...":
            "Oh, my P-Prince feels...",

        # AU game/script3.rpy:9971 (n)
        "Oh, s-screw the Champion shit...":
            "Oh, s-screw the Prince shit...",

        # AU game/script3.rpy:10096 (n)
        "I've wanted you to fuck me ever since I first saw you in that park. I thought maybe it was just a fleeting urge and it’d pass quickly... but no...":
            "I've wanted you to fuck me ever since I first saw you in that park. I thought maybe it was just a forbidden urge and it’d pass quickly... but no...",

        # AU game/script3.rpy:10106 (n)
        "This time though... I want you to lie back and let your babysitter do all the work...":
            "This time though... I want you to lie back and let your Auntie Nancy do all the work...",

        # AU game/script3.rpy:10133 (n)
        "*Whispering* What for? It’s only a guard!":
            "*Whispering* What for? It’s only a guard! They don't know we're related.",

        # AU game/script3.rpy:10137 (n)
        "*Whispering* Oh, that's a good point.":
            "*Whispering* Oh, shit... I told Maximo earlier that Dalia was my cousin.",

        # AU game/script3.rpy:10177 (n)
        "(Why does God hate me?)":
            "(Why does God hate me? Is this divine punishment?)",

        # AU game/script3.rpy:10213 (n)
        "(Man, I was so damn close to fucking Nancy...!)":
            "(Man, I was so damn close to fucking Nancy...! It's so... wrong...)",

        # AU game/script3.rpy:10221 (n)
        "(Little do they know... heh.)":
            "(I hope I can still look them in the face after this...)",


    # -----------------------------------------
    # 0.4 game/script4.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU game/script4.rpy:2275 (n)
        "I'm not Nancy's daughter. I mean, I'm not even a girl! Do I have to spell it out or what?":
            "I'm not Nancy's daughter, I'm her nephew. I mean, I'm not even a girl! Do I have to spell it out or what?",

        # AU game/script4.rpy:2281 (n)
        "(With so many people living under the same roof, it'll be hard to find some time alone.)":
            "(With all our family living under the same roof, it'll be hard to find some time alone.)",

        # AU game/script4.rpy:2425 (d)
        "Thanks buddy. You're a good friend.":
            "Thanks cuz. You're a good friend.",

        # AU game/script4.rpy:3031 (d)
        "I didn't know you were dating!":
            "I didn't know you were dating! Wait, aren't you two cousins?",

        # AU game/script4.rpy:3043 (d)
        "Why didn't you tell me, [mc]?!":
            "Hold on, you two aren't actually cousins?! Is she adopted?! Why didn't you tell me, [mc]?!",

        # AU game/script4.rpy:3049 (d)
        "We're not dating!":
            "W-What? No! We're not {i}dating!",

        # AU game/script4.rpy:3050 (d)
        "We're just old friends!":
            "We're just cousins!",

        # AU game/script4.rpy:3056 (d)
        "It doesn't mean anything!":
            "It doesn't mean anything! A-And I heard that in Europe, cousins kiss each other all the time!!",

        # AU game/script4.rpy:3145 (d)
        "I'm the lame one? Go tell that to that crybaby girlfriend of yours.":
            "I'm the lame one? Go tell that to that crybaby cousin of yours.",

        # AU game/script4.rpy:3688 (d)
        "I know you already saw me naked, but I hope this can still get you in the mood." :
            "I know you already saw me naked, but I hope this can still get you in the mood. I trust that us being cousins won't be an issue for little [mc].",

        # AU game/script4.rpy:3690 (d)
        "Well... I hope this is enough to get you in the mood.":
            "Well... I hope this is enough to get you in the mood. I trust that us being cousins won't be an issue for little [mc].",

        # AU game/script4.rpy:3977 (d)
        "Well, well, well... so you openly admit having fantasized about how my cum tastes, huh...?":
            "Well, well, well... so you openly admit having fantasized about how your cousin's cum tastes, huh...?",

        # AU game/script4.rpy:4192 game/chat.rpy:950 (chat) (p)
        "Thanks [mc]  {image=images/MENUS/e_heart.png}":
            "Thanks little cuz  {image=images/MENUS/e_heart.png}",

        # AU game/script4.rpy:5113 (other)
        "Nancy, Penelope, and Dalia are all very nice to me. They treat me as one of the family. You know I’ve always wanted sisters, so I really feel like they’re giving me that experience!":
            "Nancy, Penelope, and Dalia are all very nice to me. They treat me as part of your family. You know I’ve always wanted sisters, so I really feel like they’re giving me that experience!",

        # AU game/script4.rpy:7330 (p)
        "Thanks! You’re a sweetheart. I've been practicing with Luna these past few days. I can't stop playing!":
            "Thanks, little cuz! You’re a sweetheart. I've been practicing with Luna these past few days. I can't stop playing!",

        # AU game/script4.rpy:7347 (p)
        "There's no way out of this friend zone...":
            "Guess she still just sees me as her little cousin...",

        # AU game/script4.rpy:7402 (p)
        "What other people? You? Mom? Annie? I'm sure [mc] doesn't mind either. He's like... family. Like a little brother, almost.":
            "What other people? You? Mom? Annie? I'm sure [mc] doesn't mind either. He's just family. Like a little brother, almost.",

        # AU game/script4.rpy:7408 (p)
        "With [mc]? Pffft, please, my bar is WAY higher. You’ve seen my Instagram DMs: models, actors, influencers... did you know that that Gigachad meme guy from a few years ago tried sliding into my DMs?":
            "With [mc]? Pffft, please, even if he {i}wasn't{/i} our cousin, my bar is WAY higher. You’ve seen my Instagram DMs: models, actors, influencers... did you know that that Gigachad meme guy from a few years ago tried sliding into my DMs?",

        # AU game/script4.rpy:8176 (misc)
        "Actually, he was caught with HER sister in HIS office!":
            "Actually, he was caught with HIS OWN sister in HIS office!",


    # -----------------------------------------
    # 0.5 game/script5.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU game/script5.rpy:448 (d)
        "(Yeah, that would be fair. Just so we're even.)":
            "(If I had to go down on my own cousin, he should do it too. Just so we're even.)",

        # AU game/script5.rpy:465 (d)
        "(I don't even like him. The only guy I kinda liked lately wasn’t even into me.)":
            "(I don't even like him. The only guy I kinda liked lately was my own cousin... and he wasn’t even into me.)",

        # AU game/script5.rpy:1124 (n)
        "What have I done to deserve this? What god have I pissed off?!":
            "What have I done to deserve this? What god have I pissed off?! I haven't committed any sins...{w} other than, um... {w}lust, fornication, incest, greed, pride, and {i}so{/i} much temptation...",

        # AU game/script5.rpy:4799 (p)
        "*Knocks on the door* [mc]? Is that you?":
            "*Knocks on the door* Little cuz? Is that you?",

        # AU game/script5.rpy:4858 (p)
        "*Chuckles* Are you alright?":
            "*Chuckles* Are you alright, little cuz?",

        # AU game/script5.rpy:4902 (p)
        "Yeah, I'll let you finish your shower, sorry. Didn’t mean to give you a {i}hard{/i} time.":
            "Yeah, I'll let you finish your shower. Sorry, cuz. Didn’t mean to give you a {i}hard{/i} time.",

        # AU game/script5.rpy:5086 (p)
        "*Chuckles* Don’t be silly! You're staying with us until we say so. No escaping the Carters!":
            "*Chuckles* Don’t be silly, little cuz! You're staying with us until we say so. No escaping the Carters!",

        # ED/N: I completely rewrote the next three lines.
        # I've added the most incest lines for Penelope, and it's especially prevalent in casual conversation, which I left almost entirely untouched for Nancy and Dalia. During the party, I decided to dial it all back, so they're pretending to be just friends. Hopefully, you can feel the distinct absence of all the "little cuz"es, even though the lines are just vanilla. It also matches with the incest roleplay theme of Nancy's path in 0.5, except instead of pretending to be related, they're pretending not to be.
        # It's definitely not because I was going insane trying to figure out how to rewrite the truth or dare game if everyone knows they're related without them seeming absolutely insane...

        # AU game/script5.rpy:5217 (p)
        "*Chuckles* You're too excited, [mc].":
            "Hey, cuz... before we go in, let's agree not to tell anyone we're related.",

        # AU game/script5.rpy:5218 (p)
        "If you think this is going to be like American Pie, you'll be disappointed.":
            "There are a few people here I have some... {i}disagreements{/i} with, and I don't want to get you involved in it.",

        # AU game/script5.rpy:5219 (p)
        "Hey, there's a passed out Power Ranger next to a bottle of vodka by the entrance. That's promising.":
            "Alright, that makes sense... But if they pick a fight with me, that's fair game, right?",

        # AU game/script5.rpy:5286 (p)
        "Y-You... what?!":
            "Y-You... what?! B-But aren't you guys... y'know, blood-related?",

        # ED/N: I combined the next two lines to make space for a new line.
        # AU game/script5.rpy:5288 (p)
        "Isn't it crazy?!":
            "Isn't it crazy?! I've never been attracted to guys younger than me, let alone my little cousin, but I don't know... he's really cute! And...",

        # AU game/script5.rpy:5289 (p)
        "I've never been attracted to guys younger than me, but I don't know... he's really cute!":
            "*Whispering* Honestly, the fact that we're related makes it {i}{b}so{/b}{/i} much more exciting!",

        # AU game/script5.rpy:5302 (p)
        "But he might not be into me like that so... keep it secret!":
            "But we're still family, and he might not be into me like that so... keep it secret!",

        # AU game/script5.rpy:5316 (p)
        "(A BIG one!)":
            "(A BIG one! The biggest one I've ever heard!)",

        # AU game/script5.rpy:5322 (p)
        "(But holy shit, did she say she has a crush on [mc] too?!)":
            "(But holy shit, did she say she has a crush on [mc] too?! Her own {i}cousin!!{/i} I mean, I'm an only child, so I don't really know how their family works, but...)",

        # AU game/script5.rpy:5344 (p)
        "(Nothing happened. So what if my new bestie Penny and I have a crush on the same boy?)":
            "(Nothing happened. So what if my new bestie Penny and I have a crush on the same boy? So what if h-he's her cousin?)",

        # AU game/script5.rpy:7840 (p)
        "Or... your girlfriend, or anything.":
            "Or... your girlfriend, or anything. We're just cousins.",

        # AU game/script5.rpy:7888 (p)
        "I'd be mad too if someone had ignored me like that just to try to hook up with someone I don't like.":
            "I'd be mad too if my own cousin had ignored me like that just to try to hook up with someone I don't like.",

        # AU game/script5.rpy:7981 (p)
        "So... did you need anything, or were you just missing me?":
            "So... did you need anything, little cuz? Or were you just missing me?",

        # AU game/script5.rpy:7990 (p)
        "And you thought of asking your big titty blonde bimbo friend to lend you hers, right?":
            "And you thought of asking your big titty blonde bimbo cousin to lend you hers, right?",

        # AU game/script5.rpy:8022 (p)
        "And I need to wash my hair before it's too late! See ya!":
            "And I need to wash my hair before it's too late! See ya, cuzzy!",

        # AU game/script5.rpy:8317 (p)
        "I came with Penelope. I live with her, as part of the Student Exchange Program.":
            "I came with Penelope. I- uhh, I live with her, as part of the Student Exchange Program.",

        # AU game/script5.rpy:9062 (p)
        "Okay, it's about that damn yearbook.":
            "Okay, it's about that damn yearbook. I just didn't wanna get you mixed up in this.",

        # AU game/script5.rpy:9088 (p)
        "*Giggles* I knew I could count on you.":
            "*Giggles* I knew I could count on you, little cuz.",

        # AU game/script5.rpy:9149 (p)
        "Don't be such a bore! Where did you leave your spine, [mc]?":
            "Don't be such a bore! Where did you leave your spine, little cuz?",

        # AU game/script5.rpy:9217 (p)
        "But... wait, she's {i}interested{/i}?":
            "But... w-wait, she's {i}interested{/i}?",

        # AU game/script5.rpy:9218 (p)
        "What do you know? Did she tell you anything?":
            "What do you know? D-Did she tell you anything?",

        # AU game/script5.rpy:9303 (p)
        "Just a friend who's gonna help me sneak into the dorm room of someone who stole something from me.":
            "Just a kid who's gonna help me sneak into the dorm room of someone who stole something from me.",

        # AU game/script5.rpy:9505 (p)
        "*Whispering* I'm sorry I dragged you into this, [mc].":
            "*Whispering* I'm sorry I dragged you into this, cuz.",

        # AU game/script5.rpy:9577 (p)
        "My fucking god, [mc], you're hung like a fucking horse. That cock is a weapon!":
            "My fucking god, little cuz, you're hung like a fucking horse. That cock is a weapon!",

        # AU game/script5.rpy:9630 (p)
        "I'm {i}so{/i} very sorry for flaunting my lewd body in front of you, [mc]. I had no idea it would cause you so much stress...":
            "I'm {i}so{/i} very sorry for flaunting my lewd body in front of you, little cousin. I had no idea it would cause you so much stress...",

        # AU game/script5.rpy:9670 (p)
        "Okay, take a good look, [mc].":
            "Okay, take a good look, little cuz.",

        # AU game/script5.rpy:9681 (p)
        "Do you forgive me for acting naughty? For being such a tease? For flaunting myself all around you?":
            "Do you forgive me for acting naughty? For being such a tease? For flaunting myself all around my own cousin?",

        # AU game/script5.rpy:9725 (p)
        "You move closer to Penelope, frantically trying to memorize every square inch of the model’s ethereal body.":
            "You move closer to Penelope, frantically trying to memorize every square inch of your cousin’s ethereal body.",

        # AU game/script5.rpy:9747 (p)
        "*Giggles* You're crazy, [mc]...":
            "*Giggles* You're crazy, little cuz...",

        # AU game/script5.rpy:9750 (p)
        "You wrap your arms around Penelope's waist, holding her in place with a firm grip before beginning to suck on the blonde's voluptuous breasts.":
            "You wrap your arms around Penelope's waist, holding her in place with a firm grip before beginning to suck on your cousin's voluptuous breasts.",

        # AU game/script5.rpy:9765 (p)
        "She's mine... For at least tonight, Penelope Carter is all mine...":
            "She's mine... For at least tonight, my big cousin, Penelope Carter, is all mine...",

        # AU game/script5.rpy:9784 (p)
        "*Giggles* You're a filthy little degenerate.":
            "*Giggles* You're a filthy little degenerate, aren't you, cousin?",

        # AU game/script5.rpy:9797 (p)
        "*Giggles* Jesus, [mc], how long can you keep up an erection like that?":
            "*Giggles* Jesus, cuz, how long can you keep up an erection like that?",

        # AU game/script5.rpy:9813 (p)
        "What if it slips out of your costume again? We can’t have Nova or another girl accidentally catching sight of this monster dick, can we?":
            "What if it slips out of your costume again? We can’t have Nova or another girl accidentally catching sight of my cousin's monster dick, can we?",

        # AU game/script5.rpy:9823 (p)
        "*Giggles* I can imagine. Do you like feeling my big titties wrapped around your cock like this?":
            "*Giggles* I can imagine. Do you like feeling my big titties wrapped around your cock like this, little cousin?",

        # AU game/script5.rpy:9841 (p)
        "I rejected all their requests, but here I am doing it for free, for some high school kid with a fat dick.":
            "I rejected all their requests, but here I am doing it for free, for my kid cousin's fat dick.",

        # AU game/script5.rpy:9844 (p)
        "But I’m not just some high school kid, y’know...":
            "But I’m not just some kid, y’know...",

        # AU game/script5.rpy:9851 (p)
        "Yeah, I guess you can take a shot...":
            "Yeah, I guess you can take a shot, little cuz...",

        # AU game/script5.rpy:9859 (p)
        "I'm FUCKING the best tits on Instagram!":
            "I'm FUCKING my cousin's tits! The best tits on Instagram!",

        # AU game/script5.rpy:9888 (p)
        "Besides, we don't even have a condom...":
            "Besides, that would be incest. We're blood-related and... w-we don't even have a condom...",

        # AU game/script5.rpy:9899 (p)
        "AAaaaah... What are you d-doing to me?":
            "AAaaaah... What are you d-doing to me, c-cuz?",

        # AU game/script5.rpy:9910 (p)
        "Do you like this? Gliding your pussy along my cock?":
            "Do you like this? Gliding your pussy along your little cousin's thick cock?",

        # AU game/script5.rpy:9927 (p)
        "Your hands wrap around Penelope’s soft neck as you hasten your pace, your hips slamming relentlessly against the blonde's buttocks.":
            "Your hands wrap around Penelope’s soft neck as you hasten your pace, your hips slamming relentlessly against your cousin's buttocks.",

        # AU game/script5.rpy:9933 (p)
        "K-Keep up that pace, [mc]...":
            "K-Keep up that pace, cuzzy...",

        # AU game/script5.rpy:9954 (p)
        "*Choking* Y-Yeagh... u-use me as your fucking toy, [mc]...":
            "*Choking* Y-Yeagh... u-use me as your fucking toy, little cuz...",

        # AU game/script5.rpy:10010 (p)
        "I'm gonna have to ask you to come to all the parties I'm invited to from now on, [mc].":
            "I'm gonna have to ask you to come to all the parties I'm invited to from now on, little cuz.",

        # AU game/script5.rpy:10143 (p)
        "What are your plans, [mc]?":
            "What are your plans, cuz?",

        # AU game/script5.rpy:10274 (p)
        "Thanks, [mc]. You're a good friend.":
            "Thanks, [mc]. You're a good cousin.",

        # AU game/script5.rpy:10276 (p)
        "Hey, that's what friends are for.":
            "Hey, that's what family is for.",

        # AU game/script5.rpy:10307 (p)
        "Good night, [mc]...":
            "Good night, little cuz...",

        # AU game/script5.rpy:10317 (p)
        "I'm glad to have you as a friend.":
            "I'm glad I have you as my family.",

        # AU game/script5.rpy:10483 (n)
        "After all these years, you’re still taking care of me like a babysitter, eh Nancy?":
            "After all these years, you’re still taking care of me like a mother, eh Nancy?",

        # AU game/script5.rpy:10599 (n)
        "I'm not a girl, and I'm not Nancy's child.":
            "I'm not a girl, and Nancy isn't my mom. She's my aunt.",

        # AU game/script5.rpy:10730 (n)
        "And you, dear [mc]... are going to retrieve that information.":
            "And you, dear nephew... are going to retrieve that information.",

        # AU game/script5.rpy:11331 (n)
        "And that's not even taking into account our age difference or my background as your old nanny.":
            "And that's not even taking into account our age difference or the fact that you're my sister's child, and I raised you like my own son until you were 9 years old.",

        # AU game/script5.rpy:11374 (n)
        "Our age difference, my daughters, the Student Exchange Program, my history as your former nanny...":
            "Our age difference, our family, the Student Exchange Program... the fact that you're my sister's child, and I raised you like my own son until you were 9 years old...",

        # AU game/script5.rpy:11406 (n)
        "I'll take what I want.":
            "I don't care if it's wrong. I don't care if it's incest. I'll take what I want.",

        # AU game/script5.rpy:11446 (n)
        "Let me take care of you...":
            "Let your Auntie Nancy take care of you. You’ve been such a good boy, after all...",

        # AU game/script5.rpy:11458 (n)
        "Oh my, are you not excited enough? Wanna play with my titties in front of your face again?":
            "Oh my, are you not excited enough? Wanna play with my titties in front of your face again, baby boy?",

        # AU game/script5.rpy:11502 (n)
        "*Kneeling down* You know, my mother used to say that risk-takers defy destiny with every decision. I’ve always kept that thought in my head.":
            "*Kneeling down* You know, your grandmother used to say that risk-takers defy destiny with every decision. I’ve always kept that thought in my head.",

        # AU game/script5.rpy:11636 (n)
        "S-She's about to fuck me!":
            "M-My aunt is about to fuck me!",

        # AU game/script5.rpy:11670 (n)
        "Nancy starts moving up and down. Your penis spreads her wet lips apart, while quickly adjusting to the redhead's vicious pace.":
            "Nancy starts moving up and down. Your penis spreads her wet lips apart, while quickly adjusting to your aunt's vicious pace.",

        # AU game/script5.rpy:11712 (n)
        "Can you handle me going faster, sweetie? I’ll start slowly... and it’ll make your old babysitter feel so much better...":
            "Can you handle me going faster, sweetie? I’ll start slowly... and it’ll make your Auntie Nancy feel so much better...",

        # AU game/script5.rpy:11778 (n)
        "The poor security guard having to watch the two of us – AGH... FUCK! – h-having sweaty, animal sex in an elevator in the middle of the day...":
            "The poor security guard having to watch the two of us – AGH... FUCK! – h-having sweaty, incestuous sex in an elevator in the middle of the day...",

        # AU game/script5.rpy:11816 (n)
        "What a naughty mommy... what if your daughters could see you being fucked like this?":
            "What a naughty mommy... what if your daughters could see you being fucked like this by their own cousin?",

        # AU game/script5.rpy:11818 (n)
        "What a naughty empress... what if your subjects could see you being fucked like this?":
            "What a naughty empress... what if your subjects could see you being fucked like this by your own nephew?",

        # AU game/script5.rpy:11857 (n)
        "Don't worry, my queen, just lean against the wall and let me do the work here...":
            "Don't worry, my queen, just lean against the wall and let your prince do the work here...",

        # AU game/script5.rpy:11871 (n)
        "F-Fuck me again, [mc]...":
            "F-Fuck your Auntie again, [mc]...",

        # AU game/script5.rpy:11907 (n)
        "[mc] s-s-stop joking!":
            "[mc] s-s-stop joking! Th-this is incest! I-I can't have a baby w{size=40}AAAHHHHhhh{/size}... {w=1.5}w-with my own n-nephew!",

        # AU game/script5.rpy:11911 (n)
        "I can’t upset her, though... not if I want to do this again...":
            "I can’t cross that line, though... not if I want to do this again...",

        # AU game/script5.rpy:11963 (n)
        "I can't be fired, [mc], I have a family to feed!":
            "I can't be fired, [mc], I have to feed our family!",

        # AU game/script5.rpy:12409 (n)
        "You’ve really made the household... authentic. It’s almost like we were missing something before you came back.":
            "You’ve really made our family... authentic. It’s almost like we were missing something before you came back.",


    # -----------------------------------------
    # 0.6 game/script6.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU game/script6:


    # -----------------------------------------
    # 0.7 game/script7.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU game/script7:


    # -----------------------------------------
    # 0.8 game/script8.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU game/script8:


    # -----------------------------------------
    # 0.9 game/script9.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU game/script9:


    # -----------------------------------------


    # -----------------------------------------
        # Annie as stepsister, MC's dad remarried in UK
        # Combined with Nancy as aunt (mother's sister), Penelope and Dalia as cousins in annie_aunt_map
        # No name changes
        # Original map
        # (Probably) incompatible with other maps
        # -----------------------------------------
        # Annie stepsister character notes
        # 
        # - Annie: Only add references to not being blood-related during lines where they waver on sibling boundaries. Note: Never use "stepsibling" in their dialogue, especially when it gets emotional. Their relationship is 100% brother and sister, even if they're not biologically related. The "step-" doesn't matter to them in terms of boundaries. They should only call each other "big bro" and "little sis" in intimate lines as a little "younger sister" kick, and they usually just refer to each other by name. This path is the most emotionally incestuous, since they have a much more intimate relationship than anyone else.
        # -----------------------------------------
        # ST = Annie stepsister lines in annie_aunt_map
        # game/script.rpy:0000 = path/file name:line number
        # (menu) = Choice menu line
        # (chat) = Phone chat line
        # (n) = Nancy line
        # (p) = Penelope line
        # (d) = Dalia line
        # (a) = Annie line
        # (other) = Other line (Any/all main)
        # (misc) = Miscellaneous line (Extras/side characters)
        # These tags aren't based on who's speaking, but who the line and scene are about.
        # ED/N = Editor's notes
        # (REVIEW) = Line needs to be reviewed
        # -----------------------------------------


    # -----------------------------------------
    # 0.1 game/script.rpy Annie stepsister lines

        # ST game/script.rpy:1046 (a)
        "(Annie is a close friend from my childhood.)":
            "(Annie is my stepsister.)",

        # ST game/script.rpy:1047 (a)
        "(When I moved from Kredon, she was my next-door neighbor and the first person I met, along with Chang.)":
            "(When we moved from Kredon, she and her mother were our next-door neighbors, and she was the first person I met, along with Chang.)",

        # ST game/script.rpy:1049 (a)
        "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them.)":
            "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them, especially after they divorced.)",

        # ED/N: I combined this line with the next line to make space for a new line.
        # ST game/script.rpy:1050 (a)
        "(We were both lost... and lonely.)":
            "(Even after my dad and her mom got remarried, nothing changed. All we gained was one more absent parent.)",

        # ST game/script.rpy:1051 (a)
        "(After finding a companion within each other, we’ve been inseparable ever since.)":
            "(We were both lost... and lonely. After finding a companion within each other, we’ve been inseparable ever since.)"

        # ST game/script.rpy:1053 (a)
        "(Because of how close we were, people always believed we were dating... but the truth is, we're just friends.)":
            "(Because of how close we were, people always assumed we were dating... but the truth is, we're just siblings. Stepsiblings.)",

        # ST game/script.rpy:1054 (a)
        "(I mean… she's cute, and we love spending time with each other, but I've never tried to make a move on her.)":
            "(I mean… she's cute, and we love spending time with each other, but she's my little sister. I'd never try to make a move on her.)",

        # ST game/script.rpy:1059 (a)
        "(It would be... weird for us. Yeah! That's the word. Weird.)":
            "(It would be... weird for us. Yeah! What would our parents say?)",

        # ST game/script.rpy:1060 (a)
        "(It's just not the kind of relationship we have.)":
            "(She's my family, and we'll always be close friends. It's just not the kind of relationship we have.)",

        # ST game/script.rpy:1179 (a)
        "You're nothing but a big ball of envy because your best friend can play Eternum and you can't since you didn't save any money.":
            "You're nothing but a big ball of envy because your one-and-only little sister and best friend can play Eternum, and you can't since you didn't save any money.",

        # ST game/script.rpy:1233 (a)
        "I guess it would be you, Annie.":
            "I guess it would be you, sis.",

        # ST game/script.rpy:1254 (misc)
        "You're my best... male friend!":
            "You're my best... bro!",

        # ST game/script.rpy:1262 (misc)
        "Ahh, it's a deal, my friend!":
            "Ahh, it's a deal, brother!",

        # ST game/script.rpy:1344 (a)
        "I know you're excited Annie, but I'd appreciate it if you could at least carry your hand baggage!":
            "I know you're excited sis, but I'd appreciate it if you could at least carry your hand baggage!",

        # ST game/script.rpy:1757 (a)
        "Mission failed, [mc]...":
            "Mission failed, bro...",

        # ST game/script.rpy:1970 (a)
        "Oh, and you must be Annie! Nice to meet you too!":
            "Oh, and you must be Annie, [mc]'s stepsister! Nice to meet you too!",

        # ST game/script.rpy:2799 (a)
        "(I guess I should let them walk to school on their own, since I don't wanna look like a jealous boyfriend or something.)":
            "(I guess I should let them walk to school on their own, since I don't wanna look like an overprotective older brother or something.)",

        # ST game/script.rpy:2816 (a)
        "(Bah, Annie's a big girl. She doesn't need protecting.)":
            "(Bah, Annie isn't my baby sister anymore. She doesn't need protecting.)",

        # ST game/script.rpy:2910 (a)
        "The lady said no, buddy.":
            "Hands off my little sister, buddy. The lady said no.",

        # ST game/script.rpy:2934 (a)
        "The lady said no.":
            "Hands off my little sister. The lady said no.",

        # ST game/script.rpy:2952 and game/script4.rpy:4803 (a)
        "Are you okay, Annie?":
            "Are you okay, sis?",

        # ST game/script.rpy:3006 (a)
        "And... thank you again for helping me out back there, [mc].":
            "And... thank you again for helping me out back there, big bro.",

        # ST game/script.rpy:5178 (a)
        "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal when I was living with my dad.":
            "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal when I was living with my dad and stepmom.",

        # ST game/script.rpy:6697 (a)
        "So this is the [mc] you're always talking about?":
            "So this is the {i}big brother{/i} you're always talking about?",

        # ST game/script.rpy:7130 (a)
        "(That's a bad idea...)":
            "(That's a bad idea... she's my little sister.)",

        # ST game/script.rpy:7176 (a)
        "(Jeez, I've always tried to not think of Annie in \"that\" way because I don't want to ruin our friendship, but now...)":
            "(Shit, I've always tried to not think of Annie in \"that\" way because I don't want to ruin our relationship, but now...)",

        # ST game/script.rpy:7186 (a)
        "(Damn... I guess she’s not the skinny kid she used to be...)":
            "(Damn... I guess she’s not the skinny baby sister she used to be...)",

        # ST game/script.rpy:8102 (a)
        "Erm... Y-You're the best friend ever!":
            "Erm... Y-You're the best big brother ever!",

        # ST game/script.rpy:8468 (a)
        "The pleasure was all mine, Annie. Eternum is awesome. I’m so grateful I had you by my side.":
            "The pleasure was all mine, little sis. Eternum is awesome. I’m so grateful I had you by my side.",


    # -----------------------------------------
    # 0.2 game/script2.rpy Annie stepsister lines

        # ST game/script2.rpy:106 (a)
        "*Laughs* Don't mind him...":
            "*Laughs* Don't mind my brother...",

        # ST game/script2.rpy:138 (a)
        "*Laughs* Come on, the last time we watched a horror movie, you couldn’t sleep alone for an entire two weeks!":
            "*Laughs* Come on, sis! The last time we watched a horror movie, you couldn’t sleep alone for an entire two weeks!",

        # ST game/script2.rpy:1014 (a)
        "Annie should be waiting for us already.":
            "Your sister should be waiting for us already.",

        # ST game/script2.rpy:3408 (a)
        "Oh, [mc]! I wasn’t sure if you were asleep already!":
            "Oh, hey bro! I wasn’t sure if you were asleep already!",

        # ST game/script2.rpy:3418 (a)
        "I told you! You shouldn't have played in Luna's server, Annie! You can't handle that scary stuff! Remember when we played Dead Space?":
            "I told you! You shouldn't have played in Luna's server, sis! You can't handle that scary stuff! Remember when we played Dead Space?",

        # ST game/script2.rpy:3474 (a)
        "You can sleep here as many times as you want. You don’t even have to ask, alright?":
            "You can sleep here as many times as you want. You don’t even have to ask, alright? Just like when we were little.",

        # ST game/script2.rpy:3479 (a)
        "Anytime, Annie.":
            "Anytime, sis.",

        # ST game/script2.rpy:3504 (a)
        "G-Goodnight, [mc].":
            "G-Goodnight, bro.",

        # ST game/script2.rpy:3506 (a)
        "Goodnight Annie.":
            "Goodnight sis.",

        # ST game/script2.rpy:3530 (a)
        "(We're in quite an... intimate position... I don't want her to think I'm trying to take advantage of her while she sleeps.)":
            "(We're in quite an... intimate position... I don't want her to think her brother is trying to take advantage of her while she sleeps.)",

        # ST game/script2.rpy:3557 (a)
        "Baloo?":
            "Mr. Baloo? That teddy bear your mom gave you when you were 5?",

        # ST game/script2.rpy:3559 (a)
        "Oh... Well... It's a stuffed bear that my mother gave me when I was 5, and...":
            "Y-yeah, Mr. Baloo...",

        # ST game/script2.rpy:3564 (a)
        "Oh... I didn't know about Baloo.":
            "Oh... I didn't know you still had him.",

        # ST game/script2.rpy:3594 (a)
        "(He probably just sees me as the little girl who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)":
            "(He probably just sees me as the little sister who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)",

        # ST game/script2.rpy:3595 (a)
        "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack.)":
            "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack. Not a weirdo like me who has feelings for her own big brother...)",

        # ST game/script2.rpy:3596 (a)
        "(I'll always just be Annie, the \"best friend\".)":
            "(I'll always just be Annie, the \"little sister\".)",

        # ST game/script2.rpy:3602 (a)
        "(I'm a fucking mess. She needs someone more mature.)":
            "(I'm a fucking mess. She needs someone more mature... not a creep who has a crush on his little sister.)",

        # ST game/script2.rpy:3603 (a)
        "(This is why I'll always just be [mc], the \"best friend\"...)":
            "(This is why I'll always just be [mc], the \"big brother\"...)",

        # ST game/script2.rpy:3631 (a)
        "It’s just a shirt after all, right...?":
            "It’s just a shirt after all, right...? You've seen me without it before...",

        # ED/N: I combined this line with the next line to make space for a new line.
        # ST game/script2.rpy:3633 (a)
        "(I'm not sure where she’s going with all of this...)":
            "(The last time I saw her topless was when we were 9 and still bathing together, though...)",

        # ST game/script2.rpy:3634 (a)
        "(But I sure as hell want to find out...)":
            "(I'm not sure where she’s going with all of this... but I sure as hell want to find out...)",

        # ST game/script2.rpy:3642 (a)
        "(This doesn't seem like the Annie I’ve known since I was young... Is she trying to prove something?)":
            "(This doesn't seem like my sister... Is she trying to prove something?)",

        # ST game/script2.rpy:3647 (a)
        "(Holy shit, I’ve never seen her in such an... intimate way...)":
            "(Holy shit, I never noticed know how much she had... grown up...)",

        # ST game/script2.rpy:3652 (a)
        "(This is really Annie... {i}my{/i} Annie.)":
            "(This is really my sister... {i}my{/i} sister.)",

        # ST game/script2.rpy:3658 (a)
        "We're just... friends getting a little more comfortable.":
            "We're just... a brother and sister getting a little more comfortable.",

        # ST game/script2.rpy:3703 (a)
        "Your skin feels so soft, Annie. It feels... really nice holding you...":
            "Your skin feels so soft, sis. It feels... really nice holding you...",

        # ST game/script2.rpy:3711 (a)
        "(Oh my god, am I the only one feeling all this tension in the air? I want to make a move, but... I don’t want to overstep my bounds...)":
            "(Oh my god, am I the only one feeling all this tension in the air? I want to make a move, but... I really don’t want to overstep my bounds...)",

        # ST game/script2.rpy:3718 (a)
        "(But it’s not just any guy. It’s [mc].)":
            "(But it’s not just any guy. It’s [mc]. Your big brother.)",

        # ST game/script2.rpy:3721 (a)
        "(But... I don't want to scare her away. Annie has always been so special to me. If I try something and it doesn't work out, I couldn’t bear the thought of losing her...)":
            "(But... I don't want to scare her away. Annie has always been more than a friend, more than a sister to me. If I try something and it doesn't work out, I couldn’t bear the thought of losing her...)",

        # ST game/script2.rpy:3722 (a)
        "(I can’t deny it... I want more of him...)":
            "(I can’t deny it, I want more of him... I mean, we aren’t even blood-related...)",

        # ST game/script2.rpy:3729 (a)
        "(Baby steps, [mc]. Baby steps.)":
            "(A-And this all still feels so wrong... we shouldn't go any further than this... {w}right...?)",

        # ST game/script2.rpy:3740 (a)
        "Um... Annie...?":
            "Um... sis...?",

        # ST game/script2.rpy:3763 (a)
        "I’m sorry, Annie... I can’t help it... you’re driving me insane...":
            "I’m sorry, sis... I can’t help it... you’re driving me insane...",

        # ST game/script2.rpy:3800 (a)
        "[mc]. I said I’m nervous, but that doesn’t mean I... don’t want to...":
            "Big bro. I said I’m nervous, but that doesn’t mean I... don’t want to...",

        # ST game/script2.rpy:3826 (a)
        "I thought you weren’t interested in me...":
            "I thought you weren’t interested in me... I was just your little sister...",

        # ST game/script2.rpy:3828 (a)
        "Where did you get that idea from?":
            "Annie, you've never been {i}just{/i} my little sister.",

        # ST game/script2.rpy:3829 (a)
        "You're perfect.":
            "You're... perfect.",

        # ST game/script2.rpy:3830 (a)
        "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our friendship.":
            "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our relationship as brother and sister.",

        # ST game/script2.rpy:3840 (a)
        "*Chuckles* You know I’m not one to break my promises.":
            "*Chuckles* You know I’m not one to break my promises, sis.",

        # ST game/script2.rpy:3867 (a)
        "(Holy shit, this is really happening! I'm fucking Annie's thighs!)":
            "(Holy shit, this is really happening! I'm fucking my little sister's thighs!)",

        # ST game/script2.rpy:3870 (a)
        "(I never would’ve thought I’d have a chance with him...)":
            "(I never would’ve thought I’d have a chance to do this with my big brother...)",

        # ST game/script2.rpy:3872 (a)
        "Jesus, Annie...":
            "Jesus, sis...",

        # ST game/script2.rpy:3924 (a)
        "Oh shit, I'm sorry, Annie...":
            "Oh shit, I'm sorry, sis...",

        # ST game/script2.rpy:3942 (a)
        "I only came here t-to sleep and then... next thing I know I’m doing that...":
            "I only came here t-to sleep and then... next thing I know I’m doing that... with my big brother!",

        # ST game/script2.rpy:3946 (a)
        "I started m-moving and then I c-couldn't stop and... now I’m not going to have my fairy tale ending... because what kind of Disney princess romance begins with a THIGH JOB?! AHAHAH!!":
            "I started m-moving and then I c-couldn't stop and... now I’m not going to have my fairy tale ending... because what kind of Disney princess romance begins with a BROTHER-SISTER THIGH JOB?! AHAHAH!!",

        # ST game/script2.rpy:3952 (a)
        "We skipped like 14 steps! In one night!":
            "We skipped like 14 steps and broke a dozen rules! In one night!",

        # ST game/script2.rpy:3964 (a)
        "I'm gonna... go... think! Good night [mc]!":
            "I'm gonna... go... think! Good night bro!",

        # ST game/script2.rpy:3981 (a)
        "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing Annie’s secret kinky side... and I loved every moment of it!)":
            "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing my sister's secret kinky side... it felt so wrong... and I loved every moment of it!)",

        # ST game/script2.rpy:5413 (n)
        "(I bet if I tried to do anything at home, Dalia or Penny would surely notice.)":
            "(I bet if I tried to do anything at home, one of the girls would surely notice.)",

        # ST game/script2.rpy:5937 (a)
        "And on the first day of school, I saw him harassing a close friend of mine.":
            "And on the first day of school, I saw him harassing my sister.",

        # ST game/script2.rpy:6103 (a)
        "I never met my mother and my father was always absent in my life. He was constantly too occupied with his work.":
            "I never met my mother, and my father and stepmother were always absent in my life. They were constantly too occupied with their work.",


    # -----------------------------------------
    # 0.3 game/script3.rpy Annie stepsister lines

        # ST game/script3.rpy:3343 (a)
        "Not a worry in mah noggin, homie. I just be... chillaxin’ all day! Yeahhhh...":
            "Not a worry in mah noggin, bro. I just be... chillaxin’ all day! Yeahhhh...",

        # ST game/script3.rpy:3402 (a)
        "(That's all I want... just to stay friends with her.)":
            "(That's all I want... just to be brother and sister again.)",

        # ST game/script3.rpy:3428 (a)
        "I've liked you ever since we were 10. If I’m being real with you, the only reason why I was willing to come back to Kredon at all was because you were coming too.":
            "I've liked you ever since we were 10. If I’m being real with you, the only reason why I was willing to come back to Kredon at all was because you were coming with me.",

        # ST game/script3.rpy:3431 (a)
        "You're my best friend.":
            "You're my little sister and my best friend.",

        # ST game/script3.rpy:3434 (a)
        "And in my heart I know, I want us to be so much more than that, too...":
            "And in my heart I know, even if it's wrong, I want us to be so much more than that, too...",

        # ST game/script3.rpy:3439 (a)
        "And, as much as I loved that night, I know things might’ve felt like they were moving way too fast for you.":
            "And, as much as I loved that night, I think we both felt like things were moving way too fast.",

        # ST game/script3.rpy:3446 (a)
        "I don't want to lose our friendship, Annie. I’d be miserable without you in my life.":
            "I don't want to lose you, sis. I’d be miserable without you in my life.",

        # ST game/script3.rpy:3449 (a)
        "I just want us to stay friends forever!":
            "I just want us to stay together forever!",

        # ST game/script3.rpy:3467 (a)
        "That sounds great! Just spending some time together as good friends. Like how we’ve always done it!":
            "That sounds great! Just spending some time together as siblings. Like how we’ve always done it!",

        # ST game/script3.rpy:3483 (a)
        "Like... a fun date between friends?":
            "Like... a fun date between siblings?",

        # ST game/script3.rpy:3484 (a)
        "Hmmm... no, more like a date with a girl that I like. And I just happen to be so lucky in that, she’s also my best friend too. As for what the future holds? Who knows...":
            "Hmmm... no, more like a date with a girl that I like. And it just happens to be that she’s also my adorable little sister, and my best friend too. As for what the future holds? Who knows...",

        # ST game/script3.rpy:3511 (a)
        "And not a word to anyone. I mean... there's no need for it, really. We’re just two people going on a date, and there’s no need to overthink it.":
            "And not a word to anyone. I mean... there's no need for it, really. We’re just two {i}totally non-blood-related{/i} people going on a date, and there’s no need to overthink it.",

        # ST game/script3.rpy:3540 (a)
        "I know you want to take things slow. And I’m perfectly okay with that.":
            "I know you want to take things slow, sis. And I’m perfectly okay with that.",

        # ST game/script3.rpy:3561 (a)
        "That was quite the goodbye for just a couple of... friends.":
            "That was quite the goodbye for just a brother and sister...",

        # ST game/script3.rpy:9866 (n)
        "I think this goes without saying, but let’s not mention this to anyone. My daughters especially... heaven knows what they’d think if they learned we bathed together.":
            "I think this goes without saying, but let’s not mention this to anyone. My daughters and your stepsister especially... heaven knows what they’d think if they learned we bathed together.",


    # -----------------------------------------
    # 0.4 game/script4.rpy Annie stepsister lines

        # ST game/script4.rpy:4335 (a)
        "(A date with [mc]!)":
            "(A date with my big brother!)",

        # ST game/script4.rpy:4336 (a)
        "(A date in Eternum WITH [mc]!)":
            "(A date in Eternum WITH my big brother!)",

        # ST game/script4.rpy:4914 (a)
        "I feel so comfortable with Annie that sometimes I forget we're not really... a couple.":
            "I feel so comfortable with Annie that sometimes I forget we're just siblings, not really a... a couple.",

        # ST game/script4.rpy:5004 (a)
        "You and Chang have always been my best friends, and neither of you played Eternum until recently, so... I've always felt kind of alone here.":
            "You and Chang have always been by my side, and neither of you played Eternum until recently, so... I've always felt kind of alone here.",

        # ST game/script4.rpy:5008 (a)
        "You’re the one who’s really made these first few weeks in Eternum worthwhile, Annie. I couldn't have asked for anyone better to spend time with.":
            "You’re the one who’s really made these first few weeks in Eternum worthwhile, sis. I couldn't have asked for anyone better to spend time with.",

        # ST game/script4.rpy:5131 (a)
        "Oh! Come on, Annie! You can't be serious!":
            "Oh! Come on, sis! You can't be serious!",

        # ST game/script4.rpy:5250 (a)
        "(Maybe... it's just not the right time yet...?)":
            "(Maybe... was this all a mistake...?)",

        # ST game/script4.rpy:5311 and Multi-Mod game/script4.rpy:5339 and Bonus Mod game/script4.rpy:5366 (menu)
        "Decline and stay as friends":
            "{color=[walk_path]}Decline and stay as stepsiblings [red][mt](Closes Annie's path)",

        # ST game/script4.rpy:5314 (a)
        "I like you, and you're my best friend, you already know that.":
            "I like you, and you're my beloved little sister and my best friend. You already know that.",

        # ST game/script4.rpy:5315 (a)
        "But... I also feel like we're not meant to be more than that. Things would get awkward if we tried to get together, and our friendship is too important to risk, for me at least.":
            "But... I also feel like we're not meant to be more than that. Things would get so complicated if we tried to get together as stepsiblings, and our friendship, our {i}family{/i}, is too important to risk, for me at least.",

        # ED/N: I completely rewrote the next four lines.
        # This is the biggest change I've made so far in the writing, beyond just adding incest themes. I felt like this scene needed more conversation and emotional weight, especially for his little sister. He sounds way too flippant in the original. The theme is, "Maybe MC is right and this would ruin their relationship... or maybe he's just growing up and scared of change. But he's definitely not mature enough to deal with it now."
        # Shit, it took me a whole afternoon to think of what to say to her, and 99% of players won't even see it. I'll try not to make these rewrites a habit, since I also think it's important to preserve the original writing.

        # ST game/script4.rpy:5316 (a)
        "I just like spending time with you!":
            "I just... Annie, I don’t want these feelings to overwrite all the memories and the relationship we’ve built until now.",

        # ST game/script4.rpy:5317 (a)
        "I... I think we're meant to be friends. Best friends!":
            "Sometimes, when I look at you, I don’t recognize the Annie I’ve always known.",

        # ST game/script4.rpy:5318 (a)
        "So... let's just stay like this for now, okay?":
            "Sometimes, I don’t recognize myself.",

        # ST game/script4.rpy:5319 (a)
        "I just don’t have those feelings for you right now.":
            "It feels like we’re on the edge of losing something we’ve always had, and I’m...{w}{i}{size=27} I-I’m scared we’ll never get it back.",

        # ST game/script4.rpy:5320 (a)
        "In the future... who knows? Maybe. But I don’t want to lead you on, either.":
            "I can’t commit to this... {i}thing{/i} between us. Not right now. In the future... I don’t know. Maybe. But I don’t want to lead you on, either.",

        # ST game/script4.rpy:5326 (a)
        "No worries! I totally understand. My head has been all over the place too, you know, with all this back and forth...":
            "It's not your fault, Annie, it's mine. I know I've been sending you mixed signals, bringing you here today. My head has been all over the place too, you know, with all this back and forth...  You don't deserve that.",

        # ST game/script4.rpy:5327 (a)
        "We can have this conversation again after we gather the 10 Gems!":
            "I'm sorry, sis. This isn't how I wanted today to go. For what it's worth, I still enjoyed spending this time with you.",

        # ST game/script4.rpy:5369 (a)
        "Y-Yeah... It's been like... 10 years since we first met?":
            "Y-Yeah... It's been like... 10 years since we became family?",

        # ST game/script4.rpy:5405 (a)
        "Seeing you undressing just for me was hot as fuck, Annie.":
            "Seeing you undressing just for me was hot as fuck, sis.",

        # ST game/script4.rpy:5436 (a)
        "But... Do you think I'm NOT nervous? I'm super scared too! I mean, in my arms, I'm holding an adorably precious, absolutely gorgeous girl whom I’ve liked for years.":
            "But... Do you think I'm NOT nervous? I'm super scared too! I mean, in my arms, I'm holding my adorably precious, absolutely gorgeous little sister whom I’ve liked for years.",

        # ST game/script4.rpy:5438 (a)
        "I know it's scary to get out of your comfort zone, but... I think we can overcome it together.":
            "After so long together, I know it's scary to go outside what's familiar to us, but... I think we can overcome it together.",

        # ST game/script4.rpy:5442 (a)
        "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay friends!":
            "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay as siblings and friends!",

        # ST game/script4.rpy:5443 (a)
        "It’ll be a little awkward at first, but our friendship is strong, and I know we’d be back to normal in no time.":
            "It’ll be a little awkward at first, but our relationship is strong, and I know we’d be back to normal in no time.",

        # ST game/script4.rpy:5447 (a)
        "I know it's scary to cross this bridge when you're not sure what your partner might want, so let me be clear...":
            "I know it's scary to cross this bridge when you're not sure what your partner might want, or what our relationship is even supposed to be, so let me be clear...",

        # ST game/script4.rpy:5449 (a)
        "You are so ridiculously pretty, Annie, that I can’t help but want to take our relationship to the next level.":
            "You’re my beloved little sister and my best friend, and that part of us will never change. But... you’re so ridiculously pretty, Annie, that I can’t help but want to take our relationship to the next level.",

        # ST game/script4.rpy:5471 (a)
        "*Caressing her cheek* I feel like I could never get enough of you, Annie...":
            "*Caressing her cheek* I feel like I could never get enough of you, sis...",

        # ST game/script4.rpy:5518 (a)
        "Have I been fooled all these years? Innocent, shy Annie is actually a horny, perverted little girl?":
            "Have I been fooled all these years? My innocent, shy sister is actually a horny, perverted little girl?",

        # ST game/script4.rpy:5526 (a)
        "God, there are so many things I want to do to Annie right now... but it's still Annie. I don't wanna cross any line too fast.":
            "God, there are so many things I want to do to Annie right now... but she's still my little sister. I don't wanna cross any line too fast.",

        # ST game/script4.rpy:5562 (a)
        "It'll only get better from here, babe...":
            "It'll only get better from here, sis...",

        # ST game/script4.rpy:5604 (a)
        "*Panting* K-Keep going, [mc]! Y-You’re hitting just the... r-right spot!":
            "*Panting* K-Keep going, b-big bro! Y-You’re hitting just the... r-right spot!",

        # ST game/script4.rpy:5619 (a)
        "W-What are you *moans* doooooing to m-me...?":
            "W-What are you *moans* doooooing to m-me, b-big brotheeeerrrr...?",

        # ST game/script4.rpy:5624 (a)
        "Don't worry, babe...":
            "Don't worry, sis...",

        # ST game/script4.rpy:5665 (a)
        "([mc] made me... {i} cum{/i}!)":
            "(My big brother made me... {i} cum{/i}!)",

        # ST game/script4.rpy:5682 (a)
        "Of course you can see it... After all, you’re responsible for it...":
            "Of course you can see it, little sis... After all, you’re responsible for it...",

        # ST game/script4.rpy:5724 (a)
        "You’re such a good girl, Annie...":
            "You’re such a good little sister, Annie...",

        # ST game/script4.rpy:5758 (a)
        "I love beating off your... massive... pulsing... d-dirty cock...":
            "I love beating off my b-big brother's... massive... pulsing... d-dirty cock...",

        # ST game/script4.rpy:5765 (a)
        "*Panting* F-Fuck, I won't last much longer, Annie...":
            "*Panting* F-Fuck, I won't last much longer, sis...",

        # ST game/script4.rpy:5767 (a)
        "I want to make you cum, [mc]... You were so kind to me...":
            "I want to make you cum, big bro... You were so kind to me...",

        # ST game/script4.rpy:5823 (a)
        "I want you so bad, Annie... I can’t wait ‘til the day you can finally take this dick... But not yet...":
            "I want you so bad, sis... I can’t wait ‘til the day you can finally take this dick... But not yet...",

        # ST game/script4.rpy:5825 (a)
        "W-We’ve g-gotta do some practicing b-beforehand, [mc]...":
            "W-We’ve g-gotta do some practicing b-beforehand, b-bro...",

        # ST game/script4.rpy:6924 (a)
        "Oh Annie... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?":
            "Oh sis... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?",

        # ST game/script4.rpy:7250 (a)
        "Thank you for an amazing day, [mc].":
            "Thank you for an amazing day, big bro.",

        # ST game/script4.rpy:7252 (a)
        "I'm glad you enjoyed it, Annie. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.":
            "I'm glad you enjoyed it, sis. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.",

        # ST game/script4.rpy:7431 (a)
        "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what best friends do, I guess.":
            "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what brothers do, I guess.",


    # -----------------------------------------
    # 0.5 game/script5.rpy Annie stepsister lines

        # ST game/script5.rpy:842 (a)
        "I don't really mind anymore. I'm happy being just a good friend.":
            "I don't really mind anymore. I'm happy just being his little sister.",

        # ST game/script5.rpy:12104 (n)
        "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters would take the news.":
            "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters or your sister would take the news.",


    # -----------------------------------------
    # 0.6 game/script6.rpy Annie stepsister lines

        # ST game/script6:


    # -----------------------------------------
    # 0.7 game/script7.rpy Annie stepsister lines

        # ST game/script7:


    # -----------------------------------------
    # 0.8 game/script8.rpy Annie stepsister lines

        # ST game/script8:


    # -----------------------------------------
    # 0.9 game/script9.rpy Annie stepsister lines

        # ST game/script9:

    }

    def _build_replace_map():
        """
        Build the active replacement map from flags.
        """
        incest_enabled = getattr(renpy.store, 'annie_incest', False)
        sister_enabled = getattr(renpy.store, 'annie_sister', False)
        mom_enabled = getattr(renpy.store, 'annie_mom', False)
        half_enabled = getattr(renpy.store, 'annie_half_sister', False)
        aunt_enabled = getattr(renpy.store, 'annie_aunt', False)
        # cousin_override = getattr(renpy.store, 'im_cousin_override', False)
        mapping = {}

        if mom_enabled:
            # Nancy Mom uses base map only.
            mapping.update(mom_map)

        if incest_enabled:
            # Full Incest uses base + sister map (as requested).
            mapping.update(annie_sister_map)
        elif sister_enabled:
            # Only sister uses its own extra map.
            mapping.update(annie_only_sister_map)

        if half_enabled:
            # Half-sister uses base + half-sister map.
            mapping.update(annie_half_sister_map)

        if aunt_enabled:
            # Aunt uses its own map.
            mapping.update(annie_aunt_map)

        # if cousin_override:
        #     mapping.update(cousin_map)  # highest priority overrides

        # Disabled: no replacements.
        return mapping

# -----------------------------------------
# Helpers + Replacer
# -----------------------------------------
init python:
    import re

    # Normalize curly quotes/dashes so translated strings with ASCII punctuation still match
    _in_char_equiv_table = {
        ord("\u2018"): "'",
        ord("\u2019"): "'",
        ord("\u201a"): "'",
        ord("\u201c"): "\"",
        ord("\u201d"): "\"",
        ord("\u201e"): "\"",
        ord("\u2013"): "-",
        ord("\u2014"): "-",
        ord("\u2212"): "-",
        ord("\u00a0"): " ",
        ord("\u2026"): "...",
    }

    _in_strip_tag_re = re.compile(r"\{/?[^{}]+\}")

    def _in_normalize_equiv_text(value):
        if not isinstance(value, str):
            return value
        simplified = value.translate(_in_char_equiv_table)
        # collapse whitespace differences so translations missing spaces still match
        simplified = re.sub(r"\s+", " ", simplified.strip())
        return simplified

    def _in_strip_tags(value):
        if not isinstance(value, str):
            return value
        return _in_strip_tag_re.sub("", value)

    # cache last speaker for "extend"
    try:
        _last_say_who
    except NameError:
        _last_say_who = None
    try:
        _last_say_who_name
    except NameError:
        _last_say_who_name = None
    try:
        _in_ast_module = renpy.ast
    except Exception:
        _in_ast_module = None

    def _normalize_who(who):
        if who is None:
            return None
        return str(getattr(who, "name", who)).strip()

    def _in_current_speaker():
        """
        Identify the active speaker while the say/menu filter runs.
        Ren'Py updates last_say() *after* the filter executes, so we look up
        the current AST node directly to determine who is talking.
        """
        global _last_say_who
        global _last_say_who_name
        ast_mod = _in_ast_module
        if ast_mod is None:
            return (_last_say_who, _last_say_who_name)
        try:
            ctx = renpy.game.context()
            node_id = getattr(ctx, "current", None)
            if not node_id:
                return (_last_say_who, _last_say_who_name)
            node = renpy.game.script.lookup(node_id)
        except Exception:
            return (_last_say_who, _last_say_who_name)
        SayCls = getattr(ast_mod, "Say", None)
        if SayCls is None or not isinstance(node, SayCls):
            return (_last_say_who, _last_say_who_name)
        raw_who = getattr(node, "who", None)
        if isinstance(raw_who, str):
            raw_who = raw_who.strip()
        if not raw_who:
            _last_say_who = None
            _last_say_who_name = None
            return (None, None)
        if raw_who == "extend":
            return (_last_say_who, _last_say_who_name)
        who_obj = None
        try:
            who_obj = ast_mod.eval_who(node.who, node.who_fast)
        except Exception:
            who_obj = None
        who_name = _normalize_who(who_obj)
        if not who_name and isinstance(raw_who, str):
            who_name = raw_who
        _last_say_who = who_obj
        _last_say_who_name = who_name
        return (_last_say_who, _last_say_who_name)

    def _is_mc_like(who_obj, who_name):
        """
        Check if speaker is MC (object identity + name fallbacks).
        """
        try:
            store = renpy.store
            mc_objs = [
                getattr(store, "mc", None),
                getattr(store, "mct", None),
                getattr(store, "mcd", None),
                getattr(store, "mcsc", None),
            ]
            if who_obj is not None and any(who_obj is x for x in mc_objs if x is not None):
                return True
        except Exception:
            pass

        return who_name in ("mc", "mct", "mcd", "mcsc", "[mc]", "MC", "You")

    def _in_any_mode_active():
        return (
            getattr(renpy.store, 'annie_incest', False)
            or getattr(renpy.store, 'annie_sister', False)
            or getattr(renpy.store, 'annie_mom', False)
            or getattr(renpy.store, 'annie_half_sister', False)
            or getattr(renpy.store, 'annie_aunt', False)
        )

    def _in_transform_text(s: str) -> str:
        t = s
        # If neither mode is active, skip all replacements entirely.
        if not _in_any_mode_active():
            return t
        t_norm = _in_normalize_equiv_text(t)
        t_norm_stripped = _in_normalize_equiv_text(_in_strip_tags(t))

        # 2) resolve [mc] and [lastname] as shown on screen
        mc_display = None
        lastname_display = None
        try:
            mc_display = renpy.substitute("[mc]")
            if not mc_display or mc_display == "[mc]":
                for cand in ("player_name", "mc_name", "name_mc"):
                    val = getattr(renpy.store, cand, None)
                    if isinstance(val, str) and val.strip():
                        mc_display = val.strip()
                        break
            if not mc_display:
                mc_display = "[mc]"
        except Exception:
            mc_display = "[mc]"

        try:
            lastname_display = renpy.substitute("[lastname]")
            if not lastname_display or lastname_display == "[lastname]":
                for cand in ("lastname", "mc_lastname", "last_name", "surname"):
                    val = getattr(renpy.store, cand, None)
                    if isinstance(val, str) and val.strip():
                        lastname_display = val.strip()
                        break
            if not lastname_display:
                lastname_display = "[lastname]"
        except Exception:
            lastname_display = "[lastname]"

        # 3) apply mapping first (before Nancy->Mom)
        try:
            mapping = _build_replace_map()
            for old, new in mapping.items():
                if not old:
                    continue




                # Build candidate variants allowing either raw placeholders or resolved values
                candidates = set([old])
                if "[mc]" in old and mc_display != "[mc]":
                    candidates.add(old.replace("[mc]", mc_display))
                # Expand for [lastname] on top of current candidates
                if "[lastname]" in old and lastname_display != "[lastname]":
                    for base in list(candidates):
                        candidates.add(base.replace("[lastname]", lastname_display))

                replaced_once = False
                for cand in candidates:
                    if not cand:
                        continue

                    cand_match = (t == cand)
                    if (not cand_match) and (t_norm is not None):
                        cand_match = (_in_normalize_equiv_text(cand) == t_norm)
                    if cand_match:
                        rep = new
                        if "[mc]" in rep:
                            rep = rep.replace("[mc]", mc_display)
                        if "[lastname]" in rep:
                            rep = rep.replace("[lastname]", lastname_display)
                        t = rep
                        t_norm = _in_normalize_equiv_text(t)
                        t_norm_stripped = _in_normalize_equiv_text(_in_strip_tags(t))
                        replaced_once = True
                        break

                # regex fallback allowing either [mc] or resolved name
                if (not replaced_once) and ("[mc]" in old) and (mc_display != "[mc]"):
                    try:
                        pattern = "^" + re.escape(old).replace(
                            re.escape("[mc]"),
                            r"(?:\[mc\]|%s)" % re.escape(mc_display)
                        ) + "$"
                        rep = new.replace("[mc]", mc_display)
                        if "[lastname]" in rep:
                            rep = rep.replace("[lastname]", lastname_display)
                        if re.fullmatch(pattern, t):
                            t = rep
                            t_norm = _in_normalize_equiv_text(t)
                            t_norm_stripped = _in_normalize_equiv_text(_in_strip_tags(t))
                            replaced_once = True
                    except Exception:
                        pass
                # regex fallback for [lastname]
                if (not replaced_once) and ("[lastname]" in old) and (lastname_display != "[lastname]"):
                    try:
                        pattern = "^" + re.escape(old).replace(
                            re.escape("[lastname]"),
                            r"(?:\[lastname\]|%s)" % re.escape(lastname_display)
                        ) + "$"
                        rep = new
                        if "[mc]" in rep:
                            rep = rep.replace("[mc]", mc_display)
                        rep = rep.replace("[lastname]", lastname_display)
                        if re.fullmatch(pattern, t):
                            t = rep
                            t_norm = _in_normalize_equiv_text(t)
                            t_norm_stripped = _in_normalize_equiv_text(_in_strip_tags(t))
                            replaced_once = True
                    except Exception:
                        pass
                # final fallback: compare strings with tags stripped (handles cases
                # where Ren'Py injects extra formatting tags before our replacer)
                if (not replaced_once) and (t_norm_stripped is not None):
                    for cand2 in candidates:
                        if not cand2:
                            continue
                        try:
                            cand_stripped = _in_normalize_equiv_text(_in_strip_tags(cand2))
                        except Exception:
                            continue
                        if cand_stripped == t_norm_stripped:
                            rep = new
                            if "[mc]" in rep:
                                rep = rep.replace("[mc]", mc_display)
                            if "[lastname]" in rep:
                                rep = rep.replace("[lastname]", lastname_display)
                            t = rep
                            t_norm = _in_normalize_equiv_text(t)
                            t_norm_stripped = _in_normalize_equiv_text(_in_strip_tags(t))
                            replaced_once = True
                            break
        except Exception:
            pass

        # 4) speaker-aware "Nancy" -> "Mom" only for MC lines
        #    Some lines intentionally keep "Nancy" for clarity.
        try:
            skip_nancy_swap = False
            try:
                if t_norm == _in_normalize_equiv_text("No, I came with Nancy, my mother."):
                    skip_nancy_swap = True
            except Exception:
                pass
            # Ensure Grandpa alias only while sister route is active
            try:
                _adad = getattr(renpy.store, 'adad', None)
                if _adad is not None and hasattr(_adad, 'name'):
                    orig_attr = '_im_adad_orig_name'
                    store = renpy.store
                    default_name = "Annie's father"
                    stored_original = getattr(store, orig_attr, None)
                    if stored_original in (None, "", "Grandpa"):
                        base_name = _adad.name
                        if not base_name or base_name == "Grandpa":
                            base_name = default_name
                        setattr(store, orig_attr, base_name)
                        stored_original = base_name

                    if getattr(store, 'annie_sister', False):
                        if _adad.name != "Grandpa":
                            _adad.name = "Grandpa"
                    else:
                        original = stored_original or default_name
                        if original and _adad.name != original:
                            _adad.name = original
            except Exception:
                pass
            who_obj, who_name = _in_current_speaker()
            if (
                _is_mc_like(who_obj, who_name)
                and not skip_nancy_swap
                and getattr(renpy.store, 'annie_mom', False)
            ):
                t = re.sub(r"\bNancy['’]s\b", "Mom's", t)  # possessive first
                t = re.sub(r"\bNancy\b", "Mom", t)
        except Exception:
            pass
        
        t = _im_strip_multimod_tags(t)
        t = _im_strip_bonusmod_tags(t)
        return t

    def _in_replace_text_callable(s: str) -> str:
        # Grab previous replacer but run it only after our replacements,
        # otherwise markup-aware filters would fire first and mutate the text
        # (removing braces), which broke matching for strings containing "{ }".
        prev = globals().get('_in_prev_replace_text_dynamic', None)

        try:
            sanitized = _im_strip_multimod_tags(s)
            sanitized = _im_strip_bonusmod_tags(sanitized)
        except Exception:
            sanitized = s
        result = _in_transform_text(sanitized)
        if callable(prev):
            try:
                result = prev(result)
            except Exception:
                pass
        elif isinstance(prev, (list, tuple)):
            for pat, rep in prev:
                try:
                    if hasattr(pat, 'sub'):
                        result = pat.sub(rep, result)
                    else:
                        result = result.replace(pat, rep)
                except Exception:
                    pass

        return result

    def _in_chat_display_text(text):
        """
        Apply incest replacements for chat message text.
        Keeps replace_text off for chat_log, chat, and
        chat_answers to avoid UI lag.
        """
        if not isinstance(text, str):
            return text
        if not _in_any_mode_active():
            return text
        if text.startswith("{image=") and text.endswith("}"):
            return text
        try:
            mc_display = renpy.substitute("[mc]")
            if not mc_display:
                mc_display = "[mc]"
        except Exception:
            mc_display = "[mc]"
        try:
            lastname_display = renpy.substitute("[lastname]")
            if not lastname_display:
                lastname_display = "[lastname]"
        except Exception:
            lastname_display = "[lastname]"

        try:
            cache = getattr(renpy.store, "_im_chatlog_cache", None)
        except Exception:
            cache = None
        if cache is None:
            cache = {}
            try:
                renpy.store._im_chatlog_cache = cache
            except Exception:
                pass

        key = (
            text,
            mc_display,
            lastname_display,
            getattr(renpy.store, 'annie_incest', False),
            getattr(renpy.store, 'annie_sister', False),
            getattr(renpy.store, 'annie_mom', False),
            getattr(renpy.store, 'annie_half_sister', False),
            getattr(renpy.store, 'annie_aunt', False),
        )
        if key in cache:
            return cache[key]

        out = _in_transform_text(text)
        if len(cache) > 5000:
            cache.clear()
        cache[key] = out
        return out

# -----------------------------------------
# Installer (define before any call)
# -----------------------------------------
init python:
    if "_in_original_replace_text" not in globals():
        base = renpy.config.replace_text
        _in_original_replace_text = None if base is _in_replace_text_callable else base

    if "_in_prev_replace_text_dynamic" not in globals():
        _in_prev_replace_text_dynamic = None

    def in_apply_text_map():
        """
        Dialogue replacements now run via say/menu filters so
        UI text remains untouched.
        """
        global _in_prev_replace_text_dynamic
        current = renpy.config.replace_text
        _in_prev_replace_text_dynamic = current

# -----------------------------------------
# Install late (after definitions exist)
# -----------------------------------------
init 990 python:
    try:
        in_apply_text_map()
    except Exception as e:
        renpy.log("in_apply_text_map() install failed: %r" % e)

# -----------------------------------------
# Ensure size-tag works in say/menu text
# -----------------------------------------
init 991 python:
    try:
        # Keep a reference to the previous filter (if any) for debugging.
        _in_prev_say_menu_filter = renpy.config.say_menu_text_filter

        def _in_allow_size_tag(text):
            """Allow common tags including {size=...} in say/menu text.

            Some builds escape unapproved tags via a filter. This wrapper
            guarantees that the 'size' tag remains active.
            """
            allowed = {
                'b', 'i', 'u', 's',
                'color', 'alpha', 'font', 'cps',
                'k', 'w', 'nw', 'p', 'br', 'rt', 'rb',
                'a',
                'size',  # crucial for this mod
            }
            try:
                sanitized = _im_strip_multimod_tags(text)
                sanitized = _im_strip_bonusmod_tags(sanitized)
            except Exception:
                sanitized = text
            try:
                transformed = _in_transform_text(sanitized)
            except Exception:
                transformed = sanitized
            try:
                # Use Ren'Py's sanitizer but with our allowlist (incl. size).
                return renpy.filter_text_tags(transformed, allow=allowed)
            except Exception:
                # Fallback: return text unchanged if something goes wrong.
                return transformed

        renpy.config.say_menu_text_filter = _in_allow_size_tag
    except Exception as e:
        renpy.log("annie say/menu filter install failed: %r" % e)

# -----------------------------------------
# Opt-in menu for flags
# -----------------------------------------
label annie_incest_optin:
    menu:
        "Select Incest mode:"
        "Disabled":
            $ annie_incest = False
            $ annie_sister = False
            $ annie_mom = False
            $ annie_half_sister = False
            $ annie_aunt = False
            $ persistent.im_incest_mode = "off"
        "I only want Nancy as Mom":
            $ annie_incest = False
            $ annie_sister = False
            $ annie_mom = True
            $ annie_half_sister = False
            $ annie_aunt = False
            $ persistent.im_incest_mode = "mom"
        "I only want Annie as a sister (coming soon)":
            $ annie_incest = False
            $ annie_sister = True
            $ annie_mom = False
            $ annie_half_sister = False
            $ annie_aunt = False
            $ persistent.im_incest_mode = "sister"
        "Nancy as Mom and Annie as half-sister":
            $ annie_incest = False
            $ annie_sister = False
            $ annie_mom = True
            $ annie_half_sister = True
            $ annie_aunt = False
            $ persistent.im_incest_mode = "half"
        "Nancy as aunt and Annie as stepsister (coming soon maybe)":
            $ annie_incest = False
            $ annie_sister = False
            $ annie_mom = False
            $ annie_half_sister = False
            $ annie_aunt = True
            $ persistent.im_incest_mode = "aunt"
        "Full Incest (Nancy as Mom and Annie as sister)":
            $ annie_incest = True
            $ annie_sister = True
            $ annie_mom = True
            $ annie_half_sister = False
            $ annie_aunt = False
            $ persistent.im_incest_mode = "incest"
    # menu:
    #     "Do you want a cousin?"
    #     "Yes":
    #         $ im_cousin_override = True
    #         $ persistent.im_cousin_override = True
    #     "No":
    #         $ im_cousin_override = False
    #         $ persistent.im_cousin_override = False
    # After flags change, refresh label overrides immediately
    $ im_apply_label_map()
    $ in_apply_text_map()
    $ _in_incest_prompted = True
    return

# -----------------------------------------
# Re-apply after loading
# -----------------------------------------
label after_load:
    $ in_apply_text_map()
    $ _im_update_checked = False
    $ _im_check_for_update()
    return

# -----------------------------------------
# Autocall screen
# -----------------------------------------
init python:
    def _in_trigger_optin():
        try:
            renpy.hide_screen("_in_incest_autocall")
        except Exception:
            pass
        # NEU: Stelle sicher, dass alle UI-Widgets geschlossen sind
        try:
            # Schließe alle offenen UI-Kontexte
            _stack = getattr(renpy.ui, "stack", None)
            if _stack:
                while len(_stack) > 1:
                    try:
                        renpy.ui.close()
                    except Exception:
                        break
        except Exception:
            pass
        renpy.call_in_new_context('annie_incest_optin')

# Und ändere den Auto-Call-Screen:
screen _in_incest_autocall():
    # Füge eine zusätzliche Bedingung hinzu
    if (
        (not _in_incest_prompted)
        and (renpy.get_screen('choice') is None)
        and (not renpy.context()._main_menu)
        and (not _im_reloading_scripts)
        # NEU: Prüfe ob URM aktiv ist
        and (renpy.get_screen('URM') is None)  
    ):
        # Erhöhe die Verzögerung
        timer 0.1 action Function(_in_trigger_optin)

init -1 python:
    if "_in_incest_autocall" not in config.overlay_screens:
        config.overlay_screens.append("_in_incest_autocall")

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
                if len(renpy.known_languages()) > 0:
                    vbox:
                        style_prefix "radio"
                        label _("Language")
                        textbutton _("English{#prefs}"):
                            action Language(None)
                        for lang in renpy.known_languages():
                            if "incest" in lang:
                                $ incest_translation = True
                            else:
                                $ option_title = language_titles.get(lang, lang)
                                $ option_font = language_title_fonts.get(lang, None)
                                textbutton option_title:
                                    action Language(lang)
                                    if option_font is not None:
                                        text_font option_font
                    if incest_translation:
                        vbox:
                            style_prefix "radio"
                            label _("Incest Mode")
                            for lang in renpy.known_languages():
                                if "incest" in lang:
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
                    textbutton _("Full Incest"):
                        action [
                            SetVariable("annie_incest", True),
                            SetVariable("annie_sister", True),
                            SetVariable("annie_mom", True),
                            SetVariable("annie_half_sister", False),
                            SetVariable("annie_aunt", False),
                            SetVariable("_in_incest_prompted", True),
                            SetVariable("persistent.im_incest_mode", "incest"),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected annie_incest
                    textbutton _("Nancy as Mom"):
                        action [
                            SetVariable("annie_incest", False),
                            SetVariable("annie_sister", False),
                            SetVariable("annie_mom", True),
                            SetVariable("annie_half_sister", False),
                            SetVariable("annie_aunt", False),
                            SetVariable("_in_incest_prompted", True),
                            SetVariable("persistent.im_incest_mode", "mom"),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected (not annie_incest and annie_mom and not annie_sister and not annie_half_sister)
                    textbutton _("Sister"):
                        action [
                            SetVariable("annie_incest", False),
                            SetVariable("annie_sister", True),
                            SetVariable("annie_mom", False),
                            SetVariable("annie_half_sister", False),
                            SetVariable("annie_aunt", False),
                            SetVariable("_in_incest_prompted", True),
                            SetVariable("persistent.im_incest_mode", "sister"),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected (not annie_incest and not annie_mom and annie_sister)
                    textbutton _("Half-Sister"):
                        action [
                            SetVariable("annie_incest", False),
                            SetVariable("annie_sister", False),
                            SetVariable("annie_mom", True),
                            SetVariable("annie_half_sister", True),
                            SetVariable("annie_aunt", False),
                            SetVariable("_in_incest_prompted", True),
                            SetVariable("persistent.im_incest_mode", "half"),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected (annie_mom and annie_half_sister)
                    textbutton _("Aunt"):
                        action [
                            SetVariable("annie_incest", False),
                            SetVariable("annie_sister", False),
                            SetVariable("annie_mom", False),
                            SetVariable("annie_half_sister", False),
                            SetVariable("annie_aunt", True),
                            SetVariable("_in_incest_prompted", True),
                            SetVariable("persistent.im_incest_mode", "aunt"),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected annie_aunt
                    textbutton _("Disabled"):
                        action [
                            SetVariable("annie_incest", False),
                            SetVariable("annie_sister", False),
                            SetVariable("annie_mom", False),
                            SetVariable("annie_half_sister", False),
                            SetVariable("annie_aunt", False),
                            SetVariable("_in_incest_prompted", True),
                            SetVariable("persistent.im_incest_mode", "off"),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected (not annie_incest and not annie_sister and not annie_mom and not annie_half_sister and not annie_aunt)

                # vbox:
                #     style_prefix "radio"
                #     label _("Cousin Mode")
                #     textbutton _("Enabled"):
                #         action [
                #             SetVariable("im_cousin_override", True),
                #             SetVariable("persistent.im_cousin_override", True),
                #             Function(in_apply_text_map),
                #         ]
                #         selected im_cousin_override
                #     textbutton _("Disabled"):
                #         action [
                #             SetVariable("im_cousin_override", False),
                #             SetVariable("persistent.im_cousin_override", False),
                #             Function(in_apply_text_map),
                #         ]
                #         selected (not im_cousin_override)

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

# -----------------------------------------
# Bonus Mod chat_log, chat, chat_answers override (Incest-aware, no global replace_text)
# -----------------------------------------
init 1100:
    screen chat_log(girl_chats):
        modal True
        style_prefix "chat"
        key 'pad_b_press' action Hide("chat_log")
        key 'b' action Hide("chat_log")

        default back_button_size = 50
        default header_height = 100

        default chat_x_padding = 20

        default msg_padding = 25
        default msg_top_padding = 32

        frame:
            style "phone_frame"
            at phone_app

            add "phone/images/wallpapers/{}.jpg".format(store.current_wallpaper['name']) yoffset top_bar_height blur 50

            vbox:
                xfill True
                ysize phone_height
                spacing 10
                    
                frame:
                    background "#000" # "#fff"
                    has hbox
                    xfill True

                    imagebutton:
                        xysize (back_button_size, back_button_size)
                        xoffset back_button_size / 2
                        xalign 0.0
                        yalign 0.5
                        idle Transform("phone/images/back_arrow2.webp", fit="contain")
                        action Hide("chat_log")

                    text list(girl_chats.values())[-1]['npc']:
                        xalign 0.5
                        yalign 0.5
                        style_prefix "normal"
                        outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]


                    imagebutton:
                        xalign 1.0
                        yalign 0.5
                        idle Transform(list(girl_chats.values())[-1]['thumbnail'], crop=(thumbnail_width - thumbnail_height, 0, thumbnail_height, thumbnail_height), fit="contain", xsize=100, ysize=100)

                viewport:
                    yfill True    
                    xsize (phone_width - chat_x_padding)
                    xalign 0.5

                    draggable True
                    mousewheel True
                    
                    vbox:
                        xfill True
                        spacing 10
                        $ print(girl_chats.items())
                        for index, chat_info in girl_chats.items():
                            text "Chat {}".format(index): # TODO Check translation
                                color "#fff"
                                outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]

                            for message in chat_info['messages']:
                                # Adapted from "screen chat()" in chats.rpy
                                vbox:
                                    at message_popup

                                    if message.who == "mc":
                                        xalign 1.0

                                    frame:
                                        yalign 0.5
                                        padding (msg_padding, msg_top_padding, msg_padding, msg_padding)

                                        if message.who == "npc":
                                            # White background for NPCs
                                            background Frame("chat_npc_background",17,17,17,17)
                                        else:
                                            # Blue background for MC
                                            background Frame("chat_mc_background",17,17,17,17)

                                        vbox:
                                            xminimum 200
                                            xmaximum 400

                                            # Handle Buu meme from 0.8 because idgaf
                                            if message.text == "{image=images/08/buumeme.jpg}":
                                                $ picture = message.text.replace("}", "").split("=")[-1]
                                                imagebutton:
                                                    xalign 0.5
                                                    idle Transform(picture, fit="contain", xsize=(phone_width - msg_padding * 2 - chat_x_padding), matrixcolor=None)
                                                    hover Transform(picture, fit="contain", xsize=(phone_width - msg_padding * 2 - chat_x_padding), matrixcolor=BrightnessMatrix(0.2)) 
                                                    action Show("show_pic", pic=picture)
                                            else:
                                                text _in_chat_display_text(message.text)

                                                if message.picture is not None:
                                                    imagebutton:
                                                        xalign 0.5
                                                        idle Transform(message.picture, fit="contain", xsize=(phone_width - msg_padding * 2 - chat_x_padding), matrixcolor=None)
                                                        hover Transform(message.picture, fit="contain", xsize=(phone_width - msg_padding * 2 - chat_x_padding), matrixcolor=BrightnessMatrix(0.2)) 
                                                        action Show("show_pic", pic=message.picture)

                                    if message.who == "npc":
                                        add "chat_npc_background_tip" 
                                    else:
                                        add "chat_mc_background_tip" xalign 1.0

    screen chat():
        style_prefix "chat"

        #
        # Background image fullscreen
        #
        add current_chat["background"]

        frame:
            style "empty"
            #
            # White transparent background under the messages
            #
            background Frame("chat_background_messages", 60, 60, 60, 60)
            xysize (1120, 930)
            pos (50, 85)

            viewport yadjustment chat_yadj:
                pos (60, 150)
                xsize 1000
                ymaximum 740
                mousewheel True
                draggable True

                vbox:
                    xsize 1000
                    spacing 10

                    for msg in [ current_chat[key] for key in chat_history]:

                        if len(msg.text) > 0:
                            vbox:
                                at message_popup
                                if msg.who == "mc":
                                    # MC's message are aligned on the right
                                    xalign 1.0

                                frame:
                                    yalign 0.5
                                    padding (25, 32, 25, 25)
                                    if msg.who == "npc":
                                        # White background for NPCs
                                        background Frame("chat_npc_background",17,17,17,17)
                                    else:
                                        # Blue background fo MC
                                        background Frame("chat_mc_background",17,17,17,17)

                                    vbox:
                                        xminimum 500
                                        xmaximum 707

                                        text _in_chat_display_text(msg.text)

                                        if msg.picture is not None:
                                            #
                                            # Display a picture in the message
                                            #
                                            imagebutton:
                                                xalign 0.5
                                                idle Transform(msg.picture, zoom=0.2)
                                                hover Transform(msg.picture, zoom=0.2, matrixcolor=BrightnessMatrix(0.2))
                                                action Show("show_pic", pic=msg.picture)

                                if msg.who == "npc":
                                    add "chat_npc_background_tip"
                                else:
                                    add "chat_mc_background_tip" xalign 1.0


        #
        # NPC thumbnail in the top left corner
        #
        add current_chat["thumbnail"]

    screen chat_answers():
        vbox:
            at answers_dissolve
            xpos 1200
            yalign 0.5
            spacing 15

            for key, msg in [ (key, current_chat[key]) for key in current_chat[chat_step].replies ]:
                if msg.is_valid():
                    vbox:
                        button:
                            padding (0, 0, 0, 0)
                            action [ Function(chat_next_step, step=key), Return() ]

                            frame:
                                xsize 700
                                padding (25, 32, 25, 25)
                                background Frame("chat_mc_background",17,17,17,17)

                                vbox:
                                    xalign 0.5

                                    text _(_in_chat_display_text(msg.text)):
                                        style "chat_button_text"
                                        if renpy.loadable("achievements/achievements.rpy"):
                                            if msg.type == "points":
                                                idle_color walk_points_chat
                                            elif msg.type == "path":
                                                idle_color walk_path_chat
                                        xalign 0.5

                                    if msg.picture is not None:
                                        #
                                        # Display a picture in the message
                                        #
                                        add Transform(msg.picture, zoom=0.2) xalign 0.5

                        add "chat_mc_background_tip" xalign 1.0
# ==========================
# Annie Opt-In (FIXED SKELETON)
# - Replacement order fixed
# - Handles [mc] placeholder vs. resolved name
# - Speaker-aware "Nancy" -> "Mom" only for MC lines
# ==========================

default im_incest_mode = None
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
default persistent.text_offset = 1
# Mod update metadata (Step 1)
default persistent.im_mod_version = "1.4.2.0"
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

    def _im_sync_adad_alias():
        """
        Ensure Annie's dad NPC uses the correct alias for the active mode
        and restore the original name when incest modes are disabled.
        """
        try:
            store = renpy.store
            _adad = getattr(store, "adad", None)
            if _adad is None or not hasattr(_adad, "name"):
                return
            orig_attr = "_im_adad_orig_name"
            default_name = "Annie's father"
            stored_original = getattr(store, orig_attr, None)
            if stored_original in (None, "", "Grandpa", "Annie's Uncle"):
                base_name = getattr(_adad, "name", None)
                if not base_name or base_name in ("Grandpa", "Annie's Uncle"):
                    base_name = default_name
                setattr(store, orig_attr, base_name)
                stored_original = base_name

            if getattr(store, "annie_sister", False):
                target_name = "Grandpa"
            elif getattr(store, "annie_half_sister", False):
                target_name = "Annie's Uncle"
            else:
                target_name = stored_original or default_name

            if _adad.name != target_name:
                _adad.name = target_name
        except Exception:
            pass

    def _im_apply_incest_mode():
        mode = getattr(store, "im_incest_mode", None)
        # store.im_cousin_override = bool(getattr(persistent, "im_cousin_override", False))
        if mode == "incest":
            store.annie_incest = True
            store.annie_sister = True
            store.annie_mom = True
            store.annie_half_sister = False
            store.annie_aunt = False
        elif mode == "mom":
            store.annie_incest = False
            store.annie_sister = False
            store.annie_mom = True
            store.annie_half_sister = False
            store.annie_aunt = False
        elif mode == "sister":
            store.annie_incest = False
            store.annie_sister = True
            store.annie_mom = False
            store.annie_half_sister = False
            store.annie_aunt = False
        elif mode == "half":
            store.annie_incest = False
            store.annie_sister = False
            store.annie_mom = True
            store.annie_half_sister = True
            store.annie_aunt = False
        elif mode == "aunt":
            store.annie_incest = False
            store.annie_sister = False
            store.annie_mom = False
            store.annie_half_sister = False
            store.annie_aunt = True
        elif mode == "off":
            store.annie_incest = False
            store.annie_sister = False
            store.annie_mom = False
            store.annie_half_sister = False
            store.annie_aunt = False
        _im_sync_adad_alias()
        try:
            refresh = getattr(store, "icmod_refresh_chat_last_names", None)
            if refresh:
                refresh(mode)
        except Exception:
            pass

    try:
        _im_apply_incest_mode()
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
        "_call_chat_18": "mod_call_chat_18",
        "menurestaurant":"menurestaurant_mod",
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
        # formerly known as base map
        # Nancy as Mom, Penny and Dalia as older sisters
        # They have the same last name as MC
        # -----------------------------------------
        # BM 0000 = Base Map, Line Number
        # Line numbers based on compiled script from v0.9.0, subject to change in future updates
        #    (which already happened in v0.9.4 fml, need to redo)
        # -----------------------------------------
        # BM script:0000 = Base Map, RPY file:Line Number
        #     Numbers based on v0.9.5, subject to change in future updates
        #     slowly adapting line numbers to this format
        # LW/N = Lucifer_W's notes
        # l9/N = l9453394's notes
        # BA/N = BlueArrow's notes
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

        # BM 961
        # LW/N: FIXED: Handle both "Nancy" and "Mom" versions
        "(Nancy used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(My mom used to look after me and my sisters in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)",

        # BM 961
        "(Mom used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(My mom used to look after me and my sisters in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)",

        # BM 962
        # LW/N: FIXED: Handle both versions
        "(I used to spend the entire afternoon playing with Nancy and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend the entire afternoon playing with Mom and my sister Dalia, but then we had to move and ended up losing touch.)",

        # BM 962
        "(I used to spend the entire afternoon playing with Mom and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend the entire afternoon playing with Mom and my sister Dalia, but then we had to move and ended up losing touch.)",

        # BM 964
        # LW/N: FIXED: Handle both versions
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

        # BM 1643 minor grammar change
        "It’s me, Nancy! Even though we’ve only been speaking on the phone for the past few days, I feel like we’ve been becoming good friends already! Isn't that right, Annie?":
            "It's me, Nancy! Even though we've only been speaking on the phone for the past few days, I feel like we're becoming good friends already! Isn't that right, Annie?",

        # BM 1655
        # BA/N: lines are identical?
        "I hope so! And please, just call me Nancy!":
            "I hope so! And please, just call me Nancy!",

        # BM 1657
        # BA/N: lines are identical?
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

        # BM script:1842
        "(Nancy used to pick me up after school and we'd come here.)":
            "(The blissful, carefree days of my childhood–especially once school was done!)",

        # BM 1719
        "(Each day I would spend the afternoon playing with her and Dalia. We had dinner every night at eight, and then Nancy drove me home once it got late.)":
            "(My afternoons were spent playing with Mom and Dalia. We had dinner every night at eight, and then went to bed.)",

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

        # BM 2015
        # LW/N: FIXED: Handle both "Nancy" and "Mom" versions
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

        # BM 2307
        # BA/N: lines are identical?
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

        # BM 5083
        # BA/N: lines are identical?
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

        # BM 5478
        # BA/N: lines are identical?
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

        # BM 14627
        # BA/N: lines are identical?
        "You know, maybe Nancy would also hear more compliments if she ever left her lab!":
            "You know, maybe Nancy would also hear more compliments if she ever left her lab!",

        # BM 14659
        # BA/N: lines are identical?
        "And of course... my beautiful little dove, Nancy.":
            "And of course... my beautiful little dove, Nancy.",

        # BM 14661
        # BA/N: lines are identical?
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

        # BM 14704
        # BA/N: lines are identical?
        "Perfect, Nancy... your graceful movements are simply unmatched...":
            "Perfect, Nancy... your graceful movements are simply unmatched...",

        # BM 14723
        # BA/N: lines are identical?
        "Our last movement will be an Acro pose and must be done in pairs. So... Raul should go with Noah, [mc] with Gertrude, and... oh! I guess that leaves me with you, Nancy.":
            "Our last movement will be an Acro pose and must be done in pairs. So... Raul should go with Noah, [mc] with Gertrude, and... oh! I guess that leaves me with you, Nancy.",

        # BM 14733
        "I mean, obviously Kai would've asked me out if I wasn't already married, but since I'm happily taken... Nancy will be a very good fit for him.":
            "I mean, obviously Kai would've asked me out if I wasn't already married, but since I'm happily taken... your mom will be a very good fit for him.",

        # BM 14864
        "Look at that perfectly toned stomach... And to think she's had 2 daughters! Unbelievable.":
            "Look at that perfectly toned stomach... And to think she's had 3 children! Unbelievable.",

        # BM 14969
        "*Giggles* Just like when I was your babysitter.":
            "*Giggles* Just like when you were still living with us.",

        # BM 15027
        # BA/N: lines are identical?
        "*Breathing heavily* I'm... so relieved... you didn't leave yet, Nancy.":
            "*Breathing heavily* I'm... so relieved... you didn't leave yet, Nancy.",

        # BM 15067
        # BA/N: lines are identical?
        "What? That's absurd! You're a goddess, Nancy! You're a modern day Aphrodite!":
            "What? That's absurd! You're a goddess, Nancy! You're a modern day Aphrodite!",

        # BM 15098
        # BA/N: lines are identical?
        "Nancy, sex is a beautiful part of life. If you have needs, you need to be taken care of. You deserve to be pampered... desired... lusted after. Even more so with you being such a beautiful woman.":
            "Nancy, sex is a beautiful part of life. If you have needs, you need to be taken care of. You deserve to be pampered... desired... lusted after. Even more so with you being such a beautiful woman.",

        # BM 15133
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

        # BM 18180
        # BA/N: moved from half-sis map
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

        # BM 24386
        # BA/N: lines are identical?
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

        # BM 29268
        # BA/N: might want to rewrite lines around this one
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

        # BM 29386 
        # BA/N: might need tweaking
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

        # BM 33152
        # BA/N: tbh a few more lines here could use work
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

        # BM 37504, 
        # BA/N: Disabled, bro does not work here
        # "“We” have a party? Who’s “we”? You and [mc]?":
        #     "“We” have a party? Who’s “we”? You and bro?",

        # BM 37507 
        # BA/N: Disabled, bro does not work here
        # "Yeah, Nova, [mc], and I are going to a party on campus. I could have sworn I told you about it...":
        #     "Yeah, Nova, bro, and I are going to a party on campus. I could have sworn I told you about it...",

        # BM 37522
        "What other people? You? Mom? Annie? I'm sure [mc] doesn't mind either. He's like... family. Like a little brother, almost.":
            "What other people? You? Mom? Annie? I'm sure [mc] doesn't mind either. He's... family. Our little brother...",

        # BM 37525
        "Yeah... like a little brother...":
            "Yeah... our little brother...",

        # BM 37528 
        # BA/N: should rewrite
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

        # BA/N: Entire truth and dare needs more work imo but I dont have any good ideas

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

        # BM 49310
        # Disabled, interferes with other lines, also doesn't work if not on other paths
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

        # BM 51640
        "I can't be fired, [mc], I have a family to feed!":
            "I can't be fired, [mc], I have our family to feed!",

        # BM 51781
        "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters would take the news.":
            "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how your sisters would take the news.",

        # BM 52082
        "I kept a mask on because I was afraid that it would scare or hurt my daughters.":
            "I kept a mask on because I was afraid that it would scare or hurt Penny and Dalia.",

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

        # BA/N: feel like Fuck Marry Kill game could use some rewrites but not really sure what to do for it

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

        # BM 69705 (menu)
        "She's not my wife":
            "She's my sister",

        # BM 69706
        "Uhh... well, she's not my wife, but... alright, let's do it.":
            "Uhh... well, she's actually my sister, but... alright, let's do it.",

        # BM 69710 (menu)
        # l9/N: Changed to be fully compatible with and without either walkthrough
        # BA/N: Disabled, reverted back to original text upon suggestion
        # "She's not my wife, yet":
        #     "{color=[walk_points]}She's my sister... [penelope_pts]",

        # BM 69711
        # BA/N: Disabled, upon suggestion
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

        # BM 74914
        # BA/N: should rework
        "Well, I know, but didn't you practically grow up around him?":
            "Oh really? I didn't know that.",

        # BM 74915
        # BA/N: ditto
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

        # BM 76766
        "*Whispering* Oh, Penny...":
            "*Whispering* Oh, sis...",

        # BM 77058 phone chat (penelope_chat4)
        "I'm proud of my hot sissy":
            "I'm proud of our hot sissy",

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

        # BM script8:2058
        "NANCY!":
            "MOM!",

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

        # BM script8:6983
        # BA/N: leaving this here for the future when we learn what exactly Luna's vision was
        # "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)":
        #     "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)",

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

        # BM 92734
        # BA/N: Added bc relation was never mentioned around Jerry, if I missed it than need to redo this line
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

        # BM 96097
        "*Panting* That the childhood friend I used to p-play with would end up ramming her p-perfect, huge ass down on my cock...":
            "*Panting* That my sister would end up ramming her p-perfect, huge ass down on my cock...",

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

        # BM script8:15862
        "Well, I don't know, then I just thank my mom for making me the way I am.":
            "Well, I don't know, then I just thank Mom for making me the way I am.",

        # BM 96729
        "(Hmm, yeah.)":
            "(Imagine her face if I tell her it was with my brother.)",

        # BM 96732
        "(Or maybe Sissy too...?)":
            "(Sissy would freak out if she knew...)",


    # -----------------------------------------
    # v0.9 script9.rpy Lines

        # BM script9:267
        "OH! Is it...":
            "Hmmm, how many other boys do you know...",

        # BM script9:268
        "*Giggles* Is it [mc]...?":
            "*Giggles* Can't be [mc]...",

        # BM script9:270
        "I-I don't...":
            "What!? Of-f course not... I-I mean...{w} {size=*0.75}he's my–{/size}{w} {size=*0.6}he's our...{/size}",

        # BM script9:287
        "YOU'RE IN LOVE WITH [mc!u]?!":
            "YOU'RE IN LOVE WITH OUR BROTHER?!",

        # BM script9:296
        "I literally asked you a couple of weeks ago and you said “you’d rather live off salads for a year”!":
            "He's our little brother! Our actual, {i}blood-related brother!{/i}",

        # BM script9:298
        "Oh... well, yeah...":
            "You think I'm not aware of that?",

        # BA/N: next 4 lines still feel a bit clunky imo

        # BM script9:299
        "A-About that...":
            "It's just, ever since [mc] came back, everything's been so...",

        # BM script9:300
        "I was... confused.":
            " Different. Better even. And... confusing.",

        # BM script9:302
        "Confused??":
            "Confusing??",

        # BM script9:304
        "Yes, confused.":
            "What else am I supposed to think? I know this is wrong!",

        # BM script9:311
        "What?! Hah! Me?! Pfft!":
            "What?! Hah! Me?! With our {i}brother?{/i} Pfft!",

        # BM script9:314
        # "You've been hovering around him like a fly lately!":
        #     "text",

        # BM script9:316
        "W-We've all been hovering around him lately.":
            "N-Not any more than the other girls do... I'm just doting on him as a big sister!",

        # BM script9:319
        "But certain blondes have been a little more... hover-y, I think.":
            "You've been quite clingy for a \"big sister\"...",

        # BM script9:323
        # "Wait, hold your horses, how did you turn this around on me?":
        #    "text",

        # BM script9:324
        # "Why are you acting like a jealous girlfriend all of a sudden?!":
        #     "text",

        # BM script9:383
        "You just can't let me have anything, can you?!":
            "You just can't let me have anything, can you?! Not even my own brother!",

        # BM script9:388
        "But I didn't fucking know??!":
            "And you had the nerve to chastise {i}me{/i} about incest?!",

        # BM script9:390
        "Oh, but I was supposed to know about you two??":
            "What, was I supposed to pretend this is all normal? You know it's not!",

        # BM script9:392
        #"You're so damn... selfish!":
        #    "text",

        # BM script9:436
        "*Grumbling to herself* My goddamn sister?!":
            "*Grumbling to herself* His other goddamn sister, too?!",

        # BM script9:439
        "*Grumbling to herself* Why didn't she tell me?!":
            "*Grumbling to herself* I thought we trusted each other more than this... Like... I get this is a huge taboo...",

        # BM script9:440
        "*Grumbling to herself* Like... I get it, we're all living crazy fucking lives, I know we've all got a million things going on and enough shit to worry about.":
            "*Grumbling to herself* And on top of that, we're all living crazy enough lives, I know we've all got a million things going on and enough shit to worry about.",

        # BM script9:441
        # "*Grumbling to herself* I get that realizing everything we thought was real could crumble is hard to digest... but still...":
        #    "text",

        # BM script9:446
        "I’D STILL HAVE APPRECIATED IT IF MY SISTER HAD TOLD ME SHE WAS SCREWING MY FUCKING BOYFRIEND!":
            "I’D STILL HAVE APPRECIATED IT IF MY SISTER HAD TOLD ME SHE WAS SCREWING MY FUCKING BROTHER!",

        # BM script9:448
        "Oh, so he's {i}your{/i} boyfriend now.":
            "As if I'm the {i}only{/i} one here screwing her brother.",

        # BM script9:449
        "You do realize you could've told me too, right?":
            "Something {i}you{/i} could've told me too, right?",

        # BM script9:450
        "Or is that not your fault either?!":
            "Or was that a special secret only for you to keep?!",

        # BM script9:488
        "Let's make him choose!":
            "Let's make him choose which {i}sister{/i} he wants!",

        # BM script9:510
        # BA/N: Disabled, consistency with below plus they're both mad at MC so calling him by name feels more appropriate
        # "{sc=3}[mc!u]!!{/sc}":
        #     "{sc=3}BRO!!{/sc}",

        # BM script9:511
        # Disabled, interferes with other lines
        # "{sc=3}[mc!u]!!!{/sc}":
        #     "{sc=3}BRO!!!{/sc}",

        # BM script9:2339
        "Last thing [mc] would want is for you to get hurt looking for him.":
            "Last thing your brother would want is for you to get hurt looking for him.",

        # BM script9:3016
        "His only family is a drunk skunk of a father living an ocean away.":
            "His only other family is a drunk skunk of a father living an ocean away.",

        # BA/N: I added next three lines during  Hyril'ar but idk if I want to keep them lel

        # BM script9:3842
        "[mc], however, appears to possess a magnetic pull, both physical and, I daresay, emotional, that draws multiple females to him alone.":
            "[mc], however, appears to possess a magnetic pull, both physical and, I daresay, emotional, that draws multiple females to him alone. Not even his own blood is exempt.",

        # BM script9:3844
        "Astounding...":
            "Even his relatives? Astounding...",

        # BM script9:4234
        "Among them is a woman named Dalia, who is just as strong, if not stronger than he is in close combat.":
            "Among them is a woman named Dalia, one of his elder sisters, who is just as strong, if not stronger than he is in close combat.",

        # BM script9:9955
        "As for me, I’m spending Christmas Eve with Nancy, Penny, Dalia, and Alex. Even though... Alex doesn't know yet. It's a surprise.":
            "As for me, I’m spending Christmas Eve with my family and Alex. Although... Alex doesn't know yet. It's a surprise.",

        # BM script9:10117
        "Last Christmas, I had a cold kebab in the kitchen while my dad passed out on the couch in the middle of his tenth beer.":
            "Last Christmas, I had a cold kebab in the kitchen while Dad passed out on the couch in the middle of his tenth beer.",

        # BM script9:10414
        "*Chuckles* Damn, I didn't know you were this into Christmas, Penny.":
            "*Chuckles* Damn, I almost forgot how into Christmas you are, sis.",

        # BM script9:10423
        "Honestly, I’d probably feel the same if I hadn’t grown up with my dad.":
            "Honestly, I’d probably still feel the same if I hadn’t grown up with Dad.",

        # BM script9:10424
        "Christmas never felt special to me.":
            "We never celebrated it in the UK, so Christmas stopped feeling special.",

        # BM script9:10876
        "You've been hiding so many secrets from me, missy.":
            "You've been hiding so many secrets from me, sissy.",

        # BM script9:10498
        "*Starts reading* {i}Dear Ms. Carter, thank you for booking my humble property for this year’s Christmas Eve.":
            "*Starts reading* {i}Dear Ms. [lastname], thank you for booking my humble property for this year’s Christmas Eve.",

        # BM script9:10877
        "I don't remember you being one when I still lived in Kredon.":
            "I don't remember you being one when I still lived with you.",

        # BM script9:11096
        "*Chuckles* You were quick, Penny. Snagged the best room in the whole place before anyone else, eh?":
            "*Chuckles* You were quick, sis. Snagged the best room in the whole place before anyone else, eh?",

        # BM script9:11121
        "I don't know about the other swimsuits you brought, but this bikini is doing things to me, Penny.":
            "I don't know about the other swimsuits you brought, but this bikini is doing things to me, sis.",

        # BM script9:11306
        "But I fucking swear to you, Penelope — I love you.":
            "But I fucking swear to you, Penelope — I love you. And I mean not as a sister... as a woman!",

        # BM script9:11563
        "I suspected.":
            "I suspected she knew something was going on. Hard for anything to escape her notice in this house.",

        # BM script9:11564
        "But thanks for confirming it.":
            "Which begs the question of what exactly she thinks of all this...{p}But thanks for confirming it.",

        # BM script9:11613
        "I mean, it’s 2034. This probably isn’t the freakiest thing you’ll see on the street nowadays.":
            "I mean, it’s 2034. This probably isn’t the freakiest thing you’ll see on the street nowadays. And we are {i}way{/i} past the whole incest thing so...",

        # BM script9:11703
        "Haven't you seen my mom? She’s almost twenty years older than me, and hers are still as firm as a twenty-year-old’s.":
            "Haven't you seen Mom? She’s almost twenty years older than me, and hers are still as firm as a twenty-year-old’s.",

        # BM script9:11704
        "Genetics are on my side, [mc].":
            "Genetics are on my side, bro.",

        # BM script9:11756
        "Time to put all those thousands of hours playing RPGs to good use and impress your girl.":
            "Time to put all those thousands of hours playing RPGs to good use and impress your big sis.",

        # BM script9:11946
        "Mmm, I don't know, Penny...":
            "Mmm, I don't know, sis...",

        # BM script9:11984
        "*Squeezing her tits* Oh, fuck, Penny...":
            "*Squeezing her tits* Oh, fuck, sis...",

        # BM script9:12008
        "W-When are you gonna... take that picture, [mc]...?":
            "W-When are you gonna... take that picture, bro...?",

        # BM script9:12033
        "*Squeezing her breasts together* O-Oh, Penny...":
            "*Squeezing her breasts together* O-Oh, sis...",

        # BM script9:12089
        "You should learn to savor the moment, [mc]...":
            "You should learn to savor the moment, bro...",

        # BM script9:12109, but also script7:9372, script9:12363 (no negative effect)
        "Oh, Penny...":
            "Oh, sis...",

        # BM script9:12117
        "*Giggles* You’re not secretly recording me, right? Taking advantage of little old blind Penny...?":
            "*Giggles* You’re not secretly recording me, right? Taking advantage of your big blind sister...?",

        # BM script9:12143
        "Take it all, Penny...":
            "Take it all, sis...",

        # BM script9:12160
        "Your moans are turning shameless, Penny...":
            "Your moans are turning shameless, sis...",

        # BM script9:12212
        "Finally got too horny, eh, Penny? Or maybe... you just love being on the submissive side?":
            "Finally got too horny, eh, sis? Or maybe... you just love being on the submissive side?",

        # BM script9:12215
        "Please... [mc]...":
            "Please... bro...",

        # BM script9:12218 (menu)
        "Make her call you something different":
            "Make her call you something different (use \"Other\" for bro)",

        # BM script9:12232 (menu)
        "No nickname":
            "Make her use your name",

        # BM script9:12234
        "What do we say...?":
            "Say my name...",

        # BM script9:12244
        "It doesn't matter how many times I see you like this, Penny... you still leave me breathless.":
            "It doesn't matter how many times I see you like this, sis... you still leave me breathless.",

        # BM script9:12303
        "I've said it before, and I'll say it again, Penny — your ass is criminally underrated...":
            "I've said it before, and I'll say it again, sis — your ass is criminally underrated...",

        # BM script9:12341
        "You're choking my cock, Penny...":
            "You're choking my cock, sis...",

        # BM script9:12363
        # Overwritten by BM script9:12109, okay

        # BM script9:12426
        "You're just too much, Penny...":
            "You're just too much, sis...",

        # BM script9:12459
        "Hey... can I... a-ask you something, [mc]?":
            "Hey... can I... a-ask you something, bro?",

        # BM script9:12519 (menu)
        "Have anal sex with Penny":
            "{color=[walk_points]}Have anal sex with your big sister [gr][mt](Anal)",

        # BA/N: temp fix for multi-mod tags not being stripped
        "Have anal sex with Penny [gr][mt](Anal)":
            "{color=[walk_points]}Have anal sex with your big sister [gr][mt](Anal)",

        # BM script9:12535
        "I’ll remember it next time, Penny... word for word.":
            "I’ll remember it next time, sis... word for word.",

        # BM script9:12570
        "Last chance to back out, Penny...":
            "Last chance to back out, sis...",

        # BM script9:12614
        "Oh... fuck Penny, this gets dry so quickly...":
            "Oh... fuck sis, this gets dry so quickly...",

        # BM script9:12638
        "Ohhh Penny... you’re gonna make me lose my f-fucking mind...":
            "Ohhh sis... you’re gonna make me lose my f-fucking mind...",

        # BM script9:12706
        "My god, Penny...":
            "My god, sis...",

        # BM script9:12870
        "I’ve never had a Christmas dinner like this before, Nan.":
            "I’ve never had a Christmas dinner like this before, Mom.",

        # BM script9:12988
        "I swear on my life, they're delicious.":
            "I swear on my life, sis, they're delicious.",

        # BM script9:13081
        "*Chuckles* (Penelope Paige Carter...)":
            "*Chuckles* (Penelope Paige [lastname]...)",

        # BM script9:13164
        "Up until this past year, Christmas didn’t mean shit to me. It was just an excuse to slack off, sleep in, and play games until my eyes burned.":
            "Ever since I moved away, Christmas didn’t mean shit to me. It just became an excuse to slack off, sleep in, and play games until my eyes burned.",

        # BM script9:13165
        "But now... damn, now I get it.":
            "But now... damn, now I remember what it really means.",

        # BM script9:13180
        "I want to be with my friends for the rest of my life, without wondering if today’s the day some psycho or evil corporation takes it all away.":
            "I want to be with my family and friends for the rest of my life, without wondering if today’s the day some psycho or evil corporation takes it all away.",

        # BM script9:13204
        # Alex line overwritten by BM 49428, tbh still works okay as a casual "bro"

        # BM script9:13216
        "I didn't know you had a poet inside you, [mc]!":
            "I didn't know you had a poet inside you, little brother!",

        # BM script9:13316
        "*Whispering* Though... something tells me that's exactly the reaction Dalia was hoping for.":
            "*Whispering* Though... something tells me that's exactly the reaction a certain girl was hoping for.",

        # BM script9:13320
        "Did you get hard just staring at Dalia?":
            "Did you get hard just staring at your sister?",

        # BM script9:13417
        "Believe me, I know. You and Dalia are my everything, but I sure as hell wasn’t planning on being a mom at eighteen.":
            "Believe me, I know. You kids are my everything, but I sure as hell wasn’t planning on being a mom at eighteen.",

        # BM script9:13474
        "Well, Dalia’s January, I’m March... so that makes [mc] the baby of the group.":
            "Well, [mc]'s the baby of your family, and I'm March... so he goes first.",

        # BM script9:13632
        "Thank you for your very... scientific, articulate observation, [mc].":
            "Thank you for your very... scientific, articulate observation, brother.",

        # BM script9:13641
        "And just from external observation...":
            "And just from objective observation...",

        # BM script9:14226
        "Yeah, you'd sure like that.":
            "Seriously? We're mostly family here.",

        # BM script9:14241
        "Half of the people here have already seen me naked a hundred times, and the rest... well, we’re just having fun. Who cares?":
            "Like you said, it's just family here, plus Alex... and well, we’re just having fun. Who cares?",

        # BM script9:14294
        "Like you said, the card didn't mention anything else. Anyone saying otherwise would just be greedy.":
            "Like you said, the card didn't mention anything else. No need to go that far in front of just family.",

        # BM script9:14421
        "Not to mention Nancy wouldn’t put herself in that position with her daughters here.":
            "And I doubt my mom or sisters would kiss me like that in front of the others.",

        # BM script9:14585
        "Like... three of us are literally family here, so...":
            "Like... four of us are literally family here, so...",

        # BM script9:14586
        "I guess we can just skip ahead and give the points to [mc] and Alex.":
            "I guess we can just skip ahead and give the points to Alex.",

        # BM script9:14589
        "Hey, hold on! We still have to vote!":
            "Hey, hold on! We still have to vote! Those are the rules!",

        # BM script9:14590
        "Those are the rules!":
            "As the only guy here, I might be taking those points!",

        # BM script9:14594
        "F-Fine, fine... let's give [mc] his ego boost.":
            "F-Fine, fine... let's give this pervert his ego boost.",

        # BM script9:14595
        "If I {i}had to{/i} have a threesome with anyone here, I’d pick... [mc] and Alex.":
            "If I {i}had to{/i} have a threesome with anyone here, I’d pick Alex and... as the only man here, [mc].",

        # BM script9:14597
        "Funny, I'd also have it with [mc] and Alex.":
            "Guess I'd also have it with [mc] and Alex.",

        # BM script9:14608
        "Well... I’d never ever dare to suggest anything that could get pearl-clutching credit card companies offended, so I'll say Alex, and...":
            "Well... As much as I’d like to avoid anything that could get pearl-clutching credit card companies offended, my options here are limited, so I'll say Alex, and...",

        # BM script9:15202
        "You... YOU HAVE TOO–?!":
            "You... YOU HAVE TOO–?! BUT HE'S– he's your–",

        # BM script9:15211
        "I feel like... she probably suspects, but it's a different case with you than it is with me.":
            "I feel like... she probably suspects, but it's obviously a much different case with you than it is with me.",

        # BM script9:15217
        "I know it all might sound like a crazy bunch of bullshit, but...":
            "I know this might sound like a crazy bunch of bullshit on top of all that, but...",

        # BM script9:15222
        "This went from zero to nuclear real quick.":
            "This went from zero to nuclear real quick. Your brother...",

        # BM script9:15236
        "Why didn't you finish your drink, Mom...?":
            "M-Mom, I can explain–{w} Wait...{p}Why didn't you finish your drink, Mom...?",

        # BM script9:15241
        "NO. FUCKING. WAY.":
            "NO. FUCKING. WAY. YOU TOO?!",

        # BM script9:15835
        "I-I mean... it’s a little weird with [mc] here too, but... whatever." :
            "I-I mean... it’s a little weird with my brother here too, but... whatever." ,

        # BM script9:15911
        "J-Jesus Christ, [mc].":
            "J-Jesus Christ, bro.",

        # BM script9:15922
        "Alex! You're drunk as fuck!":
            "Alex! That's my brother! You're drunk as fuck!",

        # BM script9:15989
        "Oh, sweet heavens, Dalia...":
            "Oh, sweet heavens, sis...",

        # BM script9:16024
        "Um... I'm good, thanks.":
            "Um... I'm not touching my brother's dick, thanks.",

        # BM script9:16026
        "Oh, come on... don't be a bore!":
            "Oh, come on... don't be a bore! No one else will find out!",

        # BM script9:16042
        "Just... don't get any weird ideas.":
            "Just... don't get any weird ideas. We're still siblings...",

        # BM script9:16051
        "*Touching herself* AAaah... t-this is so fucking hot, Dal...":
            "*Touching herself* AAaah... t-this is so fucking hot, Dal...{p}Watching you jerk off your brother...",

        # BM script9:16061
        "...Thanks.":
            "*Whispers* Hey! Alex is right there!{w} ...But, thanks.",

        # BM script9:16088
        "You're dreaming.":
            "Hey! I'm your sister! And even if I weren't, I'm-",

        # BM script9:16089
        # interferes with script5:6463
        # "I'm not...":
        #     "And even if I weren't, I'm not...",

        # BM script9:16137
        "What? N-No.":
            "What? He's my brother! O-Of course not!",

        # BA/N: Tried having Alex really push the incest angle during the threesome

        # BM script9:16148
        "I know you two have fucked.":
            "I know you and your brother have fucked.",

        # BM script9:16185
        "*Whispering* You’re a dirty, horny slut who wants to be fucked until you can’t think straight.":
            "*Whispering* You’re a dirty, horny slut who wants to be fucked by your little brother until you can’t think straight.",

        # BM script9:16232
        "Are Dalia's tits big enough for you?":
            "Are your sister's tits big enough for you?",

        # BM script9:16269
        "Let yourself go and look at the man you love losing control because of you and your beautiful body.":
            "Let yourself go and look at your beloved brother losing control because of you and your beautiful body.",

        # BM script9:16247
        "O-Ohh Dalia, that feels so fucking good...":
            "O-Ohh sis, that feels so fucking good...",

        # BM script9:16277
        "Tell me, [mc]... do you wanna fuck Dalia...?":
            "Tell me, [mc]... do you wanna fuck your sister...?",

        # BM script9:16289
        "Do you want every inch of this cock sliding deep inside you...?":
            "Do you want every inch of this incestuous cock sliding deep inside you...?",

        # BM script9:16334
        "I-I need you to fuck me, [mc]...":
            "I-I need you to fuck me, bro...",

        # BM script9:16356
        "C-Christ, you're so fucking tight, Dalia...":
            "C-Christ, you're so fucking tight, sis...",

        # BM script9:16367
        "*Panting* Yeah... f-fuck me hard, [mc]...":
            "*Panting* Yeah... f-fuck me hard, bro...",

        # BM script9:16371
        "You're taking it balls-deep f-from the start, Dalia...":
            "You're taking it balls-deep f-from the start, sis...",

        # BM script9:16380
        "S-S-Slow down, [mc]...":
            "S-S-Slow down, bro...",

        # BM script9:16410
        "*Groaning* Oh D-Dalia...":
            "*Groaning* Oh s-sis...",

        # BM script9:16425
        "*Giggles* Your mouth is asking to slow down, but those eyes rolling back are screaming “fuck me harder, [mc]”...":
            "*Giggles* Your mouth is asking to slow down, but those eyes rolling back are screaming “fuck me harder, brother”...",

        # BM script9:16456
        "You guys are {i}made{/i} to fuck...":
            "You siblings are {i}made{/i} to fuck...",

        # BM script9:16457
        "*Grinning* It's like having a live porno in front of me...":
            "*Grinning* I'm watching a live incest porno in front of me...",

        # BM script9:16462
        "O-Oooooh [mc]... b-breeeEEAAAk meEEE...":
            "O-Oooooh bbrrroooo... b-breeeEEAAAk meEEE...",

        # BM script9:16464
        "Oh, Dalia... I-I'm getting close too...":
            "Oh, sis... I-I'm getting close too...",

        # BM script9:16516
        "I should warn you, though... I'm not as easy as Dalia.":
            "I should warn you, though... I'm not as easy as your sister.",

        # BM script9:16597
        "*Choked laugh* Y-You're one t-to talk...":
            "*Choked laugh* Y-You're one t-to talk...{p}I-If he's your daddy, am I your a-auntie...?",

        # BM script9:16693
        "*Grinning* You'll be fine, Dal...":
            "*Grinning* You'll be fine, sis...",

        # BM script9:16708
        "T-That's because [mc] broke me! A-And all because of you!":
            "T-That's because my brother broke me! A-And all because of you!",

        # BM script9:16833
        "It’s insane to think about, but... this woman right here is really the reason all of this is even working somehow.":
            "It’s insane to think about, but... my mom is really the reason all of this is even working somehow.",

        # BM script9:16845
        "I just... want everyone to be happy. Especially my daughters. So I nudge, guide, push a little where I think it’ll help.":
            "I just... want everyone to be happy. Especially my children, even in this... situation of ours. So I nudge, guide, push a little where I think it’ll help.",

        # BM script9:16952
        "Dalia Carter apologizing? This truly is a Christmas miracle.":
            "Dalia [lastname] apologizing? This truly is a Christmas miracle.",

        # BM script9:17003
        "W-Well, when you say it like that it sounds a little bit weird, but...":
            "W-Well, the whole incest part is weird enough as it is, so...",

        # BM script9:17004
        "Y-Yeah, kinda. Maybe. I guess.":
            "Sharing him can't be that much worse. Maybe. I guess.",

        # BM script9:17032
        "I get to be with the guy I love and still have my sister’s love!":
            "I get to be with my beloved brother and still have my sister’s love!",

    }

    # cousin_map = {
    # }

    annie_sister_map = {
        # -----------------------------------------
        # aka the Full Incest map
        # Annie as twin sister and Nancy’s child. Add on to base map.
        # Annie has same last name as MC
        # Annie’s father converted to paternal grandparents
        #     half sis map based on this, if edits are made here check if they can be applied there too.
        # -----------------------------------------
        # AS 0000 = Annie Sister map, Line number
        # Line numbers based on compiled script from v0.9.0, subject to change in future updates
        #    (which already happened in v0.9.4 fml, need to redo)
        # -----------------------------------------
        # AS script:0000 = Annie Sister map, RPY file:Line Number
        #     Numbers based on v0.9.5, subject to change in future updates
        #     slowly adapting line numbers to this format
        # LW/N = Lucifer_W's notes
        # l9/N = l9453394's notes
        # BA/N = BlueArrow's notes
        # -----------------------------------------

    # -----------------------------------------
    # v0.1 script.rpy  Lines 1-9769

        # BA/N: Want to mention "Grandparents" at some point in the intro, otherwise their appearence comes out of no where later on. 
        # not sure where tho
        #LW/N: Sounds like a good Idea maybe with a new lable or adding to the intro lable.

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

        # AS 962
        # LW/N: FIXED: Handle both versions
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

        # AS 1640
        # Disabled, interferes with other lines
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
            "God, you can't imagine how much I missed my little twins!",

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
            "Kind of, but it's been so many years.",

        # AS 1662
        "And of his babysitter!":
            "But I do remember all the fun we had playing together!",

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


        # label welcome_mod activates here. Numbers for both original and mod provided.


        # AS script:1843 IncestLables:24
        "(Each day I would spend the afternoon playing with her and Dalia. We had dinner every night at eight, and then Nancy drove me home once it got late.)":
            "(My afternoons were spent playing with Mom, Dalia, and Annie. We had dinner every night at eight, and then went to bed.)",

        # AS script:1845 IncestLables:26
        "(She would always call me on my birthday, but... aside from that, I never reached out. I have to make it up to her somehow.)":
            "(Mom would always call us on our birthday, but... aside from that, I never reached out. I have to make it up to her somehow.)",

        # AS script:1858
        # replaced by IncestLables:39

        # AS script:1859 IncestLables:40
        "Do you like it, Annie?":
            "Do you remember it, Annie?",

        # AS script:1860 IncestLables:41
        "This place looks awesome! Are you rich?!":
            "Yes, this place looks just like I remember! It's so beautiful! ",

        # AS script:1861 IncestLables:42
        "*Laughs* No, I wish. Houses in Kredon are not that expensive.":
            "*Laughs* That's nice, it never felt whole without you two.",

        # AS script:1862 IncestLables:43
        "It's beautiful! I'm used to living in a flat, so this looks like a palace to me!":
            "We're used to living in a flat now, so this'll be like living in a palace again! ",

        # AS script:1863 IncestLables:44
        "My husband and I bought it when I was pregnant with Dalia.":
            "Yes, it is a good home.",

        # AS script:1864 IncestLables:45
        "Although he left before she was born, so I was left paying the mortgage all by myself...":
            "It's served us well the past years.",

        # AS script:1865 IncestLables:46
        "*Clears throat* But that's a story for another day!":
            "*Clears throat* Let's not get sentimental...",

        # AS script:1868 IncestLables:49
        "You first, [mc]!":
            "You first, Annie!",

        # AS script:1876 IncestLables:57
        "That's cool! I love rainy days!":
            "Oh, I remember now, too! Guess that's why I've always loved rainy days!",

        # AS 1764 script:1888 IncestLables:69
        "Did you paint that?!":
            "Do you still paint?",

        # AS 1765 script:1889 IncestLables:70
        "Yeah, I used to paint in my free time, but I haven't done anything in years.":
            "No, I haven't done anything in years.",

        # AS script:1890
        # replaced by IncestLables:71

        # AS script:1894
        # replaced by IncestLables:75

        # AS script:1916 IncestLables:97
        "I wasn't expecting you to be so excited to meet [mc] again!":
            "I wasn't expecting you to be so excited to meet your brother and sister again!",

        # AS script:1932 IncestLables:113
        "Oh, y-yeah, so excited! Hi [mc]!":
            "Oh, y-yeah, so excited! Hi Annie!",

        # AS script:1936
        # replaced by IncestLables:117

        # AS script:1962 IncestLables:143
        "Both of those things can wait! You didn't even welcome [mc] and Annie properly!":
            "Both of those things can wait! You didn't even welcome your brother and sister properly!",

        # AS script:1963 IncestLables:144
        "They're gonna live with us for a whole year. You know that, right?":
            "We haven't seen them in ten years, you know!",

        # AS script:1967 IncestLables:148
        "[mc]! I can't wait to properly meet you!":
            "Hey bro, I can't wait to hear all about what happened to you and Annie!",

        # AS script:1970 IncestLables:151
        "Oh, and you must be Annie! Nice to meet you too!":
            "Oh, and Annie! Nice to see you again, sis!",

        # AS script:1972 IncestLables:153
        "Welcome to the family!":
            "Welcome back, you two!",

        # AS script:1973 IncestLables:154
        "By the way, I love your haircut!":
            "By the way, I love your haircut, sis!",

        # AS script:1983 IncestLables:164
        "Of course he doesn't mind!":
            "Of course they don't mind!",

        # AS script:2022 IncestLables:203
        "Because he's cool! It's good to see the city didn't change you, [mc].":
            "Because he's cool! It's good to see the city didn't change you, bro.",

        # AS script:2078 IncestLables:259
        "Annie, you must have gotten the wrong impression of my daughters...":
            "Still, I was hoping for a warmer family reunion after so much time apart...",

        # AS script:2080 IncestLables:261
        "Not at all! They both seem really nice!":
            "It's okay, Mom! We have plenty of time to catch up in the days to come!",

        # AS script:2081 IncestLables:262
        "For tonight, I’d rather just unpack all my things and freshen up a bit. We have plenty of time to get to know each other in the days to come!":
            "For tonight, I’d rather just unpack all my things and freshen up a bit.",

        # AS script:2083 IncestLables:264
        "You're so nice, Annie. Is there anything I can do for you?":
            "That's nice of you to say, honey. Is there anything I can do for you?",

        # AS script:2119 IncestLables:300
        "Well, since [mc] seems to remember where everything is already... Do you want a tour of the house, Annie?":
            "Well, since [mc] doesn't want any supper... Do you want something to eat, Annie?",

        # AS script:2124 IncestLables:305
        "Goodnight [mc]! Sweet dreams!":
            "Goodnight, bro! Sweet dreams!",


        # end label welcome_mod section


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

        # AS 15134
        "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out.)":
            "(Even if, somehow, he wanted me too... and we ended up... doing it, the girls would be furious if they ever found out. And fucking my son, is that even legal?)",

        # AS 15183
        "(I bet if I tried to do anything at home, Dalia or Penny would surely notice.)":
            "(I bet if I tried to do anything at home, the girls would surely notice.)",

        # AS 15707
        "And on the first day of school, I saw him harassing a close friend of mine.":
            "And on the first day of school, I saw him harassing my sister.",


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

        # AS 24701
        # no change for now, delete or save for the future
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

        # AS 35431 (menu)
        # l9/N: Changed to be fully compatible with and without either walkthrough
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


        #LW/N: Is NOT used in the HS map the replacement comes elsewhere but I can't find where.
        # AS 44139 phone chats (annie_chat)
        "I've been shopping all day with Nancy and I had no signal!":
            "I've been shopping all day with Mom and I had no signal!",

        "Shopping with Nancy":
            "Shopping with Mom",

        "Shopping with Nancy 😊":
            "Shopping with Mom 😊",

        "Nancy's gonna wonder what's taking me so long":
            "Mom's gonna wonder what's taking me so long",

        # AS 49310
        # Disabled, interferes with other lines, also doesn't work if not on other paths
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

        # AS 54273
        "[mc]...? What are you doing here?!":
            "Bro...? What are you doing here?!",

        # AS 54302
        "It's just... that... well, I was shocked at first since we had {i}never{/i} seen each other naked, and all that.":
            "It's just... that... well, I was shocked at first since the last time I saw you naked was {i}so long{/i} ago.",

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

        # AS script8:6910
        "Oh, no, no, no. Penny, Dalia, and Nancy were not an option.":
            "Oh, no, no, no. Penny, Dalia, and Mom were not an option.",

        # AS script8:6969
        "(She's definitely going on a date with [mc].)":
            "(She's definitely going on a date with [mc]. Her own twin brother!)",

        # BM script8:6983
        # BA/N: leaving this here for the future when we learn what exactly Luna's vision was
        # "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)":
        #     "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)",

        # AS script8:7092
        "It's straightforward yet stylish, giving off a confident vibe. It shows you're not desperate but also considerate enough to dress well for a date with someone who's been your second-best friend for so many years.":
            "It's straightforward yet stylish, giving off a confident vibe. It shows you're not desperate but also considerate enough to dress well for a date with someone who's been your second-best friend your entire life.",

        # AS script8:7098
        "Hey, don’t sweat it. I already told you, it gives you a mysterious, sexy vibe.":
            "Hey, don’t sweat it. I already told you, it gives you a mysterious, sexy vibe.{p}And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.",

        # AS script8:7099
        "And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.":
            "Which is still strange to think since you're twins, but... You two mean a lot to me, and I know how much you mean to each other.{p}So, I just want to tell you again that I'll always support you two.",

        # AS script8:7101
        "*Chuckles* If you say so...":
            "*Chuckles* Thanks, man. I appreciate it a lot. I'm sure Annie would, too",

        # AS script8:7398
        "Annie Winters and Luna Hernandez travel to the super scary Red Herring server and complete–":
            "Annie [lastname] and Luna Hernandez travel to the super scary Red Herring server and complete–",

        # AS script8:7532
        "I'll show them to Nancy later so I can–":
            "I'll show them to Mom later so I can–",

        # AS script8:7696
        "No one ever thought you were useless, Annie. But after this? D-Damn, even less so.":
            "No one ever thought you were useless, sis. But after this? D-Damn, even less so.",

        # AS script8:7713
        "Bye, bye, [mc]!":
            "Bye, bye, bro!",

        # AS script8:7778
        "Why...? Come on, [mc], you've met up with Annie solo a hundred times, why the jitters now?!":
            "Why...? Come on, [mc], you always have dinner with Annie, why the jitters now?!",


        # The following section is intended to be entirely replaced by new label "menurestaurant_mod"
        # Label mod should trigger when checking phone before Annie dinner date
        # Below is a backup in case it doesn't trigger.
            # BA/N: Touched up the backup, ngl still a bit half-assed due to a bunch of short lines lol.


        # AS script8:8047
        "You said it yourself. It's just a meal with Annie, like it's been a hundred times over the past 10 years.":
            "You said it yourself. It's just another meal alone with Annie, like we’ve usually had these last 10 years.",

        # AS script8:8051
        "Can't believe it's been that long already.":
            "Can't believe it's been that long since everything changed.",

        # AS script8:8116
        # "And I'm not really alone, my dad's inside this office registering our new address.":
        #    "And I'm not really alone, my dad's inside this office registering our new address.",

        # AS script8:8125
        "I live here too! My parents have a hotpot restaurant just around the corner! You and Annie should totally come someday!":
            "I live here too! My parents have a hotpot restaurant just around the corner! You should totally come someday! Hey, you wanna come too?",

        # AS script8:8127
        "Who's Annie?":
            "Who are you talking to?",

        # AS script8:8129
        "Annie from school!":
            "The girl!",

        # AS script8:8131
        "Oh... I don't know her. I just arrived here.":
            "Which girl?",

        # AS script8:8133
        "Oh... really? And then why is she here?":
            "The one behind you?",

        # AS script8:8140
        "Hi.":
            "Hey, Annie.",

        # AS script8:8141
        "Are you Annie?":
            "Why aren't you with Grandpa anymore?",

        # AS script8:8144
        "*Whispering* Why isn't she talking...?":
            "Annie?",

        # AS script8:8146
        "*Whispering* I know her from school, but she never talks there either.":
            "Do you know each other?",

        # AS script8:8147
        "*Whispering* I think she's mute.":
            "*Whispering* Is she mute?",

        # AS script8:8155
        "I go to school with Chang. I'm Annie.":
            "I'm Annie, [mc]'s sister.",

        # AS script8:8157
        "Hi Annie. I'm [mc].":
            "This is Chang, Annie.",

        # AS script8:8159
        # Shit, this interferes with script5:1198
        # "Hi [mc].":
        #    "Hi Chang.",

        # AS script8:8160
        "D-Did you...":
            "W-We just moved here...",

        # AS script8:8161
        "Did you move here?":
            "Did [mc] already tell you?",

        # AS script8:8162
        "Yep! From the US, with my dad.":
            "Yep! We're from the US.",

        # AS script8:8167
        "You shouldn't be out here alone either, Annie.":
            "Nice to meet you, Annie.",

        # AS script8:8168
        "You could be kidnapped. Or kidnapped and then sold.":
            "You said your grandpa is here too? I don't see him.",

        # AS script8:8170
        "I'm not alone, my dad's over there.":
            "Grandpa's over there.",

        # AS script8:8172
        "He's a businessman. He's doing business calls now.":
            "He's calling different people to help Dad with the papers and stuff.",

        # AS script8:8174
        "We were gonna see the pandas at the zoo, but... he got a call. So I guess we’re not going anymore.":
            "He's taking too long so I got bored and came over here.",

        # AS script8:8177
        "I like your... h-hair, American boy.":
            "Um... I like your.. s-shirt, Chang.",

        # AS script8:8178
        "And your shirt.":
            "But you look better with it, [mc]!",

        # AS script8:8184
        "N-Not really. I mean... my mom doesn't let me watch it.":
            "Y-Yeah.",

        # AS script8:8185
        "She says those Japanese cartoons aren't for kids.":
            "I like Sailor Moon.",

        # AS script8:8187
        "Oh... too bad.":
            "She wanted to be Sailor Moon for Halloween.",

        # AS script8:8189
        "No problem! Do you wanna play with us?! Let's meet at school tomorrow at lunch and pretend to be something we all know!":
            "Cool! Do you wanna play with us?! Let's meet at school tomorrow at lunch and pretend to be something we all know!",

        # AS script8:8192
        "My mom says superhero movies are too violent.":
            "I don't know that one.",

        # AS script8:8199
        "Haven't seen it. My mom says witchcraft is the devil's work.":
            "Haven't seen it yet.",

        # AS script8:8213
        "Wait... yes! I saw it at my uncle's house!":
            "Wait... yes! We saw it!",

        # AS script8:8264
        "Yeah, I should go before my dad gets mad too.":
            "Guess we still have to wait for Dad...",

        # AS script8:8265
        "Will you... will you be at school tomorrow?":
            "I can't wait for school tomorrow! Will you play with us, too?",

        # AS script8:8273
        "You won't ignore me there...?":
            "And if we don't see Chang, you'll still play with me? You won't leave me alone?",

        # AS script8:8275
        "Of course not. Why would I...?":
            "Of course. Why wouldn't I...?",

        # AS script8:8279
        "Promise me we'll be friends!":
            "Promise me we'll be together forever!",

        # AS script8:8283
        "Friends.":
            "I'll always be by your side, sis.",

        # AS script8:8284
        "Friends forever!":
            "Together forever!",

        # AS script8:8287
        "I'll leave now!":
            "I'll go see if Dad is done yet!",

        # AS script8:8288
        "See you tomorrow... [mc]!":
            "Wait here!",

        # AS script8:8293
        "They said there weren’t many kids around here, but it seems like it’s full of weird ones.":
            "We made a friend already... and Annie's starting to smile again...",

        # AS script8:8399
        "Actually, just before you got here, I was reminiscing about the day I met you and Chang.":
            "Actually, just before you got here, I was reminiscing about the day we arrived in Europe and met Chang.",

        # AS script8:8403
        "By all means! When I moved to London, I felt like my life was falling apart. You and Chang turned everything around for me.":
            "By all means! When we moved to London, everything felt like it was falling apart. But Chang helped turn that around, and the two of us grew closer than ever.",

        # AS script8:8418
        "And where was I going that day with my dad?":
            "And what were we waiting for?",

        # AS script8:8422 (menu)
        "To the movie theater":
            "For Chang's hotpot restaurant to open",

        # AS script8:8423
        "To the movie theater.":
            "For Chang's hotpot restaurant to open.",

        # AS script8:8424 (menu)
        # l9/N: Changed to be fully compatible with and without either walkthrough
        # BA/N: Not sure why this was originally disabled, but I've reenabled it for the backup
        "To see the pandas at the zoo":
            "{color=[walk_points]}For Dad to finish the registration [annie_pts]",

        # BA/N: temp fix for multi-mod tags not being stripped
        "To see the pandas at the zoo [annie_pts]":
            "{color=[walk_points]}For Dad to finish the registration [annie_pts]",

        # AS script8:8425
        "To see the pandas at the zoo.":
            "For Dad to finish the registration.",

        # AS script8:8426
        "Although... you had to cancel those plans.":
            "You bugged him over and over until he was done.",

        # AS script8:8438 (menu)
        "To play mini golf":
            "For a bus to go see pandas at the zoo",

        # AS script8:8439
        "To play mini golf.":
            "For a bus to go see pandas at the zoo.",


        # End label backup section


        # AS script8:8450
        "Alright, tell me about the first birthday we celebrated together, a couple of years after that.":
            "Alright, tell me what happened on our tenth birthday.",

        # AS script8:8455
        "We couldn’t celebrate your birthday because you were sick, so we decided to do a joint birthday celebration three weeks later at Chang’s parents' restaurant.":
            "Dad tried to be considerate for once and plan us a big party, but in the end he didn't have the time to do anything.{p}So we had a late birthday celebration three weeks later at Chang’s parents’ restaurant.",

        # AS script8:8497
        "D-Darn it, [mc].":
            "D-Darn it, bro.",

        # AS script8:8613
        "Your answer could shape how the rest of tonight goes and... maybe even your relationship with Annie.":
            "Your answer could shape how the rest of tonight goes and... maybe even your relationship with your sister.",

        # AS script8:8791
        "Nancy, Penny, Dalia, Luna, Alex, Nova...":
            "Luna, Alex, Nova, even Mom, Penny, and Dalia...",

        # AS script8:8845
        "I'm so impressed, Annie.":
            "I'm so impressed, sis.",

        # AS script8:8938
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
    # v0.9 script9.rpy

        # AS script9:167
        "Is there anything better than spending time with my favorite sister?":
            "Is there anything better than spending time with one of my precious little sisters?",

        # AS script9:433
        "*Grumbling to herself* I had a feeling something was going on between him and Nova. Or Annie. Or even Luna, for that matter!":
            "*Grumbling to herself* I had a feeling something was going on between him and Nova. Or Alex. Or even Luna, for that matter!",

        # AS script9:527
        "*Yawns* Agh, what's with all this noise so early in the morning, girls? You're gonna wake up Annie.":
            "*Yawns* Agh, what's with all this noise so early in the morning, girls? You're gonna wake up your sister.",

        # AS script9:553
        # BA/N: Ugh Can't think of a rewrite that works well. 
        "Luckily, I don't have any more sisters he can be with at the moment.":
            "Maybe having more secret adventures with his {i}other{/i} sister, too.",

        # AS script9:3008
        "Our...":
            "My...",

        # AS script9:3009
        "Our friend disappeared.":
            "My brother disappeared.",

        # AS script9:3014
        "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit some family for a few days!":
            "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit your father again for a few days!",

        # AS script9:3016
        "His only family is a drunk skunk of a father living an ocean away.":
            "Our father is a drunk skunk of a man living an ocean away.",

        # AS script9:3123
        "First, her sister. Oh, what a {i}coincidence{/i}, the last person to see [mc].":
            "First, your other sister. Oh, what a {i}coincidence{/i}, the last person to see [mc].",

        # AS script9:3267
        "*Standing up* No! Didn't you hear Nancy?!":
            "*Standing up* No! Remember what your mom said?!",

        # AS script9:3272
        "I can't live without him, Nova.":
            "I don't know how to live without him, Nova.",

        # AS script9:9919
        # BA/N: too cluinky
        "Annie flew back to the UK a few days ago to spend Christmas with her family and all, but she’s gonna be back before New Year’s Eve.":
            " Annie flew back to the UK a few days ago. Our grandparents invited us over for Christmas for the first time ever, probably missed us too much.{p}Annie took them up on the offer, but I already went back recently so I'm staying here. She’s gonna be back before New Year’s Eve.",

        # AS script9:9941
        "Nova's doing the family thing too.":
            "Nova's got family visiting.",

        # AS script9:9955
        "As for me, I’m spending Christmas Eve with Nancy, Penny, Dalia, and Alex. Even though... Alex doesn't know yet. It's a surprise.":
            "As for me, I’m spending Christmas Eve with the rest of the family and Alex. Although... Alex doesn't know yet. It's a surprise.",

        # AS script9:10030
        "Annie flew back to London for a few days to spend Christmas with her family — same with Nova and Luna.":
            "Annie flew back to London for a few days to spend Christmas with our grandparents, while Nova and Luna have family visiting for the holidays.",

        # AS script9:10117
        "Last Christmas, I had a cold kebab in the kitchen while my dad passed out on the couch in the middle of his tenth beer.":
            "Last Christmas, Annie and I had cold kebabs in the kitchen while Dad passed out on the couch in the middle of his tenth beer.",

        # AS script9:10424
        "Christmas never felt special to me.":
            "We never really celebrated it in the UK. Annie still enjoys the idea of it, but for me, Christmas stopped feeling very special.",

        # AS script9:10706 chat:614
        "I thought Nancy said you had no signal??":
            "I thought Mom said you had no signal??",

        # AS script9:10706 chat:626
        "But I really gotta go now or my dad will get mad {image=images/MENUS/e_tongue2.png}":
            "But I really gotta go now or grandpa will get mad",

        # AS script9:12870
        "I’ve never had a Christmas dinner like this before, Nan.":
            "I wish Annie was here for this, she's missing out on quite the feast!",

        # AS script9:12871
        "Feels really special.":
            "We’ve never had a Christmas dinner like this before, Mom. Feels really special.",
    }

    annie_only_sister_map = {
        # -----------------------------------------
        # Annie is MC’s sister (still twin?), no incest with Nancy, Penny, Dalia.
        # still incomplete
        # -----------------------------------------
        # OS 0000 = Only Sister map, Line number
        # Line numbers based on compiled script from v0.9.0, subject to change in future updates
        #    (which already happened in v0.9.4 fml, too lazy to redo all the numbers)
        # -----------------------------------------
        # OS script:0000 = Only Sister map, RPY file:Line Number
        #     Numbers based on v0.9.5, subject to change in future updates
        #     slowly adapting line numbers to this format
        # LW/N = Lucifer_W's notes
        # l9/N = l9453394's notes
        # BA/N = BlueArrow's notes
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
        # Done by Alenissmart
        # Al/N: Sorry but I am too lazy to write an entire new map, so I decided to copy the twin sister map and do edits to make it fit the half sister setting
        # -----------------------------------------
        # HS 0000 = Half Sister map, Line number
        # Line numbers based on compiled script from v0.9.0, subject to change in future updates
        #    (which already happened in v0.9.4 fml, too lazy to redo all the numbers)
        # -----------------------------------------
        # HS script:0000 = Half Sister map, RPY file:Line Number
        #     Numbers based on v0.9.5, subject to change in future updates
        #     slowly adapting line numbers to this format
        # LW/N = Lucifer_W's notes
        # Al/N = Alenissmart's notes
        # l9/N = l9453394's notes
        # BA/N = BlueArrow's notes
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
            "(I mean... If the girls never found out, then would it really be so bad? It’d be our little secret...{w} Of course it would be! He's my son...)",

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

        # HS 13734
        "I'm gonna... go... think! Good night [mc]!":
            "I'm gonna... go... think! Good night bro!",

        # HS 13751
        "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing Annie’s secret kinky side... and I loved every moment of it!)":
            "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing my sister's secret kinky side... and I loved every moment of it!)",

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

        # HS 29233
        # BA/N: Umm... offering up your own daughters is one thing, but offering up someone else's is a bit much
        "What about Dalia and Penelope?":
            "What about Dalia, Penelope, and Annie?",

        # HS 29242
        # BA/N: Ditto
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

        # HS 35431 (menu)
        # l9/N: Changed to be fully compatible with and without either walkthrough
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

        # HS 35489 
        # BA/N: hmmm original 10 years line works for half sis
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

        # HS 37588
        # BA/N: disabled, original line works better for half sis
        # "I don't know Aunt Cordelia, but I'm good at making collages.":
        #     "I'm good at making collages.",


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

        # HS 49310
        # Disabled, interferes with other lines, also doesn't work if not on other paths
        # "I like where this is going...":
        #    "I like where this is going... and I am too horny to care that she is my sister... as if I had cared with Mom, Dalia, or Annie...",

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

        # HS script6:6087 (menu)
        "You know dads can be real assholes":
            "You know Dad can be a real asshole",

        # HS script6:6088
        "You know as well as I do that dads can be real assholes.":
            "You know as well as I do that Dad can be a real asshole.",

        # HS script6:6090
        "W-Well... it's true that my dad has been working a lot all his life and he's been a bit absent, but... he's always cared about me.":
            "W-Well... it's true that Dad's kind of an asshole, but...",

        # HS script6:6091
        # BA/N: switch from grandparents to mom/uncle
        "And he thinks highly of you!":
            "You still had my mom! And my uncle! They think highly of you!",

        # HS script6:6093
        "Well... yeah, I guess that's different.":
            "Well... yeah. At least there were other adults who cared about me.",

        # HS script6:6094
        "That came out wrong, I'm sorry.":
            "Sorry for spiraling like that, thinking about him can be frustrating.",

        # HS script6:6096
        "No worries! I know you didn't mean it in a bad way.":
            "No worries! I'll always pull you back when you need it!",

        # HS 58697
        "I... I'm n-not sure I'm ready, [mc].":
            "I... I'm n-not sure I'm ready, bro.",

        # HS 58784
        "AAaahh... oh god [mc]... I think I'm gonna... C-CUM...":
            "AAaahh... oh god bro... I think I'm gonna... C-CUM...",

        # HS 58786
        "[mc]! You’re gonna make me...":
            "Bro! You’re gonna make me...",

        # HS 58955
        # BA/N: Disabled, does not apply to half route
        # "The sweet, innocent, little girl I've known for years...":
        #    "The sweet, innocent, little girl I've known my entire life...",

        # HS 58985
        "You better take care of my little girl while you're in the USA, [mc].":
            "You better take care of your sister while you're in the USA, [mc].",

        # HS 58986
        # LW/N: Unnecessary for the new version.
        # "Rest assured Mr. Winters, I won’t let anything happen to her!":
        #     "Rest assured Uncle, I won’t let anything happen to her!",

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

        # HS script8:3470 last name override
        "Was that Penelope Carter?!":
            "Was that Penelope Carter?!",

        # HS script8:3787 last name override
        "The one and only... PENELOPE CARTER!":
            "The one and only... PENELOPE CARTER!",

        # HS script8:3981 last name override
        "{cps=16}However...{cps=1.5} {cps=16}the call from Dalia Carter sparked a glimmer of hope within him, so he decided to head to the coffee area and wait for her.{cps=1} {cps=16}This...{cps=1.4} {cps=16}was his chance.":
            "{cps=16}However...{cps=1.5} {cps=16}the call from Dalia Carter sparked a glimmer of hope within him, so he decided to head to the coffee area and wait for her.{cps=1} {cps=16}This...{cps=1.4} {cps=16}was his chance.",

        # HS script8:4222
        "Come on, [mc], I need you to catch on quickly! We're running out of time.":
            "Come on, bro, I need you to catch on quickly! We're running out of time.",

        # HS script8:4278
        "There's no time to hesitate, [mc]!":
            "There's no time to hesitate, bro!",

        # AS script8:6969
        "(She's definitely going on a date with [mc].)":
            "(She's definitely going on a date with [mc]. Her own brother!)",

        # AS script8:6983
        # BA/N: leaving this here for the future when we learn what exactly Luna's vision was
        # "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)":
        #     "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)",

        # HS 88122
        "No one ever thought you were useless, Annie. But after this? D-Damn, even less so.":
            "No one ever thought you were useless, sis. But after this? D-Damn, even less so.",

        # does not use label mod

        # HS script8:8170
        "I'm not alone, my dad's over there.":
            "I'm not alone, my uncle's over there.",

        # HS script8:8172
        "He's a businessman. He's doing business calls now.":
            "He's talking to Mom on the phone. We're supposed to pick up my dad and brother who just moved over here from the USA.",

        # HS script8:8174
        # BA/N: wait shouldn't annie know dad already because of the "business trips"?
        "We were gonna see the pandas at the zoo, but... he got a call. So I guess we’re not going anymore.":
            "I think-I think that's you, [mc].",

        # HS script8:8177
        "I like your... h-hair, American boy.":
            "I like your... h-hair, brother.",

        # HS script8:8264
        "Yeah, I should go before my dad gets mad too.":
            "We should wait out here for Dad then.",

        # HS script8:8265
        "Will you... will you be at school tomorrow?":
            "Nice to... Nice to meet you, brother. Will you start going to school tomorrow?",

        # HS script8:8279
        "Promise me we'll be friends!":
            "Promise me I'll always be your favorite!",

        # HS script8:8283
        "Friends.":
            "Favorite.",

        # HS script8:8284
        "Friends forever!":
            "Favorite forever!",

        # HS script8:8287
        "I'll leave now!":
            "I'll go tell uncle I found you!",

        # HS script8:8288
        "See you tomorrow... [mc]!":
            "Wait here!",

        # HS script8:8293
        "They said there weren’t many kids around here, but it seems like it’s full of weird ones.":
            "So she's my new sister? They said there weren’t many kids around here, but it seems like it’s full of weird ones.",

        # HS script8:8418
        "And where was I going that day with my dad?":
            "And what were we waiting for?",

        # HS script8:8422 (menu)
        "To the movie theater":
            "For Chang's hotpot restaurant to open",

        # HS script8:8423
        "To the movie theater.":
            "For Chang's hotpot restaurant to open.",

        # Al/N: With and without walkthrough mod should both be supported (I'm not sure I never checked without walkthrough mod)
        # l9/N: Changed to be fully compatible with and without either walkthrough
        # HS script8:8424 (menu)
        "To see the pandas at the zoo":
            "{color=[walk_points]}For Dad to finish the registration [annie_pts]",

        # BA/N: temp fix for multi-mod tags not being stripped
        "To see the pandas at the zoo [annie_pts]":
            "{color=[walk_points]}For Dad to finish the registration [annie_pts]",

        # HS script8:8425
        "To see the pandas at the zoo.":
            "For Dad to finish the registration.",

        # HS script8:8426
        "Although... you had to cancel those plans.":
            "You kept bugging all of us until Dad was done.",

        # HS script8:8438 (menu)
        "To play mini golf":
            "For a bus to go see pandas at the zoo",

        # HS script8:8439
        "To play mini golf.":
            "For a bus to go see pandas at the zoo.",

        # HS script8:8497
        "D-Darn it, [mc].":
            "D-Darn it, bro.",

        # HS script8:8617
        "Your answer could shape how the rest of tonight goes and... maybe even your relationship with Annie.":
            "Your answer could shape how the rest of tonight goes and... maybe even your relationship with your sister.",

        # HS script8:8845
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

        # HS script9:553
        # BA/N: Ugh Can't think of a rewrite that works well. 
        "Luckily, I don't have any more sisters he can be with at the moment.":
            "Maybe having some secret adventures with his half-sister, too.",

        # HS script9:3008
        "Our...":
            "My...",

        # HS script9:3009
        "Our friend disappeared.":
            "My brother disappeared.",

        # HS script9:3014
        "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit some family for a few days!":
            "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit your father again for a few days!",

        # HS script9:3016
        "His only family is a drunk skunk of a father living an ocean away.":
            "Our father is a drunk skunk of a man living an ocean away.",

        # HS script9:10498 last name override
        "*Starts reading* {i}Dear Ms. Carter, thank you for booking my humble property for this year’s Christmas Eve.":
            "*Starts reading* {i}Dear Ms. Carter, thank you for booking my humble property for this year’s Christmas Eve.",

        # HS script9:10706 chat:626
        # BA/N: change grandpa to mom
        "But I really gotta go now or my dad will get mad {image=images/MENUS/e_tongue2.png}":
            "But I really gotta go now or my mom will get mad",

        # HS script9:13081 last name override
        "*Chuckles* (Penelope Paige Carter...)":
            "*Chuckles* (Penelope Paige Carter...)",

        # HS script9:16952 last name override
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
        # Done by l9453394
        # -----------------------------------------
        # Nancy aunt/Penelope & Dalia cousin character notes
        # 
        # - Nancy: MC used to call her "Auntie Nancy" as a kid. She only sees him as an irresistible young man. The mother-son incest roleplay is only there to make it hotter for her, despite the fact that it's genuinely blood-related incest either way. She's the horniest character (other than MC) and embraces her desires the earliest.
        # - Penelope: Use diminutive nickname "little cousin/little cuz/cuz/(rarely) cuzzy" for MC when Penelope is confidently joking/flirting or asserting herself. She has the strongest/clearest boundaries, and knows what she wants. After she starts becoming submissive to MC, make it a pet name. Don't go overboard with the nickname, though. It should just add a little "older sister" kick to flirty lines.
        # - Dalia: They're the same age, so never use diminutive nicknames. They should be just like childhood friends reuniting. Before she realizes it, she develops a crush on MC, and she doesn't pull very hard against it. Neither does MC. This path is much more innocent than Annie, despite the fact that it's (legally) more incestuous than Annie. It also has the fewest edits by far.
        # -----------------------------------------
        # AU = Nancy aunt/Penelope & Dalia cousin lines in annie_aunt_map
        # script:0000 = file name:line number
        # (menu) = Choice menu line
        # (chat) = Phone chat line
        # (n) = Nancy line
        # (p) = Penelope line
        # (d) = Dalia line
        # (other) = Other line (Any/all main)
        # (misc) = Miscellaneous line (Extras/side characters)
        # These tags aren't based on who's speaking, but who the line and scene are about.
        # l9/N = l9453394's notes
        # -----------------------------------------
        
        
    # -----------------------------------------
    # 0.1 script.rpy Nancy aunt/Penelope & Dalia cousin lines
        
        # AU script:1085 (other)
        "(Nancy used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(Nancy is my mother's sister. She used to look after me in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)",
        
        # AU script:1086 (other)
        "(I used to spend the entire afternoon playing with Nancy and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend the entire afternoon playing with Auntie Nancy and my cousin Dalia, but then we had to move and ended up losing touch.)",
        
        # AU script:1089 (other)
        "(Come to find out, she actually had 2 rooms available, so Annie will have a place to stay as well!)":
            "(When she heard Annie was coming, she offered us a second room, so I can finally introduce her to my family back in Kredon!)",
        
        # AU script:1098 (other)
        "I know, but I can't help feeling a little bit nervous.":
            "I know, but I can't help feeling a little bit nervous to meet your family.",
        
        # AU script:1711 (n)
        "How could I forget you?":
            "How could I forget my Auntie Nancy?",
        
        # AU script:1749 (n)
        "You clearly need a strong female influence in your life. Seems like I have my work cut out for me, young man!":
            "You clearly need a strong female influence in your life. Seems like your aunt has her work cut out for her, young man!",
        
        # AU script:1767 (n)
        "It’s me, Nancy! Even though we’ve only been speaking on the phone for the past few days, I feel like we’ve been becoming good friends already! Isn't that right, Annie?":
            "It’s me, Nancy! Even though we’ve only been speaking on the phone for the past few days, I feel like we’re becoming family already! Isn't that right, Annie?",
        
        # AU script:1786 (n)
        "And of his babysitter!":
            "And of his aunt!",
        
        # AU script:1790 (n)
        "Yeah, since my Dad was constantly working, I've always said you were like a parent to me.":
            "Yeah, since my Dad was constantly working, I've always said you were like a mother to me.",
        
        # AU script:1793 (n)
        "Now I work in a laboratory, but back then I was still finishing my thesis. Thankfully [mc]'s father came along and offered me the babysitting gig.":
            "Now I work in a laboratory, but back then I was still finishing my thesis. Thankfully [mc]'s father came to me and offered me a babysitting gig taking care of [mc] while he was at work.",
        
        # AU script:1794 (n)
        "It was not only well-paid, but also allowed me the flexibility to take care of my daughters at the same time. And for me, being a single mother, that was essential.":
            "It was not only well-paid, but also allowed me the flexibility to take care of my daughters at the same time. And for both of us, being a single mother and a single father, that was essential.",
        
        # AU script:1798 (n)
        "Yes, Dalia and Penelope. Penny was a little older when I was [mc]'s nanny, so she used to play on her own, but Dalia got very close to him!":
            "Yes, Dalia and Penelope. Penny is a little older than [mc], so she used to play on her own, but Dalia got very close to him! They were like twins.",
        
        # AU script:1811 (n)
        "(I guess you don't notice that stuff when you're 8 years old...)":
            "(I guess you don't notice stuff like that about your aunt when you're 8 years old...)",
        
        # AU script:1916 (n)
        "I wasn't expecting you to be so excited to meet [mc] again!":
            "I wasn't expecting you to be so excited to meet your cousin again!",
        
        # AU script:1931 (p)
        "Oh... O-Of course! [mc]!":
            "Oh... O-Of course! Little [mc]!",
        
        # AU script:2395 (n)
        "It's like we're family now. I’m not bothered by you at all!":
            "It's like we're family again. I’m not bothered by you at all!",
        
        # AU script:2430 (n)
        "(Jesus, look at me. Fantasizing about the dick of the kid I used to care for.)":
            "(Jesus, look at me. Fantasizing about the dick of the kid I used to raise like my own son.)",
        
        # AU script:2431 (n)
        "(You're 20 years older than he is, Nancy, for fuck's sake.)":
            "(You're his aunt, Nancy, for fuck's sake.)",
        
        # AU script:2585 (other)
        "(I mean, I know they’re pretty much like family, so I don't mean it that way, but...)":
            "(I mean, I know they’re my family, so I don't mean it that way, but...)",
        
        # AU script:2657 (p)
        "Is that supposed to be a joke?":
            "Is that supposed to be a joke? You're my cousin.",
        
        # AU script:2678 (p)
        "Thanks, [mc].":
            "Thanks, little cousin.",
        
        # AU script:2697 (p)
        "Oh, I'm sorry I bored you, sir.":
            "Oh, I'm sorry I bored you, little cousin.",
        
        # AU script:3425 (d)
        "(It's just Dalia. You two grew up together! She's practically your sister...)":
            "(It's just Dalia. You two grew up together! She's literally your cousin...)",
        
        # AU script:3442 (d)
        "Dalia, the girl you live with?":
            "Dalia, your cousin?",
        
        # AU script:3591 (n)
        "And there's nothing like being on chore duty to strengthen a household bond!":
            "And there's nothing like being on chore duty to strengthen a family bond!",
        
        # AU script:3668 (p)
        "*Imitating Penelope's voice* {i}Wow, [mc]!":
            "*Imitating Penelope's voice* {i}Wow, little cuz!",
        
        # AU script:3828 (d)
        "(And that's... wrong! Bad [mc]! Get a hold of yourself.)":
            "(And that's... wrong! Bad [mc]! This is your cousin! Get a hold of yourself.)",
        
        # AU script:4041 (p)
        "Alright [mc], you convinced me!":
            "Alright little cuz, you convinced me!",
        
        # AU script:4844 (p)
        "Well, I definitely do not share that opinion at all.":
            "Well, I definitely do not share that opinion. You're my family, Penny.",
        
        # AU script:4846 (p)
        "Thanks for trusting me, [mc]. It means a lot.":
            "Thanks for trusting me, little cuz. It means a lot.",
        
        # AU script:5479 (p)
        "(Looking at hot pics of Penelope, yeah, great idea, [mc]. Way to not have even more fantasies of all these girls around me...)":
            "(Looking at hot pics of Penelope, yeah, great idea, [mc]. Way to not have even more fantasies of all the girls in my family...)",
        
        # AU script:5541 (n)
        "(Who would’ve known he was hiding such a monster...)":
            "(Who would’ve known my nephew was hiding such a monster...)",
        
        # AU script:5559 (n)
        "(Oh Jesus, one man comes into my house and suddenly I turn into a nymphomaniac. What the hell is wrong with me?)":
            "(Oh Jesus, one man comes into my house and suddenly I turn into a nymphomaniac. What the hell is wrong with me? He's my family!)",
        
        # AU script:5583 (n)
        "(I mean... If Dalia and Penelope never found out, then would it really be so bad? It’d be our little secret...)":
            "(I mean... If the girls never found out, then would it really be so bad? It’d be our little secret... my big boy...)",
        
        # AU script:6045 (d)
        "You said you were Dalia's friend?":
            "You said you were Dalia's cousin?",
        
        # AU script:6047 (d)
        "Yeah, we’ve known each other since we were little.":
            "Yeah, I used to stay at her house all the time when we were little.",
        
        # AU script:8503 (p)
        "Thanks for supporting me, I appreciate it.":
            "Thanks for supporting me, little cuz. I appreciate it.",
        
        # AU script:8552 (n)
        "(You're not a horny teenager. Show her you're a man now.)":
            "(You're not a horny teenager. Show her you're a man now. She's just your aunt.)",
        
        
    # -----------------------------------------
    # 0.2 script2.rpy Nancy aunt/Penelope & Dalia cousin lines
        
        # AU script2:4574 (n)
        "*Laughs* It's not that. [mc] is staying with us for a year until he finishes school. He’s part of the student exchange program.":
            "*Laughs* It's not that. [mc] is my nephew. He's staying with us for a year until he finishes school as part of the student exchange program.",
        
        # AU script2:4840 (n)
        "What? I'm not Dalia. My name is [mc].":
            "What? I'm not Dalia. My name is [mc]. Dalia is my cousin.",
        
        # AU script2:4910 (n)
        "No, I came with Nancy.":
            "No, I came with Nancy. I'm her nephew.",
        
        # AU script2:4912 (n)
        "Oh, really? You two know each other? Well I’m glad to meet you, because I’m positive you’re going to be seeing a lot more of me soon...":
            "Oh, really? You two are related? Well I'm glad to meet you, because I'm positive you're going to be seeing a lot more of me soon...",
        
        # AU script2:4977 (n)
        "(Or can I? I mean... Why am I so jealous in the first place? It's not like anything could happen between Nancy and I anyways...)":
            "(Or can I? I mean... Why am I so jealous in the first place? It's not like anything could happen between Nancy and I anyways. She's my aunt...)",
        
        # AU script2:5014 (n)
        "Y-Yeah, I know Nancy very well, and honestly she’s been in quite a heightened emotional state lately. I can’t bear the thought of that guy taking advantage of her.":
            "Y-Yeah, Nancy's my aunt, and honestly she’s been in quite a heightened emotional state lately. I can’t bear the thought of that guy taking advantage of her.",
        
        # AU script2:5199 (n)
        "*Giggles* Just like when I was your babysitter.":
            "*Giggles* Just like when you were a kid.",
        
        # AU script2:5294 (n)
        "I can't be with him. It would be... weird. We’re not supposed to be together... like {i}that{/i}.":
            "I can't be with him. It would be... wrong. We’re not supposed to be together... like {i}that{/i}.",
        
        # AU script2:5321 (n)
        "*Giggles* Um, maybe. No... But, I mean... could you imagine?!":
            "*Giggles* Um, maybe. No, that would be so wrong... But, I mean... could you imagine?!",
        
        # AU script2:5363 (n)
        "(I can't just barge in and be like, \"Hi [mc], did you know you make me feel so horny all the time? Do you wanna fuck your old babysitter?\")":
            "(I can't just barge in and be like, \"Hi [mc], did you know you make me feel so horny all the time? Do you wanna fuck your old aunt?\")",
        
        # AU script2:5364 (n)
        "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out.)":
            "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out... {w}And fucking my nephew, is that even legal?)",
        
        # AU script2:7088 (p)
        "Is that a hint of jealousy, I’m sensing?":
            "Is that a hint of jealousy I’m sensing, little cousin?",
        
        # AU script2:7117 (p)
        "(I mean... not that I care... or even had any chance, but still...)":
            "(I mean... not that I should care... or even had any chance, but still...)",
        
        # AU script2:7128 (p)
        "(It's not like I was expecting her to wait for me like a nun, but... just imagining some guy banging her... ugh.)":
            "(It's not like I was expecting her to keep her chastity like a nun, but... just imagining some guy banging her... ugh.)",
        
        # AU script2:7134 (p)
        "(Way out of your league.)":
            "(Way out of your league, and also, your cousin.)",
        
        # AU script2:7156 (p)
        "Ahhh... yeah, that’s right. [mc]...":
            "Ahhh... yeah, that’s right. Your cousin, [mc]...",
        
        # AU script2:7306 (p)
        "Someone is a good listener... thank you for remembering!":
            "My little cousin is a good listener... thank you for remembering!",
        
        # AU script2:7334 (p)
        "(Wake up [mc], we're talking about Penelope here. Still not gonna happen.)":
            "(Wake up [mc], we're talking about your cousin Penelope here. Still not gonna happen.)",
        
        # AU script2:7404 (p)
        "But that’s why I’m glad to have you here, [mc].":
            "But that’s why I’m glad to have you here, little cuz.",
        
        # AU script2:7534 (p)
        "I might need you to be my photographer more often, [mc]!":
            "I might need you to be my photographer more often, little cuz!",
        
        # AU script2:7679 (p)
        "Well, you sure do know how to push a button, [mc].":
            "Well, you sure do know how to push a button, cuz!",
        
        # AU script2:7705 (p)
        "I don't mind you seeing me like this, because... I don't know, I just feel comfortable around you.":
            "I don't mind you seeing me like this... You're my little cousin, I feel comfortable around you.",
        
        # AU script2:7819 (p)
        "Come on, you know you can trust me. I wouldn’t do you wrong.":
            "Come on, cuz, you know you can trust me. I wouldn’t do you wrong.",
        
        # AU script2:7961 (p)
        "You know... this whole thing got me thinking...":
            "You know, little cuz... this whole thing got me thinking...",
        
        # AU script2:7973 (p)
        "That Valentino guy made me realize that I'll never feel comfortable doing something like this with a stranger. But you’re no stranger, [mc], and since I have you here...":
            "That Valentino guy made me realize that I'll never feel comfortable doing something like this with a stranger. But you’re family, [mc], and since I have you here...",
        
        # AU script2:7992 (p)
        "(Oh my god, am I about to see Penelope naked?)":
            "(Oh my god, am I about to see my cousin naked?)",
        
        # AU script2:8076 (p)
        "Oh don’t be like that! It'll be fun!":
            "Oh don’t be like that, cuz! It'll be fun!",
        
        # AU script2:8115 (p)
        "Oh, come on, [mc]!":
            "Oh, come on, little cuz!",
        
        # AU script2:8140 (p)
        "(Is this huge thing I’m feeling... his...)":
            "(Is this huge thing I’m feeling... my little cousin's...)",
        
        # AU script2:8198 (p)
        "I don't know what it is about you, but... I always have so much fun when you’re around.":
            "I don't know what it is about you, little cuz, but... I always have so much fun when you’re around.",
        
        # AU script2:8315 (p)
        "I was wondering why Nancy and her shared the same last name on your followers list. Nancy is her mom!":
            "I was wondering why Nancy and her shared the same last name on your followers list. She must be your cousin!",
        
        # AU script2:8409 (p)
        "(I’ve never been good at taking a hint.)":
            "(She's always been like a big sister to me.)",
        
        # AU script2:8420 (p)
        "And now I’ve come to learn that you’re friends with Penelope too?!":
            "And now I’ve come to learn that you’re cousins with Penelope too?!",
        
        # AU script2:8624 (p)
        "Have fun playing.":
            "Have fun playing, little cuz.",
        
        
    # -----------------------------------------
    # 0.3 script3.rpy Nancy aunt/Penelope & Dalia cousin lines
        
        # AU script3:1248 (misc)
        "We will not leave until every lustful desire of yours is satisfied. Use us as your personal toys, as we surrender ourselves to every inch of you... or lay back and let us take the lead... and do all of the work.":
            "We will not leave until every lustful desire of yours is satisfied. Use us sisters as your personal toys, as we surrender ourselves to every inch of you... or lay back and let us take the lead... and do all of the work.",
        
        # AU script3:2803 (d)
        "Nah... I don’t need to sleep out here. I tricked a Kredon family into letting me live in their house for a whole year. They set me up with a bed to sleep in, too, so no park benches for me!":
            "Nah... I don’t need to sleep out here. I tricked some relatives in Kredon into letting me live in their house for a whole year. They set me up with a bed to sleep in, too, so no park benches for me!",
        
        # AU script3:2808 (d)
        "Especially the youngest daughter. She's extremely naive and easily manipulated.":
            "Especially my youngest cousin. She's extremely naive and easily manipulated.",
        
        # AU script3:2912 (d)
        "Don't worry, I’m not going to waste time on your whore anymore.":
            "Don't worry, I’m not going to waste time on your whore cousin anymore.",
        
        # AU script3:3941 (p)
        "Penelope and I know each other from college, [mc].":
            "Penelope and I know each other from college, [mc]. I don't know why you never told me you were her cousin!",
        
        # AU script3:4615 (p)
        "And this here is Penelope, and next to her...":
            "And this here is my cousin Penelope, and next to her...",
        
        # AU script3:4852 (n)
        "If Nancy asks, I ate it all!":
            "If Auntie Nancy asks, I ate it all!",
        
        # AU script3:4916 (n)
        "(This nanny gig just isn't enough to pay the bills, and between paying the girls’ tuition and the mortgage...)":
            "(This nanny gig with [mc] just isn't enough to pay the bills, and between paying the girls’ tuition and the mortgage...)",
        
        # AU script3:4919 (n)
        "([mc]'s father is already generously paying me more than he should for taking care of his son. But even with that extra money, it’s only delaying the inevitable.)":
            "([mc]'s father is already generously paying me more than he should for taking care of his son. I don't know what we'd do without his support. But even with that extra money, it’s only delaying the inevitable.)",
        
        # AU script3:5200 (p)
        "Has [mc] finished his dinner?":
            "Has little [mc] finished his dinner?",
        
        # AU script3:5234 (p)
        "I can see the mud stains from here, mister!":
            "I can see the mud stains from here, little cousin!",
        
        # AU script3:5286 (p)
        "*Giggles* That's a bold move!":
            "*Giggles* That's a bold move, little cuz!",
        
        # AU script3:5970 (p)
        "We're just friends. I've only seen her half-naked once... during a photoshoot.":
            "She's my cousin. I've only seen her half-naked once... during a photoshoot.",
        
        # AU script3:5991 (p)
        "So tell me... don't you wanna see a bit more? If I had a \"friend\" who looked like this, I’d be dying to find out what’s underneath all those clothes...":
            "So tell me... don't you wanna see a bit more? If I had a cousin who looked like this, I’d be secretly dying to find out what’s underneath all those clothes...",
        
        # AU script3:6005 (p)
        # interferes with script:1493
        # "She's perfect...":
        #     "She's... my cousin is... perfect...",
        
        # AU script3:6044 (p)
        "Or if you prefer, you can feel this huge, gorgeous ass right here...":
            "Or if you prefer, you can feel your cousin's huge, gorgeous ass right here...",
        
        # AU script3:6291 (p)
        "Sometimes I forget I'm friends with a celebrity.":
            "Sometimes I forget I'm related to a celebrity.",
        
        # AU script3:6296 (p)
        "That makes me very uncomfortable, to be honest. I’m gonna need a little more fanfare from you, [mc].":
            "That makes me very uncomfortable, to be honest. I’m gonna need a little more fanfare from you, little cousin.",
        
        # AU script3:6316 (p)
        "I couldn't care less about your social network pages or how many followers you have... I only care about the person behind it. You became a special person to me just because of who you are.":
            "I couldn't care less about your social network pages or how many followers you have... I only care about the person behind it. You're my one and only big cousin, and you always looked after me. You're special to me just because of the person you are.",
        
        # AU script3:6374 (p)
        "Nice to meet you. I’m [mc], and this is Penelope and Luna.":
            "Nice to meet you. I’m [mc], and this is Luna and my cousin Penelope.",
        
        # AU script3:6564 (p)
        "A friend!":
            "Someone I like!",
        
        # AU script3:6583 (p)
        "(That's too bad...)":
            "(Well yeah, she's my cousin...)",
        
        # AU script3:6646 (p)
        "Your BDSM-lover friend said you’ve all been to the Emporium already, right?":
            "Your BDSM-lover cousin said you’ve all been to the Emporium already, right?",
        
        # AU script3:6984 (p)
        "[mc]... can I confess something to you...? ":
            "Little cousin... can I confess something to you...? ",
        
        # AU script3:6991 (p)
        "Are you gonna fuck me, daddy?":
            "Are you gonna fuck me, little cuz?",
        
        # AU script3:7664 (p)
        "These are my friends, Penelope and Luna.":
            "This is my cousin, Penelope, and my friend Luna.",
        
        # AU script3:7688 (misc)
        "She's my cousin. Totally loves to roleplay as an elf.":
            "She's my... second cousin. Totally loves to roleplay as an elf.",
        
        # AU script3:7907 (p)
        "Don't worry [mc], I'm in good hands!":
            "Don't worry little cuz, I'm in good hands!",
        
        # AU script3:8172 (d)
        "Actually, I am! I'm looking for a friend of mine. She’s the one who invited me to the server.":
            "Actually, I am! I'm looking for my cousin. She’s the one who invited me to the server.",
        
        # AU script3:8330 (d)
        "I was just looking for her! Her name is Dalia.":
            "I was just looking for her! Her name is Dalia. She's my cousin.",
        
        # AU script3:8780 (d)
        "S-Seriously? You're a fucking pig!":
            "S-Seriously? You're a fucking pig! We're cousins!",
        
        # AU script3:8790 (d)
        "Oh damn, so you'd do all that too?!":
            "Oh, so it's fine to do all that with your cousin?!",
        
        # AU script3:9576 (n)
        "*Laughs* Oh, don’t you dare! You’re too much!":
            "*Laughs* Oh, don’t you dare! You’re my nephew, so that makes you a Prince too!",
        
        # AU script3:9585 (n)
        "Well, enough about her. I want to hear more from my esteemed Champion. Did you know this Royal Bathhouse is open only to the Emperor and the Emperor’s special guests?":
            "Well, enough about her. I want to hear more from my noble Prince. Did you know this Royal Bathhouse is open only to chosen members of the imperial family and the Emperor’s special guests?",
        
        # AU script3:9587 (n)
        "I had no idea! I feel so honored now. Does that make me your special guest?":
            "I had no idea! I feel so honored now. Does that make me your chosen family, or your special guest?",
        
        # AU script3:9588 (n)
        "Indeed... I don’t see anyone else around here...":
            "Well... No one said you couldn’t be both...",
        
        # AU script3:9648 (n)
        "You, my Champion. Will you be joining me, or do you have to get going?":
            "You, my Prince. Will you be joining me, or do you have to get going?",
        
        # AU script3:9663 (n)
        "(Keep it together! She’s been like a mother to you. Focus, [mc]! This is strictly a bath!)":
            "(Keep it together! She’s your aunt, and she's like a mother to you. Focus, [mc]! This is strictly a bath!)",
        
        # AU script3:9694 (n)
        "And I saw you! Back when you were my babysitter. I was too young to remember most of that time, but you looked exactly like you did in our old pictures!":
            "And I saw you! Back when you took care of me. I was too young to remember most of that time, but you looked exactly like you did in our old family pictures!",
        
        # AU script3:9706 (n)
        "I owe it to my mother. It seems like once she reached 25, she stopped aging. She died shortly after Dalia was born, but she was always so full of life.":
            "I owe it to your grandmother. It seems like once she reached 25, she stopped aging. She died shortly after you and Dalia were born, but she was always so full of life.",
        
        # AU script3:9714 (n)
        "Girlfriend. No doubt about it at all.":
            "Girlfriend. No doubt about it at all. No one would believe me if I said you're my aunt.",
        
        # AU script3:9736 (n)
        "I see... my young [mc] has a little experience under his belt. Very interesting...":
            "I see... my young nephew has a little experience under his belt. Very interesting...",
        
        # AU script3:9768 (n)
        "I mean... I'd never dare.":
            "I mean... th-they're my cousins. I'd never dare.",
        
        # AU script3:9770 (n)
        "Why not? I wouldn’t mind having you as my son-in-law...":
            "Just forget about that for a moment, [mc]. I know it’s taboo, but I... wouldn’t mind having you as my son-in-law...",
        
        # AU script3:9780 (n)
        "I'd be lying if I said that doesn’t sound like a dream come true.":
            "I know it would be incest, but... I'd be lying if I said that doesn’t sound like a dream come true.",
        
        # AU script3:9791 (n)
        "*Chuckles* Is someone hinting that I might be good enough...?":
            "*Chuckles* Aren't you forgetting something important...?",
        
        # AU script3:9793 (n)
        "*Giggles* I'm not sure yet. You definitely have most of the desirable qualities in a man, but still... there’s some areas of you I don’t know much about.":
            "*Giggles* You're their family, [mc]. I’ve watched you grow up together, and I know you’d treat them right. You definitely have most of the desirable qualities in a man, but still... there’s some areas of you I don’t know much about.",
        
        # AU script3:9802 (n)
        "I couldn't. I don't know... I just see them as family.":
            "I couldn't. I don't know... they're my family.",
        
        # AU script3:9804 (n)
        "Ah, I see. I guess it does make sense.":
            "Ah, I see. I guess you're probably right.",
        
        # AU script3:9820 (n)
        "Your energy is infectious. Your charm is invigorating. When I’m with you, I feel like I can take on the world. And then you awaken so many other feelings within me that I thought were long gone...":
            "Your energy is infectious. Your charm is invigorating. When I’m with you, I feel like I can take on the world. And then you awaken so many other feelings within me that I thought were long gone... feelings that I know I shouldn’t have...",
        
        # AU script3:9822 (n)
        "Wow... I had no idea, Nancy.":
            "Wow, I... I had no idea, Nancy.",
        
        # AU script3:9827 (n)
        "No, really Nancy... it honestly feels so nice to hear that coming from you. I consider you to be someone very important in my life, so it’s truly appreciated.":
            "No, really Nancy... it honestly feels so nice to hear that coming from you. You're my family and one of the most important women in my life, so it’s truly appreciated.",
        
        # AU script3:9832 (n)
        "*Chuckles* Very much. I’m honored to be your special guest... and feel so privileged to witness such a rare and honestly breathtaking sight.":
            "*Chuckles* Very much. I’m honored to be your chosen family and special guest... and feel so privileged to witness such a rare and honestly breathtaking sight.",
        
        # AU script3:9842 (n)
        "Hmph. I invite a commoner to my private baths and he can’t even contain himself. What a shame.":
            "Hmph. I invite my own nephew to our private baths and he can’t even contain himself. What a shame.",
        
        # AU script3:9865 (n)
        "(I’d hate myself if I didn’t at least try...)":
            "(She’s irresistible... even if it’s wrong, I can’t deny it...)",
        
        # AU script3:9900 (n)
        "(I can tell she was looking forward to this.)":
            "(I can tell she was looking forward to this... my Auntie Nancy...)",
        
        # AU script3:9942 (n)
        "Does the Champion truly want to serve his Empress?":
            "Does the Prince truly wish to serve his Empress?",
        
        # AU script3:9946 (n)
        "You know... I remember from my history classes that it was always taboo for royalty to intermingle with common folk...":
            "You know... I remember from my history classes that it was common for royal families to \"intermingle\" with one another...",
        
        # AU script3:9947 (n)
        "But I think we’ve broken enough rules today...":
            "As they say... {i}\"When in Rome, do as the Romans do...\"{/i}",
        
        # AU script3:9949 (n)
        "I need to feel my Champion... taste the forbidden fruit...":
            "I need to feel my Prince... taste the forbidden fruit...",
        
        # AU script3:9970 (n)
        "Oh, my C-Champion feels...":
            "Oh, my P-Prince feels...",
        
        # AU script3:9971 (n)
        "Oh, s-screw the Champion shit...":
            "Oh, s-screw the Prince shit...",
        
        # AU script3:10096 (n)
        "I've wanted you to fuck me ever since I first saw you in that park. I thought maybe it was just a fleeting urge and it’d pass quickly... but no...":
            "I've wanted you to fuck me ever since I first saw you in that park. I thought maybe it was just a forbidden urge and it’d pass quickly... but no...",
        
        # AU script3:10106 (n)
        "This time though... I want you to lie back and let your babysitter do all the work...":
            "This time though... I want you to lie back and let your Auntie Nancy do all the work...",
        
        # AU script3:10133 (n)
        "*Whispering* What for? It’s only a guard!":
            "*Whispering* What for? It’s only a guard! They don't know we're related.",
        
        # AU script3:10137 (n)
        "*Whispering* Oh, that's a good point.":
            "*Whispering* Oh, shit... I told Maximo earlier that Dalia was my cousin.",
        
        # AU script3:10177 (n)
        "(Why does God hate me?)":
            "(Why does God hate me? Is this divine punishment?)",
        
        # AU script3:10213 (n)
        "(Man, I was so damn close to fucking Nancy...!)":
            "(Man, I was so damn close to fucking Nancy...! It's so... wrong...)",
        
        # AU script3:10221 (n)
        "(Little do they know... heh.)":
            "(I hope I can still look them in the face after this...)",
        
        
    # -----------------------------------------
    # 0.4 script4.rpy Nancy aunt/Penelope & Dalia cousin lines
        
        # AU script4:2275 (n)
        "I'm not Nancy's daughter. I mean, I'm not even a girl! Do I have to spell it out or what?":
            "I'm not Nancy's daughter, I'm her nephew. I mean, I'm not even a girl! Do I have to spell it out or what?",
        
        # AU script4:2281 (n)
        "(With so many people living under the same roof, it'll be hard to find some time alone.)":
            "(With all our family living under the same roof, it'll be hard to find some time alone.)",
        
        # AU script4:2425 (d)
        "Thanks buddy. You're a good friend.":
            "Thanks cuz. You're a good friend.",
        
        # AU script4:3031 (d)
        "I didn't know you were dating!":
            "I didn't know you were dating! Wait, aren't you two cousins?",
        
        # AU script4:3043 (d)
        "Why didn't you tell me, [mc]?!":
            "Hold on, you two aren't actually cousins?! Is she adopted?! Why didn't you tell me, [mc]?!",
        
        # AU script4:3049 (d)
        "We're not dating!":
            "W-What? No! We're not {i}dating!",
        
        # AU script4:3050 (d)
        "We're just old friends!":
            "We're just cousins!",
        
        # AU script4:3056 (d)
        "It doesn't mean anything!":
            "It doesn't mean anything! A-And I heard that in Europe, cousins kiss each other all the time!!",
        
        # AU script4:3145 (d)
        "I'm the lame one? Go tell that to that crybaby girlfriend of yours.":
            "I'm the lame one? Go tell that to that crybaby cousin of yours.",
        
        # AU script4:3688 (d)
        "I know you already saw me naked, but I hope this can still get you in the mood." :
            "I know you already saw me naked, but I hope this can still get you in the mood. I trust that us being cousins won't be an issue for little [mc].",
        
        # AU script4:3690 (d)
        "Well... I hope this is enough to get you in the mood.":
            "Well... I hope this is enough to get you in the mood. I trust that us being cousins won't be an issue for little [mc].",
        
        # AU script4:3977 (d)
        "Well, well, well... so you openly admit having fantasized about how my cum tastes, huh...?":
            "Well, well, well... so you openly admit having fantasized about how your cousin's cum tastes, huh...?",
        
        # AU script4:5113 (other)
        "Nancy, Penelope, and Dalia are all very nice to me. They treat me as one of the family. You know I’ve always wanted sisters, so I really feel like they’re giving me that experience!":
            "Nancy, Penelope, and Dalia are all very nice to me. They treat me as part of your family. You know I’ve always wanted sisters, so I really feel like they’re giving me that experience!",
        
        # AU script4:7330 (p)
        "Thanks! You’re a sweetheart. I've been practicing with Luna these past few days. I can't stop playing!":
            "Thanks, little cuz! You’re a sweetheart. I've been practicing with Luna these past few days. I can't stop playing!",
        
        # AU script4:7347 (p)
        "There's no way out of this friend zone...":
            "Guess she still just sees me as her little cousin...",
        
        # AU script4:7402 (p)
        "What other people? You? Mom? Annie? I'm sure [mc] doesn't mind either. He's like... family. Like a little brother, almost.":
            "What other people? You? Mom? Annie? I'm sure [mc] doesn't mind either. He's just family. Like a little brother, almost.",
        
        # AU script4:7408 (p)
        "With [mc]? Pffft, please, my bar is WAY higher. You’ve seen my Instagram DMs: models, actors, influencers... did you know that that Gigachad meme guy from a few years ago tried sliding into my DMs?":
            "With [mc]? Pffft, please, even if he {i}wasn't{/i} our cousin, my bar is WAY higher. You’ve seen my Instagram DMs: models, actors, influencers... did you know that that Gigachad meme guy from a few years ago tried sliding into my DMs?",
        
        # AU script4:8176 (misc)
        "Actually, he was caught with HER sister in HIS office!":
            "Actually, he was caught with HIS OWN sister in HIS office!",
        
        
    # -----------------------------------------
    # 0.5 script5.rpy Nancy aunt/Penelope & Dalia cousin lines
        
        # AU script5:448 (d)
        "(Yeah, that would be fair. Just so we're even.)":
            "(If I had to go down on my own cousin, he should do it too. Just so we're even.)",
        
        # AU script5:465 (d)
        "(I don't even like him. The only guy I kinda liked lately wasn’t even into me.)":
            "(I don't even like him. The only guy I kinda liked lately was my own cousin... and he wasn’t even into me.)",
        
        # AU script5:1124 (n)
        "What have I done to deserve this? What god have I pissed off?!":
            "What have I done to deserve this? What god have I pissed off?! I haven't committed any sins...{w} other than, um... {w}lust, fornication, incest, greed, pride, and {i}so{/i} much temptation...",
        
        # AU script5:4799 (p)
        "*Knocks on the door* [mc]? Is that you?":
            "*Knocks on the door* Little cuz? Is that you?",
        
        # AU script5:4858 (p)
        "*Chuckles* Are you alright?":
            "*Chuckles* Are you alright, little cuz?",
        
        # AU script5:4902 (p)
        "Yeah, I'll let you finish your shower, sorry. Didn’t mean to give you a {i}hard{/i} time.":
            "Yeah, I'll let you finish your shower. Sorry, cuz. Didn’t mean to give you a {i}hard{/i} time.",
        
        # AU script5:5086 (p)
        "*Chuckles* Don’t be silly! You're staying with us until we say so. No escaping the Carters!":
            "*Chuckles* Don’t be silly, little cuz! You're staying with us until we say so. No escaping the Carters!",
        
        # l9/N: I completely rewrote the next three lines.
        # I've added the most incest lines for Penelope, and it's especially prevalent in casual conversation, which I left almost entirely untouched for Nancy and Dalia. During the party, I decided to dial it all back, so they're pretending to be just friends. Hopefully, you can feel the distinct absence of all the "little cuz"es, even though the lines are just vanilla. It also matches with the incest roleplay theme of Nancy's path in 0.5, except instead of pretending to be related, they're pretending not to be.
        # It's definitely not because I was going insane trying to figure out how to rewrite the truth or dare game if everyone knows they're related without them seeming absolutely insane...
        
        # AU script5:5217 (p)
        "*Chuckles* You're too excited, [mc].":
            "Hey, cuz... before we go in, let's agree not to tell anyone we're related.",
        
        # AU script5:5218 (p)
        "If you think this is going to be like American Pie, you'll be disappointed.":
            "There are a few people here I have some... {i}disagreements{/i} with, and I don't want to get you involved in it.",
        
        # AU script5:5219 (p)
        "Hey, there's a passed out Power Ranger next to a bottle of vodka by the entrance. That's promising.":
            "Alright, that makes sense... But if they pick a fight with me, that's fair game, right?",
        
        # AU script5:5286 (p)
        "Y-You... what?!":
            "Y-You... what?! B-But aren't you guys... y'know, blood-related?",
        
        # l9/N: I combined the next two lines to make space for a new line.
        # AU script5:5288 (p)
        "Isn't it crazy?!":
            "Isn't it crazy?! I've never been attracted to guys younger than me, let alone my little cousin, but I don't know... he's really cute! And...",
        
        # AU script5:5289 (p)
        "I've never been attracted to guys younger than me, but I don't know... he's really cute!":
            "*Whispering* Honestly, the fact that we're related makes it {i}{b}so{/b}{/i} much more exciting!",
        
        # AU script5:5302 (p)
        "But he might not be into me like that so... keep it secret!":
            "But we're still family, and he might not be into me like that so... keep it secret!",
        
        # AU script5:5316 (p)
        "(A BIG one!)":
            "(A BIG one! The biggest one I've ever heard!)",
        
        # AU script5:5322 (p)
        "(But holy shit, did she say she has a crush on [mc] too?!)":
            "(But holy shit, did she say she has a crush on [mc] too?! Her own {i}cousin!!{/i} I mean, I'm an only child, so I don't really know how their family works, but...)",
        
        # AU script5:5344 (p)
        "(Nothing happened. So what if my new bestie Penny and I have a crush on the same boy?)":
            "(Nothing happened. So what if my new bestie Penny and I have a crush on the same boy? So what if h-he's her cousin?)",
        
        # AU script5:7840 (p)
        "Or... your girlfriend, or anything.":
            "Or... your girlfriend, or anything. We're just cousins.",
        
        # AU script5:7888 (p)
        "I'd be mad too if someone had ignored me like that just to try to hook up with someone I don't like.":
            "I'd be mad too if my own cousin had ignored me like that just to try to hook up with someone I don't like.",
        
        # AU script5:7981 (p)
        "So... did you need anything, or were you just missing me?":
            "So... did you need anything, little cuz? Or were you just missing me?",
        
        # AU script5:7990 (p)
        "And you thought of asking your big titty blonde bimbo friend to lend you hers, right?":
            "And you thought of asking your big titty blonde bimbo cousin to lend you hers, right?",
        
        # AU script5:8022 (p)
        "And I need to wash my hair before it's too late! See ya!":
            "And I need to wash my hair before it's too late! See ya, cuzzy!",
        
        # AU script5:8317 (p)
        "I came with Penelope. I live with her, as part of the Student Exchange Program.":
            "I came with Penelope. I- uhh, I live with her, as part of the Student Exchange Program.",
        
        # AU script5:9062 (p)
        "Okay, it's about that damn yearbook.":
            "Okay, it's about that damn yearbook. I just didn't wanna get you mixed up in this.",
        
        # AU script5:9088 (p)
        "*Giggles* I knew I could count on you.":
            "*Giggles* I knew I could count on you, little cuz.",
        
        # AU script5:9149 (p)
        "Don't be such a bore! Where did you leave your spine, [mc]?":
            "Don't be such a bore! Where did you leave your spine, little cuz?",
        
        # AU script5:9217 (p)
        "But... wait, she's {i}interested{/i}?":
            "But... w-wait, she's {i}interested{/i}?",
        
        # AU script5:9218 (p)
        "What do you know? Did she tell you anything?":
            "What do you know? D-Did she tell you anything?",
        
        # AU script5:9303 (p)
        "Just a friend who's gonna help me sneak into the dorm room of someone who stole something from me.":
            "Just a kid who's gonna help me sneak into the dorm room of someone who stole something from me.",
        
        # AU script5:9505 (p)
        "*Whispering* I'm sorry I dragged you into this, [mc].":
            "*Whispering* I'm sorry I dragged you into this, cuz.",
        
        # AU script5:9577 (p)
        "My fucking god, [mc], you're hung like a fucking horse. That cock is a weapon!":
            "My fucking god, little cuz, you're hung like a fucking horse. That cock is a weapon!",
        
        # AU script5:9630 (p)
        "I'm {i}so{/i} very sorry for flaunting my lewd body in front of you, [mc]. I had no idea it would cause you so much stress...":
            "I'm {i}so{/i} very sorry for flaunting my lewd body in front of you, little cousin. I had no idea it would cause you so much stress...",
        
        # AU script5:9670 (p)
        "Okay, take a good look, [mc].":
            "Okay, take a good look, little cuz.",
        
        # AU script5:9681 (p)
        "Do you forgive me for acting naughty? For being such a tease? For flaunting myself all around you?":
            "Do you forgive me for acting naughty? For being such a tease? For flaunting myself all around my own cousin?",
        
        # AU script5:9725 (p)
        "You move closer to Penelope, frantically trying to memorize every square inch of the model’s ethereal body.":
            "You move closer to Penelope, frantically trying to memorize every square inch of your cousin’s ethereal body.",
        
        # AU script5:9747 (p)
        "*Giggles* You're crazy, [mc]...":
            "*Giggles* You're crazy, little cuz...",
        
        # AU script5:9750 (p)
        "You wrap your arms around Penelope's waist, holding her in place with a firm grip before beginning to suck on the blonde's voluptuous breasts.":
            "You wrap your arms around Penelope's waist, holding her in place with a firm grip before beginning to suck on your cousin's voluptuous breasts.",
        
        # AU script5:9765 (p)
        "She's mine... For at least tonight, Penelope Carter is all mine...":
            "She's mine... For at least tonight, my big cousin, Penelope Carter, is all mine...",
        
        # AU script5:9784 (p)
        "*Giggles* You're a filthy little degenerate.":
            "*Giggles* You're a filthy little degenerate, aren't you, cousin?",
        
        # AU script5:9797 (p)
        "*Giggles* Jesus, [mc], how long can you keep up an erection like that?":
            "*Giggles* Jesus, cuz, how long can you keep up an erection like that?",
        
        # AU script5:9813 (p)
        "What if it slips out of your costume again? We can’t have Nova or another girl accidentally catching sight of this monster dick, can we?":
            "What if it slips out of your costume again? We can’t have Nova or another girl accidentally catching sight of my cousin's monster dick, can we?",
        
        # AU script5:9823 (p)
        "*Giggles* I can imagine. Do you like feeling my big titties wrapped around your cock like this?":
            "*Giggles* I can imagine. Do you like feeling my big titties wrapped around your cock like this, little cousin?",
        
        # AU script5:9841 (p)
        "I rejected all their requests, but here I am doing it for free, for some high school kid with a fat dick.":
            "I rejected all their requests, but here I am doing it for free, for my kid cousin's fat dick.",
        
        # AU script5:9844 (p)
        "But I’m not just some high school kid, y’know...":
            "But I’m not just some kid, y’know...",
        
        # AU script5:9851 (p)
        "Yeah, I guess you can take a shot...":
            "Yeah, I guess you can take a shot, little cuz...",
        
        # AU script5:9859 (p)
        "I'm FUCKING the best tits on Instagram!":
            "I'm FUCKING my cousin's tits! The best tits on Instagram!",
        
        # AU script5:9888 (p)
        "Besides, we don't even have a condom...":
            "Besides, that would be incest. We're blood-related and... w-we don't even have a condom...",
        
        # AU script5:9899 (p)
        "AAaaaah... What are you d-doing to me?":
            "AAaaaah... What are you d-doing to me, c-cuz?",
        
        # AU script5:9910 (p)
        "Do you like this? Gliding your pussy along my cock?":
            "Do you like this? Gliding your pussy along your little cousin's thick cock?",
        
        # AU script5:9927 (p)
        "Your hands wrap around Penelope’s soft neck as you hasten your pace, your hips slamming relentlessly against the blonde's buttocks.":
            "Your hands wrap around Penelope’s soft neck as you hasten your pace, your hips slamming relentlessly against your cousin's buttocks.",
        
        # AU script5:9933 (p)
        "K-Keep up that pace, [mc]...":
            "K-Keep up that pace, cuzzy...",
        
        # AU script5:9954 (p)
        "*Choking* Y-Yeagh... u-use me as your fucking toy, [mc]...":
            "*Choking* Y-Yeagh... u-use me as your fucking toy, little cuz...",
        
        # AU script5:10010 (p)
        "I'm gonna have to ask you to come to all the parties I'm invited to from now on, [mc].":
            "I'm gonna have to ask you to come to all the parties I'm invited to from now on, little cuz.",
        
        # AU script5:10143 (p)
        "What are your plans, [mc]?":
            "What are your plans, cuz?",
        
        # AU script5:10274 (p)
        "Thanks, [mc]. You're a good friend.":
            "Thanks, [mc]. You're a good cousin.",
        
        # AU script5:10276 (p)
        "Hey, that's what friends are for.":
            "Hey, that's what family is for.",
        
        # AU script5:10307 (p)
        "Good night, [mc]...":
            "Good night, little cuz...",
        
        # AU script5:10317 (p)
        "I'm glad to have you as a friend.":
            "I'm glad I have you as my family.",
        
        # AU script5:10483 (n)
        "After all these years, you’re still taking care of me like a babysitter, eh Nancy?":
            "After all these years, you’re still taking care of me like a mother, eh Nancy?",
        
        # AU script5:10599 (n)
        "I'm not a girl, and I'm not Nancy's child.":
            "I'm not a girl, and Nancy isn't my mom. She's my aunt.",
        
        # AU script5:10730 (n)
        "And you, dear [mc]... are going to retrieve that information.":
            "And you, dear nephew... are going to retrieve that information.",
        
        # AU script5:11331 (n)
        "And that's not even taking into account our age difference or my background as your old nanny.":
            "And that's not even taking into account our age difference or the fact that you're my sister's child, and I raised you like my own son until you were 9 years old.",
        
        # AU script5:11374 (n)
        "Our age difference, my daughters, the Student Exchange Program, my history as your former nanny...":
            "Our age difference, our family, the Student Exchange Program... the fact that you're my sister's child, and I raised you like my own son until you were 9 years old...",
        
        # AU script5:11406 (n)
        "I'll take what I want.":
            "I don't care if it's wrong. I don't care if it's incest. I'll take what I want.",
        
        # AU script5:11446 (n)
        "Let me take care of you...":
            "Let your Auntie Nancy take care of you. You’ve been such a good boy, after all...",
        
        # AU script5:11458 (n)
        "Oh my, are you not excited enough? Wanna play with my titties in front of your face again?":
            "Oh my, are you not excited enough? Wanna play with my titties in front of your face again, baby boy?",
        
        # AU script5:11502 (n)
        "*Kneeling down* You know, my mother used to say that risk-takers defy destiny with every decision. I’ve always kept that thought in my head.":
            "*Kneeling down* You know, your grandmother used to say that risk-takers defy destiny with every decision. I’ve always kept that thought in my head.",
        
        # AU script5:11636 (n)
        "S-She's about to fuck me!":
            "M-My aunt is about to fuck me!",
        
        # AU script5:11670 (n)
        "Nancy starts moving up and down. Your penis spreads her wet lips apart, while quickly adjusting to the redhead's vicious pace.":
            "Nancy starts moving up and down. Your penis spreads her wet lips apart, while quickly adjusting to your aunt's vicious pace.",
        
        # AU script5:11712 (n)
        "Can you handle me going faster, sweetie? I’ll start slowly... and it’ll make your old babysitter feel so much better...":
            "Can you handle me going faster, sweetie? I’ll start slowly... and it’ll make your Auntie Nancy feel so much better...",
        
        # AU script5:11778 (n)
        "The poor security guard having to watch the two of us – AGH... FUCK! – h-having sweaty, animal sex in an elevator in the middle of the day...":
            "The poor security guard having to watch the two of us – AGH... FUCK! – h-having sweaty, incestuous sex in an elevator in the middle of the day...",
        
        # AU script5:11816 (n)
        "What a naughty mommy... what if your daughters could see you being fucked like this?":
            "What a naughty mommy... what if your daughters could see you being fucked like this by their own cousin?",
        
        # AU script5:11818 (n)
        "What a naughty empress... what if your subjects could see you being fucked like this?":
            "What a naughty empress... what if your subjects could see you being fucked like this by your own nephew?",
        
        # AU script5:11857 (n)
        "Don't worry, my queen, just lean against the wall and let me do the work here...":
            "Don't worry, my queen, just lean against the wall and let your prince do the work here...",
        
        # AU script5:11871 (n)
        "F-Fuck me again, [mc]...":
            "F-Fuck your Auntie again, [mc]...",
        
        # AU script5:11907 (n)
        "[mc] s-s-stop joking!":
            "[mc] s-s-stop joking! Th-this is incest! I-I can't have a baby w{size=40}AAAHHHHhhh{/size}... {w=1.5}w-with my own n-nephew!",
        
        # AU script5:11911 (n)
        "I can’t upset her, though... not if I want to do this again...":
            "I can’t cross that line, though... not if I want to do this again...",
        
        # AU script5:11963 (n)
        "I can't be fired, [mc], I have a family to feed!":
            "I can't be fired, [mc], I have to feed our family!",
        
        # AU script5:12409 (n)
        "You’ve really made the household... authentic. It’s almost like we were missing something before you came back.":
            "You’ve really made our family... authentic. It’s almost like we were missing something before you came back.",
        
        
    # -----------------------------------------
    # 0.6 script6.rpy Nancy aunt/Penelope & Dalia cousin lines
        
        # AU script6:
        
        
    # -----------------------------------------
    # 0.7 script7.rpy Nancy aunt/Penelope & Dalia cousin lines
        
        # AU script7:
        
        
    # -----------------------------------------
    # 0.8 script8.rpy Nancy aunt/Penelope & Dalia cousin lines
        
        # AU script8:
        
        
    # -----------------------------------------
    # 0.9 script9.rpy Nancy aunt/Penelope & Dalia cousin lines
        
        # AU script9:
        
        
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
        # script:0000 = file name:line number
        # (menu) = Choice menu line
        # (chat) = Phone chat line
        # (n) = Nancy line
        # These tags aren't based on who's speaking, but who the line and scene are about.
        # l9/N = Editor's notes
        # -----------------------------------------
        
        
    # -----------------------------------------
    # 0.1 script.rpy Annie stepsister lines
        
        # ST script:1046
        "(Annie is a close friend from my childhood.)":
            "(Annie is my stepsister.)",
        
        # ST script:1047
        "(When I moved from Kredon, she was my next-door neighbor and the first person I met, along with Chang.)":
            "(After we moved from Kredon, she and her mother were our next-door neighbors, and she was the first person I met, along with Chang.)",
        
        # ST script:1049
        "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them.)":
            "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them, especially after they divorced.)",
        
        # ST script:1050
        "(We were both lost... and lonely.)":
            "(Even after my dad and her mom got remarried, nothing changed. We were both lost... and lonely.)",
        
        # ST script:1053
        "(Because of how close we were, people always believed we were dating... but the truth is, we're just friends.)":
            "(Because of how close we were, people always assumed we were dating... but the truth is, we're just siblings. Stepsiblings.)",
        
        # ST script:1054
        "(I mean… she's cute, and we love spending time with each other, but I've never tried to make a move on her.)":
            "(I mean… she's cute, and we love spending time with each other, but she's my little sister. I'd never try to make a move on her.)",
        
        # ST script:1059
        "(It would be... weird for us. Yeah! That's the word. Weird.)":
            "(It would be... weird for us. Yeah! What would our parents say?)",
        
        # ST script:1060
        "(It's just not the kind of relationship we have.)":
            "(She's my family, and we'll always be close friends. It's just not the kind of relationship we have.)",
        
        # ST script:1179
        "You're nothing but a big ball of envy because your best friend can play Eternum and you can't since you didn't save any money.":
            "You're nothing but a big ball of envy because your one-and-only little sister and best friend can play Eternum and you can't since you didn't save any money.",
        
        # ST script:1233
        "I guess it would be you, Annie.":
            "I guess it would be you, sis.",
        
        # ST script:1254
        "You're my best... male friend!":
            "You're my best... bro!",
        
        # ST script:1262
        "Ahh, it's a deal, my friend!":
            "Ahh, it's a deal, brother!",
        
        # ST script:1344
        "I know you're excited Annie, but I'd appreciate it if you could at least carry your hand baggage!":
            "I know you're excited sis, but I'd appreciate it if you could at least carry your hand baggage!",
        
        # ST script:1757
        "Mission failed, [mc]...":
            "Mission failed, bro...",
        
        # ST script:1970
        "Oh, and you must be Annie! Nice to meet you too!":
            "Oh, and you must be Annie, [mc]'s stepsister! Nice to meet you too!",
        
        # ST script:2799
        "(I guess I should let them walk to school on their own, since I don't wanna look like a jealous boyfriend or something.)":
            "(I guess I should let them walk to school on their own, since I don't wanna look like an overprotective older brother or something.)",
        
        # ST script:2816
        "(Bah, Annie's a big girl. She doesn't need protecting.)":
            "(Bah, Annie isn't my baby sister anymore. She doesn't need protecting.)",
        
        # ST script:2910
        "The lady said no, buddy.":
            "Hands off my little sister, buddy. The lady said no.",
        
        # ST script:2934
        "The lady said no.":
            "Hands off my little sister. The lady said no.",
        
        # ST script:2952 and script4:4803
        "Are you okay, Annie?":
            "Are you okay, sis?",
        
        # ST script:3006
        "And... thank you again for helping me out back there, [mc].":
            "And... thank you again for helping me out back there, big bro.",
        
        # ST script:5178
        "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal when I was living with my dad.":
            "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal when I was living with my dad and stepmom.",
        
        # ST script:6697
        "So this is the [mc] you're always talking about?":
            "So this is the {i}big brother{/i} you're always talking about?",
        
        # ST script:7130
        "(That's a bad idea...)":
            "(That's a bad idea... she's my little sister.)",
        
        # ST script:7176
        "(Jeez, I've always tried to not think of Annie in \"that\" way because I don't want to ruin our friendship, but now...)":
            "(Shit, I've always tried to not think of Annie in \"that\" way because I don't want to ruin our relationship, but now...)",
        
        # ST script:7186
        "(Damn... I guess she’s not the skinny kid she used to be...)":
            "(Damn... I guess she’s not the skinny baby sister she used to be...)",
        
        # ST script:8102
        "Erm... Y-You're the best friend ever!":
            "Erm... Y-You're the best brother ever!",
        
        # ST script:8468
        "The pleasure was all mine, Annie. Eternum is awesome. I’m so grateful I had you by my side.":
            "The pleasure was all mine, little sis. Eternum is awesome. I’m so grateful I had you by my side.",
        
        
    # -----------------------------------------
    # 0.2 script2.rpy Annie stepsister lines
        
        # ST script2:106
        "*Laughs* Don't mind him...":
            "*Laughs* Don't mind my brother...",
        
        # ST script2:138
        "*Laughs* Come on, the last time we watched a horror movie, you couldn’t sleep alone for an entire two weeks!":
            "*Laughs* Come on, sis! The last time we watched a horror movie, you couldn’t sleep alone for an entire two weeks!",
        
        # ST script2:1014
        "Annie should be waiting for us already.":
            "Your sister should be waiting for us already.",
        
        # ST script2:3408
        "Oh, [mc]! I wasn’t sure if you were asleep already!":
            "Oh, hey bro! I wasn’t sure if you were asleep already!",
        
        # ST script2:3418
        "I told you! You shouldn't have played in Luna's server, Annie! You can't handle that scary stuff! Remember when we played Dead Space?":
            "I told you! You shouldn't have played in Luna's server, sis! You can't handle that scary stuff! Remember when we played Dead Space?",
        
        # ST script2:3474
        "You can sleep here as many times as you want. You don’t even have to ask, alright?":
            "You can sleep here as many times as you want. You don’t even have to ask, alright? Just like when we were little.",
        
        # ST script2:3479
        "Anytime, Annie.":
            "Anytime, sis.",
        
        # ST script2:3504
        "G-Goodnight, [mc].":
            "G-Goodnight, bro.",
        
        # ST script2:3506
        "Goodnight Annie.":
            "Goodnight sis.",
        
        # ST script2:3530
        "(We're in quite an... intimate position... I don't want her to think I'm trying to take advantage of her while she sleeps.)":
            "(We're in quite an... intimate position... I don't want her to think her brother is trying to take advantage of her while she sleeps.)",
        
        # ST script2:3557
        "Baloo?":
            "Mr. Baloo? That teddy bear your mom gave you when you were 5?",
        
        # ST script2:3559
        "Oh... Well... It's a stuffed bear that my mother gave me when I was 5, and...":
            "Y-yeah, Mr. Baloo...",
        
        # ST script2:3564
        "Oh... I didn't know about Baloo.":
            "Oh... I didn't know you still had him.",
        
        # ST script2:3594
        "(He probably just sees me as the little girl who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)":
            "(He probably just sees me as the little sister who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)",
        
        # ST script2:3595
        "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack.)":
            "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack. Not a weirdo like me who has feelings for her own big brother...)",
        
        # ST script2:3596
        "(I'll always just be Annie, the \"best friend\".)":
            "(I'll always just be Annie, the \"little sister\".)",
        
        # ST script2:3602
        "(I'm a fucking mess. She needs someone more mature.)":
            "(I'm a fucking mess. She needs someone more mature... not a creep who has a crush on his little sister.)",
        
        # ST script2:3603
        "(This is why I'll always just be [mc], the \"best friend\"...)":
            "(This is why I'll always just be [mc], the \"big brother\"...)",
        
        # ST script2:3631
        "It’s just a shirt after all, right...?":
            "It’s just a shirt after all, right...? You've seen me without it before...",
        
        # ST script2:3633
        "(I'm not sure where she’s going with all of this...)":
            "(The last time I saw her topless was when we were 9 and still bathing together, though...)",
        
        # ST script2:3634
        "(But I sure as hell want to find out...)":
            "(I'm not sure where she’s going with all of this... but I sure as hell want to find out...)",
        
        # ST script2:3642
        "(This doesn't seem like the Annie I’ve known since I was young... Is she trying to prove something?)":
            "(This doesn't seem like my sister... Is she trying to prove something?)",
        
        # ST script2:3647
        "(Holy shit, I’ve never seen her in such an... intimate way...)":
            "(Holy shit, I never noticed know how much she had... grown up...)",
        
        # ST script2:3652
        "(This is really Annie... {i}my{/i} Annie.)":
            "(This is really my sister... {i}my{/i} sister.)",
        
        # ST script2:3658
        "We're just... friends getting a little more comfortable.":
            "We're just... siblings getting a little more comfortable.",
        
        # ST script2:3703
        "Your skin feels so soft, Annie. It feels... really nice holding you...":
            "Your skin feels so soft, sis. It feels... really nice holding you...",
        
        # ST script2:3711
        "(Oh my god, am I the only one feeling all this tension in the air? I want to make a move, but... I don’t want to overstep my bounds...)":
            "(Oh my god, am I the only one feeling all this tension in the air? I want to make a move, but... I really don’t want to overstep my bounds...)",
        
        # ST script2:3718
        "(But it’s not just any guy. It’s [mc].)":
            "(But it’s not just any guy. It’s [mc]. Your big brother.)",
        
        # ST script2:3721
        "(But... I don't want to scare her away. Annie has always been so special to me. If I try something and it doesn't work out, I couldn’t bear the thought of losing her...)":
            "(But... I don't want to scare her away. Annie has always been more than a friend, more than a sister to me. If I try something and it doesn't work out, I couldn’t bear the thought of losing her...)",
        
        # ST script2:3722
        "(I can’t deny it... I want more of him...)":
            "(I can’t deny it, I want more of him... I mean, we aren’t even blood-related...)",
        
        # ST script2:3729
        "(Baby steps, [mc]. Baby steps.)":
            "(A-And this all still feels so wrong... we shouldn't go any further than this... {w}right...?)",
        
        # ST script2:3740
        "Um... Annie...?":
            "Um... sis...?",
        
        # ST script2:3763
        "I’m sorry, Annie... I can’t help it... you’re driving me insane...":
            "I’m sorry, sis... I can’t help it... you’re driving me insane...",
        
        # ST script2:3800
        "[mc]. I said I’m nervous, but that doesn’t mean I... don’t want to...":
            "Big bro. I said I’m nervous, but that doesn’t mean I... don’t want to...",
        
        # ST script2:3826
        "I thought you weren’t interested in me...":
            "I thought you weren’t interested in me... I was just your little sister...",
        
        # ST script2:3828
        "Where did you get that idea from?":
            "Annie, you've never been {i}just{/i} my little sister.",
        
        # ST script2:3829
        "You're perfect.":
            "You're... perfect.",
        
        # ST script2:3830
        "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our friendship.":
            "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our relationship as brother and sister.",
        
        # ST script2:3840
        "*Chuckles* You know I’m not one to break my promises.":
            "*Chuckles* You know I’m not one to break my promises, sis.",
        
        # ST script2:3867
        "(Holy shit, this is really happening! I'm fucking Annie's thighs!)":
            "(Holy shit, this is really happening! I'm fucking my little sister's thighs!)",
        
        # ST script2:3870
        "(I never would’ve thought I’d have a chance with him...)":
            "(I never would’ve thought I’d have a chance to do this with my big brother...)",
        
        # ST script2:3872
        "Jesus, Annie...":
            "Jesus, sis...",
        
        # ST script2:3924
        "Oh shit, I'm sorry, Annie...":
            "Oh shit, I'm sorry, sis...",
        
        # ST script2:3942
        "I only came here t-to sleep and then... next thing I know I’m doing that...":
            "I only came here t-to sleep and then... next thing I know I’m doing that... with my big brother!",
        
        # ST script2:3946
        "I started m-moving and then I c-couldn't stop and... now I’m not going to have my fairy tale ending... because what kind of Disney princess romance begins with a THIGH JOB?! AHAHAH!!":
            "I started m-moving and then I c-couldn't stop and... now I’m not going to have my fairy tale ending... because what kind of Disney princess romance begins with a BROTHER-SISTER THIGH JOB?! AHAHAH!!",
        
        # ST script2:3952
        "We skipped like 14 steps! In one night!":
            "We skipped like 14 steps and broke a dozen rules! In one night!",
        
        # ST script2:3964
        "I'm gonna... go... think! Good night [mc]!":
            "I'm gonna... go... think! Good night bro!",
        
        # ST script2:3981
        "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing Annie’s secret kinky side... and I loved every moment of it!)":
            "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing my sister's secret kinky side... it felt so wrong... and I loved every moment of it!)",
        
        # ST script2:5413 (n)
        "(I bet if I tried to do anything at home, Dalia or Penny would surely notice.)":
            "(I bet if I tried to do anything at home, one of the girls would surely notice.)",
        
        # ST script2:5937
        "And on the first day of school, I saw him harassing a close friend of mine.":
            "And on the first day of school, I saw him harassing my sister.",
        
        # ST script2:6103
        "I never met my mother and my father was always absent in my life. He was constantly too occupied with his work.":
            "I never met my mother, and my father and stepmother were always absent in my life. They were constantly too occupied with their work.",
        
        
    # -----------------------------------------
    # 0.3 script3.rpy Annie stepsister lines
        
        # ST script3:3343
        "Not a worry in mah noggin, homie. I just be... chillaxin’ all day! Yeahhhh...":
            "Not a worry in mah noggin, bro. I just be... chillaxin’ all day! Yeahhhh...",
        
        # ST script3:3402
        "(That's all I want... just to stay friends with her.)":
            "(That's all I want... just to be brother and sister again.)",
        
        # ST script3:3428
        "I've liked you ever since we were 10. If I’m being real with you, the only reason why I was willing to come back to Kredon at all was because you were coming too.":
            "I've liked you ever since we were 10. If I’m being real with you, the only reason why I was willing to come back to Kredon at all was because you were coming with me.",
        
        # ST script3:3431
        "You're my best friend.":
            "You're my little sister and my best friend.",
        
        # ST script3:3434
        "And in my heart I know, I want us to be so much more than that, too...":
            "And in my heart I know, even if it's wrong, I want us to be so much more than that, too...",
        
        # ST script3:3439
        "And, as much as I loved that night, I know things might’ve felt like they were moving way too fast for you.":
            "And, as much as I loved that night, I think we both felt like things were moving way too fast.",
        
        # ST script3:3446
        "I don't want to lose our friendship, Annie. I’d be miserable without you in my life.":
            "I don't want to lose you, sis. I’d be miserable without you in my life.",
        
        # ST script3:3449
        "I just want us to stay friends forever!":
            "I just want us to stay together forever!",
        
        # ST script3:3467
        "That sounds great! Just spending some time together as good friends. Like how we’ve always done it!":
            "That sounds great! Just spending some time together as siblings. Like how we’ve always done it!",
        
        # ST script3:3483
        "Like... a fun date between friends?":
            "Like... a fun date between siblings?",
        
        # ST script3:3484
        "Hmmm... no, more like a date with a girl that I like. And I just happen to be so lucky in that, she’s also my best friend too. As for what the future holds? Who knows...":
            "Hmmm... no, more like a date with a girl that I like. And it just happens to be that she’s also my adorable little sister, and my best friend too. As for what the future holds? Who knows...",
        
        # ST script3:3511
        "And not a word to anyone. I mean... there's no need for it, really. We’re just two people going on a date, and there’s no need to overthink it.":
            "And not a word to anyone. I mean... there's no need for it, really. We’re just two {i}totally non-blood-related{/i} people going on a date, and there’s no need to overthink it.",
        
        # ST script3:3540
        "I know you want to take things slow. And I’m perfectly okay with that.":
            "I know you want to take things slow, sis. And I’m perfectly okay with that.",
        
        # ST script3:3561
        "That was quite the goodbye for just a couple of... friends.":
            "That was quite the goodbye for just a brother and sister...",
        
        # ST script3:9866 (n)
        "I think this goes without saying, but let’s not mention this to anyone. My daughters especially... heaven knows what they’d think if they learned we bathed together.":
            "I think this goes without saying, but let’s not mention this to anyone. My daughters and your stepsister especially... heaven knows what they’d think if they learned we bathed together.",
        
        
    # -----------------------------------------
    # 0.4 script4.rpy Annie stepsister lines
        
        # ST script4:4335
        "(A date with [mc]!)":
            "(A date with my big brother!)",
        
        # ST script4:4336
        "(A date in Eternum WITH [mc]!)":
            "(A date in Eternum WITH my big brother!)",
        
        # ST script4:4914
        "I feel so comfortable with Annie that sometimes I forget we're not really... a couple.":
            "I feel so comfortable with Annie that sometimes I forget we're just siblings, not really a... a couple.",
        
        # ST script4:5004
        "You and Chang have always been my best friends, and neither of you played Eternum until recently, so... I've always felt kind of alone here.":
            "You and Chang have always been by my side, and neither of you played Eternum until recently, so... I've always felt kind of alone here.",
        
        # ST script4:5008
        "You’re the one who’s really made these first few weeks in Eternum worthwhile, Annie. I couldn't have asked for anyone better to spend time with.":
            "You’re the one who’s really made these first few weeks in Eternum worthwhile, sis. I couldn't have asked for anyone better to spend time with.",
        
        # ST script4:5131
        "Oh! Come on, Annie! You can't be serious!":
            "Oh! Come on, sis! You can't be serious!",
        
        # ST script4:5250
        "(Maybe... it's just not the right time yet...?)":
            "(Maybe... was this all a mistake...?)",
        
        # ST script4:5311 and Multi-Mod script4:5339 and Bonus Mod script4:5366 (menu)
        "Decline and stay as friends":
            "{color=[walk_path]}Decline and stay as stepsiblings [red][mt](Closes Annie's path)",
        
        # ST script4:5314
        "I like you, and you're my best friend, you already know that.":
            "I like you, and you're my beloved little sister and my best friend. You already know that.",
        
        # ST script4:5315
        "But... I also feel like we're not meant to be more than that. Things would get awkward if we tried to get together, and our friendship is too important to risk, for me at least.":
            "But... I also feel like we're not meant to be more than that. Things would get so complicated if we tried to get together as stepsiblings, and our friendship, our {i}family{/i}, is too important to risk, for me at least.",
        
        # l9/N: I completely rewrote the next four lines.
        # This is the biggest change I've made so far in the writing, beyond just adding incest themes. I felt like this scene needed more conversation and emotional weight, especially for his little sister. He sounds way too flippant in the original. The theme is, "Maybe MC is right and this would ruin their relationship... or maybe he's just growing up and scared of change. But he's definitely not mature enough to deal with it now."
        # Shit, it took me a whole afternoon to think of what to say to her, and 99% of players won't even see it. I'll try not to make these rewrites a habit, since I also think it's important to preserve the original writing.
        
        # ST script4:5316
        "I just like spending time with you!":
            "I just... Annie, I don’t want these feelings to overwrite all the memories and the relationship we’ve built until now.",
        
        # ST script4:5317
        "I... I think we're meant to be friends. Best friends!":
            "Sometimes, when I look at you, I don’t recognize the Annie I’ve always known.",
        
        # ST script4:5318
        "So... let's just stay like this for now, okay?":
            "Sometimes, I don’t recognize myself.",
        
        # ST script4:5319
        "I just don’t have those feelings for you right now.":
            "It feels like we’re on the edge of losing something we’ve always had, and I’m...{w}{i}{size=27} I-I’m scared we’ll never get it back.",
        
        # ST script4:5320
        "In the future... who knows? Maybe. But I don’t want to lead you on, either.":
            "I can’t commit to this... {i}thing{/i} between us. Not right now. In the future... I don’t know. Maybe. But I don’t want to lead you on, either.",
        
        # ST script4:5326
        "No worries! I totally understand. My head has been all over the place too, you know, with all this back and forth...":
            "It's not your fault, Annie, it's mine. I know I've been sending you mixed signals, bringing you here today. My head has been all over the place too, you know, with all this back and forth...  You don't deserve that.",
        
        # ST script4:5327
        "We can have this conversation again after we gather the 10 Gems!":
            "I'm sorry, sis. This isn't how I wanted today to go. For what it's worth, I still enjoyed spending this time with you.",
        
        # ST script4:5369
        "Y-Yeah... It's been like... 10 years since we first met?":
            "Y-Yeah... It's been like... 10 years since we became family?",
        
        # ST script4:5405
        "Seeing you undressing just for me was hot as fuck, Annie.":
            "Seeing you undressing just for me was hot as fuck, sis.",
        
        # ST script4:5436
        "But... Do you think I'm NOT nervous? I'm super scared too! I mean, in my arms, I'm holding an adorably precious, absolutely gorgeous girl whom I’ve liked for years.":
            "But... Do you think I'm NOT nervous? I'm super scared too! I mean, in my arms, I'm holding my adorably precious, absolutely gorgeous little sister whom I’ve liked for years.",
        
        # ST script4:5438
        "I know it's scary to get out of your comfort zone, but... I think we can overcome it together.":
            "After so long together, I know it's scary to go outside what's familiar to us, but... I think we can overcome it together.",
        
        # ST script4:5442
        "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay friends!":
            "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay as siblings and friends!",
        
        # ST script4:5443
        "It’ll be a little awkward at first, but our friendship is strong, and I know we’d be back to normal in no time.":
            "It’ll be a little awkward at first, but our relationship is strong, and I know we’d be back to normal in no time.",
        
        # ST script4:5447
        "I know it's scary to cross this bridge when you're not sure what your partner might want, so let me be clear...":
            "I know it's scary to cross this bridge when you're not sure what your partner might want, or what our relationship is even supposed to be, so let me be clear...",
        
        # ST script4:5449
        "You are so ridiculously pretty, Annie, that I can’t help but want to take our relationship to the next level.":
            "You’re my beloved little sister and my best friend, and that part of us will never change. But... you’re so ridiculously pretty, Annie, that I can’t help but want to take our relationship to the next level.",
        
        # ST script4:5471
        "*Caressing her cheek* I feel like I could never get enough of you, Annie...":
            "*Caressing her cheek* I feel like I could never get enough of you, sis...",
        
        # ST script4:5518
        "Have I been fooled all these years? Innocent, shy Annie is actually a horny, perverted little girl?":
            "Have I been fooled all these years? My innocent, shy sister is actually a horny, perverted little girl?",
        
        # ST script4:5526
        "God, there are so many things I want to do to Annie right now... but it's still Annie. I don't wanna cross any line too fast.":
            "God, there are so many things I want to do to Annie right now... but she's still my little sister. I don't wanna cross any line too fast.",
        
        # ST script4:5562
        "It'll only get better from here, babe...":
            "It'll only get better from here, sis...",
        
        # ST script4:5604
        "*Panting* K-Keep going, [mc]! Y-You’re hitting just the... r-right spot!":
            "*Panting* K-Keep going, b-big bro! Y-You’re hitting just the... r-right spot!",
        
        # ST script4:5619
        "W-What are you *moans* doooooing to m-me...?":
            "W-What are you *moans* doooooing to m-me, b-big brotheeeerrrr...?",
        
        # ST script4:5624
        "Don't worry, babe...":
            "Don't worry, sis...",
        
        # ST script4:5665
        "([mc] made me... {i} cum{/i}!)":
            "(My big brother made me... {i} cum{/i}!)",
        
        # ST script4:5682
        "Of course you can see it... After all, you’re responsible for it...":
            "Of course you can see it, little sis... After all, you’re responsible for it...",
        
        # ST script4:5724
        "You’re such a good girl, Annie...":
            "You’re such a good little sister, Annie...",
        
        # ST script4:5758
        "I love beating off your... massive... pulsing... d-dirty cock...":
            "I love beating off my b-big brother's... massive... pulsing... d-dirty cock...",
        
        # ST script4:5765
        "*Panting* F-Fuck, I won't last much longer, Annie...":
            "*Panting* F-Fuck, I won't last much longer, sis...",
        
        # ST script4:5767
        "I want to make you cum, [mc]... You were so kind to me...":
            "I want to make you cum, big bro... You were so kind to me...",
        
        # ST script4:5823
        "I want you so bad, Annie... I can’t wait ‘til the day you can finally take this dick... But not yet...":
            "I want you so bad, sis... I can’t wait ‘til the day you can finally take this dick... But not yet...",
        
        # ST script4:5825
        "W-We’ve g-gotta do some practicing b-beforehand, [mc]...":
            "W-We’ve g-gotta do some practicing b-beforehand, b-bro...",
        
        # ST script4:6924
        "Oh Annie... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?":
            "Oh sis... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?",
        
        # ST script4:7250
        "Thank you for an amazing day, [mc].":
            "Thank you for an amazing day, big bro.",
        
        # ST script4:7252
        "I'm glad you enjoyed it, Annie. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.":
            "I'm glad you enjoyed it, sis. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.",
        
        # ST script4:7431
        "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what best friends do, I guess.":
            "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what family does, I guess.",
        
        
    # -----------------------------------------
    # 0.5 script5.rpy Annie stepsister lines
        
        # ST script5:842
        "I don't really mind anymore. I'm happy being just a good friend.":
            "I don't really mind anymore. I'm happy just being his little sister.",
        
        # ST script5:12104 (n)
        "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters would take the news.":
            "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters or your sister would take the news.",
        
        
    # -----------------------------------------
    # 0.6 script6.rpy Annie stepsister lines
        
        # ST script6:
        
        
    # -----------------------------------------
    # 0.7 script7.rpy Annie stepsister lines
        
        # ST script7:
        
        
    # -----------------------------------------
    # 0.8 script8.rpy Annie stepsister lines
        
        # ST script8:
        
        
    # -----------------------------------------
    # 0.9 script9.rpy Annie stepsister lines
        
        # ST script9:
        
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
        _in_chat_speaker_override
    except NameError:
        _in_chat_speaker_override = None
    try:
        _in_ast_module = renpy.ast
    except Exception:
        _in_ast_module = None

    def _normalize_who(who):
        if who is None:
            return None
        return str(getattr(who, "name", who)).strip()

    def _in_build_mc_override():
        """
        Resolve the best-known MC speaker tuple for override contexts
        (e.g. chat bubbles rendered outside say statements).
        """
        store = renpy.store
        fallback = (None, "mc")
        try:
            for attr in ("mc", "mct", "mcd", "mcsc"):
                obj = getattr(store, attr, None)
                if obj is not None:
                    return (obj, _normalize_who(obj) or attr)
        except Exception:
            pass
        return fallback

    def _in_chat_hint_is_mc(hint):
        if hint is None:
            return False
        if isinstance(hint, bool):
            return bool(hint)
        if isinstance(hint, str):
            norm = hint.strip().lower()
            return norm in ("mc", "mct", "mcd", "mcsc", "[mc]", "you", "player")
        return False

    def _in_normalize_speaker_hint(hint):
        """
        Normalize any hint value into a (who_obj, who_name) tuple.
        Falls back to (None, None) to explicitly indicate 'not MC'.
        """
        if hint is None:
            return (None, None)
        if isinstance(hint, tuple) and len(hint) == 2:
            who_obj, who_name = hint
            norm_name = _normalize_who(who_obj)
            if not norm_name:
                if isinstance(who_name, str):
                    who_name = who_name.strip()
                norm_name = who_name if who_name else None
            return (who_obj, norm_name)
        if hasattr(hint, "name"):
            return (hint, _normalize_who(hint))
        if isinstance(hint, str):
            stripped = hint.strip()
            return (None, stripped or None)
        try:
            return (None, str(hint))
        except Exception:
            return (None, None)

    def _in_current_speaker():
        """
        Identify the active speaker while the say/menu filter runs.
        Ren'Py updates last_say() *after* the filter executes, so we look up
        the current AST node directly to determine who is talking.
        """
        global _last_say_who
        global _last_say_who_name
        global _in_chat_speaker_override
        override = _in_chat_speaker_override
        if override is not None:
            return override
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
        try:
            _im_sync_adad_alias()
        except Exception:
            pass
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

    def _in_chat_display_text(text, speaker_hint=None):
        """
        Apply incest replacements for chat message text.
        Keeps replace_text off for chat_log, chat, and
        chat_answers to avoid UI lag.
        """
        if not isinstance(text, str):
            return text
        if text.startswith("{image=") and text.endswith("}"):
            return text
        try:
            sanitized = _im_strip_multimod_tags(text)
            sanitized = _im_strip_bonusmod_tags(sanitized)
        except Exception:
            sanitized = text
        if not _in_any_mode_active():
            return sanitized
        force_mc = _in_chat_hint_is_mc(speaker_hint)
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
            sanitized,
            mc_display,
            lastname_display,
            getattr(renpy.store, 'annie_incest', False),
            getattr(renpy.store, 'annie_sister', False),
            getattr(renpy.store, 'annie_mom', False),
            getattr(renpy.store, 'annie_half_sister', False),
            getattr(renpy.store, 'annie_aunt', False),
            force_mc,
        )
        if key in cache:
            return cache[key]

        global _in_chat_speaker_override
        prev_override = _in_chat_speaker_override
        if force_mc:
            override_target = _in_build_mc_override()
        else:
            override_target = _in_normalize_speaker_hint(speaker_hint)
        if override_target is None:
            override_target = (None, None)
        _in_chat_speaker_override = override_target
        try:
            out = _in_transform_text(sanitized)
        finally:
            _in_chat_speaker_override = prev_override
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
        "Which Incest Mode would you like to use? (You can always toggle it in the Preferences menu.)"
        "Full Incest (Nancy as Mom and Annie as sister)":
            $ im_incest_mode = "incest"
        "I only want Nancy as Mom":
            $ im_incest_mode = "mom"
        "I only want Annie as sister (coming soon)":
            $ im_incest_mode = "sister"
        "Nancy as Mom and Annie as half-sister":
            $ im_incest_mode = "half"
        "Nancy as aunt and Annie as stepsister (coming soon)":
            $ im_incest_mode = "aunt"
        "Disabled":
            $ im_incest_mode = "off"
    # menu:
    #     "Do you want a cousin?"
    #     "Yes":
    #         $ im_cousin_override = True
    #         $ persistent.im_cousin_override = True
    #     "No":
    #         $ im_cousin_override = False
    #         $ persistent.im_cousin_override = False
    # After flags change, refresh label overrides immediately
    $ _im_apply_incest_mode()
    $ im_apply_label_map()
    $ in_apply_text_map()
    $ _in_incest_prompted = True
    return

# -----------------------------------------
# Re-apply after loading
# -----------------------------------------
label after_load:
    $ _im_apply_incest_mode()
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
    timer 0.01 action Function(_im_apply_incest_mode)
    # Füge eine zusätzliche Bedingung hinzu
    if (
        ((not _in_incest_prompted) or (im_incest_mode == None))
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
                            SetVariable("im_incest_mode", "incest"),
                            Function(_im_apply_incest_mode),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected im_incest_mode == "incest"
                    textbutton _("Nancy as Mom"):
                        action [
                            SetVariable("im_incest_mode", "mom"),
                            Function(_im_apply_incest_mode),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected im_incest_mode == "mom"
                    textbutton _("Annie as Sister"):
                        action [
                            SetVariable("im_incest_mode", "sister"),
                            Function(_im_apply_incest_mode),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected im_incest_mode == "sister"
                    textbutton _("Mom+Half-Sister"):
                        action [
                            SetVariable("im_incest_mode", "half"),
                            Function(_im_apply_incest_mode),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected im_incest_mode == "half"
                    textbutton _("Aunt+Stepsister"):
                        action [
                            SetVariable("im_incest_mode", "aunt"),
                            Function(_im_apply_incest_mode),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected im_incest_mode == "aunt"
                    textbutton _("Disabled"):
                        action [
                            SetVariable("im_incest_mode", "off"),
                            Function(_im_apply_incest_mode),
                            Function(im_apply_label_map),
                            Function(in_apply_text_map),
                        ]
                        selected im_incest_mode == "off" or im_incest_mode == None

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
                                                text _in_chat_display_text(message.text, message.who)

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

                                        text _in_chat_display_text(msg.text, msg.who)

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

                                    text _(_in_chat_display_text(msg.text, "mc")):
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

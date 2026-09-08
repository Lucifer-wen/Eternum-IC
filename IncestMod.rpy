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
default persistent.motion = 1.0
default persistent.im_reload_hotkey_enabled = True
default _im_reloading_scripts = False
# Dev tools
default persistent.im_dev_text_indicator = False
default _im_dev_text_modified = False
default persistent.im_dev_node_loc = False
default _im_dev_node_loc = (None, None)
default _im_post_say_pending = []
default _im_injection_queued = False
default _im_executing_injection = False
default _im_in_say_call = False
# default persistent.im_cousin_override = None

# -----------------------------------------
# Auto-install presplash (runs on every launch so fresh installs work too)
# Presplash is shown before init code, so the new images take effect from
# the SECOND launch onward – no manual file copying required.
# -----------------------------------------
init python:
    import os as _os
    import shutil as _shutil

    def _im_install_presplash():
        try:
            gamedir = renpy.config.gamedir
            # Find any mod subdirectory that contains a presplash folder,
            # regardless of what the mod folder is called.
            mod_presplash_dir = None
            try:
                for entry in _os.listdir(gamedir):
                    candidate = _os.path.join(gamedir, entry, "presplash")
                    if _os.path.isdir(candidate):
                        mod_presplash_dir = candidate
                        break
            except Exception:
                pass
            if mod_presplash_dir is None:
                return
            pairs = [
                ("presplash_background_IC", "presplash_background"),
                ("presplash_foreground_IC", "presplash_foreground"),
            ]
            for src_base, dst_base in pairs:
                for ext in (".png", ".jpg"):
                    src = _os.path.join(mod_presplash_dir, src_base + ext)
                    if _os.path.exists(src):
                        dst = _os.path.join(gamedir, dst_base + ext)
                        try:
                            if _os.path.exists(dst):
                                src_stat = _os.stat(src)
                                dst_stat = _os.stat(dst)
                                if (
                                    src_stat.st_size == dst_stat.st_size
                                    and int(src_stat.st_mtime) == int(dst_stat.st_mtime)
                                ):
                                    break
                            _shutil.copy2(src, dst)
                        except Exception:
                            # Best effort only. Presplash is cosmetic and should
                            # never slow or block startup if filesystem access fails.
                            pass
                        break
        except Exception:
            pass

    _im_install_presplash()

init python:
    # Cache results of renpy.loadable() checks — these never change after game start.
    _im_multimod_present = None
    _im_bonusmod_present = None

    def _im_strip_multimod_tags(text, *, force=False):
        """
        Remove unsupported multi-mod tags (e.g. [gr]) when
        MultiMod is not installed. Prevents NameError crashes if the tag
        isn't defined in the current environment. Set force=True to strip
        tags unconditionally (useful when matching dialogue variants).
        """
        global _im_multimod_present
        try:
            if not force:
                if _im_multimod_present is None:
                    try:
                        _im_multimod_present = renpy.loadable("mod_additions/mod_options.rpy")
                    except Exception:
                        _im_multimod_present = False
                if _im_multimod_present:
                    return text
        except Exception:
            pass
        try:
            t = text
            t = re.sub(r'\[red\]\(Insist\)', '(Insist)', t)
            t = re.sub(r'\(attack afterward\)', '', t)
            t = re.sub(r'\[(?:gr|mm|red|blue|green|pink|mt|nova_pts|nancy_pts|dalia_pts|annie_pts|alex_pts|penelope_pts|luna_pts|calypso_pts)\](?:(?:\{[^{}]+\})?\([^()]+\)(?:\{\/[^{}]+\})?)?', '', t)
            return t.strip()
        except Exception:
            return text

    def _im_define_multimod_tags():
        global _im_multimod_present
        try:
            present = renpy.loadable("mod_additions/mod_options.rpy")
            _im_multimod_present = present
            if present:
                return
        except Exception:
            _im_multimod_present = False
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
        global _im_bonusmod_present
        try:
            if _im_bonusmod_present is None:
                try:
                    _im_bonusmod_present = renpy.loadable("achievements/achievements.rpy")
                except Exception:
                    _im_bonusmod_present = False
            if _im_bonusmod_present:
                return text
        except Exception:
            pass
        try:
            t = text
            t = re.sub(r'\{color=\[(?:walk_points|walk_path|walk_points_chat|walk_path_chat|computer_color|birthday_color|reception_color|read_this_color|leave_color|stand_up_color|right_elevator_color|left_elevator_color)\]\}', '', t)
            return t.strip()
        except Exception:
            return text

    def _im_define_bonusmod_tags():
        global _im_bonusmod_present
        try:
            present = renpy.loadable("achievements/achievements.rpy")
            _im_bonusmod_present = present
            if present:
                return
        except Exception:
            _im_bonusmod_present = False
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
            # Immediately discard any queued injections so they don't fire
            # on the next say statement after mode is switched off.
            try:
                if getattr(store, "_im_post_say_pending", None):
                    del store._im_post_say_pending[:]
                store._im_injection_queued = False
            except Exception:
                pass
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

init python:
    import os as _im_os

    # -----------------------------------------------------------------
    # Map-entry helpers: extended format support
    # -----------------------------------------------------------------
    def _im_extract_entry(value):
        # Normalizes all map-value formats to (text, script_spec, injections).
        # "text"                       -> plain string (unchanged)
        # ("text", "script:2452")      -> with script-line filter
        # ("text", 2452)               -> line-number only filter
        # ["text", 'mc "..."', "show"] -> with post-line injections
        # ("text", "script:2452", [])  -> filter + injections
        if isinstance(value, str):
            return (value, None, [])
        if isinstance(value, (list, tuple)):
            items = list(value)
            if not items or not isinstance(items[0], str):
                return None
            text = items[0]
            script_spec = None
            injections = []
            for item in items[1:]:
                if isinstance(item, bool):
                    continue
                if isinstance(item, int):
                    if script_spec is None:
                        script_spec = item
                elif isinstance(item, str):
                    if script_spec is None and ":" in item:
                        script_spec = item
                    else:
                        injections.append(item)
                elif isinstance(item, (list, tuple)):
                    injections.extend(str(x) for x in item if isinstance(x, str))
            return (text, script_spec, injections)
        return None

    def _im_get_current_node_loc():
        """Returns (short_filename_without_ext, linenumber) of the current AST node."""
        try:
            node = renpy.game.script.lookup(renpy.game.context().current)
            line = getattr(node, "linenumber", None)
            fname = getattr(node, "filename", "") or ""
            short = _im_os.path.splitext(_im_os.path.basename(fname))[0]
            return (short, line)
        except Exception:
            return (None, None)

    def _im_script_spec_matches(spec):
        # Returns True if the current AST node matches the script specifier.
        # None           -> always matches
        # int            -> compare linenumber only
        # "script:2452"  -> compare filename short-name + linenumber
        # "2452"         -> compare linenumber only (string form)
        if spec is None:
            return True
        short, line = _im_get_current_node_loc()
        if isinstance(spec, int):
            return line == spec
        s = str(spec).strip()
        if ":" in s:
            parts = s.split(":", 1)
            file_hint = parts[0].strip()
            try:
                target_line = int(parts[1].strip())
            except ValueError:
                return False
            return (short == file_hint) and (line == target_line)
        try:
            return line == int(s)
        except ValueError:
            return False


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
                renpy.notify("Script reload not supported on this build.")
                return
            renpy.reload_script()
        except (renpy.game.UtterRestartException, renpy.game.RestartTopContext):
            # Expected during successful reloads; let Ren'Py handle them.
            # The default statement resets _im_reloading_scripts after restart.
            raise
        except Exception as e:
            msg = "Script reload failed: %s" % (e or e.__class__.__name__)
            try:
                renpy.notify(msg)
            except Exception:
                pass
            try:
                _im_log(msg)
            except Exception:
                pass
        finally:
            # Reset in all cases except a successful restart (which re-raises
            # before reaching here and resets via the default statement).
            _im_reloading_scripts = False

# -----------------------------------------
# Post-line injection: parse + execute + say_callback
# -----------------------------------------
init python:
    import re as _imre  # module-level import; avoids repeated import overhead per injection call

    def _im_parse_injection(s):
        # Parse an injection string into (kind, *args).
        # Supported:
        #   'mc "Text"'             -> ("say", "mc", "Text", None)
        #   'mc "Text" with dis'    -> ("say", "mc", "Text", "dis")
        #   "show train 6"          -> ("show", "train 6", None)
        #   "show train 6 with dis" -> ("show", "train 6", "dis")
        #   "hide train"            -> ("hide", "train", None)
        #   "scene bg r"            -> ("scene", "bg r", None)
        s = s.strip()

        # Strip optional trailing  with <name>
        trans_name = None
        m_with = _imre.search(r'\s+with\s+(\w+)\s*$', s, _imre.IGNORECASE)
        if m_with:
            trans_name = m_with.group(1)
            s = s[:m_with.start()].strip()

        kw_lower = s.lower()
        for kw in ("show ", "hide ", "scene "):
            if kw_lower.startswith(kw):
                return (kw.strip(), s[len(kw):].strip(), trans_name)
        # Audio: "play channel name [fadein N]", "stop channel [fadeout N]", "queue channel name"
        for kw in ("play ", "queue "):
            if kw_lower.startswith(kw):
                rest = s[len(kw):].strip().split(None, 1)
                channel    = rest[0] if rest else "music"
                audio_rest = rest[1].strip() if len(rest) > 1 else None
                fadein = 0.0
                audio  = audio_rest
                if audio_rest:
                    _mf = _imre.search(r'\s+fadein\s+(\d+(?:\.\d+)?)\s*$', audio_rest, _imre.IGNORECASE)
                    if _mf:
                        fadein = float(_mf.group(1))
                        audio  = audio_rest[:_mf.start()].strip()
                return (kw.strip(), channel, audio, fadein, trans_name)
        if kw_lower.startswith("stop "):
            _parts = s[5:].strip().split()
            channel = _parts[0] if _parts else "music"
            fadeout = float(_parts[2]) if len(_parts) >= 3 and _parts[1].lower() == "fadeout" else 0.0
            return ("stop", channel, fadeout, trans_name)
        m = _imre.match(r'^(\w+)\s+["\'](.+)["\']$', s, _imre.DOTALL)
        if m:
            return ("say", m.group(1), m.group(2), trans_name)
        return None

    def _im_reset_runtime_state(clear_pending=False):
        try:
            store._im_in_say_call = False
        except Exception:
            pass
        try:
            store._im_executing_injection = False
        except Exception:
            pass
        try:
            if clear_pending and getattr(store, "_im_post_say_pending", None):
                del store._im_post_say_pending[:]
            if clear_pending or not getattr(store, "_im_post_say_pending", None):
                store._im_injection_queued = False
        except Exception:
            pass

    def _im_cleanup_ui_stack():
        try:
            _ui = renpy.ui
            _stack = getattr(_ui, "stack", None)
            if _stack is None:
                return
            _at_stack = getattr(_ui, "at_stack", None)
            _root_ok = (
                len(_stack) == 1
                and getattr(_stack[0], "name", None) == "transient"
                and not _at_stack
            )
            if _root_ok:
                return
            try:
                _im_log("injection cleanup: reset ui stack %s" % " | ".join([repr(item) for item in _stack]))
            except Exception:
                pass
            _ui.reset()
        except Exception:
            pass

    def _im_execute_injection(s):
        parsed = _im_parse_injection(s)
        if not parsed:
            return
        kind = parsed[0]
        trans_name = parsed[-1]  # last element is always trans_name (may be None)
        trans_obj = None
        if trans_name:
            trans_obj = getattr(store, trans_name, None)
        try:
            store._im_executing_injection = True
        except Exception:
            pass
        try:
            if kind == "say":
                who_obj = getattr(store, parsed[1], None)
                try:
                    if trans_obj is not None:
                        renpy.transition(trans_obj)
                    renpy.say(who_obj, parsed[2])
                except renpy.game.CONTROL_EXCEPTIONS:
                    raise
                except Exception:
                    pass
            elif kind == "show":
                try:
                    renpy.show(parsed[1])
                    if trans_obj is not None:
                        renpy.checkpoint(hard=False)
                        renpy.with_statement(trans_obj)
                except Exception:
                    pass
            elif kind == "hide":
                try:
                    renpy.hide(parsed[1])
                    if trans_obj is not None:
                        renpy.checkpoint(hard=False)
                        renpy.with_statement(trans_obj)
                except Exception:
                    pass
            elif kind == "scene":
                try:
                    renpy.scene()
                    if parsed[1]:
                        renpy.show(parsed[1])
                    if trans_obj is not None:
                        renpy.checkpoint(hard=False)
                        renpy.with_statement(trans_obj)
                except Exception:
                    pass
            elif kind == "play":
                try:
                    channel   = parsed[1]
                    audio_tag = parsed[2]
                    fadein    = parsed[3] if len(parsed) > 4 else 0.0
                    # Resolve: store var → audio namespace → raw tag
                    _audio_ns = getattr(store, "audio", None)
                    audio_file = (
                        getattr(store, audio_tag, None) or
                        (getattr(_audio_ns, audio_tag, None) if _audio_ns else None) or
                        audio_tag
                    ) if audio_tag else None
                    if audio_file:
                        renpy.music.play(audio_file, channel=channel, fadein=fadein)
                except Exception:
                    pass
            elif kind == "queue":
                try:
                    channel   = parsed[1]
                    audio_tag = parsed[2]
                    fadein    = parsed[3] if len(parsed) > 4 else 0.0
                    _audio_ns = getattr(store, "audio", None)
                    audio_file = (
                        getattr(store, audio_tag, None) or
                        (getattr(_audio_ns, audio_tag, None) if _audio_ns else None) or
                        audio_tag
                    ) if audio_tag else None
                    if audio_file:
                        renpy.music.queue(audio_file, channel=channel, fadein=fadein)
                except Exception:
                    pass
            elif kind == "stop":
                try:
                    fadeout = parsed[2] if len(parsed) > 3 else 0.0
                    renpy.music.stop(channel=parsed[1], fadeout=fadeout)
                except Exception:
                    pass
        finally:
            try:
                store._im_executing_injection = False
            except Exception:
                pass

    def _im_char_call_wrapper(self, what, *args, **kwargs):
        is_injection = getattr(store, "_im_executing_injection", False)
        mode_active = _in_any_mode_active()
        if not is_injection and mode_active:
            try:
                store._im_injection_queued = False
                del store._im_post_say_pending[:]
            except Exception:
                pass
        # Set the flag that allows replace_text to queue injections.
        # It is set right before the say runs and cleared right after —
        # so History/log re-renders (which happen outside __call__) never
        # see it as True and cannot queue injections spuriously.
        if not is_injection:
            try:
                store._im_in_say_call = True
            except Exception:
                pass
        try:
            try:
                # Run the actual say (user clicks through).
                result = _im_orig_char_call(self, what, *args, **kwargs)
            finally:
                if not is_injection:
                    try:
                        store._im_in_say_call = False
                    except Exception:
                        pass

            if is_injection:
                return result

            # Execute injections AFTER this say completes (post-say).
            if mode_active:
                pending = list(getattr(store, "_im_post_say_pending", []))
                if pending:
                    del store._im_post_say_pending[:]
                    store._im_injection_queued = False
                    _prev_rb = renpy.config.rollback_enabled
                    renpy.config.rollback_enabled = False
                    try:
                        for _inj in pending:
                            try:
                                _im_execute_injection(_inj)
                            except renpy.game.CONTROL_EXCEPTIONS:
                                raise
                            except Exception:
                                pass
                    finally:
                        renpy.config.rollback_enabled = _prev_rb
            else:
                _im_reset_runtime_state(clear_pending=True)
            return result
        finally:
            if not is_injection:
                _im_reset_runtime_state(clear_pending=True)

    # Mark the wrapper so the patch block can detect it regardless of object identity
    # (Ren'Py creates a new function object on every script reload).
    _im_char_call_wrapper._im_is_wrapper = True

    try:
        import renpy.character as _im_char_mod
        # Character is a factory function in Ren'Py – ADVCharacter is the
        # actual class whose __call__ is invoked for every say statement.
        _im_patch_cls = getattr(_im_char_mod, "ADVCharacter", None)
        if _im_patch_cls is None or not isinstance(_im_patch_cls, type):
            # Fallback: if ADVCharacter doesn't exist, try Character as class
            _im_patch_cls = getattr(_im_char_mod, "Character", None)
            if not isinstance(_im_patch_cls, type):
                _im_patch_cls = None
        if _im_patch_cls is not None:
            current_call = _im_patch_cls.__call__
            if getattr(current_call, '_im_is_wrapper', False):
                # Already wrapped (e.g. after script reload) – restore the true
                # original from the backup so _im_orig_char_call never points at
                # a wrapper, then re-apply with the fresh function object.
                _im_orig_char_call = _im_patch_cls._im_orig_call_backup
            else:
                # First init: the current __call__ is the real original.
                _im_orig_char_call = current_call
                _im_patch_cls._im_orig_call_backup = _im_orig_char_call
            _im_patch_cls.__call__ = _im_char_call_wrapper
    except Exception:
        pass

screen _im_reload_scripts_hotkey():
    if persistent.im_reload_hotkey_enabled:
        key "K_F10" action Function(_im_reload_scripts)

init python:
    def _im_skip_to_mod_interact_cb():
        # DEV: wenn Ren'Py's Skip aktiv ist und die aktuelle Zeile vom Mod
        # verändert wurde, Skip stoppen – wie ein natürlicher Skip-Stopper.
        try:
            if renpy.config.skipping and getattr(store, "_im_dev_text_modified", False):
                renpy.config.skipping = None
        except Exception:
            pass

    _im_skip_to_mod_interact_cb._im_is_skip_to_mod_interact_cb = True

    try:
        config.interact_callbacks[:] = [
            cb for cb in config.interact_callbacks
            if not getattr(cb, '_im_is_skip_to_mod_interact_cb', False)
        ]
        config.interact_callbacks.append(_im_skip_to_mod_interact_cb)
    except Exception:
        pass

screen _im_dev_text_indicator_screen():
    # DEV: zeigt oben rechts ein Badge wenn die aktuelle Dialogzeile
    # durch den Mod verändert wurde.
    zorder 200
    if persistent.im_dev_text_indicator and _im_dev_text_modified:
        frame:
            xalign 1.0
            yalign 0.0
            xoffset -12
            yoffset 12
            xpadding 10
            ypadding 6
            background Frame("#0d1b2ae0", 6, 6)
            hbox:
                spacing 7
                yalign 0.5
                frame:
                    xsize 9
                    ysize 9
                    yalign 0.5
                    background "#00d4ff"
                    xpadding 0
                    ypadding 0
                text "IC-Mod" style "default" size 16 color "#00d4ff" bold True yalign 0.5

screen _im_dev_node_loc_screen():
    # DEV: zeigt oben rechts Datei + Zeilennummer des aktuellen Dialogs
    # als fertigen Specifier (z.B. "script8:867") zum Copy-Pasten.
    zorder 200
    if persistent.im_dev_node_loc:
        $ _dnl_short, _dnl_line = _im_dev_node_loc
        if _dnl_line is not None:
            frame:
                xalign 1.0
                yalign 0.0
                xoffset -12
                yoffset 50
                xpadding 10
                ypadding 6
                background Frame("#2a0d1be0", 6, 6)
                text "{}:{}".format(_dnl_short or "?", _dnl_line) style "default" size 14 color "#ffaa44" bold True yalign 0.5

init python:
    try:
        if "_im_reload_scripts_hotkey" not in config.overlay_screens:
            config.overlay_screens.append("_im_reload_scripts_hotkey")
        if "_im_dev_text_indicator_screen" not in config.overlay_screens:
            config.overlay_screens.append("_im_dev_text_indicator_screen")
        if "_im_dev_node_loc_screen" not in config.overlay_screens:
            config.overlay_screens.append("_im_dev_node_loc_screen")
    except Exception:
        pass

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
        #"poolalex": "poolalex_mod",
        #"versiontwo": "versiontwo_mod",
        "potionslabel": "potionslabel_mod",
        "daliacove": "daliacove_mod",
    }
    im_label_map_incest = {
        # Beispiel: "some_label": "some_label_incest_mod",
    }
    im_label_map_sister = {
        "welcome": "welcome_mod",
        "preeternum": "preeternum_mod",
        "_call_chat_18": "mod_call_chat_18",
        "menurestaurant": "menurestaurant_mod",
    }
    im_label_map_only_sister = {
        "welcome": "welcome_mod",
        "preeternum": "preeternum_mod",
        "_call_chat_18": "mod_call_chat_18",
        "menurestaurant": "menurestaurant_mod",
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
init python early:
    from renpy import exports as rpy
    from renpy import config as rconfig
    import store

    try:
        _im_label_chain
    except NameError:
        _im_label_chain = []
    if not isinstance(_im_label_chain, list):
        _im_label_chain = []

    if not hasattr(store, "_im_redirecting"):
        store._im_redirecting = False
    if not hasattr(store, "_im_prev_flags"):
        store._im_prev_flags = (bool(getattr(store, 'annie_incest', False)), bool(getattr(store, 'annie_sister', False)), bool(getattr(store, 'annie_mom', False)), bool(getattr(store, 'annie_half_sister', False)), bool(getattr(store, 'annie_aunt', False)))

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
        curr = (bool(getattr(store, 'annie_incest', False)), bool(getattr(store, 'annie_sister', False)), bool(getattr(store, 'annie_mom', False)), bool(getattr(store, 'annie_half_sister', False)), bool(getattr(store, 'annie_aunt', False)))
        if curr == getattr(store, '_im_prev_flags', None):
            return False
        store._im_prev_flags = curr
        return True

    def _im_set_override(src, dst):
        # Set runtime override and refresh the cached config map immediately.
        store.im_label_overrides[src] = dst
        _im_apply_map_to_config()

    def _im_clear_override(src=None):
        if src is None:
            store.im_label_overrides.clear()
        else:
            store.im_label_overrides.pop(src, None)
        _im_apply_map_to_config()

    def _im_toggle_redirect(on=None):
        if on is None:
            store.im_redirect_enabled = not store.im_redirect_enabled
        else:
            store.im_redirect_enabled = bool(on)

    def _im_get_override(target):
        # Use the cached config map. Rebuilding all label maps here is expensive
        # because this function can run on every label entry/fall-through.
        try:
            overrides = getattr(rconfig, "label_overrides", None)
            ov = overrides.get(target, None) if overrides else None
        except Exception:
            ov = None
        if ov and rpy.has_label(ov):
            return ov
        return None

    def _im_label_cb(label, *a, **kw):
        # Keep mapping in sync with mode switches.
        try:
            if _im_refresh_if_flags_changed():
                _im_apply_map_to_config()
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

    # Sentinel so _im_ensure_label_callback can detect our wrapper by attribute
    # instead of object identity (identity breaks on every script reload).
    _im_label_cb._im_is_label_cb = True

    def _im_register_prev_label_cb(cb):
        # Skip None, our own wrapper (any generation), and duplicates.
        if cb and not getattr(cb, '_im_is_label_cb', False) and cb not in _im_label_chain:
            _im_label_chain.append(cb)

    def _im_ensure_label_callback():
        # Ren'Py 8.x uses config.label_callbacks (a list). Some older builds
        # and mods used config.label_callback (singular). Support both while
        # avoiding duplicate callback execution after script reloads.
        try:
            callbacks = getattr(rconfig, "label_callbacks", None)
            if callbacks is not None:
                existing = list(callbacks)
                for cb in existing:
                    _im_register_prev_label_cb(cb)
                # Replace old callbacks/wrappers with a single wrapper. The
                # wrapper calls the previous callbacks exactly once, then can
                # redirect safely.
                if isinstance(callbacks, list):
                    callbacks[:] = [_im_label_cb]
                else:
                    rconfig.label_callbacks = [_im_label_cb]
        except Exception:
            pass

        try:
            curr = getattr(rconfig, "label_callback", None)
            # Use sentinel attribute instead of identity so reloads don't grow the chain.
            if not getattr(curr, '_im_is_label_cb', False):
                _im_register_prev_label_cb(curr)
                rconfig.label_callback = _im_label_cb
        except Exception:
            pass

    _im_ensure_label_callback()
    _im_apply_map_to_config()

    # Ensure fall-through labels (no explicit jump) are still intercepted.
    try:
        import renpy.ast as _im_ast
        from renpy import game as _im_game
    except Exception:
        _im_ast = None
        _im_game = None

    if _im_ast and not hasattr(_im_ast.Label, "_im_prev_execute"):
        _im_ast.Label._im_prev_execute = _im_ast.Label.execute

        def _im_label_execute_with_redirect(self, _im_ast=_im_ast, _im_game=_im_game):
            # _im_ast/_im_game are bound as defaults at definition time so this
            # permanently-patched method keeps working even if game-script
            # globals are momentarily cleared (e.g. Ren'Py calling
            # renpy.exports.load_module("_errorhandling") early on reload,
            # before this mod's init python block has re-run).
            if getattr(store, "_im_redirecting", False):
                return _im_ast.Label._im_prev_execute(self)
            if not getattr(store, "im_redirect_enabled", True):
                return _im_ast.Label._im_prev_execute(self)

            alt = None
            try:
                alt = _im_get_override(self.name)
            except Exception:
                alt = None

            if alt and alt != self.name:
                abnormal = False
                if _im_game is not None:
                    try:
                        abnormal = bool(_im_game.context().last_abnormal)
                    except Exception:
                        pass
                for cb in list(_im_label_chain):
                    try:
                        cb(self.name, abnormal)
                    except Exception:
                        pass
                if getattr(store, 'im_debug_redirect', False):
                    try:
                        rpy.notify("IM redirect: {} -> {}".format(self.name, alt))
                    except Exception:
                        pass
                store._im_redirecting = True
                try:
                    rpy.jump(alt)
                finally:
                    store._im_redirecting = False
                return

            return _im_ast.Label._im_prev_execute(self)

        _im_ast.Label.execute = _im_label_execute_with_redirect

    try:
        _im_stmt_cb_counter
    except NameError:
        _im_stmt_cb_counter = 0

    # Keep overrides in sync before each statement executes, but avoid doing
    # callback-list maintenance on every statement.
    def _im_stmt_cb(loc):
        global _im_stmt_cb_counter
        try:
            changed = _im_refresh_if_flags_changed()
            if changed:
                _im_apply_map_to_config()
                _im_ensure_label_callback()
                _im_stmt_cb_counter = 0
                return

            # Guard against another mod/script reload replacing label callbacks,
            # but check only occasionally instead of every statement.
            _im_stmt_cb_counter += 1
            if _im_stmt_cb_counter < 200:
                return
            _im_stmt_cb_counter = 0

            need_refresh = False
            callbacks = getattr(rconfig, "label_callbacks", None)
            if callbacks is not None:
                try:
                    need_refresh = not (
                        len(callbacks) == 1
                        and getattr(callbacks[0], '_im_is_label_cb', False)
                    )
                except Exception:
                    need_refresh = True
            else:
                curr = getattr(rconfig, "label_callback", None)
                need_refresh = not getattr(curr, '_im_is_label_cb', False)

            if need_refresh:
                _im_ensure_label_callback()
        except Exception:
            pass

    _im_stmt_cb._im_is_stmt_cb = True

    try:
        if getattr(rconfig, "statement_callbacks", None) is None:
            rconfig.statement_callbacks = []
        rconfig.statement_callbacks[:] = [
            cb for cb in rconfig.statement_callbacks
            if not getattr(cb, '_im_is_stmt_cb', False)
        ]
        rconfig.statement_callbacks.append(_im_stmt_cb)
    except Exception:
        pass

    def _im_export_store_api():
        # Rebind helpers after load so stale save data cannot leave them as None.
        globals()["im_export_store_api"] = _im_export_store_api
        globals()["im_set_mode"] = _im_set_mode
        globals()["im_set_override"] = _im_set_override
        globals()["im_clear_override"] = _im_clear_override
        globals()["im_toggle_redirect"] = _im_toggle_redirect
        globals()["im_apply_label_map"] = _im_apply_map_to_config

    def _im_set_mode(mode):
        global _in_replace_index_key, _in_replace_index_cache
        store.im_incest_mode = mode
        _im_apply_incest_mode()
        _im_apply_map_to_config()
        _in_replace_index_key = None
        _in_replace_index_cache = None
        in_apply_text_map()

    # export helpers to store API (without leaking renpy into store)
    _im_export_store_api()

# -----------------------------------------
# Replacement maps (CONTENT OMITTED)
# -----------------------------------------
# =========================================================
# LW/N: HOW TO WRITE MAP ENTRIES – all variants
# =========================================================
    #
    # VARIANT 1 – Simple text replacement (same as always)
    # Replaces the text everywhere it appears in the game.
    #
    #   "Original text":
    #       "New text",
    #
    # ---------------------------------------------------------
    #
    # VARIANT 2 – Replace text only at a specific location
    # Useful when the same line appears at multiple points in
    # the game and you only want to change one of them.
    # Get the specifier (e.g. script:867) from the dev overlay
    # in the top-right corner (enable in Prefs > Dev Tools >
    # "Show Script Line").
    #
    #   With filename + line number:
    #   "Original text":
    #       ("New text", "script:867"),
    #
    #   Line number only (any file):
    #   "Original text":
    #       ("New text", 867),
    #
    #   VARIANT 2b – Multiple location-specific replacements for the same line
    #   When the same dialogue appears in several places and you want to replace
    #   more than one of them differently, use a list of tuples. Each entry is
    #   checked in order; the first one whose location matches is applied.
    #
    #   "Original text": [
    #       ("New text A", "script:867"),
    #       ("New text B", "script:1234"),
    #   ],
    #
    # ---------------------------------------------------------
    #
    # VARIANT 3 – Insert extra lines after the dialogue
    # After the player clicks through the changed line, the
    # injected lines run in order, then the game continues
    # normally as if nothing was added.
    # Rollback is disabled when inside an injection to prevent
    # bugs when going back. Rolling back after injection ends will
    # skip to original line.
    #   ADDING SCRIPT NUMBER IS REQUIRED FOR THIS TO WORK PROPERLY
    #
    # Supported injection types:
    #   'mc "Some text"'      -> MC says something
    #   'annie "Some text"'   -> any character variable says something
    #   "show train 6"        -> display an image/sprite
    #   "hide train"          -> hide an image/sprite
    #   "scene bg room"       -> change the background
    #   "with dis"            -> transitions when clicking
    #   "play music name"     -> play music file in channel
    #   "stop music"          -> stop music channel
    #
    #   "Original text":
    #       ("New text", "script:867", [
    #           "show train 6",
    #           'mc "This is a test" with hunch'
    #       ]),
    #
    # EXTENDED SHOWCASE
        # "I'm Annie! It's really nice to meet you!":
        #     ("I'm Annie! Your little sister! It's really nice to meet you!",
        #     "script:868",
        #     [
        #         'a "And I mean that — we haven\'t seen each other in so long!"',
        #         "show intro 2",
        #         'a "But now we\'re finally together again." with dis',
        #         "show intro 1",
        #         'a "Hey, stop that!" with hpunch',
        #         'a "Or that!" with flash',
        #         'stop music2',
        #         "play music darksouls fadein 1",
        #         'a "Why are we playing this music?!"',
        #         'stop music',
        #         'play music2 happy1',
        #         'a "Okay, back to normal!"'
        #     ]
        # ),
    #
    # ---------------------------------------------------------
    #
    # COMPATIBILITY WITH BONUS AND MULTI MODS
    # Bonus Features Mod and Multi-Mod have different line numbers
    # In order to maintain compatibility with these mods,
    # USE VARIANT 2B which as it turns out can handle both specific
    # and injected lines. Format as follows:
    #
    # Variant 2 - specific lines
    #   "Original text":[
    #       ("New text A", "script:867"),
    #       ("New text B", "script:1234"),
    #
    #       # Bonus Mod
    #       ("New text A", "script:987"),
    #       ("New text B", "script:2345"),
    #
    #       # Multi Mod
    #       ("New text A", "script:546"),
    #       ("New text B", "script:5432"),
    #   ],
    #
    # Variant 3 - injected lines
    #   "Original text":[
    #       ("New text", "script:123", [
    #           'mc "injected lines"
    #       ]),
    #
    #       # Bonus Mod
    #       ("New text", "script:234", [
    #           'mc "injected lines"
    #       ]),
    #
    #       # Multi Mod
    #       ("New text", "script:345", [
    #           'mc "injected lines"
    #       ]),
    #   ],
    # 
    # =========================================================

init python:
    mom_map = {
        # -----------------------------------------
        # formerly known as base map
        # Nancy as Mom, Penny and Dalia as older sisters
        # They have the same last name as MC
        # MC is Dalia's "Irish twin" (born within 12 months), hence being in the same grade
        #     until he gets an official birthdate that screws us over lmao
        # -----------------------------------------
        # Character notes
        # Code auto changes Nancy->Mom for MC lines
        # Penny called "sis", "Penny", sometimes "big sis". She uses "bro", "little bro/brother", but more sparingly
        # Dalia mix of "sis" and "Dal/Daly"
        # -----------------------------------------
        # BM script:0000 = Base Map, RPY file:Line Number
        #     Numbers based on v0.9.5, subject to change in future updates
        # Tags based on who the line is about contextually, not always the speaker.
        # Selectively applied for clarification
        # (menu) = Choice menu line
        # (mc) = MC line
        # (n) = Nancy line
        # (p) = Penelope line
        # (d) = Dalia line
        # (a) = Annie line
        # (x) = Alex line
        # (l) = Luna line
        # (no) = Nova line
        # (ca) = Calypso line
        # -----------------------------------------
        # Code tags
        # {specific} = use of Variant 2 to target specific lines
        # {inject} = use of Variant 3 to inject new lines      
        # -----------------------------------------
        # LW/N = Lucifer_W's notes
        # l9/N = l9453394's notes
        # BA/N = BlueArrow's notes
        # -----------------------------------------

    # -----------------------------------------
    # v0.1 script.rpy

        # BM script:948
        "My name is [mc] [lastname]. I was born in the city of Kredon, a relatively small town on the west coast of the United States.":
            "My name is [mc] [lastname]. I was born into a family of five in the city of Kredon, a relatively small town on the west coast of the United States.",

        # BM script:950
        "My mother left shortly after I was born and my dad was never around much because he was always so focused on his job.":
            "My mother always cared for me and my sisters, but my dad was never around much. He was always so focused on his job and never made time for our family. This basically left my mom as the only parent taking care of three young kids while still juggling school.",

        # BM script:951
        "That’s actually why we ended up moving to the UK; Dad needed to relocate there to keep his position.":
            "This led to constant tension between my parents, which reached a boiling point when Dad needed to relocate to the UK to keep his position. Unable to resolve their differences, they divorced.",

        # BM script:952
        "I know, I know, this all sounds pretty gloomy... but don't worry! This is not about to be one long sob story.":
            "He got custody of me, taking me with him to the UK while she stayed behind with my two older sisters. I know it sounds a bit bleak, but don't worry - this isn't a sob story.",

        # BM script:1076
        # BA/N: Disabled to establish her name. It's clarified she's the mom two lines later anyway.
        # "I was saying that I spoke with Nancy.":
        #     "I was saying that I spoke with your mom.",

        # BM script:1082
        "*Laughs* I'm sure she will.":
            "*Laughs* I'm sure she will. She is your mother after all.",

        # BM script:1085
        # LW/N: FIXED: Handle both "Nancy" and "Mom" versions
        "(Nancy used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(My mom used to look after me and my sisters in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)",

        "(Mom used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(My mom used to look after me and my sisters in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)",

        # BM script:1086
        # LW/N: FIXED: Handle both versions
        "(I used to spend the entire afternoon playing with Nancy and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend entire afternoons playing with Mom and my older sister Dalia, but then we had to move and ended up losing touch.)",

        "(I used to spend the entire afternoons playing with Mom and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(I used to spend entire afternoons playing with Mom and my older sister Dalia, but then we had to move and ended up losing touch.)",

        # BM script:1088
        # LW/N: FIXED: Handle both versions
        "(Living with them will be much cheaper than renting a student residence, and it’ll surely be nice to see Nancy and Dalia again.)":
            "(Living with them will be much cheaper than renting a student residence, and it'll surely be nice to see my mom, Dalia, and my oldest sister Penelope again.)",

        "(Living with them will be much cheaper than renting a student residence, and it’ll surely be nice to see Mom and Dalia again.)":
            "(Living with them will be much cheaper than renting a student residence, and it'll surely be nice to see my mom, Dalia, and my oldest sister Penelope again.)",

        # BM script:1112
        # BA/N: moved from half-sis map
        "What's the first thing you're going to do when we get to our new home?":
            "What's the first thing you're going to do when we get to your old home?",

        # BM script:1354
        "Anyway, do you know where Nancy is?":
            "Anyway, do you know where your mom is?",

        # BM script:1711
        "How could I forget you?":
            "How could I forget my own mom?",

        # BM script:1767 minor grammar change
        "It’s me, Nancy! Even though we’ve only been speaking on the phone for the past few days, I feel like we’ve been becoming good friends already! Isn't that right, Annie?":
            "It's me, Nancy! Even though we've only been speaking on the phone for the past few days, I feel like we're becoming good friends already! Isn't that right, Annie?",

        # BM script:1786
        "And of his babysitter!":
            "And of his mother!",

        # BM script:1790
        "Yeah, since my Dad was constantly working, I've always said you were like a parent to me.":
            "Of course! You were the one taking care of us, after all.",

        # BM script:1793
        "Now I work in a laboratory, but back then I was still finishing my thesis. Thankfully [mc]'s father came along and offered me the babysitting gig.":
            "Now I work in a laboratory, but back then I was still finishing my studies. Luckily, [mc]'s father made enough money for the family.",

        # BM script:1794
        "It was not only well-paid, but also allowed me the flexibility to take care of my daughters at the same time. And for me, being a single mother, that was essential.":
            "I was able to focus on my thesis and taking care of our three children.",

        # BM script:1796
        "You have 2 daughters, right?":
            "You also have 2 daughters, right?",

        # BM script:1798
        "Yes, Dalia and Penelope. Penny was a little older when I was [mc]'s nanny, so she used to play on her own, but Dalia got very close to him!":
            "Yes, Dalia and Penelope. Penny is a little older than [mc], so she used to play on her own, but Dalia was always very close to him!",

        # BM script:1811
        "(I guess you don't notice that stuff when you're 8 years old...)":
            "(I guess you don't notice that stuff when you're a kid...)",

        # BM script:1813
        "(Okay, now I sound like some old perv.)":
            "(Okay, now I sound like an old pervert. Especially since she's my mother.)",

        # BM script:1842
        "(Nancy used to pick me up after school and we'd come here.)":
            "(Those blissful, carefree days of my childhood – especially once school was done!)",

        # BM script:1843
        "(Each day I would spend the afternoon playing with her and Dalia. We had dinner every night at eight, and then Nancy drove me home once it got late.)":
            "(My afternoons were spent playing with Mom and Dalia. We had dinner every night at eight, and then went to bed.)",

        # BM script:1845
        "(She would always call me on my birthday, but... aside from that, I never reached out. I have to make it up to her somehow.)":
            "(Mom would always call me on my birthday, but... aside from that, I never reached out. I have to make it up to her somehow.)",

        # BM script:1864
        "Although he left before she was born, so I was left paying the mortgage all by myself...":
            "Although when he left, I had to pay the rest of the mortgage all by myself.",

        # BM script:1894
        "*Laughs* And Penelope the preteen that was too \"cool\" to play with Dalia and me?":
            "*Laughs* And Penelope the preteen that was too \"cool\" to play with her younger siblings?",

        # BM script:1916
        "I wasn't expecting you to be so excited to meet [mc] again!":
            "I wasn't expecting you to be so excited to meet your brother again!",

        # BA/N: disabling most bro/sis lines here to give them a sense of "warming up" to each other again

        # BM script:1932 (d)
        #"Oh, y-yeah, so excited! Hi [mc]!":
        #    "Oh, y-yeah, so excited! Hi bro!",

        # BM script:1962
        "Both of those things can wait! You didn't even welcome [mc] and Annie properly!":
            "Both of those things can wait! You didn't even welcome your brother and Annie properly!",

        # BM script:1967 (p)
        "[mc]! I can't wait to properly meet you!":
            "Hey, [mc], I can't wait to hear all about what happened to you!",

        # BM script:1970
        # BA/N: moved from half-sis map
        "Oh, and you must be Annie! Nice to meet you too!":
            "Oh, and you must be Annie! Nice to meet you!",

        # BM script:1976 (d)
        #"Damn [mc], you look... tall!":
        #    "Damn, bro, you look... tall!",

        # BM script:1977
        #"Thanks, Dalia. You look... tall too.":
        #    "Thanks, sis. You look... tall too.",

        # BM script:2022 (d)
        "Because he's cool! It's good to see the city didn't change you, [mc].":
            "Because he's cool! It's good to see the city didn't change you, bro.",

        # BM script:2115 (n)
        "Your room will be on the second floor—the last one on the right.":
            "I cleaned up your old room. I hope you still remember it?",

        # BM script:2137
        "(Well, this is gonna be my room for a whole year.)":
            "(Well, this is gonna be my room again for a whole year.)",

        # BM script:2139
        # LW/N: FIXED: Handle both "Nancy" and "Mom" versions
        "(There wasn't a bed here before. I guess Nancy fitted it out to serve as a bedroom.)":
            "(My bed is bigger than before. I guess Mom replaced my old furniture.)",

        "(There wasn't a bed here before. I guess Mom fitted it out to serve as a bedroom.)":
            "(My bed is bigger than before. I guess Mom replaced my old furniture.)",

        # BM script:2205
        "N-Nancy?":
            "M-Mom?",

        # BM script:2212
        "N-Nancy? W-Who is this kid?":
            "M-Mom? W-Who is this kid?",

        # BM script:2365
        "N-Nancy! You almost gave me a heart attack!":
            "M-Mom! You almost gave me a heart attack!",

        # BM script:2376
        "I'm used to only living with my daughters, and...":
            "I'm used to only living with your sisters, and...",

        # BM script:2395
        "It's like we're family now. I'm not bothered by you at all!":
            "It's alright, we're family after all. I'm not bothered by you at all!",

        # BM script:2400
        "O-Okay... Thank you [mc]!":
            "O-Okay... Thank you, dear!",

        # BM script:2430
        "(Jesus, look at me. Fantasizing about the dick of the kid I used to care for.)":
            "(Jesus, look at me. Fantasizing about the dick of my own son.)",

        # BM script:2431
        "(You're 20 years older than he is, Nancy, for fuck's sake.)":
            "(You're his mother, Nancy, for fuck's sake! What's wrong with you?)",

        # BM script:2451
        "Hey Dalia! Good morning!":
            "Hey sis! Good morning!",

        # BM script:2452 (d), also overwrites script8:3455 (p), okay
        "Hey [mc]!":
            "Hey bro!",

        # BM script:2495
        "No problem Dalia. I don’t like being the center of attention anyway.":
            "No problem, sis. I don't like being the center of attention anyway.",

        # BM script:2573 (p)
        "Good morning...":
            "Good morning, sis...",

        # BM script:2585
        "(I mean, I know they’re pretty much like family, so I don't mean it that way, but...)":
            "(Wait no, they’re my family, I shouldn't be thinking of them in that way! But still...)",

        # BM script:2644 (p)
        "You're a fucking pig!":
            "I'm your sister, you fucking pig!",

        # BM script:2678 (p)
        "Thanks, [mc].":
            "Thanks, little brother.",

        # BM script:2752 (d)
        "Okay, okay, I'm just messing with you.":
            "Okay, okay, I'm just messing with you, bro.",

        # BM script:3200
        "*Turning around* Dalia!":
            "*Turning around* Dal!",

        # BM script:3425
        "(It's just Dalia. You two grew up together! She's practically your sister...)":
            "(It's just Dalia. It's been a decade, but she's still your sister...)",

        # BM script:3442
        "Dalia, the girl you live with?":
            "Dalia, your older sister?",

        # BM script:3454
        "Ohh... so you want to bang her?":
            "Uhh... why do you sound like you want to bang her?",

        # BM script:3456
        "O-Of course not! I'm just merely pointing out that she looks good.":
            "What? No! I'm just merely pointing out that she looks good.",

        # BM script:3577 (n)
        "(Oh my god, I like where this is going...)":
            "(Oh my god, is this is going where I think this is going?)",

        # BM script:3608
        "I knew I could count on you, [mc]!":
            "I knew I could count on you, sweetie!",

        # BM script:3591
        "And there's nothing like being on chore duty to strengthen a household bond!":
            "And there's nothing like being on chore duty to strengthen family bonds!",

        # BM script:3596
        "You’re not gonna leave poor ‘ol Nancy hanging, are you...? Will you help out?":
            "You’re not gonna leave your poor ol’ mother hanging, are you...? Will you help out?",

        # BM script:3656
        "(They're letting me and Annie stay in their house after all. This is the least I can do to show my gratitude.)":
            "(They're letting me and Annie stay here for a year after all. This is the least I can do to show my gratitude.)",

        # BM script:3369 (p) WIP
        # BA/N: maybe tone down the horny?
        #"{i}You did this?! You're sooo amazing! Do you want to celebrate by taking a hot, steamy bath with me?":
        #    "{i}You did this?! You're sooo amazing! Do you want to celebrate by test",

        # BM script:3673 (d)
        "{i}Dammit [mc], you're too good!":
            "{i}Dammit [mc], you're too good! Can you use those strong, manly arms of yours to show me how you did such an amazing cleaning job?!",

        # BM script:3674
        "{i}Can you use those strong, manly arms of yours to show me how you did such an amazing cleaning job?! I can’t promise that I won’t get wetter than this tub will be...":
            "(Jesus Christ, all this scrubbing must be driving me insane, thinking about my own mother and sisters like that.)",

        # BM script:3743 (d)
        "(I better make sure he's not home. Don’t want him getting any free looks...)":
            "(I better make sure he's not home. He may be my little brother, but I don't want him to catch me naked...)",

        # BM script:3804
        "(Oh shit, full-on chub incoming...)":
            "(Oh shit, full-on chub incoming... Oh god, snap out of it, [mc]. This is your sister!)",

        # BM script:3828
        "(And that's... wrong! Bad [mc]! Get a hold of yourself.)":
            "(And that's... wrong! Bad [mc]! This is your sister! Get a hold of yourself.)",

        # BM script:3829
        "(Man, being under the same roof as 4 women is not going to be healthy for me.)":
            "(Man, ten years apart and it's like I've stopped thinking of them as family.)",

        # BM script:3888
        "H-Hi Dalia!":
            "H-Hi sis!",

        # BM script:3897
        "You're a fucking rapist!":
            "You're a fucking pervert!",

        # BM script:3899
        "You were hiding in the bathtub so you could attack me from behind and then rape me!":
            "You were hiding in the bathtub so you could see me naked! I'm your sister, you pig!",
        
        # BM script:3901
        "So what then? You're just a perverted creep?!":
            "So what then? You were trying to creep on someone else in this house?!",

        # BM script:3921
        "Sorry if it sounds gross, but you simply have the most beautiful body I've ever seen. I didn't even know what to do!":
            "Sorry if it sounds gross since I'm your brother, but you simply have the most beautiful body I've ever seen. I didn't even know what to do!",

        # BM script:3949
        "Hi Penelope.":
            "Hi Penny.",

        # BM script:3971
        "Oh, hey Penelope!":
            "Oh, hey Penny!",

        # BM script:4012
        # BA/N: Disabled, penny will start using bro after the cafe
        # "I can't be seen there... I have a reputation to uphold, [mc].":
        #     "I can't be seen there... I have a reputation to uphold, bro.",

        # BM script:4027
        "She was going with my mom to do some shopping, or at least that’s what I was told. They should be back in time for supper.":
            "She was going with Mom to do some shopping, or at least that's what I was told. They should be back in time for supper.",

        # BM script:4041   
        # BA/N: Disabled, penny will start using bro after the cafe
        # "Alright [mc], you convinced me!":
        #     "Alright bro, you convinced me!",

        # BM script:4055
        "Thanks, Penelope!":
            "Thanks, sis!",

        # BM script:4188
        "Penelope!":
            "Penny!",

        # BM script:4200 (p)
        # BA/N: Disabled, penny will start using bro after the cafe
        # "*Laughs* Yeah, if you say so... Thanks, [mc].":
        #     "*Laughs* Yeah, if you say so... Thanks, brother.",

        # BM script:4231
        "(Wow, he's treating Penelope like a celebrity. Is she really that popular?)":
            "(Wow, he's treating big sis like a celebrity. Is she really that popular?)",

        # BM script:4271 (p)
        "*Laughs* Thank you, thank you.":
            "*Laughs* Why thank you, little bro.",

        # BM script:4844
        "Well, I definitely do not share that opinion at all.":
            "Well, I definitely do not share that opinion at all. You are my big sister after all.",

        # BM script:4846
        "Thanks for trusting me, [mc]. It means a lot.":
            "Thanks for trusting me, little brother. It means a lot.",

        # BM script:5140 (p)
        "Alright, let's go home, [mc]!":
            "Alright, let's go home, bro!",

        # BM script:5178
        "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal when I was living with my dad.":
            "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal while I was living with Dad.",

        # BM script:5218 (p)
        "It was a nice breath of fresh air. Thank you for pushing me out of my comfort zone, [mc].":
            "It was a nice breath of fresh air. Thank you for pushing me out of my comfort zone, bro.",

        # BM script:5220
        "No problem, Penelope.":
            "No problem, sis.",

        # BM script:5252 (d)
        "[mc] finally won an implant to play Eternum!":
            "Your brother finally won an implant to play Eternum!",

        # BM script:5254 (d)
        "Wow, seems like [mc] did a lot of things today.":
            "Wow, seems like my {i}brother{/i} did a lot of things today.",

        # BM script:5335
        "(Man, I've been way too horny lately...)":
            "(Man, I've been way too horny lately... I'm even thinking about my family in that way...)",

        # BM script:5337
        "(But I'm not gonna find one in this house! I need to start thinking with the head above my shoulders and not the one between my legs.)":
            "(I need to start thinking with the head above my shoulders and not the one between my legs.)",

        # BM script:5343
        "(There's only Dalia, then that uptight bitch who's friends with Axel, and...)":
            "(Besides Dalia–objectively, of course–there's that uptight bitch who's friends with Axel, and...)",

        # BM script:5370
        "I put a little extra elbow grease into it. After all, you're graciously letting me and Annie stay here and you’re sharing your food with us too!":
            "I put a little extra elbow grease into it. After all, I wanted to make you happy, Mom!",

        # BM script:5371
        "I know it doesn't come close to making up for it, but I'll try to help you out as much as I can.":
            "It's been way too long since we've seen each other.",

        # BM script:5414
        "First, neither of my daughters gets kissed by fire and inherits my lovely red hair, and now they can’t seem to keep tabs on any of their belongings!":
            "First, none of my kids get kissed by fire and inherit my lovely red hair, and now they can't seem to keep tabs on any of their belongings!",

        # BM script:5479
        "(Looking at hot pics of Penelope, yeah, great idea, [mc]. Way to not have even more fantasies of all these girls around me...)":
            "(Looking at hot pics of Penelope, yeah, great idea, [mc]. Way to not have even more fantasies of the girls in your family...)",

        # BM script:5541
        "(Who would’ve known he was hiding such a monster...)":
            "(Who would've known he was hiding such a monster... and where did he get it from? His father's certainly wasn't this size...)",

        # BM script:5559
        "(Oh Jesus, one man comes into my house and suddenly I turn into a nymphomaniac. What the hell is wrong with me?)":
            "(Oh Jesus, one man comes into my house and suddenly I turn into a nymphomaniac. What the hell is wrong with me? I'm his mother!)",

        # BM script:5583 (n) {inject}
        "(I mean... If Dalia and Penelope never found out, then would it really be so bad? It’d be our little secret...)":[
            ("(I mean... If Dalia and Penelope never found out, then would it really be so bad...?)","script:5583",[
                "show ale 31",
                'n "(What am I thinking?! Of course it would be! He’s my son...)" with dis06'
            ]),

            # Bonus Mod
            ("(I mean... If Dalia and Penelope never found out, then would it really be so bad...?)","script:5649",[
                "show ale 31",
                'n "(What am I thinking?! Of course it would be! He’s my son...)" with dis06'
            ]),

            # Multi Mod
            ("(I mean... If Dalia and Penelope never found out, then would it really be so bad...?)","script:5584",[
                "show ale 31",
                'n "(What am I thinking?! Of course it would be! He’s my son...)" with dis06'
            ]),
        ],

        # BM script:5606
        "(It was also kinda exhilarating, though... I haven’t felt excitement like that in so long...)":
            "(It was also kinda exhilarating, though... and the taboo just made it... {i}so much{/i} more exciting... I haven’t felt like that in so long...)",

        # ========== START label mod "poolalex_mod" ==========
            # line numbers for both files
        # REPLACED BY INJECTION, old code left just in case

        # BM script:5647 IncestLables:1816, also overwrites script6:1516 and script6:9319, both okay
        "Hey Dalia!":
            "Hey sis!",

        # BM script:5669 IncestLables:1838
        "I'm sorry about that, Dalia.":
            "I'm sorry about that, Dal.",

        # BM script:5937 (x) IncestLables:2106
        "By the way, I'm [mc]. I saw you before, at the pool.":
            "By the way, I'm [mc], Dalia's brother. I saw you earlier, at the pool.",

        # BM script:6045 (x) IncestLables:2219
        "You said you were Dalia's friend?":
            "You said you were Dalia's brother?",

        # BM script:6047 IncestLables:2221
        # Original non-inject version, used with labelmod
        #"Yeah, we've known each other since we were little.":
        #    "Yeah, we were separated as kids when our parents divorced.",

        # label mod lines explaining MC and Dalia's close age here

        # BM script:6047 {inject} (replaces labelmod)
        "Yeah, we've known each other since we were little.":[
            ("Yeah, we were separated as kids when our parents divorced.","script:6047",[
                "show ale 74",
                'x "Now that I think about, Dalia did mention having a brother before." with dis',
                'x "You’re younger aren’t you? How are you in the same class as us?"',
                "show ale 75",
                'mc "*Chuckles* I was actually born later that same year, close enough for us to be in the same grade."',
                "show ale 78",
                'x "So you’re almost like twins, huh?" with dis'
            ]),

            # Bonus Mod
            ("Yeah, we were separated as kids when our parents divorced.","script:6115",[
                "show ale 74",
                'x "Now that I think about, Dalia did mention having a brother before." with dis',
                'x "You’re younger aren’t you? How are you in the same class as us?"',
                "show ale 75",
                'mc "*Chuckles* I was actually born later that same year, close enough for us to be in the same grade."',
                "show ale 78",
                'x "So you’re almost like twins, huh?" with dis'
            ]),

            # Multi Mod
            ("Yeah, we were separated as kids when our parents divorced.","script:6048",[
                "show ale 74",
                'x "Now that I think about, Dalia did mention having a brother before." with dis',
                'x "You’re younger aren’t you? How are you in the same class as us?"',
                "show ale 75",
                'mc "*Chuckles* I was actually born later that same year, close enough for us to be in the same grade."',
                "show ale 78",
                'x "So you’re almost like twins, huh?" with dis'
            ]),
        ],

        # BM script:6049 use with inject
        "Probably the only two people in this class that are actually worth talking to.":
            "Well, you two are probably the only people in this class that are actually worth talking to.",

        # ========== END label mod "poolalex_mod" ==========

        # BM script:8463
        "I heard that promise, Penny! Too late to back out now!":
            "I heard that promise, sis! Too late to back out now!",

        # BM script:8505 (p)
        "*Laughs* I'm not a simp, I promise.":
            "*Laughs* Gotta help out my big sister, of course.",

        # BM script:8525 (p)
        "You know, I'm not gonna lie, when Mom told me that you and Annie were gonna live with us for a while, I got a little annoyed.":
            "You know, I'm not gonna lie, when Mom told me that you and Annie were gonna live with us for a while, I didn't know what to think. You coming back after ten years, with a stranger on top of that...",

        # BM script:8528 (p)
        "Thank you, Penelope. It means a lot hearing that from you.":
            "Thank you, Penny. It means a lot hearing that from you.",

        # BM script:8537 (p)
        "Anyway, I'll go to bed too. Goodnight, [mc].":
            "Anyway, I'll go to bed too. Goodnight, bro.",

        # BM script:8552
        "(You're not a horny teenager. Show her you're a man now.)":
            "(You're not a horny teenager, and she's your mother. Show her you're a respectable man now.)",

        # BM script:8646
        "What?! Come on, Dalia!":
            "What?! Come on, sis!",

        # BM script:8660
        "Please, Dalia! Please!":
            "Please, Daly! Please!",

        # BM script:8731 (d) {specific}, also overwrites other lines
        # Excludes script2:4200 (n) and script4:3325 (d)
        "Dalia!":[
            ("Dal!","script:8731"),
            ("Dal!","script:9368"),
            ("Dal!","script:9395"),
            ("Dal!","script4:3124"),

            # Bonus Mod
            ("Dal!","script:8820"),
            ("Dal!","script:9461"),
            ("Dal!","script:9488"),
            ("Dal!","script4:3143"),

            # Multi Mod
            ("Dal!","script:8734"),
            ("Dal!","script:9372"),
            ("Dal!","script:9399"),
            ("Dal!","script4:3147"),
        ],

        # BM script:9069
        "*Standing up* Thank god you knocked him down, Dalia...":
            "*Standing up* Thank god you knocked him down, Dal...",

        # BM script:9105
        "By the way, nice job back there. That was a nice hammering.":
            "By the way, nice job back there, bro. That was a nice hammering.",

        # BM script:9364
        "*Standing up* Dalia? Holy shit, that was unbelievable!":
            "*Standing up* Dal? Holy shit, sis, that was unbelievable!",

        # BM script:9368
        # Overwritten by BM script:8731, okay
        # "Dalia!" -> "Dal!"

        # BM script:9382
        "*Laughs* First lesson of Eternum, [mc].":
            "*Laughs* First lesson of Eternum, dear brother.",

        # BM script:9395
        # Overwritten by BM script:8731, okay
        # "Dalia!" -> "Dal!"

        # BM script:9617
        "Thanks Dalia, it means a lot coming from you.":
            "Thanks sis, it means a lot coming from you.",


    # -----------------------------------------
    # v0.2 script2.rpy

        # ========== START label mod "versiontwo_mod" ==========
            # BA/N: added label mod to add two dialogue lines I felt should've been in the intro between Luna and Annie in the first place.
            # Will also be used in other incest options too.
        # REPLACED BY INJECTION, old code left just in case

        # BM script2:112 {inject} (replaces labelmod)
        "It's so nice to meet you, Luna!":[
            ("It's so nice to meet you, Luna!","script2:112",[
                "scene aaa 15",
                'l "Same to you. You must be Annie, [mc]’s told me about you."',
                "scene aaa 14"
            ]),

            # Bonus Mod
            # script2:112, same as original

            # Multi Mod
            # script2:112, same as original
        ],

        # BM script2:113 use with inject
        "I heard [mc] managed to win a neural implant at your cafe!":
            "Yep! I heard [mc] managed to win a neural implant at your cafe!",

        # ========== END label mod "versiontwo_mod" ==========

        # BM script2:4013 (n)
        "*Knocks* [mc]? Are you up?":
            "*Knocks* Honey? Are you up?",

        # BM script2:4158
        "Dalia? Good morning!":
            "Dal? Good morning!",

        # BM script2:4281
        "Dalia? Are you up?":
            "Daly? Are you up?",

        # BM script2:4314
        "I gotta say, those were some damn good pancakes. Thank you, [mc].":
            "I gotta say, those were some damn good pancakes. Thank you, bro.",

        # BM script2:4338
        "Hmmm... I'm not so sure about that, Dalia. I've seen broom sticks thicker than your biceps.":
            "Hmmm... I'm not so sure about that, sis. I've seen broom sticks thicker than your biceps.",

        # BM script2:4374
        "A-Are you okay, Dalia?":
            "A-Are you okay, Dal?",

        # BM script2:4540
        "You’re just saying that because you feel sorry for me.":
            "You’re just saying that because you're my mom.",

        # BM script2:4544
        "Yeah, that’s just your maternal instinct. It’s like when a mom says that her son is the most beautiful baby in the world, even though it looks like E.T.":
            "Yeah, that’s just your maternal instinct. Every mom thinks their kid is the most beautiful baby in the world, even if they look like E.T.",

        # BM script2:4558
        "Oh, there's a lot you don't know about me, [mc]...":
            "Oh, there's a lot you don't know about me, sweetie...",

        # BM script2:4574
        "*Laughs* It's not that. [mc] is staying with us for a year until he finishes school. He’s part of the student exchange program.":
            "*Laughs* It's not that. This is my son I've told you about. [mc] is staying with us for a year until he finishes school. He came back as part of the student exchange program.",

        # BM script2:4580
        "Well, well, well, [mc]!":
            "Well, well, well, the fabled lost son is here!",

        # BM script2:4840
        "What? I'm not Dalia. My name is [mc].":
            "What? I'm not Dalia. My name is [mc]. Dalia is my sister.",

        # BM script2:4910
        # Handle both versions. Bypass added in skip_nancy_swap, edit down there if this line is changed
        "No, I came with Nancy.":
            "No, I came with Nancy, my mother.",

        "No, I came with Mom.":
            "No, I came with Nancy, my mother.",

        # BM script2:4912
        "Oh, really? You two know each other? Well I'm glad to meet you, because I'm positive you're going to be seeing a lot more of me soon...":
            "Oh, really? You are her son? Well I'm glad to meet you, because I'm positive you're going to be seeing a lot more of me soon...",

        # BM script2:4963
        "I mean, obviously Kai would've asked me out if I wasn't already married, but since I'm happily taken... Nancy will be a very good fit for him.":
            "I mean, obviously Kai would've asked me out if I wasn't already married, but since I'm happily taken... your mom will be a very good fit for him.",

        # BM script2:5002
        "Well, maybe not you, but... it just seems like he’s trying awfully hard to get close to Nancy...":
            "Well, maybe not you, but... it just seems like he’s trying awfully hard to get close to my mom...",

        # BM script2:5014
        "Y-Yeah, I know Nancy very well, and honestly she’s been in quite a heightened emotional state lately. I can’t bear the thought of that guy taking advantage of her.":
            "Y-Yeah. Honestly, she’s been in quite a heightened emotional state lately. I can’t bear the thought of that guy taking advantage of her.",

        # BM script2:5094
        "Look at that perfectly toned stomach... And to think she's had 2 daughters! Unbelievable.":
            "Look at that perfectly toned stomach... And to think she's had 3 children! Unbelievable.",

        # BM script2:5199
        "*Giggles* Just like when I was your babysitter.":
            "*Giggles* Just like when you were still living with us.",

        # BM script2:5294
        # BA/N: borrowed from aunt map
        "I can't be with him. It would be... weird. We’re not supposed to be together... like {i}that{/i}.":
            "I can't be with him. It would be... wrong. We’re not supposed to be together... like {i}that{/i}.",

        # BM script2:5321
        # BA/N: borrowed from aunt map
        "*Giggles* Um, maybe. No... But, I mean... could you imagine?!":
            "*Giggles* Um, maybe. No, that would be {i}so{/i} wrong... But, I mean... could you imagine?!",

        # BM script2:5363
        "(I can't just barge in and be like, \"Hi [mc], did you know you make me feel so horny all the time? Do you wanna fuck your old babysitter?\")":
            "(I can't just barge in and be like, \"Hi [mc], did you know you make me feel so horny all the time? Do you wanna fuck your mother?\")",

        # BM script2:5364
        "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out.)":
            "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be {i}furious{/i} if they ever found out. And fucking my son... God, there's so much that could go wrong for everyone...)",

        # BM script2:5416
        "(God, that would be so embarrassing.)":
            "(God, that would be {i}mortifying{/i}. How would I explain anything to them?)",

        # BM script2:6103 (x)
        "I never met my mother and my father was always absent in my life. He was constantly too occupied with his work.":
            "My father was always absent in my life, always too occupied with his work. When my parents divorced, I had to live with him for the last ten years, if you can even call it \"living with him\".",

        # BM script2:6106 (x) {inject}
        "Huh... I just assumed you were one of those pampered city boys that’s never known a hard day in his life...":[
            ("Oh right, you {i}are{/i} Dalia's brother...","script2:6106",[
                'x "Honestly, my first impression of you was that you were one of those pampered city boys that’s never known a hard day in his life..."'
            ]),

            # Bonus Mod
            ("Oh right, you {i}are{/i} Dalia's brother...","script2:6170",[
                'x "Honestly, my first impression of you was that you were one of those pampered city boys that’s never known a hard day in his life..."'
            ]),

            # Multi Mod
            ("Oh right, you {i}are{/i} Dalia's brother...","script2:6122",[
                'x "Honestly, my first impression of you was that you were one of those pampered city boys that’s never known a hard day in his life..."'
            ]),
        ],

        # BM script2:7046 (p) {specific}
        # Excludes script5:2321 (l)
        "Good morning, [mc]!":[
            ("Good morning, little brother!","script2:7046"),

            # Bonus Mod
            ("Good morning, little brother!","script2:7120"),

            # Multi Mod
            ("Good morning, little brother!","script2:7062"),
        ],

        # BM script2:7088
        "Is that a hint of jealousy, I'm sensing?":
            "Is that a hint of overprotectiveness I'm sensing, little bro?",

        # BM script2:7128
        "(It's not like I was expecting her to wait for me like a nun, but... just imagining some guy banging her... ugh.)":
            "(It's not like I was expecting her to wait for marriage like a nun, but... just imagining some guy banging her... ugh.)",

        # BM script2:7134
        "(Way out of your league.)":
            "(And I'm her little brother.)",

        # BM script2:7152
        "[mc] here is gonna be my photographer this time.":
            "My brother here is gonna be my photographer this time.",

        # BM script2:7156
        "Ahhh... yeah, that's right. [mc]...":
            "Ahhh... yeah, that's right. Your brother, [mc]...",

        # BM script2:7334
        "(Wake up [mc], we're talking about Penelope here. Still not gonna happen.)":
            "(Wake up [mc], we're talking about your big sister here. Never gonna happen.)",

        # BM script2:7404
        "But that's why I'm glad to have you here, [mc].":
            "But that's why I'm glad to have you here, bro.",

        # BM script2:7534
        "I might need you to be my photographer more often, [mc]!":
            "I might need you to be my photographer more often, little brother!",

        # BM script2:7691
        "Come on Penny, don't tell me you're actually embarrassed about yourself in these pictures?":
            "Come on sis, don't tell me you're actually embarrassed about yourself in these pictures?",

        # BM script2:7705
        "I don't mind you seeing me like this, because... I don't know, I just feel comfortable around you.":
            "I don't mind you seeing me like this, because you're my little brother.",

        # BM script2:7708
        "And besides, what would my mom say if she saw me posting those pictures? She'd probably think it was an introductory photoshoot to a porno or something...":
            "And besides, what would Mom say if she saw me posting those pictures? She'd probably think it was an introductory photoshoot to a porno or something...",

        # BM script2:7720
        "Thank you for understanding my absurdities, [mc].":
            "Thank you for understanding my absurdities, bro.",

        # BM script2:7722
        "Anytime, Penny. I hope you’ll tolerate mine too.":
            "Anytime, sis. I hope you’ll tolerate mine too.",

        # BM script2:7973
        "That Valentino guy made me realize that I'll never feel comfortable doing something like this with a stranger. But you're no stranger, [mc], and since I have you here...":
            "That Valentino guy made me realize that I'll never feel comfortable doing something like this with a stranger. But you're my little brother, [mc], and since I have you here...",

        # BM script2:7992
        "(Oh my god, am I about to see Penelope naked?)":
            "(Oh my god, am I about to see my big sister naked?)",

        # BM script2:8104
        "(Don’t think about Penelope's huge, perfect tits.)":
            "(Don’t think about your sister's huge, perfect tits.)",

        # BM script2:8107 {inject}
        "(Or how her breasts are slightly paler than the rest of her body... because she probably never sunbathes topless... meaning you're likely the first man who's gotten to see her breasts in who knows how long... and...)":[
            ("(Or how her breasts are slightly paler than the rest of her body... because she probably never sunbathes topless... meaning you're likely the first man who's gotten to see your sister's breasts in who knows how long...)","script2:8107",[
                'mc "(Shit... Why does it feel so good knowing this?)"'
            ]),

            # Bonus Mod
            ("(Or how her breasts are slightly paler than the rest of her body... because she probably never sunbathes topless... meaning you're likely the first man who's gotten to see your sister's breasts in who knows how long...)","script2:8189",[
                'mc "(Shit... Why does it feel so good knowing this?)"'
            ]),

            # Multi Mod
            ("(Or how her breasts are slightly paler than the rest of her body... because she probably never sunbathes topless... meaning you're likely the first man who's gotten to see your sister's breasts in who knows how long...)","script2:8123",[
                'mc "(Shit... Why does it feel so good knowing this?)"'
            ]),
        ],

        # BM script2:8115
        "Oh, come on, [mc]!":
            "Oh, come on, bro!",

        # BM script2:8119
        "I think that’s good enough, Penny. Valentino is gonna come back at any moment.":
            "I think that’s good enough, sis. Valentino is gonna come back at any moment.",

        # BM script2:8140
        "(Is this huge thing I'm feeling... his...)":
            "(Is this huge thing I'm feeling... my brother's...)",

        # BM script2:8180
        #"Um... Hey Penny, do you have all of your belongings?":
        #    "Um... Hey sis, do you have all of your belongings?",

        # BM script2:8198
        "I don't know what it is about you, but... I always have so much fun when you’re around.":
            "I don't know what it is about you, little brother, but... I always have so much fun when you’re around.",

        # BM script2:8200
        "Me too, Penelope.":
            "Me too, sis.",

        # BM script2:8241
        "Awesome! I can't wait to play with you, Penny!":
            "Awesome! I can't wait to play with you, sis!",

        # BM script2:8306
        "Um... Yeah. Why? Do you know her?":
            "Um... Yeah, she's my sister. Why? Do you know her?",

        # BM script2:8315
        "I was wondering why Nancy and her shared the same last name on your followers list. Nancy is her mom!":
            "I was wondering why you, Nancy, and her shared the same last name on your followers list. You're all related!",

        # BM script2:8410
        # BA/N: moved from half-sis map
        "(Nah, I'm probably imagining things... just like Chang does all the time.)":
            "(Nah, I'm probably imagining things... after all, she is my sister. There's no way she's actually flirting with me... right?)",

        # BM script2:8420
        "And now I’ve come to learn that you’re friends with Penelope too?!":
            "And now I’ve come to learn that you’re Penelope’s brother too?!",

        # BM script2:8624
        "Have fun playing.":
            "Have fun playing, bro.",


    # -----------------------------------------
    # v0.3 script3.rpy

        # BM script3:2808 (d)
        "Especially the youngest daughter. She's extremely naive and easily manipulated.":
            "Especially the middle daughter. She's extremely naive and easily manipulated.",

        # BM script3:2814
        "*Chuckles* Fine, you win, Mr. Puppet Master. But only because I don’t want to take this sun for granted. Now scooch over.":
            "*Chuckles* Fine, you win. But don't forget you're part of that \"foolish family\" too, Mr. Puppet Master. Now scooch over.",

        # BM script3:2867
        "And what about Penelope?":
            "And what about Penny?",

        # BM script3:2896 (d)
        "H-Holy shit, [mc]!":
            "H-Holy shit, bro!",

        # BM script3:2910
        "Take that back, moron. Your problem is with me, not her.":
            "Take that back, moron. Your problem is with me, not my sister.",

        # BM script3:2912
        "Don't worry, I'm not going to waste time on your whore anymore.":
            "Don't worry, I'm not going to waste time on your whore of a sister anymore.",

        # BM script3:3044
        "Yeah, Roman style. We're playing with my mom. It's gonna be her first time.":
            "Yeah, Roman style. We're playing with our mom. It's gonna be her first time.",

        # BM script3:3195 (d)
        "Hey, that's not fair! You know it was {i}Thanatos{/i} who took it from me!":
            "Hey, that's not fair sis! You know it was {i}Thanatos{/i} who took it from me!",

        # BM script3:3844
        "But we'd need Nancy and Penelope.":
            "But we'd need Mom and Penny.",

        # BM script3:3914
        "Alright, so... we need Penelope and Nancy, right?":
            "Alright, so... we need your mom and Penelope, right?",

        # BM script3:3936 (p)
        "I thought [mc] called me.":
            "I thought my brother called me.",

        # BM script3:3941
        "Penelope and I know each other from college, [mc].":
            "Penelope and I know each other from college, [mc]. I didn't realize you two were siblings.",

        # BM script3:4014
        "Now we just need Nancy to join us, and our super-heist roster will be complete!":
            "Now we just need Miss [lastname] to join us, and our super-heist roster will be complete!",

        # BM script3:4296
        "Don’t worry Penny, you'll feel better soon. It only gets better from here on out! Come on, let me give you a hand before you get soaked!":
            "Don’t worry sis, you'll feel better soon. It only gets better from here on out! Come on, let me give you a hand before you get soaked!",

        # BM script3:4615
        "And this here is Penelope, and next to her...":
            "And this here is my sister, Penelope, and next to her...",

        # BM script3:4699
        "Since it’s only your first day in Eternum, I think I should do it, Penelope. Just to be safe.":
            "Since it’s only your first day in Eternum, I think I should do it, Penny. Just to be safe.",

        # BM script3:4829 (d)
        "It’s good for you! Mommy told me!":
            "It’s good for you! Mommy told us!",

        # BM script3:4846 (d)
        "Oh yeah! Thank you [mc]!":
            "Oh yeah! Thank you bro!",

        # BM script3:4916
        "(This nanny gig just isn't enough to pay the bills, and between paying the girls' tuition and the mortgage...)":
            "(We have enough money at the moment but between paying the kids' tuition and taking over the mortgage, it's only going to increase...)",

        # BA/N: added idea for why Orion/Annie taken by dad: She wanted to raise all the children on her own but ultimately can't since she has no job yet. Dad took him/Annie to lighten the load.
            # But also I have no idea how divorce and child support works lmao

        # BM script3:4918
        "(I'm not gonna be able to hold out much longer. They'll take the house from me if I don't get some sort of extra income this month. I can only fend off the bank for so long...)":
            "(I {i}need{/i} to be able to support Dalia and Penny by myself once the divorce is done. I already had to let him take [mc] since I can't provide for all of them alone right now...)",

        # BM script3:4919
        "([mc]'s father is already generously paying me more than he should for taking care of his son. But even with that extra money, it's only delaying the inevitable.)":
            "(God, this all hurts so much...)",

        # BM script3:4924
        "(What if I don't get this job either? What if I have to take the girls out of school and transfer them? What if we don't have enough money to...)":
            "(What if I don't get this job either? What if I have to take the kids out of school and transfer them? What if we run out of money before...)",

        # BM script3:4966
        "I need you to stay and take care of Dalia and [mc].":
            "I need you to stay and take care of your siblings.",

        # BM script3:5007
        "Do you have any idea how much I've sacrificed so that you and Dalia would never be left wanting?!":
            "Do you have any idea how much I've sacrificed so that you three would never be left wanting?!",

        # BM script3:5080
        "*Clears throat* Hello, this is Nancy Carter.":
            "*Clears throat* Hello, this is Nancy [lastname].",

        # BM script3:5087
        "Um... I'm afraid I must cancel the interview. I couldn't find anyone to watch my daughter tonight, so...":
            "Um... I'm afraid I must cancel the interview. I couldn't find anyone to watch my kids tonight, so...",

        # Following 3 lines rewritten since MC should've watched Frozen before with his family

        # BM script3:5098 (d)
        "And then there's Olaf!":
            "Let's play the scene where they meet Olaf!",

        # BM script3:5099 (d)
        "He was just a normal snowman, but one day Elsa gave him life with her magic and now he can talk!":
            "I'll be Olaf and Sven, and you be Anna and Kristoff.",

        # BM script3:5100 (d)
        "He's super fun!":
            "Or do you want to be Sven this time?",

        # BM script3:5105 (d)
        "Nothing... I’m just sad because in a couple of weeks, my dad will be bringing me with him to Europe.":
            "Nothing... I'm just sad because in a couple of weeks, Dad will be bringing me with him to Europe.",

        # BM script3:5107 (d)
        "Really? For how long?":
            "Oh yeah... But you'll come back, right?",

        # BM script3:5111 (d)
        "Well you can still come play with me after school, right?":
            "Well, maybe you can come over to play with me after school?",

        # BM script3:5118 (d)
        "Well, if you can't visit me anymore, then I'm going to visit you!":
            "Well, if you can't visit me, then I'm going to visit you!",

        # BM script3:5171 (d)
        "Absolutely! Don't worry sis, I'll protect you, [mc], and Mom!":
            "Absolutely! Don't worry, sis, I'll protect you, bro, and Mom!",

        # BM script3:5210 (d)
        "[mc] ate it all in one sitting!":
            "Bro ate it all in one sitting!",

        # BM script3:5219 (d)
        "Quickly, quickly! Pick up everything, [mc]!":
            "Quickly, quickly! Pick up everything, bro!",

        # BM script3:5267 (p)
        "It was a fun day. And... well, Mom got the job, we were able to keep the house, and our lives got a lot better after that.":
            "It was a fun day. I mean, our family did split up soon after... but Mom got the job, we were able to keep the house, and things did get better for the three of us here after that.",

        # BM script3:5970 (p)
        "We're just friends. I've only seen her half-naked once... during a photoshoot.":
            "She's my sister. I've only seen her half-naked dur– I-I meant a long time ago. Y-yeah.",

        # BM script3:5972 (p) {specific}
        # Excludes script5:6310 (no), script7:10365 (no)
        "We're just friends.":[
            ("She's my sister.","script3:5972"),

            # Bonus Mod
            ("She's my sister.","script3:6016"),

            # Multi Mod
            ("She's my sister.","script3:5983"),
        ],

        # BM script3:5987
        "*Giggles* I guess I misread the looks she gave you...":
            "*Giggles* Sister, huh? I guess I {i}really{/i} misread the looks she gave you...",

        # BM script3:5991
        "So tell me... don't you wanna see a bit more? If I had a \"friend\" who looked like this, I’d be dying to find out what’s underneath all those clothes...":
            "So tell me... don't you wanna see a bit more? If I had a \"sister\" who looked like this, even I’d be dying to find out what’s underneath all those clothes...",

        # ========== START label mod "potionslabel_mod" ==========
            # line numbers for both files 

        # BM script3:6291 IncestLables:2880
        "Sometimes I forget I'm friends with a celebrity.":
            "Sometimes I forget I'm related to a celebrity.",

        # BM script3:6294 IncestLables:2883
        "*Giggles* You even sleep under the same roof as me!":
            "*Giggles* Imagine what people would give to always be this close to me!",

        # BM script3:6296 IncestLables:2885
        "That makes me very uncomfortable, to be honest. I’m gonna need a little more fanfare from you, [mc].":
            "That makes me very uncomfortable, to be honest. I’m gonna need a little more fanfare from you, little brother.",

        # BM script3:6300 IncestLables:2889
        "*Laughs* No, but seriously, that's one of the things I like about you. You just treat me like a human being.":
            "*Laughs* No, but seriously, thanks for still treating me like a human being after all this time.",

        # BM script3:6315 IncestLables:2904
        "Honestly Penny, you really are special to me, but not because you're famous on Instagram.":
            "Honestly Penny, you really are special to me, but not because you're famous on Instagram. I couldn't care less about your social network pages or how many followers you have... ",

        # BM script3:6316 IncestLables:2905
        "I couldn't care less about your social network pages or how many followers you have... I only care about the person behind it. You became a special person to me just because of who you are.":
            "I only care about the person behind it. You're my big sister, and I know the sides of you they'll never see, the real you. You're a special person to me just because of who you are.",

        # BM script3:6374 IncestLables:2963
        "Nice to meet you. I’m [mc], and this is Penelope and Luna.":
            "Nice to meet you. I’m [mc], and this is my sister Penelope, and our friend Luna.",

        # BM script3:6482 IncestLables:3071
        "This morning, in the bathroom. Right after [mc] used the shower.":
            "This morning, in the bathroom. Right after my brother used the shower.",

        # BM script3:6564 IncestLables:3153
        "A friend!":
            "Someone I know!",

        # BM script3:6575 IncestLables:3164
        "Was he [mc]?":
            "Could it be... your brother?",

        # BM script3:6583 IncestLables:3179
        "(That's too bad...)":
            "(Obviously not. We're siblings.)",

        # Label mod lines adding reactions from Luna and Prof Mandrake here

        # BM script3:6646
        "Your BDSM-lover friend said you've all been to the Emporium already, right?":
            "Your BDSM-loving sister said you've all been to the Emporium already, right?",

        # ========== END label mod "potionslabel_mod" ==========

        # BM script3:6999
        "Your looks are pretty convincing, but I'm afraid I caught you in a lie. [mc] and I have never fucked.":
            "Your looks are pretty convincing, but I'm afraid I caught you in a lie. [mc] and I would never fuck. We're siblings!",

        # BM script3:7004
        "Of course not. Ugh!":
            "Ugh, of course not! That'd be incest!",

        # BA/N: undecided which combo of Penny/Sis to use for the next four, dont want them all to be the same

        # BM script3:7338
        "It'll be my first time as well, Penny, so I wouldn't worry too much about it.":
            "It'll be my first time as well, sis, so I wouldn't worry too much about it.",

        # BM script3:7373
        #"Don't worry, Penny! You got this!":
        #    "Don't worry, sis! You got this!",

        # BM script3:7423
        "Nice job, Penny!":
            "Nice job, sis!",

        # BM script3:7445
        #"Don't be sad, Penny!":
        #    "Don't be sad, sis!",

        # BM script3:7664
        "These are my friends, Penelope and Luna.":
            "This is my eldest sister, Penelope, and my friend, Luna.",

        # BM script3:7907 (p)
        "Don't worry [mc], I'm in good hands!":
            "Don't worry bro, I'm in good hands!",

        # BM script3:8330
        "I was just looking for her! Her name is Dalia.":
            "My sister, Dalia. I was just looking for her!",

        # BM script3:8399
        "Wow... you look... hot.":
            "Wow... you look hot... I-I mean the outfit looks hot.",

        # BM script3:8710
        "Come on... I'm not gonna go there without asking for permission first.":
            "Come on, sis... I'm not gonna go there without asking for permission first.",

        # BM script3:8716
        "...It’s because I’m trying to learn to trust you, alright?":
            "...It’s because I'm trying to learn to trust you again, alright?",

        # BM script3:8726
        "(It's nice to see she’s beginning to trust me. I know she wouldn’t have told this just to anyone.)":
            "(It's nice to see she still trusts me a bit after all this time. I know she wouldn’t have told this just to anyone.)",

        # BM script3:8780
        "S-Seriously? You're a fucking pig!":
            "S-Seriously? I'm your sister, you fucking pervert!",

        # BM script3:8792
        "O-Of course not! I'd only agree to that in the first place because you'll never beat me in a fight! Like, ever!":
            "O-Of course not! You're my brother! I'd only agree to that in the first place because you'll never beat me in a fight! Like, ever!",

        # BM script3:8794
        "Well if that’s the case, then why does it matter what I want? Getting naked, testing out your... “skills”, or any other thing. You’re so positive you’re gonna win anyways!":
            "Well if that's the case, then why does it matter what I want? Getting naked, testing out your... “skills”, or any other thing. If you're so positive you're gonna win anyways, it shouldn't even matter that I'm your brother!",

        # BM script3:8798
        "Fine then, you have a deal. You’re still a pig though.":
            "Fine then, you have a deal. You’re a absolute pig though, asking that of your sister.",

        # BM script3:8813
        "I'll suck your cock.":
            "I'll suck your cock, {i}brother{/i}.",

        # BM script3:9339 (n)
        "Mmm, there’s the sweet [mc] I know...":
            "Mmm, that’s my sweet little [mc]...",

        # BM script3:9576
        "*Laughs* Oh, don’t you dare! You’re too much!":
            "*Laughs* Oh, don’t you dare! That makes you royalty too!",

        # BM script3:9588
        "Indeed... I don’t see anyone else around here...":
            "Well... Seeing as you're both my prince and the champion, bit of both...",

        # BM script3:9610
        "N-Nancy...":
            "M-Mom...",

        # BM script3:9624
        "We bathed together countless times when you were younger, remember? Your father left for business trips frequently so you stayed over all the time.":
            "We bathed together countless times when you were younger, remember?",

        # BM script3:9627
        "Well, that's different. I was, what, like... 5 years old? And I don’t remember much from back then.":
            "Well, that's different. We haven't bathed together since I was, like, 5 years old? And I don’t remember much from back then.",

        # BM script3:9648
        "You, my Champion. Will you be joining me, or do you have to get going?":
            "You, my Prince. Will you be joining me, or do you have to get going?",

        # BM script3:9663
        "(Keep it together! She’s been like a mother to you. Focus, [mc]! This is strictly a bath!)":
            "(Keep it together! She's your mother. Focus, [mc]! This is strictly a bath!)",

        # BM script3:9693
        "I mean, earlier I was playing with Penelope and we were able to revisit one of her memories in great detail! Can you believe it? An actual memory from years past!":
            "I mean, earlier I was playing with Penny and we were able to revisit one of her memories in great detail! Can you believe it? An actual memory from years past!",

        # BM script3:9694
        "And I saw you! Back when you were my babysitter. I was too young to remember most of that time, but you looked exactly like you did in our old pictures!":
            "And I saw you! Back when we lived together. I was too young to remember most of that time, but you looked exactly like you did in our old pictures!",

        # BM script3:9706
        "I owe it to my mother. It seems like once she reached 25, she stopped aging. She died shortly after Dalia was born, but she was always so full of life.":
            "I owe it to your grandma. It seems like once she reached 25, she stopped aging. She died shortly after Dalia was born. It's a shame she never got to met you, she was always so full of life.",

        # BM script3:9709
        "Dalia and Penelope are gonna be very blessed when they get older too.":
            "Dalia and Penny are gonna be very blessed when they get older too.",

        # BM script3:9714
        "Girlfriend. No doubt about it at all.":
            "Girlfriend. No doubt about it at all. No one would believe me if I said you're my mother.",

        # BM script3:9729
        "Not at all. Fire away, my Empress.":
            "Not at all. Fire away, Mom.",

        # BM script3:9736
        "I see... my young [mc] has a little experience under his belt. Very interesting...":
            "I see... my boy has a little experience under his belt. Very interesting...",

        # BM script3:9761
        "What about Dalia and Penelope?":
            "What about... Dalia and Penelope?",

        # BM script3:9767
        "Um... I... I'm not...":
            "W-What? T-They're my sisters!",

        # BM script3:9768
        "I mean... I'd never dare.":
            "I wouldn't... I'd never dare.",

        # BM script3:9770
        "Why not? I wouldn’t mind having you as my son-in-law...":
            "Forget that for just a moment. Just... as a hypothetical. ",

        # BM script3:9774
        "Let’s say one of my daughters came in here right now and asked you to have sex with them. No tricks or schemes... they just desired you. Would you say yes?":
            "Let's say one of your sisters came in here right now and asked you to have sex with them. No tricks or schemes... they just truly desired you. Would you say yes?",

        # BM script3:9779
        "I’m going to be totally frank with you here, so don’t get mad at me.":
            "I’m going to be totally frank with you Mom, so please don’t get mad at me.",

        # BM script3:9780
        "I'd be lying if I said that doesn’t sound like a dream come true.":
            "Even if it's incest... even if it's wrong... I'd be lying if I said that doesn’t sound like a dream come true.",

        # BM script3:9789
        "As a mother, I've always feared the day that my daughters would bring a boy home for dinner. Not because I don’t want them to find someone, but rather, whether that person would be good enough for them.":
            "I've always feared the day when the girls would bring a boy home for dinner. Not because I don’t want them to find someone, but rather, whether that person would be good enough for them.",

        # BM script3:9793
        "*Giggles* I'm not sure yet. You definitely have most of the desirable qualities in a man, but still... there’s some areas of you I don’t know much about.":
            "*Giggles* What shame you're their brother. You definitely have most of the desirable qualities in a man, but still... there’s some areas of you I don’t know much about.",

        # BM script3:9794
        "As a mother, I need to make sure that you’re a good candidate in... all... areas.":
            "As your mother, I need to make sure that you’re a good candidate for your future partners in... all... areas.",

        # BM script3:9796
        "All areas, huh? How will you determine that?":
            "All areas, huh? How will you determine that, Mom?",

        # BM script3:9802
        "I couldn't. I don't know... I just see them as family.":
            "I couldn't! They're my family...",

        # BM script3:9804
        "Ah, I see. I guess it does make sense.":
            "Ah, I see. How proper of you.",

        # BM script3:9806
        "Well, there goes my plan to determine whether you’d be a good candidate or not.":
            "If only you weren't their brother. I would've enjoyed testing you to see if you could be a good candidate for them...",

        # BM script3:9808
        "*Chuckles* A plan? I thought you just enjoyed spending time with me.":
            "*Chuckles* A test? I thought you just enjoyed spending time with me.",

        # BM script3:9827
        "No, really Nancy... it honestly feels so nice to hear that coming from you. I consider you to be someone very important in my life, so it’s truly appreciated.":
            "No, really Mom... it honestly feels so nice to hear that coming from you. You're a very important person in my life, so it’s truly appreciated.",

        # BM script3:9832
        "*Chuckles* Very much. I’m honored to be your special guest... and feel so privileged to witness such a rare and honestly breathtaking sight.":
            "*Chuckles* Very much. This prince is honored you've shared your private bath... and feels so privileged to witness such a rare and honestly breathtaking sight.",

        # BM script3:9842
        "Hmph. I invite a commoner to my private baths and he can’t even contain himself. What a shame.":
            "Hmph. I invite my own son to my private baths and he can’t even contain himself. What a shame.",

        # BM script3:9865
        "(I’d hate myself if I didn’t at least try...)":
            "(I'd hate myself if I didn't at least try... I guess there's no more denying it: I like my mom.)",

        # BM script3:9866
        "I think this goes without saying, but let’s not mention this to anyone. My daughters especially... heaven knows what they’d think if they learned we bathed together.":
            "I think this goes without saying, but let’s not mention this to anyone. Your sisters especially... heaven knows what they’d think if they learned we bathed together.",

        # BM script3:9900
        "(I can tell she was looking forward to this.)":
            "(I can tell she was looking forward to this... With me, her own son... If we both want this, and no one's here to stop us...)",

        # BM script3:9910
        "I guess I never paid attention back then, since I was only five and had no interest in them...":
            "I guess I never paid attention back then, since I was just a kid and had no interest in them...",

        # BM script3:9913
        "Oh [mc]... how you’ve grown into such a strong, handsome man...":
            "Oh [mc]... you're no longer the little boy I raised so long ago... you’ve grown into such a strong, handsome man...",

        # BM script3:9914
        "After having taken care of you for so long back then... I never thought we’d be in this position now...":
            "As your mother, I never would’ve thought we’d be in this position now...",

        # BM script3:9932
        "Oh, my boy...":
            "*Giggles* Oh, my baby boy... want to suckle mommy's breasts again?",

        # BM script3:9942
        "Does the Champion truly want to serve his Empress?":
            "Does my Prince truly want to serve his Empress?",

        # BM script3:9946
        "You know... I remember from my history classes that it was always taboo for royalty to intermingle with common folk...":
            #"You know... Incest was still a huge taboo in ancient Rome. It's where the word originates from...",
            "You know... the word \"Incest\" comes from Latin—it was such a huge taboo in ancient Rome...",

        # BM script3:9947
        "But I think we’ve broken enough rules today...":
            "To think this Empress is breaking such a sacred rule on her first day...",

        # BM script3:9949
        "I need to feel my Champion... taste the forbidden fruit...":
            "I need to feel my Prince... taste the forbidden fruit...",

        # BM script3:9970
        "Oh, my C-Champion feels...":
            "Oh, my P-Prince feels...",

        # BM script3:9971
        "Oh, s-screw the Champion shit...":
            "Oh, s-screw the royalty shit...",

        # BM script3:10004
        "You took care of me countless times...":
            "You’ve always taken care of me...",

        # BM script3:10100
        "I'll fulfill them all...":
            "*Chuckles* Like having sex with your son?",

        # BM script3:10103 {specific}
        # Excludes script:6153 (a), script9:18643 (mc), script9:20400 (l)
        "And now...":[
            ("*Giggles* Yes, and now...","script3:10103"),

            # Bonus Mod
            ("*Giggles* Yes, and now...","script3:10177"),

            # Multi Mod
            ("*Giggles* Yes, and now...","script3:10123"),
        ],

        # BM script3:10106
        "This time though... I want you to lie back and let your babysitter do all the work...":
            "This time though... I want you to lie back and let your mother do all the work...",

        # BM script3:10132
        "*Whispering* What for? It's only a guard!":
            "*Whispering* What for? It's only a guard! He doesn't know I'm your son.",

        # BM script3:10137
        "*Whispering* Oh, that's a good point.":
            "*Whispering* Oh, shit... I told him earlier that Dalia was my sister.",

        # BM script3:10177
        "(Why does God hate me?)":
            "(Why does God hate me? Is this karma?)",

        # BM script3:10213
        "(Man, I was so damn close to fucking Nancy...!)":
            "(Man, I was so damn close to fucking my own mom! To cross that forbidden line...)",

        # BM script3:10221 (d)(p)
        "(Little do they know... heh.)":
            "(Man, if they ever found out...)",

        # BM script3:10245 (p)
        "*From downstairs* [mc]? Is that you? Finally!":
            "*From downstairs* Bro? Is that you? Finally!",

        # BM script3:10382 (n)
        "Yeah, I took [mc] on a tour of the palace afterward. We visited the atrium for awhile and he showed me a few of the skills he’s learned.":
            "Yeah, I took your brother on a tour of the palace afterward. We visited the atrium for awhile and he showed me a few of the skills he’s learned.",

        # BM script3:10442 (d)
        "Hah! I don't think you know us as well as you believe. After all, you've only been living with us for a short while. And the others, you only met them a few weeks ago!":
            "Hah! I don't think you know us as well as you believe. After all, you've only been living with us again for a short while. We've changed in the years you were gone. And the others, you only met them a few weeks ago!",


    # -----------------------------------------
    # v0.4 script4.rpy

        # BM script4:2228 (n)
        "I guess that I'm just too persuasive.":
            "Looks like it's a siblings-only privilege today!",

        # BM script4:2230
        "That must be it...":
            "*Laughs* Oh dear, my children are finally rebelling against me.",

        # BM script4:2268
        "Bye... “Mommy.”":
            "Bye Mommy.",

        # BM script4:2275
        "I'm not Nancy's daughter. I mean, I'm not even a girl! Do I have to spell it out or what?":
            "I'm her son! I mean, I'm not even a girl! Do I have to spell it out or what?",

        # BM script4:2364
        "What the hell, Dalia?!":
            "What the hell, Dal?!",

        # BM script4:2425
        "Thanks buddy. You're a good friend.":
            "Thanks [mc]. You're a good brother.",

        # BM script4:2513
        "I'll go as fast as I can. Thank you, [mc].":
            "I'll go as fast as I can. Thank you, bro.",

        # BM script4:2658
        "Show them what you got, Dalia!":
            "Show them what you got, sis!",

        # BM script4:2930
        "And on my right, weighing in at 125 lbs... Dalia Carter!":
            "And on my right, weighing in at 125 lbs... Dalia [lastname]!",

        # BM script4:2931
        "Let's go Dalia! Kick his ass!":
            "Let's go Daly! Kick his ass!",

        # BM script4:2988
        "[mc]! I won!":
            "Bro! I won!",

        # BM script4:3002
        "Congrats, Dalia.":
            "Congrats, sis.",

        # BA/N: WIP. next three could use work, or these people are just insanely accepting lol

        # BM script4:3031
        "I didn't know you were dating!":
            "I didn't know you were dating! I thought he was your brother?",

        # BM script4:3045
        "I already knew, her mom told me. I’m her greatest confidante.":
            "I already knew, their mom told me. I’m her greatest confidante.",

        # BM script4:3047
        # BA/N: couldn't think of a reasonable alternative so went absurd instead lol
        "You two make a great couple!":
            "I wish my brother would kiss me like that!",

        # BM script4:3050
        "We're just old friends!":
            "We're just siblings!",

        # BM script4:3051
        "And d-don't tell my mom!":
            "And d-don't tell our mom!",

        # BM script4:3056
        "It doesn't mean anything!":
            "A-And I heard in Europe, siblings kiss all the time!! It doesn't mean anything!",

        # BM script4:3112
        "*Imitating Dalia* [mc]! I won! I won! Did you see it!? Muah Muah *imitates kissing noises*":
            "*Imitating Dalia* Bro! I won! I won! Did you see it!? Muah Muah *imitates kissing noises*",

        # BM script4:3124, overwritten by BM script:8731, okay
        # "Dalia!" -> "Dal!"

        # BM script4:3145
        "I'm the lame one? Go tell that to that crybaby girlfriend of yours.":
            "I'm the lame one? Go tell that to that crybaby sister of yours.",

        # ========== START label mod "daliacove_mod" ==========
            # line numbers for both files 

        # BM script4:3526 IncestLables:601
        "Thank you [mc].":
            "Thank you bro.",

        # BM script4:3583 IncestLables:663
        "What are you concocting in that pervy little brain of yours?":
            "What are you concocting in that pervy little brain of yours, brother?",

        # BM script4:3595 IncestLables:675
        "This bikini looks good on you, Dalia.":
            "This bikini looks good on you, sis.",

        # BM script4:3633 IncestLables:718
        "If I had made out with my sister yesterday, does that mean you could say that you’ve kissed Penelope too?":
            "If I had made out with Penelope yesterday, does that mean you could say that you’ve kissed Penelope too?",

        # BM script4:3648 IncestLables:733
        "I loved spending some time with you in your server, Dalia. Thanks for letting me visit.":
            "I loved spending some time with you in your server, sis. Thanks for letting me visit.",

        # BM script4:3663 IncestLables:752
        "Isn't that what you wanted?":
            "Isn't that what you wanted? For your dear sister to suck your cock?",

        # BM script4:3679 IncestLables:
        "So... as a thank you for everything... I'm choosing not to overthink your definition of \"beating me in a fight.\"":
            "So... as a thank you for everything... I'm choosing not to overthink your definition of \"beating me in a fight\"... and to ignore the fact we're siblings...",

        # BM script4:3716 IncestLables:821
        "You made me so fucking horny, Dalia. Do you see how hard you made me?":
            "You made me so fucking horny, Daly. Do you see how hard you made me?",

        # BM script4:3747 IncestLables:852
        "You're in denial today, Dalia...":
            "You're in denial today, sis...",

        # BM script4:3760 IncestLables:865
        "You're driving me insane, Dalia...":
            "You're driving me insane, sis...",

        # BM script4:3768 IncestLables:873
        "Does it feel good?":
            "Does your sister's mouth feel good?",

        # BM script4:3775 IncestLables:880
        "(Oh my god, Dalia's sucking my cock...)":
            "(Oh my god, my sister’s really sucking my cock...)",

        # BM script4:3840 IncestLables:945
        "You're basically drooling, Dalia... You like my cock that much?":
            "You're basically drooling, Daly... You like your brother's cock that much?",

        # BM script4:3844 IncestLables:949
        "If you wanna stop, just give me a sign, babe...":
            "If you wanna stop, just give me a sign, sis...",

        # BM script4:3905 IncestLables:1010
        "Would you like that, you pervert? Are you hungry for some cum?":
            "Whose the pervert now? Are you hungry for some of your brother's cum?",

        # BM script4:3909 IncestLables:1014
        "I want you to release your seed in my little mouth...":
            "I want my brother to release his seed in my little mouth...",

        # ========== END label mod "daliacove_mod" ==========

        # BM script4:5041
        "Penelope invited me to a costume party at her campus.":
            "Pennny invited me to a costume party at her campus.",

        # BM script4:7316 (p)
        "Good luck, [mc]!":
            "Good luck, bro!",

        # BM script4:7318
        "Hey! Thanks, Penny!":
            "Hey! Thanks, sis!",

        # BM script4:7347 (p)
        "There's no way out of this friend zone...":
            "She really does just think of me as her little brother...",

        # BM script4:7359 (d)
        "Heeeey! Good luck with the fat cats, [mc]!":
            "Heeeey! Good luck with the fat cats, bro!",

        # BM script4:7360
        "Thanks Dalia!":
            "Thanks sis!",

        # BM script4:7384 (d)
        # BA/N: Disabled, bro does not work here
        # "“We” have a party? Who’s “we”? You and [mc]?":
        #     "“We” have a party? Who’s “we”? You and bro?",

        # BM script4:7387 (p)
        # BA/N: Disabled, bro does not work here
        # "Yeah, Nova, [mc], and I are going to a party on campus. I could have sworn I told you about it...":
        #     "Yeah, Nova, bro, and I are going to a party on campus. I could have sworn I told you about it...",

        # BM script4:7402 (p)
        "What other people? You? Mom? Annie? I'm sure [mc] doesn't mind either. He's like... family. Like a little brother, almost.":
            "What other people? You? Mom? Annie? I'm sure [mc] doesn't mind either. He's... family. Our little brother...",

        # BM script4:7405 (d)
        "Yeah... like a little brother...":
            "Yeah... our little brother...",

        # BM script4: 7408 (p)
        "With [mc]? Pffft, please, my bar is WAY higher. You've seen my Instagram DMs: models, actors, influencers... did you know that that Gigachad meme guy from a few years ago tried sliding into my DMs?":
            "To our brother? Pffft, that would be incest! And please, even if he wasn't our brother, my bar is WAY higher. You've seen my Instagram DMs: models, actors, influencers... did you know that that Gigachad meme guy from a few years ago tried sliding into my DMs?",

        # BM script4:8176 (misc)
        # BA/N: borrowed from aunt map, random but funny change
        "Actually, he was caught with HER sister in HIS office!":
            "Actually, he was caught with HIS OWN sister in HIS office!",


    # -----------------------------------------
    # v0.5 script5.rpy

        # BM script5:290 (x)
        "He and his friends are always in some kind of trouble. Which is exhausting, but also... entertaining. In a way.":
            "He and his family and friends are always in some kind of trouble. Which is exhausting, but also... entertaining. In a way.",

        # BM script5:465 (d)
        "(I don't even like him. The only guy I kinda liked lately wasn’t even into me.)":
            "(I don't even like him. The only guy I kinda liked lately wasn’t even into me... not to mention he's my brother...)",
            #"(I don't even like him. The only guy I kinda liked lately was my own brother... and he wasn’t even into me.)",

        # BM script5:466 (d)
        "(Which was for the better, though. I can't believe I had a crush on that idiot. Thank god that's over now.)":
            "(So this is {i}definitely{/i} for the better. I can't believe I had a crush on my own little brother! Thank god that's over now.)",

        # BM script5:629
        "Oh, that is very likely, actually, Ms. Carter. It would be poetic and, at the same time, easy to make it look like an accident.":
            "Oh, that is very likely, actually, Ms. [lastname]. It would be poetic and, at the same time, easy to make it look like an accident.",

        # BM script5:1027
        "Could you help me with it, [mc]? I've gotta go before leaving.":
            "Could you help me with it, honey? I've gotta go before leaving.",

        # BM script5:1049
        "It's been quite a challenge trying to find you alone this past week, [mc]...":
            "It's been quite a challenge trying to find you alone this past week, my boy...",

        # BM script5:1067
        "I want you to fuck me, [mc]. Hard. And filthy.":
            "I want you to fuck me, son. Hard. And filthy.",

        # BM script5:1124 {inject}
        "What have I done to deserve this? What god have I pissed off?!":[
            ("What have I done to deserve this? What god have I pissed off?!","script5:1124",[
                'mct ". . ."',
                'mct "Probably one against incest, actually. Which might be a lot of them."'
            ]),

            # Bonus Mod
            ("What have I done to deserve this? What god have I pissed off?!","script5:1143",[
                'mct ". . ."',
                'mct "Probably one against incest, actually. Which might be a lot of them."'
            ]),

            # Multi Mod
            # script5:1124, same as orginal
        ],

        # BM script5:1244
        "I already told Penelope and Nova that I'd be going with them to a costume party at the University tomorrow night, so...":
            "I already told Penny and Nova that I'd be going with them to a costume party at the University tomorrow night, so...",

        # BM script5:1246
        "I already told Penelope that I'd be going with her to a costume party at the University tomorrow night, so...":
            "I already told Penny that I'd be going with her to a costume party at the University tomorrow night, so...",

        # BM script5:4438 chat:637 (no)
        "You don't live with the Carters anymore?":
            "You don't live with your family anymore?",

        # BM script5:4799 (p)
        #"*Knocks on the door* [mc]? Is that you?":
        #    "*Knocks on the door* Bro? Is that you?",

        # BM script5:4823
        "*Grabbing some bottles from the closet* I guess we have that in common. I’m perfectly fine with showing off my body too.":
            "*Grabbing some bottles from the closet* I guess we have that in common. I’m perfectly fine with showing off my body too. Plus we're family, so it's not like it's a big deal, right?",

        # BM script5:4862
        "I thought you said you didn't mind me coming in.":
            "I thought you said you didn't mind your big sis coming in.",

        # BM script5:4872
        "Anyway, now that we’ve both seen each other naked, there's really no reason to make a big deal about this in the future.":
            "Anyway, it's not like we haven’t seen each other naked before, so there's really no reason to make a big deal about this in the future.",

        # BM script5:4909
        "Penelope Carter... you’re gonna drive me mad.":
            "Penelope [lastname]... you’re gonna drive me mad.",

        # BM script5:4986
        #"Penny? I'm ready!":
        #    "Sis? I'm ready!",

        # BM script5:4993
        "You look spectacular, Penny. Really hit it out of the park!":
            "You look spectacular, sis. Really hit it out of the park!",

        # BM script5:5086
        "*Chuckles* Don’t be silly! You're staying with us until we say so. No escaping the Carters!":
            "*Chuckles* Don’t be silly, little brother! You're staying with us until we say so. No escaping the family this time!",

        # BM script5:5192
        "Can you take a pic of us before going in, [mc]?":
            "Can you take a pic of us before going in, bro?",

        # BM script5:5217
        "*Chuckles* You're too excited, [mc].":
            "*Chuckles* You're too excited, lil bro.",

        # BM script5:5220 {inject}?
        # BA/N: incorporating incest skip idea from aunt map. May not use
        #"*Laughs* Fair enough.":[
        #    ("*Laughs* Fair enough.","script5:5220",[
        #        "show df 57 with dis06",
        #        'p "Hey, [mc]... before we go in, don’t let anyone you’re related to me, okay?"',
        #        'p "There are a few people here I have some... {i}disagreements{/i} with, and I don’t want to get you involved in it."',
        #        "show df 58",
        #        'mc "Oh, if you say so. But don’t hesitate to ask me for help if you need it, alright?"',
        #        "show df 57",
        #        'p "*Chuckles* Sure, I will!"',
        #    ]),
        #
        #    # Bonus Mod script5:5268
        #
        #    # Multi Mod script5:5228
        #],

        # BM script5:5291
        "U-Uh... a-are you sure?":
            "U-Uh... i-isn't he your brother? A-are you sure?",

        # BM script5:5294
        "I thought it was just a temporary thing, but... shit, I don't know anymore.":
            "I thought it was just a temporary thing, but... shit, I don't know anymore. Honestly, I think him being my brother is making it... {i}more{/i} exciting.",

        # BM script5:5302
        # BA/N: borrowed from aunt map
        "But he might not be into me like that so... keep it secret!":
            "But we're still siblings, and he might not be into me like that so... keep it secret!",
        
        # BM script5:5316
        # BA/N: borrowed from aunt map
        "(A BIG one!)":
            "(A BIG one! The biggest one I've ever heard!)",
        
        # BM script5:5322
        #"(But holy shit, did she say she has a crush on [mc] too?!)":
        #    "(But holy shit, did she say she has a crush on her brother too?!)",

        # BM script5:5344
        # BA/N: borrowed from aunt map
        "(Nothing happened. So what if my new bestie Penny and I have a crush on the same boy?)":
            "(Nothing happened. So what if my new bestie Penny and I have a crush on the same boy? So what if he's her b-brother?)",

        # BM script5:6215 (no)
        "Penelope? Penelope Carter? That IG model in the journalism program?":
            "Penelope? Penelope [lastname]? That IG model in the journalism program?",

        # BM script5:7775
        "Tell her to join me and Penelope when she's done!":
            "Tell her to join me and Penny when she's done!",

        # BM script5:7814
        "I've gotta find Penelope before she sees the photos.":
            "I've gotta find Penny before she sees the photos.",

        # BM script5:7942
        "Hey Penny!":
            "Hey sis!",

        # BM script5:7990
        "And you thought of asking your big titty blonde bimbo friend to lend you hers, right?":
            "And you thought of asking your big titty blonde bimbo sister to lend you hers, right?",

        # BM script5:8141
        "No, not really. We're just friends. I've been in Kredon just for a couple of months, actually.":
            "No, not really. I'm her brother. I moved back to Kredon just few months ago, actually.",

        # BM script5:8184
        "Actually, yeah! I'm looking for Penelope. Penelope Carter. Do you know her?":
            "Actually, yeah! I'm looking for Penelope. Penelope [lastname]. Do you know her?",

        # BM script5:8204
        "Um... no, not really. We're just friends. I've been in Kredon just for a couple of months.":
            "Um... no, not really. I'm her brother. I moved back to Kredon just few months ago.",

        # BM script5:8275
        "Hi, [mc]! Sorry for the wait.":
            "Hey, bro! Sorry for the wait.",

        # BM script5:8281
        "Goddamn, this dress looks GREAT on you, Penny.":
            "Goddamn, this dress looks GREAT on you, sis.",

        # BM script5:8317
        "I came with Penelope. I live with her, as part of the Student Exchange Program.":
            "I came with Penelope, she's my sister. I moved back in with her as part of the Student Exchange Program.",

        # BM script5:8345
        "*Chuckles* I'd say the Carters played a big role in that, yeah...":
            "*Chuckles* I'd say my family played a big role in that, yeah...",

        # BM script5:8369
        # ONLY ACTIVATE if using skip 
        #"{i}Something{/i} tells me they don’t like each other much... I’d better not get in the middle of this.":
        #    "{i}Something{/i} tells me they don’t like each other much... This must one of the “disagreements” Penelope told me about. I’d better not get in the middle of this.",

        # ========== START Truth or Dare Game ==========
            # BA/N: Entire game needs a LOT more work imo but I dont have any good ideas
            # either the other players are just super tolerant of the incest vibes between Penny and MC
            # or take the easy option and "skip" incest like the aunt map did at AU script5:5217
                # activate BM script5:5220 if skipping 

        # BM script5:8455
        "I guess that's why Penelope likes you.":
            "Penelope, did you know he was hung like this?",

        # BM script5:8457
        "S-Shut up, Regina. I haven't even seen it yet.":
            "S-Seriously, Regina? He's my brother, of course I haven't even seen it yet.",

        # BM script5:8461
        "Uhh... I-I mean...":
            "Uhh... I-I meant in a long time... not since we were kids...",

        # BM script5:8472
        "Ohh... this is the kind of dare I like.":
            "You want me to kiss Penelope... my sister?",

        # BM script5:8474
        "*Giggles* I bet you do.":
            "*Giggles* Is little [mc] scared of a little dare?",

        # BM script5:8476
        "It's my time to shine.":
            "Not at all! If you're not backing out, then I won't either.",

        # BM script5:8479
        "*Grabbing her by the waist* I love this dress, Penny.":
            "*Grabbing her by the waist and whispering* I love this dress, sis.",

        # BM script5:8500 {specific}
        # Excludes script:8623 and script3:6475
        "(Interesting...)":[
            ("(And he's her brother? Interesting...)","script5:8500"),

            # Bonus Mod
            ("(And he's her brother? Interesting...)","script5:8568"),

            # Multi Mod
            ("(And he's her brother? Interesting...)","script5:8511"),
        ],

        # BM script5:8596
        "*Chuckles* I swear if you don't say my name, I'm gonna grab my things and go home.":
            "*Chuckles* Are you about say what I think you're about to say?",

        # BA/N: this part especially, no one reacts and idk how to deal with his lmfao

        # BM script5:8598
        "*Snorts* Okay, okay, I'm gonna say [mc].":
            "*Snorts* Yeah, okay, I'm gonna say [mc].",

        # BM script5:8599
        "Just don't let it get to your head.":
            "Not that it'll ever happen, so don't let it get to your head.",

        # BM script5:8601
        "Penelope Carter just said that she'd like to have a threesome with me. It's difficult not to be enthusiastic.":
            "*Laughs* Penelope [lastname] just said she'd like to have a threesome with her brother. How scandalous!",

        # BM script5:8603
        "I had to say someone. It's just a game.":
            "I had to say someone, better you than someone I barely know. It's just a game, anyway.",

        # BM script5:8605
        "*Chuckles* Hey, don't ruin my mood!":
            "*Chuckles* I'm definitely going to remember this.",

        # BM script5:8706
        "Do you want a glass of water, [mc]?":
            "Bro, do you want a glass of water?",

        # BM script5:8769
        # BA/N: disabled to show a bit of concern
        #"Are you okay, [mc]?":
        #    "Are you okay, lil bro?",

        # BM script5:8849
        "I'm not gonna get naked in front of everyone, [mc].":
            "Bro, I'm not gonna get naked in front of everyone.",

        # BM script5:8870
        # BA/N: tried toning down the incest implications here
        "*Laughs* You're not really gonna do this to me, right?":
            "*Laughs* Taking the easy way out, I see?",

        # BM script5:8874
        "*Chuckles* You're enjoying teasing me so much tonight, aren't you?":
            "*Chuckles* You're being such a tease tonight, aren't you?",

        # ========== END Truth or Dare Game ==========

        # BM script5:9119
        "Well, you can continue following Penelope like a puppy, like everyone else, doing what she wants and telling her how pretty she is all the time...":
            "Well, you can continue following your sister like a puppy, like everyone else, doing what she wants and telling her how pretty she is all the time...",

        # BM script5:9217
        "But... wait, she's {i}interested{/i}?":
            "...W-Wait, what do you mean she's {i}interested{/i}?",

        # BM script5:9253
        "To send them to Penelope.":
            "To send them to your sister.",

        # BM script5:9303
        "Just a friend who's gonna help me sneak into the dorm room of someone who stole something from me.":
            "Just my kid brother who's gonna help me sneak into the dorm room of someone who stole something from me.",
        
        # BM script5:9306
        "Oh, damn, that sounds exciting! That guy sounds like a real Prince Charming!":
            "Oh, damn, that sounds exciting! That brother of yours sounds like a real Prince Charming!",

        # BM script5:9309
        "Fuck that dude you were waiting for, whoever he was.":
            "Fuck waiting for your brother.",

        # BM script5:9505
        "*Whispering* I'm sorry I dragged you into this, [mc].":
            "*Whispering* I'm sorry I dragged you into this, brother.",

        # BM script5:9529
        #"Finally! I think she left, [mc]!":
        #    "Finally! I think she left, bro!",

        # BM script5:9577
        "My fucking god, [mc], you're hung like a fucking horse. That cock is a weapon!":
            "My fucking god, bro, you're hung like a fucking horse. That cock is a weapon!",

        # BM script5:9619
        "*Giggles* Oh my, I had no idea you were suffering this much, baby!":
            "*Giggles* Oh my, I had no idea you were suffering this much, bro!",

        # BM script5:9624
        "*Chuckles* Pretty please... [mc]?":
            "*Chuckles* Pretty please... little brother?",

        # BM script5:9630
        "I'm {i}so{/i} very sorry for flaunting my lewd body in front of you, [mc]. I had no idea it would cause you so much stress...":
            "I'm {i}so{/i} very sorry for flaunting my lewd body in front of you, brother. I had no idea it would cause you so much stress...",

        # BM script5:9633
        # Disabled, interferes with other lines, also doesn't work if not on other paths
        # "I like where this is going...":
        #    "I like where this is going... and I am too drunk and horny to care that she is my sister... as if I had cared with Mom and Dalia...",

        # BM script5:9670
        "Okay, take a good look, [mc].":
            "Okay, take a good look, bro.",

        # BM script5:9677
        "I'd forgotten how perfect they were, Penny.":
            "I'd forgotten how perfect they were, sis.",

        # BM script5:9681
        # BA/N: disabled, Penny and MC are roleplaying here
        #"Do you forgive me for acting naughty? For being such a tease? For flaunting myself all around you?":
        #    "Do you forgive me for acting naughty? For being such a tease? For flaunting myself all around my own brother?",

        # BM script5:9682
        "Not quite yet, Miss Carter...":
            "Not quite yet, Miss [lastname]...",

        # BM script5:9699
        "Penny... you're a fucking goddess.":
            "Sis... you're a fucking goddess.",

        # BM script5:9707
        "Admit it. You like being my personal little model, Penny.":
            "Admit it. You like being my personal little model, sister.",

        # BM script5:9725
        "You move closer to Penelope, frantically trying to memorize every square inch of the model’s ethereal body.":
            "You move closer to Penelope, frantically trying to memorize every square inch of your eldest sister’s ethereal body.",

        # BM script5:9747
        "*Giggles* You're crazy, [mc]...":
            "*Giggles* You're crazy, bro...",

        # BM script5:9750
        "You wrap your arms around Penelope's waist, holding her in place with a firm grip before beginning to suck on the blonde's voluptuous breasts.":
            "You wrap your arms around Penelope's waist, holding her in place with a firm grip before beginning to suck on your sister's voluptuous breasts.",

        # BM script5:9751, also overwrites script9:13204 (x)
        # BA/N: could fix (bottom line) but kinda like it lol
        "Damn, [mc]...":
            "Damn, bro...",
            #("Damn, bro...","script5:9751"), #{specific}

        # BM script5:9763
        "Yet here I am, seeing them up close and personal.":
            "Yet here I am, her little brother, seeing them up close and personal.",

        # BM script5:9765
        "She's mine... For at least tonight, Penelope Carter is all mine...":
            "She's mine... For at least tonight, Penelope [lastname] is all mine...",

        # BM script5:9777
        "Not my fault. Your tits are literally making me lose my mind, Penny.":
            "Not my fault. Your tits are literally making me lose my mind, sis.",

        # BM script5:9784
        # BA/N: borrowed from aunt map
        "*Giggles* You're a filthy little degenerate.":
            "*Giggles* You're a filthy little degenerate, aren't you, little brother?",

        # BM script5:9797
        "*Giggles* Jesus, [mc], how long can you keep up an erection like that?":
            "*Giggles* Jesus, bro, how long can you keep up an erection like that?",

        # BM script5:9800
        "I mean... holy fuck, Penny.":
            "I mean... holy fuck, sis.",

        # BM script5:9803
        "Well, I'm not the only one with their “features” pushed to the max here...":
            "Well, I guess it runs in the family, since I'm not the only one with their “features” pushed to the max here... ",

        # BM script5:9823
        "*Giggles* I can imagine. Do you like feeling my big titties wrapped around your cock like this?":
            "*Giggles* I can imagine. Do you like feeling your sister's big titties wrapped around your cock like this?",

        # BM script5:9830
        "My god, Penny, please don't stop...":
            "My god, sis, please don't stop...",

        # BM script5:9849
        "I think it’s time for me to take the lead, Penny...":
            "I think it’s time for me to take the lead, sis...",

        # BM script5:9859
        # BA/N: borrowed from aunt map
        "I'm FUCKING the best tits on Instagram!":
            "I'm FUCKING my sister's tits! The best tits on Instagram!",

        # BM script5:9882
        "Your lips are literally dripping over my cock, Penelope...":
            "Your lips are literally dripping over my cock, Penny...",

        # BM script5:9886
        #"Don’t even think about it, [mc].":
        #    "Don’t even think about it, bro.",

        # BM script5:9887
        "W-We're not gonna f-fuck. I’m not a first date kinda girl, y’know...":
            "W-We're not gonna f-fuck. We... we shouldn't... That'd be going too far...",

        # BM script5:9910
        "Do you like this? Gliding your pussy along my cock?":
            "Do you like this? Gliding your pussy along your little brother's thick cock?",

        # BM script5:9913
        "You want it faster? Tell me, Penny...":
            "You want it faster? Tell me, sis...",

        # BM script5:9927
        "Your hands wrap around Penelope’s soft neck as you hasten your pace, your hips slamming relentlessly against the blonde's buttocks.":
            "Your hands wrap around Penelope’s soft neck as you hasten your pace, your hips slamming relentlessly against your sister's buttocks.",

        # BM script5:9929
        "Ohhh Penny...":
            "Ohhh sis...",

        # BM script5:9933
        "K-Keep up that pace, [mc]...":
            "K-Keep up that pace, bro...",

        # BM script5:9945
        #"You want everyone to treat you like a princess, but deep down you’re a kinky little girl, aren’t you, Penny...?":
        #    "You want everyone to treat you like a princess, but deep down you’re a kinky little girl, aren’t you, sis...?",

        # BM script5:9946
        "Don't think I forgot what you said that day in Warthogs, miss...":
            "Don't think I forgot what you said that day in Warthogs, sister...",

        # BM script5:9952
        "Ohh... f-fuck me, Penny...":
            "Ohh... f-fuck me, sis...",

        # BM script5:9954
        "*Choking* Y-Yeagh... u-use me as your fucking toy, [mc]...":
            "*Choking* Y-Yeagh... u-use me as your fucking toy, bro...",

        # BM script5:9955
        "I wanna make your body writhe in pleasure, Penny...":
            "I wanna make your body writhe in pleasure, sis...",

        # BM script5:9960
        "Y-You’re telling me you haven’t jacked off to me since arriving in Kredon?":
            "Y-You’re telling me you haven’t jacked off to your big sis since arriving in Kredon?",

        # BM script5:9970
        "*Choking* F-Fuck... I'm gonna cum, [mc]...":
            "*Choking* F-Fuck... I'm gonna cum, bro...",

        # BM script5:9972
        "F-Fuck, [mc]... I'm gonna cum...":
            "F-Fuck, bro... I'm gonna cum...",

        # BM script5:10002
        "You're something else, Penny...":
            "You're something else, sis...",

        # BM script5:10010
        "I'm gonna have to ask you to come to all the parties I'm invited to from now on, [mc].":
            "I'm gonna have to ask you to come to all the parties I'm invited to from now on, bro.",

        # BM script5:10019
        "I like the way you think, miss.":
            "I like the way you think, sis.",

        # BM script5:10045
        "*Snorts* You're such a dork. You’re lucky I think you’re cute.":
            "*Snorts* You're such a dork. You’re lucky you’re my cute little brother.",

        # BM script5:10143
        "What are your plans, [mc]?":
            "What are your plans, bro?",

        # BM script5:10258
        "Didn't you tell me you didn't get to go to Kredon's Spring Dance when you were little?":
            "Didn't you tell me you didn't get to go to Kredon's Spring Dance when you were little because you had to take care of us?",

        # BM script5:10274
        "Thanks, [mc]. You're a good friend.":
            "Thanks for being a good influence, [mc].",

        # BM script5:10276
        "Hey, that's what friends are for.":
            "Hey, that's what family is for.",

        # BM script5:10282
        "I had a lot of fun tonight, [mc]. Thank you.":
            "I had a lot of fun tonight, bro. Thank you.",

        # BM script5:10317
        "I'm glad to have you as a friend.":
            "I'm glad you're my brother.",

        # BM script5:10404
        "That's the [mc] I know!":
            "That's my son!",

        # BM script5:10413
        "Thanks for sacrificing your sleep for the mission, [mc].":
            "Thanks for sacrificing your sleep for the mission, honey.",

        # BM script5:10483
        "After all these years, you're still taking care of me like a babysitter, eh Nancy?":
            "After all these years, you're still taking care of me, eh Mom?",

        # BM script5:10487
        "Aww, you're too sweet, [mc]! Of course I’ve gotta take care of you.":
            "Aww, of course, sweetie! No matter how old you get, Mommy will always care for you.",

        # BM script5:10502
        # BA/N: Disabled, getting seen was never part of the plan
        #"Don't worry, it's Sunday, so the office will be empty.":
        #    "Don't worry, it's Sunday, so the office will be empty. If it comes to it, I'll just say I'm showing my son where I work.",

        # BM script5:10565 (menu)
        "Roleplay as Nancy's child":
            "Roleplay as Dalia",

        # BM script5:10568
        "I've been looking forward to seeing where my... mom works, so she invited me to come with her today.":
            "I've been looking forward to seeing where my mom works, so she invited me to come with her today.",

        # BM script5:10599
        "I'm not a girl, and I'm not Nancy's child.":
            "I'm not her daughter, I'm her {i}son{/i}!",

        # BM script5:10687
        "Alright, Nan...":
            "Alright, Mom...",

        # BM script5:10730
        "And you, dear [mc]... are going to retrieve that information.":
            "And you, dear boy... are going to retrieve that information.",

        # BM script5:11331
        "And that's not even taking into account our age difference or my background as your old nanny.":
            "And that's not even taking into account the fact we're mother and son.",

        # BM script5:11374
        "Our age difference, my daughters, the Student Exchange Program, my history as your former nanny...":
            "The Student Exchange Program, your sisters, the fact we're mother and son...",

        # BM script5:11383
        "It’s like we’re fighting against fate or destiny or something like that.":
            "It’s like we’re fighting against fate or destiny, telling us what we’re doing is wrong.",

        # BM script5:11406
        "I'll take what I want.":
            "I'll take what I want. I don't care if it's wrong.",

        # BM script5:11407
        "And what I want... is you, [mc].":
            "And what I want... is you, [mc]. My one and only son.",

        # BM script5:11502
        "*Kneeling down* You know, my mother used to say that risk-takers defy destiny with every decision. I’ve always kept that thought in my head.":
            "*Kneeling down* You know, your grandmother used to say that risk-takers defy destiny with every decision. I’ve always kept that thought in my head.",

        # BM script5:11508
        "What do they feed you boys nowadays?":
            "What do they feed you boys nowadays? You certainly didn't get this from your father...",

        # BM script5:11636
        "S-She's about to fuck me!":
            "M-My mom's about to fuck me!",

        # BM script5:11670
        "Nancy starts moving up and down. Your penis spreads her wet lips apart, while quickly adjusting to the redhead's vicious pace.":
            "Nancy starts moving up and down. Your penis spreads her wet lips apart, while quickly adjusting to your mother's vicious pace.",

        # BM script5:11712
        "Can you handle me going faster, sweetie? I'll start slowly... and it'll make your old babysitter feel so much better...":
            "Can you handle me going faster, sweetie? I'll start slowly... and it'll make your mother feel so much better...",

        # BM script5:11778
        "The poor security guard having to watch the two of us – AGH... FUCK! – h-having sweaty, animal sex in an elevator in the middle of the day...":
            "The poor security guard having to watch the two of us – AGH... FUCK! – h-having sweaty, incestuous sex in an elevator in the middle of the day...",

        # BM script5:11816
        "What a naughty mommy... what if your daughters could see you being fucked like this?":
            "What a naughty mommy... what if my sisters could see their mother and brother fucking like this?",

        # BM script5:11818
        # BA/N: borrowed from aunt map
        "What a naughty empress... what if your subjects could see you being fucked like this?":
            "What a naughty empress... what if your subjects could see you being fucked like this by your own son?",

        # BM script5:11820
        "Do you like being fucked roughly by me?":
            "Do you like being fucked roughly by your son?",

        # BM script5:11857
        # BA/N: borrowed from aunt map
        "Don't worry, my queen, just lean against the wall and let me do the work here...":
            "Don't worry, my queen, just lean against the wall and let your prince do the work here...",

        # BM script5:11907
        # BA/N: borrowed from aunt map
        "[mc] s-s-stop joking!":
            "[mc] s-s-stop joking! I-I can't have a baby w{size=40}AAAHHHHhhh{/size}... {w=1.5}w-with my own s-son!",

        # BM script5:11911
        # BA/N: borrowed from aunt map
        "I can’t upset her, though... not if I want to do this again...":
            "I can’t cross that line, though... not if I want to do this again...",

        # BM script5:11963
        "I can't be fired, [mc], I have a family to feed!":
            "I can't be fired, [mc], I have our family to feed!",

        # BM script5:12104
        "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters would take the news.":
            "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how your sisters would take the news.",

        # BM script5:12405
        "I kept a mask on because I was afraid that it would scare or hurt my daughters.":
            "I kept a mask on because I was afraid that it would scare or hurt Penelope and Dalia.",

        # BM script5:12476
        "Of course not! I swear on my daughters!":
            "Of course not! I swear on my children!",

        # BM script5:12484
        "I have two girls, Dalia and Penelope.":
            "I have two girls and one son, Dalia, Penelope, and [mc] here.",

        # BM script5:12485
        "The younger one will start college next fall, and the older one will graduate in a couple of years.":
            "The younger ones will start college next fall, and the oldest one will graduate in a couple of years.",

        # BM script5:12499
        "I... Whatever you do, you need to hang onto your daughters for as long as you can.":
            "I... Whatever you do, you need to hang onto your kids for as long as you can.",


    # -----------------------------------------
    # v0.6 script6.rpy

        # BM script6:1516
        # Overwritten by BM script:5647, okay
        # "Hey Dalia!" -> "Hey sis!"

        # BM script6:1554 (d)
        "Goddammit, nice job, [mc]!":
            "Goddammit, nice job, bro!",

        # BM script6:1676
        "But well, at least it was nice to see my grandparents and a few friends.":
            "But well, at least it was nice to see our grandparents and a few friends.",

        # BM script6:1701 (p)
        "No worries [mc], there's nothing important to do tonight.":
            "No worries bro, there's nothing important to do tonight.",

        # BM script6:1808
        "*Snorts* Of course you’d say that! I'm afraid I'll have to shower alone today, my insatiable stud.":
            "*Snorts* Of course you'd say that! I'm afraid I'll have to shower alone today, my insatiable son.",

        # BM script6:6770 (a)
        "Don't be nasty!":
            "Don't be nasty! That's your mother!",

        # BM script6:7806 (d)
        "Wow, I love your hair. You look absolutely stunning.":
            "Wow, I love your hair, sis. You look absolutely stunning.",

        # BM script6:8135 (d) {specific}
        # Excludes script3:4717 (p)
        "Thanks [mc]!":[
            ("Thanks bro!","script6:8135"),

            # Bonus Mod
            ("Thanks bro!","script6:8196"),

            # Multi Mod
            ("Thanks bro!","script6:8163"),
        ],

        # BM script6:9319
        # Overwritten by BM script:5647, okay
        # "Hey Dalia!" -> "Hey sis!"

        # BM script6:9323
        "Oh, hi [mc].":
            "Oh, hey bro.",

        # BM script6:9413
        "It's a battle of wits, my friend.":
            "It's a battle of wits, brother.",

        # BM script6:9505
        #"Sorry, Dalia.":
        #    "Sorry, sis.",

        # BM script6:9520
        "Handling the loss like a true sportswoman, Miss Carter.":
            "Handling the loss like a true sportswoman, Miss [lastname].",
            #"Handling the loss like a true sportswoman, sister.",

        # BM script6:9526
        #"I told you, [mc].":
        #    "I told you, bro.",

        # BM script6:9691
        "Good luck, Dalia.":
            "Good luck, Dal.",

        # BM script6:9775
        "Dalia? Did you fall asleep back there?":
            "Daly? Did you fall asleep back there?",

        # BM script6:9895
        "Did you see that, Dalia?":
            "Did you see that, Dal?",

        # BM script6:9899
        "*Pushing you inside* Goddammit [mc], shut up and get the fuck in!":
            "*Pushing you inside* Goddammit bro, shut up and get the fuck in!",

        # ========== START Fuck Marry Kill ==========
            # BA/N: want to change these lines but idk if my replacements really work.

        # BM script6:10076
        "Oh... so I'd be your lover. Nice...":
            "Oh... so I'd be your secret lover. Nice...",

        # BM script6:10078
        "*Laughs* I didn't say that. Don't get your hopes up.":
            "*Laughs* What makes you think I'd fuck my brother more than once?",

        # BM script6:10103, also overwrites script6:10130
        "No way I'm wasting a chance to marry you.":
            "If this is the only time I can marry you, I'm taking it.",

        # BM script6:10104, also overwrites script6:10131
        "And don't worry, unlike Jerry's, our marriage also implies lots of sex.":
            "And don't worry, unlike Jerry's, our marriage is completely open to sex.",

        # ========== END Fuck Marry Kill  ==========

        # BM script6:10376
        "You always leave me speechless...":
            "You always leave me speechless, sis...",

        # BM script6:10451
        "*Taking her shirt off* We know each other pretty well already, [mc].":
            "*Taking her shirt off* We know each other pretty well already, brother.",

        # BM script6:10483
        "(I can't believe I really asked him to go down on me. Alex is such a bad influence, I shouldn't listen to her.)":
            "(I can't believe I really asked my brother to go down on me. Alex is such a bad influence, I shouldn't listen to her.)",

        # BM script6:10535
        "I want you to get carried away so bad, Dalia...":
            "I want you to get carried away so bad, sis...",

        # BM script6:10540
        "We're in a cabin in the middle of nowhere, who cares?":
            "We're in a cabin in the middle of nowhere, who cares? No one else will ever know.",

        # BM script6:10557
        "It's not... weird, right?":
            "It's not... that much weirder, right?",

        # BM script6:10559
        "Is it weird?":
            "Is it too weird? I mean, we're still siblings as it is...",

        # BM script6:10569
        "Fuck, you have no fucking idea of how much you're turning me on right now, Dalia.":
            "Fuck, you have no fucking idea of how much you're turning me on right now, sis.",

        # BM script6:10575
        "Now it's you who's being overly confident, [mc]...":
            "Now it's you who's being overly confident, brother...",

        # BM script6:10598
        "(With [mc].)":
            "(With my brother.)",

        # BM script6:10623
        "You feel your dick head disappear inside of Dalia's mouth, even though you can't actually see it.":
            "You feel your dick head disappear inside of your sister's mouth, even though you can't actually see it.",

        # BM script6:10666
        #"F-FUCK, [mc!u]...":
        #    "F-FUCK, BRO...",

        # BM script6:10667, also overwrites script8:15179
        "Oh, Dalia...":
            "Oh, Dal...",

        # BM script6:10748
        "H-H-Holy fuck, [mc]...":
            "H-H-Holy fuck, bro...",

        # BM script6:10761
        "I swear this booty of yours should be worshipped, Dal.":
            "I swear this booty of yours should be worshipped, sis.",

        # BM script6:10790 (d) {specific}
        # Excludes 7 other lines (x)(no)(l)(a)
        "Oh babe...":[
            ("Oh sis...","script6:10790"),
            ("Oh sis...","script6:10811"),

            # Bonus Mod
            ("Oh sis...","script6:10867"),
            ("Oh sis...","script6:10888"),

            # Multi Mod
            ("Oh sis...","script6:10821"),
            ("Oh sis...","script6:10842"),
        ],

        # BM script6:10797
        #"God, Dalia...":
        #    "God, Dal...",

        # BM script6:10805 (d) {specific}
        # Excludes script6:6438 (a), script6:13016 (x)
        "Not...":[
            ("B-But we're siblings...","script6:10805"),

            # Bonus Mod
            ("B-But we're siblings...","script6:10882"),

            # Multi Mod
            ("B-But we're siblings...","script6:10836"),
        ],

        # BM script6:10806
        "N-Not now. Not here...":
            "W-We can't.. Not now. N-Not here...",

        # BM script6:10807
        "Does that mean... that you want me to fuck you another day...?":
            "Does that mean... you'd be okay if we fuck another time...?",

        # BM script6:10809
        "M-Maybe in... another s-situation.":
            "I d-don't know... m-maybe...",

        # BM script6:10811
        # Overwritten by BM script6:10790, okay
        # "Oh babe..." -> "Oh sis..."

        # BM script6:10842
        "Just like her sis... interesting.":
            "Just like big sis... interesting.",

        # BM script6:10848
        "Fuck, this feels so good, Dalia...":
            "Fuck, this feels so good, sis...",

        # BM script6:10885
        "(Do I really want [mc] to... fuck me?)":
            "(Do I really want my brother to... fuck me?)",

        # BM script6:10887
        "(He's... the one...)":
            "(He's... the one... even if we're...)",

        # BM script6:10976
        "I'm g-gonna cum, Dalia...":
            "I'm g-gonna cum, Dal...",

        # BM script6:10982
        "Fuck, Dalia, you're not gonna leave me hanging now, right...?":
            "Fuck, sis, you're not gonna leave me hanging now, right...?",

        # BM script6:11018
        "Oh Lord, Dalia...":
            "Oh Lord, Daly...",

        # BM script6:11047
        "*Giggles* You're a terrible liar, [mc].":
            "*Giggles* You're a terrible liar, bro.",

        # BM script6:11073
        "Take it all, babe...":
            "Take it all, sis...",

        # BM script6:11396 {specific}
        # Excludes script6:12044 (x)
        "See you later, [mc].":[
            ("See you later, bro.","script6:11396"),

            # Bonus Mod
            ("See you later, bro.","script6:11493"),

            # Multi Mod
            ("See you later, bro.","script6:11427"),
        ],

        # BM script6:11398
        "Goodbye, Dalia.":
            "Goodbye, sis.",

        # BM script6:14151
        "Although... not as much as when you went to Wyatt's house with Nancy Carter, that's for sure.":
            "Although... not as much as when you went to Wyatt's house with your mother, Nancy [lastname], that's for sure.",

        # BM script6:14214
        "H-Hey Dalia!":
            "H-Hey Dal!",

        # BM script6:14300 (d) {specific}, also overwrites script9:14153 (d), okay
        # Excludes script:5378 (n)
        "Thank you, [mc]!":[
            ("Thanks, bro!","script6:14300"),
            ("Thanks, bro!","script9:14153"),

            # Bonus Mod
            ("Thanks, bro!","script6:14425"),
            ("Thanks, bro!","script9:14292"),

            # Multi Mod
            ("Thanks, bro!","script6:14331"),
            ("Thanks, bro!","script9:14167"),
        ],


    # -----------------------------------------
    # v0.7 script7.rpy

        # BM script7:19
        "I know you've been fooling around with the WRE with your peculiar group of... {i}friends.":
            "I know you've been fooling around with the WRE with your peculiar group of... {i}friends{/i} and {i}family{/i}.",

        # BM script7:422 (d)
        "*Snorts* Don't worry, I'm kidding, I'm kidding!":
            "*Snorts* Don't worry, I'm kidding, I'm kidding! He {i}is{/i} your brother, after all.",

        # BM script7:727 (n)
        "About anything.":
            "About {i}anything{/i}.",

        # BM script7:905
        "Penelope Carter plays Eternum!":
            "Penelope [lastname] plays Eternum!",

        # BM script7:1031 (no)
        "*Hyperventilating* I left my drawing utensils at the Carter house last time I was there!":
            "*Hyperventilating* I left my drawing utensils at the [lastname] house last time I was there!",

        # BM script7:2489
        "You raise your gaze from Penelope's chest to meet her eyes, finding her staring at you in a bemused manner.":
            "You raise your gaze from your sister's chest to meet her eyes, finding her staring at you in a bemused manner.",

        # BM script7:2931 (menu)
        "She's not my wife":
            "She's my sister",

        # BM script7:2932
        "Uhh... well, she's not my wife, but... alright, let's do it.":
            "Uhh... well, she's actually my sister, but... alright, let's do it.",

        # BM script7:2936 (menu)
        # l9/N: Changed to be fully compatible with and without either walkthrough
        # BA/N: Disabled, reverted back to original text upon suggestion
        # "She's not my wife, yet":
        #     "{color=[walk_points]}She's my sister... [penelope_pts]",

        # BM script7:2937
        # BA/N: Disabled, upon suggestion
        # "Well, she's not my wife {i}yet{/i}, but... alright, let's do it.":
        #     "Well, she's my sister and not my wife {i}yet{/i}, but... alright, let's do it.",

        # BM script7:4111 (d)
        "Nice job, [mc].":
            "Nice job, bro.",

        # BM script7:4186
        "Come on, Dalia!":
            "Come on, sis!",

        # BM script7:4702 (p) {specific}
        # Excludes script7:4670 (l)
        "Be careful.":[
            ("Be careful, little brother.","script7:4702"),

            # Bonus Mod
            ("Be careful, little brother.","script7:4732"),

            # Multi Mod
            ("Be careful, little brother.","script7:4718"),
        ],

        # ========== START harem thoughts ==========

        # BM script7:7396 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7396",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7452",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7454",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # BM script7:7398 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7398",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7454",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7456",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # BM script7:7400 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7400",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7456",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7458",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # BM script7:7402 {inject}
        # no change here, leaving for copy-paste purposes
        #"Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.":[
        #    ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7402",[
        #        'mct "no change"',
        #    ]),
        #
        #    # Bonus Mod script7:7458
        #
        #    # Multi Mod script7:7460
        #],

        # BM script7:7404 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7404",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7460",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7462",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # BM script7:7425 {inject}
        # BA/N: technically this wouldn't work if you're not on any of the incest routes but don't feel like making a labelmod to add if statement just for this
        #    but also why would you be playing an incest mod without following at least one incest path right?
        "I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?":[
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7425",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),

            # Bonus Mod
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7481",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),

            # Multi Mod
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7483",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),
        ],

        # ========== END harem thoughts ==========

        # BM script7:7739
        "You look incredible, Penny.":
            "You look incredible, sis.",

        # BM script7:7766
        "I've come to recognize that horndog expression by now, [mc].":
            "I've come to recognize that horndog expression by now, little bro.",

        # BM script7:7863
        "(You know that all this teasing with him isn't right.)":
            "(You know that all this teasing with your brother isn't right.)",

        # BM script7:7963
        "I mean... of course I like him, but not in that way, you know?":
            "I mean... of course I like him, he's my little brother, but not in {i}that{/i} way, you know?",

        # BM script7:8017
        "Penelope Carter is my bestie.":
            "Penelope [lastname] is my bestie.",

        # BM script7:8137
        "What are you talking about, he's not my step-anything.":
            "What are you talking about? He's not my step-brother, he's my actual brother.",

        # BM script7:8139
        "Well, I know, but didn't you practically grow up around him?":
            "Wait, really? I thought he only stayed with you for a little while.",

        # BM script7:8140
        "You even mentioned babysitting him when your mom had to work.":
            "And didn't you mention babysitting him when your mom had to work?",

        # BM script7:8142
        "That literally only happened once, and... yeah, so what?":
            "Isn't that a normal thing to do as a big sister?",

        # BM script7:8143
        "That was ages ago.":
            "And besides, that was ages ago.",

        # BM script7:8195
        "(But the trouble it'd cause...)":
            "(But in the end we’re still siblings. It’d cause so much trouble...)",

        # BM script7:8202
        "(You can't be fixated on [mc] like some teenage crush, Penny. There's plenty more fish in the sea!)":
            "(You can’t be fixated on your own younger brother like some teenage crush, Penny. There’s plenty more fish in the sea!)",

        # BM script7:8256
        "(We're just two friends goofing around.)":
            "(We're just two siblings goofing around.)",

        # BM script7:8338
        "{sc=2}PENELOPE{w=.5} P. {w=.5}CARTER.{/sc}":
            "{sc=2}PENELOPE{w=.5} P. {w=.5}[lastname!u].{/sc}",

        # BM script7:8378
        "Ohh... you brought your photographer friend!":
            "Ohh... you brought your brother again!",

        # BM script7:8454
        "I'm [mc] [lastname] – Penelope Carter's representative.":
            "I'm [mc] [lastname] – Penelope [lastname]'s representative.",

        # BM script7:8736
        "P-Penelope Paige Carter.":
            "P-Penelope Paige [lastname].",

        # BM script7:8840
        "Penelope Paige Carter.":
            "Penelope Paige [lastname].",

        # BM script7:9257
        "I'm glad I have a friend who I trust and with whom I can do these kinds of things, [mc].":
            "I'm glad I have someone who I trust and with whom I can do these kinds of things, [mc].",

        # BM script7:9319
        "*Sitting on the car* Are you okay? Your mind seems to be elsewhere, [mc].":
            "*Sitting on the car* Are you okay, bro? Your mind seems to be elsewhere.",

        # BM script7:9372
        # Overwritten by BM script9:12109, okay?
        # "Oh, Penny..." -> "Oh, sis..."

        # BM script7:9384 {inject}
        "I tried to stop... but I couldn't.":[
            ("We're siblings. We can’t be doing these things.","script7:9384",[
                'p "So I tried to stop... but I couldn’t."'
            ]),

            # Bonus Mod
            ("We're siblings. We can’t be doing these things.","script7:9448",[
                'p "So I tried to stop... but I couldn’t."'
            ]),

            # Multi Mod
            ("We're siblings. We can’t be doing these things.","script7:9442",[
                'p "So I tried to stop... but I couldn’t."'
            ]),
        ],

        # BM script7:9386
        "That I would stop thinking about you 24/7.":
            "That I would stop thinking about you like this 24/7... thinking these thoughts about my own little brother.",

        # BM script7:9389
        "*Biting her lip* F-FUCK, this isn't working, [mc]." :
            "*Biting her lip* F-FUCK, bro, this isn't working." ,

        # BM script7:9439
        "And we could go back to being our regular selves.":
            "And we could go back to being our regular selves. Being regular brother and sister.",

        # BM script7:9469
        "S-Shit... this is crazy, [mc].":
            "S-Shit... this is crazy, bro.",

        # BM script7:9470 {inject}
        "We're crazy.":[
            ("We're both crazy.","script7:9470",[
                'mc "*Chuckles* We share the same blood after all..."',
            ]),

            # Bonus Mod
            ("We're both crazy.","script7:9534",[
                'mc "*Chuckles* We share the same blood after all..."',
            ]),

            # Multi Mod
            ("We're both crazy.","script7:9528",[
                'mc "*Chuckles* We share the same blood after all..."',
            ]),
        ],

        # BM script7:9491
        "Holy fuck, [mc], that feels...":
            "Holy fuck, bro, that feels...",

        # BM script7:9497
        "Ooh PENNY....":
            "Ooh SIS....",

        # BM script7:9502
        "I'm having sex with her. I'm fucking Penelope Carter.":
            "I'm having sex with her. I'm fucking my big sister.",

        # BM script7:9505
        "*Moaning* Aaaghhh, [mc]...":
            "*Moaning* Aaaghhh, bro...",

        # BM script7:9507
        "*Giggles* Oh y-yeah? You thought about this...? Thought about fucking little old me?":
            "*Giggles* Oh y-yeah? You thought about this...? Thought about fucking your big sister?",

        # BM script7:9518
        "Jesus Christ, that feels good, Penny...":
            "Jesus Christ, that feels good, sis...",

        # BM script7:9526
        "*Groaning* F-Fuck, you're so fucking big, [mc]...":
            "*Groaning* F-Fuck, you're so fucking big, bro...",

        # BM script7:9532
        "Try it for me, baby girl...":
            "Try it for me, sis...",

        # BM script7:9548
        "O-Oh Penny...":
            "O-Oh sis...",

        # BM script7:9555
        "You're asking for a lot there, Penny...":
            "You're asking for a lot there, sister...",

        # BM script7:9568
        "O-Oh my god, [mc], you're stretching me out so much...":
            "O-Oh my god, bro, you're stretching me out so much...",

        # BM script7:9569
        "Y-You're taking it like a pro, Penny...":
            "Y-You're taking it like a pro, sis...",

        # BM script7:9578
        "*Panting* F-Fuck, I'm getting tired, [mc]...":
            "*Panting* F-Fuck, I'm getting tired, bro...",

        # BM script7:9596
        "Fuck me hard, [mc]...":
            "Fuck me hard, bro...",

        # BM script7:9600
        "*Panting* I-I'm gonna cum so hard, [mc]...":
            "*Panting* I-I'm gonna cum so hard, bro...",

        # BM script7:9674
        "C’mon... you were talking such a big game earlier, [mc]...":
            "C’mon... you were talking such a big game earlier, little brother...",

        # BM script7:9689
        "*Panting* I just can't stop, Penny...":
            "*Panting* I just can't stop, sis...",

        # BM script7:9694
        #"{sc=2}SWEET LORD, [mc!u]...{/sc}":
        #    "{sc=2}SWEET LORD, BROTHER...{/sc}",

        # BM script7:9719
        "O-Oh my god, Penny...":
            "O-Oh my god, sis...",

        # BM script7:9757
        "AAAAAAARGHHH, fuck, PENNY...":
            "AAAAAAARGHHH, fuck, SIS...",

        # BM script7:9773
        "*Panting* Fuck, [mc]... don't you ever run out of stamina?":
            "*Panting* Fuck, bro... don't you ever run out of stamina?",

        # BM script7:9794
        "Your tits are the fucking best I've ever seen in my life, Penny, but goddamn, this butt of yours deserves some attention too...":
            "Your tits are the fucking best I've ever seen in my life, sis, but goddamn, this butt of yours deserves some attention too...",

        # BM script7:9803
        "*Panting* Oh dear Lord, y-your pussy is so fucking tight, Penny...":
            "*Panting* Oh dear Lord, y-your pussy is so fucking tight, sis...",

        # BM script7:9826
        "Crush me against this car, [mc]...":
            "Crush me against this car, bro...",

        # BM script7:9828
        "Oh yeah, Penny...":
            "Oh yeah, sis...",

        # BM script7:9870
        "I-I'm at my limit, Penny...":
            "I-I'm at my limit, sis...",

        # BM script7:9889
        # BA/N: Disabled for seriousness
        #"*Whispering* S-Shit, Penny, keep it down! We need to leave!":
        #    "*Whispering* S-Shit, sis, keep it down! We need to leave!",

        # BM script7:9898
        # BA/N: Disabled for seriousness
        #"G-G-Ggggghhhh... P-Pennyyy s-stay quieeeeet...":
        #    "G-G-Ggggghhhh... S-Siiiiiiissssss s-stay quieeeeet...",

        # BM script7:9986
        "You can feel how Penelope orgasms again at the same time as you finish unloading an insane amount of jizz deep inside her warm vagina.":
            "You can feel how Penelope orgasms again at the same time as you finish unloading an insane amount of jizz deep inside your sister's warm vagina.",

        # BM script7:9987
        "*Whispering* Oh, Penny...":
            "*Whispering* Oh, sis...",

        # BM script7:10027
        #"*Panting* Oh god, Penny...":
        #    "*Panting* Oh god, sis...",

        # BM script7:10283 chat:917 and chat:918 (p)->(d)
        "I'm proud of my hot sissy":
            "I'm proud of our hot sissy",

        # BM script7:10311
        "*Turning around* Ah, good morning Na-":
            "*Turning around* Ah, good morning Mo-",

        # BM script7:10314
        "*Gulps* N-Nancy.":
            "*Gulps* M-Mom.",

        # BM script7:10371
        #"Yeah, we're all {i}really{/i} lucky to have you as our friend.":
        #    "Yeah, they're all {i}really{/i} lucky to have you as their friend.",

        # BM script7:10409
        "I can see where Penny inherited her love for teasing me.":
            "I can see where Penny and I got our love for teasing.",

        # BM script7:10483
        "And join Nancy on The New World server.":
            "And join my mom on The New World server.",

        # BM script7:10726
        "Sooo... should we log in now? Nancy must be waiting for us already.":
            "Sooo... should we log in now? My mom must be waiting for us already.",


    # -----------------------------------------
    # v0.8 script8.rpy

        # BM script8:662
        "I was trying to focus on Nancy's house, but I still appeared on the same exact spot where I left. Maybe I need more practice?":
            "I was trying to focus on my house, but I still appeared on the same exact spot where I left. Maybe I need more practice?",

        # BM script8:794
        "Turns out... I decided to pick up a couple of pizzas for Nancy and me.":
            "Turns out... I decided to pick up a couple of pizzas for my mom and me.",

        # BM script8:2058
        "NANCY!":
            "MOM!",

        # ========== START Stanley Parable ==========
            # Some of these lines have voiceovers that we can't change
            # just have to deal with it 
            # voiceover lines marked with {VO}

        # BM script8:3103 {VO}
        #   nvm, this one isn't necessary
        #"{cps=15}Ten long years had passed since he and his friends gathered the ten Gems of Doom... yet, the sense of powerlessness that had overtaken him since then still lingered.":
        #    "{cps=15}Ten long years had passed since he, his friends, and his family gathered the ten Gems of Doom... yet, the sense of powerlessness that had overtaken him since then still lingered.",

        # BM script8:3455 (p)
        # Overwritten by BM script:2452 (d), okay
        # "Hey [mc]!" -> "Hey bro!"

        # BM script8:3458
        "{i}Listen, I was just calling to see if you've heard anything about my mom. I haven't heard from her in a few months.":
            "{i}Listen, I was just calling to see if you've heard anything about Mom. I haven't heard from her in a few months.",

        # BM script8:3460
        "What...? There's no power in this world strong enough to stop Nancy from talking to her daughters.":
            "What...? There's no power in this world strong enough to stop Mom from talking to her kids.",

        # BM script8:3470
        "Was that Penelope Carter?!":
            "Was that your sister, Penelope [lastname]?!",

        # BM script8:3787
        "The one and only... PENELOPE CARTER!":
            "The one and only... PENELOPE [lastname!u]!",

        # BM script8:3911
        "Dalia?! Is that you?!":
            "Daly?! Is that you?!",

        # BM script8:3981 {VO}
        "{cps=16}However...{cps=1.5} {cps=16}the call from Dalia Carter sparked a glimmer of hope within him, so he decided to head to the coffee area and wait for her.{cps=1} {cps=16}This...{cps=1.4} {cps=16}was his chance.":
            "{cps=16}However...{cps=1.5} {cps=16}the call from Dalia [lastname] sparked a glimmer of hope within him, so he decided to head to the coffee area and wait for her.{cps=1} {cps=16}This...{cps=1.4} {cps=16}was his chance.",

        # BM script8:4058 (d)
        "Remember when we were foolin' around in Kredon...?":
            "Remember when we were foolin’ around in Kredon? Doin’ things no brother and s-sister should be doin’...?",

        # BM script8:4071 (d)
        "Fuck me, [mc]...":
            "Fuck me, brother...",

        # BM script8:4087 {VO}
        "{cps=17}Our hero was unable to resist the sight of his old friend's ample bosom and alluring figure.{cps=0.6} {cps=16}Overwhelmed by desire, he accepted her offer and surrendered himself to her embrace.":
            "{cps=17}Our hero was unable to resist the sight of his sister's ample bosom and alluring figure.{cps=0.6} {cps=16}Overwhelmed by desire, he accepted her offer and surrendered himself to her embrace.",

        # ========== END Stanley Parable ==========

        # BM script8:4719
        "Ah, a very smart choice, [mc]... always making the most of every situation. I expected no less!":
            "Ah, a very smart choice, my boy... always making the most of every situation. I expected no less from my son!",
        
        # BM script8:4885 {inject}
        "And how about you, Nancy? Have you ever caught Dalia or Penny... you know, giving in to their impulses?":[
            ("And how about you, Mom? Have you ever caught Dalia or Penny... you know, giving in to their impulses? ","script8:4885",[
                'mc "Oh, and the one time you burst into MY room doesn’t count, I was just getting dressed!"'
            ]),

            # Bonus Mod
            ("And how about you, Mom? Have you ever caught Dalia or Penny... you know, giving in to their impulses? ","script8:4967",[
                'mc "Oh, and the one time you burst into MY room doesn’t count, I was just getting dressed!"'
            ]),

            # Multi Mod
            ("And how about you, Mom? Have you ever caught Dalia or Penny... you know, giving in to their impulses? ","script8:4913",[
                'mc "Oh, and the one time you burst into MY room doesn’t count, I was just getting dressed!"'
            ]),
        ],

        # BM script8:5016
        "And honestly, I had some reservations at first, but now I don't regret it one bit.":
            "And honestly, I had a lot of reservations at first, but now I don't regret it one bit.",

        # BM script8:5018
        "N-Nancy...?":
            "M-Mom...?",
        
        # BM script8:5025
        "WHEN?":
            "B-{w=0.2}but... {sc=3}{w=0.8}{size=40}AREN'T YOU{sc=5}{w=0.5}{size=50}{i}HIS {b}MOM?!",

        # BM script8:5027
        "A few weeks ago.":
            "Indeed. It was something we both desired.",

        # BM script8:5031
        "Holy shit, I-I really didn't expect that.":
            "Holy shit, that-that's {i}insane{/i}. I-I really didn't expect that.",

        # BM script8:5033
        "*Giggles* Don't worry, I won't get in your way.":
            "*Giggles* Does it bother you? And don't worry, I won't get in your way.",

        # BM script8:5211
        "I think I should keep my distance from Nancy, [mc].":
            "I think I should keep my distance from your mother, [mc].",

        # BM script8:5527
        "*Pulling Nancy towards you* Hmph...":
            "*Pulling your mother towards you* Hmph...",

        # BM script8:5558
        "How are you still tight after giving birth to two children...?":
            "How are you still tight after giving birth to three children...?",

        # BM script8:5692
        "My balls are about to explode, but... I still think we can give Nancy one last ride.":
            "My balls are about to explode, but... I still think we can give my mom one last ride.",

        # BM script8:5695
        "Come here, Nan...":
            "Come here, Mom...",

        # BM script8:5709
        "This is completely surreal. I'm fucking two stunning red-haired goddesses at the same time.":
            "This is completely surreal. I'm fucking two stunning red-haired goddesses at the same time. And one of them's my mother!",

        # BM script8:5803
        # exact line used for both Nancy and Nova so can't change without labelmod
        #"*Cumming* Y-Yeeah, take it all, babe...":
        #    "*Cumming* Y-Yeeah, take it all, Mom...",

        # BM script8:6983 (l)
        # BA/N: leaving this here for the future when we learn what exactly Luna's vision was
        # "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)":
        #     "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)",

        # BM script8:8077
        "Oh... well, I didn't buy mine either. Nancy did.":
            "Oh... well, I didn't buy mine either. My mom did.",

        # BM script8:8078
        "My... nanny. She got it for my birthday.":
            "She got it for my birthday.",

        # BM script8:10132
        "Where'd you find yourself a man like that?":
            "I need to find myself a man like that.",

        # BM script8:10141 {inject}
        "*Chuckles* Seems reasonable to me.":[
            ("*Chuckles* Seems reasonable to me.","script8:10141",[
                'd "Do you... want to try asking him out?"',
                'mil "Nah, I prefer dating people I don’t know from work."',
                'mil "And it feels like he’s got someone on his mind lately."'
            ]),

            # Bonus Mod
            ("*Chuckles* Seems reasonable to me.","script8:10282",[
                'd "Do you... want to try asking him out?"',
                'mil "Nah, I prefer dating people I don’t know from work."',
                'mil "And it feels like he’s got someone on his mind lately."'
            ]),

            # Multi Mod
            ("*Chuckles* Seems reasonable to me.","script8:10170",[
                'd "Do you... want to try asking him out?"',
                'mil "Nah, I prefer dating people I don’t know from work."',
                'mil "And it feels like he’s got someone on his mind lately."'
            ]),
        ],

        # BM script8:10167
        "Hey, Dalia, I'm done over here!":
            "Hey, Dal, I'm done over here!",

        # BM script8:10356, also overwrites script8:10397, script8:10420
        "It's just some silly gift for... a very special girl." :
            "It's just some silly gift for... my very special sister.",

        # BM script8:10353
        "Thank you so much, [mc]. You're the best.":
            "Thank you so much, bro. You're the best.",

        # BM script8:10393 {specific}
        # Excludes script8:10416 (d) and script9:19240 (l)
        "Thank you so much, [mc].":[
            ("Thank you so much, bro.","script8:10393"),

            # Bonus Mod
            ("Thank you so much, bro.","script8:10534"),

            # Multi Mod
            ("Thank you so much, bro.","script8:10422"),
        ],

        # BM script8:10609 (x)
        "You know Nancy's offer still stands, right?":
            "You know my mom's offer still stands, right?",

        # BM script8:11966
        "Your abs are looking good, Dalia.":
            "Your abs are looking good, Daly.",

        # BM script8:12123
        "I... usually just eat whatever Nancy cooks.":
            "I... usually just eat whatever my mom cooks.",

        # BM script8:12254
        "*Giggles* You get carried away too easily, [mc].":
            "*Giggles* You get carried away too easily, brother.",

        # BM script8:12261
        "In the end I’m gonna start thinking you’re actually into me, Dalia...":
            "In the end I’m gonna start thinking you’re actually into me, sister...",

        # BM script8:12308
        # BA/N: Added bc relation was never mentioned around Jerry, if I missed it than need to redo this line
        "That's... a little embarrassing.":
            "That's... a little embarrassing. Shit, does Jerry know we're related?",

        # BM script8:12363
        "Damn... that took a sad turn all of a sudden.":
            "It doesn't seem like he’s figured out that Dalia and I are related at least, but damn... that took a sad turn all of a sudden.",

        # BM script8:12858
        "My dad left before I was even born, you fucking idiot.":
            "My dad left when I was a kid, you fucking idiot.",

        # BM script8:13437
        "You think Nancy wants to play the role of some sort of intermediary? Because she wants it too?":
            "You think this... {i}Mom{/i} wants to play the role of some sort of intermediary? Because she wants it too?",

        # BM script8:13458
        "But anyway, thank you for listening, I guess.":
            "But anyway, thank you for listening, I guess. And please keep this conversation private!",

        # BM script8:14697
        "Hey, hey... what's wrong, Dal? Are you okay?":
            "Hey, hey... what's wrong, sis? Are you okay?",

        # BM script8:14906
        "Thank you for... humoring me with my ramblings, [mc].":
            "Thank you for... humoring me with my ramblings, bro.",

        # BM script8:14910
        "I also love spending time with you, Dalia.":
            "I also love spending time with you, sis.",

        # BM script8:14913
        # BA/N: Disabled for seriousness
        #"Do you like me, [mc]?":
        #    "Do you like me, bro?",

        # BM script8:14926
        "Are you okay, Dalia...?":
            "Are you okay, Dal...?",

        # BM script8:14956
        "I mean, like me like... “ah, yeah, she's hot. I like her... butt”?":
            "I mean, like me like... “of course, she's my sister”?",

        # BM script8:14957
        "Or like me, like...":
            "Or like me, like... “ah, yeah, she's hot–”",

        # BM script8:14971
        "You mean... love me... like a good friend? Or like a sister?":
            "You mean... love me... as your sister?",

        # BM script8:15007
        "Yeah, you're smoking hot, but no, I didn't come looking for you because of your “butt”.":
            "Yeah, you're smoking hot, but no, I didn't come looking for you because of your “butt”. It doesn't matter that you're my sister.",

        # BM script8:15137
        "I know you love it, Dalia, you can't fool me...":
            "I know you love it, sis, you can't fool me...",

        # BM script8:15138
        "Me? You've been watching too much porn, [mc].":
            "Me? You've been watching too much porn, bro.",

        # BM script8:15149
        "How is a cute little kiss not enough? You're getting so greedy, [mc]...":
            "How is a cute little kiss not enough? You're getting so greedy, brother...",

        # BM script8:15179
        # Overwritten by BM script6:10667, okay
        # "Oh, Dalia..." -> "Oh, Dal..."

        # BM script8:15193
        "Fuck yes, babe...":
            "Fuck yes, sis...",

        # BM script8:15236
        #"O-Oohhh baby, yeah...":
        #    "O-Oohhh sis, yeah...",

        # BM script8:15245
        "Aghh... you're the best, Dalia...":
            "Aghh... you're the best, sis...",

        # BM script8:15314
        "*Panting* O-OOH D-D-DALIA, HANG IN RIGHT THERE...":
            "*Panting* O-OOH D-D-DALY, HANG IN RIGHT THERE...",

        # BM script8:15357
        "You're a horny dog, [mc]. Don't you ever run out of fuel?":
            "You're a horny dog, bro. Don't you ever run out of fuel?",

        # BM script8:15374
        "You're underestimating the amount of “energy” you just unloaded a minute ago, [mc].":
            "You're underestimating the amount of “energy” you just unloaded a minute ago, brother.",

        # BM script8:15410
        "As you expected, just the sight of Dalia baring herself before you and the thoughts of what you'd do to her make you hard again in an instant.":
            "As you expected, just the sight of your sister baring herself before you and the thoughts of what you'd do to her make you hard again in an instant.",

        # BM script8:15435
        "*Whispers* Do you want to {i}fuck{/i} me, [mc]...?":
            "*Whispers* Do you want to {i}fuck{/i} me, [mc]...? Do you want to fuck your sister...?",

        # BM script8:15436
        "My god, Dalia, I do...":
            "My god, sis, I do...",

        # BM script8:15467
        "OH, BABE, YES...":
            "OH, DALIA, YES...",

        # BM script8:15506
        "O-Oh Dalia, I've been waiting for this forever...":
            "O-Oh sis, I've been waiting for this forever...",

        # BM script8:15521
        "Agghhh... oh [mc]...":
            "Agghhh... oh bro...",

        # BM script8:15525
        "You have no idea how good your pussy is making me feel right now, Dalia...":
            "You have no idea how good your pussy is making me feel right now, sis...",

        # BM script8:15527
        "*Moans* AAAAAhhh... [mc]...":
            "*Moans* AAAAAhhh... bro...",

        # BM script8:15551
        #"[mc], I'm gonna cum...":
        #    "Brother, I'm gonna cum...",

        # BM script8:15555
        "[mc], I'm cumming...":
            "Bro, I'm cumming...",

        # BM script8:15558
        "You d-don't have to hold back, Dalia.":
            "You d-don't have to hold back, sis.",

        # BM script8:15590
        "*Panting* I-I want you to make me cum again, [mc]...":
            "*Panting* I-I want you to make me cum again, bro...",

        # BM script8:15604
        "*Moans* I-I want you to be the only one t-to ever have me, [mc]...":
            "*Moans* I-I want you to be the only one t-to ever have me, bro...",

        # BM script8:15663
        "O-Ohh, fuck, Dalia...":
            "O-Ohh, fuck, sis...",

        # BM script8:15671
        "*Panting* That the childhood friend I used to p-play with would end up ramming her p-perfect, huge ass down on my cock...":
            "*Panting* That my sister would end up ramming her p-perfect, huge ass down on my cock...",

        # BM script8:15673
        "*Giggling breathlessly* That the idiot who m-moved back in with us w-would...":
            "*Giggling breathlessly* That my idiot brother who m-moved back in with us w-would...",

        # BM script8:15675
        "Oh fuck, I'm cumming again, [mc]...":
            "Oh fuck, I'm cumming again, bro...",

        # BM script8:15694
        "Fuck, we can't stop now, Dal...":
            "Fuck, we can't stop now, sis...",

        # BM script8:15711
        "*Panting* Oh sweet L-Lord, [mc]...":
            "*Panting* Oh sweet L-Lord, bro...",

        # BM script8:15765
        "F-F-FUCK ME, [mc]...":
            "F-F-FUCK ME, BRO...",

        # BM script8:15767
        "*Panting* Oh, babe...":
            "*Panting* Oh, sis...",

        # BM script8:15768
        "*Panting* Y-Your pussy's pure fucking magic, Dalia...":
            "*Panting* Y-Your pussy's pure fucking magic, Dal...",

        # BM script8:15834
        "You sound exhausted, Dalia.":
            "You sound exhausted, sis.",

        # BM script8:15862
        "Well, I don't know, then I just thank my mom for making me the way I am.":
            "Well, I don't know, then I just thank Mom for making me the way I am.",

        # BM script8:16065 {inject}
        "T-That was awkward.":[
            ("T-That was awkward.","script8:16065",[
                "show gd 146",
                'd "Does... Does Jerry remember we’re siblings?" with dis',
                "show gd 145",
                'mc "When I talked to him earlier, it didn’t seem like he knew."',
                'mc "We should probably be more careful around him though. I’ll order him to keep this a secret."',
                "show gd 152",
                'd "O-Okay. So we should be safe for now." with dis06',
            ]),

            # Bonus Mod
            ("T-That was awkward.","script8:16242",[
                "show gd 146",
                'd "Does... Does Jerry remember we’re siblings?" with dis',
                "show gd 145",
                'mc "When I talked to him earlier, it didn’t seem like he knew."',
                'mc "We should probably be more careful around him though. I’ll order him to keep this a secret."',
                "show gd 152",
                'd "O-Okay. So we should be safe for now." with dis06',
            ]),

            # Multi Mod
            ("T-That was awkward.","script8:16098",[
                "show gd 146",
                'd "Does... Does Jerry remember we’re siblings?" with dis',
                "show gd 145",
                'mc "When I talked to him earlier, it didn’t seem like he knew."',
                'mc "We should probably be more careful around him though. I’ll order him to keep this a secret."',
                "show gd 152",
                'd "O-Okay. So we should be safe for now." with dis06',
            ]),
        ],

        # BM script8:16303 (x)
        "(Hmm, yeah.)":
            "(Imagine her face if I tell her it was with my brother.)",

        # BM script8:16306 (p)
        "(Or maybe Sissy too...?)":
            "(Sissy would freak out if she found out...)",


    # -----------------------------------------
    # v0.9 script9.rpy Lines

        # BM script9:267 (p)
        "OH! Is it...":
            "Hmmm, how many other boys do you know...",

        # BM script9:268 (p)
        "*Giggles* Is it [mc]...?":
            "*Giggles* Can't be [mc]...",

        # BM script9:270 (d)
        "I-I don't...":
            "What!? Of-f course not... I-I mean...{w} {size=*0.75}he's my–{/size}{w} {size=*0.6}he's our...{/size}",

        # BM script9:287 (p)
        "YOU'RE IN LOVE WITH [mc!u]?!":
            "YOU'RE IN LOVE WITH OUR BROTHER?!",

        # BM script9:296 (p)
        "I literally asked you a couple of weeks ago and you said “you’d rather live off salads for a year”!":
            "He's our little brother! Our actual, {i}blood-related brother!{/i}",

        # BM script9:298 (d)
        "Oh... well, yeah...":
            "You think I'm not aware of that?",

        # BM script9:299 (d)
        "A-About that...":
            "It's just, ever since [mc] came back, everything's been so... different.",

        # BM script9:300 (d)
        "I was... confused.":
            "Better really. Every time I'm with him, I'm just so happy and... confused.",

        # BM script9:304 (d)
        "Yes, confused.":
            "Of course I’m confused! I know it’s wrong to feel this way!",

        # BM script9:311 (p)
        "What?! Hah! Me?! Pfft!":
            "What?! Hah! Me?! With our {i}brother?{/i} Pfft!",

        # BM script9:316 (p)
        "W-We've all been hovering around him lately.":
            "N-Not any more than the other girls do... I'm just doting on him as a big sister!",

        # BM script9:319 (d)
        "But certain blondes have been a little more... hover-y, I think.":
            "You've been quite clingy for a \"big sister\"...",

        # BM script9:383 (d)
        "You just can't let me have anything, can you?!":
            "You just can't let me have anything, can you?! Not even my own brother!",

        # BM script9:388 (d)
        "But I didn't fucking know??!":
            "And you had the nerve to judge {i}me{/i} for liking my brother?!",
            #"And you had the nerve to judge {i}me{/i} about incest?!",

        # BM script9:390 (p)
        "Oh, but I was supposed to know about you two??":
            "What, was I supposed to pretend that {i}incest{/i} is all normal?",
            #"What, was I supposed to pretend this {i}incest{/i} is all normal? You know it's not!",

        # BM script9:392 (d)
        "You're so damn... selfish!":
            "You're such a... selfish hypocrite!",

        # BM script9:436 (p)
        "*Grumbling to herself* My goddamn sister?!":
            "*Grumbling to herself* His other goddamn sister, too?!",

        # BM script9:439 (d)
        "*Grumbling to herself* Why didn't she tell me?!":
            "*Grumbling to herself* I thought we trusted each other more than this... Like... I get this is a huge taboo...",

        # BM script9:440 (d)
        "*Grumbling to herself* Like... I get it, we're all living crazy fucking lives, I know we've all got a million things going on and enough shit to worry about.":
            "*Grumbling to herself* And on top of that, we're all living crazy enough lives, I know we've all got a million things going on and enough shit to worry about.",

        # BM script9:446 (d)
        "I’D STILL HAVE APPRECIATED IT IF MY SISTER HAD TOLD ME SHE WAS SCREWING MY FUCKING BOYFRIEND!":
            "I’D STILL HAVE APPRECIATED IT IF MY SISTER HAD TOLD ME SHE WAS SCREWING MY FUCKING BROTHER!",

        # BM script9:448 (p)
        "Oh, so he's {i}your{/i} boyfriend now.":
            "As if I'm the {i}only{/i} one here screwing her brother.",

        # BM script9:449 (p)
        "You do realize you could've told me too, right?":
            "Something {i}you{/i} could've told me too, right?",

        # BM script9:450 (d)
        "Or is that not your fault either?!":
            "Or are you the only one allowed to keep such a secret?!",

        # BM script9:488 (p)
        "Let's make him choose!":
            "Let's make him choose which {i}sister{/i} he wants!",

        # BM script9:510 (p)
        # BA/N: Disabled, consistency with below
        # "{sc=3}[mc!u]!!{/sc}":
        #     "{sc=3}BRO!!{/sc}",

        # BM script9:511 (d)
        # Disabled, interferes with other lines, plus they're both mad at MC so calling him by name feels more appropriate
        # "{sc=3}[mc!u]!!!{/sc}":
        #     "{sc=3}BRO!!!{/sc}",

        # BM script9:2339 (d)
        "Last thing [mc] would want is for you to get hurt looking for him.":
            "Last thing your brother would want is for you to get hurt looking for him.",

        # BM script9:3016
        "His only family is a drunk skunk of a father living an ocean away.":
            "His only other family is a drunk skunk of a father living an ocean away.",

        # BM script9:3123 (d)
        "First, her sister. Oh, what a {i}coincidence{/i}, the last person to see [mc].":
            "First, the other sister. Oh, what a {i}coincidence{/i}, the last person to see [mc].",

        # BA/N: I added next three lines during Hyril'ar but idk if I want to keep them lel

        # BM script9:3842 (ca)
        "[mc], however, appears to possess a magnetic pull, both physical and, I daresay, emotional, that draws multiple females to him alone.":
            "[mc], however, appears to possess a magnetic pull, both physical and, I daresay, emotional, that draws multiple females to him alone. Even his own blood is caught in its grasp.",

        # BM script9:3844
        "Astounding...":
            "Even his relatives? Astounding...",

        # BM script9:4234
        "Among them is a woman named Dalia, who is just as strong, if not stronger than he is in close combat.":
            "Among them is a woman named Dalia, one of his sisters, who is just as strong, if not stronger than he is in close combat.",

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

        # BM script9:10498
        "*Starts reading* {i}Dear Ms. Carter, thank you for booking my humble property for this year’s Christmas Eve.":
            "*Starts reading* {i}Dear Ms. [lastname], thank you for booking my humble property for this year’s Christmas Eve.",

        # BM script9:10876
        "You've been hiding so many secrets from me, missy.":
            "You've been hiding so many secrets from me, sissy.",

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

        # BM script9:11563 (n)
        "I suspected.":
            "It’s hard for anything to escape her notice in this house, so I suspected she knew something was going on. But thanks for confirming it. ",

        # BM script9:11564 (n)
        "But thanks for confirming it.":
            "Still, I can’t believe she actually talked with you about this... {i}stuff{/i} happening between us, her own kids! Just what is she thinking?",
            #"Which begs the question of what exactly she thinks of all this going on between her kids...",

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

        # BM script9:11776
        "*Snorts* Looks like you should’ve invested another thousand hours in Skyrim, [mc].":
            "*Snorts* Looks like you should’ve invested another thousand hours in Skyrim, little brother.",

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
            "You should learn to savor the moment, lil bro...",

        # BM script9:12109, also overwrites script7:9372, script9:12363, both okay
        "Oh, Penny...":
            "Oh, sis...",

        # BM script9:12117
        "*Giggles* You’re not secretly recording me, right? Taking advantage of little old blind Penny...?":
            "*Giggles* You’re not secretly recording me, right? Taking advantage of your blind big sister...?",

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
            "Please... brother...",

        # BM script9:12218 (menu)
        "Make her call you something different":
            "Make her call you something different (Use \"Other\" for \"little brother\"/\"bro\")",

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

        # BM script9:12303
        "Such a bad girl...":
            "Wanting to get fucked by my little brother...",
            #"Wanting my little brother to fuck me...",

        # BM script9:12341
        "You're choking my cock, Penny...":
            "You're choking my cock, sis...",

        # BM script9:12363
        # Overwritten by BM script9:12109, okay
        # "Oh, Penny..." -> "Oh, sis..."

        # BM script9:12426
        "You're just too much, Penny...":
            "You're just too much, sis...",

        # BM script9:12459
        "Hey... can I... a-ask you something, [mc]?":
            "Hey... can I... a-ask you something, bro?",

        # BM script9:12519 (menu)
        "Have anal sex with Penny":
            "{color=[walk_points]}Have anal sex with your big sister [gr][mt](Anal)",

        # BM script9:12535
        "I’ll remember it next time, Penny... word for word.":
            "I’ll remember it next time, sister... word for word.",

        # BM script9:12570
        "Last chance to back out, Penny...":
            "Last chance to back out, sis...",

        # BM script9:12614
        "Oh... fuck Penny, this gets dry so quickly...":
            "Oh... fuck sis, this gets dry so quickly...",

        # BM script9:12638
        "Ohhh Penny... you’re gonna make me lose my f-fucking mind...":
            "Ohhh sister... you’re gonna make me lose my f-fucking mind...",

        # BM script9:12706
        "My god, Penny...":
            "My god, sis...",

        # BM script9:12870
        "I’ve never had a Christmas dinner like this before, Nan.":
            "I’ve never had a Christmas dinner like this before, Mom.",

        # BM script9:12988 (d)
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

        # BM script9:13204 (x)
        # Alex line overwritten by BM script5:9751 (p), tbh still works okay as a casual "bro" (she'll join the family eventually lol)
        # "Damn, [mc]..." -> "Damn, bro..."

        # BM script9:13216 (p)
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

        # BM script9:13632 (p)
        "Thank you for your very... scientific, articulate observation, [mc].":
            "Thank you for your very... scientific, articulate observation, brother.",

        # BM script9:13641
        "And just from external observation...":
            "And just from objective observation...",

        # BM script9:14153 (d)
        # Overwritten by BM script6:14300 (d), okay
        # ""Thank you, [mc]!" -> "Thanks, bro!"

        # BM script9:14226 (d)
        "Yeah, you'd sure like that.":
            "Seriously? We're mostly family here.",

        # BM script9:14241 (p)
        "Half of the people here have already seen me naked a hundred times, and the rest... well, we’re just having fun. Who cares?":
            "Like you said, it's just family here, plus Alex... and well, we’re just having fun. Who cares?",

        # BM script9:14294
        "Like you said, the card didn't mention anything else. Anyone saying otherwise would just be greedy.":
            "Like you said, the card didn't mention anything else. We can keep it “family-friendly.”",

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

        # BM script9:14590 {specific}
        # Excludes script3:7862
        "Those are the rules!":[
            ("As the only guy here, I might be taking those points!","script9:14590"),

            # Bonus Mod
            ("As the only guy here, I might be taking those points!","script9:14731"),

            # Multi Mod
            ("As the only guy here, I might be taking those points!","script9:14604"),
        ],

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

        # BM script9:14668 (d)
        "Let's go, [mc]! Time to put on a show!":
            "Let's go, bro! Time to put on a show!",

        # BM script9:14956 (n)
        "Well, thank you, [mc].":
            "Well, thank you, dear.",

        # BM script9:15202 (p)
        "You... YOU HAVE TOO–?!":
            "You... YOU HAVE TOO–?! {w=0.7}BUT HE'S– {w=0.5}he's your–",

        # BM script9:15211
        "I feel like... she probably suspects, but it's a different case with you than it is with me.":
            "I feel like... she probably suspects, but it's obviously a much different case with you than it is with me.",

        # BM script9:15217
        "I know it all might sound like a crazy bunch of bullshit, but...":
            "I know this might sound like a crazy bunch of bullshit on top of all that, but...",

        # BM script9:15222
        "This went from zero to nuclear real quick.":
            "This went from zero to nuclear real quick. With your own brother...",

        # BM script9:15236 (n) {inject}
        "Why didn't you finish your drink, Mom...?":[
            ("M-Mom, I can explai–","script9:15236",[
                'p "Wait..."',
                'p "Why... Why didn’t you finish your drink, Mom...?"'
            ]),

            # Bonus Mod
            ("M-Mom, I can explai–","script9:15379",[
                'p "Wait..."',
                'p "Why... Why didn’t you finish your drink, Mom...?"'
            ]),

            # Multi Mod
            ("M-Mom, I can explai–","script9:15250",[
                'p "Wait..."',
                'p "Why... Why didn’t you finish your drink, Mom...?"'
            ]),
        ],

        # BM script9:15241 (n)
        "NO. FUCKING. WAY.":
            "NO. FUCKING. WAY. YOU TOO?!",

        # BM script9:15247
        "This family is WILD!":
            "This family is {b}{i}WILD!",

        # BM script9:15280 (p)
        "No. No, no... no. Not really.":
            "No. No, no... no. Of course not.",

        # BM script9:15556
        "But seriously, I'm off to bed! Goodnight, [mc].":
            "But seriously, I'm off to bed! Goodnight, bro.",

        # BM script9:15559, also overwrites script9:15650
        "Goodnight, Dalia.":
            "Goodnight, sis.",

        # BM script9:15647 (d) {specific}
        # Excludes script:2127 (n)
        "Goodnight, [mc].":[
            ("Goodnight, bro.","script9:15647"),

            # Bonus Mod
            ("Goodnight, bro.","script9:15798"),

            # Multi Mod
            ("Goodnight, bro.","script9:15661"),
        ],

        # BM script9:15835 (d)
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
            "*Touching herself* AAaah... watching you j-jerk off your brother is so fucking hot, Dal......",

        # BM script9:16060 {specific}
        # Excludes 1411 other lines
        ". . .":[
            ("*Whispers sharply* Hey! Alex is right there!","script9:16060"),

            # Bonus Mod
            ("*Whispers sharply* Hey! Alex is right there!","script9:16217"),

            # Multi Mod
            ("*Whispers sharply* Hey! Alex is right there!","script9:16074"),
        ],

        # BM script9:16061
        "...Thanks.":
            "*Whispering* ...But, thanks.",

        # BM script9:16088
        "You're dreaming.":
            "HEY! I'm your sister! And even if I weren't, I'm-",

        # BM script9:16089
        # interferes with script5:6463. works better this way ngl
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

        # BM script9:16247
        "O-Ohh Dalia, that feels so fucking good...":
            "O-Ohh sis, that feels so fucking good...",

        # BM script9:16269
        "Let yourself go and look at the man you love losing control because of you and your beautiful body.":
            "Let yourself go and look at your beloved brother losing control because of you and your beautiful body.",

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
            "*Groaning* Oh D-Daly...",

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

        # BM script9:16597 {inject}
        "*Choked laugh* Y-You're one t-to talk...":[
            ("*Choked laugh* Y-You're one t-to talk, girl... ","script9:16597",[
                'd "I-If he’s your daddy, am I your a-auntie...?"',
                'x "*Breathless giggle* Is t-that what you want, Auntie D-Dal?"'
            ]),

            # Bonus Mod
            ("*Choked laugh* Y-You're one t-to talk, girl... ","script9:16762",[
                'd "I-If he’s your daddy, am I your a-auntie...?"',
                'x "*Breathless giggle* Is t-that what you want, Auntie D-Dal?"'
            ]),

            # Multi Mod
            ("*Choked laugh* Y-You're one t-to talk, girl... ","script9:16611",[
                'd "I-If he’s your daddy, am I your a-auntie...?"',
                'x "*Breathless giggle* Is t-that what you want, Auntie D-Dal?"'
            ]),
        ],

        # BM script9:16693
        "*Grinning* You'll be fine, Dal...":
            "*Grinning* You'll be fine, sis...",

        # BM script9:16708
        "T-That's because [mc] broke me! A-And all because of you!":
            "T-That's because my brother broke me! A-And all because of you!",

        # BM script9:16722
        "How does it feel, huh? Going around making every girl with daddy issues fall for you. Must be one hell of a power trip.":
            "How does it feel, huh? Going around making every girl with daddy issues fall for you. Even your own {i}sister{/i}. Must be one hell of a power trip.",

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

        # BM script9:20898
        "Yeah, yeah — your nose isn't lying, Dalia. I brought crepes for everyone!":
            "Yeah, yeah — your nose isn't lying, Daly. I brought crepes for everyone!",
    }

    # cousin_map = {
    # }

    annie_sister_map = {
        # -----------------------------------------
        # aka the Full Incest map, is an add on to base map.
        # Annie as twin sister and Nancy’s child. Thus Dalia's Irish twin (triplet?) as well. 
        # Annie has same last name as MC
        # Annie’s father and mother mentions converted to paternal grandparents
        #     MC's grandparents canonically exist in UK (script6:1392)
        # half sis map and only sis map based on this, if edits are made here check if they can be applied there too.
        # -----------------------------------------
        # Character Notes
        # Annie has been playing for 3 years (script:8183)
        # MC and Annie are closer so they use bro/sis more often
        # revert to names when being more serious
        # Annie and Penny call each other lil/big sis, Dalia is just sis
        # -----------------------------------------
        # AS script:0000 = Annie Sister map, RPY file:Line Number
        #     Numbers based on v0.9.5, subject to change in future updates
        # Tags based who the line is about contextually, not always the speaker.
        # Selectively applied for clarification
        # (menu) = Choice menu line
        # (mc) = MC line
        # (n) = Nancy line
        # (p) = Penelope line
        # (d) = Dalia line
        # (a) = Annie line
        # (x) = Alex line
        # (l) = Luna line
        # (no) = Nova line
        # (ca) = Calypso line
        # -----------------------------------------
        # Code tags
        # {specific} = use of Variant 2 to target specific lines
        # {inject} = use of Variant 3 to inject new lines      
        # -----------------------------------------
        # LW/N = Lucifer_W's notes
        # l9/N = l9453394's notes
        # BA/N = BlueArrow's notes
        # -----------------------------------------

    # -----------------------------------------
    # v0.1 script.rpy

        # BA/N: Want to mention "Grandparents" at some point in the intro, otherwise their appearance comes out of no where later on. 
        # not sure where tho
        # LW/N: Sounds like a good Idea maybe with a new lable or adding to the intro lable.
        # BA/N: Added in the train scene

        # AS script:948
        "My name is [mc] [lastname]. I was born in the city of Kredon, a relatively small town on the west coast of the United States.":
            "My name is [mc] [lastname]. I was born into a family of six in the city of Kredon, a relatively small town on the west coast of the United States.",

        # AS script:950
        "My mother left shortly after I was born and my dad was never around much because he was always so focused on his job.":
            "My mother always cared for me and my sisters, but my dad was never around much. He was always so focused on his job and never made time for our family. This basically left my mom as the only parent taking care of four young kids while still juggling school.",

        # AS script:952
        "I know, I know, this all sounds pretty gloomy... but don't worry! This is not about to be one long sob story.":
            "He got custody of me and my twin sister, taking us with him to the UK while my mom stayed behind with our two older sisters. I know it sounds a bit bleak, but don't worry - this isn't a sob story.",

        # AS script:957
        "He had to work to support us both. Heaven knows where I'd be without him.":
            "He had to work to support the three of us. Heaven knows where we'd be without him.",

        # AS script:1046
        "(Annie is a close friend from my childhood.)":
            "(Annie is my younger twin sister.)",

        # BA/N: reworked next few lines to flesh out UK backstory and mention grandparents. Still a bit clunky ngl

        # AS script:1047
        "(When I moved from Kredon, she was my next-door neighbor and the first person I met, along with Chang.)":
            "(When we moved from Kredon, all we had were each other until we met Chang. He helped fill the gap of our missing family, but obviously couldn't be around us all the time.)",

        # AS script:1048
        "(We quickly bonded after discovering we both had something in common... the absence of our parents.)":
            "(We did have our grandparents on our dad's side living in the UK. They loved to pamper us when they could, but rarely were able to visit.)",

        # AS script:1049
        "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them.)":
            "(With our father always off working, it was pretty much just the two of us at home most of the time.)",

        # AS script:1050
        "(We were both lost... and lonely.)":
            "(In those chaotic and lonely times, we gave each other stability.)",

        # AS script:1051
        "(After finding a companion within each other, we’ve been inseparable ever since.)":
            "(As cliche as it may be for twins, we've naturally become inseparable ever since.)",

        # AS script:1053
        "(Because of how close we were, people always believed we were dating... but the truth is, we're just friends.)":
            "(Because of how close we were, people liked to joke that we would've make a great couple... but the truth is, we're just siblings.)",

        # AS script:1054
        "(I mean… she's cute, and we love spending time with each other, but I've never tried to make a move on her.)":
            "(. . .)",

        # AS script:1055 {inject}
        "(I could never do it.)":[
            ("(Well... she is cute... and we love spending time with each other...)","script:1055",[
                'mc "(I mean, if–){nw=0.8}"'
            ]),

            # Bonus Mod
            ("(Well... she is cute... and we love spending time with each other...)","script:1092",[
                'mc "(I mean, if–){nw=0.8}"'
            ]),

            # Multi Mod
            # script:1055, same as original
        ],

        # AS script:1056
        "(She'd probably freak out if I did.)":
            "(NO.{w=0.5} Stop it.{w=1} She'd probably freak out if I did.)",

        # AS script:1059
        "(It would be... weird for us. Yeah! That's the word. Weird.)":
            "(It would be... wrong. Very wrong! We're twin siblings after all.)",

        # AS script:1060
        "(It's just not the kind of relationship we have.)":
            "(Why am I even thinking about this!?)",

        # AS script:1076
        "I was saying that I spoke with Nancy.":
            "I was saying that I spoke with Mom.",

        # AS script:1080
        "I can't wait to see her. I hope she recognizes me.":
            "I can't wait to see her. I hope she recognizes us.",

        # AS script:1082
        "*Laughs* I'm sure she will.":
            "*Laughs* I'm sure she will. She is our mother after all.",

        # AS script:1085
        # bypass added in skip_nancy_swap, edit down there if this line is changed
        "(Nancy used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(Our mother, Nancy, used to look after us and our sisters in Kredon. Since our father was always working, I can recall more memories with her than with him.)",

        # AS script:1086
        # LW/N: FIXED: Handle both versions
        "(I used to spend the entire afternoon playing with Nancy and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(The two of us used to spend entire afternoons playing with Mom and our older sister Dalia, but then we had to move and ended up losing touch.)",

        "(I used to spend the entire afternoon playing with Mom and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(The two of us used to spend entire afternoons playing with Mom and our older sister Dalia, but then we had to move and ended up losing touch.)",

        # AS script:1088
        # Handle both versions
        "(Living with them will be much cheaper than renting a student residence, and it’ll surely be nice to see Nancy and Dalia again.)":
            "(Living with them will be much cheaper than renting a student residence, and it'll surely be nice to see Mom, Dalia, and our oldest sister Penelope again.)",

        "(Living with them will be much cheaper than renting a student residence, and it’ll surely be nice to see Mom and Dalia again.)":
            "(Living with them will be much cheaper than renting a student residence, and it'll surely be nice to see Mom, Dalia, and our oldest sister Penelope again.)",

        # AS script:1089
        "(Come to find out, she actually had 2 rooms available, so Annie will have a place to stay as well!)":
            "(Come to find out, she actually had our old rooms available!)",

        # AS script:1090
        "(She’s actually been the one who’s been coordinating with Nancy over the phone, even though they didn’t know each other beforehand.)":
            "(Annie’s actually been the one who’s been coordinating with Mom over the phone, I didn't have to do anything.)",

        # AS script:1093
        "Do you think she will like me?":
            "I'm really excited, do you think everything will go well?",

        # AS script:1095
        "Nancy? Of course!":
            "Don't worry sis, it'll be alright.",

        # AS script:1096
        "Don't worry about it, Annie. I haven't seen her in over 10 years, so it’ll probably feel like I’m meeting her for the first time too!":
            "And anyways, it's not like it's a stranger we're meeting, it's our family.",

        # AS script:1112
        "What's the first thing you're going to do when we get to our new home?":
            "What's the first thing you're going to do when we get to our old home?",

        # AS script:1157
        "You should go to sleep too, Annie. We have to wake up early tomorrow.":
            "You should go to sleep too, sis. We have to wake up early tomorrow.",

        # AS script:1179
        "You're nothing but a big ball of envy because your best friend can play Eternum and you can't since you didn't save any money.":
            "You're nothing but a big ball of envy because your dear sister and bestie can play Eternum and you can't since you didn't save any money.",

        # AS script:1184
        "B-Best friend?":
            "B-Bestie?",

        # AS script:1220
        "But that doesn't mean you aren’t also my best friend, Annie!":
            "But that doesn't mean you aren’t also my best friend, Annie! And my precious twin sister!",

        # AS script:1241
        "We've been through too much together, Annie.":
            "We've literally been together since birth, sis.",

        # AS script:1254
        "You're my best... male friend!":
            "You're my best... male friend! Basically my brother!",

        # AS script:1262
        "Ahh, it's a deal, my friend!":
            "Ahh, it's a deal, bro!",

        # AS script:1339
        "Hello everyone! Annie is here!":
            "Hello everyone! Annie is back!",

        # AS script:1344
        "I know you're excited Annie, but I'd appreciate it if you could at least carry your hand baggage!":
            "I know you're excited sis, but I'd appreciate it if you could at least carry your hand baggage!",

        # AS script:1347
        "It's just that I'm excited to discover the town where you grew up!":
            "It's just that I'm excited to be in our hometown again!",

        # AS script:1348
        "Well, I left this place when I was 8, so I don’t really remember anything.":
            "Well, I understand, but we left this place when we were 8, so I don't really remember anything.",

        # AS script:1363
        "I’ve never had a chance to come back ‘til now, so I'm excited to relive all my childhood memories!":
            "We’ve never had a chance to come back ‘til now, so I'm excited to relive all our childhood memories!",

        # AS script:1354
        "Anyway, do you know where Nancy is?":
            "Anyway, do you know where Mom is?",

        # AS script:1757
        "Mission failed, [mc]...":
            "Mission failed, bro...",

        # AS script:1762
        "You must be Annie!":
            "Annie! My precious little girl!",

        # AS script:1763 (n)
        "Is that right?!":
            "I missed you so much!",

        # AS script:1764 (a) {specific}
        # Excludes other lines
        "Y-Yeah.":[
            ("Y-Yeah, me too.","script:1764"),

            # Bonus Mod
            ("Y-Yeah, me too.","script:1807"),

            # Multi Mod
            ("Y-Yeah, me too.","script:1765"),
        ],

        # AS script:1765
        "You're even cuter than I imagined! Your voice matches your appearance so much!":
            "You're even cuter than when I last saw you. You've grown so much!",

        # AS script:1766 (a)
        "T-Thank you, miss.":
            "T-Thank you, Mom.",

        # AS script:1767
        "It’s me, Nancy! Even though we’ve only been speaking on the phone for the past few days, I feel like we’ve been becoming good friends already! Isn't that right, Annie?":
            "God, you can't imagine how much I missed my little twins!",

        # AS script:1769 (a)
        "Definitely! I’d say we’ve been hitting it off pretty well!":
            "We missed you too, Mom...",

        # AS script:1770 (a)
        "It's so nice to finally meet you!":
            "It's so nice to finally see you again!",

        # AS script:1775
        "I've prepared a room for each of you, though I must warn you – don't expect anything fancy. The bedrooms are pretty small.":
            "I've prepared your old rooms for each of you, though I must warn you – don't expect anything fancy.",

        # AS script:1777 (a)
        "No worries, miss! I'm sure it'll be more than enough!":
            "No worries, Mom! I'm sure it'll be more than enough!",

        # AS script:1779
        "I hope so! And please, just call me Nancy!":
            "I hope so!",

        # AS script:1781
        "Okay! Thank you, Nancy!":
            "If our rooms didn't shrink since last time, it'll be alright.",

        # AS script:1783
        "Have you ever been to the USA before, Annie?":
            "*Laughs* Well, you two are also much bigger now. Do you remember your time in the USA, Annie?",

        # AS script:1785
        "Never! But I’ve always wanted to visit. [mc] has always spoken very well of his time in Kredon.":
            "Kind of, but it's been so many years.",

        # AS script:1786
        "And of his babysitter!":
            "But I do remember all the fun we had playing together!",

        # AS script:1790
        "Yeah, since my Dad was constantly working, I've always said you were like a parent to me.":
            "Of course! How could we forget those times?",

        # BA/N: flow of the next 2 lines still could use improvement

        # AS script:1793
        "Now I work in a laboratory, but back then I was still finishing my thesis. Thankfully [mc]'s father came along and offered me the babysitting gig.":
            "After you left, I was able to finish my thesis.",

        # AS script:1794
        "It was not only well-paid, but also allowed me the flexibility to take care of my daughters at the same time. And for me, being a single mother, that was essential.":
            "Thanks to that, I work in laboratory now. It pays pretty well.",

        # AS script:1796
        "You have 2 daughters, right?":
            "That's great! So how are our sisters doing?",

        # AS script:1798
        "Yes, Dalia and Penelope. Penny was a little older when I was [mc]'s nanny, so she used to play on her own, but Dalia got very close to him!":
            "They're doing well, they've grown up wonderfully like you.",

        # AS script:1800
        "*Laughs* I remember she was always stealing my games!":
            "*Chuckles* That's good to hear!",

        # AS script:1802
        "But then, after my daughters grew up, I was able to start a better job within a local company.":
            "Yes... in the beginning I worked a lower-paying job but now that those two are older, I was able to start a better job within a local company.",

        # AS script:1807
        "Ahh, aren't you cute!":
            "Ahh, thank you, honey!",

        # AS script:1821
        "Alright then! Let's go to the car! Dalia and Penelope are dying to see you again!":
            "Alright then! Let's go to the car! Dalia and Penelope are dying to see you two again!",

        # ========== START label mod "welcome_mod" ==========
            # line numbers for both files 

        # AS script:1843 IncestLables:24
        "(Each day I would spend the afternoon playing with her and Dalia. We had dinner every night at eight, and then Nancy drove me home once it got late.)":
            "(My afternoons were spent playing with Mom, Dalia, and Annie. We had dinner every night at eight, and then went to bed.)",

        # AS script:1845 IncestLables:26
        "(She would always call me on my birthday, but... aside from that, I never reached out. I have to make it up to her somehow.)":
            "(Mom would always call us on our birthday, but... aside from that, I never reached out. I have to make it up to her somehow.)",

        # AS script:1858 (a)
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

        # AS script:1928
        # replaced by IncestLables:109

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
            "Hey [mc], I can't wait to hear all about what happened to you and Annie!",

        # AS script:1970 IncestLables:151
        "Oh, and you must be Annie! Nice to meet you too!":
            "Oh, and Annie! Nice to see you again!",

        # AS script:1972 IncestLables:153
        "Welcome to the family!":
            "Welcome back, you two!",

        # AS script:1973 IncestLables:154
        "By the way, I love your haircut!":
            "By the way, I love your haircut, sis!",

        # AS script:1983 IncestLables:164
        "Of course he doesn't mind!":
            "Of course they don't mind!",

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

        # AS script:2115 IncestLables:296
        "Your room will be on the second floor—the last one on the right.":
            "Do you remember the way to your old room?",

        # AS script:2116 IncestLables:297
        "Ah, I remember that room! It was the one with a lot of natural light.":
            "I think so. Second floor, last one on the right, right? The one with a lot of natural light.{w} (Hey, that rhymed!)",

        # AS script:2119 IncestLables:300
        "Well, since [mc] seems to remember where everything is already... Do you want a tour of the house, Annie?":
            "Well, since [mc] doesn't want any supper... Do you want something to eat, Annie?",

        # AS script:2124 IncestLables:305
        "Goodnight [mc]! Sweet dreams!":
            "Goodnight, bro! Sweet dreams!",

        # ========== END label mod "welcome_mod" ==========

        # AS script:2407
        "Annie, Penelope, and Dalia have been up for a while!":
            "Your sisters have been up for a while!",

        # AS script:2436
        "(Although, I think I'll wait a couple of weeks. I don't want [mc] and Annie to think I'm a promiscuous woman or anything...)":
            "(Although, I think I'll wait a couple of weeks. I don't want [mc] and Annie to think I've become a promiscuous woman or anything...)",

        # AS script:2760
        "That's what I said, but she told us she wanted to take a tour of the neighborhood.":
            "That's what I said, but she told us she really wanted to revisit the neighborhood.",

        # AS script:2762
        "Oh yeah, that sounds like Annie. I guess she already told you she also plays Eternum?":
            "Oh yeah, that sounds like sis. I guess she already told you she also plays Eternum?",

        # AS script:2798
        "(Annie was always good at making friends.)":
            "(Like me, Annie was always good at making friends. Must run in our blood.)",

        # AS script:2799
        "(I guess I should let them walk to school on their own, since I don't wanna look like a jealous boyfriend or something.)":
            "(I guess I should let them walk to school on their own, since I don't wanna look like the cliche overprotective brother.)",

        # AS script:2826
        "Believe me, Kredon can seem like a very boring place until you’re able to discover it with someone that knows all the hotspots.":
            "Believe me, Kredon can seem like a very boring place unless you’re able to re-discover it with someone that knows all the hotspots.",

        # AS script:2830
        "*Laughs* Like what? I thought you just got here yesterday.":
            "*Laughs* Like what? I thought you just got back yesterday.",

        # AS script:2836
        "I know you're new around here, but you have no idea how lucky you are right now.":
            "I know you're basically new around here, but you have no idea how lucky you are right now.",

        # AS script:2910
        "The lady said no, buddy.":
            "Hands off my sister, you jerk.",

        # AS script:2934
        "The lady said no.":
            "Her brother. And she said no.",

        # AS script:2952, also overwrites script4:4803, okay
        "Are you okay, Annie?":
            "Are you okay, sis?",

        # AS script:2996
        "Will you be alright, Annie?":
            "Will you be alright, sis?",

        # AS script:3006
        "And... thank you again for helping me out back there, [mc].":
            "And... thank you again for helping me out back there, bro.",

        # AS script:5178
        "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal when I was living with my dad.":
            "I don't know, it felt pretty special to me. Annie and I never really had a nice, home-cooked meal while we were living with Dad.",

        # AS script:5200
        "Tomorrow you'll finally be connected to Eternum, [mc]! After waiting for so many years!":
            "Tomorrow you'll finally be connected to Eternum, bro! After waiting for so many years!",

        # AS script:5207
        "We’re only missing Nancy and Penelope, then our group would be complete!":
            "We’re only missing Mom and Penelope, then our whole family would be complete!",

        # AS script:5209 (p)
        "*Laughs* I wouldn't count on it, Annie, sorry.":
            "*Laughs* I wouldn't count on it, lil sis, sorry.",

        # AS script:5308 (p)
        "Nah, don't worry Annie, it's my turn today. But thank you!":
            "Nah, don't worry, lil sis, it's my turn today. But thank you!",

        # AS script:5331 (a)
        "Goodnight [mc]!!":
            "Goodnight, bro!!",

        # AS script:5479
        "(Looking at hot pics of Penelope, yeah, great idea, [mc]. Way to not have even more fantasies of all these girls around me...)":
            "(Looking at hot pics of Penelope, yeah, great idea, [mc]. Way to not have even more fantasies of all the girls in your family...)",

        # AS script:5583 (n) {inject}
        "(I mean... If Dalia and Penelope never found out, then would it really be so bad? It’d be our little secret...)":[
            ("(I mean... If the girls never found out, then would it really be so bad...?)","script:5583",[
                "show ale 31",
                'n "(What am I thinking?! Of course it would be! He’s my son...)" with dis06'
            ]),

            # Bonus Mod
            ("(I mean... If the girls never found out, then would it really be so bad...?)","script:5649",[
                "show ale 31",
                'n "(What am I thinking?! Of course it would be! He’s my son...)" with dis06'
            ]),

            # Multi Mod
            ("(I mean... If the girls never found out, then would it really be so bad...?)","script:5584",[
                "show ale 31",
                'n "(What am I thinking?! Of course it would be! He’s my son...)" with dis06'
            ]),
        ],

        # base map label mod lines explaining MC, Annie, and Dalia's close age here
            # REPLACED BY INJECTION, below

        # AS script:6047 {inject} (replaces labelmod)
        "Yeah, we've known each other since we were little.":[
            ("Yeah, we were separated as kids when our parents divorced.","script:6047",[
                "show ale 74",
                'x "Now that I think about, Dalia did mention having younger siblings before." with dis',
                'x "How are you in the same class as us?"',
                "show ale 75",
                'mc "*Chuckles* I was actually born later that same year, close enough for us to be in the same grade."',
                'mc "The other younger sibling is my twin sister, so she’s also in our grade."',
                'mc "She’s in a different class though."',
                "show ale 78",
                'x "Oh, wow. That’s quite the family." with dis'
            ]),

            # Bonus Mod
            ("Yeah, we were separated as kids when our parents divorced.","script:6115",[
                "show ale 74",
                'x "Now that I think about, Dalia did mention having younger siblings before." with dis',
                'x "How are you in the same class as us?"',
                "show ale 75",
                'mc "*Chuckles* I was actually born later that same year, close enough for us to be in the same grade."',
                'mc "The other younger sibling is my twin sister, so she’s also in our grade."',
                'mc "She’s in a different class though."',
                "show ale 78",
                'x "Oh, wow. That’s quite the family." with dis'
            ]),

            # Multi Mod
            ("Yeah, we were separated as kids when our parents divorced.","script:6048",[
                "show ale 74",
                'x "Now that I think about, Dalia did mention having younger siblings before." with dis',
                'x "How are you in the same class as us?"',
                "show ale 75",
                'mc "*Chuckles* I was actually born later that same year, close enough for us to be in the same grade."',
                'mc "The other younger sibling is my twin sister, so she’s also in our grade."',
                'mc "She’s in a different class though."',
                "show ale 78",
                'x "Oh, wow. That’s quite the family." with dis'
            ]),
        ],

        # AS script:6049 use with inject
        "Probably the only two people in this class that are actually worth talking to.":
            "Well, you and Dalia are probably the only people in this class that are actually worth talking to.",

        # ========== START label mod "preeternum_mod" backup ==========
            # Full replacement label with some line/image rearrangements
            # Rewrote because since they lived together in the UK, MC should already know some basics from how often Annie plays
            # Below is original draft/backup if mod does not trigger.

        # AS script:6093
        "Let's go! We're already late!":
            "Let's go, bro! We're already late!",

        # AS script:6094
        # interferes with script:7111 (a), the cause of switching to label mod but now that Variant 2 exists dont feel like changing it anymore lol
        #"*Laughs* What are you wearing?":
        #    "*Laughs* Already got your Eternum E-Suit on, huh?",

        # AS script:6095
        "No time for questions! Come on!":
            "It's the Eternum E-Suit, dummy! Now, come on already!",

        # AS script:6099
        "But seriously, what are you wearing?":
            "You always play in your room, so I forgot about the E-sui—Oh crap, I don't have one yet!",

        # AS script:6101
        "Eternum's official E-Suit, of course!":
            "It should've been included with the game.",

        # AS script:6102
        "Didn't you see all the stuff that was inside the game’s box??":
            "Did you look through everything in the box?",

        # AS script:6106
        "So... I have to wear that suit too?":
            "So... do I have to wear the entire thing?",

        # AS script:6115
        "Nah, I just wanted to show you how cool the suit looks.":
            "Nah, I just have it on so I can quickly jump in later.",

        # AS script:6124
        "You can look if you want...":
            "You can look if you want, sis...",

        # AS script:6147
        "Sorry! Did that hurt?!":
            "Sorry, bro! Did that hurt?!",

        # AS script:6179, also overwrites script:6728, script4:6902, both okay
        "Annie?!":
            "Hey, sis?!",

        # ========== END label mod "preeternum_mod" backup ==========

        # AS script:6511
        #"(Dammit, Annie didn't tell me about any of this...)":
        #    "(Dammit, sis didn't tell me about any of this...)",

        # AS script:6606
        "By the way, your outfit looks awesome!":
            "By the way, your outfit looks awesome, sis!",

        # AS script:6695
        "No, he's not! He's [mc]! He's tough!":
            "No, he's not! He's my brother! He's tough!",

        # AS script:6697
        "So this is the [mc] you're always talking about?":
            "So this is the twin brother you're always talking about?",

        # AS script:6712
        "That's the thing, [mc]!":
            "That's the thing, bro!",

        # AS script:6728
        # Overwritten by AS script:6179, okay
        # "Annie?!" -> "Hey, sis?!"

        # AS script:6810
        "Thank god I have you, Annie... I’d probably be lost in a ditch somewhere without you!":
            "Thank god I have you, sis... I’d probably be lost in a ditch somewhere without you!",

        # AS script:6942
        "Thanks, Annie!":
            "Thanks, sis!",

        # AS script:6982
        "Alright. Thank you Annie!":
            "Alright. Thanks again, sis!",

        # AS script:7130
        "(That's a bad idea...)":
            "(Nope, bad idea. She's my sister!)",

        # AS script:7142, also overwrites script:7172
        "*Laughs* Don't get lost or get yourself into much trouble, alright?":
            "*Laughs* Don't get lost or get yourself into much trouble, alright bro?",

        # AS script:7176
        "(Jeez, I've always tried to not think of Annie in \"that\" way because I don't want to ruin our friendship, but now...)":
            "(Jeez, I {i}really{/i} need to stop this... but...)",

        # AS script:7179
        "(She's got curves in all the right places...)":
            "(She's not the skinny kid she used to be... she's got curves in all the right places now...)",

        # AS script:7186
        "(Damn... I guess she’s not the skinny kid she used to be...)":
            "(Dammit... Stop looking at your sister, [mc]...)",

        # AS script:7977
        "Oh... Come on Annie, it doesn't matter!":
            "Oh... Come on sis, it doesn't matter!",

        # AS script:8016, also overwrites script:8040
        "*Laughs* You always know how to make me laugh.":
            "*Laughs* You always know how to make me laugh, bro.",

        # AS script:8055
        "(Hehe, a little look won't hurt anyone...)":
            "(I guess a little look won't hurt anyone...)",

        # AS script:8102
        "Erm... Y-You're the best friend ever!":
            "Erm... Y-You're the best brother ever!",

        # AS script:8103
        "I'm glad you like it, Annie.":
            "I'm glad you like it, sis.",

        # AS script:8224
        # BA/N: Disabled for seriousness
        #"No. You have much more to lose, Annie.":
        #    "No. You have much more to lose, sis.",

        # AS script:8467
        "Thank you so much for playing with me, [mc]. It means a lot.":
            "Thank you so much for playing with me, bro. It means a lot.",

        # AS script:8468
        "The pleasure was all mine, Annie. Eternum is awesome. I’m so grateful I had you by my side.":
            "The pleasure was all mine, sis. Eternum is awesome. I’m so grateful I had you by my side.",

        # AS script:8525 (p)
        "You know, I'm not gonna lie, when Mom told me that you and Annie were gonna live with us for a while, I got a little annoyed.":
            "You know, I'm not gonna lie, when Mom told me that you and Annie were gonna come back for a while, I wasn't sure what to feel. Ten years apart is a long time after all.",

        # AS script:8526 (p)
        "But hey, I’m glad to say I was wrong. Both of you breathe so much life into this house. It almost feels like you've always lived here.":
            "But hey, I’m glad to say I was wrong. Both of you breathe so much life into this house. It almost feels like you never left.",


    # -----------------------------------------
    # v0.2 script2.rpy

        # AS script2:40
        "I have a feeling this shit is much bigger than we think, Annie.":
            "I have a feeling this shit is much bigger than we think, sis.",

        # AS script2:52
        "*Whispering* I don't like this, Annie...":
            "*Whispering* I don't like this, sis...",

        # AS script2:82
        "I don't know, Annie... him having a stroke? I'm not buying it.":
            "I don't know, sis... him having a stroke? I'm not buying it.",

        # AS script2:106
        "*Laughs* Don't mind him...":
            "*Laughs* Don't mind my brother...",

        # ========== START label mod "versiontwo_mod" ==========
            # edit of lines added by "versiontwo_mod"
        # REPLACED BY INJECTION, old code left just in case

        # AS IncestLables:2500
        #"Same to you. You must be Annie, [mc]'s told me about you.":
        #    "Same to you. You must be Annie, his twin sister. [mc]'s told me about you.",

        # AS IncestLables:2502
        #"Yep! I heard [mc] managed to win a neural implant at your cafe!":
        #    "Yep! I heard my brother managed to win a neural implant at your cafe!",

        # AS script2:112 {inject} (replaces labelmod)
        "It's so nice to meet you, Luna!":[
            ("It's so nice to meet you, Luna!","script2:112",[
                "scene aaa 15",
                'l "Same to you. You must be Annie, his twin sister. [mc]’s told me about you."',
                "scene aaa 14"
            ]),

            # Bonus Mod
            # script2:112, same as original

            # Multi Mod
            # script2:112, same as original
        ],

        # AS script2:113 used with inject
        "I heard [mc] managed to win a neural implant at your cafe!":
            "Yep! I heard my brother managed to win a neural implant at your cafe!",

        # ========== END label mod "versiontwo_mod" ==========

        # AS script2:113 disable if using inject
        #"I heard [mc] managed to win a neural implant at your cafe!":
        #    "I heard my brother managed to win a neural implant at your cafe!",

        # AS script2:126
        "Can I play with you guys, [mc]?!":
            "Can I play with you guys, bro?!",

        # AS script2:133
        "Horror? Okay... maybe it'd be better if you didn't join us, Annie.":
            "Horror? Okay... maybe it'd be better if you didn't join us, sis.",

        # AS script2:167
        "But you're not allowed to complain if you’re scared, Annie!":
            "But you're not allowed to complain if you’re scared, sis!",

        # AS script2:174
        "I'm sorry Annie, we both know you can't handle horror... no matter how light it is.":
            "I'm sorry sis, we both know you can't handle horror... no matter how light it is.",

        # AS script2:810
        "(Maybe his girlfriend...?)":
            "(Maybe his girlfriend... or his sister...?)",

        # AS script2:1014
        "Annie should be waiting for us already.":
            "Your sister should be waiting for us already.",

        # AS script2:1117
        "I love your outfit, Annie!":
            "I love your outfit, sis!",

        # AS script2:1389
        "Y-You're scaring me, [mc].":
            "Y-You're scaring me, bro.",

        # AS script2:1965
        "It's okay Annie, I know you’re not one for spooky things, but you’ve been doing good! I’m proud of you!":
            "It's okay sis, I know you’re not one for spooky things, but you’ve been doing good! I’m proud of you!",

        # AS script2:2051
        "Right, Annie?!":
            "Right, sis?!",

        # AS script2:2085, also overwrites script4:4995, okay
        "Right, Annie?":
            "Right, sis?",

        # AS script2:2187
        "(Then Luna will shower me with hugs and Annie will gush non-stop about how I'm the bravest man she's ever met.)":
            "(Then Luna will shower me with hugs and Annie will gush non-stop about how I'm the bravest man she's ever known.)",

        # AS script2:2905
        "What about you, Annie?":
            "What about you, sis?",

        # AS script2:3331
        "(He must think I'm a useless, scared kid...)":
            "(He must think I'm still a kid – a useless, scared kid...)",

        # AS script2:3339
        "(Yeah, nice job impressing [mc] in Eternum, Annie.)":
            "(Yeah, nice job impressing your brother in Eternum, Annie.)",

        # AS script2:3408
        "Oh, [mc]! I wasn’t sure if you were asleep already!":
            "Oh, hey bro! I wasn’t sure if you were asleep already!",

        # AS script2:3418
        "I told you! You shouldn't have played in Luna's server, Annie! You can't handle that scary stuff! Remember when we played Dead Space?":
            "I told you, sis! You shouldn't have played in Luna's server! You can't handle that scary stuff! Remember when we played Dead Space?",

        # AS script2:3474
        "You can sleep here as many times as you want. You don’t even have to ask, alright?":
            "You can sleep here as many times as you want. You don’t even have to ask, alright? Just like when we were little.",

        # AS script2:3479
        "Anytime, Annie.":
            "Anytime, sis.",

        # AS script2:3488
        "Hey, your room is so cozy!":
            "Wow, I forgot how cozy your room was!",

        # AS script2:3489
        "And you have a nice view of the backyard!":
            "And how nice the view of the backyard is from here!",

        # AS script2:3490
        "It is pretty nice!":
            "Yeah, sometimes I like to just look out the window and reminisce about playing down there when we were kids.",

        # AS script2:3491
        "My room faces the front yard. It’s a nice view too, but sometimes you can hear all the cars passing by.":
            "*Giggles* We'd always get so muddy because of how much it rained.",

        # AS script2:3495
        "Luckily your bed is big enough for the both of us. You could probably even fit three or four people on here!":
            "Luckily your new bed is big enough for the both of us. You could probably even fit three or four people on here!",

        # AS script2:3499
        "For sure... She's been super nice so far.":
            "For sure... There's so much more we need to thank Mom for too.",

        # AS script2:3500
        "We gotta prepare something to thank her one of these days.":
            "We gotta prepare something extra special for her one of these days.",

        # AS script2:3504
        "G-Goodnight, [mc].":
            "G-Goodnight, bro.",

        # AS script2:3506
        "Goodnight Annie.":
            "Goodnight sis.",

        # AS script2:3518
        #"(Oh yeah... I forgot that Annie came to sleep in my room.)":
        #    "(Oh yeah... I forgot that sis came to sleep in my room.)",

        # AS script2:3526
        "(She's probably used to hugging a pillow while she sleeps, or something.)":
            "(She used to hug a pillow or stuffed animal while she sleeps. I guess that hasn't changed.)",

        # AS script2:3530
        "(We're in quite an... intimate position... I don't want her to think I'm trying to take advantage of her while she sleeps.)":
            "(We're in quite an... intimate position... I don't want her to think her brother is trying to take advantage of her while she sleeps.)",

        # AS script2:3545
        "A-Are you awake, Annie?":
            "A-Are you awake, sis?",

        # AS script2:3557
        "Baloo?":
            "Baloo? The teddy bear Mom gave you when you were 5?",

        # AS script2:3559
        "Oh... Well... It's a stuffed bear that my mother gave me when I was 5, and...":
            "Yes, that Baloo...",

        # AS script2:3562
        "(Oh my god, why did I say that?! Now I probably sound like a child to him...)":
            "(Oh my god, why did I say that?! Now he probably thinks I'm still a child...)",

        # AS script2:3564
        "Oh... I didn't know about Baloo.":
            "Oh... I didn't know you still slept with Baloo.",

        # AS script2:3594
        "(He probably just sees me as the little girl who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)":
            "(He probably still sees me as his little sister who plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)",

        # AS script2:3595
        "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack.)":
            "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack. And not blood-related ones... he's not a weirdo like me who has feelings for her twin brother.)",

        # AS script2:3596
        "(I'll always just be Annie, the \"best friend\".)":
            "(I'll always just be Annie, the \"little sister\".)",

        # AS script2:3602
        "(I'm a fucking mess. She needs someone more mature.)":
            "(I'm a fucking mess. She needs someone more mature... And someone not blood-related... she's not a weirdo like me who has feelings for his twin sister.)",

        # AS script2:3607
        "(This is why I'll always just be [mc], the \"best friend\"...)":
            "(This is why I'll always just be [mc], the \"big brother\"...)",

        # AS script2:3630
        "I'm not s-shy...":
            "I'm not s-shy... It’s just a shirt after all, right...?",

        # AS script2:3631
        "It’s just a shirt after all, right...?":
            "I-It’s not like we haven't seen each other naked before...",

        # AS script2:3633
        "(I'm not sure where she’s going with all of this...)":
            "(Yeah, but... not since we last bathed together when we were nine.)",

        # AS script2:3634
        "(But I sure as hell want to find out...)":
            "(I'm not sure where she’s going with all of this... But I sure as hell want to find out...)",

        # AS script2:3642
        "(This doesn't seem like the Annie I’ve known since I was young... Is she trying to prove something?)":
            "(This doesn't seem like the sister I know... Is she trying to prove something?)",

        # AS script2:3644
        "(...No. You’re a woman now, Annie. It’s time to prove it to yourself... and prove it to [mc].) ":
            "(...No. You’re a woman now, Annie. It’s time to prove it to yourself... and prove it to your brother.)",

        # AS script2:3647
        "(Holy shit, I’ve never seen her in such an... intimate way...)":
            "(Holy shit, I never noticed know how much she grew over the past years...)",

        # AS script2:3652
        # BA/N: Disabled, name simply works better
        #"(This is really Annie... {i}my{/i} Annie.)":
        #    "(This is really Annie... {i}my{/i} sister.)",

        # AS script2:3658
        "We're just... friends getting a little more comfortable.":
            "We're just... siblings getting a little more comfortable.",

        # AS script2:3672
        "(My precious Annie...)":
            "(My precious little sister...)",

        # AS script2:3675
        "Um, [mc]...? Oh man, I must look weird or someth—":
            "Um, bro...? Oh man, I must look weird or someth—",

        # AS script2:3677
        "Annie... you are so... beautiful...":
            "Sis... you are so... beautiful...",

        # AS script2:3703
        "Your skin feels so soft, Annie. It feels... really nice holding you...":
            "Your skin feels so soft, sis. It feels... really nice holding you...",

        # AS script2:3711
        "(Oh my god, am I the only one feeling all this tension in the air? I want to make a move, but... I don’t want to overstep my bounds...)":
            "(Oh my god, am I the only one feeling all this tension in the air? I kind of want to make a move, but... I don’t want to overstep my bounds... I'm her brother, after all.)",

        # AS script2:3718
        "(But it’s not just any guy. It’s [mc].)":
            "(But it’s not just any guy. It’s [mc]. My twin brother!)",

        # AS script2:3719
        "(You've had a crush on him since you were nine years old. You’ve been fantasizing about this moment for so long. Now it’s finally here... what are you going to do about it?)":
            "(And despite that, you've had a crush on him since you were nine years old. You’ve been fantasizing about this moment for so long. Now it’s finally here... what are you going to do about it?)",

        # AS script2:3721
        "(But... I don't want to scare her away. Annie has always been so special to me. If I try something and it doesn't work out, I couldn’t bear the thought of losing her...)":
            "(But... I don't want to scare her away. Annie has always been so special – more than just a sister to me. If I try something and it doesn't work out, I couldn’t bear the thought of losing her...)",

        # AS script2:3729
        "(Baby steps, [mc]. Baby steps.)":
            "(A-And she's still my sister! It's just not right!)",

        # AS script2:3730
        "Goodnight, Annie.":
            "Goodnight, sis.",

        # AS script2:3732
        "G-Good night, [mc].":
            "G-Good night, bro.",

        # AS script2:3740
        "Um... Annie...?":
            "Um... sis...?",

        # AS script2:3746 {inject}
        "R-Really? W-Well... I guess that’s normal, given the circumstances.":[
            ("R-Really? W-Well... I guess that’s normal, given the circumstances.","script2:3746",[
                'a "It’s j-just a totally natural physical reaction."'
                ]),

            # Bonus Mod
            ("R-Really? W-Well... I guess that’s normal, given the circumstances.","script2:3795",[
                'a "It’s j-just a totally natural physical reaction."'
                ]),

            # Multi Mod
            ("R-Really? W-Well... I guess that’s normal, given the circumstances.","script2:3757",[
                'a "It’s j-just a totally natural physical reaction."'
                ]),
        ],

        # AS script2:3763
        "I’m sorry, Annie... I can’t help it... you’re driving me insane...":
            "I’m sorry, sis... I can’t help it... you’re driving me insane...",

        # AS script2:3776
        "Oh god, Annie...":
            "Oh god, sis...",

        # AS script2:3792
        "[mc]... Um, I don’t know if I’m ready to go all the way toni-":
            "B-bro... Um, I don’t know if I’m ready to go all the way toni-",

        # AS script2:3797
        "I’m sorry. I’m just a little nervous because no one has ever touched me there before, or even seen it, for that matter.":
            "I’m sorry. I’m just a little nervous because no one has ever touched me there before.",

        # AS script2:3800
        "[mc]. I said I’m nervous, but that doesn’t mean I... don’t want to...":
            "I said I’m nervous, brother, but that doesn’t mean I... don’t want to...",

        # AS script2:3823
        "I’ve never been more sure, Annie.":
            "I’ve never been more sure, sis.",

        # AS script2:3826
        "I thought you weren’t interested in me...":
            "I thought, as your sister, you'd never be interested in me...",

        # AS script2:3828
        # BA/N: borrowed from stepsis map
        "Where did you get that idea from?":
            "Oh Annie, you've never been just my sister.",

        # AS script2:3830
        "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our friendship.":
            "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our relationship as brother and sister.",

        # AS script2:3843
        "*Kissing her neck* And don’t you worry. I’m perfectly fine with going as slow as you want.":
            "*Kissing her neck* And don’t you worry, sis. I’m perfectly fine with going as slow as you want.",

        # AS script2:3845
        "Y-Yeah... m-much better. You’re so warm...":
            "Y-Yeah... m-much better. You’re so warm, bro...",

        # AS script:3854
        "You’re... so wet...":
            "Annie... You’re... so wet...",

        # AS script2:3865 {specific}, also overwrites script4:5819, script6:6414, script6:6556, script8:9636
        # Excludes script2:3905, script8:9293
        "Oh Annie...":[
            ("Oh sis...","script2:3865"),
            ("Oh sis...","script4:5819"),
            ("Oh sis...","script6:6414"),
            ("Oh sis...","script6:6556"),
            ("Oh sis...","script8:9636"),

            # Bonus Mod
            ("Oh sis...","script2:3914"),
            ("Oh sis...","script4:5880"),
            ("Oh sis...","script6:6454"),
            ("Oh sis...","script6:6596"),
            ("Oh sis...","script8:9767"),

            # Multi Mod
            ("Oh sis...","script2:3880"),
            ("Oh sis...","script4:5852"),
            ("Oh sis...","script6:6442"),
            ("Oh sis...","script6:6584"),
            ("Oh sis...","script8:9665"),
        ],

        # AS script2:3867
        "(Holy shit, this is really happening! I'm fucking Annie's thighs!)":
            "(Holy shit, this is really happening! I'm fucking my sister's thighs!)",

        # AS script2:3872
        "Jesus, Annie...":
            "Jesus, sis...",

        # AS script2:3924
        "Oh shit, I'm sorry, Annie...":
            "Oh shit, I'm sorry, sis...",

        # AS script2:3931
        "Did I do something wrong, Annie? I’m sorry! I didn’t know it was going to be that much!":
            "Did I do something wrong, sis? I’m sorry! I didn’t know it was going to be that much!",

        # AS script2:3942
        "I only came here t-to sleep and then... next thing I know I’m doing that...":
            "I only came here t-to sleep and then... next thing I know I’m doing that... with my brother...",

        # AS script2:3945
        "No, no! It's okay! You’re good! I like you, Annie! We can...":
            "No, no! It's okay! You’re good! I like you, sis! We can...",

        # AS script2:3952
        "We skipped like 14 steps! In one night!":
            "We skipped like 14 steps and broke a dozen rules! In one night!",

        # AS script2:3957
        "What will [mc] think of me after all of this?!":
            "What will my brother think of me after all of this?!",

        # AS script2:3965
        "I'm gonna... go... think! Good night [mc]!":
            "I'm gonna... go... think! Good night, bro!",

        # AS script2:3979
        "(Maybe something between us could work after all.)":
            "(Even if we're siblings, maybe something between us could work after all.)",

        # AS script2:3981
        "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing Annie’s secret kinky side... and I loved every moment of it!)":
            "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing my sister's secret kinky side... and I loved every moment of it!)",

        # AS script2:4474
        "Annie! Do you have a minute? I wanted to talk to you!":
            "Sis! Do you have a minute? I wanted to talk to you!",

        # AS script2:5094 (n)
        "Look at that perfectly toned stomach... And to think she's had 2 daughters! Unbelievable.":
            "Look at that perfectly toned stomach... And to think she's had 4 children! Unbelievable.",

        # AS script2:5364 (n)
        "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out.)":
            "(Even if, somehow, he wanted me too... and we ended up... doing it, the girls would be {i}furious{/i} if they ever found out. And fucking my son... God, there's so much that could go wrong for everyone...)",

        # AS script2:5413 (n)
        "(I bet if I tried to do anything at home, Dalia or Penny would surely notice.)":
            "(I bet if I tried to do anything at home, the girls would surely notice.)",

        # BA/N: also wanted to add a line about how Alex and MC are both twins but can't find a good place to fit it in

        # AS script2:5937 (x)
        "And on the first day of school, I saw him harassing a close friend of mine.":
            "And on the first day of school, I saw him harassing my twin sister.",

        # ========== START WIP ==========
            # BA/N: technically with Annie as sister, MC was never completely alone; Not sure how to fit that in while keeping the sentiment of the original.

        # BM script2:6102 (x)
        #"It probably doesn’t mean much, but I can sort of understand where you’re coming from.":
        #    "It probably doesn’t mean much, but I can sort of understand where you’re coming from.",

        # BM script2:6103 (x)
        #"I never met my mother and my father was always absent in my life. He was constantly too occupied with his work.":
        #    "My father was always absent in my life, always too occupied with his work. When my parents divorced, I had to live with him for the last ten years, if you can even call it \"living with him\".",

        # BM script2:6104 (x)
        #"I know what it's like to be alone.":
        #    "I know what it's like to feel alone.",

        # BM script2:6106 (x) {inject}
        #"Huh... I just assumed you were one of those pampered city boys that’s never known a hard day in his life...":[
        #    ("Oh right, you {i}are{/i} Dalia's brother...","script2:6106",[
        #        'x "Honestly, my first impression of you was that you were one of those pampered city boys that’s never known a hard day in his life..."'
        #    ]),

            # Bonus Mod script2:6170

            # Multi Mod script2:6122
        #],

        # ========== END WIP ==========


    # -----------------------------------------
    # v0.3 script3.rpy

        # AS script3:2877 (d)
        "And with Annie and you too? Now that’s what I call a party!":
            "And I never thought I'd be able to play with Annie and you too! A party with the entire family!",

        # AS script3:3343
        "Not a worry in mah noggin, homie. I just be... chillaxin’ all day! Yeahhhh...":
            "Not a worry in mah noggin, bro. I just be... chillaxin’ all day! Yeahhhh...",

        # AS script3:3362
        "Good morning, Annie!":
            "Good morning, sis!",

        # AS script3:3368
        "Um... Oh! [mc]! Good morning!":
            "Um... Oh! Bro! Good morning!",

        # AS script3:3392
        "But no biggie. I was scared. Not thinking clearly.":
            "But no biggie, bro. I was scared. Not thinking clearly.",

        # AS script3:3400
        "(She's right. Forgetting about this might be the best option right now.)":
            "(She's right. Forgetting about this might be the best option. We crossed way too many lines that night.)",

        # AS script3:3402
        "(That's all I want... just to stay friends with her.)":
            "(That's all I want... just to have a normal sibling relationship with her.)",

        # AS script3:3412
        "That sounds great. Take care, Annie!":
            "That sounds great. Take care, sis!",

        # AS script3:3414
        "Thank you, [mc]. I needed this talk.":
            "Thank you, bro. I needed this talk.",

        # AS script3:3420
        "*Taking a deep breath* (Well [mc], it's now or never. Time to grow a pair and man up!)":
            "*Taking a deep breath* (Well [mc], it's now or never. Time to grow a pair and man up! Let your sister know how you really feel.)",

        # AS script3:3423
        # BA/N: disabled, using name adds a bit of seriousness here
        #"I like you, Annie.":
        #    "I like you, sis.",

        # AS script3:3428
        "I've liked you ever since we were 10. If I’m being real with you, the only reason why I was willing to come back to Kredon at all was because you were coming too.":
            "And I mean I {i}like{/i} like you. I've felt this way since we were 10. If I’m being real with you, the only reason why I was willing to come back to Kredon at all was because you were coming too.",

        # AS script3:3431
        "You're my best friend.":
            "You're my twin sister.",

        # AS script3:3434
        "And in my heart I know, I want us to be so much more than that, too...":
            "So I know this is so, very wrong... but in my heart, I want us to be so much more than that.",

        # AS script3:3446
        "I don't want to lose our friendship, Annie. I’d be miserable without you in my life.":
            "I don't want to lose you, sis. I’d be miserable without you in my life.",

        # AS script3:3449
        "I just want us to stay friends forever!":
            "I just want us to be together forever!",

        # AS script3:3467
        "That sounds great! Just spending some time together as good friends. Like how we’ve always done it!":
            "That sounds great! Just some quality sibling bonding time. Like how we’ve always done it!",

        # AS script3:3483
        "Like... a fun date between friends?":
            "Like... a fun date with your sister?",

        # AS script3:3484
        "Hmmm... no, more like a date with a girl that I like. And I just happen to be so lucky in that, she’s also my best friend too. As for what the future holds? Who knows...":
            "Hmmm... no, more like a date with a girl that I like. Who just happens to be both my sister, and my best friend too. As for what the future holds? Who knows...",

        # AS script3:3505
        "Look, [mc], I know we’re going on a {i}date{/i} date, but I really do want to take it slow too. I don’t want you to assume that–":
            "Look, bro, I know we’re going on a {i}date{/i} date, but I really do want to take it slow too. I don’t want you to assume that–",

        # AS script3:3511
        "And not a word to anyone. I mean... there's no need for it, really. We’re just two people going on a date, and there’s no need to overthink it.":
            "We’re just two people going on a date, there’s no need to overthink it. But uh, not a word to anyone. Don't want others to think weird things...",

        # AS script3:3518
        "T-Thank you, [mc]. I needed this talk.":
            "T-Thank you, bro. I needed this talk.",

        # AS script3:3526
        "Um... yeah, I guess she does have that...":
            "Um... what's up with you and our sister's ass...?",

        # AS script3:3540
        # BA/N: borrowed from stepsis map
        "I know you want to take things slow. And I’m perfectly okay with that.":
            "I know you want to take things slow, sis. And I’m perfectly okay with that.",

        # AS script3:3561
        "That was quite the goodbye for just a couple of... friends.":
            "That was quite the goodbye for just... siblings.",

        # AS script3:3578
        "(Maybe a good movie? Or a walk along the beach. Or even a date in Eternum!)":
            "(Maybe a good movie? Or a walk along the beach. Or even a date in Eternum! We wouldn't have to worry about running into people who know us there.)",

        # AS script3:4828 (d)
        # BA/N: added Annie mention at start of flashback, also sets up for AS script3:5231
        "And it helps you grow up to be strong!":
            "Mommy said it's good for us! Helps us grow up to be strong!",

        # AS script3:4829 (d)
        "It’s good for you! Mommy told me!":
            "This is why you and Annie are such sleepyheads.",

        # AS script3:4918 (n)
        "(I'm not gonna be able to hold out much longer. They'll take the house from me if I don't get some sort of extra income this month. I can only fend off the bank for so long...)":
            "(I {i}need{/i} to be able to support Dalia and Penny by myself once the divorce is done. I already had to let him take the twins since I can't provide for all of them alone right now......)",

        # AS script3:4982
        "I... I know honey, but I don't have anyone else I can call on such short notice to take care of Dalia and [mc].":
            "I... I know honey, but I don't have anyone else I can call on such short notice to take care of the little ones.",

        # AS script3:5007
        "Do you have any idea how much I've sacrificed so that you and Dalia would never be left wanting?!":
            "Do you have any idea how much I've sacrificed so that you four would never be left wanting?!",

        # AS script3:5046
        "And... what about Dalia and [mc]?":
            "And... what about Dalia, Annie, and [mc]?",

        # AS script3:5105
        "Nothing... I’m just sad because in a couple of weeks, my dad will be bringing me with him to Europe.":
            "Nothing... I'm just sad because in a couple of weeks, Dad will be taking me and Annie with him to Europe.",

        # AS script3:5111
        "Well you can still come play with me after school, right?":
            "Well, maybe you two can come over to play with me after school?",

        # AS script3:5171
        "Absolutely! Don't worry sis, I'll protect you, [mc], and Mom!":
            "Absolutely! Don't worry sis, I'll protect you, and [mc], and Annie, and Mom too!",

        # AS script3:5228
        "But you got to bathe first!":
            "But you two got to bathe first! I can see the mud stains on you!",

        # AS script3:5230
        "Come on [mc], let's go to the bathroom.":
            "Where's Annie? She was playing with you outside earlier.",

        # AS script3:5231
        "Me too?!":
            "She got sleepy and went to bed.",

        # AS script3:5232
        "Yeah, let's go! We're all gonna bathe together!":
            "Already? Wake her up, she also needs to bathe first!",

        # AS script3:5233
        "But I'm not dirty!":
            "Okay!",

        # AS script3:5234
        "I can see the mud stains from here, mister!":
            "After that, we can all watch movies together!",

        # AS script3:9706
        "I owe it to my mother. It seems like once she reached 25, she stopped aging. She died shortly after Dalia was born, but she was always so full of life.":
            "I owe it to your grandma. It seems like once she reached 25, she stopped aging. She died shortly after Dalia was born. It's a shame she never got to met you and Annie, she was always so full of life.",

        # AS script3:9709
        "Dalia and Penelope are gonna be very blessed when they get older too.":
            "Annie, Dalia, and Penny are all gonna be very blessed when they get older too.",

        # AS script3:9761
        "What about Dalia and Penelope?":
            "What about... Dalia, Penelope, and Annie?",


    # -----------------------------------------
    # v0.4 script4.rpy

        # AS script4:4286
        "(I'm going on a date with [mc]!)":
            "(I'm going on a date with my brother!)",

        # AS script4:4339
        "*Chuckles* I think you're getting too excited about this, Annie. You need to relax. You'll enjoy it more if you take it less seriously!":
            "*Chuckles* I think you're getting too excited about this, sister. You need to relax. You'll enjoy it more if you take it less seriously!",

        # AS script4:4347
        "Chillin’ like a villain on penicillin, bro!":
            "Chillin’ like a villain on penicillin, yo!",

        # AS script4:4349
        "Gonna play some Eternum with ma' homie...":
            "Gonna play some Eternum with ma' bro...",

        # AS script4:4397
        "Send invitation... to... Annie Winters.":
            "Send invitation... to... Annie [lastname].",

        # AS script4:4411
        "Annie? Is that you?":
            "Sis? Is that you?",

        # AS script4:4621
        "Quick, [mc], make a wish!":
            "Quick, bro, make a wish!",

        # AS script4:4686
        "Let's watch Interstellar. It's one of my favorite movies, and I know you haven't seen it yet.":
            "Let's watch Interstellar, it's one of my favorite movies. It's the one I've been trying to get you to watch since you love sci-fi.",

        # AS script4:4687
        "With how much you love sci-fi, I'm sure you'll like it too!":
            "You were busy every time I wanted to watch it with you, so now's our chance!",

        # AS script4:4803
        # Overwritten by AS script:2952, okay
        # "Are you okay, Annie?" -> "Are you okay, sis?"

        # AS script4:4825
        "I can see why! I remember you talking about it, but I never got the chance to see it until now.":
            "I can see why! You were so right, I should've watched this sooner.",

        # AS script4:4915
        "I mean... of course we're not. We haven't even...":
            "I mean... of course we're not. We're still {i}just{/i} siblings, we haven't...",

        # AS script4:4926
        "*Chuckles* A likely story, Ms. Winters... I'll believe you, for now...":
            "*Chuckles* A likely story, dear sister... I'll believe you, for now...",

        # AS script4:4977
        "Come here, [mc]! Jump!":
            "Come here, bro! Jump!",

        # AS script4:4984
        "Have you ever done any scuba diving?":
            "We've never done any scuba diving?",

        # AS script4:4995
        # Overwritten by AS script2:2085, okay
        # "Right, Annie?" -> "Right, sis?"

        # AS script4:4997
        "Annie, you awake? I can go call the Astrocorp employee if we’re ready to wrap this up.":
            "Sis, you awake? I can go call the Astrocorp employee if we’re ready to wrap this up.",

        # AS script4:5004
        "You and Chang have always been my best friends, and neither of you played Eternum until recently, so... I've always felt kind of alone here.":
            "You and Chang have always been by my side, and neither of you played Eternum until recently, so... I've always felt kind of alone here.",

        # AS script4:5008
        "You’re the one who’s really made these first few weeks in Eternum worthwhile, Annie. I couldn't have asked for anyone better to spend time with.":
            "You’re the one who’s really made these first few weeks in Eternum worthwhile, sis. I couldn't have asked for anyone better to spend time with.",

        # AS script4:5108
        "How's life in Kredon so far?":
            "How's life back in Kredon so far?",

        # AS script4:5111
        "You were right, it's a rather small town, but there's everything you need!":
            "It's still a rather small town like I remembered, but there's everything we need!",

        # AS script4:5112
        "And I felt super welcome in our new home!":
            "And it really feels like we never left!",

        # AS script4:5113
        "Nancy, Penelope, and Dalia are all very nice to me. They treat me as one of the family. You know I’ve always wanted sisters, so I really feel like they’re giving me that experience!":
            "Mom, Penny, and Dalia are still so nice to me. You know I’ve always wanted to see our sisters again, so I really feel suuuuuper happy!",

        # AS script4:5129
        "Assets.":
            "Assets... I'm the only girl in the family without them!",

        # AS script4:5131
        "Oh! Come on, Annie! You can't be serious!":
            "Oh! Come on, sis! You can't be serious!",

        # AS script4:5216
        "*Jumps on the bed* Oh my god, [mc]! Look at this!":
            "*Jumps on the bed* Oh my god, bro! Look at this!",

        # AS script4:5250
        # BA/N: borrowed from stepsis map
        "(Maybe... it's just not the right time yet...?)":
            "(Maybe... was this all a mistake...?)",

        # AS script4:5311 (menu)
        # l9/N: Changed to be fully compatible with and without either walkthrough
        "Decline and stay as friends":
            "{color=[walk_path]}Decline and stay as siblings [red][mt](Closes Annie's path)",

        # AS script4:5314
        "I like you, and you're my best friend, you already know that.":
            "I like you, and you're my sister, you already know that.",

        # AS script4:5315
        "But... I also feel like we're not meant to be more than that. Things would get awkward if we tried to get together, and our friendship is too important to risk, for me at least.":
            "But... I also feel like we're not meant to be more than that. Things would get {i}so{/i} complicated if we tried to get together, and our relationship is too important to risk, for me at least.",

        # BA/N: next 7 lines borrowed and modified from stepsis map, which rewrote them to be a bit more emotional which I agree with, but tried to keep more of the original lines in it than the stepsis map did.

        # AS script4:5316
        "I just like spending time with you!":
            "I'm still your brother and I'll always be there for you, but...",

        # AS script4:5317
        "I... I think we're meant to be friends. Best friends!":
            "I... I don't think we're meant to be anything more than siblings.",

        # AS script4:5318
        "So... let's just stay like this for now, okay?":
            "So... let's just go back to what we always were, okay?",

        # AS script4:5319
        "I just don’t have those feelings for you right now.":
            "I can’t commit to this... {i}thing{/i} between us. Not right now. ",

        # AS script4:5320
        "In the future... who knows? Maybe. But I don’t want to lead you on, either.":
            "In the future... I don’t know. Maybe. But I don’t want to lead you on, either.",

        # AS script4:5326
        "No worries! I totally understand. My head has been all over the place too, you know, with all this back and forth...":
            "It's not your fault, Annie, it's mine. I know I've been sending you mixed signals, bringing you here today. My head has been all over the place too, you know, with all this back and forth... You don't deserve that.",

        # AS script4:5327
        "We can have this conversation again after we gather the 10 Gems!":
            "I'm sorry, sis. This isn't how I wanted today to go. For what it's worth, I still enjoyed spending this time with you.",

        # AS script4:5369
        "Y-Yeah... It's been like... 10 years since we first met?":
            "Y-Yeah...",

        # AS script4:5371
        "That’s quite a while... No big deal.":
            "No big deal.",

        # AS script4:5382
        "You're so pretty, Annie...":
            "You're so pretty, sis...",

        # AS script4:5395
        "[mc]! What are you doing?!":
            "Bro! What are you doing?!",

        # AS script4:5405
        "Seeing you undressing just for me was hot as fuck, Annie.":
            "Seeing you undressing just for me was hot as fuck, sis.",

        # AS script4:5436
        "But... Do you think I'm NOT nervous? I'm super scared too! I mean, in my arms, I'm holding an adorably precious, absolutely gorgeous girl whom I’ve liked for years.":
            "But... Do you think I'm NOT nervous? I'm super scared too! I mean, in my arms, I'm holding my adorably precious, absolutely gorgeous twin sister whom I’ve liked for years.",

        # AS script4:5438
        "I know it's scary to get out of your comfort zone, but... I think we can overcome it together.":
            "I know it's terrifying thing we're trying, starting a relationship as siblings, but... I think we can overcome it together.",

        # AS script4:5442
        "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay friends!":
            "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and just be siblings again!",

        # AS script4:5443
        "It’ll be a little awkward at first, but our friendship is strong, and I know we’d be back to normal in no time.":
            "It’ll be a little awkward at first, but our relationship is strong, and I know we’d be back to normal in no time.",

        # AS script4:5471
        "*Caressing her cheek* I feel like I could never get enough of you, Annie...":
            "*Caressing her cheek* I feel like I could never get enough of you, sis...",

        # AS script4:5494
        "Is that so? What have you been thinking about, exactly, Ms. Winters?":
            "Is that so? What have you been thinking about, exactly, Ms. [lastname]?",

        # AS script4:5518
        "Have I been fooled all these years? Innocent, shy Annie is actually a horny, perverted little girl?":
            "Have I been fooled all these years? My innocent, shy little sister is actually a horny, perverted little girl?",

        # AS script4:5526
        "God, there are so many things I want to do to Annie right now... but it's still Annie. I don't wanna cross any line too fast.":
            "God, there are so many things I want to do to Annie right now... but she is still my sister. I don't wanna cross any line too fast.",

        # AS script4:5528
        "You're making me so horny, Annie...":
            "You're making me so horny, sis...",

        # AS script4:5562
        "It'll only get better from here, babe...":
            "It'll only get better from here, Annie...",

        # AS script4:5604
        "*Panting* K-Keep going, [mc]! Y-You’re hitting just the... r-right spot!":
            "*Panting* K-Keep going, bro! Y-You’re hitting just the... r-right spot!",

        # AS script4:5621
        "Y-You have to stop! S-STOP! [mc]!":
            "Y-You have to stop! S-STOP! [mc!u]!",

        # AS script4:5624
        "Don't worry, babe...":
            "Don't worry, sis...",

        # AS script4:5665
        "([mc] made me... {i} cum{/i}!)":
            "(My brother made me... {i} cum{/i}!)",

        # AS script4:5675
        "You turn me on so much, Annie... I'd be lying if I said I wasn’t rock-hard the whole time...":
            "You turn me on so much, sis... I'd be lying if I said I wasn’t rock-hard the whole time...",

        # AS script4:5721
        "That's it, baby...":
            "That's it, sis...",

        # AS script4:5724
        "You’re such a good girl, Annie...":
            "You’re such a good girl, sis...",

        # AS script4:5753
        "D-Do you like beating off my cock, Annie?":
            "D-Do you like beating off my cock, sis?",

        # AS script4:5765
        "*Panting* F-Fuck, I won't last much longer, Annie...":
            "*Panting* F-Fuck, I won't last much longer, sis...",

        # AS script4:5767
        "I want to make you cum, [mc]... You were so kind to me...":
            "I want to make you cum, bro... You were so kind to me...",

        # AS script4:5819
        # Overwritten by AS script2:3865, okay
        # "Oh Annie..." -> "Oh sis..."

        # AS script4:5823
        "I want you so bad, Annie... I can’t wait ‘til the day you can finally take this dick... But not yet...":
            "I want you so bad, sis... I can’t wait ‘til the day you can finally take this dick... But not yet...",

        # AS script4:5825
        "W-We’ve g-gotta do some practicing b-beforehand, [mc]...":
            "W-We’ve g-gotta do some practicing b-beforehand, bro...",

        # AS script4:6106
        "My date left the room and went to the canteen, and a few minutes later... the lights went out and everyone had disappeared!":
            "My si- my date left the room and went to the canteen, and a few minutes later... the lights went out and everyone had disappeared!",

        # AS script4:6902
        # Overwritten by AS script:6179, okay
        # "Annie?!" -> "Hey, sis?!"

        # AS script4:6924
        "Oh Annie... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?":
            "Oh sis... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?",

        # AS script4:6942
        "Look, Annie! A teleporter! We can get out of here!":
            "Look, sis! A teleporter! We can get out of here!",

        # AS script4:6952
        "*Pulling your shirt* [mc]...":
            "*Pulling your shirt* Bro...",

        # AS script4:6986
        "D-Don't look at him, Annie.":
            "D-Don't look at him, sis.",

        # AS script4:7014
        "*Whispering* O-Okay Annie...":
            "*Whispering* O-Okay sis...",

        # AS script4:7052
        "*Sobbing* [mc]?":
            "*Sobbing* [mc_dash]?",

        # AS script4:7054
        # BA/N: Disabled for seriousness
        #"D-Don't worry, Annie...":
        #    "D-Don't worry, sis...",

        # AS script4:7250
        "Thank you for an amazing day, [mc].":
            "Thank you for an amazing day, bro.",

        # AS script4:7252
        "I'm glad you enjoyed it, Annie. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.":
            "I'm glad you enjoyed it, sis. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.",

        # AS script4:7429
        "Oh, already?! Good luck, [mc]! Be sure to get plenty of information!":
            "Oh, already?! Good luck, bro! Be sure to get plenty of information!",

        # AS script4:7431
        "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what best friends do, I guess.":
            "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what brothers do, I guess.",

        # AS script4:7467
        "I can help you out if you want, ma'am.":
            "I can help you out if you want, Mom.",

        # AS script4:7468
        "I don't know Aunt Cordelia, but I'm good at making collages.":
            "I don't remember Aunt Cordelia very well, but I'm good at making collages.",

        # AS script4:7473
        "Thank you Annie!":
            "Thank you, sweetie! You've grown into such a good girl!",


    # -----------------------------------------
    # v0.5 script5.rpy

        # AS script5:809
        # BA/N: tried reworking "best friends" bit, idk if it works
        "The scholarship that was granted to [mc] and his best friends is the best thing that has happened to me in a very long time.":
            "The scholarship that was granted to my twins and their best friend is the best thing that has happened to me in a very long time.",

        # AS script5:811
        "*Clears throat* I think it's best not to dig too deep into the \"best friend\" subject.":
            "*Clears throat* I think it's best not to bring up the \"best friend\" subject.",

        # AS script5:842
        "I don't really mind anymore. I'm happy being just a good friend.":
            "I don't really mind anymore. I'm happy just being his sister.",

        # AS script5:903
        "We won’t fail you, Nancy! No stone will be left unturned!":
            "We won’t fail you, Mom! No stone will be left unturned!",

        # AS script5:1005
        "B-Bye, [mc]! I'll see you at home!":
            "B-Bye, bro! I'll see you at home!",

        # AS script5:2044
        "I mean, Dad has only called me once since I got here.":
            "I mean, Dad has only called us once since we got here. Our grandparents called every other week.",

        # AS script5:4455 chat:517
        "I've been shopping all day with Nancy and I had no signal!":
            "I've been shopping all day with Mom and I had no signal!",

        # AS script5:4455 chat:544
        "Nancy's gonna wonder what's taking me so long {image=images/MENUS/e_blush2.png}":
            "Mom's gonna wonder what's taking me so long {image=images/MENUS/e_blush2.png}",

        # AS script5:4455 chat:548
        "Shopping with Nancy {image=images/MENUS/e_blush.png}":
            "Shopping with Mom {image=images/MENUS/e_blush.png}",

        # AS script5:9633
        # Disabled, interferes with other lines, also doesn't work if not on other paths
        # "I like where this is going...":
        #     "I like where this is going... and I am too horny to care that she is my sister... as if I had cared with Mom, Dalia, or Annie...",

        # AS script5:10045 (p)
        "*Snorts* You're such a dork. You’re lucky I think you’re cute.":
            "*Snorts* You’re such a dork, my cute little brother. I think you have enough twins in your life already.",

        # AS script5:12484 (n)
        "I have two girls, Dalia and Penelope.":
            "I have three girls and one son, Dalia, Penelope, Annie, and [mc] here.",


    # -----------------------------------------
    # v0.6 script6.rpy

        # AS script6:229 (d)
        "Truth is, you do look really good, Annie!":
            "Truth is, you do look really good, sis!",

        # AS script6:243
        "Private Annie Winters reports!":
            "Private Annie [lastname] reports!",

        # AS script6:249 (a)
        "T-Thank you, sir, ma'am, sir.":
            "T-Thank you, Mo-sir, ma'am, sir.",

        # AS script6:655 (p)
        "Nice job, Annie!":
            "Nice job, lil sis!",

        # AS script6:1674 {inject}
        # working in why annie didn't go too, elaborated later on
        "I thought I'd be way more homesick.":[
            ("I thought I'd be way more homesick.","script6:1674",[
                'show ep 41',
                'a "I told you you booked it too soon!" with dis',
                'show ep 40',
                'mc "Yeah, I might’ve rushed a bit since the ticket was cheap."'
            ]),

            # Bonus Mod
            ("I thought I'd be way more homesick.","script6:1684",[
                'show ep 41',
                'a "I told you you booked it too soon!" with dis',
                'show ep 40',
                'mc "Yeah, I might’ve rushed a bit since the ticket was cheap."'
            ]),

            # Multi Mod
            # script6:1674, same as original
        ],

        # AS script6:1678
        "How was your father?":
            "How was Dad?",

        # AS script6:1767
        "Wow, how come you don’t get this excited when you're playing with your beloved sister?":
            "Wow, how come you don’t get this excited when you're playing with your beloved older sister?",

        # AS script6:1785
        "Good night!!":
            "Good night bro!!",

        # AS script6:1804
        "Right now? With Penelope, Dalia, and Annie in the house?":
            "Right now? With your sisters in the house?",

        # AS script6:1975
        "[mc]...? What are you doing here?!":
            "Bro...? What are you doing here?!",

        # AS script6:2004
        "It's just... that... well, I was shocked at first since we had {i}never{/i} seen each other naked, and all that.":
            "It's just... that... well, I was shocked at first since the last time I saw you naked was {i}so long{/i} ago.",

        # AS script6:2008 (no)
        "A bit striking because I {i}never{/i} saw you naked before either.":
            "A bit striking because I {i}never{/i} saw you naked before.",

        # ========== START Murder Mystery ==========
            # adding this just to note that this section is organized by script line, and does not really reflect the order the events actually play out in game

        # AS script6:3524
        "What? Annie?":
            "What? Sis?",

        # AS script6:3536
        "Elementary, my dear [mc].":
            "Elementary, my dear brother.",

        # AS script6:3689
        "Well, you should still get it, [mc].":
            "Well, you should still get it, bro.",

        # AS script6:4970
        "We're just... friends.":
            "Delilah's just... a friend. And Annie's my sister.",

        # AS script6:4975
        "Are you seriously telling me you have those two fun-sized cuties around you and you're not doing anything with them?":
            "What a shame. I couldn't imagine having these two fun-sized cuties around me and not doing anything with them.",

        # AS script6:5473
        "Um... Annie? We have a problem.":
            "Um... Sis? We have a problem.",

        # AS script6:5474
        "Wow, come here, [mc]!":
            "Wow, come here, bro!",

        # AS script6:5504
        "Oh, thanks for the reassurance, [mc]! I feel much, much better now!":
            "Oh, thanks for the reassurance, brother! I feel much, much better now!",

        # AS script6:5523
        "Can you focus and stop being a pig?!":
            "Can you focus and stop being a pervert?!",

        # AS script6:5739 (a) {specific}
        # Excludes script:3745 (d), script3:734 (no)
        "[mc]!!":[
            ("Bro!!","script6:5739"),

            # Bonus Mod
            ("Bro!!","script6:5775"),

            # Multi Mod
            ("Bro!!","script6:5767"),
        ],

        # ========== END Murder Mystery ==========

        # AS script6:5970
        "*Knocking on the door* Annie?":
            "*Knocking on the door* Sis?",

        # AS script6:6012
        "B-But thank you.":
            "B-But thank you, bro.",

        # AS script6:6014
        "Penelope has been teaching me different ways to style it too.":
            "Penny has been teaching me different ways to style it too.",

        # AS script6:6026 {inject}
        # adding why Annie didn't go with you
        "*Eating another cookie* Mm-yeah, people mentioned how much my hair had grown during my visit too.":[
            ("*Eating another cookie* Mm-yeah, people mentioned how much my hair had grown during my visit too.","script6:6026",[
                'mc "They were also really surprised that you didn’t come with me."',
                "show eaa 11",
                'a "*Laughs* True, I don’t think we’ve been apart for this long before."',
                'a "Sorry to make you go alone, but I knew I wouldn’t be ready to go back so soon."',
                "show eaa 10",
                'mc "Nah, you were right about that. Though was kind of interesting to be completely on my own for once."',
            ]),

            # Bonus Mod
            ("*Eating another cookie* Mm-yeah, people mentioned how much my hair had grown during my visit too.","script6:6064",[
                'mc "They were also really surprised that you didn’t come with me."',
                "show eaa 11",
                'a "*Laughs* True, I don’t think we’ve been apart for this long before."',
                'a "Sorry to make you go alone, but I knew I wouldn’t be ready to go back so soon."',
                "show eaa 10",
                'mc "Nah, you were right about that. Though was kind of interesting to be completely on my own for once."',
            ]),

            # Multi Mod
            ("*Eating another cookie* Mm-yeah, people mentioned how much my hair had grown during my visit too.","script6:6054",[
                'mc "They were also really surprised that you didn’t come with me."',
                "show eaa 11",
                'a "*Laughs* True, I don’t think we’ve been apart for this long before."',
                'a "Sorry to make you go alone, but I knew I wouldn’t be ready to go back so soon."',
                "show eaa 10",
                'mc "Nah, you were right about that. Though was kind of interesting to be completely on my own for once."',
            ]),
        ],

        # AS script6:6031 {inject}
        "I don't care if I find discounted plane tickets again, I have no reason to go back there.":[
            ("I don't care if I find discounted plane tickets again, I have no reason to go back there.","script6:6031",[
                "show eaa 11",
                'a "Ouch. I’m telling Grandpa and Grandma that next time they call."',
                "show eaa 10",
                'mc "*Laughs* Okay, maybe two reasons."'
            ]),

            # Bonus Mod
            ("I don't care if I find discounted plane tickets again, I have no reason to go back there.","script6:6069",[
                "show eaa 11",
                'a "Ouch. I’m telling Grandpa and Grandma that next time they call."',
                "show eaa 10",
                'mc "*Laughs* Okay, maybe two reasons."'
            ]),

            # Multi Mod
            ("I don't care if I find discounted plane tickets again, I have no reason to go back there.","script6:6059",[
                "show eaa 11",
                'a "Ouch. I’m telling Grandpa and Grandma that next time they call."',
                "show eaa 10",
                'mc "*Laughs* Okay, maybe two reasons."'
            ]),
        ],

        # AS script6:6033
        "And how was your dad?":
            "And how was Dad?",

        # AS script6:6035
        "My dad...?":
            "Dad...?",

        # AS script6:6050
        "Tell Na-":
            "Tell Annie and Na-",

        # AS script6:6063
        "So... yeah, you know how my father is.":
            "So... yeah, you know how Dad is. Couldn’t even get his own kids’ names right...",

        # AS script6:6065
        "Awh, I'm so sorry, [mc]...":
            "Awh, I'm so sorry, bro...",

        # AS script6:6066
        "I can’t imagine how that must’ve felt after traveling all that way.":
            "That must've really hurt to hear now that we’ve reunited with them.",
            #"I know a part of us is always hoping to get a bit more from him.",

        # AS script6:6087 (menu)
        "You know dads can be real assholes":
            "You know Dad can be a real asshole",

        # AS script6:6088
        "You know as well as I do that dads can be real assholes.":
            "You know as well as I do that Dad can be a real asshole.",

        # AS script6:6090
        "W-Well... it's true that my dad has been working a lot all his life and he's been a bit absent, but... he's always cared about me.":
            "W-Well... it’s true that Dad’s always been pretty absent because of work, but...",

        # AS script6:6091
        "And he thinks highly of you!":
            "We still had our grandparents! And Chang’s parents too!",

        # AS script6:6093
        "Well... yeah, I guess that's different.":
            "Well... yeah. At least we had some adults looking out for us. Even if we didn't see them very often.",

        # AS script6:6094
        "That came out wrong, I'm sorry.":
            "Grandpa and Grandma miss you by the way.",

        # AS script6:6096
        "No worries! I know you didn't mean it in a bad way.":
            "I miss them too! I'll need make it up to them sometime.",

        # AS script6:6190
        "*Laughs* Don't be so dramatic.":
            "*Laughs* Don't be so dramatic, sis.",

        # AS script6:6215 {specific}
        # Excludes script:8614 (n)
        "Good night, [mc]!":[
            ("Good night, bro!","script6:6215"),

            # Bonus Mod
            ("Good night, bro!","script6:6253"),

            # Multi Mod
            ("Good night, bro!","script6:6243"),
        ],

        # AS script6:6218 {specific}
        # Excludes script6:5866 (no) and script6:3453 (mc)
        "Good night, Annie!":[
            ("Good night, sis!","script6:6218"),

            # Bonus Mod
            ("Good night, sis!","script6:6256"),

            # Multi Mod
            ("Good night, sis!","script6:6246"),
        ],

        # AS script6:6256
        "Y-You know what I mean!":
            "N-No, I just– y-you know what I mean!",

        # AS script6:6278
        # Disabled for impact
        #"You need to be more direct, Annie.":
        #    "You need to be more direct, sis.",

        # AS script6:6338
        "I’ll never get tired of seeing your gorgeous body, Annie.":
            "I’ll never get tired of seeing your gorgeous body, sis.",

        # AS script6:6399
        "I... I'm n-not sure I'm ready, [mc].":
            "I... I'm n-not sure I'm ready, bro.",

        # AS script6:6414
        # Overwritten by AS script2:3865, okay
        # "Oh Annie..." -> "Oh sis..."

        # AS script6:6426
        "I’m dying to taste you, Annie.":
            "I’m dying to taste you, sis.",

        # AS script6:6427
        "[mc], I... I-I'm not sure if I'm ready for that either!":
            "Brother, I... I-I'm not sure if I'm ready for that either!",

        # AS script6:6440
        "Oh [mc]... that feels...":
            "Oh brooo... that feels...",

        # AS script6:6450
        "You begin to taste every inch of Annie, spreading her tight lips as you gracefully move your tongue back and forth.":
            "You begin to taste every inch of your twin sister, spreading her tight lips as you gracefully move your tongue back and forth.",

        # AS script6:6454
        "Oh my god, [mc]...":
            "Oh my god, bro...",

        # AS script6:6471
        "[mc]. . . . . . . . . . .  . !":
            "Broooo. . . . . . . . . . .  . !",

        # AS script6:6486
        "AAaahh... oh god [mc]... I think I'm gonna... C-CUM...":
            "AAaahh... oh god bro... I think I'm gonna... C-CUM...",

        # AS script6:6488
        "[mc]! You’re gonna make me...":
            "Bro! You’re gonna make me...",

        # AS script6:6556
        # Overwritten by AS script2:3865, okay
        # "Oh Annie..." -> "Oh sis..."

        # AS script6:6559
        "I can feel you pulsing, [mc]...":
            "I can feel you pulsing, bro...",

        # AS script6:6605
        "Yeah... keep going... suck it as hard as you can, babe...":
            "Yeah... keep going... suck it as hard as you can, sister...",

        # AS script6:6627
        "*Panting* Annie...?":
            "*Panting* Sis...?",

        # AS script6:6644
        "You grab Annie's head and start fucking her mouth. You can hear her choking with each thrust, but Annie's throat willingly takes all of you.":
            "You grab your sister's head and start fucking her mouth. You can hear her choking with each thrust, but Annie's throat willingly takes all of you.",

        # AS script6:6657
        "The sweet, innocent, little girl I've known for years...":
            "My sweet, innocent, little twin sister...",
            #"The sweet, innocent, little girl I've known my entire life...",

        # AS script6:6666
        "Come on Annie, you're gonna miss the entire movie!":
            "Come on sis, you're gonna miss the entire movie!",

        # AS script6:6681
        "AAAAargh... fuck, Annie...":
            "AAAAargh... fuck, sis...",

        # AS script6:6687
        "You better take care of my little girl while you're in the USA, [mc].":
            "You better take care of your sister while you're in the USA, [mc].",
        
        # AS script6:6688
        "Rest assured Mr. Winters, I won’t let anything happen to her!":
            "Rest assured Grandpa, I won’t let anything happen to her!",

        # AS script6:6689
        "I'll take care of Annie as if she was my sister!":
            "I'll always take care of Annie!",

        # AS script6:6700
        "Oh GOD, Annie, I'm gonna fucking cum!":
            "Oh GOD, sis, I'm gonna fucking cum!",

        # AS script6:6718
        "*Panting* Do it... empty y-yourself all over me, [mc]...":
            "*Panting* Do it... empty y-yourself all over me, bro...",

        # AS script6:6719
        "Oh god Annie, I'm...":
            "Oh god sis, I'm...",

        # AS script6:6750
        "Goddammit Annie... that was mind-blowing.":
            "Goddammit sis... that was mind-blowing.",

        # AS script6:6757
        "Well, I'm sure Dalia and Penelope would knock before entering your room.":
            "Well, I'm sure Dalia and Penny would knock before entering your room.",

        # AS script6:6762
        "Imagine if Nancy had caught us... she'd kick us out of the house!":
            "Imagine if Mom had caught us... she'd go feral! We'd be kicked out a-and maybe even disowned!",

        # AS script6:6766
        "Why would she? We weren't doing anything wrong.":
            "She loves us too much to do anything like that.",

        # AS script6:6770 base map override
        "Don't be nasty!":
            "Don't be nasty!",

        # AS script6:6787
        "Good night, Annie.":
            "Good night, sis.",

        # ========== START Fuck Marry Kill ==========

        # AS script6:10185 (d)
        "And then I'd fuck... Annie.":
            "And then I'd marry... Annie.",

        # AS script6:10185 (d)
        "She's so cute. She’s small, but... in a hot way. You know what I mean?":
            "She’s so small and cute. Imagine having that adorable girl by your side all the time... though I suppose you already know what that’s like.",

        # AS script6:10185 (d)
        "You said fuck twice.":
            "You said marry twice.",

        # ========== END Fuck Marry Kill ==========


    # -----------------------------------------
    # v0.7 script7.rpy

        # AS script7:1461
        "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, Annie.":
            "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, sis.",

        # AS script7:1468 {specific}
        # Excludes script:7779 (eva)
        "Thank you, [mc]...":[
            ("Thank you, bro...","script7:1468"),

            # Bonus Mod
            ("Thank you, bro...","script7:1480"),

            # Multi Mod
            # script7:1468, same as original
        ],

        # AS script7:1502
        "Are you sure you don't want to join us, Annie?":
            "Are you sure you don't want to join us, sis?",

        # AS script7:1622
        "Give my best to Penny when you see her too.":
            "Give my best to big sis when you see her too.",

        # AS script7:1635
        "Penny? We literally have dinner together every day." :
            "Big sis? We literally have dinner together every day." ,

        # AS script7:1640
        "Take care, Annie.":
            "Take care, sis.",

        # ========== START harem thoughts ==========

        # AS script7:7396 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7396",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7452",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7454",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),
        ],

        # AS script7:7398 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7398",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7454",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7456",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),
        ],

        # AS script7:7400 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7400",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7456",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7458",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # AS script7:7402 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7402",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7458",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7460",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # AS script7:7404 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7404",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7460",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7462",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),
        ],

        # AS script7:7425 {inject}
        # BA/N: technically this wouldn't work if you're not on any of the incest routes but don't feel like making a labelmod to add if statement just for this
        #    but also why would you be playing an incest mod without following at least one incest path right?
        "I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?":[
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7425",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),

            # Bonus Mod
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7481",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),

            # Multi Mod
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7483",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),
        ],

        # ========== END harem thoughts ==========

        # AS script7:8196 (p)
        "(How would we even explain this to Mom or Dalia?)":
            "(How would we even explain this to Mom, or Dalia, or Annie?)",

        # AS script7:9816 (p)
        "*Panting* I want Mom and Dalia to hear me scream...":
            "*Panting* I want the whole family to hear me scream...",


    # -----------------------------------------
    # v0.8 script8.rpy

        # AS script8:4222
        "Come on, [mc], I need you to catch on quickly! We're running out of time.":
            "Come on, bro, I need you to catch on quickly! We're running out of time.",

        # AS script8:4231
        "Thank you for making me look so adorable!":
            "Thank you for making me look so adorable, bro!",

        # AS script8:4278
        #"There's no time to hesitate, [mc]!":
        #    "There's no time to hesitate, bro!",

        # AS script8:5558 (n)
        "How are you still tight after giving birth to two children...?":
            "How are you still tight after giving birth to four children...?",

        # AS script8:6521 (n)
        "If you ever hurt Nova, Annie, Luna, or Alex... I'll be seriously mad at you, young man.":
            "If you ever hurt Nova, Luna, or Alex... I'll be seriously mad at you, young man.",

        # AS script8:6523 (n)
        "Oh, and if you EVER hurt Penny or Dalia...":
            "Oh, and if you EVER hurt Penny, Dalia, or Annie...",

        # AS script8:6910
        "Oh, no, no, no. Penny, Dalia, and Nancy were not an option.":
            "Oh, no, no, no. Penny, Dalia, and Mom were not an option.",

        # AS script8:6969
        "(She's definitely going on a date with [mc].)":
            "(She's definitely going on a date with [mc]. Her own twin brother!)",

        # AS script8:6983 (l)
        # BA/N: leaving this here for the future when we learn what exactly Luna's vision was
        # "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)":
        #     "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)",

        # AS script8:7092
        "It's straightforward yet stylish, giving off a confident vibe. It shows you're not desperate but also considerate enough to dress well for a date with someone who's been your second-best friend for so many years.":
            "It's straightforward yet stylish, giving off a confident vibe. It shows you're not desperate but also considerate enough to dress well for a date with someone who's been your second-best friend your entire life.",

        # AS script8:7098
        # Original non-inject version for safekeeping
        #"Hey, don’t sweat it. I already told you, it gives you a mysterious, sexy vibe.":
        #    "Hey, don’t sweat it. I already told you, it gives you a mysterious, sexy vibe.{p}And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.",

        # AS script8:7099
        # Original non-inject version for safekeeping
        #"And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.":
        #    "Which is still strange to think about since you’re twins, but... You two mean a lot to me, and I know how much you mean to each other.{p}So, I just want to tell you again that I’ll always support you two.",

        # AS script8:7099 {inject}
        "And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.":[
            ("And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.","script8:7099",[
                "show gf 35",
                'c "Which is still {i}really{/i} strange to think about since you’re actual twins, but..."',
                'c "Honestly, I probably could’ve seen it coming. I know how first-hand just much you two mean to each other."',
                "show gf 36",
                'c "So I just want to tell you again that you and Annie are my best friends, and I’ll always support you two." with dis08',
            ]),

            # Bonus Mod
            ("And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.","script8:7208",[
                "show gf 35",
                'c "Which is still {i}really{/i} strange to think about since you’re actual twins, but..."',
                'c "Honestly, I probably could’ve seen it coming. I know how first-hand just much you two mean to each other."',
                "show gf 36",
                'c "So I just want to tell you again that you and Annie are my best friends, and I’ll always support you two." with dis08',
            ]),

            # Multi Mod
            ("And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.","script8:7127",[
                "show gf 35",
                'c "Which is still {i}really{/i} strange to think about since you’re actual twins, but..."',
                'c "Honestly, I probably could’ve seen it coming. I know how first-hand just much you two mean to each other."',
                "show gf 36",
                'c "So I just want to tell you again that you and Annie are my best friends, and I’ll always support you two." with dis08',
            ]),
        ],

        # AS script8:7101 {specific}
        # Excludes script4:2443 (d). original backup line saved just in case
        "*Chuckles* If you say so...":[
            ("*Chuckles* Thanks, man. I appreciate it a lot. I'm sure Annie would, too.","script8:7101"),
            #"*Chuckles* Thanks, bro. I appreciate it.",

            # Bonus Mod
            ("*Chuckles* Thanks, man. I appreciate it a lot. I'm sure Annie would, too.","script8:7210"),

            # Multi Mod
            ("*Chuckles* Thanks, man. I appreciate it a lot. I'm sure Annie would, too.","script8:7129"),
        ],

        # AS script8:7205
        #"[mc], over here!":
        #    "Bro, over here!",

        # AS script8:7209
        "Ah, hey there!":
            "Ah, hey there, sis!",

        # AS script8:7398
        "Annie Winters and Luna Hernandez travel to the super scary Red Herring server and complete–":
            "Annie [lastname] and Luna Hernandez travel to the super scary Red Herring server and complete–",

        # AS script8:7532
        "I'll show them to Nancy later so I can–":
            "I'll show them to Mom later so I can–",

        # AS script8:7569
        "A-Annie...?":
            "Uh sis...?",

        # AS script8:7622
        "*Turning around* Um... Annie...":
            "*Turning around* Um... sis...",

        # AS script8:7696
        "No one ever thought you were useless, Annie. But after this? D-Damn, even less so.":
            "No one ever thought you were useless, sis. But after this? D-Damn, even less so.",

        # AS script8:7713
        "Bye, bye, [mc]!":
            "Bye, bye, bro!",

        # AS script8:7778
        "Why...? Come on, [mc], you've met up with Annie solo a hundred times, why the jitters now?!":
            "Why...? Come on, [mc], you always have dinner with Annie, why the jitters now?!",

        # ========== START label mod "menurestaurant_mod" backup ==========
            # Full replacement label to rewrite the flashback with Annie in the UK.
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

        # AS script8:8159 {specific}
        # Excludes script5:1198 (l)
        "Hi [mc].":[
            ("Hi Chang.","script8:8159"),

            # Bonus Mod
            ("Hi Chang.","script8:8278"),

            # Multi Mod
            ("Hi Chang.","script8:8187"),
        ],

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
            "He's calling a bunch of people to help Dad with the papers and stuff.",

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

        # AS script8:8384
        "Sure thing! It's one Penelope recommended me.":
            "Sure thing! It's one Penny recommended me.",

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

        # ========== END label mod "menurestaurant_mod" backup ==========

        # AS script8:8450
        "Alright, tell me about the first birthday we celebrated together, a couple of years after that.":
            "Alright, tell me what happened on our tenth birthday.",

        # AS script8:8455 {inject}
        "We couldn’t celebrate your birthday because you were sick, so we decided to do a joint birthday celebration three weeks later at Chang’s parents' restaurant.":[
            ("Dad tried to be considerate for once and plan us a big party, but in the end he didn't have the time to do anything.","script8:8455",[
                'a "So we had a late birthday celebration three weeks later at Chang’s parents’ restaurant."'
            ]),

            # Bonus Mod
            ("Dad tried to be considerate for once and plan us a big party, but in the end he didn't have the time to do anything.","script8:8580",[
                'a "So we had a late birthday celebration three weeks later at Chang’s parents’ restaurant."'
            ]),

            # Multi Mod
            ("Dad tried to be considerate for once and plan us a big party, but in the end he didn't have the time to do anything.","script8:8483",[
                'a "So we had a late birthday celebration three weeks later at Chang’s parents’ restaurant."'
            ]),
        ],

        # AS script8:8497
        "D-Darn it, [mc].":
            "D-Darn it, bro.",

        # AS script8:8569
        "After all these years, I think I can read you pretty well.":
            "We've been together our whole lives, I think I can read you pretty well.",

        # AS script8:8617
        "Your answer could shape how the rest of tonight goes and... maybe even your relationship with Annie.":
            "Your answer could shape how the rest of tonight goes and... maybe even your relationship with your sister.",

        # AS script8:8769
        #"*Standing up* Are you alright, Annie?":
        #    "*Standing up* Are you alright, sis?",

        # AS script8:8791
        "Nancy, Penny, Dalia, Luna, Alex, Nova...":
            "Luna, Alex, Nova, even Mom, Penny, and Dalia...",

        # AS script8:8839
        #"I’m sorry, Annie. I swear I didn't–":
        #    "I’m sorry, sis. I swear I didn't–",

        # AS script8:8845
        "I'm so impressed, Annie.":
            "I'm so impressed, sis.",

        # AS script8:8938
        "Dalia, Penny, Nancy, Luna, Nova, Alex...":
            "Dalia, Penny, Mom, Luna, Nova, Alex...",

        # AS script8:9084
        "Annie Winters.":
            "Annie [lastname].",

        # AS script8:9155
        "The way you’re tracing your finger on my chest is kind of turning me on more than it should, Annie...":
            "The way you’re tracing your finger on my chest is kind of turning me on more than it should, sis...",

        # AS script8:9200
        "After so many years thinking I’d never be more than friends with Annie... it's finally happening.":
            "After so many years thinking we’d never be more than siblings... it's finally happening.",

        # AS script8:9225
        "Phew... you sure know how to drive me crazy, Annie.":
            "Phew... you sure know how to drive me crazy, sister.",

        # AS script8:9275
        "You climb on top of Annie, trailing passionate kisses along her neck as she moans softly in appreciation.":
            "You climb on top of your sister, trailing passionate kisses along her neck as she moans softly in appreciation.",

        # AS script8:9292
        "You take a moment to contemplate Annie's plump, virgin pussy lips.":
            "You take a moment to contemplate your sister's plump, virgin pussy lips.",

        # AS script8:9313
        "*Moans* Ohh mmmm-y-yes, [mc]...":
            "*Moans* Ohh mmmm-y-yes, brother...",

        # AS script8:9382, also overwrites script8:9494
        "*Tracing Annie's figure* Oh, babe...":
            "*Tracing Annie's figure* Oh, sis...",

        # AS script8:9451
        "*Sobbing* Maybe we're just not compatible.":
            "*Sobbing* Maybe... maybe this is a sign that it was wrong for us to be together after all.",

        # AS script8:9515
        "*Panting* Ohh, [mc]...":
            "*Panting* Ohh, bro...",

        # AS script8:9530
        "You’ve got me all kinds of messed up with how great you look, Annie...":
            "You’ve got me all kinds of messed up with how great you look, sis...",

        # AS script8:9540
        #"Oh, trust me, you've seen nothing yet, my love...":
        #    "Oh, trust me, you've seen nothing yet, sis...",

        # AS script8:9543
        "I-I can't handle this unbearable teasing anymore, Annie...":
            "I-I can't handle this unbearable teasing anymore, sis...",

        # AS script8:9559 {specific}
        # Excludes other lines (x)(no)(l)
        # with necessary overrides to keep dalia lines
        "Oh babe...":[
            ("Oh sis...","script6:10790"), #dalia
            ("Oh sis...","script6:10811"), #dalia
            ("Oh sis...","script8:9559"), #annie

            # Bonus Mod
            ("Oh sis...","script6:10867"), #dalia
            ("Oh sis...","script6:10888"), #dalia
            ("Oh sis...","script8:9690"), #annie

            # Multi Mod
            ("Oh sis...","script6:10821"), #dalia
            ("Oh sis...","script6:10842"), #dalia
            ("Oh sis...","script8:9588"), #annie
        ],

        # AS script8:9583 {inject} WIP
        #"*Moans* I can feel it...":[
        #    ("*Moans* I can feel it...","script8:9583",[
        #        'a "*Giggles* We’re finally connected..."'
        #    ]),
        #],

        # AS script8:9591
        "You're doing great, babe...":
            "You're doing great, sis...",

        # AS script8:9614
        "Oh babe, y-you feel so good...":
            "Oh Annie, y-you feel so good...",

        # AS script8:9636
        # Overwritten by AS script2:3865, okay
        # "Oh Annie..." -> "Oh sis..."

        # AS script8:9639
        "*Panting* I-I'm cumming, [mc]...":
            "*Panting* I-I'm cumming, bro...",

        # AS script8:9696
        "Not really, but that's not an exact science. You know that.":
            "Not really, but that's not an exact science. Plus we’re siblings, so we especially can’t be taking risks.",

        # AS script8:9872
        "You thrust deeply into Annie once more, letting yourself be engulfed by her warmth as your hands explore her, memorizing every ridge and curve of her body.":
            "You thrust deeply into your sister once more, letting yourself be engulfed by her warmth as your hands explore her, memorizing every ridge and curve of her body.",

        # AS script8:9944
        "My perfect, beautiful, innocent little Miss Winters...":
            "My perfect, beautiful, innocent little twin sister...",

        # AS script8:9964
        "*Panting* F-Fuck, me too, babe...":
            "*Panting* F-Fuck, me too, sis...",

        # AS script8:9974
        #"*Panting* I WANT... YOUR... S-S-SEED INSIDE OF ME...":
        #    "*Panting* I WANT... MY BROTHER'S... S-S-SEED INSIDE OF ME...",

        # AS script8:9999
        "T-That was... almost a religious experience, Annie.":
            "T-That was... almost a religious experience, sis.",

        # AS script8:10057
        "You came over and helped me study, even though you missed a football game with some other kids from school because of it.":
            "You stayed home and helped me study, even though you missed a football game with some other kids from school because of it.",

        # AS script8:10069
        "B-But I've liked you since the day I met you!":
            "B-But I've always liked you!",


    # -----------------------------------------
    # v0.9 script9.rpy

        # AS script9:167 (p)
        "Is there anything better than spending time with my favorite sister?":
            "Is there anything better than spending time with one of my precious little sisters?",

        # AS script9:432 (p)
        "*Grumbling to herself* I had a feeling something was going on between him and Nova. Or Annie. Or even Luna, for that matter!":
            "*Grumbling to herself* I had a feeling something was going on between him and Nova. Or Alex. Or even Luna, for that matter!",

        # AS script9:527 (n)
        "*Yawns* Agh, what's with all this noise so early in the morning, girls? You're gonna wake up Annie.":
            "*Yawns* Agh, what's with all this noise so early in the morning, girls? You're gonna wake up your sister.",

        # AS script9:553 (p)
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

        # AS script9:3123 (d)
        "First, her sister. Oh, what a {i}coincidence{/i}, the last person to see [mc].":
            "First, your other sister. Oh, what a {i}coincidence{/i}, the last person to see [mc].",

        # AS script9:3267
        "*Standing up* No! Didn't you hear Nancy?!":
            "*Standing up* No! Remember what your mom said?!",

        # AS script9:3272
        "I can't live without him, Nova.":
            "I don't know how to live without him, Nova.",

        # AS script9:9919
        # Original non-inject version
        #"Annie flew back to the UK a few days ago to spend Christmas with her family and all, but she’s gonna be back before New Year’s Eve.":
        #    "Annie flew back to the UK a few days ago. Our grandparents invited us over for Christmas for the first time since we were kids.{p}Annie accepted their invite, but I already saw them when I went back recently so I'm staying here. She’s gonna be back before New Year’s Eve.",

        # AS script9:9919 {inject}
        "Annie flew back to the UK a few days ago to spend Christmas with her family and all, but she’s gonna be back before New Year’s Eve.":[
            ("Annie flew back to the UK a few days ago to spend Christmas with our grandparents. They haven’t been able to invite us over for the holidays since we were kids, so Annie took them up on the offer.","script9:9919",[
                'mc "I already saw them when I went back to the UK, so I’m staying here this time. Annie’s gonna be back before New Year’s Eve."'
            ]),

            # Bonus Mod
            ("Annie flew back to the UK a few days ago to spend Christmas with our grandparents. They haven’t been able to invite us over for the holidays since we were kids, so Annie took them up on the offer.","script9:9983",[
                'mc "I already saw them when I went back to the UK, so I’m staying here this time. Annie’s gonna be back before New Year’s Eve."'
            ]),

            # Multi Mod
            ("Annie flew back to the UK a few days ago to spend Christmas with our grandparents. They haven’t been able to invite us over for the holidays since we were kids, so Annie took them up on the offer.","script9:9927",[
                'mc "I already saw them when I went back to the UK, so I’m staying here this time. Annie’s gonna be back before New Year’s Eve."'
            ]),
        ],

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
            "But I really gotta go now or grandpa will get mad {image=images/MENUS/e_tongue2.png}",

        # AS script9:12870
        "I’ve never had a Christmas dinner like this before, Nan.":
            "I wish Annie was here for this, she's missing out on quite the feast!",

        # AS script9:12871
        "Feels really special.":
            "We’ve never had a Christmas dinner like this before, Mom. Feels really special.",
    }

    annie_only_sister_map = {
        # -----------------------------------------
        # Annie is MC’s twin sister, no incest with Nancy, Penny, Dalia.
        # Annie has same last name as MC
        # Annie’s father and mother mentions converted to paternal grandparents
        #     MC's grandparents canonically exist in UK (script6:1392)
        # Original map, reworked from full incest map
        # -----------------------------------------
        # Character Notes
        # Annie has been playing for 3 years (script:8183)
        # MC and Annie are close, using bro/sis often
        # revert to names when being more serious
        # -----------------------------------------
        # OS script:0000 = Only Sister map, RPY file:Line Number
        #     Numbers based on v0.9.5, subject to change in future updates
        # Tags based who the line is about contextually, not always the speaker.
        # Selectively applied for clarification
        # (menu) = Choice menu line
        # (mc) = MC line
        # (n) = Nancy line
        # (p) = Penelope line
        # (d) = Dalia line
        # (a) = Annie line
        # (x) = Alex line
        # (l) = Luna line
        # (no) = Nova line
        # (ca) = Calypso line
        # -----------------------------------------
        # Code tags
        # {specific} = use of Variant 2 to target specific lines
        # {inject} = use of Variant 3 to inject new lines      
        # -----------------------------------------
        # LW/N = Lucifer_W's notes
        # l9/N = l9453394's notes
        # BA/N = BlueArrow's notes
        # -----------------------------------------

    # -----------------------------------------
    # v0.1 script.rpy

        # OS script:948
        "My name is [mc] [lastname]. I was born in the city of Kredon, a relatively small town on the west coast of the United States.":
            "My name is [mc] [lastname]. I was born as a twin in the city of Kredon, a relatively small town on the west coast of the United States.",

        # OS script:950
        "My mother left shortly after I was born and my dad was never around much because he was always so focused on his job.":
            "My mother left shortly after my twin and I were born and my dad was never around much because he was always so focused on his job.",

        # OS script:957
        "He had to work to support us both. Heaven knows where I'd be without him.":
            "He had to work to support the three of us. Heaven knows where we'd be without him.",

        # OS script:1046
        "(Annie is a close friend from my childhood.)":
            "(Annie is my younger twin sister.)",

        # OS script:1047
        "(When I moved from Kredon, she was my next-door neighbor and the first person I met, along with Chang.)":
            "(When we moved from Kredon, all we had were each other until we met Chang.)",
        
        # OS script:1048
        "(We quickly bonded after discovering we both had something in common... the absence of our parents.)":
            "(We found out our grandparents also lived in the UK. They loved to pamper us when they could, but rarely were able to visit.)",

        # OS script:1049
        "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them.)":
            "(With our father always off working, it was pretty much just the two of us at home most of the time.)",

        # OS script:1050
        "(We were both lost... and lonely.)":
            "(We gave each other stability in those lonely times.)",

        # OS script:1051
        "(After finding a companion within each other, we’ve been inseparable ever since.)":
            "(As cliche as it may be for twins, we've naturally become inseparable ever since.)",

        # OS script:1053
        "(Because of how close we were, people always believed we were dating... but the truth is, we're just friends.)":
            "(Because of how close we were, people liked to joke that we would've make a great couple... but the truth is, we're just siblings.)",

        # OS script:1054
        "(I mean… she's cute, and we love spending time with each other, but I've never tried to make a move on her.)":
            "(. . .)",

        # OS script:1055 {inject}
        "(I could never do it.)":[
            ("(Well... she is cute... and we love spending time with each other...)","script:1055",[
                'mc "(I mean, if–){nw=0.8}"'
            ]),

            # Bonus Mod
            ("(Well... she is cute... and we love spending time with each other...)","script:1092",[
                'mc "(I mean, if–){nw=0.8}"'
            ]),

            # Multi Mod
            # script:1055, same as original
        ],

        # OS script:1056
        "(She'd probably freak out if I did.)":
            "(NO.{w=0.5} Stop it.{w=1} She'd probably freak out if I did.)",

        # OS script:1059
        "(It would be... weird for us. Yeah! That's the word. Weird.)":
            "(It would be... wrong. Very wrong! We're twins after all.)",

        # OS script:1060
        "(It's just not the kind of relationship we have.)":
            "(Why am I even thinking about this!?)",

        # OS script:1080
        "I can't wait to see her. I hope she recognizes me.":
            "I can't wait to see her. I hope she recognizes us.",

        # OS script:1085
        "(Nancy used to be my babysitter in Kredon. Since my father was always working, I can recall more memories with her than with my dad.)":
            "(Nancy used to be our babysitter in Kredon. Since our father was always working, I can recall more memories with her than with our dad.)",

        # OS script:1086
        "(I used to spend the entire afternoon playing with Nancy and her daughter Dalia, but then we had to move and ended up losing touch.)":
            "(We used to spend the entire afternoon playing with Nancy and her daughter Dalia, but then we had to move and ended up losing touch.)",

        # OS script:1089
        "(Come to find out, she actually had 2 rooms available, so Annie will have a place to stay as well!)":
            "(Come to find out, she actually had 2 rooms available, so Annie and I could stay together!)",

        # OS script:1090
        "(She’s actually been the one who’s been coordinating with Nancy over the phone, even though they didn’t know each other beforehand.)":
            "(Annie’s actually been the one who’s been coordinating with Nancy over the phone, I didn't have to do anything.)",

        # OS script:1093
        "Do you think she will like me?":
            "I'm really excited, do you think everything will go well?",

        # OS script:1095
        "Nancy? Of course!":
            "Don't worry sis, it'll be alright.",

        # OS script:1096
        "Don't worry about it, Annie. I haven't seen her in over 10 years, so it’ll probably feel like I’m meeting her for the first time too!":
            "And anyways, it's not like it's a stranger we're meeting, it's our old babysitter.",

        # OS script:1157
        "You should go to sleep too, Annie. We have to wake up early tomorrow.":
            "You should go to sleep too, sis. We have to wake up early tomorrow.",

        # OS script:1179
        "You're nothing but a big ball of envy because your best friend can play Eternum and you can't since you didn't save any money.":
            "You're nothing but a big ball of envy because your dear sister and bestie can play Eternum and you can't since you didn't save any money.",

        # OS script:1184
        "B-Best friend?":
            "B-Bestie?",

        # OS script:1220
        "But that doesn't mean you aren’t also my best friend, Annie!":
            "But that doesn't mean you aren’t also my best friend, Annie! And my precious twin sister!",

        # OS script:1241
        "We've been through too much together, Annie.":
            "We've literally been together since birth, sis.",

        # OS script:1254
        "You're my best... male friend!":
            "You're my best... male friend! Basically my brother!",

        # OS script:1262
        "Ahh, it's a deal, my friend!":
            "Ahh, it's a deal, bro!",

        # OS script:1339
        "Hello everyone! Annie is here!":
            "Hello everyone! Annie is back!",

        # OS script:1344
        "I know you're excited Annie, but I'd appreciate it if you could at least carry your hand baggage!":
            "I know you're excited sis, but I'd appreciate it if you could at least carry your hand baggage!",

        # OS script:1347
        "It's just that I'm excited to discover the town where you grew up!":
            "It's just that I'm excited to be in our hometown again!",

        # OS script:1348
        "Well, I left this place when I was 8, so I don’t really remember anything.":
            "Well, I understand, but we left this place when we were 8, so I don't really remember anything.",

        # OS script:1363
        "I’ve never had a chance to come back ‘til now, so I'm excited to relive all my childhood memories!":
            "We’ve never had a chance to come back ‘til now, so I'm excited to relive all our childhood memories!",

        # OS script:1757
        "Mission failed, [mc]...":
            "Mission failed, bro...",

        # OS script:1762
        "You must be Annie!":
            "Annie! Come here and let me see that adorable face!",

        # OS script:1763 (n)
        "Is that right?!":
            "It's been so long!",

        # OS script:1765
        "You're even cuter than I imagined! Your voice matches your appearance so much!":
            "You're even cuter than when I last saw you. You've grown so much!",

        # OS script:1766 (a)
        "T-Thank you, miss.":
            "T-Thank you, Nancy.",

        # OS script:1767
        "It’s me, Nancy! Even though we’ve only been speaking on the phone for the past few days, I feel like we’ve been becoming good friends already! Isn't that right, Annie?":
            "It's so good to see the two of you after all these years.",

        # OS script:1769 (a)
        "Definitely! I’d say we’ve been hitting it off pretty well!":
            "Same here, Nancy!",

        # OS script:1770 (a)
        "It's so nice to finally meet you!":
            "It's so nice to finally see you again!",

        # OS script:1777 (a)
        "No worries, miss! I'm sure it'll be more than enough!":
            "No worries, Nancy! I'm sure it'll be more than enough!",

        # OS script:1779
        "I hope so! And please, just call me Nancy!":
            "I sure hope so!",

        # OS script:1781
        "Okay! Thank you, Nancy!":
            "I remember your rooms being pretty spacious when we stayed over.",

        # OS script:1783
        "Have you ever been to the USA before, Annie?":
            "*Laughs* You two were also much smaller back then. Do you remember your time in the USA, Annie?",

        # OS script:1785
        "Never! But I’ve always wanted to visit. [mc] has always spoken very well of his time in Kredon.":
            "Kind of, but it's been so many years.",

        # OS script:1786
        "And of his babysitter!":
            "But I do remember all the fun we had playing together!",

        # OS script:1790
        "Yeah, since my Dad was constantly working, I've always said you were like a parent to me.":
            "Yeah, since our Dad was constantly working, we've always said you were like a parent to us.",

        # OS script:1793
        "Now I work in a laboratory, but back then I was still finishing my thesis. Thankfully [mc]'s father came along and offered me the babysitting gig.":
            "Back then I was still finishing my thesis. Thanks to your father offering me the babysitting gig, I had the flexibility to take care of my daughters at the same time.",

        # OS script:1794
        "It was not only well-paid, but also allowed me the flexibility to take care of my daughters at the same time. And for me, being a single mother, that was essential.":
            "Since you left, I've started working in laboratory. It pays pretty well.",

        # OS script:1796
        "You have 2 daughters, right?":
            "That's great! So how are your daughters doing?",

        # OS script:1798
        "Yes, Dalia and Penelope. Penny was a little older when I was [mc]'s nanny, so she used to play on her own, but Dalia got very close to him!":
            "They're both doing well! Penelope's in college and Dalia will going to school with you. I remember the the two of you and Dalia were very close as children.",

        # OS script:1802
        "But then, after my daughters grew up, I was able to start a better job within a local company.":
            "Yes... in the beginning I worked a lower-paying job but now that those two are older, I was able to start a better job within a local company.",

        # OS script:1821
        "Alright then! Let's go to the car! Dalia and Penelope are dying to see you again!":
            "Alright then! Let's go to the car! Dalia and Penelope are dying to see you two again!",

        # ========== START label mod "welcome_mod" ==========
            # line numbers for both files 

        # OS script:1842 IncestLables:23
        "(Nancy used to pick me up after school and we'd come here.)":
            "(Nancy used to pick us up after school and we'd come here.)",

        # OS script:1843 IncestLables:24
        "(Each day I would spend the afternoon playing with her and Dalia. We had dinner every night at eight, and then Nancy drove me home once it got late.)":
            "(Each day we would spend the afternoon playing with her and Dalia. We had dinner every night at eight, and then Nancy drove us home once it got late.)",

        # OS script:1845 IncestLables:26
        "(She would always call me on my birthday, but... aside from that, I never reached out. I have to make it up to her somehow.)":
            "(Nancy would always call us on our birthday, but... aside from that, I never reached out. I have to make it up to her somehow.)",

        # OS script:1858 (a)
        # replaced by IncestLables:39

        # OS script:1859 IncestLables:40
        "Do you like it, Annie?":
            "Do you remember it, Annie?",

        # OS script:1860 IncestLables:41
        "This place looks awesome! Are you rich?!":
            "Yes, this place looks just like I remember! It's so beautiful! ",

        # OS script:1861 IncestLables:42
        "*Laughs* No, I wish. Houses in Kredon are not that expensive.":
            "*Laughs* Thank you, sweetie.",

        # OS script:1862 IncestLables:43
        "It's beautiful! I'm used to living in a flat, so this looks like a palace to me!":
            "We're used to living in a flat, so this'll be like living in a palace! ",

        # OS script:1863 IncestLables:44
        "My husband and I bought it when I was pregnant with Dalia.":
            "Yes, it is a good home. My husband and I bought it when I was pregnant with Dalia.",

        # OS script:1868 IncestLables:49
        "You first, [mc]!":
            "You first, Annie!",

        # OS script:1876 IncestLables:57
        "That's cool! I love rainy days!":
            "Oh, I remember now, too! Guess that's why I've always loved rainy days!",

        # OS 1764 script:1888 IncestLables:69
        "Did you paint that?!":
            "Do you still paint?",

        # OS 1765 script:1889 IncestLables:70
        "Yeah, I used to paint in my free time, but I haven't done anything in years.":
            "No, I haven't done anything in years.",

        # OS script:1890
        # replaced by IncestLables:71

        # OS script:1894
        "*Laughs* And Penelope the preteen that was too \"cool\" to play with Dalia and me?":
            "*Laughs* And Penelope the preteen that was too \"cool\" to play with us younger kids?",

        # OS IncestLables:75 labelmod override
        "*Laughs* And Penelope the preteen that was too \"cool\" to play with her younger siblings?":
            "*Laughs* And Penelope the preteen that was too \"cool\" to play with us younger kids?",

        # OS script:1916 IncestLables:97
        "I wasn't expecting you to be so excited to meet [mc] again!":
            "I wasn't expecting you to be so excited to meet [mc] and Annie again!",

        # OS script:1928
        # replaced by IncestLables:109

        # OS script:1932 IncestLables:113
        "Oh, y-yeah, so excited! Hi [mc]!":
            "Oh, y-yeah, so excited! Hi Annie!",

        # OS IncestLables:117 labelmod override
        "So good to see you, sisters!":
            "So good to see you!",

        # OS script:1970 IncestLables:151
        "Oh, and you must be Annie! Nice to meet you too!":
            "Oh, and Annie! Nice to see you again!",

        # OS script:1972 IncestLables:153
        "Welcome to the family!":
            "Welcome to the family, you two!",

        # OS script:1983 IncestLables:164
        "Of course he doesn't mind!":
            "Of course they don't mind!",

        # OS script:2078 IncestLables:259
        "Annie, you must have gotten the wrong impression of my daughters...":
            "Still, I was hoping for us to have a warmer reunion...",

        # OS script:2080 IncestLables:261
        "Not at all! They both seem really nice!":
            "It's okay, Nancy! We have plenty of time to catch up in the days to come!",

        # OS script:2081 IncestLables:262
        "For tonight, I’d rather just unpack all my things and freshen up a bit. We have plenty of time to get to know each other in the days to come!":
            "For tonight, I’d rather just unpack all my things and freshen up a bit.",

        # OS script:2083 IncestLables:264
        "You're so nice, Annie. Is there anything I can do for you?":
            "That's nice of you to say, sweetie. Is there anything I can do for you?",

        # OS script:2119 IncestLables:300
        "Well, since [mc] seems to remember where everything is already... Do you want a tour of the house, Annie?":
            "Well, since [mc] doesn't want any supper... Do you want something to eat, Annie?",

        # OS script:2124 IncestLables:305
        "Goodnight [mc]! Sweet dreams!":
            "Goodnight, bro! Sweet dreams!",

        # ========== END label mod "welcome_mod" ==========

        # OS script:2407
        "Annie, Penelope, and Dalia have been up for a while!":
            "Your sister, Penelope, and Dalia have been up for a while!",

        # OS script:2436
        "(Although, I think I'll wait a couple of weeks. I don't want [mc] and Annie to think I'm a promiscuous woman or anything...)":
            "(Although, I think I'll wait a couple of weeks. I don't want the twins to think I've become a promiscuous woman or anything...)",

        # OS script:2760
        "That's what I said, but she told us she wanted to take a tour of the neighborhood.":
            "That's what I said, but she told us she really wanted to revisit the neighborhood.",

        # OS script:2762
        "Oh yeah, that sounds like Annie. I guess she already told you she also plays Eternum?":
            "Oh yeah, that sounds like my sister. I guess she already told you she also plays Eternum?",

        # OS script:2798
        "(Annie was always good at making friends.)":
            "(Like me, Annie was always good at making friends. Must run in our blood.)",

        # OS script:2799
        "(I guess I should let them walk to school on their own, since I don't wanna look like a jealous boyfriend or something.)":
            "(I guess I should let them walk to school on their own, since I don't wanna look like the cliche overprotective brother.)",

        # OS script:2826
        "Believe me, Kredon can seem like a very boring place until you’re able to discover it with someone that knows all the hotspots.":
            "Believe me, Kredon can seem like a very boring place unless you’re able to re-discover it with someone that knows all the hotspots.",

        # OS script:2830
        "*Laughs* Like what? I thought you just got here yesterday.":
            "*Laughs* Like what? I thought you just got back yesterday.",

        # OS script:2836
        "I know you're new around here, but you have no idea how lucky you are right now.":
            "I know you're basically new around here, but you have no idea how lucky you are right now.",

        # OS script:2910
        "The lady said no, buddy.":
            "Hands off my sister, you jerk.",

        # OS script:2934
        "The lady said no.":
            "Her brother. And she said no.",

        # OS script:2952, also overwrites script4:4803, okay
        "Are you okay, Annie?":
            "Are you okay, sis?",

        # OS script:2996
        "Will you be alright, Annie?":
            "Will you be alright, sis?",

        # OS script:3006
        "And... thank you again for helping me out back there, [mc].":
            "And... thank you again for helping me out back there, bro.",

        # OS script:5178
        "I don't know, it felt pretty special to me. I never had a nice, home-cooked meal when I was living with my dad.":
            "I don't know, it felt pretty special to me. Annie and I never really had a nice, home-cooked meal while we were living with our dad.",

        # OS script:5200
        "Tomorrow you'll finally be connected to Eternum, [mc]! After waiting for so many years!":
            "Tomorrow you'll finally be connected to Eternum, bro! After waiting for so many years!",

        # OS script:5331 (a)
        "Goodnight [mc]!!":
            "Goodnight, bro!!",

        # OS script:5583 (n)
        "(I mean... If Dalia and Penelope never found out, then would it really be so bad? It’d be our little secret...)":
            "(I mean... If the girls never found out, then would it really be so bad? It’d be our little secret...)",

        # ========== START label mod "preeternum_mod" backup ==========
            # Full replacement label with some line/image rearrangements
            # Rewrote because since they lived together in the UK, MC should already know some basics from how often Annie plays
            # Below is original draft/backup if mod does not trigger.

        # OS script:6093
        "Let's go! We're already late!":
            "Let's go, bro! We're already late!",

        # OS script:6094
        # interferes with script:7111 (a), the cause of switching to label mod but now that Variant 2 exists dont feel like changing it anymore lol
        #"*Laughs* What are you wearing?":
        #    "*Laughs* Already got your Eternum E-Suit on, huh?",

        # OS script:6095
        "No time for questions! Come on!":
            "It's the Eternum E-Suit, dummy! Now, come on already!",

        # OS script:6099
        "But seriously, what are you wearing?":
            "You always play in your room, so I forgot about the E-sui—Oh crap, I don't have one yet!",

        # OS script:6101
        "Eternum's official E-Suit, of course!":
            "It should've been included with the game.",

        # OS script:6102
        "Didn't you see all the stuff that was inside the game’s box??":
            "Did you look through everything in the box?",

        # OS script:6106
        "So... I have to wear that suit too?":
            "So... do I have to wear the entire thing?",

        # OS script:6115
        "Nah, I just wanted to show you how cool the suit looks.":
            "Nah, I just have it on so I can quickly jump in later.",

        # OS script:6124
        "You can look if you want...":
            "You can look if you want, sis...",

        # OS script:6147
        "Sorry! Did that hurt?!":
            "Sorry, bro! Did that hurt?!",

        # OS script:6179, also overwrites script:6728, script4:6902, both okay
        "Annie?!":
            "Hey, sis?!",

        # ========== END label mod "preeternum_mod" backup ==========

        # OS script:6511
        "(Dammit, Annie didn't tell me about any of this...)":
            "(Dammit, sis didn't tell me about any of this...)",

        # OS script:6606
        "By the way, your outfit looks awesome!":
            "By the way, your outfit looks awesome, sis!",

        # OS script:6695
        "No, he's not! He's [mc]! He's tough!":
            "No, he's not! He's my brother! He's tough!",

        # OS script:6697
        "So this is the [mc] you're always talking about?":
            "So this is the twin brother you're always talking about?",

        # OS script:6712
        "That's the thing, [mc]!":
            "That's the thing, bro!",

        # OS script:6728
        # Overwritten by OS script:6179, okay
        # "Annie?!" -> "Hey, sis?!"

        # OS script:6810
        "Thank god I have you, Annie... I’d probably be lost in a ditch somewhere without you!":
            "Thank god I have you, sis... I’d probably be lost in a ditch somewhere without you!",

        # OS script:6942
        "Thanks, Annie!":
            "Thanks, sis!",

        # OS script:6982
        "Alright. Thank you Annie!":
            "Alright. Thanks again, sis!",

        # OS script:7130
        "(That's a bad idea...)":
            "(Nope, bad idea. She's my sister!)",

        # OS script:7142, also overwrites script:7172
        "*Laughs* Don't get lost or get yourself into much trouble, alright?":
            "*Laughs* Don't get lost or get yourself into much trouble, alright bro?",

        # OS script:7176
        "(Jeez, I've always tried to not think of Annie in \"that\" way because I don't want to ruin our friendship, but now...)":
            "(Jeez, I {i}really{/i} need to stop this... but...)",

        # OS script:7179
        "(She's got curves in all the right places...)":
            "(She's not the skinny kid she used to be... she's got curves in all the right places now...)",

        # OS script:7186
        "(Damn... I guess she’s not the skinny kid she used to be...)":
            "(Dammit... Stop looking at your sister, [mc]...)",

        # OS script:7977
        "Oh... Come on Annie, it doesn't matter!":
            "Oh... Come on sis, it doesn't matter!",

        # OS script:8016, also overwrites script:8040
        "*Laughs* You always know how to make me laugh.":
            "*Laughs* You always know how to make me laugh, bro.",

        # OS script:8055
        "(Hehe, a little look won't hurt anyone...)":
            "(I guess a little look won't hurt anyone...)",

        # OS script:8102
        "Erm... Y-You're the best friend ever!":
            "Erm... Y-You're the best brother ever!",

        # OS script:8103
        "I'm glad you like it, Annie.":
            "I'm glad you like it, sis.",

        # OS script:8224
        # BA/N: Disabled for seriousness
        #"No. You have much more to lose, Annie.":
        #    "No. You have much more to lose, sis.",

        # OS script:8467
        "Thank you so much for playing with me, [mc]. It means a lot.":
            "Thank you so much for playing with me, bro. It means a lot.",

        # OS script:8468
        "The pleasure was all mine, Annie. Eternum is awesome. I’m so grateful I had you by my side.":
            "The pleasure was all mine, sis. Eternum is awesome. I’m so grateful I had you by my side.",


    # -----------------------------------------
    # v0.2 script2.rpy

        # OS script2:40
        "I have a feeling this shit is much bigger than we think, Annie.":
            "I have a feeling this shit is much bigger than we think, sis.",

        # OS script2:52
        "*Whispering* I don't like this, Annie...":
            "*Whispering* I don't like this, sis...",

        # OS script2:82
        "I don't know, Annie... him having a stroke? I'm not buying it.":
            "I don't know, sis... him having a stroke? I'm not buying it.",

        # OS script2:106
        "*Laughs* Don't mind him...":
            "*Laughs* Don't mind my brother...",

        # ========== START label mod "versiontwo_mod" ==========
            # edit of lines added by "versiontwo_mod"
        # REPLACED BY INJECTION, old code left just in case

        # OS IncestLables:2500
        #"Same to you. You must be Annie, [mc]'s told me about you.":
        #    "Same to you. You must be Annie, his twin sister. [mc]'s told me about you.",

        # OS IncestLables:2502
        #"Yep! I heard [mc] managed to win a neural implant at your cafe!":
        #    "Yep! I heard my brother managed to win a neural implant at your cafe!",

        # OS script2:112 {inject} (replaces labelmod)
        "It's so nice to meet you, Luna!":[
            ("It's so nice to meet you, Luna!","script2:112",[
                "scene aaa 15",
                'l "Same to you. You must be Annie, his twin sister. [mc]’s told me about you."',
                "scene aaa 14"
            ]),

            # Bonus Mod
            # script2:112, same as original

            # Multi Mod
            # script2:112, same as original
        ],

        # OS script2:113 used with inject
        "I heard [mc] managed to win a neural implant at your cafe!":
            "Yep! I heard my brother managed to win a neural implant at your cafe!",

        # ========== END label mod "versiontwo_mod" ==========

        # OS script2:113 disable if using inject
        #"I heard [mc] managed to win a neural implant at your cafe!":
        #    "I heard my brother managed to win a neural implant at your cafe!",

        # OS script2:126
        "Can I play with you guys, [mc]?!":
            "Can I play with you guys, bro?!",

        # OS script2:133
        "Horror? Okay... maybe it'd be better if you didn't join us, Annie.":
            "Horror? Okay... maybe it'd be better if you didn't join us, sis.",

        # OS script2:167
        "But you're not allowed to complain if you’re scared, Annie!":
            "But you're not allowed to complain if you’re scared, sis!",

        # OS script2:174
        "I'm sorry Annie, we both know you can't handle horror... no matter how light it is.":
            "I'm sorry sis, we both know you can't handle horror... no matter how light it is.",

        # OS script2:810
        "(Maybe his girlfriend...?)":
            "(Maybe his girlfriend... or his sister...?)",

        # OS script2:1014
        "Annie should be waiting for us already.":
            "Your sister should be waiting for us already.",

        # OS script2:1117
        "I love your outfit, Annie!":
            "I love your outfit, sis!",

        # OS script2:1389
        "Y-You're scaring me, [mc].":
            "Y-You're scaring me, bro.",

        # OS script2:1965
        "It's okay Annie, I know you’re not one for spooky things, but you’ve been doing good! I’m proud of you!":
            "It's okay sis, I know you’re not one for spooky things, but you’ve been doing good! I’m proud of you!",

        # OS script2:2051
        "Right, Annie?!":
            "Right, sis?!",

        # OS script2:2085, also overwrites script4:4995, okay
        "Right, Annie?":
            "Right, sis?",

        # OS script2:2187
        "(Then Luna will shower me with hugs and Annie will gush non-stop about how I'm the bravest man she's ever met.)":
            "(Then Luna will shower me with hugs and Annie will gush non-stop about how I'm the bravest man she's ever known.)",

        # OS script2:2905
        "What about you, Annie?":
            "What about you, sis?",

        # OS script2:3331
        "(He must think I'm a useless, scared kid...)":
            "(He must think I'm still a kid – a useless, scared kid...)",

        # OS script2:3339
        "(Yeah, nice job impressing [mc] in Eternum, Annie.)":
            "(Yeah, nice job impressing your brother in Eternum, Annie.)",

        # OS script2:3408
        "Oh, [mc]! I wasn’t sure if you were asleep already!":
            "Oh, hey bro! I wasn’t sure if you were asleep already!",

        # OS script2:3418
        "I told you! You shouldn't have played in Luna's server, Annie! You can't handle that scary stuff! Remember when we played Dead Space?":
            "I told you, sis! You shouldn't have played in Luna's server! You can't handle that scary stuff! Remember when we played Dead Space?",

        # OS script2:3474
        "You can sleep here as many times as you want. You don’t even have to ask, alright?":
            "You can sleep here as many times as you want. You don’t even have to ask, alright? Just like when we were little.",

        # OS script2:3479
        "Anytime, Annie.":
            "Anytime, sis.",

        # OS script2:3490
        "It is pretty nice!":
            "It is pretty nice! Do you remember how we'd play down there with Dalia when we were kids?",

        # OS script2:3491
        "My room faces the front yard. It’s a nice view too, but sometimes you can hear all the cars passing by.":
            "*Giggles* Yeah, we'd always get so muddy because of how much it rained. My room has a nice view of the front yard, but sometimes you can hear all the cars passing by.",

        # OS script2:3504
        "G-Goodnight, [mc].":
            "G-Goodnight, bro.",

        # OS script2:3506
        "Goodnight Annie.":
            "Goodnight sis.",

        # OS script2:3518
        "(Oh yeah... I forgot that Annie came to sleep in my room.)":
            "(Oh yeah... I forgot that sis came to sleep in my room.)",

        # OS script2:3526
        "(She's probably used to hugging a pillow while she sleeps, or something.)":
            "(She used to hug a pillow or stuffed animal while she sleeps. I guess that hasn't changed.)",

        # OS script2:3530
        "(We're in quite an... intimate position... I don't want her to think I'm trying to take advantage of her while she sleeps.)":
            "(We're in quite an... intimate position... I don't want her to think her brother is trying to take advantage of her while she sleeps.)",

        # OS script2:3545
        "A-Are you awake, Annie?":
            "A-Are you awake, sis?",

        # OS script2:3557
        "Baloo?":
            "Baloo? The teddy bear Nancy gave you when you were 5?",

        # OS script2:3559
        "Oh... Well... It's a stuffed bear that my mother gave me when I was 5, and...":
            "Yes, that Baloo...",

        # OS script2:3562
        "(Oh my god, why did I say that?! Now I probably sound like a child to him...)":
            "(Oh my god, why did I say that?! Now he probably thinks I'm still a child...)",

        # OS script2:3564
        "Oh... I didn't know about Baloo.":
            "Oh... I didn't know you still slept with Baloo.",

        # OS script2:3594
        "(He probably just sees me as the little girl who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)":
            "(He probably still sees me as his little sister who plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)",

        # OS script2:3595
        "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack.)":
            "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack. And not blood-related ones... he's not a weirdo like me who has feelings for her twin brother.)",

        # OS script2:3596
        "(I'll always just be Annie, the \"best friend\".)":
            "(I'll always just be Annie, the \"little sister\".)",

        # OS script2:3602
        "(I'm a fucking mess. She needs someone more mature.)":
            "(I'm a fucking mess. She needs someone more mature... And someone not blood-related... she's not a weirdo like me who has feelings for his twin sister.)",

        # OS script2:3607
        "(This is why I'll always just be [mc], the \"best friend\"...)":
            "(This is why I'll always just be [mc], the \"big brother\"...)",

        # OS script2:3630
        "I'm not s-shy...":
            "I'm not s-shy... It’s just a shirt after all, right...?",

        # OS script2:3631
        "It’s just a shirt after all, right...?":
            "I-It’s not like we haven't seen each other naked before...",

        # OS script2:3633
        "(I'm not sure where she’s going with all of this...)":
            "(Yeah, but... not since we last bathed together when we were nine.)",

        # OS script2:3634
        "(But I sure as hell want to find out...)":
            "(I'm not sure where she’s going with all of this... But I sure as hell want to find out...)",

        # OS script2:3642
        "(This doesn't seem like the Annie I’ve known since I was young... Is she trying to prove something?)":
            "(This doesn't seem like the sister I know... Is she trying to prove something?)",

        # OS script2:3644
        "(...No. You’re a woman now, Annie. It’s time to prove it to yourself... and prove it to [mc].) ":
            "(...No. You’re a woman now, Annie. It’s time to prove it to yourself... and prove it to your brother.)",

        # OS script2:3647
        "(Holy shit, I’ve never seen her in such an... intimate way...)":
            "(Holy shit, I never noticed know how much she grew over the past years...)",

        # OS script2:3652
        # BA/N: Disabled, name simply works better
        #"(This is really Annie... {i}my{/i} Annie.)":
        #    "(This is really Annie... {i}my{/i} sister.)",

        # OS script2:3658
        "We're just... friends getting a little more comfortable.":
            "We're just... siblings getting a little more comfortable.",

        # OS script2:3672
        "(My precious Annie...)":
            "(My precious twin sister...)",

        # OS script2:3675
        "Um, [mc]...? Oh man, I must look weird or someth—":
            "Um, bro...? Oh man, I must look weird or someth—",

        # OS script2:3677
        "Annie... you are so... beautiful...":
            "Sis... you are so... beautiful...",

        # OS script2:3703
        "Your skin feels so soft, Annie. It feels... really nice holding you...":
            "Your skin feels so soft, sis. It feels... really nice holding you...",

        # OS script2:3711
        "(Oh my god, am I the only one feeling all this tension in the air? I want to make a move, but... I don’t want to overstep my bounds...)":
            "(Oh my god, am I the only one feeling all this tension in the air? I kind of want to make a move, but... I don’t want to overstep my bounds... I'm her brother, after all.)",

        # OS script2:3718
        "(But it’s not just any guy. It’s [mc].)":
            "(But it’s not just any guy. It’s [mc]. My twin brother!)",

        # OS script2:3719
        "(You've had a crush on him since you were nine years old. You’ve been fantasizing about this moment for so long. Now it’s finally here... what are you going to do about it?)":
            "(And despite that, you've had a crush on him since you were nine years old. You’ve been fantasizing about this moment for so long. Now it’s finally here... what are you going to do about it?)",

        # OS script2:3721
        "(But... I don't want to scare her away. Annie has always been so special to me. If I try something and it doesn't work out, I couldn’t bear the thought of losing her...)":
            "(But... I don't want to scare her away. Annie has always been so special – more than just a sister to me. If I try something and it doesn't work out, I couldn’t bear the thought of losing her...)",

        # OS script2:3729
        "(Baby steps, [mc]. Baby steps.)":
            "(A-And she's still my sister! It's just not right!)",

        # OS script2:3730
        "Goodnight, Annie.":
            "Goodnight, sis.",

        # OS script2:3732
        "G-Good night, [mc].":
            "G-Good night, bro.",

        # OS script2:3740
        "Um... Annie...?":
            "Um... sis...?",

        # OS script2:3746 {inject}
        "R-Really? W-Well... I guess that’s normal, given the circumstances.":[
            ("R-Really? W-Well... I guess that’s normal, given the circumstances.","script2:3746",[
                'a "It’s j-just a totally natural physical reaction."'
                ]),

            # Bonus Mod
            ("R-Really? W-Well... I guess that’s normal, given the circumstances.","script2:3795",[
                'a "It’s j-just a totally natural physical reaction."'
                ]),

            # Multi Mod
            ("R-Really? W-Well... I guess that’s normal, given the circumstances.","script2:3757",[
                'a "It’s j-just a totally natural physical reaction."'
                ]),
        ],

        # OS script2:3763
        "I’m sorry, Annie... I can’t help it... you’re driving me insane...":
            "I’m sorry, sis... I can’t help it... you’re driving me insane...",

        # OS script2:3776
        "Oh god, Annie...":
            "Oh god, sis...",

        # OS script2:3792
        "[mc]... Um, I don’t know if I’m ready to go all the way toni-":
            "B-bro... Um, I don’t know if I’m ready to go all the way toni-",

        # OS script2:3797
        "I’m sorry. I’m just a little nervous because no one has ever touched me there before, or even seen it, for that matter.":
            "I’m sorry. I’m just a little nervous because no one has ever touched me there before.",

        # OS script2:3800
        "[mc]. I said I’m nervous, but that doesn’t mean I... don’t want to...":
            "I said I’m nervous, bro, but that doesn’t mean I... don’t want to...",

        # OS script2:3823
        "I’ve never been more sure, Annie.":
            "I’ve never been more sure, sis.",

        # OS script2:3826
        "I thought you weren’t interested in me...":
            "I thought, as your sister, you'd never be interested in me...",

        # OS script2:3828
        # BA/N: borrowed from stepsis map
        "Where did you get that idea from?":
            "Oh Annie, you've never been just my sister.",

        # OS script2:3830
        "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our friendship.":
            "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our relationship as brother and sister.",

        # OS script2:3843
        "*Kissing her neck* And don’t you worry. I’m perfectly fine with going as slow as you want.":
            "*Kissing her neck* And don’t you worry, sis. I’m perfectly fine with going as slow as you want.",

        # OS script2:3845
        "Y-Yeah... m-much better. You’re so warm...":
            "Y-Yeah... m-much better. You’re so warm, bro...",

        # OS script:3854
        "You’re... so wet...":
            "Annie... You’re... so wet...",

        # OS script2:3865 {specific}, also overwrites script4:5819, script6:6414, script6:6556, script8:9636
        # Excludes script2:3905, script8:9293
        "Oh Annie...":[
            ("Oh sis...","script2:3865"),
            ("Oh sis...","script4:5819"),
            ("Oh sis...","script6:6414"),
            ("Oh sis...","script6:6556"),
            ("Oh sis...","script8:9636"),

            # Bonus Mod
            ("Oh sis...","script2:3914"),
            ("Oh sis...","script4:5880"),
            ("Oh sis...","script6:6454"),
            ("Oh sis...","script6:6596"),
            ("Oh sis...","script8:9767"),

            # Multi Mod
            ("Oh sis...","script2:3880"),
            ("Oh sis...","script4:5852"),
            ("Oh sis...","script6:6442"),
            ("Oh sis...","script6:6584"),
            ("Oh sis...","script8:9665"),
        ],

        # OS script2:3867
        "(Holy shit, this is really happening! I'm fucking Annie's thighs!)":
            "(Holy shit, this is really happening! I'm fucking my sister's thighs!)",

        # OS script2:3872
        "Jesus, Annie...":
            "Jesus, sis...",

        # OS script2:3924
        "Oh shit, I'm sorry, Annie...":
            "Oh shit, I'm sorry, sis...",

        # OS script2:3931
        "Did I do something wrong, Annie? I’m sorry! I didn’t know it was going to be that much!":
            "Did I do something wrong, sis? I’m sorry! I didn’t know it was going to be that much!",

        # OS script2:3942
        "I only came here t-to sleep and then... next thing I know I’m doing that...":
            "I only came here t-to sleep and then... next thing I know I’m doing that... and with my brother...",

        # OS script2:3945
        "No, no! It's okay! You’re good! I like you, Annie! We can...":
            "No, no! It's okay! You’re good! I like you, sis! We can...",

        # OS script2:3952
        "We skipped like 14 steps! In one night!":
            "We skipped like 14 steps and broke a dozen rules! In one night!",

        # OS script2:3957
        "What will [mc] think of me after all of this?!":
            "What will my brother think of me after all of this?!",

        # OS script2:3965
        "I'm gonna... go... think! Good night [mc]!":
            "I'm gonna... go... think! Good night, bro!",

        # OS script2:3979
        "(Maybe something between us could work after all.)":
            "(Even if we're siblings, maybe something between us could work after all.)",

        # OS script2:3981
        "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing Annie’s secret kinky side... and I loved every moment of it!)":
            "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing my sister's secret kinky side... and I loved every moment of it!)",

        # OS script2:4474
        "Annie! Do you have a minute? I wanted to talk to you!":
            "Sis! Do you have a minute? I wanted to talk to you!",

        # OS script2:5364 (n)
        "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out.)":
            "(Even if, somehow, he wanted me too... and we ended up... doing it, the girls would be furious if they ever found out.)",

        # OS script2:5413 (n)
        "(I bet if I tried to do anything at home, Dalia or Penny would surely notice.)":
            "(I bet if I tried to do anything at home, the girls would surely notice.)",

        # OS script2:5937 (x)
        "And on the first day of school, I saw him harassing a close friend of mine.":
            "And on the first day of school, I saw him harassing my sister.",

        # BA/N: also wanted to add a line about how Alex and MC are both twins but can't find a good place to fit it in

        # ========== START WIP ==========
            # BA/N: technically with Annie as sister, MC was never completely alone; Not sure how to fit that in while keeping the sentiment of the original.

        # BM script2:6102 (x)
        #"It probably doesn’t mean much, but I can sort of understand where you’re coming from.":
        #    "It probably doesn’t mean much, but I can sort of understand where you’re coming from.",

        # BM script2:6103 (x)
        #"I never met my mother and my father was always absent in my life. He was constantly too occupied with his work.":
        #    "My father was always absent in my life, always too occupied with his work. When my parents divorced, I had to live with him for the last ten years, if you can even call it \"living with him\".",

        # OS script2:6104 (x)
        "I know what it's like to be alone.":
            "I know what it's like to feel alone.",

        # BM script2:6106 (x) {inject}
        #"Huh... I just assumed you were one of those pampered city boys that’s never known a hard day in his life...":[
        #    ("Oh right, you {i}are{/i} Dalia's brother...","script2:6106",[
        #        'x "Honestly, my first impression of you was that you were one of those pampered city boys that’s never known a hard day in his life..."'
        #    ]),

            # Bonus Mod script2:6170

            # Multi Mod script2:6122
        #],

        # ========== END WIP ==========


    # -----------------------------------------
    # v0.3 script3.rpy

        # OS script3:3343
        "Not a worry in mah noggin, homie. I just be... chillaxin’ all day! Yeahhhh...":
            "Not a worry in mah noggin, bro. I just be... chillaxin’ all day! Yeahhhh...",

        # OS script3:3362
        "Good morning, Annie!":
            "Good morning, sis!",

        # OS script3:3368
        "Um... Oh! [mc]! Good morning!":
            "Um... Oh! Bro! Good morning!",

        # OS script3:3392
        "But no biggie. I was scared. Not thinking clearly.":
            "But no biggie, bro. I was scared. Not thinking clearly.",

        # OS script3:3400
        "(She's right. Forgetting about this might be the best option right now.)":
            "(She's right. Forgetting about this might be the best option. We crossed way too many lines that night.)",

        # OS script3:3402
        "(That's all I want... just to stay friends with her.)":
            "(That's all I want... just to have a normal sibling relationship with her.)",

        # OS script3:3412
        "That sounds great. Take care, Annie!":
            "That sounds great. Take care, sis!",

        # OS script3:3414
        "Thank you, [mc]. I needed this talk.":
            "Thank you, bro. I needed this talk.",

        # OS script3:3420
        "*Taking a deep breath* (Well [mc], it's now or never. Time to grow a pair and man up!)":
            "*Taking a deep breath* (Well [mc], it's now or never. Time to grow a pair and man up! Let your sister know how you really feel.)",

        # OS script3:3423
        # BA/N: disabled, using name adds a bit of seriousness here
        #"I like you, Annie.":
        #    "I like you, sis.",

        # OS script3:3428
        "I've liked you ever since we were 10. If I’m being real with you, the only reason why I was willing to come back to Kredon at all was because you were coming too.":
            "And I mean I {i}like{/i} like you. I've felt this way since we were 10. If I’m being real with you, the only reason why I was willing to come back to Kredon at all was because you were coming too.",

        # OS script3:3431
        "You're my best friend.":
            "You're my twin sister.",

        # OS script3:3434
        "And in my heart I know, I want us to be so much more than that, too...":
            "So I know this is so, very wrong... but in my heart, I want us to be so much more than that.",

        # OS script3:3446
        "I don't want to lose our friendship, Annie. I’d be miserable without you in my life.":
            "I don't want to lose you, sis. I’d be miserable without you in my life.",

        # OS script3:3449
        "I just want us to stay friends forever!":
            "I just want us to be together forever!",

        # OS script3:3467
        "That sounds great! Just spending some time together as good friends. Like how we’ve always done it!":
            "That sounds great! Just some quality sibling bonding time. Like how we’ve always done it!",

        # OS script3:3483
        "Like... a fun date between friends?":
            "Like... a fun date with your sister?",

        # OS script3:3484
        "Hmmm... no, more like a date with a girl that I like. And I just happen to be so lucky in that, she’s also my best friend too. As for what the future holds? Who knows...":
            "Hmmm... no, more like a date with a girl that I like. Who just happens to be both my sister, and my best friend too. As for what the future holds? Who knows...",

        # OS script3:3505
        "Look, [mc], I know we’re going on a {i}date{/i} date, but I really do want to take it slow too. I don’t want you to assume that–":
            "Look, bro, I know we’re going on a {i}date{/i} date, but I really do want to take it slow too. I don’t want you to assume that–",

        # OS script3:3511
        "And not a word to anyone. I mean... there's no need for it, really. We’re just two people going on a date, and there’s no need to overthink it.":
            "We’re just two people going on a date, there’s no need to overthink it. But uh, not a word to anyone. Don't want others to think weird things...",

        # OS script3:3518
        "T-Thank you, [mc]. I needed this talk.":
            "T-Thank you, bro. I needed this talk.",

        # OS script3:3540
        # BA/N: borrowed from stepsis map
        "I know you want to take things slow. And I’m perfectly okay with that.":
            "I know you want to take things slow, sis. And I’m perfectly okay with that.",

        # OS script3:3561
        "That was quite the goodbye for just a couple of... friends.":
            "That was quite the goodbye for just... siblings.",

        # OS script3:3578
        "(Maybe a good movie? Or a walk along the beach. Or even a date in Eternum!)":
            "(Maybe a good movie? Or a walk along the beach. Or even a date in Eternum! We wouldn't have to worry about running into people who know us there.)",

        # OS script3:4828 (d)
        # BA/N: added Annie mention at start of flashback, also sets up for AS script3:5231
        "And it helps you grow up to be strong!":
            "Mommy said it's good for you! Helps you grow up to be strong!",

        # OS script3:4829 (d)
        "It’s good for you! Mommy told me!":
            "This is why you and Annie are such sleepyheads.",

        # OS script3:4919 (n)
        "([mc]'s father is already generously paying me more than he should for taking care of his son. But even with that extra money, it's only delaying the inevitable.)":
            "([mc] and Annie's father is already generously paying me more than he should for taking care of his children. But even with that extra money, it's only delaying the inevitable.)",

        # OS script3:4982
        "I... I know honey, but I don't have anyone else I can call on such short notice to take care of Dalia and [mc].":
            "I... I know honey, but I don't have anyone else I can call on such short notice to take care of the little ones.",

        # OS script3:5046
        "And... what about Dalia and [mc]?":
            "And... what about Dalia, Annie, and [mc]?",

        # OS script3:5105
        "Nothing... I’m just sad because in a couple of weeks, my dad will be bringing me with him to Europe.":
            "Nothing... I'm just sad because in a couple of weeks, my dad will be taking me and Annie with him to Europe.",

        # OS script3:5111
        "Well you can still come play with me after school, right?":
            "Well you two can still come play with me after school, right?",

        # OS script3:5171
        "Absolutely! Don't worry sis, I'll protect you, [mc], and Mom!":
            "Absolutely! Don't worry sis, I'll protect you, and [mc], and Annie, and Mom too!",

        # OS script3:5228
        "But you got to bathe first!":
            "But you two got to bathe first! I can see the mud stains on you!",

        # OS script3:5230
        "Come on [mc], let's go to the bathroom.":
            "Where's Annie? She was playing with you outside earlier.",

        # OS script3:5231
        "Me too?!":
            "She got sleepy and took a nap.",

        # OS script3:5232
        "Yeah, let's go! We're all gonna bathe together!":
            "Go wake her up, she also needs to bathe!",

        # OS script3:5233
        "But I'm not dirty!":
            "Okay!",

        # OS script3:5234
        "I can see the mud stains from here, mister!":
            "After that, we can all watch movies together!",

        # OS script3:9866 (n)
        "I think this goes without saying, but let’s not mention this to anyone. My daughters especially... heaven knows what they’d think if they learned we bathed together.":
            "I think this goes without saying, but let’s not mention this to anyone. My daughters and your sister especially... heaven knows what they’d think if they learned we bathed together.",


    # -----------------------------------------
    # v0.4 script4.rpy

        # OS script4:4286
        "(I'm going on a date with [mc]!)":
            "(I'm going on a date with my brother!)",

        # OS script4:4339
        "*Chuckles* I think you're getting too excited about this, Annie. You need to relax. You'll enjoy it more if you take it less seriously!":
            "*Chuckles* I think you're getting too excited about this, sis. You need to relax. You'll enjoy it more if you take it less seriously!",

        # OS script4:4347
        "Chillin’ like a villain on penicillin, bro!":
            "Chillin’ like a villain on penicillin, yo!",

        # OS script4:4349
        "Gonna play some Eternum with ma' homie...":
            "Gonna play some Eternum with ma' bro...",

        # OS script4:4397
        "Send invitation... to... Annie Winters.":
            "Send invitation... to... Annie [lastname].",

        # OS script4:4411
        "Annie? Is that you?":
            "Sis? Is that you?",

        # OS script4:4621
        "Quick, [mc], make a wish!":
            "Quick, bro, make a wish!",

        # OS script4:4686
        "Let's watch Interstellar. It's one of my favorite movies, and I know you haven't seen it yet.":
            "Let's watch Interstellar, it's one of my favorite movies. It's the one I've been trying to get you to watch since you love sci-fi.",

        # OS script4:4687
        "With how much you love sci-fi, I'm sure you'll like it too!":
            "You were busy every time I wanted to watch it with you, so now's our chance!",

        # OS script4:4803
        # Overwritten by OS script:2952, okay
        # "Are you okay, Annie?" -> "Are you okay, sis?"

        # OS script4:4825
        "I can see why! I remember you talking about it, but I never got the chance to see it until now.":
            "I can see why! You were so right, I should've watched this sooner.",

        # OS script4:4915
        "I mean... of course we're not. We haven't even...":
            "I mean... of course we're not. We're still {i}just{/i} siblings, we haven't...",

        # OS script4:4926
        "*Chuckles* A likely story, Ms. Winters... I'll believe you, for now...":
            "*Chuckles* A likely story, dear sister... I'll believe you, for now...",

        # OS script4:4977
        "Come here, [mc]! Jump!":
            "Come here, bro! Jump!",

        # OS script4:4984
        "Have you ever done any scuba diving?":
            "We've never done any scuba diving?",

        # OS script4:4995
        # Overwritten by OS script2:2085, okay
        # "Right, Annie?" -> "Right, sis?"

        # OS script4:4997
        "Annie, you awake? I can go call the Astrocorp employee if we’re ready to wrap this up.":
            "Sis, you awake? I can go call the Astrocorp employee if we’re ready to wrap this up.",

        # OS script4:5004
        "You and Chang have always been my best friends, and neither of you played Eternum until recently, so... I've always felt kind of alone here.":
            "You and Chang have always been by my side, and neither of you played Eternum until recently, so... I've always felt kind of alone here.",

        # OS script4:5008
        "You’re the one who’s really made these first few weeks in Eternum worthwhile, Annie. I couldn't have asked for anyone better to spend time with.":
            "You’re the one who’s really made these first few weeks in Eternum worthwhile, sis. I couldn't have asked for anyone better to spend time with.",

        # OS script4:5108
        "How's life in Kredon so far?":
            "How's life back in Kredon so far?",

        # OS script4:5111
        "You were right, it's a rather small town, but there's everything you need!":
            "It's still a rather small town like I remembered, but there's everything we need!",

        # OS script4:5113
        "Nancy, Penelope, and Dalia are all very nice to me. They treat me as one of the family. You know I’ve always wanted sisters, so I really feel like they’re giving me that experience!":
            "Nancy, Penny, and Dalia are still so nice to me. They treat like I'm their sister, which makes me feel suuuuuper happy!",

        # OS script4:5131
        "Oh! Come on, Annie! You can't be serious!":
            "Oh! Come on, sis! You can't be serious!",

        # OS script4:5216
        "*Jumps on the bed* Oh my god, [mc]! Look at this!":
            "*Jumps on the bed* Oh my god, bro! Look at this!",

        # OS script4:5250
        # BA/N: borrowed from stepsis map
        "(Maybe... it's just not the right time yet...?)":
            "(Maybe... was this all a mistake...?)",

        # OS script4:5311 (menu)
        # l9/N: Changed to be fully compatible with and without either walkthrough
        "Decline and stay as friends":
            "{color=[walk_path]}Decline and stay as siblings [red][mt](Closes Annie's path)",

        # OS script4:5314
        "I like you, and you're my best friend, you already know that.":
            "I like you, and you're my sister, you already know that.",

        # OS script4:5315
        "But... I also feel like we're not meant to be more than that. Things would get awkward if we tried to get together, and our friendship is too important to risk, for me at least.":
            "But... I also feel like we're not meant to be more than that. Things would get {i}so{/i} complicated if we tried to get together, and our relationship is too important to risk, for me at least.",

        # BA/N: next 7 lines borrowed and modified from stepsis map, which rewrote them to be a bit more emotional which I agree with, but tried to keep more of the original lines in it than the stepsis map did.

        # OS script4:5316
        "I just like spending time with you!":
            "I'm still your brother and I'll always be there for you, but...",

        # OS script4:5317
        "I... I think we're meant to be friends. Best friends!":
            "I... I don't think we're meant to be anything more than siblings.",

        # OS script4:5318
        "So... let's just stay like this for now, okay?":
            "So... let's just go back to what we always were, okay?",

        # OS script4:5319
        "I just don’t have those feelings for you right now.":
            "I can’t commit to this... {i}thing{/i} between us. Not right now. ",

        # OS script4:5320
        "In the future... who knows? Maybe. But I don’t want to lead you on, either.":
            "In the future... I don’t know. Maybe. But I don’t want to lead you on, either.",

        # OS script4:5326
        "No worries! I totally understand. My head has been all over the place too, you know, with all this back and forth...":
            "It's not your fault, Annie, it's mine. I know I've been sending you mixed signals, bringing you here today. My head has been all over the place too, you know, with all this back and forth... You don't deserve that.",

        # OS script4:5327
        "We can have this conversation again after we gather the 10 Gems!":
            "I'm sorry, sis. This isn't how I wanted today to go. For what it's worth, I still enjoyed spending this time with you.",

        # OS script4:5369
        "Y-Yeah... It's been like... 10 years since we first met?":
            "Y-Yeah...",

        # OS script4:5371
        "That’s quite a while... No big deal.":
            "No big deal.",

        # OS script4:5382
        "You're so pretty, Annie...":
            "You're so pretty, sis...",

        # OS script4:5395
        "[mc]! What are you doing?!":
            "Bro! What are you doing?!",

        # OS script4:5405
        "Seeing you undressing just for me was hot as fuck, Annie.":
            "Seeing you undressing just for me was hot as fuck, sis.",

        # OS script4:5436
        "But... Do you think I'm NOT nervous? I'm super scared too! I mean, in my arms, I'm holding an adorably precious, absolutely gorgeous girl whom I’ve liked for years.":
            "But... Do you think I'm NOT nervous? I'm super scared too! I mean, in my arms, I'm holding my adorably precious, absolutely gorgeous twin sister whom I’ve liked for years.",

        # OS script4:5438
        "I know it's scary to get out of your comfort zone, but... I think we can overcome it together.":
            "I know it's terrifying thing we're trying, starting a relationship as siblings, but... I think we can overcome it together.",

        # OS script4:5442
        "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay friends!":
            "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and just be siblings again!",

        # OS script4:5443
        "It’ll be a little awkward at first, but our friendship is strong, and I know we’d be back to normal in no time.":
            "It’ll be a little awkward at first, but our relationship is strong, and I know we’d be back to normal in no time.",

        # OS script4:5471
        "*Caressing her cheek* I feel like I could never get enough of you, Annie...":
            "*Caressing her cheek* I feel like I could never get enough of you, sis...",

        # OS script4:5494
        "Is that so? What have you been thinking about, exactly, Ms. Winters?":
            "Is that so? What have you been thinking about, exactly, Ms. [lastname]?",

        # OS script4:5518
        "Have I been fooled all these years? Innocent, shy Annie is actually a horny, perverted little girl?":
            "Have I been fooled all these years? My innocent, shy little sister is actually a horny, perverted little girl?",

        # OS script4:5526
        "God, there are so many things I want to do to Annie right now... but it's still Annie. I don't wanna cross any line too fast.":
            "God, there are so many things I want to do to Annie right now... but she is still my sister. I don't wanna cross any line too fast.",

        # OS script4:5528
        "You're making me so horny, Annie...":
            "You're making me so horny, sis...",

        # OS script4:5562
        "It'll only get better from here, babe...":
            "It'll only get better from here, Annie...",

        # OS script4:5604
        "*Panting* K-Keep going, [mc]! Y-You’re hitting just the... r-right spot!":
            "*Panting* K-Keep going, bro! Y-You’re hitting just the... r-right spot!",

        # OS script4:5621
        "Y-You have to stop! S-STOP! [mc]!":
            "Y-You have to stop! S-STOP! [mc!u]!",

        # OS script4:5624
        "Don't worry, babe...":
            "Don't worry, sis...",

        # OS script4:5665
        "([mc] made me... {i} cum{/i}!)":
            "(My brother made me... {i} cum{/i}!)",

        # OS script4:5675
        "You turn me on so much, Annie... I'd be lying if I said I wasn’t rock-hard the whole time...":
            "You turn me on so much, sis... I'd be lying if I said I wasn’t rock-hard the whole time...",

        # OS script4:5721
        "That's it, baby...":
            "That's it, sis...",

        # OS script4:5724
        "You’re such a good girl, Annie...":
            "You’re such a good girl, sis...",

        # OS script4:5753
        "D-Do you like beating off my cock, Annie?":
            "D-Do you like beating off my cock, sis?",

        # OS script4:5765
        "*Panting* F-Fuck, I won't last much longer, Annie...":
            "*Panting* F-Fuck, I won't last much longer, sis...",

        # OS script4:5767
        "I want to make you cum, [mc]... You were so kind to me...":
            "I want to make you cum, bro... You were so kind to me...",

        # OS script4:5819
        # Overwritten by OS script2:3865, okay
        # "Oh Annie..." -> "Oh sis..."

        # OS script4:5823
        "I want you so bad, Annie... I can’t wait ‘til the day you can finally take this dick... But not yet...":
            "I want you so bad, sis... I can’t wait ‘til the day you can finally take this dick... But not yet...",

        # OS script4:5825
        "W-We’ve g-gotta do some practicing b-beforehand, [mc]...":
            "W-We’ve g-gotta do some practicing b-beforehand, bro...",

        # OS script4:6106
        "My date left the room and went to the canteen, and a few minutes later... the lights went out and everyone had disappeared!":
            "My si- my date left the room and went to the canteen, and a few minutes later... the lights went out and everyone had disappeared!",

        # OS script4:6902
        # Overwritten by AS script:6179, okay
        # "Annie?!" -> "Hey, sis?!"

        # OS script4:6924
        "Oh Annie... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?":
            "Oh sis... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?",

        # OS script4:6942
        "Look, Annie! A teleporter! We can get out of here!":
            "Look, sis! A teleporter! We can get out of here!",

        # OS script4:6952
        "*Pulling your shirt* [mc]...":
            "*Pulling your shirt* Bro...",

        # OS script4:6986
        "D-Don't look at him, Annie.":
            "D-Don't look at him, sis.",

        # OS script4:7014
        "*Whispering* O-Okay Annie...":
            "*Whispering* O-Okay sis...",

        # OS script4:7052
        "*Sobbing* [mc]?":
            "*Sobbing* [mc_dash]?",

        # OS script4:7054
        # BA/N: Disabled for seriousness
        #"D-Don't worry, Annie...":
        #    "D-Don't worry, sis...",

        # OS script4:7250
        "Thank you for an amazing day, [mc].":
            "Thank you for an amazing day, bro.",

        # OS script4:7252
        "I'm glad you enjoyed it, Annie. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.":
            "I'm glad you enjoyed it, sis. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.",

        # OS script4:7429
        "Oh, already?! Good luck, [mc]! Be sure to get plenty of information!":
            "Oh, already?! Good luck, bro! Be sure to get plenty of information!",

        # OS script4:7431
        "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what best friends do, I guess.":
            "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what brothers do, I guess.",

        # OS script4:8176 (misc)
        # BA/N: borrowed from aunt map, random but funny change
        "Actually, he was caught with HER sister in HIS office!":
            "Actually, he was caught with HIS OWN sister in HIS office!",


    # -----------------------------------------
    # v0.5 script5.rpy

        # OS script5:809
        "The scholarship that was granted to [mc] and his best friends is the best thing that has happened to me in a very long time.":
            "The scholarship that was granted to these three best friends is the best thing that has happened to me in a very long time.",

        # OS script5:811
        "*Clears throat* I think it's best not to dig too deep into the \"best friend\" subject.":
            "*Clears throat* I think it's best not to bring up the \"best friend\" subject.",

        # OS script5:842
        "I don't really mind anymore. I'm happy being just a good friend.":
            "I don't really mind anymore. I'm happy just being his sister.",

        # OS script5:1005
        "B-Bye, [mc]! I'll see you at home!":
            "B-Bye, bro! I'll see you at home!",

        # OS script5:2044
        "I mean, Dad has only called me once since I got here.":
            "I mean, Dad has only called us once since we got here. Our grandparents called every other week.",

        # OS script5:10045 (p)
        "*Snorts* You're such a dork. You’re lucky I think you’re cute.":
            "*Snorts* You’re such a cute little dork. Don’t you have enough twins in your life already?",

        # OS script5:12104 (n)
        "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters would take the news.":
            "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters or your sister would take the news.",


    # -----------------------------------------
    # v0.6 script6.rpy

        # OS script6:243
        "Private Annie Winters reports!":
            "Private Annie [lastname] reports!",

        # OS script6:1674 {inject}
        # working in why annie didn't go too, elaborated later on
        "I thought I'd be way more homesick.":[
            ("I thought I'd be way more homesick.","script6:1674",[
                'show ep 41',
                'a "I told you you booked it too soon!" with dis',
                'show ep 40',
                'mc "Yeah, I might’ve rushed a bit since the ticket was cheap."'
            ]),

            # Bonus Mod
            ("I thought I'd be way more homesick.","script6:1684",[
                'show ep 41',
                'a "I told you you booked it too soon!" with dis',
                'show ep 40',
                'mc "Yeah, I might’ve rushed a bit since the ticket was cheap."'
            ]),

            # Multi Mod
            # script6:1674, same as original
        ],

        # OS script6:1678
        "How was your father?":
            "How was Dad?",

        # OS script6:1785
        "Good night!!":
            "Good night bro!!",

        # OS script6:1975
        "[mc]...? What are you doing here?!":
            "Bro...? What are you doing here?!",

        # OS script6:2004
        "It's just... that... well, I was shocked at first since we had {i}never{/i} seen each other naked, and all that.":
            "It's just... that... well, I was shocked at first since the last time I saw you naked was {i}so long{/i} ago.",

        # OS script6:2008 (no)
        "A bit striking because I {i}never{/i} saw you naked before either.":
            "A bit striking because I {i}never{/i} saw you naked before.",

        # ========== START Murder Mystery ==========
            # adding this just to note that this section is organized by script line, and does not really reflect the order the events actually play out in game

        # OS script6:3524
        "What? Annie?":
            "What? Sis?",

        # OS script6:3536
        "Elementary, my dear [mc].":
            "Elementary, my dear brother.",

        # OS script6:3689
        "Well, you should still get it, [mc].":
            "Well, you should still get it, bro.",

        # OS script6:4970
        "We're just... friends.":
            "Delilah's just... a friend. And Annie's my sister.",

        # OS script6:4975
        "Are you seriously telling me you have those two fun-sized cuties around you and you're not doing anything with them?":
            "What a shame. I couldn't imagine having these two fun-sized cuties around me and not doing anything with them.",

        # OS script6:5473
        "Um... Annie? We have a problem.":
            "Um... Sis? We have a problem.",

        # OS script6:5474
        "Wow, come here, [mc]!":
            "Wow, come here, bro!",

        # OS script6:5504
        "Oh, thanks for the reassurance, [mc]! I feel much, much better now!":
            "Oh, thanks for the reassurance, brother! I feel much, much better now!",

        # OS script6:5523
        "Can you focus and stop being a pig?!":
            "Can you focus and stop being a pervert?!",

        # OS script6:5739 (a) {specific}
        # Excludes script:3745 (d), script3:734 (no)
        "[mc]!!":[
            ("Bro!!","script6:5739"),

            # Bonus Mod
            ("Bro!!","script6:5775"),

            # Multi Mod
            ("Bro!!","script6:5767"),
        ],

        # ========== END Murder Mystery ==========

        # OS script6:5970
        "*Knocking on the door* Annie?":
            "*Knocking on the door* Sis?",

        # OS script6:6012
        "B-But thank you.":
            "B-But thank you, bro.",

        # OS script6:6014
        "Penelope has been teaching me different ways to style it too.":
            "Penny has been teaching me different ways to style it too.",

        # OS script6:6026 {inject}
        # adding why Annie didn't go with you
        "*Eating another cookie* Mm-yeah, people mentioned how much my hair had grown during my visit too.":[
            ("*Eating another cookie* Mm-yeah, people mentioned how much my hair had grown during my visit too.","script6:6026",[
                'mc "They were also really surprised that you didn’t come with me."',
                "show eaa 11",
                'a "*Laughs* True, I don’t think we’ve been apart for this long before."',
                'a "Sorry to make you go alone, but I knew I wouldn’t be ready to go back so soon."',
                "show eaa 10",
                'mc "Nah, you were right about that. Though was kind of interesting to be completely on my own for once."',
            ]),

            # Bonus Mod
            ("*Eating another cookie* Mm-yeah, people mentioned how much my hair had grown during my visit too.","script6:6064",[
                'mc "They were also really surprised that you didn’t come with me."',
                "show eaa 11",
                'a "*Laughs* True, I don’t think we’ve been apart for this long before."',
                'a "Sorry to make you go alone, but I knew I wouldn’t be ready to go back so soon."',
                "show eaa 10",
                'mc "Nah, you were right about that. Though was kind of interesting to be completely on my own for once."',
            ]),

            # Multi Mod
            ("*Eating another cookie* Mm-yeah, people mentioned how much my hair had grown during my visit too.","script6:6054",[
                'mc "They were also really surprised that you didn’t come with me."',
                "show eaa 11",
                'a "*Laughs* True, I don’t think we’ve been apart for this long before."',
                'a "Sorry to make you go alone, but I knew I wouldn’t be ready to go back so soon."',
                "show eaa 10",
                'mc "Nah, you were right about that. Though was kind of interesting to be completely on my own for once."',
            ]),
        ],

        # OS script6:6031 {inject}
        "I don't care if I find discounted plane tickets again, I have no reason to go back there.":[
            ("I don't care if I find discounted plane tickets again, I have no reason to go back there.","script6:6031",[
                "show eaa 11",
                'a "Ouch. I’m telling Grandpa and Grandma that next time they call."',
                "show eaa 10",
                'mc "*Laughs* Okay, maybe two reasons."'
            ]),

            # Bonus Mod
            ("I don't care if I find discounted plane tickets again, I have no reason to go back there.","script6:6069",[
                "show eaa 11",
                'a "Ouch. I’m telling Grandpa and Grandma that next time they call."',
                "show eaa 10",
                'mc "*Laughs* Okay, maybe two reasons."'
            ]),

            # Multi Mod
            ("I don't care if I find discounted plane tickets again, I have no reason to go back there.","script6:6059",[
                "show eaa 11",
                'a "Ouch. I’m telling Grandpa and Grandma that next time they call."',
                "show eaa 10",
                'mc "*Laughs* Okay, maybe two reasons."'
            ]),
        ],

        # OS script6:6033
        "And how was your dad?":
            "And how was Dad?",

        # OS script6:6035
        "My dad...?":
            "Dad...?",

        # OS script6:6050
        "Tell Na-":
            "Tell Annie and Na-",

        # OS script6:6063
        "So... yeah, you know how my father is.":
            "So... yeah, you know how Dad is.",

        # OS script6:6065
        "Awh, I'm so sorry, [mc]...":
            "Awh, I'm so sorry, bro...",

        # OS script6:6066
        "I can’t imagine how that must’ve felt after traveling all that way.":
            "That must've really hurt to hear now that we’ve reunited with them.",
            #"I know a part of us is always hoping to get a bit more from him.",

        # OS script6:6087 (menu)
        "You know dads can be real assholes":
            "You know Dad can be a real asshole",

        # OS script6:6088
        "You know as well as I do that dads can be real assholes.":
            "You know as well as I do that Dad can be a real asshole.",

        # OS script6:6090
        "W-Well... it's true that my dad has been working a lot all his life and he's been a bit absent, but... he's always cared about me.":
            "W-Well... it’s true that Dad’s always been pretty absent because of work, but...",

        # OS script6:6091
        "And he thinks highly of you!":
            "We still had our grandparents! And Chang’s parents too!",

        # OS script6:6093
        "Well... yeah, I guess that's different.":
            "Well... yeah. At least we had some adults looking out for us. Even if we didn't see them very often.",

        # OS script6:6094
        "That came out wrong, I'm sorry.":
            "Grandpa and Grandma miss you by the way.",

        # OS script6:6096
        "No worries! I know you didn't mean it in a bad way.":
            "I miss them too! I'll need make it up to them sometime.",

        # OS script6:6190
        "*Laughs* Don't be so dramatic.":
            "*Laughs* Don't be so dramatic, sis.",

        # OS script6:6215 {specific}
        # Excludes script:8614 (n)
        "Good night, [mc]!":[
            ("Good night, bro!","script6:6215"),

            # Bonus Mod
            ("Good night, bro!","script6:6253"),

            # Multi Mod
            ("Good night, bro!","script6:6243"),
        ],

        # OS script6:6218 {specific}
        # Excludes script6:5866 (no) and script6:3453 (mc)
        "Good night, Annie!":[
            ("Good night, sis!","script6:6218"),

            # Bonus Mod
            ("Good night, sis!","script6:6256"),

            # Multi Mod
            ("Good night, sis!","script6:6246"),
        ],

        # OS script6:6278
        # Disabled for impact
        #"You need to be more direct, Annie.":
        #    "You need to be more direct, sis.",

        # OS script6:6338
        "I’ll never get tired of seeing your gorgeous body, Annie.":
            "I’ll never get tired of seeing your gorgeous body, sis.",

        # OS script6:6399
        "I... I'm n-not sure I'm ready, [mc].":
            "I... I'm n-not sure I'm ready, bro.",

        # OS script6:6414
        # Overwritten by AS script2:3865, okay
        # "Oh Annie..." -> "Oh sis..."

        # OS script6:6426
        "I’m dying to taste you, Annie.":
            "I’m dying to taste you, sis.",

        # OS script6:6427
        "[mc], I... I-I'm not sure if I'm ready for that either!":
            "Bro, I... I-I'm not sure if I'm ready for that either!",

        # OS script6:6440
        "Oh [mc]... that feels...":
            "Oh brooo... that feels...",

        # OS script6:6450
        "You begin to taste every inch of Annie, spreading her tight lips as you gracefully move your tongue back and forth.":
            "You begin to taste every inch of your twin sister, spreading her tight lips as you gracefully move your tongue back and forth.",

        # OS script6:6454
        "Oh my god, [mc]...":
            "Oh my god, bro...",

        # OS script6:6471
        "[mc]. . . . . . . . . . .  . !":
            "Broooo. . . . . . . . . . .  . !",

        # OS script6:6486
        "AAaahh... oh god [mc]... I think I'm gonna... C-CUM...":
            "AAaahh... oh god bro... I think I'm gonna... C-CUM...",

        # OS script6:6488
        "[mc]! You’re gonna make me...":
            "Bro! You’re gonna make me...",

        # OS script6:6556
        # Overwritten by AS script2:3865, okay
        # "Oh Annie..." -> "Oh sis..."

        # OS script6:6559
        "I can feel you pulsing, [mc]...":
            "I can feel you pulsing, bro...",

        # OS script6:6605
        "Yeah... keep going... suck it as hard as you can, babe...":
            "Yeah... keep going... suck it as hard as you can, sis...",

        # OS script6:6627
        "*Panting* Annie...?":
            "*Panting* Sis...?",

        # OS script6:6644
        "You grab Annie's head and start fucking her mouth. You can hear her choking with each thrust, but Annie's throat willingly takes all of you.":
            "You grab your sister's head and start fucking her mouth. You can hear her choking with each thrust, but Annie's throat willingly takes all of you.",

        # OS script6:6657
        "The sweet, innocent, little girl I've known for years...":
            "My sweet, innocent, twin sister...",
            #"The sweet, innocent, little girl I've known my entire life...",

        # OS script6:6666
        "Come on Annie, you're gonna miss the entire movie!":
            "Come on sis, you're gonna miss the entire movie!",

        # OS script6:6681
        "AAAAargh... fuck, Annie...":
            "AAAAargh... fuck, sis...",

        # OS script6:6687
        "You better take care of my little girl while you're in the USA, [mc].":
            "You better take care of your sister while you're in the USA, [mc].",
        
        # OS script6:6688
        "Rest assured Mr. Winters, I won’t let anything happen to her!":
            "Rest assured Grandpa, I won’t let anything happen to her!",

        # OS script6:6689
        "I'll take care of Annie as if she was my sister!":
            "I'll always take great care of Annie!",

        # OS script6:6700
        "Oh GOD, Annie, I'm gonna fucking cum!":
            "Oh GOD, sis, I'm gonna fucking cum!",

        # OS script6:6718
        "*Panting* Do it... empty y-yourself all over me, [mc]...":
            "*Panting* Do it... empty y-yourself all over me, bro...",

        # OS script6:6719
        "Oh god Annie, I'm...":
            "Oh god sis, I'm...",

        # OS script6:6750
        "Goddammit Annie... that was mind-blowing.":
            "Goddammit sis... that was mind-blowing.",

        # OS script6:6757
        "Well, I'm sure Dalia and Penelope would knock before entering your room.":
            "Well, I'm sure Dalia and Penny would knock before entering your room.",

        # OS script6:6766
        "Why would she? We weren't doing anything wrong.":
            "She cares about us too much to do anything like that.",

        # OS script6:6787
        "Good night, Annie.":
            "Good night, sis.",

        # ========== START Fuck Marry Kill ==========
            # BA/N: keeping this section because though not sisters here, Dalia is less likely to pick Fuck if she also knew Annie from childhood

        # OS script6:10185 (d)
        "And then I'd fuck... Annie.":
            "And then I'd marry... Annie.",

        # OS script6:10185 (d)
        "She's so cute. She’s small, but... in a hot way. You know what I mean?":
            "She’s so small and cute. Imagine having that adorable girl by your side all the time... though I suppose you already know what that’s like.",

        # OS script6:10185 (d)
        "You said fuck twice.":
            "You said marry twice.",

        # ========== END Fuck Marry Kill ==========


    # -----------------------------------------
    # v0.7 script7.rpy

        # OS script7:1461
        "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, Annie.":
            "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, sis.",

        # OS script7:1468 {specific}
        # Excludes script:7779 (eva)
        "Thank you, [mc]...":[
            ("Thank you, bro...","script7:1468"),

            # Bonus Mod
            ("Thank you, bro...","script7:1480"),

            # Multi Mod
            # script7:1468, same as original
        ],

        # OS script7:1502
        "Are you sure you don't want to join us, Annie?":
            "Are you sure you don't want to join us, sis?",

        # OS script7:1640
        "Take care, Annie.":
            "Take care, sis.",

        # ========== START harem thoughts ==========

        # OS script7:7396 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7396",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7452",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7454",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # OS script7:7398 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7398",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7454",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7456",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # OS script7:7402 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7402",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7458",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7460",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # OS script7:7404 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7404",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7460",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7462",[
                'mct "Well, Annie’s my twin sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # OS script7:7425 {inject}
        # BA/N: technically this wouldn't work if you're not on Annie's path but don't feel like making a labelmod to add if statement just for this
        #    but also why would you be playing this Annie sister mod without actually following Annie's path right?
        "I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?":[
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7425",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),

            # Bonus Mod
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7481",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),

            # Multi Mod
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7483",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),
        ],

        # ========== END harem thoughts ==========


    # -----------------------------------------
    # v0.8 script8.rpy

        # OS script8:4222
        "Come on, [mc], I need you to catch on quickly! We're running out of time.":
            "Come on, bro, I need you to catch on quickly! We're running out of time.",

        # OS script8:4231
        "Thank you for making me look so adorable!":
            "Thank you for making me look so adorable, bro!",

        # OS script8:4278
        #"There's no time to hesitate, [mc]!":
        #    "There's no time to hesitate, bro!",

        # OS script8:6521 (n) {inject}
        "If you ever hurt Nova, Annie, Luna, or Alex... I'll be seriously mad at you, young man.":[
            ("If you ever hurt Nova, Luna, or Alex... I'll be seriously mad at you, young man. Not to mention Annie... ","script8:6521",[
                "show gp 84",
                'n "I won’t judge you two, but she’s still your sister, so be especially careful with her." with dis12',
                "show gp 85",
                'mc "Of course I will."',
            ]),

            # Bonus Mod
            ("If you ever hurt Nova, Luna, or Alex... I'll be seriously mad at you, young man. Not to mention Annie...","script8:6624",[
                "show gp 84",
                'n "I won’t judge you two, but she’s still your sister, so be especially careful with her." with dis12',
                "show gp 85",
                'mc "Of course I will."',
            ]),

            # Multi Mod
            ("If you ever hurt Nova, Luna, or Alex... I'll be seriously mad at you, young man. Not to mention Annie...","script8:6549",[
                "show gp 84",
                'n "I won’t judge you two, but she’s still your sister, so be especially careful with her." with dis12',
                "show gp 85",
                'mc "Of course I will."',
            ]),
        ],

        # OS script8:6969
        "(She's definitely going on a date with [mc].)":
            "(She's definitely going on a date with [mc]. Her own twin brother!)",

        # OS script8:6983 (l)
        # BA/N: leaving this here for the future when we learn what exactly Luna's vision was
        # "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)":
        #     "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)",

        # OS script8:7092
        "It's straightforward yet stylish, giving off a confident vibe. It shows you're not desperate but also considerate enough to dress well for a date with someone who's been your second-best friend for so many years.":
            "It's straightforward yet stylish, giving off a confident vibe. It shows you're not desperate but also considerate enough to dress well for a date with someone who's been your second-best friend your entire life.",

        # OS script8:7098
        # Original non-inject version for safekeeping
        #"Hey, don’t sweat it. I already told you, it gives you a mysterious, sexy vibe.":
        #    "Hey, don’t sweat it. I already told you, it gives you a mysterious, sexy vibe.{p}And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.",

        # OS script8:7099
        # Original non-inject version for safekeeping
        #"And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.":
        #    "Which is still strange to think about since you’re twins, but... You two mean a lot to me, and I know how much you mean to each other.{p}So, I just want to tell you again that I’ll always support you two.",

        # OS script8:7099 {inject}
        "And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.":[
            ("And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.","script8:7099",[
                "show gf 35",
                'c "Which is still {i}really{/i} strange to think about since you’re actual twins, but..."',
                'c "Honestly, I probably could’ve seen it coming. I know how first-hand just much you two mean to each other."',
                "show gf 36",
                'c "So I just want to tell you again that you and Annie are my best friends, and I’ll always support you two." with dis08',
            ]),

            # Bonus Mod
            ("And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.","script8:7208",[
                "show gf 35",
                'c "Which is still {i}really{/i} strange to think about since you’re actual twins, but..."',
                'c "Honestly, I probably could’ve seen it coming. I know how first-hand just much you two mean to each other."',
                "show gf 36",
                'c "So I just want to tell you again that you and Annie are my best friends, and I’ll always support you two." with dis08',
            ]),

            # Multi Mod
            ("And in any case, no worries — Annie’s going to look at you with those lovey-dovey eyes of hers, so she’ll only see the good stuff.","script8:7127",[
                "show gf 35",
                'c "Which is still {i}really{/i} strange to think about since you’re actual twins, but..."',
                'c "Honestly, I probably could’ve seen it coming. I know how first-hand just much you two mean to each other."',
                "show gf 36",
                'c "So I just want to tell you again that you and Annie are my best friends, and I’ll always support you two." with dis08',
            ]),
        ],

        # OS script8:7101 {specific}
        # Excludes script4:2443 (d). original backup line saved just in case
        "*Chuckles* If you say so...":[
            ("*Chuckles* Thanks, man. I appreciate it a lot. I'm sure Annie would, too.","script8:7101"),
            #"*Chuckles* Thanks, bro. I appreciate it.",

            # Bonus Mod
            ("*Chuckles* Thanks, man. I appreciate it a lot. I'm sure Annie would, too.","script8:7210"),

            # Multi Mod
            ("*Chuckles* Thanks, man. I appreciate it a lot. I'm sure Annie would, too.","script8:7129"),
        ],

        # OS script8:7205
        #"[mc], over here!":
        #    "Bro, over here!",

        # OS script8:7209
        "Ah, hey there!":
            "Ah, hey there, sis!",

        # OS script8:7398
        "Annie Winters and Luna Hernandez travel to the super scary Red Herring server and complete–":
            "Annie [lastname] and Luna Hernandez travel to the super scary Red Herring server and complete–",

        # OS script8:7569
        "A-Annie...?":
            "Uh sis...?",

        # OS script8:7622
        "*Turning around* Um... Annie...":
            "*Turning around* Um... sis...",

        # OS script8:7696
        "No one ever thought you were useless, Annie. But after this? D-Damn, even less so.":
            "No one ever thought you were useless, sis. But after this? D-Damn, even less so.",

        # OS script8:7713
        "Bye, bye, [mc]!":
            "Bye, bye, bro!",

        # AS script8:7778
        "Why...? Come on, [mc], you've met up with Annie solo a hundred times, why the jitters now?!":
            "Why...? Come on, [mc], you always have dinner with Annie, why the jitters now?!",

        # ========== START label mod "menurestaurant_mod" backup ==========
            # Full replacement label to rewrite the flashback with Annie in the UK.
            # Below is a backup in case it doesn't trigger.
            # BA/N: Touched up the backup, ngl still a bit half-assed due to a bunch of short lines lol.

        # OS script8:8047
        "You said it yourself. It's just a meal with Annie, like it's been a hundred times over the past 10 years.":
            "You said it yourself. It's just another meal alone with Annie, like we’ve usually had these last 10 years.",

        # OS script8:8051
        "Can't believe it's been that long already.":
            "Can't believe it's been that long since everything changed.",

        # OS IncestLables:8077 labelmod override
        "Oh... well, I didn't buy mine either. My mom did.":
            "Oh... well, I didn't buy mine either. Nancy did.",

        # OS IncestLables:8078 labelmod override
        "She got it for my birthday.":
            "My... nanny. She got it for my birthday.",

        # OS script8:8116
        # "And I'm not really alone, my dad's inside this office registering our new address.":
        #    "And I'm not really alone, my dad's inside this office registering our new address.",

        # OS script8:8125
        "I live here too! My parents have a hotpot restaurant just around the corner! You and Annie should totally come someday!":
            "I live here too! My parents have a hotpot restaurant just around the corner! You should totally come someday! Hey, you wanna come too?",

        # OS script8:8127
        "Who's Annie?":
            "Who are you talking to?",

        # OS script8:8129
        "Annie from school!":
            "The girl!",

        # OS script8:8131
        "Oh... I don't know her. I just arrived here.":
            "Which girl?",

        # OS script8:8133
        "Oh... really? And then why is she here?":
            "The one behind you?",

        # OS script8:8140
        "Hi.":
            "Hey, Annie.",

        # OS script8:8141
        "Are you Annie?":
            "Why aren't you with Grandpa anymore?",

        # OS script8:8144
        "*Whispering* Why isn't she talking...?":
            "Annie?",

        # OS script8:8146
        "*Whispering* I know her from school, but she never talks there either.":
            "Do you know each other?",

        # OS script8:8147
        "*Whispering* I think she's mute.":
            "*Whispering* Is she mute?",

        # OS script8:8155
        "I go to school with Chang. I'm Annie.":
            "I'm Annie, [mc]'s sister.",

        # OS script8:8157
        "Hi Annie. I'm [mc].":
            "This is Chang, Annie.",

        # OS script8:8159 {specific}
        # Excludes script5:1198 (l)
        "Hi [mc].":[
            ("Hi Chang.","script8:8159"),

            # Bonus Mod
            ("Hi Chang.","script8:8278"),

            # Multi Mod
            ("Hi Chang.","script8:8187"),
        ],

        # OS script8:8160
        "D-Did you...":
            "W-We just moved here...",

        # OS script8:8161
        "Did you move here?":
            "Did [mc] already tell you?",

        # OS script8:8162
        "Yep! From the US, with my dad.":
            "Yep! We're from the US.",

        # OS script8:8167
        "You shouldn't be out here alone either, Annie.":
            "Nice to meet you, Annie.",

        # OS script8:8168
        "You could be kidnapped. Or kidnapped and then sold.":
            "You said your grandpa is here too? I don't see him.",

        # OS script8:8170
        "I'm not alone, my dad's over there.":
            "Grandpa's over there.",

        # OS script8:8172
        "He's a businessman. He's doing business calls now.":
            "He's calling a bunch of people to help Dad with the papers and stuff.",

        # OS script8:8174
        "We were gonna see the pandas at the zoo, but... he got a call. So I guess we’re not going anymore.":
            "He's taking too long so I got bored and came over here.",

        # OS script8:8177
        "I like your... h-hair, American boy.":
            "Um... I like your.. s-shirt, Chang.",

        # OS script8:8178
        "And your shirt.":
            "But you look better with it, [mc]!",

        # OS script8:8184
        "N-Not really. I mean... my mom doesn't let me watch it.":
            "Y-Yeah.",

        # OS script8:8185
        "She says those Japanese cartoons aren't for kids.":
            "I like Sailor Moon.",

        # OS script8:8187
        "Oh... too bad.":
            "She wanted to be Sailor Moon for Halloween.",

        # OS script8:8189
        "No problem! Do you wanna play with us?! Let's meet at school tomorrow at lunch and pretend to be something we all know!":
            "Cool! Do you wanna play with us?! Let's meet at school tomorrow at lunch and pretend to be something we all know!",

        # OS script8:8192
        "My mom says superhero movies are too violent.":
            "I don't know that one.",

        # OS script8:8199
        "Haven't seen it. My mom says witchcraft is the devil's work.":
            "Haven't seen it yet.",

        # OS script8:8213
        "Wait... yes! I saw it at my uncle's house!":
            "Wait... yes! We saw it!",

        # OS script8:8264
        "Yeah, I should go before my dad gets mad too.":
            "Guess we still have to wait for Dad...",

        # OS script8:8265
        "Will you... will you be at school tomorrow?":
            "I can't wait for school tomorrow! Will you play with us, too?",

        # OS script8:8273
        "You won't ignore me there...?":
            "And if we don't see Chang, you'll still play with me? You won't leave me alone?",

        # OS script8:8275
        "Of course not. Why would I...?":
            "Of course. Why wouldn't I...?",

        # OS IncestLables:1592 labelmod override
        "I don’t want people to disappear again... like with Mom, and Dalia, and Penny...":
            "I don’t want people to disappear again... Mom left, and now we won't see Dalia, or Nancy, or Penny...",

        # OS script8:8279
        "Promise me we'll be friends!":
            "Promise me we'll be together forever!",

        # OS script8:8283
        "Friends.":
            "I'll always be by your side, sis.",

        # OS script8:8284
        "Friends forever!":
            "Together forever!",

        # OS script8:8287
        "I'll leave now!":
            "I'll go see if Dad is done yet!",

        # OS script8:8288
        "See you tomorrow... [mc]!":
            "Wait here!",

        # OS script8:8293
        "They said there weren’t many kids around here, but it seems like it’s full of weird ones.":
            "We made a friend already... and Annie's starting to smile again...",

        # OS script8:8384
        "Sure thing! It's one Penelope recommended me.":
            "Sure thing! It's one Penny recommended me.",

        # OS script8:8399
        "Actually, just before you got here, I was reminiscing about the day I met you and Chang.":
            "Actually, just before you got here, I was reminiscing about the day we arrived in Europe and met Chang.",

        # OS script8:8403
        "By all means! When I moved to London, I felt like my life was falling apart. You and Chang turned everything around for me.":
            "By all means! When we moved to London, everything felt like it was falling apart. But Chang helped turn that around, and the two of us grew closer than ever.",

        # OS script8:8418
        "And where was I going that day with my dad?":
            "And what were we waiting for?",

        # OS script8:8422 (menu)
        "To the movie theater":
            "For Chang's hotpot restaurant to open",

        # OS script8:8423
        "To the movie theater.":
            "For Chang's hotpot restaurant to open.",

        # OS script8:8424 (menu)
        # l9/N: Changed to be fully compatible with and without either walkthrough
        # BA/N: Not sure why this was originally disabled, but I've reenabled it for the backup
        "To see the pandas at the zoo":
            "{color=[walk_points]}For Dad to finish the registration [annie_pts]",

        # OS script8:8425
        "To see the pandas at the zoo.":
            "For Dad to finish the registration.",

        # OS script8:8426
        "Although... you had to cancel those plans.":
            "You bugged him over and over until he was done.",

        # OS script8:8438 (menu)
        "To play mini golf":
            "For a bus to go see pandas at the zoo",

        # OS script8:8439
        "To play mini golf.":
            "For a bus to go see pandas at the zoo.",

        # ========== END label mod "menurestaurant_mod" backup ==========

        # OS script8:8450
        "Alright, tell me about the first birthday we celebrated together, a couple of years after that.":
            "Alright, tell me what happened on our tenth birthday.",

        # OS script8:8455 {inject}
        "We couldn’t celebrate your birthday because you were sick, so we decided to do a joint birthday celebration three weeks later at Chang’s parents' restaurant.":[
            ("Dad tried to be considerate for once and plan us a big party, but in the end he didn't have the time to do anything.","script8:8455",[
                'a "So we had a late birthday celebration three weeks later at Chang’s parents’ restaurant."'
            ]),

            # Bonus Mod
            ("Dad tried to be considerate for once and plan us a big party, but in the end he didn't have the time to do anything.","script8:8580",[
                'a "So we had a late birthday celebration three weeks later at Chang’s parents’ restaurant."'
            ]),

            # Multi Mod
            ("Dad tried to be considerate for once and plan us a big party, but in the end he didn't have the time to do anything.","script8:8483",[
                'a "So we had a late birthday celebration three weeks later at Chang’s parents’ restaurant."'
            ]),
        ],

        # OS script8:8497
        "D-Darn it, [mc].":
            "D-Darn it, bro.",

        # OS script8:8569
        "After all these years, I think I can read you pretty well.":
            "We've been together our whole lives, I think I can read you pretty well.",

        # OS script8:8617
        "Your answer could shape how the rest of tonight goes and... maybe even your relationship with Annie.":
            "Your answer could shape how the rest of tonight goes and... maybe even your relationship with your sister.",

        # OS script8:8769
        #"*Standing up* Are you alright, Annie?":
        #    "*Standing up* Are you alright, sis?",

        # OS script8:8791
        "Nancy, Penny, Dalia, Luna, Alex, Nova...":
            "Luna, Alex, Nova, even Nancy, Penny, and Dalia...",

        # OS script8:8839
        #"I’m sorry, Annie. I swear I didn't–":
        #    "I’m sorry, sis. I swear I didn't–",

        # OS script8:8845
        "I'm so impressed, Annie.":
            "I'm so impressed, sis.",

        # OS script8:9084
        "Annie Winters.":
            "Annie [lastname].",

        # OS script8:9155
        "The way you’re tracing your finger on my chest is kind of turning me on more than it should, Annie...":
            "The way you’re tracing your finger on my chest is kind of turning me on more than it should, sis...",

        # OS script8:9200
        "After so many years thinking I’d never be more than friends with Annie... it's finally happening.":
            "After so many years thinking we’d never be more than siblings... it's finally happening.",

        # OS script8:9225
        "Phew... you sure know how to drive me crazy, Annie.":
            "Phew... you sure know how to drive me crazy, sis.",

        # OS script8:9275
        "You climb on top of Annie, trailing passionate kisses along her neck as she moans softly in appreciation.":
            "You climb on top of your sister, trailing passionate kisses along her neck as she moans softly in appreciation.",

        # OS script8:9292
        "You take a moment to contemplate Annie's plump, virgin pussy lips.":
            "You take a moment to contemplate your sister's plump, virgin pussy lips.",

        # OS script8:9313
        "*Moans* Ohh mmmm-y-yes, [mc]...":
            "*Moans* Ohh mmmm-y-yes, bro...",

        # OS script8:9382, also overwrites script8:9494
        "*Tracing Annie's figure* Oh, babe...":
            "*Tracing Annie's figure* Oh, sis...",

        # OS script8:9451
        "*Sobbing* Maybe we're just not compatible.":
            "*Sobbing* Maybe... maybe this is a sign that it was wrong for us to be together after all.",

        # OS script8:9515
        "*Panting* Ohh, [mc]...":
            "*Panting* Ohh, bro...",

        # OS script8:9530
        "You’ve got me all kinds of messed up with how great you look, Annie...":
            "You’ve got me all kinds of messed up with how great you look, sis...",

        # OS script8:9540
        #"Oh, trust me, you've seen nothing yet, my love...":
        #    "Oh, trust me, you've seen nothing yet, sis...",

        # OS script8:9543
        "I-I can't handle this unbearable teasing anymore, Annie...":
            "I-I can't handle this unbearable teasing anymore, sis...",

        # OS script8:9559 {specific}
        # Excludes other lines (d)(x)(no)(l)
        "Oh babe...":[
            ("Oh sis...","script8:9559"), #annie

            # Bonus Mod
            ("Oh sis...","script8:9690"), #annie

            # Multi Mod
            ("Oh sis...","script8:9588"), #annie
        ],

        # OS script8:9583 {inject} WIP
        #"*Moans* I can feel it...":[
        #    ("*Moans* I can feel it...","script8:9583",[
        #        'a "*Giggles* We’re finally connected..."'
        #    ]),
        #],

        # OS script8:9591
        "You're doing great, babe...":
            "You're doing great, sis...",

        # OS script8:9614
        "Oh babe, y-you feel so good...":
            "Oh Annie, y-you feel so good...",

        # OS script8:9636
        # Overwritten by AS script2:3865, okay
        # "Oh Annie..." -> "Oh sis..."

        # OS script8:9639
        "*Panting* I-I'm cumming, [mc]...":
            "*Panting* I-I'm cumming, bro...",

        # OS script8:9696
        "Not really, but that's not an exact science. You know that.":
            "Not really, but that's not an exact science. Plus we’re siblings, so we especially can’t be taking risks.",

        # OS script8:9872
        "You thrust deeply into Annie once more, letting yourself be engulfed by her warmth as your hands explore her, memorizing every ridge and curve of her body.":
            "You thrust deeply into your sister once more, letting yourself be engulfed by her warmth as your hands explore her, memorizing every ridge and curve of her body.",

        # OS script8:9944
        "My perfect, beautiful, innocent little Miss Winters...":
            "My perfect, beautiful, innocent little twin sister...",

        # OS script8:9964
        "*Panting* F-Fuck, me too, babe...":
            "*Panting* F-Fuck, me too, sis...",

        # OS script8:9974
        #"*Panting* I WANT... YOUR... S-S-SEED INSIDE OF ME...":
        #    "*Panting* I WANT... MY BROTHER'S... S-S-SEED INSIDE OF ME...",

        # OS script8:9999
        "T-That was... almost a religious experience, Annie.":
            "T-That was... almost a religious experience, sis.",

        # OS script8:10057
        "You came over and helped me study, even though you missed a football game with some other kids from school because of it.":
            "You stayed home and helped me study, even though you missed a football game with some other kids from school because of it.",

        # OS script8:10069
        "B-But I've liked you since the day I met you!":
            "B-But I've always liked you!",


    # -----------------------------------------
    # v0.9 script9.rpy

        # OS script9:432 (p)
        "*Grumbling to herself* I had a feeling something was going on between him and Nova. Or Annie. Or even Luna, for that matter!":
            "*Grumbling to herself* I had a feeling something was going on between him and Nova. Or Alex. Or even Luna, for that matter!",

        # OS script9:3008
        "Our...":
            "My...",

        # OS script9:3009
        "Our friend disappeared.":
            "My brother disappeared.",

        # OS script9:3014
        "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit some family for a few days!":
            "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit your father again for a few days!",

        # OS script9:3016
        "His only family is a drunk skunk of a father living an ocean away.":
            "Our father is a drunk skunk of a man living an ocean away.",

        # OS script9:3272
        "I can't live without him, Nova.":
            "I don't know how to live without him, Nova.",

        # OS script9:9919
        # Original non-inject version
        #"Annie flew back to the UK a few days ago to spend Christmas with her family and all, but she’s gonna be back before New Year’s Eve.":
        #    "Annie flew back to the UK a few days ago. Our grandparents invited us over for Christmas for the first time since we were kids.{p}Annie accepted their invite, but I already saw them when I went back recently so I'm staying here. She’s gonna be back before New Year’s Eve.",

        # OS script9:9919 {inject}
        "Annie flew back to the UK a few days ago to spend Christmas with her family and all, but she’s gonna be back before New Year’s Eve.":[
            ("Annie flew back to the UK a few days ago to spend Christmas with our grandparents. They haven’t been able to invite us over for the holidays since we were kids, so Annie took them up on the offer.","script9:9919",[
                'mc "I already saw them when I went back to the UK, so I’m staying here this time. Annie’s gonna be back before New Year’s Eve."'
            ]),

            # Bonus Mod
            ("Annie flew back to the UK a few days ago to spend Christmas with our grandparents. They haven’t been able to invite us over for the holidays since we were kids, so Annie took them up on the offer.","script9:9983",[
                'mc "I already saw them when I went back to the UK, so I’m staying here this time. Annie’s gonna be back before New Year’s Eve."'
            ]),

            # Multi Mod
            ("Annie flew back to the UK a few days ago to spend Christmas with our grandparents. They haven’t been able to invite us over for the holidays since we were kids, so Annie took them up on the offer.","script9:9927",[
                'mc "I already saw them when I went back to the UK, so I’m staying here this time. Annie’s gonna be back before New Year’s Eve."'
            ]),
        ],

        # OS script9:9941
        "Nova's doing the family thing too.":
            "Nova's got family visiting.",

        # OS script9:10030
        "Annie flew back to London for a few days to spend Christmas with her family — same with Nova and Luna.":
            "Annie flew back to London for a few days to spend Christmas with our grandparents, while Nova and Luna have family visiting for the holidays.",

        # OS script9:10117
        "Last Christmas, I had a cold kebab in the kitchen while my dad passed out on the couch in the middle of his tenth beer.":
            "Last Christmas, Annie and I had cold kebabs in the kitchen while our dad passed out on the couch in the middle of his tenth beer.",

        # OS script9:10424
        "Christmas never felt special to me.":
            "We never really celebrated it. Annie still enjoys the idea of it, but for me, Christmas never felt very special.",

        # OS script9:10706 chat:626
        "But I really gotta go now or my dad will get mad {image=images/MENUS/e_tongue2.png}":
            "But I really gotta go now or grandpa will get mad {image=images/MENUS/e_tongue2.png}",

        # OS script9:12870
        "I’ve never had a Christmas dinner like this before, Nan.":
            "I wish Annie was here for this, she's missing out on quite the feast!",

        # OS script9:12871
        "Feels really special.":
            "We’ve never had a Christmas dinner like this before, Nan. Feels really special.",
    }

    annie_half_sister_map = {
        # -----------------------------------------
        # Annie as half-sister, result of Dad cheating while on business trips to the UK. Add on to base map.
        # No last name changes as Nancy and Annie's mom keep their maiden names
        # Annie's dad becomes Annie's uncle (mom's brother)
        # Done by Alenissmart initially, additional edits by BlueArrow
        # Al/N: Sorry but I am too lazy to write an entire new map, so I decided to copy the twin sister map and do edits to make it fit the half sister setting
        # -----------------------------------------
        # HS script:0000 = Half Sister map, RPY file:Line Number
        #     Numbers based on v0.9.5, subject to change in future updates
        # Tags based who the line is about contextually, not always the speaker.
        # Selectively applied for clarification
        # (menu) = Choice menu line
        # (mc) = MC line
        # (n) = Nancy line
        # (p) = Penelope line
        # (d) = Dalia line
        # (a) = Annie line
        # (x) = Alex line
        # (l) = Luna line
        # (no) = Nova line
        # (ca) = Calypso line
        # -----------------------------------------
        # Code tags
        # {specific} = use of Variant 2 to target specific lines
        # {inject} = use of Variant 3 to inject new lines      
        # -----------------------------------------
        # LW/N = Lucifer_W's notes
        # Al/N = Alenissmart's notes
        # l9/N = l9453394's notes
        # BA/N = BlueArrow's notes
        # -----------------------------------------

    # -----------------------------------------
    # v0.1 script.rpy

        # HS script:951
        "That’s actually why we ended up moving to the UK; Dad needed to relocate there to keep his position.":
            "Things went south when Mom discovered that many of his so-called \"work trips\", were to be with his second wife and family in the UK. This led to a huge quarrel and an ugly divorce.",

        # HS script:952
        "I know, I know, this all sounds pretty gloomy... but don't worry! This is not about to be one long sob story.":
            "Dad somehow managed to get custody of me while my two older sisters stayed with Mom. He took me with him when he relocated to live with his other family in the UK. I know it sounds a bit bleak, but don't worry—this isn't a sob story.",

        # HS script:956
        "Even after moving, my father continued to work all day. I could never really blame him, though.":
            "The same can't be said of my dad's second marriage, though. It never really worked out, so he soon divorced once again, leaving my father with only me under his care.",

        # HS script:957
        "He had to work to support us both. Heaven knows where I'd be without him.":
            "Despite his other problems, at least he didn't fail to support us both economically. Heaven knows where I'd be without him.",

        # HS script:1046
        "(Annie is a close friend from my childhood.)":
            "(Annie is my half-sister.)",

        # HS script:1047
        "(When I moved from Kredon, she was my next-door neighbor and the first person I met, along with Chang.)":
            "(When we moved from Kredon, she was the first person I met, along with Chang.)",

        # HS script:1048
        "(We quickly bonded after discovering we both had something in common... the absence of our parents.)":
            "(Living in the same semi-functional family, albeit not for long, naturally made us really close.)",

        # HS script:1049
        "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them.)":
            "(It was a chaotic time and we gave each other stability.)",

        # HS script:1051
        "(After finding a companion within each other, we’ve been inseparable ever since.)":
            "(Even after our parents divorced, we've been as inseparable as ever.)",

        # HS script:1053
        "(Because of how close we were, people always believed we were dating... but the truth is, we're just friends.)":
            "(Because of how close we were, people always joked we would've make a great couple... but the truth is, we're just siblings.)",

        # HS script:1054
        "(I mean… she's cute, and we love spending time with each other, but I've never tried to make a move on her.)":
            "(. . .)",

        # HS script:1055
        "(I could never do it.)":
            "(Well you know... I mean if...)",

        # HS script:1056
        "(She'd probably freak out if I did.)":
            "(NO. Stop it. She'd probably freak out if I did.)",

        # HS script:1059
        "(It would be... weird for us. Yeah! That's the word. Weird.)":
            "(It would be... so weird for us. Yeah! She's still my sister after all.)",

        # HS script:1060
        "(It's just not the kind of relationship we have.)":
            "(Why am I even thinking about this!?)",

        # HS script:1089
        "(Come to find out, she actually had 2 rooms available, so Annie will have a place to stay as well!)":
            "(Come to find out, she actually had not only my old room, but also an extra room available, so Annie will have a place to stay as well!)",

        # HS script:1090
        "(She’s actually been the one who’s been coordinating with Nancy over the phone, even though they didn’t know each other beforehand.)":
            "(She’s actually been the one who’s been coordinating with Nancy over the phone, and things seem to be well despite the complicated family matter.)",

        # HS script:1093
        "Do you think she will like me?":
            "Do you think she will like me? I mean, considering all those things between her and Dad...",

        # HS script:1095
        "Nancy? Of course!":
            "Mom? Of course she's going to like you! You don't have to burden yourself with Dad's mistake.",

        # HS script:1096
        "Don't worry about it, Annie. I haven't seen her in over 10 years, so it’ll probably feel like I’m meeting her for the first time too!":
            "She was never a petty person, and despite not seeing her in over 10 years, I'm sure she hasn't changed in that aspect.",

        # HS script:1157
        "You should go to sleep too, Annie. We have to wake up early tomorrow.":
            "You should go to sleep too, sis. We have to wake up early tomorrow.",

        # HS script:1179
        "You're nothing but a big ball of envy because your best friend can play Eternum and you can't since you didn't save any money.":
            "You're nothing but a big ball of envy because your favorite sister can play Eternum and you can't since you didn't save any money.",

        # HS script:1184
        "B-Best friend?":
            "F-Favorite?",

        # HS script:1185
        "I thought I was your best friend, [mc]!":
            "I thought I was your favorite, [mc]!",

        # HS script:1190
        "I'm not your best friend?":
            "I'm not your favorite?",

        # HS script:1192
        "Um... well, yeah, of course you’re my best friend Annie!":
            "Um... well, yeah, of course you’re my favorite Annie!",

        # HS script:1195
        "You're both my best friends!":
            "You're both my favorite people!",

        # HS script:1199
        "Yeah, who's your {i}bestest{/i} friend, me or Chang?":
            "Yeah, who's your {i}favorite{/i}, me or Chang?",

        # HS script:1200
        "T-They're different kinds of friendship!":
            "T-They're different kinds of favorite!",

        # HS script:1201
        "Who is the {b}ONE TRUE{/b} best friend?!":
            "Who is the {b}ONE TRUE{/b} favorite?!",

        # HS script:1220
        "But that doesn't mean you aren’t also my best friend, Annie!":
            "But that doesn't mean you aren’t also my favorite {i}sister{/i}, Annie!",

        # HS script:1240
        "We've been through too much together, Annie.":
            "We've literally lived under the same roof, Annie.",

        # HS script:1244
        "But that doesn't mean you aren’t also my best friend, Chang!":
            "But that doesn't mean you aren’t also my favorite, Chang. You are my best friend!",

        # HS script:1254
        "You're my best... male friend!":
            "You're my favorite... non-family!",

        # HS script:1344
        "I know you're excited Annie, but I'd appreciate it if you could at least carry your hand baggage!":
            "I know you're excited sis, but I'd appreciate it if you could at least carry your hand baggage!",

        # HS script:1757
        "Mission failed, [mc]...":
            "Mission failed, bro...",

        # HS script:1775
        # BA/N: Disabled, BM script:2115 exists
        # "I've prepared a room for each of you, though I must warn you – don't expect anything fancy. The bedrooms are pretty small.":
        #     "I've prepared a room for each of you, though I must warn you – don't expect anything fancy. Remember your old room, [mc]?",

        # HS script:2762
        "Oh yeah, that sounds like Annie. I guess she already told you she also plays Eternum?":
            "Oh yeah, that sounds like sis. I guess she already told you she also plays Eternum?",

        # HS script:2798
        "(Annie was always good at making friends.)":
            "(Sis was always good at making friends.)",

        # HS script:2799
        "(I guess I should let them walk to school on their own, since I don't wanna look like a jealous boyfriend or something.)":
            "(I guess I should let them walk to school on their own, since I don't wanna look like the cliche overprotective brother.)",

        # HS script:2934
        "The lady said no.":
            "Her brother. And she said no.",

        # HS script:2910
        "The lady said no, buddy.":
            "Hands off my sister, you jerk.",

        # HS script:2952, also overwrites script4:4803, okay
        "Are you okay, Annie?":
            "Are you okay, sis?",

        # HS script:2996
        "Will you be alright, Annie?":
            "Will you be alright, sis?",

        # HS script:3006
        "And... thank you again for helping me out back there, [mc].":
            "And... thank you again for helping me out back there, bro.",

        # HS script:5200
        "Tomorrow you'll finally be connected to Eternum, [mc]! After waiting for so many years!":
            "Tomorrow you'll finally be connected to Eternum, bro! After waiting for so many years!",

        # HS script:5331
        "Goodnight [mc]!!":
            "Goodnight, bro!!",

        # HS script:5583 (n) {inject}
        "(I mean... If Dalia and Penelope never found out, then would it really be so bad? It’d be our little secret...)":[
            ("(I mean... If the girls never found out, then would it really be so bad...?)","script:5583",[
                "show ale 31",
                'n "(What am I thinking?! Of course it would be! He’s my son...)" with dis06'
            ]),

            # Bonus Mod
            ("(I mean... If the girls never found out, then would it really be so bad...?)","script:5649",[
                "show ale 31",
                'n "(What am I thinking?! Of course it would be! He’s my son...)" with dis06'
            ]),

            # Multi Mod
            ("(I mean... If the girls never found out, then would it really be so bad...?)","script:5584",[
                "show ale 31",
                'n "(What am I thinking?! Of course it would be! He’s my son...)" with dis06'
            ]),
        ],

        # HS script:6093
        "Let's go! We're already late!":
            "Let's go, bro! We're already late!",

        # HS script:6147
        "Sorry! Did that hurt?!":
            "Sorry, bro! Did that hurt?!",

        # HS script:6179, also overwrites script:6728, script4:6902, both okay
        "Annie?!":
            "Hey, sis?!",

        # HS script:6511
        "(Dammit, Annie didn't tell me about any of this...)":
            "(Dammit, sis didn't tell me about any of this...)",

        # HS script:6606
        "By the way, your outfit looks awesome!":
            "By the way, your outfit looks awesome, sis!",

        # HS script:6695
        "No, he's not! He's [mc]! He's tough!":
            "No, he's not! He's my brother! He's tough!",

        # HS script:6697
        "So this is the [mc] you're always talking about?":
            "So this is the brother you're always talking about?",

        # HS script:6728
        # Overwritten by HS script:6179, okay
        # "Annie?!" -> "Hey, sis?!"

        # HS script:6810
        "Thank god I have you, Annie... I’d probably be lost in a ditch somewhere without you!":
            "Thank god I have you, sis... I’d probably be lost in a ditch somewhere without you!",

        # HS script:7130
        "(That's a bad idea...)":
            "(Nope, bad idea. She's my sister!)",

        # HS script:7176
        "(Jeez, I've always tried to not think of Annie in \"that\" way because I don't want to ruin our friendship, but now...)":
            "(Jeez, I've always tried to not think of Annie in \"that\" way because I don't want to ruin our relationship, but now...)",

        # HS script:7179
        "(She's got curves in all the right places...)":
            "(She's not the skinny kid she used to be... she's got curves in all the right places now...)",

        # HS script:7186
        "(Damn... I guess she’s not the skinny kid she used to be...)":
            "(Dammit... Stop looking at your sister, [mc]...)",

        # HS script:7977
        "Oh... Come on Annie, it doesn't matter!":
            "Oh... Come on sis, it doesn't matter!",

        # HS script:8102
        "Erm... Y-You're the best friend ever!":
            "Erm... Y-You're the best brother ever!",

        # HS script:8103
        "I'm glad you like it, Annie.":
            "I'm glad you like it, sis.",

        # HS script:8467
        "Thank you so much for playing with me, [mc]. It means a lot.":
            "Thank you so much for playing with me, bro. It means a lot.",

        # HS script:8468
        "The pleasure was all mine, Annie. Eternum is awesome. I’m so grateful I had you by my side.":
            "The pleasure was all mine, sis. Eternum is awesome. I’m so grateful I had you by my side.",

        # HS script:8525 (p)
        "You know, I'm not gonna lie, when Mom told me that you and Annie were gonna live with us for a while, I got a little annoyed.":
            "You know, I'm not gonna lie, when Mom told me that you and Annie were gonna live with us for a while, I was a little annoyed, mostly because of all the things with Dad... Which I know was silly, since it neither of you were to blame.",

        # HS script:8526 (p)
        "But hey, I’m glad to say I was wrong. Both of you breathe so much life into this house. It almost feels like you've always lived here.":
            "But hey, I’m glad we're all still able to get along. Both of you breathe so much life into this house. It almost feels like you've always lived here.",


    # -----------------------------------------
    # v0.2 script2.rpy

        # HS script2:40
        "I have a feeling this shit is much bigger than we think, Annie.":
            "I have a feeling this shit is much bigger than we think, sis.",

        # HS script2:52
        "*Whispering* I don't like this, Annie...":
            "*Whispering* I don't like this, sis...",

        # HS script2:82
        "I don't know, Annie... him having a stroke? I'm not buying it.":
            "I don't know, sis... him having a stroke? I'm not buying it.",

        # HS script2:106
        "*Laughs* Don't mind him...":
            "*Laughs* Don't mind my brother...",

        # ========== START label mod "versiontwo_mod" ==========
            # edit of lines added by "versiontwo_mod"
        # REPLACED BY INJECTION, old code left just in case

        # HS IncestLables:2500
        #"Same to you. You must be Annie, [mc]'s told me about you.":
        #    "Same to you. You must be Annie, one of his sisters. [mc]'s told me about you.",

        # HS IncestLables:2502
        #"Yep! I heard [mc] managed to win a neural implant at your cafe!":
        #    "Yep! I heard my brother managed to win a neural implant at your cafe!",

        # HS script2:112 {inject} (replaces labelmod)
        "It's so nice to meet you, Luna!":[
            ("It's so nice to meet you, Luna!","script2:112",[
                "scene aaa 15",
                'l "Same to you. You must be Annie, one of his sisters. [mc]’s told me about you."',
                "scene aaa 14"
            ]),

            # Bonus Mod
            # script2:112, same as original

            # Multi Mod
            # script2:112, same as original
        ],

        # HS script2:113 use with inject
        "I heard [mc] managed to win a neural implant at your cafe!":
            "Yep! I heard my brother managed to win a neural implant at your cafe!",

        # ========== END label mod "versiontwo_mod" ==========

        # HS script2:113 disable if using inject
        #"I heard [mc] managed to win a neural implant at your cafe!":
        #    "I heard my brother managed to win a neural implant at your cafe!",

        # HS script2:126
        "Can I play with you guys, [mc]?!":
            "Can I play with you guys, bro?!",

        # HS script2:133
        "Horror? Okay... maybe it'd be better if you didn't join us, Annie.":
            "Horror? Okay... maybe it'd be better if you didn't join us, sis.",

        # HS script2:167
        "But you're not allowed to complain if you’re scared, Annie!":
            "But you're not allowed to complain if you’re scared, sis!",

        # HS script2:1014
        "Annie should be waiting for us already.":
            "Your sister should be waiting for us already.",

        # HS script2:1117
        "I love your outfit, Annie!":
            "I love your outfit, sis!",

        # HS script2:1389
        "Y-You're scaring me, [mc].":
            "Y-You're scaring me, bro.",

        # HS script2:1965
        "It's okay Annie, I know you’re not one for spooky things, but you’ve been doing good! I’m proud of you!":
            "It's okay sis, I know you’re not one for spooky things, but you’ve been doing good! I’m proud of you!",

        # HS script2:2905
        "What about you, Annie?":
            "What about you, sis?",

        # HS script2:3339
        "(Yeah, nice job impressing [mc] in Eternum, Annie.)":
            "(Yeah, nice job impressing your brother in Eternum, Annie.)",

        # HS script2:3408
        "Oh, [mc]! I wasn’t sure if you were asleep already!":
            "Oh, hey bro! I wasn’t sure if you were asleep already!",

        # HS script2:3418
        "I told you! You shouldn't have played in Luna's server, Annie! You can't handle that scary stuff! Remember when we played Dead Space?":
            "I told you! You shouldn't have played in Luna's server, sis! You can't handle that scary stuff! Remember when we played Dead Space?",

        # HS script2:3474
        "You can sleep here as many times as you want. You don’t even have to ask, alright?":
            "You can sleep here as many times as you want. You don’t even have to ask, alright? Just like when we were little.",

        # HS script2:3479
        "Anytime, Annie.":
            "Anytime, sis.",

        # HS script2:3504
        "G-Goodnight, [mc].":
            "G-Goodnight, bro.",

        # HS script2:3506
        "Goodnight Annie.":
            "Goodnight sis.",

        # HS script2:3518
        "(Oh yeah... I forgot that Annie came to sleep in my room.)":
            "(Oh yeah... I forgot that sis came to sleep in my room.)",

        # HS script2:3526
        "(She's probably used to hugging a pillow while she sleeps, or something.)":
            "(I remember seeing her hugging a teddy bear at night when we still lived together, so that's probably why she grabbed me.)",

        # HS script2:3530
        "(We're in quite an... intimate position... I don't want her to think I'm trying to take advantage of her while she sleeps.)":
            "(We're in quite an... intimate position... I don't want her to think I'm trying to take advantage of her while she sleeps, especially since I'm her brother for Christ's sake.)",

        # HS script2:3545
        "A-Are you awake, Annie?":
            "A-Are you awake, sis?",

        # HS script2:3564
        "Oh... I didn't know about Baloo.":
            "Oh... I think I remember seeing Baloo before.",

        # HS script2:3594
        "(He probably just sees me as the little girl who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)":
            "(He probably just sees me as his little sister who still plays with stuffed animals... the tiny little thing who’s barely tall enough to ride a rollercoaster.)",

        # HS script2:3595
        "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack.)":
            "(I can't blame him. He probably prefers real women... taller ones, over 5'5 at least, with a big butt and a nice rack. And not blood-related ones... he's not a weirdo like me who has feelings for their sibling.)",

        # HS script2:3596
        "(I'll always just be Annie, the \"best friend\".)":
            "(I'll always just be Annie, the \"little sister\".)",

        # HS script2:3602
        "(I'm a fucking mess. She needs someone more mature.)":
            "(I'm a fucking mess. She needs someone more mature... And someone not blood-related... she's not a weirdo like me who has feelings for their sibling.)",

        # HS script2:3607
        "(This is why I'll always just be [mc], the \"best friend\"...)":
            "(This is why I'll always just be [mc], the \"big brother\"...)",

        # HS script2:3630
        "I'm not s-shy...":
            "I'm not s-shy... It’s just a shirt after all, right...?",

        # HS script2:3631
        "It’s just a shirt after all, right...?":
            "I-It’s not like we haven't seen each other naked before...",

        # HS script2:3633
        "(I'm not sure where she’s going with all of this...)":
            "(Yeah, but... not since we last bathed together when we were nine.)",

        # HS script2:3634
        "(But I sure as hell want to find out...)":
            "(I'm not sure where she’s going with all of this... But I sure as hell want to find out...)",

        # HS script2:3642
        "(This doesn't seem like the Annie I’ve known since I was young... Is she trying to prove something?)":
            "(This doesn't seem like the sister I know... Is she trying to prove something?)",

        # HS script2:3644
        "(...No. You’re a woman now, Annie. It’s time to prove it to yourself... and prove it to [mc].) ":
            "(...No. You’re a woman now, Annie. It’s time to prove it to yourself... and prove it to your brother.)",

        # HS script2:3647
        "(Holy shit, I’ve never seen her in such an... intimate way...)":
            "(Holy shit, I never noticed know how much she grew over the past years...)",

        # HS script2:3652
        #"(This is really Annie... {i}my{/i} Annie.)":
        #    "(This is really sis... {i}my{/i} sister.)",

        # HS script2:3658
        "We're just... friends getting a little more comfortable.":
            "We're just... siblings getting a little more comfortable.",

        # HS script2:3672
        "(My precious Annie...)":
            "(My precious sister...)",

        # HS script2:3675
        "Um, [mc]...? Oh man, I must look weird or someth—":
            "Um, bro...? Oh man, I must look weird or someth—",

        # HS script2:3677
        "Annie... you are so... beautiful...":
            "Sis... you are so... beautiful...",

        # HS script2:3703
        "Your skin feels so soft, Annie. It feels... really nice holding you...":
            "Your skin feels so soft, sis. It feels... really nice holding you...",

        # HS script2:3711
        "(Oh my god, am I the only one feeling all this tension in the air? I want to make a move, but... I don’t want to overstep my bounds...)":
            "(Oh my god, am I the only one feeling all this tension in the air? I kind of want to make a move, but... I don’t want to overstep my bounds... I AM her brother after all)",

        # HS script2:3718
        "(But it’s not just any guy. It’s [mc].)":
            "(But it’s not just any guy. It’s [mc]. My brother!)",

        # HS script2:3719
        "(You've had a crush on him since you were nine years old. You’ve been fantasizing about this moment for so long. Now it’s finally here... what are you going to do about it?)":
            "(You've had a crush on him since you were nine years old, even though he's your brother. You’ve been fantasizing about this moment for so long. Now it’s finally here... what are you going to do about it?)",

        # HS script2:3721
        # BA/N: borrowed from stepsis map
        "(But... I don't want to scare her away. Annie has always been so special to me. If I try something and it doesn't work out, I couldn’t bear the thought of losing her...)":
            "(But... I don't want to scare her away. Annie has always been more than a friend, more than a sister to me. If I try something and it doesn't work out, I couldn’t bear the thought of losing her...)",

        # HS script2:3729
        "(Baby steps, [mc]. Baby steps.)":
            "(A-And she's still my sister! It's just not right!)",

        # HS script2:3730
        "Goodnight, Annie.":
            "Goodnight, sis.",

        # HS script2:3732
        "G-Good night, [mc].":
            "G-Good night, bro.",

        # HS script2:3740
        "Um... Annie...?":
            "Um... Sis...?",

        # HS script2:3763
        "I’m sorry, Annie... I can’t help it... you’re driving me insane...":
            "I’m sorry, sis... I can’t help it... you’re driving me insane...",

        # HS script2:3776
        "Oh god, Annie...":
            "Oh god, sis...",

        # HS script2:3792
        "[mc]... Um, I don’t know if I’m ready to go all the way toni-":
            "Bro... Um, I don’t know if I’m ready to go all the way toni-",

        # HS script2:3797
        "I’m sorry. I’m just a little nervous because no one has ever touched me there before, or even seen it, for that matter.":
            "I’m sorry. I’m just a little nervous because no one has ever touched me there before.",

        # HS script2:3800
        "[mc]. I said I’m nervous, but that doesn’t mean I... don’t want to...":
            "Bro. I said I’m nervous, but that doesn’t mean I... don’t want to...",

        # HS script2:3823
        "I’ve never been more sure, Annie.":
            "I’ve never been more sure, sis.",

        # HS script2:3826
        "I thought you weren’t interested in me...":
            "I thought, as your little sister, you weren’t interested in me...",

        # HS script2:3828
        "Where did you get that idea from?":
            "Annie, you've never been just my sister.",

        # HS script2:3830
        "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our friendship.":
            "And I’m not just saying that because I’m finally seeing your gorgeous body. You’ve always been perfect to me... inside and out. I just didn’t want to risk ruining our relationship as brother and sister.",

        # HS script2:3867
        "(Holy shit, this is really happening! I'm fucking Annie's thighs!)":
            "(Holy shit, this is really happening! I'm fucking my sister's thighs!)",

        # HS script2:3872
        "Jesus, Annie...":
            "Jesus, sis...",

        # HS script2:3924
        "Oh shit, I'm sorry, Annie...":
            "Oh shit, I'm sorry, sis...",

        # HS script2:3931
        "Did I do something wrong, Annie? I’m sorry! I didn’t know it was going to be that much!":
            "Did I do something wrong, sis? I’m sorry! I didn’t know it was going to be that much!",

        # HS script2:3942
        "I only came here t-to sleep and then... next thing I know I’m doing that...":
            "I only came here t-to sleep and then... next thing I know I’m doing that... and with my brother...",

        # HS script2:3945
        "No, no! It's okay! You’re good! I like you, Annie! We can...":
            "No, no! It's okay! You’re good! I like you, sis! We can...",

        # HS script2:3952
        "We skipped like 14 steps! In one night!":
            "We skipped like 14 steps and broke a dozen rules! In one night!",

        # HS script2:3965
        "I'm gonna... go... think! Good night [mc]!":
            "I'm gonna... go... think! Good night bro!",

        # HS script2:3981
        "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing Annie’s secret kinky side... and I loved every moment of it!)":
            "(HOLY SHIT! All of that really happened! That was incredible! That was my first time seeing my sister's secret kinky side... and I loved every moment of it!)",

        # HS script2:4474
        "Annie! Do you have a minute? I wanted to talk to you!":
            "Sis! Do you have a minute? I wanted to talk to you!",

        # HS script2:5364 (n)
        "(Even if, somehow, he wanted me too... and we ended up... doing it, Dalia and Penny would be furious if they ever found out.)":
            "(Even if, somehow, he wanted me too... and we ended up... doing it, the girls would be furious if they ever found out. And fucking my son, is that even legal?)",

        # HS script2:5413 (n)
        "(I bet if I tried to do anything at home, Dalia or Penny would surely notice.)":
            "(I bet if I tried to do anything at home, one of the girls would surely notice.)",

        # HS script2:5937 (x)
        "And on the first day of school, I saw him harassing a close friend of mine.":
            "And on the first day of school, I saw him harassing my sister.",

        # HS script2:5938 (x) {inject}
        # BA/N: Funny extra lines, disable if too clunky
        "Honestly, I couldn't help it.":[
            ("Honestly, I couldn't help it.","script2:5938",[
                'show aaz 44',
                'x "Wait, Dalia?" with dis',
                'show aaz 46',
                'mc "Ah, no. Annie, my half-sister... It’s complicated." with dis',
                'show aaz 44',
                'x "How many sisters do you have?" with dis'
                ''
            ]),

            # Bonus Mod
            ("Honestly, I couldn't help it.","script2:6002",[
                'show aaz 44',
                'x "Wait, Dalia?" with dis',
                'show aaz 46',
                'mc "Ah, no. Annie, my half-sister... It’s complicated." with dis',
                'show aaz 44',
                'x "How many sisters do you have?" with dis'
                ''
            ]),

            # Multi Mod
            ("Honestly, I couldn't help it.","script2:5954",[
                'show aaz 44',
                'x "Wait, Dalia?" with dis',
                'show aaz 46',
                'mc "Ah, no. Annie, my half-sister... It’s complicated." with dis',
                'show aaz 44',
                'x "How many sisters do you have?" with dis'
                ''
            ]),
        ],

        # HS script2:5945 (x) use with above
        "Well, I think I respect you a little bit more now because of what you did.":
            "Well, anyway, I think I respect you a little bit more now because of what you did.",

        # HS script2:8306 base map override (p)
        "Um... Yeah. Why? Do you know her?":
            "Um... Yeah. Why? Do you know her?",

        # HS script2:8315 last name override (p)
        "I was wondering why Nancy and her shared the same last name on your followers list. Nancy is her mom!":
            "I was wondering why Nancy and her shared the same last name on your followers list. Nancy is her mom!",

        # HS script2:8318 (p)
        "Never mind...":
            "Oh never mind... Well, actually she's also my sister, but-",

        # HS script2:8320 (p)
        "Can I go say hi?":
            "That's even better then, you can introduce me! Can I go say hi?",

    # -----------------------------------------
    # v0.3 script3.rpy

        # HS script3:3362
        "Good morning, Annie!":
            "Good morning, sis!",

        # HS script3:3368
        "Um... Oh! [mc]! Good morning!":
            "Um... Oh! Bro! Good morning!",

        # HS script3:3400
        "(She's right. Forgetting about this might be the best option right now.)":
            "(She's right. Forgetting about this might be the best option. We crossed way too many lines that night.)",

        # HS script3:3402
        "(That's all I want... just to stay friends with her.)":
            "(That's all I want... just to have a normal sibling relationship with her.)",

        # HS script3:3412
        "That sounds great. Take care, Annie!":
            "That sounds great. Take care, sis!",

        # HS script3:3414
        "Thank you, [mc]. I needed this talk.":
            "Thank you, bro. I needed this talk.",

        # HS script3:3420
        "*Taking a deep breath* (Well [mc], it's now or never. Time to grow a pair and man up!)":
            "*Taking a deep breath* (Well [mc], it's now or never. Time to grow a pair and man up! Oh, and fuck the fact that she is your sister, you're well past that point.)",

        # HS script3:3423
        # BA/N: disabled, using name adds a bit of seriousness here
        #"I like you, Annie.":
        #    "I like you, sis.",

        # HS script3:3431
        "You're my best friend.":
            "You're my sister.",

        # HS script3:3434
        "And in my heart I know, I want us to be so much more than that, too...":
            "But you know what, fuck it I say. I want us to be so much more than that.",

        # HS script3:3446
        "I don't want to lose our friendship, Annie. I’d be miserable without you in my life.":
            "I don't want to lose you, sis. I’d be miserable without you in my life.",

        # HS script3:3449
        "I just want us to stay friends forever!":
            "I just want us to stay together forever!",

        # HS script3:3467
        "That sounds great! Just spending some time together as good friends. Like how we’ve always done it!":
            "That sounds great! Just spending some time together as siblings. Like how we’ve always done it!",

        # HS script3:3483
        "Like... a fun date between friends?":
            "Like... a fun date with your sister?",

        # HS script3:3484
        "Hmmm... no, more like a date with a girl that I like. And I just happen to be so lucky in that, she’s also my best friend too. As for what the future holds? Who knows...":
            "Hmmm... no, more like a date with a girl that I like. As for what the future holds? Who knows...",

        # HS script3:3505
        "Look, [mc], I know we’re going on a {i}date{/i} date, but I really do want to take it slow too. I don’t want you to assume that–":
            "Look, bro, I know we’re going on a {i}date{/i} date, but I really do want to take it slow too. I don’t want you to assume that–",

        # HS script3:3518
        "T-Thank you, [mc]. I needed this talk.":
            "T-Thank you, bro. I needed this talk.",

        # HS script3:3540
        # BA/N: borrowed from stepsis map
        "I know you want to take things slow. And I’m perfectly okay with that.":
            "I know you want to take things slow, sis. And I’m perfectly okay with that.",

        # HS script3:3561
        "That was quite the goodbye for just a couple of... friends.":
            "That was quite the goodbye for just... siblings.",

        # HS script3:3578
        "(Maybe a good movie? Or a walk along the beach. Or even a date in Eternum!)":
            "(Maybe a good movie? Or a walk along the beach. Or even a date in Eternum! We wouldn't have to worry about running into people who know us there.)",

        # HS script3:5080 last name override
        "*Clears throat* Hello, this is Nancy Carter.":
            "*Clears throat* Hello, this is Nancy Carter.",

        # HS script3:9761
        # BA/N: Disabled. makes no sense for Nancy to include someone else's daughter.
        #"What about Dalia and Penelope?":
        #    "What about Dalia, Penelope, and Annie?",

        # HS 29242
        # BA/N: Ditto
        #"Why not? I wouldn’t mind having you as my son-in-law...":
        #    "Why not? I wouldn't mind. I'm sure Annie's mom wouldn't mind as well...",


    # -----------------------------------------
    # v0.4 script4.rpy

        # HS script4:2930 last name override
        "And on my right, weighing in at 125 lbs... Dalia Carter!":
            "And on my right, weighing in at 125 lbs... Dalia Carter!",

        # HS script4:4286
        "(I'm going on a date with [mc]!)":
            "(I'm going on a date with my brother!)",

        # HS script4:4339
        "*Chuckles* I think you're getting too excited about this, Annie. You need to relax. You'll enjoy it more if you take it less seriously!":
            "*Chuckles* I think you're getting too excited about this, sis. You need to relax. You'll enjoy it more if you take it less seriously!",

        # HS script4:4349
        "Gonna play some Eternum with ma' homie...":
            "Gonna play some Eternum with ma' bro...",

        # HS script4:4411
        "Annie? Is that you?":
            "Sis? Is that you?",

        # HS script4:4621
        "Quick, [mc], make a wish!":
            "Quick, bro, make a wish!",

        # HS script4:4803
        # Overwritten by HS script:2952, okay
        # "Are you okay, Annie?" -> "Are you okay, sis?"

        # HS script4:4915
        "I mean... of course we're not. We haven't even...":
            "I mean... of course we're not. We are siblings, after all...",

        # HS script4:4977
        "Come here, [mc]! Jump!":
            "Come here, bro! Jump!",

        # HS script4:4997
        "Annie, you awake? I can go call the Astrocorp employee if we’re ready to wrap this up.":
            "Sis, you awake? I can go call the Astrocorp employee if we’re ready to wrap this up.",

        # HS script4:5004
        "You and Chang have always been my best friends, and neither of you played Eternum until recently, so... I've always felt kind of alone here.":
            "You and Chang have always been by my side, and neither of you played Eternum until recently, so... I've always felt kind of alone here.",

        # HS script4:5008
        "You’re the one who’s really made these first few weeks in Eternum worthwhile, Annie. I couldn't have asked for anyone better to spend time with.":
            "You’re the one who’s really made these first few weeks in Eternum worthwhile, sis. I couldn't have asked for anyone better to spend time with.",

        # HS script4:5112
        "And I felt super welcome in our new home!":
            "And I felt super welcome in your old home!",

        # HS script4:5113
        "Nancy, Penelope, and Dalia are all very nice to me. They treat me as one of the family. You know I’ve always wanted sisters, so I really feel like they’re giving me that experience!":
            "Nancy, Penelope, and Dalia are all very nice to me. I was worried they would hold a grudge against me or my mom, but nothing like that ever happened. They treat me as one of the family!",

        # HS script4:5115
        "Happy to hear that!":
            "I told you that you were thinking too much on the train, didn't I? I'm so happy that you're able to get along with them.",

        # HS script4:5131
        "Oh! Come on, Annie! You can't be serious!":
            "Oh! Come on, sis! You can't be serious!",

        # HS script4:5216
        "*Jumps on the bed* Oh my god, [mc]! Look at this!":
            "*Jumps on the bed* Oh my god, bro! Look at this!",

        # HS script4:5250
        # BA/N: borrowed from stepsis map
        "(Maybe... it's just not the right time yet...?)":
            "(Maybe... was this all a mistake...?)",

        # HS script4:5311 (menu)
        # l9/N: Changed to be fully compatible with and without either walkthrough
        "Decline and stay as friends":
            "{color=[walk_path]}Decline and stay as siblings [red][mt](Closes Annie's path)",

        # HS script4:5314
        "I like you, and you're my best friend, you already know that.":
            "I like you, and you're my sister, you already know that.",

        # HS script4:5315
        "But... I also feel like we're not meant to be more than that. Things would get awkward if we tried to get together, and our friendship is too important to risk, for me at least.":
            "But... I also feel like we're not meant to be more than that. Things would get awkward if we tried to get together, and our relationship is too important to risk, for me at least.",

        # BA/N: next 7 lines borrowed and modified from stepsis map, which rewrote them to be a bit more emotional which I agree with, but tried to keep more of the original lines in it than the stepsis map did.

        # HS script4:5316
        "I just like spending time with you!":
            "I just... Annie, I don’t want these feelings to overwrite all the memories and the relationship we’ve built until now.",

        # HS script4:5317
        "I... I think we're meant to be friends. Best friends!":
            "I am and will always be your brother... but I think we're only meant to be that. Siblings.",

        # HS script4:5318
        "So... let's just stay like this for now, okay?":
            "So... let's just go back to what we always were, okay?",

        # HS script4:5319
        "I just don’t have those feelings for you right now.":
            "I can’t commit to this... {i}thing{/i} between us. Not right now. ",

        # HS script4:5320
        "In the future... who knows? Maybe. But I don’t want to lead you on, either.":
            "In the future... I don’t know. Maybe. But I don’t want to lead you on, either.",

        # HS script4:5326
        "No worries! I totally understand. My head has been all over the place too, you know, with all this back and forth...":
            "It's not your fault, Annie, it's mine. I know I've been sending you mixed signals, bringing you here today. My head has been all over the place too, you know, with all this back and forth... You don't deserve that.",

        # HS script4:5327
        "We can have this conversation again after we gather the 10 Gems!":
            "I'm sorry, sis. This isn't how I wanted today to go. For what it's worth, I still enjoyed spending this time with you.",

        # HS script4:5369
        # BA/N: disabled, original line works for half sis
        #"Y-Yeah... It's been like... 10 years since we first met?":
        #    "Y-Yeah...",

        # HS script4:5371
        #"That’s quite a while... No big deal.":
        #    "No big deal.",

        # HS script4:5382
        "You're so pretty, Annie...":
            "You're so pretty, sis...",

        # HS script4:5395
        "[mc]! What are you doing?!":
            "Bro! What are you doing?!",

        # HS script4:5405
        "Seeing you undressing just for me was hot as fuck, Annie.":
            "Seeing you undressing just for me was hot as fuck, sis.",

        # HS script4:5436
        "But... Do you think I'm NOT nervous? I'm super scared too! I mean, in my arms, I'm holding an adorably precious, absolutely gorgeous girl whom I’ve liked for years.":
            "But... Do you think I'm NOT nervous? I'm super scared too! I mean, in my arms, I'm holding my adorably precious, absolutely gorgeous sister whom I’ve liked for years.",

        # HS script4:5438
        "I know it's scary to get out of your comfort zone, but... I think we can overcome it together.":
            "I know it's a scary, difficult line we're crossing, but... I think we can overcome it together.",

        # HS script4:5442
        "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and stay friends!":
            "That’s how I feel. If you don't feel the same way... we can always go back to where we were a month ago and just be siblings again!",

        # HS script4:5443
        "It’ll be a little awkward at first, but our friendship is strong, and I know we’d be back to normal in no time.":
            "It’ll be a little awkward at first, but our relationship is strong, and I know we’d be back to normal in no time.",

        # HS script4:5471
        "*Caressing her cheek* I feel like I could never get enough of you, Annie...":
            "*Caressing her cheek* I feel like I could never get enough of you, sis...",

        # HS script4:5526
        "God, there are so many things I want to do to Annie right now... but it's still Annie. I don't wanna cross any line too fast.":
            "God, there are so many things I want to do to Annie right now... but she is still my sister. I don't wanna cross any line too fast.",

        # HS script4:5528
        "You're making me so horny, Annie...":
            "You're making me so horny, sis...",

        # HS script4:5604
        "*Panting* K-Keep going, [mc]! Y-You’re hitting just the... r-right spot!":
            "*Panting* K-Keep going, bro! Y-You’re hitting just the... r-right spot!",

        # HS script4:5621
        "Y-You have to stop! S-STOP! [mc]!":
            "Y-You have to stop! S-STOP! BRO!",

        # HS script4:5675
        "You turn me on so much, Annie... I'd be lying if I said I wasn’t rock-hard the whole time...":
            "You turn me on so much, sis... I'd be lying if I said I wasn’t rock-hard the whole time...",

        # HS script4:5724
        "You’re such a good girl, Annie...":
            "You’re such a good girl, sis...",

        # HS script4:5753
        "D-Do you like beating off my cock, Annie?":
            "D-Do you like beating off my cock, sis?",

        # HS script4:5765
        "*Panting* F-Fuck, I won't last much longer, Annie...":
            "*Panting* F-Fuck, I won't last much longer, sis...",

        # HS script4:5767
        "I want to make you cum, [mc]... You were so kind to me...":
            "I want to make you cum, bro... You were so kind to me...",

        # HS script4:5823
        "I want you so bad, Annie... I can’t wait ‘til the day you can finally take this dick... But not yet...":
            "I want you so bad, sis... I can’t wait ‘til the day you can finally take this dick... But not yet...",

        # HS script4:5825
        "W-We’ve g-gotta do some practicing b-beforehand, [mc]...":
            "W-We’ve g-gotta do some practicing b-beforehand, bro...",

        # HS script4:6902
        # Overwritten by HS script:6179, okay
        # "Annie?!" -> "Hey, sis?!"

        # HS script4:6924
        "Oh Annie... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?":
            "Oh sis... I wouldn’t ever do that to you! I care for you way too much... You see how silly you’re being, right?",

        # HS script4:6942
        "Look, Annie! A teleporter! We can get out of here!":
            "Look, sis! A teleporter! We can get out of here!",

        # HS script4:6952
        "*Pulling your shirt* [mc]...":
            "*Pulling your shirt* Bro...",

        # HS script4:6986
        "D-Don't look at him, Annie.":
            "D-Don't look at him, sis.",

        # HS script4:7052
        "*Sobbing* [mc]?":
            "*Sobbing* [mc_dash]?",

        # HS script4:7054
        # BA/N: Disabled for seriousness
        #"D-Don't worry, Annie...":
        #    "D-Don't worry, sis...",

        # HS script4:7250
        "Thank you for an amazing day, [mc].":
            "Thank you for an amazing day, bro.",

        # HS script4:7252
        "I'm glad you enjoyed it, Annie. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.":
            "I'm glad you enjoyed it, sis. Even with the alien attack, and... well, the bloodbath... it was still one of the best days I've ever had.",

        # HS script4:7429
        "Oh, already?! Good luck, [mc]! Be sure to get plenty of information!":
            "Oh, already?! Good luck, bro! Be sure to get plenty of information!",

        # HS script4:7431
        "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what best friends do, I guess.":
            "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what brothers do, I guess.",

        # HS script4:7468
        # BA/N: disabled, original line works better for half sis
        # "I don't know Aunt Cordelia, but I'm good at making collages.":
        #     "I'm good at making collages.",


    # -----------------------------------------
    # v0.5 script5.rpy

        # HS script5:629 last name override
        "Oh, that is very likely, actually, Ms. Carter. It would be poetic and, at the same time, easy to make it look like an accident.":
            "Oh, that is very likely, actually, Ms. Carter. It would be poetic and, at the same time, easy to make it look like an accident.",

        # HS script5:809
        "The scholarship that was granted to [mc] and his best friends is the best thing that has happened to me in a very long time.":
            "The scholarship that was granted to [mc] and his favorite people is the best thing that has happened to me in a very long time.",

        # HS script5:811
        "*Clears throat* I think it's best not to dig too deep into the \"best friend\" subject.":
            "*Clears throat* I think it's best not to dig too deep into the \"favorite\" subject.",

        # HS script5:817
        "I don't really care about the \"best friend\" status anymore, now that [mc] and I are...":
            "I don't really care about the \"favorite\" status anymore, now that [mc] and I are...",

        # HS script5:826
        "N-Now that we are {b}SUPER{/b} best friends!":
            "N-Now that I am his {b}SUPER{/b} favorite!",

        # HS script5:829
        "Super-duper best friends!":
            "Super-duper favorite!",

        # HS script5:830
        "Wait... did [mc] say Chang is his best friend?! And not me?!":
            "Wait... did [mc] say Chang is his favorite?! And not me?!",

        # HS script5:842
        "I don't really mind anymore. I'm happy being just a good friend.":
            "I don't really mind anymore. I'm happy just being his little sister.",

        # HS script5:1005
        "B-Bye, [mc]! I'll see you at home!":
            "B-Bye, bro! I'll see you at home!",

        # HS script5:2044
        "I mean, Dad has only called me once since I got here.":
            "I mean, Dad has only called me once since we got here. Even Annie's mom called me more times.",

        # HS script5:4909 last name override
        "(Penelope Carter... you’re gonna drive me mad.)":
            "(Penelope Carter... you’re gonna drive me mad.)",

        # HS script5:5086 last name override
        "*Chuckles* Don’t be silly! You're staying with us until we say so. No escaping the Carters!":
            "*Chuckles* Don’t be silly! You're staying with us until we say so. No escaping this family!",

        # HS script5:6215 last name override
        "Penelope? Penelope Carter? That IG model in the journalism program?":
            "Penelope? Penelope Carter? That IG model in the journalism program?",

        # HS script5:8184 last name override
        "Actually, yeah! I'm looking for Penelope. Penelope Carter. Do you know her?":
            "Actually, yeah! I'm looking for Penelope. Penelope Carter. Do you know her?",

        # HS script5:8601 last name override
        "Penelope Carter just said that she'd like to have a threesome with me. It's difficult not to be enthusiastic.":
            "Penelope Carter just said she'd like to have a threesome with her brother. How scandalous!",

        # HS script5:9633
        # Disabled, interferes with other lines, also doesn't work if not on other paths
        # "I like where this is going...":
        #    "I like where this is going... and I am too horny to care that she is my sister... as if I had cared with Mom, Dalia, or Annie...",

        # HS script5:9682 last name override
        "Not quite yet, Miss Carter...":
            "Not quite yet, Miss Carter...",

        # HS script5:9765 last name override
        "She's mine... For at least tonight, Penelope Carter is all mine...":
            "She's mine... For at least tonight, Penelope Carter is all mine...",


    # -----------------------------------------
    # v0.6 script6.rpy

        # HS script6:1678
        "How was your father?":
            "How was Dad?",

        # HS script6:1785
        "Good night!!":
            "Good night bro!!",

        # HS script6:1975
        "[mc]...? What are you doing here?!":
            "Bro...? What are you doing here?!",

        # HS script6:2004
        "It's just... that... well, I was shocked at first since we had {i}never{/i} seen each other naked, and all that.":
            "It's just... that... well, I was shocked at first since the last time I saw you naked was {i}so long{/i} ago.",

        # HS script6:2008 (no)
        "A bit striking because I {i}never{/i} saw you naked before either.":
            "A bit striking because I {i}never{/i} saw you naked before.",

        # ========== START Murder Mystery ==========
            # adding this just to note that this section is organized by script line, and does not really reflect the order the events actually play out in game

        # HS script6:3536
        "Elementary, my dear [mc].":
            "Elementary, my dear brother.",

        # HS script6:4970
        "We're just... friends.":
            "Delilah's just... a friend. And Annie's my sister.",

        # HS script6:4975
        "Are you seriously telling me you have those two fun-sized cuties around you and you're not doing anything with them?":
            "What a shame. I couldn't imagine having these two fun-sized cuties around me and not doing anything with them.",

        # HS script6:5504
        "Oh, thanks for the reassurance, [mc]! I feel much, much better now!":
            "Oh, thanks for the reassurance, brother! I feel much, much better now!",

        # ========== END Murder Mystery ==========

        # HS script6:5970
        "*Knocking on the door* Annie?":
            "*Knocking on the door* Sis?",

        # HS script6:6033
        "And how was your dad?":
            "And how was Dad?",

        # HS script6:6035
        "My dad...?":
            "Dad...?",

        # HS script6:6063
        "So... yeah, you know how my father is.":
            "So... yeah, you know how Dad is. He didn't even tell me to say hello to you...",

        # HS script6:6065
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

        # HS script6:6399
        "I... I'm n-not sure I'm ready, [mc].":
            "I... I'm n-not sure I'm ready, bro.",

        # HS script6:6486
        "AAaahh... oh god [mc]... I think I'm gonna... C-CUM...":
            "AAaahh... oh god bro... I think I'm gonna... C-CUM...",

        # HS script6:6488
        "[mc]! You’re gonna make me...":
            "Bro! You’re gonna make me...",

        # HS script6:6657
        # BA/N: Disabled, does not apply to half route
        # "The sweet, innocent, little girl I've known for years...":
        #    "The sweet, innocent, little girl I've known my entire life...",

        # HS script6:6687
        "You better take care of my little girl while you're in the USA, [mc].":
            "You better take care of your sister while you're in the USA, [mc].",

        # HS script6:6688
        # LW/N: Unnecessary for the new version.
        # "Rest assured Mr. Winters, I won’t let anything happen to her!":
        #     "Rest assured Uncle, I won’t let anything happen to her!",

        # HS script6:6689
        "I'll take care of Annie as if she was my sister!":
            "I'll take great care of Annie as always!",

        # HS script6:6700
        "Oh GOD, Annie, I'm gonna fucking cum!":
            "Oh GOD, sis, I'm gonna fucking cum!",

        # HS script6:6718
        "*Panting* Do it... empty y-yourself all over me, [mc]...":
            "*Panting* Do it... empty y-yourself all over me, bro...",

        # HS script6:6719
        "Oh god Annie, I'm...":
            "Oh god sis, I'm...",

        # HS script6:6750
        "Goddammit Annie... that was mind-blowing.":
            "Goddammit sis... that was mind-blowing.",

        # HS script6:6762
        "Imagine if Nancy had caught us... she'd kick us out of the house!":
            "Imagine if Nancy had caught us... she'd kick us, or at least me, out of the house!",

        # HS script6:6766
        "Why would she? We weren't doing anything wrong.":
            "She's just not that type of person.",

        # HS script6:6787
        "Good night, Annie.":
            "Good night, sis.",

        # HS script6:14151 last name override
        "Although... not as much as when you went to Wyatt's house with Nancy Carter, that's for sure.":
            "Although... not as much as when you went to Wyatt's house with your mother, Nancy Carter, that's for sure.",


    # -----------------------------------------
    # v0.7 script7.rpy

        # HS script7:905 last name override
        "Penelope Carter plays Eternum!":
            "Penelope Carter plays Eternum!",

        # HS script7:1031 last name override
        "*Hyperventilating* I left my drawing utensils at the Carter house last time I was there!":
            "*Hyperventilating* I left my drawing utensils at the Carter house last time I was there!",

        # HS script7:1461
        "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, Annie.":
            "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, sis.",

        # HS script7:1502
        "Are you sure you don't want to join us, Annie?":
            "Are you sure you don't want to join us, sis?",

        # ========== START harem thoughts ==========

        # HS script7:7396 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7396",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7452",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7454",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),
        ],

        # HS script7:7398 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7398",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7454",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7456",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),
        ],

        # HS script7:7400 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7400",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7456",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7458",[
                'mct "Well, Dalia’s my sister so that’d be a whole scandal instead. As for the others..."',
            ]),
        ],

        # HS script7:7402 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7402",[
                'mct "Well, Annie’s my half-sister so that’d be a bit of a scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7458",[
                'mct "Well, Annie’s my half-sister so that’d be a bit of a scandal instead. As for the others..."',
            ]),


            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7460",[
                'mct "Well, Annie’s my half-sister so that’d be a bit of a scandal instead. As for the others..."',
            ]),

        ],

        # HS script7:7404 {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7404",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7460",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7462",[
                'mct "Well, two of them are my sisters so that’d be a huge scandal instead. As for the others..."',
            ]),
        ],

        # HS script7:7425 {inject}
        # BA/N: technically this wouldn't work if you're not on any of the incest routes but don't feel like making a labelmod to add if statement just for this
        #    but also why would you be playing an incest mod without following at least one incest path right?
        "I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?":[
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7425",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),

            # Bonus Mod
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7481",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),

            # Multi Mod
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7483",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),
        ],

        # ========== END harem thoughts ==========

        # HS script7:8017 last name override
        "Penelope Carter is my bestie.":
            "Penelope Carter is my bestie.",

        # HS script7:8196 (p)
        "(How would we even explain this to Mom or Dalia?)":
            "(How would we even explain this to Mom or Dalia? Or even Annie?)",

        # HS script7:8338 last name override
        "{sc=2}PENELOPE{w=.5} P. {w=.5}CARTER.{/sc}":
            "{sc=2}PENELOPE{w=.5} P. {w=.5}CARTER.{/sc}",

        # HS script7:8454 last name override
        "I'm [mc] [lastname] – Penelope Carter's representative.":
            "I'm [mc] [lastname] – Penelope Carter's representative.",

        # HS script7:8736 last name override
        "P-Penelope Paige Carter.":
            "P-Penelope Paige Carter.",

        # HS script7:8840 last name override
        "Penelope Paige Carter.":
            "Penelope Paige Carter.",


    # -----------------------------------------
    # v0.8 script8.rpy

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

        # HS script8:6969
        "(She's definitely going on a date with [mc].)":
            "(She's definitely going on a date with [mc]. Her own brother!)",

        # HS script8:6983 (l)
        # BA/N: leaving this here for the future when we learn what exactly Luna's vision was
        # "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)":
        #     "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)",

        # HS script8:7569
        "A-Annie...?":
            "Uh sis...?",

        # HS script8:7696
        "No one ever thought you were useless, Annie. But after this? D-Damn, even less so.":
            "No one ever thought you were useless, sis. But after this? D-Damn, even less so.",

        # HS script8:7713
        "Bye, bye, [mc]!":
            "Bye, bye, bro!",

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

        # HS script8:8425
        "To see the pandas at the zoo.":
            "For Dad to finish the registration so Uncle could take us to to our new home.",

        # HS script8:8426
        "Although... you had to cancel those plans.":
            "You kept bugging the rest of us until Dad was done.",

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

        # HS script8:9155
        "The way you’re tracing your finger on my chest is kind of turning me on more than it should, Annie...":
            "The way you’re tracing your finger on my chest is kind of turning me on more than it should, sis...",

        # HS script8:9200
        "After so many years thinking I’d never be more than friends with Annie... it's finally happening.":
            "After so many years thinking we’d never be more than siblings... it's finally happening.",

        # HS script8:9225
        "Phew... you sure know how to drive me crazy, Annie.":
            "Phew... you sure know how to drive me crazy, sis.",

        # HS script8:9313
        "*Moans* Ohh mmmm-y-yes, [mc]...":
            "*Moans* Ohh mmmm-y-yes, bro...",

        # HS script8:9382 and HS script8:9494
        "*Tracing Annie's figure* Oh, babe...":
            "*Tracing Annie's figure* Oh, sis...",

        # HS script8:9451
        "*Sobbing* Maybe we're just not compatible.":
            "*Sobbing* Maybe... maybe this is a sign that it was wrong for us to be together after all.",

        # HS script8:9515
        "*Panting* Ohh, [mc]...":
            "*Panting* Ohh, bro...",

        # HS script8:9540
        "Oh, trust me, you've seen nothing yet, my love...":
            "Oh, trust me, you've seen nothing yet, sis...",

        # HS script8:9582
        "*Moans* Oh good grief, it's IN...":
            "*Moans* Oh good grief, it's IN... I can feel it...",

        # HS script8:9583
        "*Moans* I can feel it...":
            "*Moans* My brother’s finally inside of me...",

        # HS script8:9639
        "*Panting* I-I'm cumming, [mc]...":
            "*Panting* I-I'm cumming, bro...",

        # HS script8:9974
        "*Panting* I WANT... YOUR... S-S-SEED INSIDE OF ME...":
            "*Panting* I WANT... MY BROTHER'S... S-S-SEED INSIDE OF ME...",

        # HS script8:10069
        "B-But I've liked you since the day I met you!":
            "B-But I've liked you since the first day!",

        # HS script8:13437
        "You think Nancy wants to play the role of some sort of intermediary? Because she wants it too?":
            "\"Mom\" huh? Kinky. So, you think \"Mom\" wants to play the role of some sort of intermediary? Because she wants it too?",

        # HS script8:13439
        "Exactly! That's what she implied.":
            "It's not... never mind. But yes, that's exactly what she implied.",


    # -----------------------------------------
    # v0.9 script9.rpy

        # HS script9:432 (p)
        "*Grumbling to herself* I had a feeling something was going on between him and Nova. Or Annie. Or even Luna, for that matter!":
            "*Grumbling to herself* I had a feeling something was going on between him and Nova. Or Alex. Or even Luna, for that matter!",

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
            "But I really gotta go now or my mom will get mad {image=images/MENUS/e_tongue2.png}",

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
        # Done by l9453394, with lw & ba for v0.6 onwards
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
        # These tags aren't based on who's speaking, but who the line and scene are about.#
        # -----------------------------------------
        # Code tags
        # {specific} = use of Variant 2 to target specific lines
        # {inject} = use of Variant 3 to inject new lines      
        # -----------------------------------------
        # l9/N = l9453394's notes
        # LW/N = Lucifer_W's notes
        # BA/N = BlueArrow's notes
        # -----------------------------------------
        
    # -----------------------------------------
    # v0.1 script.rpy Nancy aunt/Penelope & Dalia cousin lines
        
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
    # v0.2 script2.rpy Nancy aunt/Penelope & Dalia cousin lines
        
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
    # v0.3 script3.rpy Nancy aunt/Penelope & Dalia cousin lines
        
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
        
        # AU script3:6005 (p) {specific}
        # Excludes script:1493 (chang)
        "She's perfect...":[
            ("She's... my cousin is... perfect...","script3:6005"),

            # Bonus Mod
            ("She's... my cousin is... perfect...","script3:6049"),

            # Multi Mod
            ("She's... my cousin is... perfect...","script3:6016"),
        ],
        
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
        # BA/N: side note but looking into it, incest was still taboo for roman nobility lol. Not sure if you want to take that into account or not.
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
    # v0.4 script4.rpy Nancy aunt/Penelope & Dalia cousin lines
        
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
        
        # AU script4:4192 chat:950 (chat) (p)
        "Thanks [mc]  {image=images/MENUS/e_heart.png}":
            "Thanks little cuz  {image=images/MENUS/e_heart.png}",

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
    # v0.5 script5.rpy Nancy aunt/Penelope & Dalia cousin lines
        
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
            "*Whispering* Honestly, the fact that we're related makes it {i}{b}so {/b}{/i}much more exciting!",
        
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
    # v0.6 script6.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU script6:1569 (d)
        "My god, did Dalia's ass get even bigger while I was in the UK? Or... rounder?":
            "My god, did my cousin's ass get even bigger while I was in the UK? Or... rounder?",

        # AU script6:1808 (n)
        "*Snorts* Of course you’d say that! I'm afraid I'll have to shower alone today, my insatiable stud.":
            "*Snorts* Of course you’d say that! I'm afraid I'll have to shower alone today, my insatiable nephew.",

        # AU script6:7752 (n)(p)
        "Nancy and Penelope definitely have some competition in that department...":
            "Nancy and Penelope definitely have some competition in that department... not that I should be sizing up my own aunt and cousin like that.",

        # AU script6:9413 (d)
        #"It's a battle of wits, my friend.":
        #    "It's a battle of wits, cousin/cuz.",

        # AU script6:10483 (d)
        "(I can't believe I really asked him to go down on me. Alex is such a bad influence, I shouldn't listen to her.)":
            "(I can't believe I really asked my own cousin to go down on me. Alex is such a bad influence, I shouldn't listen to her.)",

        # AU script6:10598 (d)
        #"(With [mc].)":
        #    "(With [mc]. My own cousin.)",

        # AU script6:10887 (d)
        #"(He's... the one...)":
        #    "(He's... the one... even if we're...)",


    # -----------------------------------------
    # v0.7 script7.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU script7:422 (d)
        "*Snorts* Don't worry, I'm kidding, I'm kidding!":
            "*Snorts* Don't worry, I'm kidding, I'm kidding! I mean, he's your cousin, right?",

        # AU script7:422 (p)
        "I can't believe I actually got to shove my cock between Penny's massive tits at the party.":
            "I can't believe I actually got to shove my cock between my cousin's massive tits at the party.",

        # ========== START harem thoughts ==========
            # includes annie stepsister logic for convenience since it's part of the same map

        # AU script7:7396 (other) {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7396",[
                'mct "Well, two of them are my family so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7452",[
                'mct "Well, two of them are my family so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, Annie, or Alex are a little more than just “pals”.","script7:7454",[
                'mct "Well, two of them are my family so that’d be a huge scandal instead. As for the others..."',
            ]),
        ],

        # AU script7:7398 (other) {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7398",[
                'mct "Well, two of them are my family so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7454",[
                'mct "Well, two of them are my family so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Annie are a little more than just “pals”.","script7:7456",[
                'mct "Well, two of them are my family so that’d be a huge scandal instead. As for the others..."',
            ]),
        ],

        # AU script7:7400 (other) {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7400",[
                'mct "Well, Dalia’s my cousin so that’d be bit of a scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7456",[
                'mct "Well, Dalia’s my cousin so that’d be a bit of a scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Dalia, or Alex are a little more than just “pals”.","script7:7458",[
                'mct "Well, Dalia’s my cousin so that’d be a bit of a scandal instead. As for the others..."',
            ]),
        ],

        # AU script7:7402 (other) {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7402",[
                'mct "Well, Annie’s my stepsister so that’d be quite a scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7458",[
                'mct "Well, Annie’s my stepsister so that’d be quite a scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Luna, Annie, or Alex are a little more than just “pals”.","script7:7460",[
                'mct "Well, Annie’s my stepsister so that’d be quite a scandal instead. As for the others..."',
            ]),
        ],

        # AU script7:7404 (other) {inject}
        "Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.":[
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7404",[
                'mct "Well, two of them are my family so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Bonus Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7460",[
                'mct "Well, two of them are my family so that’d be a huge scandal instead. As for the others..."',
            ]),

            # Multi Mod
            ("Hmm, I wonder what the gang at school would say if they knew me and Dalia, Annie, or Alex are a little more than just “pals”.","script7:7462",[
                'mct "Well, two of them are my family so that’d be a huge scandal instead. As for the others..."',
            ]),
        ],

        # AU script7:7425 (other) {inject}
        # BA/N: technically this wouldn't work if you're not on any of the incest routes but don't feel like making a labelmod to add if statement just for this
        #    but also why would you be playing an incest mod without following at least one incest path right?
        "I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?":[
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7425",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),

            # Bonus Mod
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7481",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),

            # Multi Mod
            ("I mean... I'm not “officially” dating anyone, and no one's popped the exclusive question, so... I'm not doing anything wrong, am I...?","script7:7483",[
                'mct "Besides the incest... but if we both want it, then it’s fine, right?"',
            ]),
        ],

        # ========== END harem thoughts ==========

        # AU script7:7766 (p)
        "I've come to recognize that horndog expression by now, [mc].":
            "I've come to recognize that horndog expression by now, little cuz.",

        # AU script7:8137 (p)
        "What are you talking about, he's not my step-anything.":
            "What are you talking about? He's my cousin, not my step-brother.",

        # AU script7:8196 (p)
        "(How would we even explain this to Mom or Dalia?)":
            "(How would we even explain this to Mom or Dalia? “Hey, guess who I hooked up with — my own cousin”?)",

        # AU script7:8202 (p)
        "(You can't be fixated on [mc] like some teenage crush, Penny. There's plenty more fish in the sea!)":
            "(You can't be fixated on your own cousin like some teenage crush, Penny. There's plenty more fish in the sea that aren't blood-related!)",

        # ========== START car photoshoot / first time ==========

        # AU script7:9257 (p)
        "I'm glad I have a friend who I trust and with whom I can do these kinds of things, [mc].":
            "I'm glad I have a cousin who I trust and with whom I can do these kinds of things, [mc].",

        # AU script7:9319 (p)
        "*Sitting on the car* Are you okay? Your mind seems to be elsewhere, [mc].":
            "*Sitting on the car* Are you okay, little cuz? Your mind seems to be elsewhere.",

        # AU script7:9325 (p)
        "I'd never let another man see you in your most glorious form.":
            "I'd never let another man see you in your most glorious form. Then again, I'm not exactly “another man”, am I?",

        # AU script7:9360 (p)
        "We're just humans after all. We have a history together, and this is quite an... explicit session.":
            "We're just humans after all. We're cousins, sure, but we have a history together, and this is quite an... explicit session.",

        # AU script7:9453 (p)
        "Let's cross this line... just once.":
            "Let's cross this line... the one line we probably shouldn't... just once.",

        # AU script7:9454 (p)
        "And after this... the game will be over. It will be... our secret.":
            "And after this... the game will be over. It will be... our own little family secret.",

        # AU script7:9502 (p)
        "I'm having sex with her. I’m fucking Penelope Carter.":
            "I'm having sex with her. I’m fucking my own cousin, Penelope Carter.",

        # AU script7:9503 (p)
        "I'm living out the fantasy of what her 180,000 followers can only dream of.":
            "I'm living out the fantasy of what her 180,000 followers can only dream of. Not that any of them know she's my cousin.",

        # AU script7:9507 (p)
        "*Giggles* Oh y-yeah? You thought about this...? Thought about fucking little old me?":
            "*Giggles* Oh y-yeah? You thought about this...? Thought about fucking your own cousin?",

        # AU script7:9527 (p)
        "You can feel Penelope's tight cavity slowly adjust to your size. Each of her movements feels extra sensitive on your dick.":
            "You can feel your cousin's tight cavity slowly adjust to your size. Each of her movements feels extra sensitive on your dick.",

        # AU script7:9576 (p)
        "Penny’s jiggling, voluptuous body fills your every sense, as each individual bounce and thrust causes your body to radiate with a divine pleasure.":
            "Your cousin’s jiggling, voluptuous body fills your every sense, as each individual bounce and thrust causes your body to radiate with a divine pleasure.",

        # AU script7:9596 (p)
        "Fuck me hard, [mc]...":
            "Fuck me hard, cuz...",

        # AU script7:9599 (p)
        "You keep hammering Penelope's pussy, your ears drowning in her small, constant whimpers of pleasure.":
            "You keep hammering your cousin's pussy, your ears drowning in her small, constant whimpers of pleasure.",

        # AU script7:9631 (p)
        "Penelope orgasms, soaking your cock in vaginal fluids and contracting all of her muscles at once.":
            "Your cousin orgasms, soaking your cock in vaginal fluids and contracting all of her muscles at once.",

        # AU script7:9646 (p)
        "Man, I can't believe I just fucked Penny.":
            "Man, I can't believe I just fucked my own cousin.",

        # AU script7:9675 (p)
        "Split me in half...":
            "Split me in half, little cuz...",

        # AU script7:9826 (p)
        "Crush me against this car, [mc]...":
            "Crush me against this car, cuzzy...",

        # ========== END car photoshoot / first time ==========


    # -----------------------------------------
    # v0.8 script8.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU script8:4087 (d) {VO}
        "{cps=17}Our hero was unable to resist the sight of his old friend's ample bosom and alluring figure.{cps=0.6} {cps=16}Overwhelmed by desire, he accepted her offer and surrendered himself to her embrace.":
            "{cps=17}Our hero was unable to resist the sight of his cousin's ample bosom and alluring figure.{cps=0.6} {cps=16}Overwhelmed by desire, he accepted her offer and surrendered himself to her embrace.",

        # AU script8:5024 (n)
        "You two... what?":
            "You two... but you're his.. w-what?",

        # AU script8:5031 (n)
        "Holy shit, I-I really didn't expect that.":
            "Holy shit, that's crazy. I-I really didn't expect that.",

        # AU script8:5527 (n)
        "*Pulling Nancy towards you* Hmph...":
            "*Pulling your aunt towards you* Hmph...",

        # AU script8:8078 (n)
        "My... nanny. She got it for my birthday.":
            "My aunt. She got it for my birthday.",

        # ========== START Dalia first time (fireplace scene) ==========
        # l9/N: kept light on purpose, same as the rest of Dalia's path — she and MC barely acknowledge it out loud

        # AU script8:15454 (d)
        "Sh-Should we really do it?":
            "Sh-Should we really do it? I mean... we're cousins, [mc]...",

        # AU script8:15671 (d)
        "*Panting* That the childhood friend I used to p-play with would end up ramming her p-perfect, huge ass down on my cock...":
            "*Panting* That the cousin I used to play with as a kid would end up ramming her p-perfect, huge ass down on my cock...",

        # AU script8:15871 (d)
        "We... connected. As if we had been lovers for years.":
            "We... connected. I guess it makes sense, though. We've basically been family for years — just, well... in a very different way now.",

        # ========== END Dalia first time (fireplace scene) ==========

        
    # -----------------------------------------
    # v0.9 script9.rpy Nancy aunt/Penelope & Dalia cousin lines

        # AU script9:446 (d)
        "I’D STILL HAVE APPRECIATED IT IF MY SISTER HAD TOLD ME SHE WAS SCREWING MY FUCKING BOYFRIEND!":
            "I’D STILL HAVE APPRECIATED IT IF MY SISTER HAD TOLD ME SHE WAS SCREWING OUR OWN FUCKING COUSIN!",

        # AU script9:448 (p)
        "Oh, so he's {i}your{/i} boyfriend now.":
            "Oh, so now he's suddenly {i}your{/i} cousin more than mine?",

        # AU script9:3016 (mc)
        # BA/N: ST version takes priority
        #"His only family is a drunk skunk of a father living an ocean away.":
        #    "His only other family is a drunk skunk of a father living an ocean away.",

        # ========== START blindfold cabin scene ==========

        # AU script9:11613 (other)
        "I mean, it’s 2034. This probably isn’t the freakiest thing you’ll see on the street nowadays.":
            "I mean, it’s 2034. This probably isn’t the freakiest thing you’ll see on the street nowadays. And it’s not like relationships between cousins were ever that unusual so...",

        # AU script9:11704 (p)
        "Genetics are on my side, [mc].":
            "Genetics are on my side, cuz.",

        # AU script9:11776 (p)
        "*Snorts* Looks like you should’ve invested another thousand hours in Skyrim, [mc].":
            "*Snorts* Looks like you should’ve invested another thousand hours in Skyrim, little cuz.",

        # AU script9:11814 (p)
        "*Snorts* You're such a pervert, [mc]. You ever think about anything besides sex?":
            "*Snorts* You're such a pervert, cuz. You ever think about anything besides sex?",

        # AU script9:11911 (p)
        "You press your lips against Penelope's neck, trailing soft kisses over her skin as your hands slide over her curves.":
            "You press your lips against your cousin's neck, trailing soft kisses over her skin as your hands slide over her curves.",

        # AU script9:12000 (p)
        "You instinctively take Penelope's nipple into your mouth. She arches her back with a soft moan, starting to stroke you with deliberate, slow pumps.":
            "You instinctively take your cousin's nipple into your mouth. She arches her back with a soft moan, starting to stroke you with deliberate, slow pumps.",

        # AU script9:12014 (p)
        "I just want to devour every single inch of you... down to the very last freckle...":
            "I just want to devour every single inch of my own cousin... down to the very last freckle...",

        # AU script9:12089 (p)
        "You should learn to savor the moment, [mc]...":
            "You should learn to savor the moment, little cuz...",

        # AU script9:12117 (p)
        "*Giggles* You’re not secretly recording me, right? Taking advantage of little old blind Penny...?":
            "*Giggles* You’re not secretly recording me, right? Taking advantage of your own little blind cousin...?",

        # AU script9:12135 (p)
        "Penelope's mouth finally closes around your cock.":
            "Your cousin's mouth finally closes around your cock.",

        # AU script9:12303 (p)
        #"Such a bad girl...":
        #    "Wanting my own cousin to fuck me...",

        # AU script9:12338 (p)
        "You sink your cock into Penelope — slick, warm, and indescribably tight.":
            "You sink your cock into your cousin — slick, warm, and indescribably tight.",

        # AU script9:12345 (p)
        "F-Fuck, I love you Penny...":
            "F-Fuck, I love you Penny... and I don't care that you're my cousin...",

        # AU script9:12381 (p)
        "You lift Penelope's leg up in the air, and slam back into her with brutal force, the thrumming sounds of your bodies colliding and liquids sloshing radiating through the room.":
            "You lift your cousin's leg up in the air, and slam back into her with brutal force, the thrumming sounds of your bodies colliding and liquids sloshing radiating through the room.",

        # AU script9:12466 (p)(d)
        # B/N: Disabled, Dalia is Penny's sister so this makes no sense
        #"Have you ever... fucked Dalia's ass?":
        #    "Have you ever... fucked our cousin Dalia's ass?",

        # AU script9:12500 (p)
        "I wanna be your first.":
            "I wanna be your first, cuz.",

        # ========== END blindfold cabin scene ==========

        # AU script9:13632 (p)
        #"Thank you for your very... scientific, articulate observation, [mc].":
        #    "Thank you for your very... scientific, articulate observation, cuz.",

        # AU script9:14585 (other)
        "Like... three of us are literally family here, so...":
            "Like... four of us here are related, so...",

        # AU script9:14586 (other)
        "I guess we can just skip ahead and give the points to [mc] and Alex.":
            "I guess we can just skip ahead and give the points to Alex.",

        # AU script9:14594 (mc)
        "F-Fine, fine... let's give [mc] his ego boost.":
            "F-Fine, fine... let's give this pervert his ego boost.",

        # AU script9:14608 (misc)
        "Well... I’d never ever dare to suggest anything that could get pearl-clutching credit card companies offended, so I'll say Alex, and...":
            "Well... As much as I’d like to avoid anything that could get pearl-clutching credit card companies offended, my options here are limited, so I'll say Alex, and...",

        # AU script9:15202 (p)
        "You... YOU HAVE TOO–?!":
            "You... YOU HAVE TOO–?! But he's your cousin!",

        # AU script9:15280 (p)
        "No. No, no... no. Not really.":
            "No. No, no... no. Of course not.",

        # ========== START sauna scene ==========
        # BA/N: Added lines of Alex pushing the incest angle from mom map just to play up the kink since Dalia and MC dont usually acknowledge it. disable if others disagree

        # AU script9:15835 (d)
        "I-I mean... it’s a little weird with [mc] here too, but... whatever." :
            "I-I mean... it’s a little weird with my cousin here too, but... whatever." ,

        # AU script9:16042 (d)
        "Just... don't get any weird ideas.":
            "Just... don't get any weird ideas. We're still cousins...",

        # AU script9:16051 (d)
        "*Touching herself* AAaah... t-this is so fucking hot, Dal...":
            "*Touching herself* AAaah... watching you j-jerk off your cousin is so fucking hot, Dal......",

        # AU script9:16137 (d)
        "What? N-No.":
            "What? O-Of course not! We're cousins!",

        # AU script9:16185 (d)
        "*Whispering* You’re a dirty, horny slut who wants to be fucked until you can’t think straight.":
            "*Whispering* You’re a dirty, horny slut who wants to be fucked by your cousin until you can’t think straight.",

        # AU script9:16232 (d)
        "Are Dalia's tits big enough for you?":
            "Are your cousin's tits big enough for you?",

        # AU script9:16277 (d)
        "Tell me, [mc]... do you wanna fuck Dalia...?":
            "Tell me, [mc]... do you wanna fuck your cousin...?",

        # AU script9:16425 (x)
        "*Giggles* Your mouth is asking to slow down, but those eyes rolling back are screaming “fuck me harder, [mc]”...":
            "*Giggles* Your mouth is asking to slow down, but those eyes rolling back are screaming “fuck me harder, cuz”...",

        # AU script9:16457 (d)
        "*Grinning* It's like having a live porno in front of me...":
            "*Grinning* I'm watching a live incest porno in front of me...",

        # ========== END sauna scene ==========

        # AU script9:17003 (d)(p)
        "W-Well, when you say it like that it sounds a little bit weird, but...":
            "W-Well, us being cousins is weird enough as it is, so...",

        # AU script9:17004 (d)(p)
        "Y-Yeah, kinda. Maybe. I guess.":
            "Sharing him can't be that much worse. Maybe. I guess.",

    # -----------------------------------------
    # Annie Stepsister Map
        # -----------------------------------------
        # Annie as stepsister, MC's dad remarried in UK
        # Combined with Nancy as aunt (mother's sister), Penelope and Dalia as cousins in annie_aunt_map
        # No name changes
        # Original map
        # (Probably) incompatible with other maps
        # -----------------------------------------
        # Annie stepsister character notes
        # 
        # - Annie: Only add references to not being blood-related during lines where they waver on sibling boundaries. 
        #       - Note: Never use "stepsibling" in their dialogue, especially when it gets emotional. 
        #       - Their relationship is 100% brother and sister, even if they're not biologically related. 
        #       - The "step-" doesn't matter to them in terms of boundaries. 
        #       - They should only call each other "big bro" and "little sis" in intimate lines as a little "younger sister" kick, and they usually just refer to each other by name. 
        #      - this path is the most emotionally incestuous, since they have a much more intimate relationship than anyone else.
        # -----------------------------------------
        # ST = Annie stepsister lines in annie_aunt_map
        # script:0000 = file name:line number
        # (menu) = Choice menu line
        # (chat) = Phone chat line
        # (n) = Nancy line
        # These tags aren't based on who's speaking, but who the line and scene are about.
        #-----------------------------------------
        # Code tags
        # {specific} = use of Variant 2 to target specific lines
        # {inject} = use of Variant 3 to inject new lines      
        # -----------------------------------------
        # l9/N = l9453394's notes
        # LW/N = Lucifer_W's notes
        # BA/N = BlueArrow's notes
        # -----------------------------------------
        
        
    # -----------------------------------------
    # v0.1 script.rpy Annie stepsister lines
        
        # ST script:1046
        "(Annie is a close friend from my childhood.)":
            "(Annie is my stepsister.)",
        
        # ST script:1047
        "(When I moved from Kredon, she was my next-door neighbor and the first person I met, along with Chang.)":
            "(When we moved from Kredon, she and her mother were our next-door neighbors, and she was the first person I met, along with Chang.)",
        
        # ST script:1049
        "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them.)":
            "(Her father was a traveling salesman and her mother was a flight attendant, so she almost never got to see the two of them, especially after they got divorced.)",
        
        # ST script:1050
        "(We were both lost... and lonely.)":
            "(Even after my dad and her mom married each other, nothing really changed for us—just one more absent parent. We were both still lost... and lonely.)",
        
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
        
        # ST script:2952, also overwrites script4:4803
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
    # v0.2 script2.rpy Annie stepsister lines
        
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
    # v0.3 script3.rpy Annie stepsister lines
        
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
    # v0.4 script4.rpy Annie stepsister lines
        
        # ST script4:4335
        "(A date with [mc]!)":
            "(A date with my big brother!)",
        
        # ST script4:4336
        "(A date in Eternum WITH [mc]!)":
            "(A date in Eternum WITH my big brother!)",
        
        # ST script4:4803
        # Overwritten by ST script:2952, okay
        # "Are you okay, Annie?" -> "Are you okay, sis?"

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
            "Annie has been distant, but I'm happy to see her smile. I guess that's all I need for now. That's what brothers do, I guess.",
        
        
    # -----------------------------------------
    # v0.5 script5.rpy Annie stepsister lines
        
        # ST script5:842
        "I don't really mind anymore. I'm happy being just a good friend.":
            "I don't really mind anymore. I'm happy just being his little sister.",
        
        # ST script5:12104 (n)
        "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters would take the news.":
            "*Chuckles* Let's keep these dreams of yours between us, though. I don’t know how my daughters or your sister would take the news.",
        
        
    # -----------------------------------------
    # v0.6 script6.rpy Annie stepsister lines
        
        # ST script6:2004
        "It's just... that... well, I was shocked at first since we had {i}never{/i} seen each other naked, and all that.":
            "It's just... that... well, I was shocked at first since the last time I saw you naked was {i}so long{/i} ago.",

        # ST script6:2008 (no)
        "A bit striking because I {i}never{/i} saw you naked before either.":
            "A bit striking because I {i}never{/i} saw you naked before.",

        # ========== START Murder Mystery ==========
            # adding this just to note that this section is organized by script line, and does not really reflect the order the events actually play out in game

        # ST script6:3536
        "Elementary, my dear [mc].":
            "Elementary, my dear brother.",

        # ST script6:4970
        "We're just... friends.":
            "Delilah's just... a friend. And Annie's my sister.",

        # ST script6:4975 (misc)
        "Are you seriously telling me you have those two fun-sized cuties around you and you're not doing anything with them?":
            "What a shame. I couldn't imagine having these two fun-sized cuties around me and not doing anything with them.",

        # ========== END Murder Mystery ==========

        # ST script6:6063
        "So... yeah, you know how my father is.":
            "So... yeah, you know how Dad is. He didn't even tell me to say hello to you...",

        # ST script6:6090
        "W-Well... it's true that my dad has been working a lot all his life and he's been a bit absent, but... he's always cared about me.":
            "W-Well... it's true that my dad was always working a lot all his life and he was a bit absent, but... he's always cared about me.",

        # ========== START annie room scene ==========

        # ST script6:6338
        "I’ll never get tired of seeing your gorgeous body, Annie.":
            "I’ll never get tired of seeing your gorgeous body, sis.",

        # ST script6:6426
        "I’m dying to taste you, Annie.":
            "I’m dying to taste you, sis.",

        # ST script6:6427
        "[mc], I... I-I'm not sure if I'm ready for that either!":
            "Big bro, I... I-I'm not sure if I'm ready for that either!",

        # ST script6:6472
        "Annie's body language screams of ecstasy as you continue attacking her swollen clit.":
            "Your little sister's body language screams of ecstasy as you continue attacking her swollen clit.",

        # ST script6:6481
        "But I have to resist the urge, for now. I know Annie better than herself, and I know she’s really close but not quite ready to go all the way.":
            "But I have to resist the urge, for now. I know my little sister better than she knows herself, and I know she’s really close but not quite ready to go all the way.",

        # ST script6:6486
        "AAaahh... oh god [mc]... I think I'm gonna... C-CUM...":
            "AAaahh... oh god big bro... I think I'm gonna... C-CUM...",

        # ST script6:6488
        "[mc]! You’re gonna make me...":
            "Bro! You’re gonna make me...",

        # AS script6:6559
        "I can feel you pulsing, [mc]...":
            "I can feel you pulsing, big bro...",

        # ST script6:6657
        "The sweet, innocent, little girl I've known for years...":
            "My sweet, innocent, little sister...",

        # AS script6:6666
        "Come on Annie, you're gonna miss the entire movie!":
            "Come on sis, you're gonna miss the entire movie!",

        # ST script6:6689
        "I'll take care of Annie as if she was my sister!":
            "I'll always take care of my little sister!",

        # ST script6:6718
        "*Panting* Do it... empty y-yourself all over me, [mc]...":
            "*Panting* Do it... empty y-yourself all over me, big bro...",

        # ST script6:6719
        "Oh god Annie, I'm...":
            "Oh god sis, I'm...",

        # ST script6:6750
        "Goddammit Annie... that was mind-blowing.":
            "Goddammit sis... that was mind-blowing.",

        # ST script6:6766 (n)
        "Why would she? We weren't doing anything wrong.":
            "She's just not that type of person.",

        # ST script6:6787
        "Good night, Annie.":
            "Good night, sis.",

        # ========== END annie room scene ==========

    # -----------------------------------------
    # v0.7 script7.rpy Annie stepsister lines

        # ST script7:1461
        "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, Annie.":
            "Well, I don’t want to be the only one without a compliment, but I have to say, I absolutely love your hair, sis.",

        # ST script7:1468 {specific}
        # Excludes script:7779 (eva)
        "Thank you, [mc]...":[
            ("Thank you, big bro...","script7:1468"),

            # Bonus Mod
            ("Thank you, big bro...","script7:1480"),

            # Multi Mod
            # script7:1468, same as original
        ],

        # ========== START harem thoughts ==========
            # included in aunt map section for convenience since it's part of the same map
        # ========== END harem thoughts ==========

    # -----------------------------------------
    # v0.8 script8.rpy Annie stepsister lines

        # ST script8:4231
        "Thank you for making me look so adorable!":
            "Thank you for making me look so adorable, big bro!",

        # ST script8:6969
        "(She's definitely going on a date with [mc].)":
            "(She's definitely going on a date with [mc]. Her own brother!{p}...well, {i}step{/i}-brother... if that makes it any better...)",

        # ST script8:6983 (l)
        # BA/N: leaving this here for the future when we learn what exactly Luna's vision was
        # "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)":
        #     "(And I... actually seemed to be enjoying myself in that vision. We all were. Which is... strange. I've almost always seen bad things.)",

        # ST script8:7092
        "It's straightforward yet stylish, giving off a confident vibe. It shows you're not desperate but also considerate enough to dress well for a date with someone who's been your second-best friend for so many years.":
            "It's straightforward yet stylish, giving off a confident vibe. It shows you're not desperate but also considerate enough to dress well for a date with your own sister, after all these years.",

        # ST script8:8047
        "You said it yourself. It's just a meal with Annie, like it's been a hundred times over the past 10 years.":
            "You said it yourself. It's just a meal with your sister, like it's been a hundred times over the past 10 years.",

        # ST script8:8617
        "Your answer could shape how the rest of tonight goes and... maybe even your relationship with Annie.":
            "Your answer could shape how the rest of tonight goes and... maybe even your relationship with your sister.",

        # ========== START romantic dinner / first time ==========

        # ST script8:9200
        "After so many years thinking I’d never be more than friends with Annie... it's finally happening.":
            "After so many years thinking I’d never be more than her brother... it's finally happening.",

        # ST script8:9313
        "*Moans* Ohh mmmm-y-yes, [mc]...":
            "*Moans* Ohh mmmm-y-yes, big brother...",

        # ST script8:9370
        "[mc], I'm g-gonna cum...":
            "Big bro, I'm g-gonna cum...",

        # ST script8:9543
        "I-I can't handle this unbearable teasing anymore, Annie...":
            "I-I can't handle this unbearable teasing anymore, sis...",

        # ST script8:94571
        "You slowly start pushing yourself into Annie's petite body.":
            "You slowly start pushing yourself into your sister's petite body.",

        # ST script8:9589
        "I'm finally taking Annie's virginity...":
            "I'm finally taking my little sister's virginity...",

        # ST script8:9944
        "My perfect, beautiful, innocent little Miss Winters...":
            "My perfect, beautiful, innocent little sister...",

        # ST script8:9974
        "*Panting* I WANT... YOUR... S-S-SEED INSIDE OF ME...":
            "*Panting* I WANT MY... BIG BROTHER'S... S-S-SEED INSIDE OF ME...",

        # ST script8:10057
        "You came over and helped me study, even though you missed a football game with some other kids from school because of it.":
            "You stayed home and helped me study, even though you missed a football game with some other kids from school because of it.",

        # ========== END romantic dinner / first time ==========

    # -----------------------------------------
    # v0.9 script9.rpy Annie stepsister lines

        # ST script9:3008
        "Our...":
            "My...",

        # ST script9:3009
        "Our friend disappeared.":
            "My brother disappeared.",

        # ST script9:3014
        "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit some family for a few days!":
            "She mentioned he sometimes plays Eternum for hours on end, right? Or maybe he just went to visit his father again for a few days!",

        # ST script9:3016
        "His only family is a drunk skunk of a father living an ocean away.":
            "His father is a drunk skunk of a man living an ocean away.",

        # ST script9:10706 chat:626
        # BA/N: like HS map, mom seems like better fit
        "But I really gotta go now or my dad will get mad {image=images/MENUS/e_tongue2.png}":
            "But I really gotta go now or my mom will get mad {image=images/MENUS/e_tongue2.png}",


    }

    _build_replace_map_cache = {}
    _build_replace_map_flags = None

    def _build_replace_map():
        """
        Build the active replacement map from flags, cached until flags change.
        """
        global _build_replace_map_cache, _build_replace_map_flags
        incest_enabled = bool(getattr(renpy.store, 'annie_incest', False))
        sister_enabled = bool(getattr(renpy.store, 'annie_sister', False))
        mom_enabled    = bool(getattr(renpy.store, 'annie_mom', False))
        half_enabled   = bool(getattr(renpy.store, 'annie_half_sister', False))
        aunt_enabled   = bool(getattr(renpy.store, 'annie_aunt', False))
        current_flags  = (incest_enabled, sister_enabled, mom_enabled, half_enabled, aunt_enabled)

        if current_flags == _build_replace_map_flags and _build_replace_map_cache:
            return _build_replace_map_cache

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

        _build_replace_map_flags = current_flags
        _build_replace_map_cache = mapping
        return mapping

# -----------------------------------------
# Helpers + Replacer
# -----------------------------------------
init python:
    import re

    # Cache for resolved player name / lastname — only changes at character creation
    _in_display_cache = {}          # {"mc": str, "lastname": str}
    _in_display_cache_keys = {}     # snapshot of store values used to build the cache

    # Cache for _im_sync_adad_alias — only needs to run when mode flags change
    _in_adad_sync_flags = None

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

    def _im_get_current_say_raw_text():
        ast_mod = _in_ast_module
        if ast_mod is None:
            return None
        try:
            ctx = renpy.game.context()
            node_id = getattr(ctx, "current", None)
            if not node_id:
                return None
            node = renpy.game.script.lookup(node_id)
        except Exception:
            return None
        SayCls = getattr(ast_mod, "Say", None)
        if SayCls is None or not isinstance(node, SayCls):
            return None
        raw_what = getattr(node, "what", None)
        if isinstance(raw_what, str):
            return raw_what
        return None

    def _im_matches_active_say_text(text):
        active = getattr(store, "_im_active_say_text", None)
        if not isinstance(text, str) or not isinstance(active, str):
            return False
        try:
            active_cmp = _im_strip_bonusmod_tags(_im_strip_multimod_tags(active, force=True))
            text_cmp = _im_strip_bonusmod_tags(_im_strip_multimod_tags(text, force=True))
        except Exception:
            active_cmp = active
            text_cmp = text
        if _in_normalize_equiv_text(active_cmp) == _in_normalize_equiv_text(text_cmp):
            return True
        return (
            _in_normalize_equiv_text(_in_strip_tags(active_cmp))
            == _in_normalize_equiv_text(_in_strip_tags(text_cmp))
        )

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

    # Pre-compiled Nancy substitution patterns — declared before _in_transform_text
    # so they are available when the function runs.
    _in_nancy_possessive_re = re.compile(r"\bNancy['']s\b")
    _in_nancy_re = re.compile(r"\bNancy\b")

    # Pre-normalized skip-list strings for the Nancy swap — computed once,
    # not on every MC say line.
    _in_nancy_skip1 = _in_normalize_equiv_text("No, I came with Nancy, my mother.")
    _in_nancy_skip2 = _in_normalize_equiv_text("(Our mother, Nancy, used to look after us and our sisters in Kredon. Since our father was always working, I can recall more memories with her than with him.)")

    # Static allow-list for say/menu filtering. Building this set once avoids
    # allocating it on every dialogue/menu line.
    _in_allowed_say_tags = frozenset((
        'b', 'i', 'u', 's',
        'color', 'alpha', 'font', 'cps',
        'k', 'w', 'nw', 'p', 'br', 'rt', 'rb',
        'a',
        'size', 'sc', 'bt', 'move',
    ))

    # Active replacement index. The old implementation scanned the entire
    # active replacement map for every say/menu string. This index turns the
    # common path into a handful of dictionary lookups.
    _in_replace_index_key = None
    _in_replace_index_cache = None

    def _in_add_replace_index_entry(bucket, key, entry):
        if key is None:
            return
        bucket.setdefault(key, []).append(entry)

    def _in_expand_candidate_placeholders(old, mc_display, lastname_display):
        candidates = set([old])
        if "[mc]" in old and mc_display != "[mc]":
            candidates.add(old.replace("[mc]", mc_display))
        if "[lastname]" in old and lastname_display != "[lastname]":
            for base in list(candidates):
                candidates.add(base.replace("[lastname]", lastname_display))
        return candidates

    def _in_get_replace_index(mapping, mc_display, lastname_display):
        global _in_replace_index_key, _in_replace_index_cache
        try:
            flags_key = _build_replace_map_flags
        except Exception:
            flags_key = None
        key = (flags_key, len(mapping), mc_display, lastname_display)
        if key == _in_replace_index_key and _in_replace_index_cache is not None:
            return _in_replace_index_cache

        exact = {}
        norm = {}
        stripped = {}
        multimod = {}
        order = 0
        for old, new in mapping.items():
            if not old:
                order += 1
                continue

            if isinstance(new, (list, tuple)) and new and isinstance(new[0], (list, tuple)):
                alternatives = new
            else:
                alternatives = (new,)

            for alt_index, alt in enumerate(alternatives):
                extracted = _im_extract_entry(alt)
                if extracted is None:
                    continue
                rep, spec, inj = extracted
                entry = (order, alt_index, old, rep, spec, tuple(inj or ()))
                for cand in _in_expand_candidate_placeholders(old, mc_display, lastname_display):
                    if not cand:
                        continue
                    _in_add_replace_index_entry(exact, cand, entry)
                    try:
                        _in_add_replace_index_entry(norm, _in_normalize_equiv_text(cand), entry)
                    except Exception:
                        pass
                    try:
                        _in_add_replace_index_entry(stripped, _in_normalize_equiv_text(_in_strip_tags(cand)), entry)
                    except Exception:
                        pass
                    try:
                        _in_add_replace_index_entry(multimod, _in_normalize_equiv_text(_im_strip_multimod_tags(cand, force=True)), entry)
                    except Exception:
                        pass
            order += 1

        _in_replace_index_key = key
        _in_replace_index_cache = (exact, norm, stripped, multimod)
        return _in_replace_index_cache

    def _in_find_indexed_replacement(t, t_norm, t_norm_stripped, t_norm_multimod, mc_display, lastname_display, min_order=0, resolve_names=True):
        mapping = _build_replace_map()
        if not mapping:
            return None
        exact, norm, stripped, multimod = _in_get_replace_index(mapping, mc_display, lastname_display)

        found = []
        seen = set()

        def _collect(entries):
            if not entries:
                return
            for entry in entries:
                ident = (entry[0], entry[1])
                if ident in seen:
                    continue
                seen.add(ident)
                found.append(entry)

        _collect(exact.get(t))
        if t_norm is not None:
            _collect(norm.get(t_norm))
        if t_norm_stripped is not None:
            _collect(stripped.get(t_norm_stripped))
        if t_norm_multimod is not None:
            _collect(multimod.get(t_norm_multimod))

        if not found:
            return None
        found.sort(key=lambda entry: (entry[0], entry[1]))

        for order, alt_index, old, rep, spec, inj in found:
            if order < min_order:
                continue
            if not _im_script_spec_matches(spec):
                continue
            # Only resolve [mc]/[lastname] when the text is already past
            # Ren'Py's substitution stage. In the say/menu filter the
            # placeholders must survive: Ren'Py interpolates them later, and
            # keeping them makes the resulting string a stable translation key.
            if resolve_names:
                if "[mc]" in rep:
                    rep = rep.replace("[mc]", mc_display)
                if "[lastname]" in rep:
                    rep = rep.replace("[lastname]", lastname_display)
            return (rep, list(inj), order + 1)
        return None

    def _in_transform_text(s: str, resolve_names: bool = True) -> str:
        global _in_adad_sync_flags, _in_display_cache, _in_display_cache_keys
        t = s

        # _im_sync_adad_alias only needs to run when mode flags change, not every say.
        try:
            curr_flags = (
                bool(getattr(renpy.store, 'annie_sister',      False)),
                bool(getattr(renpy.store, 'annie_half_sister', False)),
            )
            if curr_flags != _in_adad_sync_flags:
                _im_sync_adad_alias()
                _in_adad_sync_flags = curr_flags
        except Exception:
            pass

        # If neither mode is active, skip all replacements entirely.
        if not _in_any_mode_active():
            return t
        t_norm = _in_normalize_equiv_text(t)
        t_norm_stripped = _in_normalize_equiv_text(_in_strip_tags(t))
        try:
            t_norm_multimod = _in_normalize_equiv_text(
                _im_strip_multimod_tags(t, force=True)
            )
        except Exception:
            t_norm_multimod = None

        # 2) resolve [mc] and [lastname] as shown on screen — cached until store changes
        mc_src = getattr(renpy.store, "player_name", None) or getattr(renpy.store, "mc_name", None) or getattr(renpy.store, "name_mc", None)
        ln_src = getattr(renpy.store, "lastname", None) or getattr(renpy.store, "mc_lastname", None) or getattr(renpy.store, "last_name", None) or getattr(renpy.store, "surname", None)
        cache_key = (mc_src, ln_src)

        if cache_key != _in_display_cache_keys or not _in_display_cache:
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

            _in_display_cache = {"mc": mc_display, "lastname": lastname_display}
            _in_display_cache_keys = cache_key
        else:
            mc_display = _in_display_cache["mc"]
            lastname_display = _in_display_cache["lastname"]

        # 3) apply mapping first (before Nancy->Mom). Use the cached
        # replacement index so this does not scan every map entry per line.
        try:
            _im_next_order = 0
            # The old code could cascade into later map entries after a match.
            # Keep that behavior, but cap the loop to avoid accidental cycles.
            for _im_replace_pass in range(8):
                _im_repl = _in_find_indexed_replacement(
                    t,
                    t_norm,
                    t_norm_stripped,
                    t_norm_multimod,
                    mc_display,
                    lastname_display,
                    _im_next_order,
                    resolve_names,
                )
                if _im_repl is None:
                    break
                t, _im_inj, _im_next_order = _im_repl
                t_norm = _in_normalize_equiv_text(t)
                t_norm_stripped = _in_normalize_equiv_text(_in_strip_tags(t))
                try:
                    t_norm_multimod = _in_normalize_equiv_text(
                        _im_strip_multimod_tags(t, force=True)
                    )
                except Exception:
                    t_norm_multimod = None

                if _im_inj:
                    # Only queue when we are inside a real say __call__.
                    # replace_text also runs on History/log re-renders; the
                    # _im_in_say_call flag (set in _im_char_call_wrapper only
                    # while the say is active) prevents those from queuing.
                    try:
                        if (
                            getattr(store, "_im_in_say_call", False)
                            and not getattr(store, "_im_injection_queued", False)
                        ):
                            store._im_injection_queued = True
                            store._im_post_say_pending.extend(_im_inj)
                    except Exception:
                        pass
        except Exception:
            pass

        # 4) speaker-aware "Nancy" -> "Mom" only for MC lines.
        #    Avoid the AST/speaker lookup unless the active text can actually match.
        try:
            if getattr(renpy.store, 'annie_mom', False) and "Nancy" in t:
                skip_nancy_swap = False
                try:
                    if t_norm == _in_nancy_skip1:
                        skip_nancy_swap = True
                    elif t_norm == _in_nancy_skip2:
                        skip_nancy_swap = True
                except Exception:
                    pass
                if not skip_nancy_swap:
                    who_obj, who_name = _in_current_speaker()
                    if _is_mc_like(who_obj, who_name):
                        t = _in_nancy_possessive_re.sub("Mom's", t)  # possessive first
                        t = _in_nancy_re.sub("Mom", t)
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
            out = _in_transform_text(sanitized, resolve_names=False)
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
            allowed = _in_allowed_say_tags
            try:
                sanitized = _im_strip_multimod_tags(text)
                sanitized = _im_strip_bonusmod_tags(sanitized)
            except Exception:
                sanitized = text
            # Ren'Py also invokes this filter while predicting future dialogue.
            # Remember that state so local table translation can still happen,
            # while potentially expensive third-party filters are skipped.
            predicting = False
            try:
                predicting = bool(renpy.predicting())
            except Exception:
                pass
            try:
                transformed = _in_transform_text(sanitized, resolve_names=False)
            except Exception:
                transformed = sanitized
            mod_transformed = transformed
            # Translate immediately after the IC transformation. Multi-Mod
            # decorates menu choices with numeric prefixes and can substitute
            # [mc]/[lastname] before Character.__call__ reaches Ren'Py's normal
            # late string lookup. Waiting for that lookup therefore produces
            # keys such as "1. Full Incest..." or player-name-specific text,
            # neither of which exists in the translation table. Returning the
            # already translated string keeps choices and placeholder-bearing
            # dialogue stable; the later lookup simply leaves German intact.
            try:
                _im_before_tl = transformed
                transformed = renpy.translation.translate_string(_im_before_tl)

                # Multi-Mod can number a menu label before this filter sees
                # it ("1. Choice"). Its German pack contains numbered forms
                # for the base game, but naturally none for IC-Mod's own menu.
                # If the complete key misses, translate the unnumbered body
                # and restore the decoration.
                if transformed == _im_before_tl:
                    _im_numbered = re.match(r"^(\s*\d+\.\s+)(.*)$", _im_before_tl, re.S)
                    if _im_numbered:
                        _im_choice_prefix = _im_numbered.group(1)
                        _im_choice_body = _im_numbered.group(2)
                        _im_choice_tl = renpy.translation.translate_string(_im_choice_body)

                        if _im_choice_tl != _im_choice_body:
                            transformed = _im_choice_prefix + _im_choice_tl
            except Exception:
                pass
            # Preserve a previously installed dialogue filter (for example
            # Translator3000).  Eternum-IC must transform the original English
            # text first so its exact-string mappings can match. During
            # prediction, skip the previous filter because Translator3000 can
            # perform synchronous web requests for invisible future lines.
            try:
                if (not predicting) and callable(_in_prev_say_menu_filter):
                    transformed = _in_prev_say_menu_filter(transformed)
            except Exception:
                pass
            # Dev: track whether this dialogue line was changed by the mod
            try:
                if getattr(persistent, "im_dev_text_indicator", False):
                    prev = getattr(store, "_im_dev_last_filter_input", None)
                    if sanitized != prev:
                        store._im_dev_last_filter_input = sanitized
                        store._im_dev_text_modified = (mod_transformed != sanitized)
            except Exception:
                pass
            # Dev: capture current AST node location for the specifier overlay
            try:
                if getattr(persistent, "im_dev_node_loc", False):
                    store._im_dev_node_loc = _im_get_current_node_loc()
            except Exception:
                pass
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
        "I only want Annie as sister":
            $ im_incest_mode = "sister"
        "Nancy as Mom and Annie as half-sister":
            $ im_incest_mode = "half"
        "Nancy as aunt and Annie as stepsister":
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
    # After flags change, refresh all incest-mode hooks immediately.
    $ im_set_mode(im_incest_mode)
    $ _in_incest_prompted = True
    return

# -----------------------------------------
# Re-apply after loading
# -----------------------------------------
label after_load:
    $ im_export_store_api()
    $ _im_apply_incest_mode()
    $ in_apply_text_map()
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
                    label _("Incest Mode")
                    textbutton _("Full Incest"):
                        action Function(im_set_mode, "incest")
                        selected im_incest_mode == "incest"
                    textbutton _("Nancy as Mom"):
                        action Function(im_set_mode, "mom")
                        selected im_incest_mode == "mom"
                    textbutton _("Annie as Sister"):
                        action Function(im_set_mode, "sister")
                        selected im_incest_mode == "sister"
                    textbutton _("Mom+Half-Sister"):
                        action Function(im_set_mode, "half")
                        selected im_incest_mode == "half"
                    textbutton _("Aunt+Stepsister"):
                        action Function(im_set_mode, "aunt")
                        selected im_incest_mode == "aunt"
                    textbutton _("Disabled"):
                        action Function(im_set_mode, "off")
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

                # ── DEV TOOLS ─────────────────────────────────────────────────────
                vbox:
                    style_prefix "check"
                    label "{color=#888888}Dev Tools{/color}"
                    textbutton _("Text-Change Indicator"):
                        action ToggleField(persistent, "im_dev_text_indicator")
                        selected persistent.im_dev_text_indicator
                        tooltip _("DEV: Zeigt IC-Mod-Badge (oben rechts) wenn der aktuelle Dialog-Text durch den Mod veraendert wurde.")
                    textbutton _("Show Script Line"):
                        action ToggleField(persistent, "im_dev_node_loc")
                        selected persistent.im_dev_node_loc
                        tooltip _("DEV: Zeigt oben rechts Datei und Zeilennummer (z.B. script8:867) des aktuellen Dialogs - zum Copy-Pasten als Script-Specifier.")
                # ──────────────────────────────────────────────────────

                null height (4 * gui.pref_spacing)


        # textbutton "Return" action Return()    xpos 91    yalign 0.93    yoffset -45
        default return_h = None
        button:
            action Return()
            focus_mask True
            image "gui/msp5/return.png"
            image Transform("gui/msp5/return.png", matrixcolor=ColorizeMatrix('#f1f1f180', '#f1f1f180')):
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

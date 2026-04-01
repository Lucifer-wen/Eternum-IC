################################################################################
# Chat thumbnail overrides for the Eternum-IC mod.
# Builds the header dynamically so names can change at runtime.
################################################################################

define gui.chat_name_font = "Eternum-IC/chat_thumbnails/ARLRDBD.TTF"

default icmod_chat_thumb_overrides = {}

default icmod_chat_last_names = {
    "annie": "Winters",
    "dalia": "Carter",
    "nancy": "Carter",
    "penelope": "Carter",
}

style icmod_chat_thumb_text is default:
    font gui.chat_name_font
    size 40
    #bold True
    color "#000000"
    outlines [
        (2, "#ffffffd0"),
        #(1, "#000000"),
    ]
    kerning 1
    textalign 1.0
    yalign 0.5

style icmod_chat_thumb_text_shadow is icmod_chat_thumb_text:
    color "#00000080"
    outlines []

init offset = 20

init python:
    from renpy.display.layout import Composite, DynamicDisplayable
    from renpy.display.transform import Transform
    from renpy.text.text import Text
    import renpy.store as store

    _ICMOD_THUMB_SIZE = (1225, 245)
    _ICMOD_TEXT_RIGHT = 980      # rechte Grenze des Texts (x kurz vor dem Profilkreis)
    _ICMOD_LAST_NAME_DEFAULTS = {
        "annie": "Winters",
        "dalia": "Carter",
        "nancy": "Carter",
        "penelope": "Carter",
    }

    def _icmod_get_mc_last_name():
        candidates = []
        try:
            sub = renpy.substitute("[lastname]")
            if sub and sub != "[lastname]":
                candidates.append(sub)
        except Exception:
            pass

        for attr in ("lastname", "mc_lastname", "last_name", "surname"):
            val = getattr(store, attr, None)
            if isinstance(val, str) and val.strip():
                candidates.append(val.strip())

        for val in candidates:
            if val:
                return val
        return "Richards"

    def icmod_refresh_chat_last_names(mode=None):
        defaults = dict(_ICMOD_LAST_NAME_DEFAULTS)
        if mode is None:
            mode = getattr(store, "im_incest_mode", None)

        mc_last = _icmod_get_mc_last_name()
        carter_keys = ("nancy", "dalia", "penelope")
        all_keys = tuple(defaults.keys())

        if mode == "incest":
            for key in all_keys:
                defaults[key] = mc_last
        elif mode == "mom":
            for key in carter_keys:
                defaults[key] = mc_last
        elif mode == "sister":
            defaults["annie"] = mc_last
        elif mode in ("aunt", "half"):
            pass
        elif mode == "off" or mode is None:
            pass

        icmod_chat_last_names.clear()
        icmod_chat_last_names.update(defaults)
        try:
            renpy.restart_interaction()
        except Exception:
            pass

    def _icmod_build_thumb(name_key, source, first, default_last, right_x=None, text_pos=None, text_anchor=None):
        right = right_x if right_x is not None else _ICMOD_TEXT_RIGHT

        def _render(_st, _at):
            override = store.icmod_chat_thumb_overrides.get(name_key, None)
            if override:
                label = override.strip()
            else:
                # Compute last name dynamically so it updates after the player
                # enters their name at character creation (avoids stale init cache).
                _mode = getattr(store, "im_incest_mode", None)
                _mc_last = _icmod_get_mc_last_name()
                _carter = ("nancy", "dalia", "penelope")
                if _mode == "incest":
                    last = _mc_last
                elif _mode == "mom" and name_key in _carter:
                    last = _mc_last
                elif _mode == "sister" and name_key == "annie":
                    last = _mc_last
                else:
                    # Use manually-set override if present, otherwise the default
                    last = store.icmod_chat_last_names.get(name_key, default_last) or ""
                last = last.strip()
                if last:
                    label = "{} {}".format(first, last)
                else:
                    label = first

            text_displayable = Text(label, style="icmod_chat_thumb_text")

            # Tatsächliche Textgröße messen, dann rechtsbündig platzieren
            text_surf = renpy.render(text_displayable, _ICMOD_THUMB_SIZE[0], _ICMOD_THUMB_SIZE[1], _st, _at)
            text_w, text_h = text_surf.get_size()

            text_x = max(0, right - int(text_w))
            text_y = (_ICMOD_THUMB_SIZE[1] - int(text_h)) // 2

            composite = Composite(
                _ICMOD_THUMB_SIZE,
                (0, 0), source,
                (text_x, text_y), text_displayable,
            )
            return composite, 0.0

        return DynamicDisplayable(_render)

    def icmod_set_chat_last_name(name_key, last_name):
        store.icmod_chat_last_names[name_key] = (last_name or "").strip()
        renpy.restart_interaction()

    def icmod_set_chat_thumb_name(name_key, text):
        trimmed = (text or "").strip()
        if trimmed:
            store.icmod_chat_thumb_overrides[name_key] = trimmed
        elif name_key in store.icmod_chat_thumb_overrides:
            del store.icmod_chat_thumb_overrides[name_key]
        renpy.restart_interaction()

    try:
        icmod_refresh_chat_last_names()
    except Exception:
        pass

image chat_annie_1 = _icmod_build_thumb(
    "annie",
    "Eternum-IC/chat_thumbnails/chat_annie_1_icmod.png",
    "Annie",
    "Winters",
)

image chat_dalia_1 = _icmod_build_thumb(
    "dalia",
    "Eternum-IC/chat_thumbnails/chat_dalia_1_icmod.png",
    "Dalia",
    "Carter",
)

image chat_dalia_1b = _icmod_build_thumb(
    "dalia",
    "Eternum-IC/chat_thumbnails/chat_dalia_1b_icmod.png",
    "Dalia",
    "Carter",
)

image chat_nancy_1 = _icmod_build_thumb(
    "nancy",
    "Eternum-IC/chat_thumbnails/chat_nancy_1_icmod.png",
    "Nancy",
    "Carter",
)

image chat_penelope_1 = _icmod_build_thumb(
    "penelope",
    "Eternum-IC/chat_thumbnails/chat_penelope_1.png",
    "Penelope",
    "Carter",
)
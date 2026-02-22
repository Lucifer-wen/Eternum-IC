################################################################################
# Chat thumbnail overrides for the Eternum-IC mod.
# Builds the header dynamically so names can change at runtime.
################################################################################

define gui.chat_name_font = "mods/chat_thumbnails/ARLRDBD.TTF"

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
    textalign 0.0
    xalign 0.0
    yalign 0.5

style icmod_chat_thumb_text_shadow is icmod_chat_thumb_text:
    color "#00000080"
    outlines []

init offset = 20

init python:
    from renpy.display.layout import LiveComposite, DynamicDisplayable
    from renpy.display.transform import Transform
    from renpy.text.text import Text
    import renpy.store as store

    _ICMOD_THUMB_SIZE = (1225, 245)
    _ICMOD_NAME_POS = (520, 95)
    _ICMOD_TEXT_ANCHOR = (0.0, 0.5)
    _ICMOD_TEXT_MAX_WIDTH = 760
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

    def _icmod_build_thumb(name_key, source, first, default_last, text_pos=None, text_anchor=None):
        pos = text_pos or _ICMOD_NAME_POS
        anchor = text_anchor or _ICMOD_TEXT_ANCHOR

        def _render(_st, _at):
            override = store.icmod_chat_thumb_overrides.get(name_key, None)
            if override:
                label = override.strip()
            else:
                last = store.icmod_chat_last_names.get(name_key, default_last) or ""
                last = last.strip()
                if last:
                    label = "{} {}".format(first, last)
                else:
                    label = first

            text_displayable = Text(
                label.upper(),
                style="icmod_chat_thumb_text",
                xmaximum=_ICMOD_TEXT_MAX_WIDTH,
            )
            name_text = Transform(text_displayable, anchor=anchor)

            composite = LiveComposite(
                _ICMOD_THUMB_SIZE,
                (0, 0), source,
                pos, name_text,
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
    "mods/chat_thumbnails/chat_annie_1_icmod.png",
    "Annie",
    "Winters",
)

image chat_dalia_1 = _icmod_build_thumb(
    "dalia",
    "mods/chat_thumbnails/chat_dalia_1_icmod.png",
    "Dalia",
    "Carter",
)

image chat_dalia_1b = _icmod_build_thumb(
    "dalia",
    "mods/chat_thumbnails/chat_dalia_1b_icmod.png",
    "Dalia",
    "Carter",
)

image chat_nancy_1 = _icmod_build_thumb(
    "nancy",
    "mods/chat_thumbnails/chat_nancy_1_icmod.png",
    "Nancy",
    "Carter",
)

image chat_penelope_1 = _icmod_build_thumb(
    "penelope",
    "mods/chat_thumbnails/chat_penelope_1_icmod.png",
    "Penelope",
    "Carter",
)
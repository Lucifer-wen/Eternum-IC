################################################################################
# Info screen name image overrides for the Eternum-IC mod.
# Overrides sc_sub_point (pax.rpy) to use mod _l.png files and dynamically
# render the last name below the baked-in first-name graphic.
################################################################################

init offset = 1

style icmod_info_last_name is default:
    font "Eternum-IC/InfoNames/Anton-Regular.ttf"
    size 54
    color "#f0f0f0"
    outlines [(3, "#00000044", 2, 3)]

style icmod_info_last_name_shadow is icmod_info_last_name:
    color "#000000"
    outlines []

style icmod_info_last_name_glow is icmod_info_last_name_shadow

init python:
    from renpy.display.layout import LiveComposite, DynamicDisplayable
    from renpy.display.transform import Transform
    from renpy.text.text import Text
    import renpy.store as store

    _ICMOD_INFO_IMG_SIZE = (1920, 1080)
    _ICMOD_INFO_LAST_NAME_BASE_SIZE = 54.0

    def _icmod_info_cfg(source_path, default_last, max_width=176):
        return {
            "source_path": source_path,
            "default_last": default_last,
            "text_pos": (45, 194),
            "max_width": max_width,
            "font_size": 54.0,
            "shadow_offset": (0, 4),
            "shadow_alpha": 0.80,
            "glow_offset": (0, 0),
            "glow_blur": 5.0,
            "glow_alpha": 0.59,
        }

    _ICMOD_INFO_NAME_CFG = {
        "annie":    _icmod_info_cfg("Eternum-IC/InfoNames/annie_l.png",    "Winters"),
        "dalia":    _icmod_info_cfg("Eternum-IC/InfoNames/dalia_l.png",    "Carter"),
        "nancy":    _icmod_info_cfg("Eternum-IC/InfoNames/nancy_l.png",    "Carter"),
        "penelope": _icmod_info_cfg("Eternum-IC/InfoNames/penelope_l.png", "Carter"),
    }

    def _icmod_info_last_name_layers(last, cfg, _st, _at):
        base_text = Text(last, style="icmod_info_last_name")
        text_w, _text_h = renpy.render(base_text, _ICMOD_INFO_IMG_SIZE[0], _ICMOD_INFO_IMG_SIZE[1], _st, _at).get_size()

        zoom = float(cfg.get("font_size", _ICMOD_INFO_LAST_NAME_BASE_SIZE)) / _ICMOD_INFO_LAST_NAME_BASE_SIZE
        scaled_w = text_w * zoom
        max_width = float(cfg.get("max_width", 0))
        if max_width > 0.0 and scaled_w > max_width and scaled_w > 0.0:
            zoom *= max_width / scaled_w

        x, y = cfg["text_pos"]
        gx, gy = cfg.get("glow_offset", (0, 0))
        sx, sy = cfg.get("shadow_offset", (0, 0))

        return [
            ((x + gx, y + gy), Transform(Text(last, style="icmod_info_last_name_glow"), zoom=zoom, alpha=cfg.get("glow_alpha", 0.0), blur=cfg.get("glow_blur", 0.0))),
            ((x + sx, y + sy), Transform(Text(last, style="icmod_info_last_name_shadow"), zoom=zoom, alpha=cfg.get("shadow_alpha", 1.0))),
            ((x, y), Transform(base_text, zoom=zoom)),
        ]

    def _icmod_build_info_name(char_key, cfg):
        source_path = cfg["source_path"]
        default_last = cfg["default_last"]

        def _render(_st, _at):
            chat_names = getattr(store, "icmod_chat_last_names", {})
            last = (chat_names.get(char_key) or default_last or "").strip().upper()

            parts = [(0, 0), source_path]
            if last:
                for pos, displayable in _icmod_info_last_name_layers(last, cfg, _st, _at):
                    parts.extend([pos, displayable])

            composite = LiveComposite(
                _ICMOD_INFO_IMG_SIZE,
                *parts
            )
            return composite, 0.0

        return DynamicDisplayable(_render)

    _ICMOD_INFO_DYN = {
        "annie":    _icmod_build_info_name("annie",    _ICMOD_INFO_NAME_CFG["annie"]),
        "dalia":    _icmod_build_info_name("dalia",    _ICMOD_INFO_NAME_CFG["dalia"]),
        "nancy":    _icmod_build_info_name("nancy",    _ICMOD_INFO_NAME_CFG["nancy"]),
        "penelope": _icmod_build_info_name("penelope", _ICMOD_INFO_NAME_CFG["penelope"]),
    }

    def _icmod_l_path(name):
        d = _ICMOD_INFO_DYN.get(name)
        if d is not None:
            return d
        return "gui/sp2/{}_l.png".format(name)

screen sc_sub_point(hovered=None, selected=None, data=None):

    if selected:
        $ loc_points = getattr(store, selected + "_points")
        $ assets = { "nova": ["nova_bg.png", "nova_h.png", "nova_l.png", "nova_d.png"], "calypso": ["calypso_bg.png", "calypso_h.png", "calypso_l.png", "calypso_d.png"], "annie": ["annie_bg.png", "annie_h.png", "annie_l.png", "annie_d.png"], "dalia": ["dalia_bg.png", "dalia_h.png", "dalia_l.png", "dalia_d.png"], "alex": ["alex_bg.png", "alex_h.png", "alex_l.png", "alex_d.png"], "penelope": ["penelope_bg.png", "penelope_h.png", "penelope_l.png", "penelope_d.png"], "luna": ["luna_bg.png", "luna_h.png", "luna_l.png", "luna_d.png"], "nancy": ["nancy_bg.png", "nancy_h.png", "nancy_l.png", "nancy_d.png"], }
        add _icmod_l_path(selected)
        if data:
            add "gui/sp2/" + data
        else:
            add "gui/sp2/" + assets[selected][3]
        add "gui/sp2/relationship.png"
        hbox:
            pos (32, 350)
            spacing -36
            add "bios_heart_on"
            for i in range(2, 7):
                if getattr(girls_hearts[selected], f"hearts{i}") != -1 and loc_points >= getattr(girls_hearts[selected], f"hearts{i}"):
                    add "bios_heart_on"
                else:
                    add "bios_heart_off"
    else:
        $ loc_points = getattr(store, hovered + "_points")
        add "gui/sp2/" + str(hovered) + "_bg.png" at pp2_fade_in
        if hovered == "calypso":
            add 'gui/sp2/calypso_h.png' at pp2_fl
        else:
            add "lk_" + hovered + str(looks[hovered][current_look] if 0 <= current_look < len(looks[hovered]) else 0) xoffset 500 at pp2_fl
        add _icmod_l_path(str(hovered)) at fbottom(0.0)
        if data:
            add "gui/sp2/" + data at fbottom(0.1)
        else:
            add "gui/sp2/" + str(hovered) + "_d.png" at fbottom(0.1)
        add "gui/sp2/relationship.png" at fbottom(0.05)
        hbox:
            pos (32, 350)
            spacing -36
            add "bios_heart_on"
            for i in range(2, 7):
                if getattr(girls_hearts[hovered], f"hearts{i}") != -1 and loc_points >= getattr(girls_hearts[hovered], f"hearts{i}"):
                    add "bios_heart_on"
                else:
                    add "bios_heart_off"
            at hearts_h()

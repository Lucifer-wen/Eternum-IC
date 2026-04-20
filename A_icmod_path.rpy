################################################################################
# Detects the mod root directory at runtime so the folder can be renamed or
# placed in any subfolder inside game/ without breaking asset paths.
# Loads first (A_) so _ICMOD_ROOT is available to all other mod files.
################################################################################

init -1000 python:
    import os as _os

    def _icmod_find_root():
        gamedir = renpy.config.gamedir
        sentinel = "IncestMod.rpy"
        try:
            for dirpath, dirnames, filenames in _os.walk(gamedir):
                # Don't search more than 3 levels deep to keep it fast
                depth = dirpath[len(gamedir):].count(_os.sep)
                if depth > 3:
                    dirnames[:] = []
                    continue
                if sentinel in filenames:
                    rel = _os.path.relpath(dirpath, gamedir)
                    return rel.replace("\\", "/")
        except Exception:
            pass
        return "Eternum-IC"

    _ICMOD_ROOT = _icmod_find_root()

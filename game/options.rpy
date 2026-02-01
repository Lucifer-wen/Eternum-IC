## This file contains options that can be changed to customize your game.
##
## Lines beginning with two '#' marks are comments, and you shouldn't uncomment
## them. Lines beginning with a single '#' mark are commented-out code, and you
## may want to uncomment them when appropriate.


## Basics ######################################################################

## A human-readable name of the game. This is used to set the default window
## title, and shows up in the interface and error reports.
##
## The _() surrounding the string marks it as eligible for translation.

define config.name = _("Eternum")



## Determines if the title given above is shown on the main menu screen. Set
## this to False to hide the title.

define gui.show_name = False


## The version of the game.

define config.version = "0.9.5"
define myconfig.version = 0.8


## Text that is placed on the game's about screen. Place the text between the
## triple-quotes, and leave a blank line between paragraphs.

define gui.about = _p("""
""")


## A short name for the game used for executables and directories in the built
## distribution. This must be ASCII-only, and must not contain spaces, colons,
## or semicolons.

define build.name = "Eternum"


## Sounds and music ############################################################

## These three variables control which mixers are shown to the player by
## default. Setting one of these to False will hide the appropriate mixer.

define config.has_sound = True
define config.has_music = True
define config.has_voice = True


## To allow the user to play a test sound on the sound or voice channel,
## uncomment a line below and use it to set a sample sound to play.

# define config.sample_sound = "sample-sound.ogg"
# define config.sample_voice = "sample-voice.ogg"


## Uncomment the following line to set an audio file that will be played while
## the player is at the main menu. This file will continue playing into the
## game, until it is stopped or another file is played.

define config.main_menu_music = "orion.mp3"


## Transitions #################################################################
##
## These variables set transitions that are used when certain events occur.
## Each variable should be set to a transition, or None to indicate that no
## transition should be used.

## Entering or exiting the game menu.

define config.enter_transition = dissolve
define config.exit_transition = dissolve


## Between screens of the game menu.

define config.intra_transition = dissolve


## A transition that is used after a game has been loaded.

define config.after_load_transition = None


## Used when entering the main menu after the game has ended.

define config.end_game_transition = Dissolve(1)


## A variable to set the transition used when the game starts does not exist.
## Instead, use a with statement after showing the initial scene.


## Window management ###########################################################
##
## This controls when the dialogue window is displayed. If "show", it is always
## displayed. If "hide", it is only displayed when dialogue is present. If
## "auto", the window is hidden before scene statements and shown again once
## dialogue is displayed.
##
## After the game has started, this can be changed with the "window show",
## "window hide", and "window auto" statements.

define config.window = "hide"


## Transitions used to show and hide the dialogue window

define config.window_show_transition = None
define config.window_hide_transition = None


## Preference defaults #########################################################

## Controls the default text speed. The default, 0, is infinite, while any other
## number is the number of characters per second to type out.

default preferences.text_cps = 0


## The default auto-forward delay. Larger numbers lead to longer waits, with 0
## to 30 being the valid range.

default preferences.afm_time = 15


## Save directory ##############################################################
##
## Controls the platform-specific place Ren'Py will place the save files for
## this game. The save files will be placed in:
##
## Windows: %APPDATA\RenPy\<config.save_directory>
##
## Macintosh: $HOME/Library/RenPy/<config.save_directory>
##
## Linux: $HOME/.renpy/<config.save_directory>
##
## This generally should not be changed, and if it is, should always be a
## literal string, not an expression.

define config.save_directory = "Eternum-1610153667"


## Icon ########################################################################
##
## The icon displayed on the taskbar or dock.

define config.window_icon = "gui/window_icon.png"


## Build configuration #########################################################
##
## This section controls how Ren'Py turns your project into distribution files.
init python:
    config.movie_mixer = "sfx"

    if preferences.transitions == 0:
        preferences.transitions = 2

    def mouse_mov():
        pos_now = renpy.get_mouse_pos()
        pos_go = [960, 384]
        if pos_now[0] != pos_go[0] or pos_now[1] != pos_go[1] :
            renpy.set_mouse_pos(pos_go[0],pos_go[1],0.1)
    def mouse_mov2():
        pos_now = renpy.get_mouse_pos()
        pos_go = [960, 450]
        if pos_now[0] != pos_go[0] or pos_now[1] != pos_go[1] :
            renpy.set_mouse_pos(pos_go[0],pos_go[1],0.1)

    def show_countdown(st, at, length):
        if st > length:
            return Text("0.0", style="mytextcountdown"), None
        else:
            d = Text("{:.1f}".format(length - st), style="mytextcountdown")
            return d, 0.1

    renpy.music.register_channel("music", mixer="music", loop=None, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("musicb", mixer="music", loop=None, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("music2", mixer="music", loop=None, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("music2b", mixer="music", loop=None, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("music3", mixer="music", loop=None, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("music3b", mixer="music", loop=None, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("musicnoloop", mixer="music", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("sound", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("sound2", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("sound3", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("sound4", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("sound5", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("sound6", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("sound7", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("sound8", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("sound9", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("soundloop", mixer="sfx", loop=None, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("soundloop2", mixer="sfx", loop=None, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("soundloop3", mixer="sfx", loop=None, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("soundloop4", mixer="sfx", loop=None, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("soundlow", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)
    renpy.music.register_channel("soundlow2", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix='', file_suffix='', buffer_queue=True)

    def game_version_to_sortable_string(version_str):
        """Turn a version string into a sortable string.
        
        Example: "0.8.6" -> "0.08.06"

        An example problem this solves: 0.12 is a higher version than 0.5,
        but would be sorted lower because of the 1. This can't happen with
        0.12 and 0.05!"""

        # Define exact length of version number components
        # (to be filled with leading zeroes)
        MAJOR_VERSION_DIGITS = 1
        MINOR_VERSION_DIGITS = 2
        PATCH_VERSION_DIGITS = 2
        error_message = (
            f"ERROR: Badly formatted version string: \"{version_str}\". "
            "Use <number>.<number> or <number>.<number>.<number>, for example: "
            "0.4 or 1.2.5"
        )

        # Disassemble original string
        version_split = config.version.split(".")
        if len(version_split) < 2 or len(version_split) > 3:
            raise RuntimeError(error_message)
        try:
            major_version = int(version_split[0])
            minor_version = int(version_split[1])
            if len(version_split) == 3:
                patch_version = int(version_split[2])
            else:
                patch_version = 0
        except:
            raise RuntimeError(error_message)
        
        # Check for out of bounds
        major_version_max = (10 ** MAJOR_VERSION_DIGITS) - 1
        if major_version < 0 or major_version > major_version_max:
            raise RuntimeError(
                f"ERROR: Badly formatted version string: \"{version_str}\". "
                f"The first number must be between 0 and {major_version_max}"
            )
        minor_version_max = (10 ** MINOR_VERSION_DIGITS) - 1
        if minor_version < 0 or minor_version > minor_version_max:
            raise RuntimeError(
                f"ERROR: Badly formatted version string: \"{version_str}\". "
                f"The second number must be between 0 and {minor_version_max}"
            )
        patch_version_max = (10 ** PATCH_VERSION_DIGITS) - 1
        if patch_version < 0 or patch_version > patch_version_max:
            raise RuntimeError(
                f"ERROR: Badly formatted version string: \"{version_str}\". "
                f"The third number must be between 0 and {patch_version_max}"
            )
        
        # Do the actual conversion
        return (
            str(major_version).zfill(MAJOR_VERSION_DIGITS) + "." +
            str(minor_version).zfill(MINOR_VERSION_DIGITS) + "." +
            str(patch_version).zfill(PATCH_VERSION_DIGITS)
        )
    
    # Declare name for sortable archive
    SORTABLE_VERSION = game_version_to_sortable_string(config.version)

    ## Declare name for IC archive

    IC_ARCHIVE_NAME = "Eternum-IC"
    build.archive(IC_ARCHIVE_NAME, "IC")

    ## To archive files, classify them as 'IC'.

    build.classify("game/IncestMod.rpy", IC_ARCHIVE_NAME)
    build.classify("game/IncestMod.rpyc", IC_ARCHIVE_NAME)
    build.classify("game/tl/incest_*/**.rpy", IC_ARCHIVE_NAME)
    build.classify("game/tl/incest_*/**.rpyc", IC_ARCHIVE_NAME)

    build.package("Eternum-IC_v" + im_mod_version, "zip", "IC")

## Set this to a string containing your Apple Developer ID Application to enable
## codesigning on the Mac. Be sure to change it to your own Apple-issued ID.

# define build.mac_identity = "Developer ID Application: Guy Shy (XHTE5H7Z42)"


## A Google Play license key is required to download expansion files and perform
## in-app purchases. It can be found on the "Services & APIs" page of the Google
## Play developer console.

# define build.google_play_key = "..."


## The username and project name associated with an itch.io project, separated
## by a slash.

# define build.itch_project = "renpytom/test-project"

default persistent.quick_menu = True
default persistent.text_size = gui.text_size
default persistent.text_outline = 2
default persistent.textbox_opacity = 0.0
default persistent.textbox_height = gui.textbox_height
default persistent.textbox_width = gui.dialogue_width

default persistent.motion = 1 if not renpy.variant('mobile') else 0 

# New shortcuts for quick save/quick load
init 2000:
    $ config.keymap['quickload'] = [ 'L', 'shift_K_l', 'K_F9' ]
    $ config.underlay[0].keymap['quickload'] = QuickLoad()

    $ config.keymap['quicksave'] = [ 'S', 'shift_K_s', 'K_F5' ]
    $ config.underlay[0].keymap['quicksave'] = QuickSave()

    $ config.keymap['prefmenu'] = [ 'P', 'shift_K_p' ]
    $ config.underlay[0].keymap['prefmenu'] = ShowMenu('preferences')

    $ config.keymap['toggle_afm'] = [ 'alt_K_a' ]




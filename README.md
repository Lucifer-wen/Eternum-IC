# Generating a New Translation

**Note: The translations for incest_full, incest_mom, incest_only_sister, incest_half_sister, and incest_aunt have already been generated and updated to the latest version (as of 01-Feb-26). You should not have to generate a new translation.**

1. Download and install [Ren'Py 8.3.2 SDK](https://www.renpy.org/release/8.3.2) (the version Eternum runs on).

2. Download [RPA Extract](https://iwanplays.itch.io/rpaex) or any other RPA extractor.

3. Extract Eternum-X.XX.XX-pc.zip into renpy-8.3.2-sdk folder.

4. Extract Eternum-X.XX.XX-pc/game/archive_X.XX.XX.rpa with RPA Extract by dragging it onto the rpaExtract.exe icon.

5. Open Ren'Py Launcher (renpy-8.3.2-sdk/renpy.exe) and find the Eternum-X.XX.XX-pc project.

6. Press 'Generate Translations'.

7. Set the Language ID to incest_*name* (ex. incest_mom).

8. Uncheck 'Generate empty strings for translations'

9. Press 'Generate Translations'.

10. The new translation should be in the folder Eternum-X.XX.XX-pc/game/tl/incest_*name*.

11. (Optional) Open all .RPY files, scroll to the bottom and add a note on each new TODO line for what game version was added. (ex. # TODO: Translation updated at 2026-01-28 10:20 **(Eternum-0.9.5-pc)**)

12. Run the game to compile .RPYCs.

13. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to experimental/translations-main branch.

14. Copy Eternum-X.XX.XX-pc/game/tl/incest_*name* folder, paste in Eternum-IC/game/tl.

15. Commit experimental/translations-main branch, push to origin.


# Adding Mod Compatibility to Translations

**Note: The process is exactly the same for mod updates.**

1. Download and install [Ren'Py 8.3.2 SDK](https://www.renpy.org/release/8.3.2) (the version Eternum runs on).

2. Extract Eternum-X.XX.XX-pc.zip into renpy-8.3.2-sdk folder.

**Note: You do not need to extract game/archive_X.XX.XX.rpa for adding mod compatibility.**

3. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to experimental/translations-main branch.

4. Copy Eternum-IC/game/tl folder, paste in Eternum-X.XX.XX-pc/game.

5. Download [Eternum Bonus Mod](https://cncmods.itch.io/eternum-bonus-mod) or [Eternum Multi-Mod](https://f95zone.to/threads/93424/). For the Bonus Mod, download the non-RPA version.

**Repeat Steps 6-13 once for each mod.**

6. Extract mod files into Eternum-X.XX.XX-pc/game.

7. Open Ren'Py Launcher (renpy-8.3.2-sdk/renpy.exe) and find the Eternum-X.XX.XX-pc project.

**Repeat Steps 8-11 once for each translation.**

8. Press 'Generate Translations'.

9. Set the Language ID to incest_*name* (ex. incest_mom).

10. Uncheck 'Generate empty strings for translations'.

11. Press 'Generate Translations'.

12. Delete mod files from Eternum-X.XX.XX-pc/game.

13. (Optional) Open all .RPY files, scroll to the bottom and add a note on each new TODO line for what mod version was added/updated. (ex. # TODO: Translation updated at 2026-01-28 12:09 **(Eternum_feature_mod_0.9.5.v3)**)

14. Run the game to compile .RPYCs.

15. Copy Eternum-X.XX.XX-pc/game/tl folder, paste in Eternum-IC/game.

16. Commit experimental/translations-main branch, push to origin.


# Updating Translations

1. Download and install [Ren'Py 8.3.2 SDK](https://www.renpy.org/release/8.3.2) (the version Eternum runs on).

2. Download [RPA Extract](https://iwanplays.itch.io/rpaex) or any other RPA extractor.

3. Extract Eternum-X.XX.XX-pc.zip into renpy-8.3.2-sdk folder.

4. Extract game/archive_X.XX.XX.rpa with RPA Extract by dragging it onto the rpaExtract.exe icon.

5. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to experimental/translations-main branch.

6. Copy Eternum-IC/game/tl folder, paste in Eternum-X.XX.XX-pc/game.

7. Open Ren'Py Launcher (renpy-8.3.2-sdk/renpy.exe) and find the Eternum-X.XX.XX-pc project.

**Repeat Steps 8-11 once for each translation.**

8. Press 'Generate Translations'.

9. Set the Language ID to incest_*name* (ex. incest_mom).

10. Uncheck 'Generate empty strings for translations'.

11. Press 'Generate Translations'.

12. (Optional) Open all .RPY files, scroll to the bottom and add a note on each new TODO line for what game version was updated. (ex. # TODO: Translation updated at 2026-01-28 10:20 **(Eternum-0.9.5-pc)**)

13. Run the game to compile .RPYCs.

14. Copy Eternum-X.XX.XX-pc/game/tl folder, paste in Eternum-IC/game.

15. Commit experimental/translations-main branch, push to origin.


# Editing a Translation

1. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to experimental/translations-main branch.

2. Make edits to the .RPY files.

**Note: Do not delete any files or translation lines.**

3. Copy edited Eternum-IC/game/tl/incest_*name* folder(s) (ex. incest_mom), paste in Eternum-X.XX.XX-pc/game/tl.

4. Run the game to compile .RPYCs.

5. Copy Eternum-X.XX.XX-pc/game/tl/incest_*name* folder(s), paste in Eternum-IC/game/tl.

6. Commit experimental/translations-main branch, push to origin.


# Preparing Translations for Release

**Note: This should be done for every release. It massively reduces file size and loading time. Consider writing a program to do the regex replacements automatically.**

1. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to experimental/translations_main branch.

2. Copy Eternum-IC/game/tl folder, paste in Eternum-X.XX.XX-pc/game.

3. Switch to experimental/translations_release branch.

4. Take Eternum-X.XX.XX-pc/game/tl/None folder out of Eternum-X.XX.XX-pc/game/tl temporarily.

5. Open Eternum-X.XX.XX-pc/game/tl folder in VSCODE or other IDE.

6. Open Replace in Files with Ctrl+Shift+H and enable 'Use Regular Expression'.

7. Use 'Regex Delete Unchanged' and 'Regex Delete Empty Strings' (below). You will need to use it multiple times, since there is a limit on how many lines you can delete each time.

8. Put Eternum-X.XX.XX-pc/game/tl/None folder back in Eternum-X.XX.XX-pc/game/tl.

9. Run the game to compile .RPYCs.

10. Copy Eternum-X.XX.XX-pc/game/tl folder, paste in Eternum-IC/game.

11. Commit experimental/translations_release branch, push to origin.


# Building a Release

1. Download and install [Ren'Py 8.3.2 SDK](https://www.renpy.org/release/8.3.2) (the version Eternum runs on).

2. Extract Eternum-X.XX.XX-pc.zip into renpy-8.3.2-sdk folder.

**Note: You do not need to extract game/archive_X.XX.XX.rpa for building a release.**

3. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to experimental/translations_release branch.

4. Copy Eternum-IC/game folder, paste in Eternum-X.XX.XX-pc.

5. Run the game to compile .RPYCs one last time.

6. Open Ren'Py Launcher (renpy-8.3.2-sdk/renpy.exe) and find the Eternum-X.XX.XX-pc project.

7. Press 'Build Distributions'.

8. Under 'Build Packages:', only select Eternum-IC_vX.X.X.X.

9. Uncheck 'Add from clauses to calls' and 'Force Recompile'.

10. Press 'Build'.

11. The new Release should be in the folder renpy-8.3.2-sdk/Eternum-X.XX.XX-dists.

12. Release on [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and [Eternum Incest Mod thread](https://f95zone.to/threads/267184/). Don't forget to update the Mod Version and Changelog.

13. To install, just drag Eternum-IC.rpa into Eternum-X.XX.XX-pc/game.


## Regex Replacements

### Regex Find Modified

You can use regex Find with
```
(?<=# )(\w+ ".+)$(?!\n *\1\n\n)|(?<=old )(".*")$(?!\n *new \2)
```
to find lines you've modified. Useful for editing.

### Regex Delete Unchanged

You can use regex Find with
```
(?: *# \S+.rpy:\d+\n *translate \w+ \w+:\n+ *# (\w* ?".+)$\n *\1\n+| *# \S+.rpym?:\d+\n *old (".*")$\n *new \2\n+)
```
and Replace All with nothing to delete all unchanged lines for RELEASE versions in order to reduce file size and loading time.

### Regex Delete Empty Strings

Then, you can use regex Find with
```
(?: *translate \w+ strings:(?!\n*.*\n *old ".*"))
```
and Replace All with nothing to delete any empty
```
translate incest_aunt strings:
```


# Important

Translation branches (ex. tl/incest_mom) should keep *ALL* lines for adding mod compatibility or updating translations with Ren'Py SDK. Only delete unchanged lines in experimental/translations-main branch to prepare for a release.

Make sure you *ALWAYS* include the .RPYC files as well as the .RPY files and *NEVER* delete them.


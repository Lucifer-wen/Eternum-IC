# Generating a New Translation

**Note: The translations for incest_full, incest_mom, incest_only_sister, incest_half_sister, and incest_aunt have already been generated and updated to the latest version (as of 01-Feb-26). You should not have to generate a new translation.**

1. Download and install [Ren'Py 8.3.2 SDK](https://www.renpy.org/release/8.3.2) (the version Eternum runs on).

2. Download [RPA Extract](https://iwanplays.itch.io/rpaex) or any other RPA extractor.

3. Extract Eternum-X.XX.XX-pc.zip into renpy-8.3.2-sdk folder.

4. Extract game/archive_X.XX.XX.rpa with RPA Extract by dragging it onto the rpaExtract.exe icon.

5. Open Ren'Py Launcher (renpy-8.3.2-sdk/renpy.exe) and find the Eternum-X.XX.XX-pc project.

6. Press 'Generate Translations'.

7. Set the Language ID to incest_*name* (ex. incest_mom).

8. Uncheck 'Generate empty strings for translations'

9. Press 'Generate Translations'.

10. The new translation should be in the translation folder game/tl/incest_*name*.

11. (Optional) Open all .RPY files, scroll to the bottom and add a note on each new TODO line for what game version was added. (ex. # TODO: Translation updated at 2026-01-28 10:20 (Eternum-0.9.5-pc))

12. Run the game to compile .RPYCs.

13. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to tl/incest_generic branch.

14. Create a new translation branch called tl/incest_*name* based on tl/incest_generic.

15. Copy updated files in translation folder to translation branch.

16. Commit translation branch, publish/push to origin.


# Adding Mod Compatibility to a Translation

**Note: The process is exactly the same for mod updates.**

1. Download and install [Ren'Py 8.3.2 SDK](https://www.renpy.org/release/8.3.2) (the version Eternum runs on).

2. Extract Eternum-X.XX.XX-pc.zip into renpy-8.3.2-sdk folder.

**Note: You do not need to extract game/archive_X.XX.XX.rpa for adding mod compatibility.**

3. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to a translation branch (ex. tl/incest_mom).

4. Open Eternum-X.XX.XX-pc/game/tl and make a translation folder called incest_*name* (ex. incest_mom).

5. Copy translation branch files to translation folder.

6. Download [Eternum Bonus Mod](https://cncmods.itch.io/eternum-bonus-mod) or [Eternum Multi-Mod](https://f95zone.to/threads/93424/). For the Bonus Mod, download the non-RPA version.

**Note: Do Steps 8-14 once for each mod.**

7. Extract mod files into Eternum-X.XX.XX-pc/game.

8. Open Ren'Py Launcher (renpy-8.3.2-sdk/renpy.exe) and find the Eternum-X.XX.XX-pc project.

9. Press 'Generate Translations'.

10. Set the Language ID to incest_*name* (ex. incest_mom).

11. Uncheck 'Generate empty strings for translations'.

12. Press 'Generate Translations'.

13. Delete mod files from Eternum-X.XX.XX-pc/game.

14. (Optional) Open all .RPY files, scroll to the bottom and add a note on each new TODO line for what mod version was added/updated. (ex. # TODO: Translation updated at 2026-01-28 12:09 (Eternum_feature_mod_0.9.5.v3))

15. Run the game to compile .RPYCs.

16. Copy updated files in translation folder back to translation branch.

17. Commit translation branch, push to origin.


# Updating a Translation

1. Download and install [Ren'Py 8.3.2 SDK](https://www.renpy.org/release/8.3.2) (the version Eternum runs on).

2. Download [RPA Extract](https://iwanplays.itch.io/rpaex) or any other RPA extractor.

3. Extract Eternum-X.XX.XX-pc.zip into renpy-8.3.2-sdk folder.

4. Extract game/archive_X.XX.XX.rpa with RPA Extract by dragging it onto the rpaExtract.exe icon.

5. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to a translation branch (ex. tl/incest_mom).

6. Open Eternum-X.XX.XX-pc/game/tl and make a translation folder called incest_*name* (ex. incest_mom).

7. Copy translation branch files to translation folder.

8. Open Ren'Py Launcher (renpy-8.3.2-sdk/renpy.exe) and find the Eternum-X.XX.XX-pc project.

9. Press 'Generate Translations'.

10. Set the Language ID to incest_*name* (ex. incest_mom).

11. Uncheck 'Generate empty strings for translations'.

12. Press 'Generate Translations'.

13. (Optional) Open all .RPY files, scroll to the bottom and add a note on each new TODO line for what game version was updated. (ex. # TODO: Translation updated at 2026-01-28 10:20 (Eternum-0.9.5-pc))

14. Run the game to compile .RPYCs.

15. Copy updated files in translation folder back to translation branch.

16. Commit translation branch, push to origin.


# Editing a Translation

1. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to a translation branch (ex. tl/incest_mom).

2. Make edits to the .RPY files.

**Note: Do not delete any files or translation lines.**

3. Open Eternum-X.XX.XX-pc/game/tl and make a translation folder called incest_*name* (ex. incest_mom).

4. Copy translation branch files to translation folder.

5. Run the game to compile .RPYCs.

6. Copy updated files in translation folder back to translation branch.

7. Commit translation branch, push to origin.


# Preparing a Translation for Release

**Note: This should be done for each translation that has been updated since the last mod release, for every release. It massively reduces file size and loading time. You can do all translations at the same time by opening game/tl instead of the translation folder in Step 5. Consider writing a program to do the regex replacements automatically.**

1. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to a translation branch (ex. tl/incest_mom).

2. Open Eternum-X.XX.XX-pc/game/tl and make a translation folder called incest_*name* (ex. incest_mom).

3. Copy translation branch files to translation folder.

4. Switch to experimental/translations_main branch.

5. Open translation folder in VSCODE or other IDE.

6. Open Replace in Files with Ctrl+Shift+H and enable 'Use Regular Expression'.

7. Use 'Regex Delete Unchanged' and 'Regex Delete Empty Strings' (below). You will need to use it multiple times, since there is a limit on how many lines you can delete each time.

8. Run the game to compile .RPYCs.

9. Copy translation folder to experimental/translations_main branch in game/tl folder.

10. Commit experimental/translations_main branch, push to origin.


# Building a Release

1. Download and install [Ren'Py 8.3.2 SDK](https://www.renpy.org/release/8.3.2) (the version Eternum runs on).

2. Extract Eternum-X.XX.XX-pc.zip into renpy-8.3.2-sdk folder.

3. Clone [Eternum-IC repo](https://github.com/Lucifer-wen/Eternum-IC) and switch to experimental/translations_main branch.

4. Copy game folder from experimental/translations_main branch to Eternum-X.XX.XX-pc folder.

5. Run the game to compile .RPYCs one last time.

6. Open Ren'Py Launcher (renpy-8.3.2-sdk/renpy.exe) and find the Eternum-X.XX.XX-pc project.

7. Press 'Build Distributions'.

8. Under 'Build Packages:', only select Eternum-IC_vX.X.X.X.

9. Uncheck 'Add from clauses to calls' and 'Force Recompile'.

10. Press 'Build'.

11. The new Release should be in the folder renpy-8.3.2-sdk/Eternum-X.XX.XX-dists.

12. To install, just drag Eternum-IC.rpa into Eternum-X.XX.XX-pc/game.


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


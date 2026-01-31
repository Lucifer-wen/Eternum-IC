## Tools

You can use regex Find with
```
(?<=# )(\w+ ".+)$(?!\n *\1\n\n)|(?<=old )(".*")$(?!\n *new \2)
```
to find lines you've modified.


You can use regex Find with
```
(?: *# \S+.rpy:\d+\n *translate \w+ \w+:\n+ *# (\w* ?".+)$\n *\1\n+| *# \S+.rpym?:\d+\n *old (".*")$\n *new \2\n+)
```
and Replace All with nothing to delete all unchanged lines for RELEASE versions in order to reduce file size and loading time.

Then, you can use regex Find with
```
(?: *translate \w+ strings:(?!\n*.*\n *old ".*"))
```
and Replace All with nothing to delete any empty
```
translate incest_aunt strings:
```


# Important

Working copies should keep *ALL* lines for regeneration with Ren'Py SDK.

Make sure you *ALWAYS* include the .RPYC files as well as the .RPY files and *NEVER* delete them.


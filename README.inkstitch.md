NOTE: This is a fork of the original, https://github.com/EmbroidePy/pyembroidery.  
Releases to PyPi are published from the EmbroidePy repository.

Differences from Upstream
=========================

This fork differs from upstream in several ways:

* We have a differeng G-code writer that satisfies the needs of Ink/Stitch users.
* Our primary branch is named `main`.
* We have a couple of changes and bug-fixes.

Pulling in changes from upstream
================================

To pull in changes from https://github.com/EmbroidePy/pyembroidery, do the following:

1. Clone this repository.
2. Add a remote for `upstream`: `git remote add upstream git@github.com:EmbroidePy/pyembroidery`
3. Fetch upstream: `git fetch upstream`
4. Rebase our changes on upstream's: `git rebase upstream/master`
5. If there are conflicts:
  * fix the conflicting files
  * do `git add <file>` for all conflicting files
  * do `git rebase --continue`
6. **Force-push** the `main` branch to `inkstitch/pyembroidery`.

You can also skip a conflicting commit if upstream applied the same fix (`git rebase`'s output will tell you how to skip).

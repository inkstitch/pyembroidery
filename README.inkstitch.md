NOTE: This is a fork of the original, https://github.com/EmbroidePy/pyembroidery.  
Releases to PyPi are published from the EmbroidePy repository.

Differences from Upstream
=========================

This fork differs from upstream in several ways:

* We have a couple of changes and bug-fixes.

* Additional readers:
  * IQP
  * PLT
  * QCC
* Additional writers:
  * We have a differeng G-code writer that satisfies the needs of Ink/Stitch users.
  * PLT
  * QCC

Pulling in changes from upstream
================================

To pull in changes from https://github.com/EmbroidePy/pyembroidery, do the following:

1. Clone this repository.
2. Add a remote for `upstream`: `git remote add upstream git@github.com:EmbroidePy/pyembroidery`
3. Fetch upstream: `git fetch upstream`
4. Rebase our changes on upstream's: `git rebase upstream/main`
5. If there are conflicts:
  * fix the conflicting files
  * do `git add <file>` for all conflicting files
  * do `git rebase --continue`
6. **Force-push** the `main` branch to `inkstitch/pystitch`.

You can also skip a conflicting commit if upstream applied the same fix (`git rebase`'s output will tell you how to skip).

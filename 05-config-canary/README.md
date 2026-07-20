# Patch 05: Config Canary

**What's broken out of the box:** Claude Code never tells you when your hooks stop existing. It tells you when a hook *fails*, loudly, with a non-zero exit. It says nothing at all when a hook is simply not there anymore, because from the runtime's point of view there is nothing to run and nothing to report. Your setup degrades into a plain chat box and every session after that looks completely normal.

Settings files get clobbered in ordinary ways. A script that swaps `settings.json` and crashes before restoring it. A sync between two machines where the older copy wins. A tool that rewrites the file and drops keys it does not recognize. A hand edit that breaks the JSON so the whole block is skipped. In my case a background script swapped my settings for an isolated profile, got killed by a closed terminal before its restore ran, and my real config sat archived beside the live one for weeks while I worked against a stripped copy.

**The trap in the obvious fix:** register a SessionStart hook that checks whether your hooks are still there. I did exactly that, months before any of this. It never fired, because the wipe that removed my hooks removed the checker along with them. A monitor that lives inside the thing it monitors cannot report the failure that takes them both out. That is the actual lesson, and it is why this patch is a scheduled script and not a hook.

**The fix:** a standalone canary that keeps a known-good snapshot of your settings beside the real one, compares the hook wiring on a schedule, and restores from the snapshot when hooks go missing. It runs outside Claude Code, so it survives whatever takes Claude Code's config down.

It compares hook wiring only, never your whole file, so `model`, `theme`, `permissions` and anything else drift freely without tripping it. Add a hook and it rolls the snapshot forward rather than reverting you.

## Install / Use

Paste this into Claude Code.

````
Install the Config Canary patch from github.com/0xLoqi/claude-code-patches.

1. Fetch https://raw.githubusercontent.com/0xLoqi/claude-code-patches/main/05-config-canary/config_canary.py
   and save it to ~/.claude/config_canary.py (create directories as needed).
2. Take the first snapshot now, and show me the output:
      python ~/.claude/config_canary.py --snapshot
   If it reports 0 hooks, STOP and tell me, because that means my settings.json
   has no hooks to protect and snapshotting it would pin a broken state.
3. Register it to run on a schedule, OUTSIDE Claude Code. This placement is the
   whole point of the patch, so do not "simplify" it into a SessionStart hook.

   On Windows:
      schtasks /Create /TN "ClaudeConfigCanary" /TR "python %USERPROFILE%\.claude\config_canary.py --quiet" /SC HOURLY /F

   On macOS or Linux, add to crontab:
      0 * * * * python3 ~/.claude/config_canary.py --quiet

4. Prove it actually works before we trust it. In a scratch directory, copy my
   settings.json, snapshot it, overwrite the copy with {"hooks":{},"model":"x"},
   run the canary against the copy, and show me that it detected the missing
   hooks and restored them. Never run this test against my real settings.json.
5. Report the scheduled task name, the snapshot path, and the test result.

Then tell me one control in this setup that still shares a failure domain with
the thing it is supposed to be watching.
````

## What changes

**Before:** A script swaps your `settings.json` and dies before restoring it. Every session afterward starts clean, with no hooks, no startup context, and no complaint. You notice weeks later when you finally wonder why a thing you built stopped happening, and you have no idea when it stopped.

**After:** Within the hour, the canary sees that the hooks in your snapshot are absent from the live file, archives the broken copy, restores your real settings, and tells you to restart. The window between "my config got eaten" and "my config is back" is one scheduler tick instead of however long it takes you to notice.

## The trade-off

It restores the snapshot **wholesale**, not key by key. A settings file that lost its hooks is usually a foreign file that replaced yours, so merging would be the wrong call. The cost is that unrelated edits made after the wipe get rolled back too. Your broken copy is archived in `~/.claude/_canary-archive/`, so nothing is lost, but you may have to go get something out of it.

It also only knows what a healthy config looks like from the snapshot. If you snapshot a broken state, it will faithfully protect the broken state. That is why step 2 refuses to snapshot a file with zero hooks.

And it is one more scheduled job, running hourly, forever. If you already have an ops-monitoring habit, put this check inside that instead of adding another timer.

---

*Drops with a LinkedIn post: [Elijah Wilbanks](https://www.linkedin.com/in/elijah-wilbanks/)*

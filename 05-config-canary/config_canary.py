#!/usr/bin/env python3
"""Config Canary: notice when your Claude Code hooks quietly disappear, and put them back.

Runs OUTSIDE Claude Code, on a scheduler. That placement is the entire point. A
canary implemented as a SessionStart hook cannot detect its own removal, because
whatever wiped your hooks wiped the canary too. Put the check in a different
failure domain than the thing it checks.

How it works
------------
It keeps a known-good snapshot of settings.json beside the real one and compares
the hook wiring on every run.

  - No snapshot yet        -> take one, assume current state is healthy, exit.
  - Live has >= snapshot   -> you added hooks. Refresh the snapshot, exit.
  - Live is MISSING hooks  -> restore settings.json from the snapshot, archive
                              the broken copy, and report loudly.

It only ever compares HOOK WIRING, never your whole settings file, so unrelated
keys (model, theme, permissions) can drift freely without tripping it. When it
restores, it restores the snapshot wholesale, because a settings file that lost
its hooks is usually a foreign file that replaced yours rather than yours with an
edit.

Usage
-----
  python config_canary.py             check, and repair if broken
  python config_canary.py --check     check only, exit 1 if broken, change nothing
  python config_canary.py --snapshot  force-refresh the known-good snapshot
  python config_canary.py --settings PATH   point at a non-default settings.json

Exit codes: 0 healthy or repaired, 1 broken (--check only), 2 error.
"""

import argparse
import datetime
import json
import os
import shutil
import sys

DEFAULT_SETTINGS = os.path.expanduser("~/.claude/settings.json")


def hook_commands(settings):
    """Every hook command in the file, as a flat set. Order and nesting do not matter."""
    out = set()
    for event, groups in (settings.get("hooks") or {}).items():
        for group in groups or []:
            for h in (group.get("hooks") or []):
                cmd = str(h.get("command", "")).strip()
                if cmd:
                    out.add(f"{event}::{cmd}")
    return out


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--settings", default=DEFAULT_SETTINGS)
    ap.add_argument("--check", action="store_true", help="report only, change nothing")
    ap.add_argument("--snapshot", action="store_true", help="force-refresh the snapshot")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    settings_p = os.path.abspath(os.path.expanduser(args.settings))
    snap_p = settings_p + ".known-good"
    archive_d = os.path.join(os.path.dirname(settings_p), "_canary-archive")

    def say(msg):
        if not args.quiet:
            print(msg)

    if not os.path.exists(settings_p):
        # A missing settings.json is itself a wipe worth repairing.
        if os.path.exists(snap_p) and not args.check:
            os.makedirs(archive_d, exist_ok=True)
            shutil.copy2(snap_p, settings_p)
            say(f"REPAIRED: {settings_p} was missing entirely, restored from snapshot.")
            return 0
        say(f"ERROR: no settings file at {settings_p}")
        return 2

    try:
        live = load(settings_p)
    except Exception as e:
        say(f"ERROR: settings.json is unreadable ({e}). Not touching it.")
        return 2

    live_hooks = hook_commands(live)

    if args.snapshot or not os.path.exists(snap_p):
        if args.check:
            say("no snapshot yet; nothing to compare against")
            return 0
        shutil.copy2(settings_p, snap_p)
        say(f"snapshot taken: {len(live_hooks)} hook(s) recorded as known-good")
        return 0

    try:
        snap_hooks = hook_commands(load(snap_p))
    except Exception as e:
        say(f"ERROR: snapshot is unreadable ({e})")
        return 2

    missing = snap_hooks - live_hooks

    if not missing:
        # Healthy. If hooks were ADDED, roll the snapshot forward so the canary
        # tracks your real setup instead of pinning you to an old one.
        if live_hooks - snap_hooks and not args.check:
            shutil.copy2(settings_p, snap_p)
            say(f"healthy; snapshot rolled forward (+{len(live_hooks - snap_hooks)} new hook(s))")
        else:
            say(f"healthy; {len(live_hooks)} hook(s) present")
        return 0

    # Broken.
    say(f"BROKEN: {len(missing)} hook(s) present in the snapshot are missing from settings.json:")
    for m in sorted(missing):
        say("  - " + m)

    if args.check:
        return 1

    os.makedirs(archive_d, exist_ok=True)
    shutil.copy2(settings_p, os.path.join(archive_d, f"settings.json.broken.{stamp()}"))
    shutil.copy2(snap_p, settings_p)
    say(f"REPAIRED: restored settings.json from snapshot. Broken copy archived in {archive_d}.")
    say("Restart Claude Code so the restored hooks load.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)

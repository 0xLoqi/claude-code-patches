# Patch 03: Blocker Review

**What's broken out of the box:** Claude Code keeps a complete record of every session in `~/.claude/projects/*/*.jsonl`, but nothing reads it. You hit the same friction over and over (rejected tool calls, permission prompts you keep approving, bash errors from the same env quirk, course corrections you keep making) and every session starts fresh. The signal is sitting on disk; the loop never closes.

**The fix:** A skill that scans your session logs, finds where you blocked Claude (rejections, interrupts, corrections, env failures), and proposes permanent fixes per blocker. Run it weekly and the friction monotonically drops.

Inspired by Felix/OpenClaw's daily blocker review for the same reason: the cheapest way to make the next session smoother is to read what made the last one rough.

## Install

Paste this prompt into Claude Code. It will install the skill at `~/.claude/skills/blocker-review/SKILL.md`.

````
Install the Blocker Review patch from github.com/0xLoqi/claude-code-patches/03-blocker-review.

1. Create directory `~/.claude/skills/blocker-review/` if it doesn't exist.
2. Fetch the SKILL.md file from this patch's GitHub directory and save it to `~/.claude/skills/blocker-review/SKILL.md`. If WebFetch isn't available, ask me to paste the SKILL.md content and write what I paste.
3. Verify the skill is registered by listing files in `~/.claude/skills/blocker-review/`.
4. Tell me the slash commands now available: `/blocker-review`, `/blocker-review 3`, `/blocker-review week`. Run `/blocker-review` once now against the last 24h of my session logs and present the report.

The skill scans `~/.claude/projects/*/*.jsonl` for blocker patterns (tool rejections, user interrupts, course corrections, repeated permission prompts, environment failures), proposes permanent fixes per blocker, and writes the report to `~/.claude/blocker-reviews/YYYY-MM/`.

After the first run, ask me which quick-win fixes to apply.
````

## What changes

Before: friction repeats. You approve the same permission prompt, hit the same env error, get the same kind of correction across sessions. Each session starts as a clean slate that re-encounters last session's lessons.

After: weekly closes the loop. Sample report from a real session:

```
# Blocker Review: 2026-05-04

Sessions analyzed: 7
Total blockers detected: 55
Real corrections: 2  |  Hard rejections: 1
Env-failure blockers: 39

Top Blockers:

1. `rtk` prefixed onto subcommands rtk doesn't handle (cat, awk, mkdir, cp, pwd, wc)
   Cat E (env failure) | 14 occurrences | ~25 turns lost
   Proposed fix: CLAUDE.md correction (rtk version was stale)

2. Anti-gate violations ("should I / want me to") inside long sessions
   Cat D (unnecessary permission prompts) | 75 occurrences across 2 megasessions
   Proposed fix: hook (optional) or CLAUDE.md reinforcement
...

Quick Wins:
1. Update CLAUDE.md rtk section: enumerate which commands rtk handles
2. Add CLAUDE.md line: stale .git/index.lock → diagnose, don't retry
3. Investigate stale hook reference left over from a workspace migration

Apply? Pick numbers or say "all".
```

The "snowball trust" angle: tool rejections, interrupts, and corrections should trend down review-over-review. If they don't, something is broken in the loop.

## When to run

- Weekly cadence is the default.
- Before starting a long session in a domain you keep hitting friction in.
- After major workspace changes (restructures, tool installs, hook changes) to catch what broke.
- When you suspect Claude is repeating mistakes — it usually is, and the logs say where.

## Tips for actual use

**The first review will surface a lot.** Don't try to fix everything; pick the top three quick wins by cost (turns wasted) and ship those. The next review will rank the remaining items more accurately because the noisy ones got absorbed.

**Filter false-positives in your head.** "No files found" inside a user-role message looks like a correction but is just a Glob/Grep tool result. The skill filters the obvious ones; you'll catch the rest.

**Check tool versions before patching.** If a blocker is "tool X errors a lot," check whether X is current before designing a workaround. A stale tool can manufacture a 30-blocker review entirely from one bug that was fixed upstream months ago. (Ask how I know.)

## Output location

Reports land in `~/.claude/blocker-reviews/YYYY-MM/YYYY-MM-DD-blocker-review.md`. Trend tracking compares against prior reports in the same directory automatically.

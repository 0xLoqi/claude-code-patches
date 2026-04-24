# Patch 01: Take Ownership

**What's broken out of the box:** When you ask Claude Code to do something, it often outlines the steps instead of doing them. "Here's how you could run this script." "You might want to check X." "You can use this prompt to..."

You didn't ask for instructions. You asked it to do the thing.

**The fix:** A CLAUDE.md rule that tells Claude explicitly to take ownership of tasks it has the tools to execute, and only gate on genuinely irreversible or high-stakes decisions.

## Install

Open your global `CLAUDE.md` at `~/.claude/CLAUDE.md` (create if it doesn't exist), and paste the contents of [`CLAUDE.md`](./CLAUDE.md) in this folder.

Or if you only want this to apply to one project, paste it into the `CLAUDE.md` in that project's root.

Restart your Claude Code session.

## What changes

Before:
> You can run `npm install` to get the dependencies, then `npm run dev` to start the server. Let me know if you want me to help with anything else!

After:
> Running `npm install` and `npm run dev`... dev server up on port 3000, no errors.

The default shift: Claude stops handing you instructions and starts executing. You get outputs, not outlines.

## The trade-off

Claude will take more actions without explicit permission. The rule has built-in exceptions for genuinely risky ops (money, irreversible actions, destructive commands), but you're giving up some of the "are you sure?" friction. That's the point.

If you work on production systems where auto-execution could cause real damage, tighten the exceptions list before pasting.

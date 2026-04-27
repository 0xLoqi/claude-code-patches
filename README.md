# Claude Code Patches

**Out of the box, Claude Code doesn't know what it can do.**

It defaults to advisor mode: outlines steps, gives you prompts, drafts plans for you to execute. You wanted it to *do the thing*.

This repo is a library of patches that flip Claude from advisor mode into doer mode. Each patch is a single prompt you paste into Claude Code. Claude installs the patch on your machine, appends rules to your `CLAUDE.md`, and self-announces when the patch fires so you can watch it work.

No install instructions. No "open this file, edit that line, restart this thing." You paste the prompt, Claude does the rest.

---

## How It Works

Each patch in this repo has a `README.md` with:

1. **The failure mode** out of the box (what Claude does wrong)
2. **The install prompt** — one block, copy it, paste it into Claude Code, done
3. **What changes** — before/after examples of how Claude behaves once installed

Behind the scenes, the install prompt tells Claude to:
- Run any required install commands (MCP servers, dependencies)
- Append the patch's rule to your `~/.claude/CLAUDE.md`
- Verify the install worked
- **Self-announce** the first time the patch fires in a session, prepending a tag like `[Doer Mode]` or `[Chrome DevTools]` so you can see the patch in action

The self-announce makes the patches *teachable* — you watch Claude reach for them in the wild and learn when each one applies.

---

## The Patches

| # | Patch | What it fixes |
|---|-------|---------------|
| 01 | [Doer Mode](./01-take-ownership/) | Claude outlines steps instead of doing the work |
| 02 | [Chrome DevTools MCP](./02-chrome-devtools-mcp/) | Claude can't drive your browser |

More patches dropping weekly. Star the repo to get notified.

---

## The Thesis

Most Claude Code users are running at 20% of what the tool can do. They tried it once, felt it was "fancy autocomplete," and moved on. That's not Claude's fault, that's the defaults.

The gap between advisor mode and doer mode is the biggest unlock in the product. These patches are how you cross it.

---

## What's Coming

- More patches mined from real power use (memory rules, hooks, MCP servers, skills, behavior corrections)
- A hands-on setup walkthrough for people who want the full system installed and explained end-to-end ([email me](mailto:elijah.wbanks@gmail.com) if interested, limited spots)
- A Discord or Telegram for people running the patches to share what they're shipping with them

---

## Follow Along

- LinkedIn: [Elijah Wilbanks](https://www.linkedin.com/in/elijah-wilbanks/) — each new patch drops with a post explaining the failure it fixes
- GitHub: star this repo to get notified of new patches

## License

MIT. Use, modify, remix, sell your own course on top. Credit appreciated but not required.

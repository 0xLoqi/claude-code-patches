# Claude Code Patches

**Out of the box, Claude Code doesn't know what it can do.**

It defaults to advisor mode: tells you the steps, gives you prompts, drafts test plans. You wanted it to *do the thing*.

This repo is the collection of patches that flip Claude Code from advisor mode into doer mode. Each one is a fix for a specific failure mode I caught while actually using Claude Code to ship real products. Copy-paste into your own setup, feel the difference in your first session.

---

## The Patches

| # | Patch | What it fixes | Install time |
|---|-------|---------------|--------------|
| 01 | [Take Ownership](./01-take-ownership/) | Claude outlines steps instead of doing the work | 30 seconds |
| 02 | [Chrome DevTools MCP](./02-chrome-devtools-mcp/) | Claude can't actually drive your browser | 5 minutes |

More patches dropping weekly. Star the repo to get notified.

---

## How to Use

Each patch lives in its own folder with a README explaining:
- The failure mode out of the box
- The fix
- How to install it
- What changes in your day-to-day

Patches marked with `CLAUDE.md` have a snippet you paste into your own `CLAUDE.md` file (global at `~/.claude/CLAUDE.md` or project-level in the repo root). MCP patches have install commands. Hook patches have `settings.json` config.

---

## The Thesis

Most Claude Code users are running at 20% of what the tool can do. They tried it once, felt it was "fancy autocomplete," and moved on. That's not Claude's fault, that's the defaults.

The gap between advisor mode and doer mode is the biggest unlock in the product. These patches are how you cross it.

---

## What's Coming

- More patches from my actual setup (memory system, hooks, skills, MCP config)
- A hands-on setup walkthrough for people who want the full system dropped in, configured, and explained end-to-end ([email me](mailto:elijah.wbanks@gmail.com) if interested — limited spots)
- A Discord or Telegram for people running the patches to share what they're building

---

## Follow Along

- LinkedIn: [Elijah Wilbanks](https://www.linkedin.com/in/elijah-wilbanks/) — each new patch drops with a post explaining the failure it fixes
- GitHub: star this repo to get notified of new patches

## License

MIT. Use, modify, remix, sell your own course on top. Credit appreciated but not required.

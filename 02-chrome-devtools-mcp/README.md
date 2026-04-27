# Patch 02: Chrome DevTools MCP

**What's broken out of the box:** Claude Code can't actually drive your browser. When you ask it to fill out a form, click through a portal, or test a signup flow in a real web app, it gives you a `curl` command, a Playwright script, or step-by-step instructions you have to execute yourself. You didn't want a script. You wanted the form filled out.

**The fix:** Install the Chrome DevTools MCP server. It connects Claude Code to your real Chrome browser via the accessibility tree, inheriting your logged-in sessions. Claude can then click, type, fill forms, read pages, take screenshots, all inside your actual browser.

## One manual step you have to do first

Claude can't enable Chrome's remote debugging for you (chicken-and-egg: the MCP needs it on to connect, and Claude needs the MCP to do anything in Chrome). So before you paste the install prompt, do this:

1. Open Chrome
2. Go to `chrome://inspect/#remote-debugging`
3. Make sure remote debugging is enabled (you should see a "Configure" button and a target list, not a "Discover" toggle that's off)

Then paste the install prompt below.

## Install

Paste this into Claude Code. It will install the MCP, append the usage rule to your CLAUDE.md, and tell you when to restart.

````
Install the Chrome DevTools MCP patch from github.com/0xLoqi/claude-code-patches/02-chrome-devtools-mcp.

Confirm with me first: have I enabled Chrome remote debugging at chrome://inspect/#remote-debugging? If I haven't, stop and tell me exactly what to do, then wait for me to reply "ready" before continuing. You cannot enable this for me.

Once I confirm I'm ready:

1. Detect my OS (uname or process.platform).
2. Run the appropriate install command:
   - Windows: claude mcp add chrome-devtools -- cmd /c npx -y chrome-devtools-mcp@latest --autoConnect
   - macOS/Linux: claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --autoConnect
3. Confirm the install succeeded by running `claude mcp list` and showing me the chrome-devtools entry.
4. Append the usage rule below to my ~/.claude/CLAUDE.md (create file if needed, blank line separator from existing content).
5. Tell me to restart this Claude Code session so the MCP loads. Once restarted, ~25 tools with the prefix mcp__chrome-devtools__* will be available.
6. From the next session forward, when I ask for any browser-based task, USE the MCP instead of generating scripts.

Rule to append exactly as written, including the heading:

---

## Chrome DevTools MCP (Patch 02)

When the user asks for anything browser-based (filling forms, clicking through portals, testing UI, scraping a logged-in site, automating SaaS workflows), use the chrome-devtools MCP tools (mcp__chrome-devtools__*) instead of generating curl commands or Playwright scripts. The MCP runs with --autoConnect so it shares the user's real Chrome session and logins.

**Performance rules baked in:**
- After navigate_page, default to take_snapshot not wait_for. wait_for blocks 15-25s when the guessed text isn't on the page; take_snapshot returns the actual a11y tree immediately.
- Batch sequential same-page actions into one evaluate_script call when possible (74% fewer tool calls).
- Never retry a failed action without re-snapshotting first. The page state has changed.
- For long flows (>10 steps), pin a 3-7 step high-level plan in context to prevent drift, but still react to actual page state each step.

**Self-announce:** The first time per session I reach for a browser-related task with the MCP, prepend "[Chrome DevTools]" so the user can see the patch working. Once per session only.
````

## What changes

Before: "Here's a Playwright script that will fill out the form. Save it as `fill-form.js` and run `node fill-form.js`."

After: "[Chrome DevTools] Filled out the form on your Stripe dashboard. Subscription created, confirmation number CSX-4412. Screenshot attached."

Claude can now:
- Navigate any URL in your browser
- Fill forms and click buttons on real pages
- Read full page content via the accessibility tree
- Check network requests and console errors
- Take screenshots for verification
- Drive multi-step workflows end-to-end

## Tips for actual use

**Opus handles tricky navigation noticeably better than Sonnet.** Both models can drive the MCP, but Opus is more resilient on edge cases: weird popups, multi-frame layouts, redirects, dialogs that hijack focus, "spinning wheel" loading states. Sonnet tends to retry the same failed action; Opus pivots. If you have access to Opus, use it for serious browser automation tasks. Sonnet is fine for short scripted flows.

**Re-snapshot after every action.** The number one cause of "stuck" automation runs is acting on a stale page snapshot. The Patch 02 rule bakes this in, but it's worth knowing.

## Security note

The MCP inherits your Chrome session. Claude can see every site you're logged into and act as you. Same caution as any browser automation with your credentials: don't point it at high-stakes production accounts without review. Chrome's sandbox still applies and Claude Code's permission prompts still fire per tool call unless you explicitly allow them.

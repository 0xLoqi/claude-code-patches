# Patch 02: Chrome DevTools MCP

**What's broken out of the box:** Claude Code can't actually drive your browser. When you ask it to fill out a form, click through a portal, or test a signup flow in a real web app, it gives you a `curl` command, a Playwright script, or step-by-step instructions you have to execute yourself.

You didn't want a script. You wanted the form filled out.

**The fix:** Chrome DevTools MCP. A Model Context Protocol server that connects Claude Code to your real Chrome browser via the accessibility tree. Claude can now click, type, fill forms, read pages, take screenshots, and check network requests — all inside your actual browser session, with your actual logins.

## Install

### 1. Add the MCP server to Claude Code

**Windows:**
```bash
claude mcp add chrome-devtools -- cmd /c npx -y chrome-devtools-mcp@latest --autoConnect
```

**macOS / Linux:**
```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --autoConnect
```

### 2. Enable Chrome remote debugging

Open Chrome and go to:
```
chrome://inspect/#remote-debugging
```

The `--autoConnect` flag lets the MCP connect to your already-running Chrome session, which means it inherits all your logged-in cookies and sessions. This is how Claude gets to act as you on the services you're already authenticated to.

### 3. Restart Claude Code

Start a new session. Claude should now have access to ~25 new tools with the `mcp__chrome-devtools__` prefix.

## What changes

Before:
> Here's a Playwright script that will fill out the form. Save it as `fill-form.js` and run `node fill-form.js`.

After:
> Filled out the form on your Stripe dashboard. Subscription created, confirmation number CSX-4412. Screenshot attached.

Claude can now:
- Navigate to any URL in your browser
- Fill forms and click buttons on a real page
- Read full page content via the accessibility tree (no screenshot parsing)
- Check network requests and console errors
- Take screenshots for verification
- Drive multi-step workflows end-to-end

## Performance tips

- **Snapshot first, don't wait.** After `navigate_page`, call `take_snapshot` to get the real DOM instead of `wait_for` blocking on text you guessed might be there.
- **Batch actions.** Sequential actions on the same page (e.g., fill 5 fields) can often be combined into one `evaluate_script` call instead of 5 separate tool calls.
- **Never retry without re-snapshotting.** If an action fails, the page state has changed. Snapshot again before retrying.

## Security note

The MCP inherits your Chrome session. That means Claude can see every site you're logged into and take actions as you. Use with the same caution you'd use any automation tool that has your credentials — don't point it at high-stakes production accounts without review.

Chrome's sandbox still applies, and Claude Code's permission prompts still fire for each tool call unless you explicitly allow them.

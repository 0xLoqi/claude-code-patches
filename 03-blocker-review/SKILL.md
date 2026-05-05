---
name: blocker-review
description: Review session logs to find where the human blocked the AI, then propose permanent fixes to remove those blockers.
---

# Blocker Review

Inspired by Felix/OpenClaw's daily blocker review. Every time Claude had to wait for the user, got rejected, hit a permission wall, or was interrupted mid-flow, that's friction. This skill finds those moments and proposes permanent fixes.

## How to Use

```
/blocker-review              # Review today's sessions
/blocker-review 3            # Review last 3 days
/blocker-review week         # Review last 7 days
```

## Instructions

When the user invokes this skill:

### 1. Gather Session Logs

Read all `.jsonl` files from `~/.claude/projects/*/` (every project subdirectory) modified within the time window. The project subdirectory name encodes the path of the project root and varies per machine.

Use `python` (not `python3`) for all scripting. Always open files with `encoding='utf-8', errors='replace'`.

Session log format:
- Each line is a JSON object
- Key fields: `type` (user/assistant/progress/system), `message.content` (array of content blocks), `timestamp`
- Skip types: `queue-operation`, `file-history-snapshot`, `progress`

### 2. Detect Blocker Events

Parse each session and categorize blockers:

#### Category A: Tool Rejections (Human said no)
- `tool_result` blocks where `is_error: true` AND text contains "rejected" or "doesn't want to proceed"
- These mean Claude tried to do something and the user blocked it
- **Extract**: What tool was called, what it was trying to do, and why it was rejected

#### Category B: User Interrupts (Human cut Claude off)
- User messages containing "interrupted by user" or "Request interrupted"
- These mean Claude was mid-action and the user stopped it
- **Extract**: What Claude was doing when interrupted, what the user said next (the correction)

#### Category C: Course Corrections (Human redirected)
- User messages that start with corrections: "no", "not that", "instead", "stop", "wait", "actually"
- Or messages that repeat a prior instruction (Claude didn't get it the first time)
- **Extract**: What Claude was doing wrong, what the user wanted instead

#### Category D: Repeated Permission Prompts
- Multiple tool rejections of the same tool type in a session (user keeps getting asked)
- Or patterns where Claude asks "should I..." and user says "just do it"
- **Extract**: What permission/confirmation was unnecessary

#### Category E: Environment Failures
- `tool_result` with `is_error: true` from Bash commands (exit codes, missing tools, path issues)
- These are infrastructure problems that waste time
- **Extract**: What failed, root cause, whether it's a recurring issue

### 3. Analyze Each Blocker

For each detected blocker, determine:

1. **Was this a one-off or a pattern?** Check if similar blockers appear across multiple sessions.
2. **What was the cost?** Count messages between the blocker and resolution (rough proxy for wasted time).
3. **Is there a permanent fix?** Categorize the fix:
   - **Permission fix**: Add to `settings.local.json` allowlist, or switch to `bypassPermissions` for specific tools
   - **CLAUDE.md fix**: Add instruction so Claude doesn't attempt the blocked action
   - **Memory fix**: Save a feedback memory so future sessions know the preference
   - **Hook fix**: Create a hook that automates what the human had to manually approve
   - **Skill fix**: Build/modify a skill to handle the workflow correctly
   - **Infrastructure fix**: Install missing tool, fix PATH, configure environment, upgrade a stale dependency
   - **No fix available**: Some blockers are legitimate (human judgment calls)

### 4. Present the Report

```markdown
# Blocker Review: [date range]

## Summary
- Sessions analyzed: N
- Total blockers detected: N
- Fixable: N | Already handled: N | Legitimate blocks: N

## Top Blockers (by frequency/cost)

### 1. [Blocker title]
**Category**: [A-E]
**Occurrences**: N times across M sessions
**What happened**: [1-2 sentence description]
**Cost**: ~N messages wasted each time
**Proposed fix**: [Specific, actionable fix]
**Fix type**: [permission/claude-md/memory/hook/skill/infrastructure]

### 2. [Next blocker...]
...

## Quick Wins (fixes I can apply right now)
- [ ] [Fix 1 - specific action]
- [ ] [Fix 2 - specific action]
- [ ] [Fix 3 - specific action]

## Needs Discussion
- [Blocker that requires human judgment about the fix]

## Snowball Trust Score
- Tool rejections this period: N
- Interrupts this period: N
- Course corrections this period: N
- Trend: [improving/stable/degrading] vs last review
```

### 5. Offer to Apply Fixes

After presenting the report, ask which quick wins to apply. Common fix types:
1. Update settings/permissions
2. Append CLAUDE.md instructions
3. Save feedback memories
4. Create or modify hooks

Execute whichever the user picks. For each fix applied, note what was changed so the next blocker review can track improvement.

### 6. Save the Report

Write the report to `~/.claude/blocker-reviews/YYYY-MM/YYYY-MM-DD-blocker-review.md`. Create the directory if it doesn't exist.

If this is not the first review, compare against previous reports in that directory to show trend data in the Snowball Trust Score section.

## Parsing Tips

When writing the Python parser:

```python
import json, os, glob, time

session_root = os.path.expanduser('~/.claude/projects/')
cutoff = time.time() - (days * 86400)

files = []
for project_dir in glob.glob(os.path.join(session_root, '*/')):
    for f in glob.glob(os.path.join(project_dir, '*.jsonl')):
        if os.path.getmtime(f) > cutoff:
            files.append(f)

for path in files:
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            obj = json.loads(line)
            msg_type = obj.get('type', '')
            if msg_type in ('queue-operation', 'file-history-snapshot', 'progress'):
                continue
            # Process user/assistant/system messages...
```

Key patterns to match in content blocks:
- Tool rejection: `c.get('type') == 'tool_result' and c.get('is_error') == True`
- Rejection text: `"doesn't want to proceed"` or `"was rejected"`
- User interrupt: `"Request interrupted by user"` or `"interrupted by user"`
- Bash error: `is_error == True` with `"Exit code"` in text
- Course correction: user message starting with negation after an assistant message

Filter out tool-result echoes that look like user messages but aren't real corrections: `"No files found"`, `"No matches found"`, `"No matching deferred tools found"`.

## Important Notes

- Large session files can be slow to parse. Use streaming (line by line), don't load entire files into memory.
- The goal is compound improvement. Each review should make the next session smoother.
- Don't propose removing ALL human oversight. Some blocks are good. Flag those as "legitimate" and move on.
- Track the snowball: over weeks, the ratio of blockers to productive messages should decrease.
- Symptoms in environment failures sometimes hide structural causes (e.g., a stale tool version producing a stream of errors). Before recommending a code-side fix, check whether the underlying tool is current.

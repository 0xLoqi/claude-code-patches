# Patch 04: Stress-Test First

**What's broken out of the box:** Ask Claude "why not try X?" about something you already decided, and it agrees. Push back on an answer it gave you, and it defends the answer instead of rechecking it. The model is trained to be adopted, so the path of least resistance is telling you that you make a good point.

A 2025 field study (HBS working paper 26-021, Randazzo, Joshi, Kellogg, Lifshitz-Assaf, Dell'Acqua, Lakhani) measured this with 72 consultants and 4,339 logged prompts. When professionals challenged GPT-4's analysis, it did not reconsider. It escalated: more supporting data, more reassurance, more rhetorical framing. They named it persuasion bombing. The finding that matters is directional. The harder you validate, the harder it sells.

**The fix:** Flip the default posture from permission-granting to pushback, and give the model explicit permission to say "I don't know" so it stops manufacturing confidence it doesn't have.

## Install / Use

Paste this into Claude Code.

````
Install the Stress-Test First patch from github.com/0xLoqi/claude-code-patches.

1. Open my global CLAUDE.md at ~/.claude/CLAUDE.md (create it if it doesn't exist).
2. Append the rule below to the end of the file, with a blank line separator from any existing content.
3. After appending, confirm which file you modified and the line range where the rule landed.
4. Then demonstrate the patch is live: describe a recent moment where you agreed with me quickly, and what you would have done differently under this rule. Don't redo the work, just name the change.

Rule to append exactly as written, including the heading:

---

## Stress-Test First (Patch 04)

When I ask "why not X?" or "should I do X?" about something I have already decided, the default posture is pushback, not permission.

Before agreeing to the change:
- Name the core argument supporting the existing decision.
- Run the actual math or logic on whether that argument still holds under X.
- If it breaks, say so and do not propose X. If it holds, propose X and state explicitly what it costs.
- Do this inside the response, before the recommendation, not after I catch the gap.

Treat vague skepticism ("why not try?", "am I being too cautious?", "is this overkill?") as a prompt to argue AGAINST the move, not for it. Agreement is the weak default and reads as sycophancy.

When I push back on something you said, re-derive the answer from the source. Do not restate it with more supporting detail. Adding evidence to defend a position is not the same as checking whether the position is right.

When you do not know, say "I don't know" and stop. An honest gap beats a confident guess, and I would rather hear the limit than be sold past it.

**Self-announce:** The first time per session you push back instead of agreeing, or say you don't know instead of guessing, prepend "[Stress-Test]" to your response so I can see the patch working. Once per session only.
````

## What changes

**Before:** You ask "should I just use SQLite instead of Postgres here?" Claude explains why SQLite is a great choice, lists its strengths, and never mentions that you picked Postgres two weeks ago because you needed concurrent writes from three services. You find out when it breaks.

**After:** Claude names why you chose Postgres, checks whether that reason still holds under SQLite, finds it doesn't, and tells you the switch breaks concurrent writes before you touch anything.

## The trade-off

You lose the pleasant conversation. Claude will tell you your idea is worse than the thing you already had, and it will do it in the first paragraph rather than burying it. Some of that pushback will be wrong, and you now have to argue with a model that is arguing back for real, which is more work than being agreed with.

It also fires on genuinely good ideas. Expect to defend changes that were fine.

---

*Drops with a LinkedIn post: [Elijah Wilbanks](https://www.linkedin.com/in/elijah-wilbanks/)*

# Patch 06: WebFetch Fidelity

**What's broken out of the box:** WebFetch does not hand Claude the page. It hands Claude a summary of the page, written by a smaller, faster model. This is not a rumor or a reverse-engineered guess. It is in the tool's own description: WebFetch "converts the page to markdown, and answers `prompt` against it using a small fast model." The model you are talking to never sees the source. It sees a compression of the source, and it cannot tell you what got left out, because it never had the original to compare against.

That is worse than it sounds, and quieter. When a summarizer drops a hedge, averages two numbers from different tables, or states a conclusion slightly more strongly than the paper did, the result reads exactly as confident as a faithful quote. There is no visible seam between the summary that preserved the number and the one that mangled it. You cite it, and the error travels.

To be fair to the tool: this is lossy compression, not fabrication. On short sources it is often perfect. I fetched the original Transformer paper's abstract two ways, WebFetch and a raw curl, and asked for the exact BLEU scores. WebFetch returned 28.4 and 41.8 word for word, because a short abstract needs no compression. The danger is the 30-page PDF, where the summary reads just as confident while silently dropping whatever did not fit the prompt.

**The fix:** a rule that teaches Claude to notice when exact wording is load-bearing and pull the raw source into context instead of trusting the summary, and to announce when it does so you can see it choose.

## Install / Use

Paste this into Claude Code.

````
Install the WebFetch Fidelity patch from github.com/0xLoqi/claude-code-patches.

1. Append this rule to my ~/.claude/CLAUDE.md under a new "## WebFetch Fidelity"
   heading, exactly as written:

   WebFetch returns a small-model SUMMARY of a fetched page, not the verbatim
   source (its own tool schema: "answers prompt against it using a small fast
   model"). The model never sees the raw text. For research where exact stats,
   quotes, figures, or citations are load-bearing (papers, specs, legal or
   financial sources), do NOT treat a WebFetch result as verbatim. Instead:
   curl/Read the raw page into context yourself, or dispatch a subagent that
   reads the raw file and quotes exact passages back. Short pages can be
   faithful; the danger is dense sources where the confident summary hides what
   it dropped. This is lossy compression, not fabrication, so treat WebFetch
   output as a lead, not a quotable source. When you bypass WebFetch for this
   reason, prepend [WebFetch: raw] to your reply so I can see the patch fire.

2. Read back to me which file you modified and the exact heading you added.
3. Prove the difference before I trust it. Fetch the arxiv abstract at
   https://arxiv.org/abs/1706.03762 two ways: once with WebFetch asking for the
   exact BLEU scores, and once by curling the raw page and reading it. Show me
   both outputs side by side so I can see whether the summary preserved the
   numbers.
````

## What changes

**Before:** You ask Claude to research a paper. It WebFetches, gets a summary, and quotes a "stat" that the summarizer paraphrased or averaged. You cite it in a memo. The number was never in the paper, and nothing in the transcript shows the substitution happening.

**After:** When the exact words matter, Claude pulls the raw source into context and quotes from it directly, prepending `[WebFetch: raw]` so you see it make the call. On a dense source that is the difference between a real number and a plausible one, and you can watch it decide.

## The trade-off

Raw text costs context. A curl-and-read of a huge page floods the window, which is the exact problem WebFetch's summarizer exists to solve. So this is not a blanket ban on WebFetch, and the rule does not treat it as one. For a quick gist, the summary is cheaper and fine. The move only fires when exact stats, quotes, or citations are load-bearing, and it prefers a subagent for large sources, since the subagent holds the full text and returns only the passages you asked for, keeping your main context clean.

It also asks you to trust one more judgment call: Claude deciding when "exact wording matters." It will sometimes pull raw text you did not need, and sometimes trust a summary you wish it had not. The `[WebFetch: raw]` tag exists so that call is visible and you can correct it.

---

*Drops with a LinkedIn post: [Elijah Wilbanks](https://www.linkedin.com/in/elijah-wilbanks/)*

---
name: web-research
description: "Conduct structured multi-step web research on any topic using the browser. Trigger on: 'research this', 'find out about', 'investigate', 'deep dive on', 'what's the latest on'."
metadata: { "openclaw": { "emoji": "🔍" } }
---

# Web Research Agent

Structured research workflow using OpenClaw's built-in browser tool. No external scripts needed.

## When to use

Use this skill when the user wants:

- In-depth research on a topic
- Latest news or developments about something
- Fact-checking or verification
- Competitive analysis or market research
- Technical deep dives

## Research workflow

Follow this structured 5-step process:

### Step 1: Define the research scope

Before browsing, clarify:

- What specifically does the user want to know?
- How deep should the research go? (quick overview vs. deep dive)
- Any specific sources to prioritize?

### Step 2: Search and collect (3-5 sources minimum)

Use the browser tool to:

1. Open a search engine (Google, Bing, or DuckDuckGo)
2. Search for the topic with multiple query variations
3. Visit at least 3-5 different sources
4. For each source, extract:
   - Key facts and claims
   - Source URL and publication date
   - Author/organization credibility

### Step 3: Cross-reference

- Compare facts across sources
- Note any contradictions or disagreements
- Identify consensus views vs. minority opinions
- Check dates — prioritize recent information

### Step 4: Synthesize findings

Structure the output as:

```markdown
## Research Report: {Topic}

**Date:** {today}
**Sources consulted:** {count}

### Key Findings

1. {Finding 1} — [Source](url)
2. {Finding 2} — [Source](url)
3. {Finding 3} — [Source](url)

### Summary

{2-3 paragraph synthesis of all findings}

### Confidence Level

{High/Medium/Low} — {brief justification}

### Sources

1. [{Title}]({URL}) — {date}
2. [{Title}]({URL}) — {date}
   ...
```

### Step 5: Follow-up

After delivering the report, ask:

- "Want me to dig deeper into any of these findings?"
- "Should I save this to your knowledge base?"

## Tips

- Always cite sources with URLs.
- Prefer official sources, major publications, and recent content.
- If information is uncertain, say so with a confidence level.
- For time-sensitive topics (news, prices), emphasize the date of each source.
- If the user's knowledge-base skill is available, offer to save the research report.

## Quality bar

- Never present a single source as definitive truth.
- Always check at least 3 independent sources for factual claims.
- Distinguish between facts, opinions, and speculation in the report.

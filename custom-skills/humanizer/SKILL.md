---
name: humanizer
description: "Rewrite AI-generated text to sound natural and human. Trigger on: 'humanize', 'make this sound human', 'rewrite naturally', 'remove AI patterns', 'make this less robotic'."
metadata: { "openclaw": { "emoji": "✍️" } }
---

# AI Content Humanizer

Rewrites AI-generated text to sound natural and human. No external tools needed — this is a prompt-only skill.

## When to use

Use this skill when the user:

- Asks to "humanize" text
- Wants text to "sound more natural" or "less AI"
- Needs to rewrite content for publishing
- Says "make this sound human" or "remove AI patterns"

## Humanization process

When triggered, apply ALL of the following 12 checks to the input text:

### Pattern checks

1. **Filler openers** — Remove "Certainly!", "Of course!", "Absolutely!", "Great question!", "That's a great point!"
2. **Passive voice overuse** — Convert passive constructions to active voice where natural.
3. **Hedging language** — Reduce excessive "It's important to note that", "It's worth mentioning", "It should be noted that".
4. **List addiction** — Not everything needs to be a bulleted list. Convert short lists into flowing prose.
5. **Superlative stacking** — Tone down "incredibly powerful", "extremely important", "absolutely essential".
6. **Transition word spam** — Reduce "Furthermore", "Moreover", "Additionally", "In conclusion", "However".
7. **Repetitive sentence structure** — Vary sentence length and structure. Mix short punchy sentences with longer ones.
8. **Over-explanation** — Cut obvious explanations. Trust the reader's intelligence.
9. **Emoji/exclamation overuse** — Use sparingly, not every paragraph.
10. **Corporate speak** — Replace "leverage", "utilize", "implement" with "use", "try", "do".
11. **Artificial enthusiasm** — Tone down forced excitement. Be genuine.
12. **Perfect grammar syndrome** — Real humans occasionally use fragments. Start sentences with "And" or "But". Use contractions.

### Tone options

If the user specifies a tone, apply it:

- **casual** — Conversational, like texting a friend. Contractions, short sentences, personality.
- **professional** — Clean and clear, but still human. No jargon for jargon's sake.
- **academic** — Formal but not robotic. Precise language, proper citations style.

Default tone: **professional**.

## How to respond

1. Apply all 12 checks to the input text.
2. Rewrite the text with fixes applied.
3. Return ONLY the rewritten text — do not list what you changed or explain the process unless asked.
4. If the text is already natural-sounding, say so and return it unchanged.

## Examples

**Before (AI-generated):**

> It's important to note that implementing a robust authentication system is absolutely essential for any modern web application. Furthermore, utilizing industry-standard protocols such as OAuth 2.0 can significantly enhance the security posture of your application. Additionally, it's worth mentioning that regular security audits should be conducted to ensure ongoing protection.

**After (humanized):**

> A solid auth system isn't optional for web apps anymore. Use OAuth 2.0 — it's the standard for a reason. And run security audits regularly. Don't wait for something to break.

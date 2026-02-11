---
name: knowledge-base
description: "Personal knowledge base — save, search, and organize notes, ideas, and reference material as markdown files. Trigger on: 'save note', 'remember this', 'knowledge base', 'my notes', 'what do I know about'."
metadata: { "openclaw": { "emoji": "📚", "requires": { "bins": ["grep"] } } }
---

# Personal Knowledge Base

File-based knowledge system using markdown files in `~/.openclaw/knowledge/`.

## When to use

Use this skill when the user wants to:

- Save a note, idea, or piece of information for later
- Search their saved knowledge
- List notes by topic/category
- Recall something they previously saved
- Organize their personal knowledge

## Storage structure

```
~/.openclaw/knowledge/
├── general/          # Default category
├── research/         # Research findings
├── people/           # Notes about people
├── projects/         # Project-related notes
├── ideas/            # Ideas and brainstorms
├── reference/        # Reference material
└── daily/            # Daily notes / journal
```

## Commands

### Save a note

```bash
# Create category dir if needed, then write the note
mkdir -p ~/.openclaw/knowledge/{category}
cat > ~/.openclaw/knowledge/{category}/{slug}.md << 'EOF'
# {Title}

**Date:** {YYYY-MM-DD}
**Tags:** {tag1, tag2}

{Content}
EOF
```

- Generate a slug from the title (lowercase, hyphens, no special chars).
- Pick the most appropriate category folder.
- Always include date and relevant tags at the top.

### Search knowledge

```bash
# Full-text search across all notes
grep -ril "{query}" ~/.openclaw/knowledge/

# Search with context (shows matching lines)
grep -rin --include="*.md" "{query}" ~/.openclaw/knowledge/

# Search by tag
grep -ril "Tags:.*{tag}" ~/.openclaw/knowledge/

# Search by date range
find ~/.openclaw/knowledge/ -name "*.md" -newer /tmp/date_marker -exec grep -l "{query}" {} \;
```

### List notes

```bash
# List all notes in a category
ls -lt ~/.openclaw/knowledge/{category}/

# List recent notes (last 7 days)
find ~/.openclaw/knowledge/ -name "*.md" -mtime -7 -exec ls -lt {} \;

# Count notes per category
for d in ~/.openclaw/knowledge/*/; do echo "$(basename $d): $(find "$d" -name '*.md' | wc -l)"; done
```

### Read a note

```bash
cat ~/.openclaw/knowledge/{category}/{slug}.md
```

### Delete a note

```bash
rm ~/.openclaw/knowledge/{category}/{slug}.md
```

## Tips

- When the user says "remember this" or "save this for later", create a note in the most relevant category.
- Use descriptive filenames: `meeting-with-ahmed-2026-02-11.md` not `note1.md`.
- When searching, read the full content of matching files and summarize relevant parts.
- If the user asks "what do I know about X?", search and synthesize across multiple notes.
- Always confirm what was saved: "Saved to knowledge-base/research/topic-name.md".

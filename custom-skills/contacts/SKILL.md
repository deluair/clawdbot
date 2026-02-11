---
name: contacts
description: "Personal CRM — add, search, update, and tag contacts in a local SQLite database. Trigger on: 'save contact', 'find contact', 'who is', 'contact list', 'add person'."
metadata: { "openclaw": { "emoji": "📇", "requires": { "bins": ["python3"] } } }
---

# Personal Contacts CRM

Lightweight contact manager backed by SQLite at `~/.openclaw/contacts.db`.

## When to use

Use this skill when the user wants to:

- Save, add, or update a contact
- Search for a person by name, company, role, or notes
- List contacts by tag or category
- Delete a contact
- Import/export contacts as CSV

## Commands

### Add a contact

```bash
python3 {baseDir}/scripts/contacts.py add --name "John Doe" --phone "+1234567890" --email "john@example.com" --company "Acme Corp" --role "Developer" --tags "tech,friend" --notes "Met at conference 2026"
```

All fields except `--name` are optional.

### Search contacts

```bash
# Search across all fields (name, company, role, notes, tags)
python3 {baseDir}/scripts/contacts.py search "google"

# Search by specific field
python3 {baseDir}/scripts/contacts.py search --field company "Google"
python3 {baseDir}/scripts/contacts.py search --field tags "client"
```

### List all contacts

```bash
python3 {baseDir}/scripts/contacts.py list
python3 {baseDir}/scripts/contacts.py list --tag "client"
python3 {baseDir}/scripts/contacts.py list --limit 20
```

### Update a contact

```bash
python3 {baseDir}/scripts/contacts.py update --id 5 --phone "+9876543210" --notes "Changed phone number"
```

### Delete a contact

```bash
python3 {baseDir}/scripts/contacts.py delete --id 5
```

### Export / Import

```bash
python3 {baseDir}/scripts/contacts.py export --format csv > ~/contacts.csv
python3 {baseDir}/scripts/contacts.py import --file ~/contacts.csv
```

## Output format

- Default: human-readable table
- Add `--json` for machine-readable output

## Tips

- When the user says "save this contact" with details inline, parse name/phone/email/company from the message.
- When searching, try the broadest query first. If too many results, narrow by field.
- Tags are comma-separated. Use them for grouping (e.g., "client", "friend", "vendor", "family").

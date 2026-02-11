#!/usr/bin/env python3
"""Personal contacts CRM backed by SQLite."""
import argparse, json, os, sqlite3, sys, csv, io
from datetime import datetime

DB = os.path.expanduser("~/.openclaw/contacts.db")

def get_db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT DEFAULT '',
        email TEXT DEFAULT '',
        company TEXT DEFAULT '',
        role TEXT DEFAULT '',
        tags TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        created TEXT DEFAULT (datetime('now')),
        updated TEXT DEFAULT (datetime('now'))
    )""")
    conn.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS contacts_fts
        USING fts5(name, phone, email, company, role, tags, notes, content=contacts, content_rowid=id)""")
    conn.commit()
    return conn

def rebuild_fts(conn):
    conn.execute("INSERT INTO contacts_fts(contacts_fts) VALUES('rebuild')")
    conn.commit()

def add(args):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO contacts (name, phone, email, company, role, tags, notes) VALUES (?,?,?,?,?,?,?)",
        (args.name, args.phone or '', args.email or '', args.company or '',
         args.role or '', args.tags or '', args.notes or ''))
    conn.commit()
    rebuild_fts(conn)
    cid = cur.lastrowid
    if args.json:
        print(json.dumps({"id": cid, "status": "added", "name": args.name}))
    else:
        print(f"✅ Contact added (ID: {cid}): {args.name}")

def search(args):
    conn = get_db()
    query = args.query
    if args.field:
        rows = conn.execute(f"SELECT * FROM contacts WHERE {args.field} LIKE ? ORDER BY name",
                            (f"%{query}%",)).fetchall()
    else:
        try:
            rows = conn.execute(
                "SELECT c.* FROM contacts c JOIN contacts_fts f ON c.id = f.rowid WHERE contacts_fts MATCH ? ORDER BY rank",
                (query,)).fetchall()
        except sqlite3.OperationalError:
            rows = conn.execute(
                "SELECT * FROM contacts WHERE name LIKE ? OR company LIKE ? OR role LIKE ? OR tags LIKE ? OR notes LIKE ? OR email LIKE ? OR phone LIKE ? ORDER BY name",
                tuple(f"%{query}%" for _ in range(7))).fetchall()
    print_rows(rows, args.json)

def list_contacts(args):
    conn = get_db()
    q = "SELECT * FROM contacts"
    params = []
    if args.tag:
        q += " WHERE tags LIKE ?"
        params.append(f"%{args.tag}%")
    q += " ORDER BY name"
    if args.limit:
        q += " LIMIT ?"
        params.append(args.limit)
    rows = conn.execute(q, params).fetchall()
    print_rows(rows, args.json)

def update(args):
    conn = get_db()
    fields, vals = [], []
    for f in ('name','phone','email','company','role','tags','notes'):
        v = getattr(args, f, None)
        if v is not None:
            fields.append(f"{f}=?")
            vals.append(v)
    if not fields:
        print("Nothing to update."); return
    fields.append("updated=datetime('now')")
    vals.append(args.id)
    conn.execute(f"UPDATE contacts SET {','.join(fields)} WHERE id=?", vals)
    conn.commit()
    rebuild_fts(conn)
    if args.json:
        print(json.dumps({"id": args.id, "status": "updated"}))
    else:
        print(f"✅ Contact {args.id} updated.")

def delete(args):
    conn = get_db()
    conn.execute("DELETE FROM contacts WHERE id=?", (args.id,))
    conn.commit()
    rebuild_fts(conn)
    if args.json:
        print(json.dumps({"id": args.id, "status": "deleted"}))
    else:
        print(f"🗑️ Contact {args.id} deleted.")

def export_contacts(args):
    conn = get_db()
    rows = conn.execute("SELECT * FROM contacts ORDER BY name").fetchall()
    if args.format == 'csv':
        w = csv.writer(sys.stdout)
        w.writerow([k for k in rows[0].keys()] if rows else [])
        for r in rows: w.writerow(list(r))
    else:
        print(json.dumps([dict(r) for r in rows], indent=2))

def import_contacts(args):
    conn = get_db()
    count = 0
    with open(args.file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            conn.execute(
                "INSERT INTO contacts (name,phone,email,company,role,tags,notes) VALUES (?,?,?,?,?,?,?)",
                (row.get('name',''), row.get('phone',''), row.get('email',''),
                 row.get('company',''), row.get('role',''), row.get('tags',''), row.get('notes','')))
            count += 1
    conn.commit()
    rebuild_fts(conn)
    print(f"✅ Imported {count} contacts.")

def print_rows(rows, as_json=False):
    if not rows:
        print("No contacts found."); return
    if as_json:
        print(json.dumps([dict(r) for r in rows], indent=2))
    else:
        for r in rows:
            tags = f" [{r['tags']}]" if r['tags'] else ""
            company = f" @ {r['company']}" if r['company'] else ""
            role = f" ({r['role']})" if r['role'] else ""
            print(f"  #{r['id']} {r['name']}{role}{company}{tags}")
            if r['phone']: print(f"     📱 {r['phone']}")
            if r['email']: print(f"     ✉️  {r['email']}")
            if r['notes']: print(f"     📝 {r['notes']}")
            print()

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Personal Contacts CRM")
    p.add_argument("--json", action="store_true", help="JSON output")
    sub = p.add_subparsers(dest="cmd")

    a = sub.add_parser("add")
    a.add_argument("--name", required=True)
    for f in ('phone','email','company','role','tags','notes'):
        a.add_argument(f"--{f}")

    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--field", choices=['name','company','role','tags','notes','email','phone'])

    l = sub.add_parser("list")
    l.add_argument("--tag")
    l.add_argument("--limit", type=int)

    u = sub.add_parser("update")
    u.add_argument("--id", required=True, type=int)
    for f in ('name','phone','email','company','role','tags','notes'):
        u.add_argument(f"--{f}")

    d = sub.add_parser("delete")
    d.add_argument("--id", required=True, type=int)

    e = sub.add_parser("export")
    e.add_argument("--format", choices=['csv','json'], default='csv')

    i = sub.add_parser("import")
    i.add_argument("--file", required=True)

    args = p.parse_args()
    if not args.cmd:
        p.print_help(); sys.exit(1)

    {"add": add, "search": search, "list": list_contacts, "update": update,
     "delete": delete, "export": export_contacts, "import": import_contacts}[args.cmd](args)

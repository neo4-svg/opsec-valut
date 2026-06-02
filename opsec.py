#!/usr/bin/env python3
"""
opsec.py
Identity Splitter — manage multiple personas for OPSEC.
Pure Python3, no external dependencies.
"""

import argparse
import json
import os
from pathlib import Path

DATA_FILE = Path.home() / ".opsec_personas.json"

def load_personas():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_personas(personas):
    with open(DATA_FILE, "w") as f:
        json.dump(personas, f, indent=2)

def add_persona(name, email, notes=""):
    personas = load_personas()
    if name in personas:
        print(f"[!] Persona '{name}' already exists.")
        return
    personas[name] = {"email": email, "notes": notes}
    save_personas(personas)
    print(f"[+] Added persona '{name}'.")

def list_personas():
    personas = load_personas()
    if not personas:
        print("[!] No personas stored.")
        return
    for name, data in personas.items():
        print(f"- {name} ({data['email']}) :: {data.get('notes','')}")

def export_persona(name, fmt="json"):
    personas = load_personas()
    if name not in personas:
        print(f"[!] Persona '{name}' not found.")
        return
    data = personas[name]
    if fmt == "json":
        print(json.dumps({name: data}, indent=2))
    elif fmt == "env":
        print(f"PERSONA_NAME={name}")
        print(f"PERSONA_EMAIL={data['email']}")
        print(f"PERSONA_NOTES={data.get('notes','')}")
    else:
        print(f"[!] Unsupported format: {fmt}")

def delete_persona(name):
    personas = load_personas()
    if name not in personas:
        print(f"[!] Persona '{name}' not found.")
        return
    del personas[name]
    save_personas(personas)
    print(f"[-] Deleted persona '{name}'.")

def main():
    parser = argparse.ArgumentParser(description="Identity Splitter — OPSEC persona manager")
    sub = parser.add_subparsers(dest="command")

    add_cmd = sub.add_parser("add", help="Add a new persona")
    add_cmd.add_argument("--name", required=True)
    add_cmd.add_argument("--email", required=True)
    add_cmd.add_argument("--notes", default="")

    sub.add_parser("list", help="List all personas")

    export_cmd = sub.add_parser("export", help="Export persona")
    export_cmd.add_argument("--name", required=True)
    export_cmd.add_argument("--format", choices=["json","env"], default="json")

    del_cmd = sub.add_parser("delete", help="Delete persona")
    del_cmd.add_argument("--name", required=True)

    args = parser.parse_args()

    if args.command == "add":
        add_persona(args.name, args.email, args.notes)
    elif args.command == "list":
        list_personas()
    elif args.command == "export":
        export_persona(args.name, args.format)
    elif args.command == "delete":
        delete_persona(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

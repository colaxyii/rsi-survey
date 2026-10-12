#!/usr/bin/env python3
"""Scan installed Codex skills and dump name/description/path as JSON."""
import json
import os
import re

HOME = os.path.expanduser("~")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills.json")

ROOTS = [
    ("user", os.path.join(HOME, ".codex", "skills")),
    ("plugin", os.path.join(HOME, ".codex", "plugins", "cache")),
]


def read_frontmatter(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    block = m.group(1)
    meta = {}
    # simple key: value parser that tolerates folded blocks and quoted strings
    for km in re.finditer(
        r"^([A-Za-z_][\w-]*):[ \t]*(.*?)(?=^[A-Za-z_][\w-]*:[ \t]|\Z)", block + "\n", re.S | re.M
    ):
        key, val = km.group(1), km.group(2)
        val = val.strip()
        if val.startswith((">", "|")):
            val = "\n".join(
                line.strip() for line in val.splitlines()[1:] if line.strip() and line.strip() != "-"
            )
        val = val.strip().strip('"').strip("'")
        meta[key] = re.sub(r"\s+", " ", val).strip()
    return meta


def main():
    out = []
    for kind, root in ROOTS:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
            if "SKILL.md" not in filenames:
                continue
            rel = os.path.relpath(dirpath, root)
            meta = read_frontmatter(os.path.join(dirpath, "SKILL.md"))
            out.append(
                {
                    "kind": kind,
                    "rel": rel,
                    "dir": dirpath,
                    "name": meta.get("name") or os.path.basename(dirpath),
                    "description": meta.get("description", ""),
                }
            )
    out.sort(key=lambda r: (r["kind"], r["dir"]))
    json.dump(out, open(os.path.normpath(OUT), "w"), ensure_ascii=False, indent=1)
    print("total", len(out))
    for r in out:
        desc = r["description"][:80].replace("\n", " ")
        print(f'{r["kind"]:6s} | {r["name"][:38]:38s} | {desc}')


if __name__ == "__main__":
    main()

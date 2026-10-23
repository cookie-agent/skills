#!/usr/bin/env python3
"""Rewrites index.json's file hashes from the skills on disk.

Each `<name>/` with a SKILL.md is listed with every file below it. A skill
already in the index keeps its version and requires_cookie; a new one starts
at version 1.0.0 and must have its requires_cookie set by hand. Bump a
skill's version whenever its files change.
"""
import hashlib
import json
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(root, "index.json")
index = json.load(open(path))
known = {skill["name"]: skill for skill in index.get("skills", [])}
skills = []
for name in sorted(os.listdir(root)):
    directory = os.path.join(root, name)
    if name.startswith(".") or not os.path.isfile(os.path.join(directory, "SKILL.md")):
        continue
    files = []
    for parent, _, names in sorted(os.walk(directory)):
        for file in sorted(names):
            full = os.path.join(parent, file)
            relative = os.path.relpath(full, directory).replace(os.sep, "/")
            files.append({"path": relative, "sha256": hashlib.sha256(open(full, "rb").read()).hexdigest()})
    entry = known.get(name, {"name": name, "version": "1.0.0", "requires_cookie": ""})
    if not entry["requires_cookie"]:
        print(f"{name}: set requires_cookie in index.json", file=sys.stderr)
    skills.append({"name": name, "version": entry["version"], "requires_cookie": entry["requires_cookie"], "files": files})
with open(path, "w") as out:
    json.dump({"version": 1, "skills": skills}, out, indent=2)
    out.write("\n")

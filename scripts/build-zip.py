#!/usr/bin/env python3
"""Build dist/huddle.zip for upload to Claude (Settings > Capabilities > Skills).

Zip layout: huddle/SKILL.md and huddle/templates/page.md, with the folder name
matching the `name:` in SKILL.md. README and scripts are not packaged.
Run from anywhere: python3 scripts/build-zip.py
"""
import re, sys, zipfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
skill = (root / "SKILL.md").read_text()

m = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n---\n", skill, re.S)
if not m:
    sys.exit("SKILL.md frontmatter must start with name: and description:")
name, desc = m.group(1), m.group(2)
if len(name) > 64 or len(desc) > 1024:
    sys.exit(f"name/description too long: {len(name)}/{len(desc)}")

files = ["SKILL.md", "templates/page.md"]
out = root / "dist" / f"{name}.zip"
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(root / f, f"{name}/{f}")
print(f"built {out} ({out.stat().st_size} bytes); description {len(desc)} chars")
with zipfile.ZipFile(out) as z:
    for n in z.namelist():
        print(" ", n)

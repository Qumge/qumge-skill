#!/usr/bin/env python3
"""Check shipped skill entry points and local resource integrity without network access."""
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
metadata = json.loads((root / "marketplace.json").read_text())
entries = metadata["skills"]
assert {entry["name"] for entry in entries} == {"qumge", "qumge-publish"}
for entry in entries:
    skill = root / entry["path"]
    text = skill.read_text()
    assert text.startswith("---\n") and text.count("\n---") >= 1, skill
    frontmatter = text.split("---", 2)[1]
    name = re.search(r"^name: ([a-z0-9-]+)$", frontmatter, re.M)
    assert name and name[1] == entry["name"], skill
    assert re.search(r"^description: \S", frontmatter, re.M), skill
    for relative in re.findall(r"\]\(([^)]+)\)", text):
        if "://" not in relative and not relative.startswith("#"):
            target = (skill.parent / relative.split("#", 1)[0]).resolve()
            assert target.is_relative_to(skill.parent.resolve()), (skill, relative)
            assert target.is_file(), (skill, relative)
canonical = root / "skills/qumge-publish/references/qumge.example.json"
assert canonical.read_bytes() == (root / "references/qumge.example.json").read_bytes()
example = json.loads(canonical.read_text())
assert example["qumge"] == "2"
result = subprocess.run([sys.executable, str(root / "skills/qumge-publish/scripts/preflight.py"), str(canonical)], capture_output=True, text=True)
report = json.loads(result.stdout)
assert result.returncode == 1 and report["findings"], "Example URLs must not look deployed"
assert {finding["code"] for finding in report["findings"]} == {"https_url"}, report
for resource in ("scripts/preflight.py", "references/platform-access.md", "references/adaptation.md", "references/resume.md", "agents/openai.yaml"):
    assert (root / "skills/qumge-publish" / resource).is_file(), resource
print("OK: consumer and publisher entries, self-contained resources and compatible managed-v2 examples")

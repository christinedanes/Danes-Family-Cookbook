from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
START = "<!-- RECIPES-START -->"
END = "<!-- RECIPES-END -->"


def title_of(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


sections = []
folders = sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith("."))
for folder in folders:
    recipes = sorted(folder.glob("*.md"), key=lambda p: title_of(p).lower())
    if not recipes:
        continue
    lines = ["## " + folder.name.replace("-", " ").title()]
    for recipe in recipes:
        link = quote(f"{folder.name}/{recipe.name}")
        lines.append(f"- [{title_of(recipe)}]({link})")
    sections.append("\n".join(lines))

text = README.read_text(encoding="utf-8")
if START not in text or END not in text:
    raise SystemExit("README is missing the RECIPES-START / RECIPES-END markers")

before, rest = text.split(START, 1)
_, after = rest.split(END, 1)
new_text = f"{before}{START}\n" + "\n\n".join(sections) + f"\n{END}{after}"

if new_text != text:
    README.write_text(new_text, encoding="utf-8")
    print("Table of contents updated")
else:
    print("Table of contents already up to date")

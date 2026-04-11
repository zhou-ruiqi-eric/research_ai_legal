#!/usr/bin/env python3
import re

# Read files
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

with open("TREE.md", "r", encoding="utf-8") as f:
    tree_lines = f.read().strip().splitlines()

# Color function (HTML spans)
def color_name(name: str, prefix: str) -> str:
    name = name.strip()
    if not name:
        return name

    if "Knowledge_Base" in name:
        return f'<span style="color:#2ecc71">{name}</span>'      # green
    if "Individual" in name:
        return f'<span style="color:#9b59b6">{name}</span>'      # violet
    if name.startswith("AI-"):
        return f'<span style="color:#1abc9c">{name}</span>'      # teal
    if any(sym in prefix for sym in ["├──", "└──", "│   ", "│   "]) and len(prefix.strip()) > 0:
        return f'<span style="color:#f39c12">{name}</span>'      # orange
    if any(sym in prefix for sym in ["│   │", "│   │"]) or len(prefix) > 8:
        return f'<span style="color:#3498db">{name}</span>'      # blue
    return name

# Process tree lines
processed_tree = []
for line in tree_lines:
    line = re.sub(r'\.md$', '', line)
    match = re.match(r'([├└│─\s]+)(.+)', line)
    if match:
        prefix = match.group(1)
        name = match.group(2).strip()
        line = prefix + color_name(name, prefix)
    processed_tree.append(line)

tree_colored = "\n".join(processed_tree)

# New block with standalone <pre> (colors now render correctly)
new_block = """### 🌳 AI & Legal Knowledge Map

**This is not** the literal output of the `tree` command.  
It is a **curated visual knowledge map** designed to organize the AI industry, legal-tech research, and people.

**Color Legend & Structure (3 Types of Folders):**
- <span style="color:#9b59b6">👤 Individual</span> → Real people names & profiles  
- <span style="color:#2ecc71">📚 Knowledge_Base</span> → Concepts, standards, certificates, frameworks (used as [[wiki links]])  
- <span style="color:#1abc9c">🤖 AI Industry</span>:
  - Top level (teal): Major domains (AI-Legal, AI-Medicine…)  
  - Second level (orange): Sub-segments (GRC, RegTech…)  
  - Third level (blue): Specific companies or websites

<pre style="font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; white-space: pre; line-height: 1.4; overflow-x: auto; background-color: #0d1117; padding: 16px; border-radius: 8px; color: #c9d1d9;">
""" + tree_colored + """
</pre>"""

# Safe replacement
def replace_tree(match):
    return "<!-- AUTO-TREE-START -->\n" + new_block + "\n<!-- AUTO-TREE-END -->"

content = re.sub(
    r"<!-- AUTO-TREE-START -->.*?<!-- AUTO-TREE-END -->",
    replace_tree,
    content,
    flags=re.DOTALL
)

# Write back
with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ HTML-colored tree map (colors now visible) successfully updated in README.md")
#!/usr/bin/env python3
import re

# Read files
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

with open("TREE.md", "r", encoding="utf-8") as f:
    tree_lines = f.read().strip().splitlines()

# Color function — using string concatenation (no f-string issues)
def color_name(name: str, prefix: str) -> str:
    name = name.strip()
    if not name:
        return name

    if "Knowledge_Base" in name:
        return "$${\\color{green}{" + name + "}}$$"
    
    if "Individual" in name:
        return "$${\\color{violet}{" + name + "}}$$"
    
    if name.startswith("AI-"):
        return "$${\\color{teal}{" + name + "}}$$"
    
    # Sub-segments (GRC, RegTech...)
    if any(sym in prefix for sym in ["├──", "└──", "│   ", "│   "]) and len(prefix.strip()) > 0:
        return "$${\\color{orange}{" + name + "}}$$"
    
    # Companies / third level
    if any(sym in prefix for sym in ["│   │", "│   │"]) or len(prefix) > 8:
        return "$${\\color{blue}{" + name + "}}$$"
    
    return name

# Process every tree line
processed_tree = []
for line in tree_lines:
    # Remove .md extension
    line = re.sub(r'\.md$', '', line)
    
    # Split tree prefix + name
    match = re.match(r'([├└│─\s]+)(.+)', line)
    if match:
        prefix = match.group(1)
        name = match.group(2).strip()
        line = prefix + color_name(name, prefix)
    processed_tree.append(line)

tree_colored = "\n".join(processed_tree)

# Final block (using your tested KaTeX syntax)
new_block = """### 🌳 AI & Legal Knowledge Map

**This is not** the literal output of the `tree` command.  
It is a **curated visual knowledge map** designed to organize the AI industry, legal-tech research, and people.

**Color Legend & Structure (3 Types of Folders):**
- $${\\color{violet}{👤 Individual}}$$ → Real people names & profiles  
- $${\\color{green}{📚 Knowledge_Base}}$$ → Concepts, standards, certificates, frameworks (used as [[wiki links]])  
- $${\\color{teal}{🤖 AI Industry}}$$:
  - Top level (teal): Major domains (AI-Legal, AI-Medicine…)  
  - Second level (orange): Sub-segments (GRC, RegTech…)  
  - Third level (blue): Specific companies or websites

""" + tree_colored

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

print("✅ KaTeX colored tree map successfully updated in README.md")
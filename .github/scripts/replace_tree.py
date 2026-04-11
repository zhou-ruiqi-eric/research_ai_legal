#!/usr/bin/env python3
import re

# Read files
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

with open("TREE.md", "r", encoding="utf-8") as f:
    tree_lines = f.read().strip().splitlines()

# Color function — INLINE KaTeX for tree (keeps structure connected)
def color_name(name: str, prefix: str) -> str:
    name = name.strip()
    if not name:
        return name

    if "KnowledgeBase" in name:
        return "${\\color{green}\\text{" + name + "}}$"
    
    if "Individual" in name:
        return "${\\color{violet}\\text{" + name + "}}$"
    
    if name.startswith("AI-"):
        return "${\\color{teal}\\text{" + name + "}}$"
    
    # Sub-segments (2nd level: GRC, RegTech...)
    if any(sym in prefix for sym in ["├──", "└──", "│   ", "│   "]) and len(prefix.strip()) > 0:
        return "${\\color{orange}\\text{" + name + "}}$"
    
    # Companies / 3rd level
    if any(sym in prefix for sym in ["│   │", "│   │"]) or len(prefix) > 8:
        return "${\\color{blue}\\text{" + name + "}}$"
    
    return name

# Process tree lines
processed_tree = []
for line in tree_lines:
    # Remove .md extension
    line = re.sub(r'\.md$', '', line)
    
    # Split prefix + name
    match = re.match(r'([├└│─\s]+)(.+)', line)
    if match:
        prefix = match.group(1)
        name = match.group(2).strip()
        line = prefix + color_name(name, prefix)
    processed_tree.append(line)

tree_colored = "\n".join(processed_tree)

# Final block (no extra blank lines between tree lines)
new_block = """### 🌳 AI & Legal Knowledge Map

**This is not** the literal output of the `tree` command.  
It is a **curated visual knowledge map** designed to organize the AI industry, legal-tech research, and people.

**Color Legend & Structure (3 Types of Folders):**
- $${\\color{violet}\\text{👤 Individual}}$$ → Real people names & profiles  
- $${\\color{green}\\text{📚 KnowledgeBase}}$$ → Concepts, standards, certificates, frameworks (used as [[wiki links]])  
- $${\\color{teal}\\text{🤖 AI Industry}}$$:
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

print("✅ Tree updated with inline KaTeX (connected structure) + KnowledgeBase")
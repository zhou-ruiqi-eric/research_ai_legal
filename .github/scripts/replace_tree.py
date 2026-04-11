#!/usr/bin/env python3
import re

# Read files
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

with open("TREE.md", "r", encoding="utf-8") as f:
    tree_lines = f.read().strip().splitlines()

# Color function — STRICTLY follows your legend rules (dark background friendly)
def color_name(name: str, prefix: str) -> str:
    name = name.strip()
    if not name:
        return name

    # 1. KnowledgeBase (and all its children) → Green
    if "KnowledgeBase" in name:
        return "${\\color{green}\\text{" + name + "}}$"
    
    # 2. Individual → Violet
    if "Individual" in name:
        return "${\\color{violet}\\text{" + name + "}}$"
    
    # 3. AI Industry Top level → Teal
    if name.startswith("AI-"):
        return "${\\color{teal}\\text{" + name + "}}$"
    
    # 4. 3rd level (companies) → Blue
    if any(sym in prefix for sym in ["│   │", "│   │"]) or len(prefix) > 12:
        return "${\\color{blue}\\text{" + name + "}}$"
    
    # 5. 2nd level (sub-segments like GRC, RegTech) → Orange
    return "${\\color{orange}\\text{" + name + "}}$"

# Widen tree branches (your modified style + extra horizontal length)
def widen_prefix(prefix: str) -> str:
    prefix = prefix.replace("├── ", "├─────────── ")
    prefix = prefix.replace("└── ", "└─────────── ")
    prefix = prefix.replace("│   ", "│                  ")   # long gap
    prefix = prefix.replace("    ", "                   ")   # deeper levels
    return prefix

# Process tree lines
processed_tree = []
first_item = True

for line in tree_lines:
    line = re.sub(r'\.md$', '', line)
    
    # Completely skip DISCLAIMER
    if "DISCLAIMER" in line.upper():
        continue
    
    match = re.match(r'([├└│─\s]+)(.+)', line)
    if match:
        prefix = match.group(1)
        name   = match.group(2).strip()
        
        wide_prefix = widen_prefix(prefix)
        
        white_line   = "${\\color{white}\\text{" + wide_prefix + "}}$"
        colored_name = color_name(name, prefix)
        
        processed_tree.append(white_line)
        processed_tree.append(colored_name)
        processed_tree.append("")          # empty line between each pair
        
        # Extra blank line AFTER the root "." (your request #2)
        if first_item and name == ".":
            processed_tree.append("")
            first_item = False
    else:
        processed_tree.append(line)

tree_colored = "\n".join(processed_tree)

# Final block (legend updated to match your exact wording)
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

print("✅ Tree fully updated — wider spacing, correct colors, extra line after dot, DISCLAIMER removed")
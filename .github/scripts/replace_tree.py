#!/usr/bin/env python3
import re

# Read files
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

with open("TREE.md", "r", encoding="utf-8") as f:
    tree_lines = f.read().strip().splitlines()

# Redesigned colors for DARK background (high contrast + easy to read)
def color_name(name: str, prefix: str) -> str:
    name = name.strip()
    if not name:
        return name

    if "KnowledgeBase" in name:
        return "${\\color{#2ecc71}\\text{" + name + "}}$"      # bright green
    
    if "Individual" in name:
        return "${\\color{#bb86fc}\\text{" + name + "}}$"      # bright violet (better on dark)
    
    if name.startswith("AI-"):
        return "${\\color{#00d4aa}\\text{" + name + "}}$"      # brighter teal
    
    # Sub-segments (2nd level: GRC, RegTech...)
    if any(sym in prefix for sym in ["├──", "└──", "│   ", "│   "]) and len(prefix.strip()) > 0:
        return "${\\color{#ff9500}\\text{" + name + "}}$"      # vivid orange
    
    # Companies / 3rd level
    if any(sym in prefix for sym in ["│   │", "│   │"]) or len(prefix) > 8:
        return "${\\color{#4da6ff}\\text{" + name + "}}$"      # bright blue
    
    return name

# Extend prefix to make the tree HORIZONTALLY LONGER (your desired width)
def extend_prefix(original_prefix: str) -> str:
    p = original_prefix
    
    # Top level
    p = p.replace("├──", "├───────    ")
    p = p.replace("└──", "└───────    ")
    
    # Second level
    p = p.replace("│   ├──", "│   ├──────── ")
    p = p.replace("│   └──", "│   └──────── ")
    
    # Third level
    p = p.replace("│   │   ├──", "│   │   ├──────── ")
    p = p.replace("│   │   └──", "│   │   └──────── ")
    
    # Fourth level (if any)
    p = p.replace("│   │   │   ├──", "│   │   │   ├──────── ")
    p = p.replace("│   │   │   └──", "│   │   │   └──────── ")
    
    return p

# Process every tree line → white symbols + colored name + BLANK LINE
processed_tree = []
for line in tree_lines:
    # Remove .md extension
    line = re.sub(r'\.md$', '', line)
    
    # Split prefix + name
    match = re.match(r'([├└│─\s]+)(.+)', line)
    if match:
        original_prefix = match.group(1)
        name = match.group(2).strip()
        
        # Make branches wider
        wide_prefix = extend_prefix(original_prefix)
        
        # Line 1: white tree symbols (soft white for dark background)
        white_prefix = "${\\color{#e0e0e0}\\text{" + wide_prefix + "}}$"
        
        # Line 2: colored name
        colored_name = color_name(name, original_prefix)
        
        processed_tree.append(white_prefix)
        processed_tree.append(colored_name)
        processed_tree.append("")        # empty line between each pair
    else:
        processed_tree.append(line)

tree_colored = "\n".join(processed_tree)

# Final block
new_block = """### 🌳 AI & Legal Knowledge Map

**This is not** the literal output of the `tree` command.  
It is a **curated visual knowledge map** designed to organize the AI industry, legal-tech research, and people.

**Color Legend & Structure (3 Types of Folders):**
- $${\\color{#bb86fc}\\text{👤 Individual}}$$ → Real people names & profiles  
- $${\\color{#2ecc71}\\text{📚 KnowledgeBase}}$$ → Concepts, standards, certificates, frameworks (used as [[wiki links]])  
- $${\\color{#00d4aa}\\text{🤖 AI Industry}}$$:
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

print("✅ Tree updated: wider branches + redesigned colors for dark background")
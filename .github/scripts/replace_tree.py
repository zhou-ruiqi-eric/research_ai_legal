#!/usr/bin/env python3
import re

# Read files
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

with open("TREE.md", "r", encoding="utf-8") as f:
    tree_lines = f.read().strip().splitlines()

# Color function — STRICTLY follows the picture legend (exact hex codes)
def color_name(name: str, prefix: str) -> str:
    name = name.strip()
    if not name:
        return name

    # 1. Individual (real people, names & profiles) → Purple / Violet Main: #C084FC
    if "Individual" in name:
        return "${\\color{#C084FC}\\text{" + name + "}}$"
    
    # 2. KnowledgeBase (concepts, standards, frameworks like GDPR, ISO, etc.) → Green Main: #4ADE80
    if "KnowledgeBase" in name:
        return "${\\color{#4ADE80}\\text{" + name + "}}$"
    
    # 3. AI Industry (domains, sub-segments, companies)
    # Top level / Main → Electric Cyan #00F5FF
    if name.startswith("AI-") or name == "AI Industry":
        return "${\\color{#00F5FF}\\text{" + name + "}}$"
    
    # Third level (companies) → #A5F3FC
    if any(sym in prefix for sym in ["│   │", "│   │"]) or len(prefix) > 12:
        return "${\\color{#A5F3FC}\\text{" + name + "}}$"
    
    # Second level (sub-segments) → #67E8F9
    return "${\\color{#67E8F9}\\text{" + name + "}}$"

# Widen tree branches (your modified style + extra horizontal length)
def widen_prefix(prefix: str) -> str:
    prefix = prefix.replace("├── ", "├─────────── ")
    prefix = prefix.replace("└── ", "└─────────── ")
    prefix = prefix.replace("│   ", "│\qquad\qquad\qquad\qquad")
    prefix = prefix.replace("    ", "\qquad\qquad\qquad\qquad")   # deeper levels
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
        
        # Extra blank line AFTER the root "." 
        if first_item and name == ".":
            processed_tree.append("")
            first_item = False
    else:
        processed_tree.append(line)
        if line.strip() == ".":
            processed_tree.append("")

tree_colored = "\n".join(processed_tree)

# Final block — legend updated to match the picture exactly
new_block = """### 🌳 AI & Legal Knowledge Map

**This is not** the literal output of the `tree` command.  
It is a **curated visual knowledge map** designed to organize the AI industry, legal-tech research, and people.

**Color Legend & Structure (3 Types of Folders):**
- $${\\color{#C084FC}\\text{👤 Individual}}$$ → Real people names & profiles (Purple / Violet — Main: #C084FC)  
- $${\\color{#4ADE80}\\text{📚 KnowledgeBase}}$$ → Concepts, standards, frameworks (GDPR, ISO, etc.) (Green — Main: #4ADE80)  
- $${\\color{#00F5FF}\\text{🤖 AI Industry}}$$ (Electric Cyan as chosen):
  - Top level / Main (#00F5FF): Major domains  
  - Second level (#67E8F9): Sub-segments  
  - Third level (#A5F3FC): Specific companies or websites

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

print("✅ Tree fully updated — colors now exactly match the picture legend (#C084FC, #4ADE80, #00F5FF, #67E8F9, #A5F3FC)")
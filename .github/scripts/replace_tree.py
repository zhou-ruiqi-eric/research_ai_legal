#!/usr/bin/env python3
import re

# Read files
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

with open("TREE.md", "r", encoding="utf-8") as f:
    tree_lines = f.read().strip().splitlines()

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
        
        white_line = "${\\color{white}\\text{" + wide_prefix + "}}$"
        white_name = "${\\color{white}\\text{" + name + "}}$"

        processed_tree.append(white_line)
        processed_tree.append(white_name)
        processed_tree.append("")          # empty line between each pair
        
        # Extra blank line AFTER the root "." 
        if first_item and name == ".":
            processed_tree.append("")
            first_item = False
    else:
        processed_tree.append(line)
        if line.strip() == ".":
            processed_tree.append("")

tree_output = "\n".join(processed_tree)

# Safe replacement
def replace_tree(match):
    return "<!-- AUTO-TREE-START -->\n" + tree_output + "\n<!-- AUTO-TREE-END -->"

content = re.sub(
    r"<!-- AUTO-TREE-START -->.*?<!-- AUTO-TREE-END -->",
    replace_tree,
    content,
    flags=re.DOTALL
)

# Write back
with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Tree fully updated — all tree labels use white (no category color rules)")
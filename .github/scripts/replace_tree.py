#!/usr/bin/env python3
import re
from urllib.parse import quote

# Configuration
REPO_URL_BASE = "https://github.com/zhou-ruiqi-eric/research_ai_legal/blob/master/"

# Read files
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

with open("TREE.md", "r", encoding="utf-8") as f:
    tree_lines = f.read().strip().splitlines()

# Widen tree branches (exactly your original style)
def widen_prefix(prefix: str) -> str:
    prefix = prefix.replace("├── ", "├─────────── ")
    prefix = prefix.replace("└── ", "└─────────── ")
    prefix = prefix.replace("│   ", "│\\qquad\\qquad\\qquad\\qquad")
    prefix = prefix.replace("    ", "\\qquad\\qquad\\qquad\\qquad")   # deeper levels
    return prefix

# Process tree lines with path tracking + leaf detection
processed_tree = []
path_stack = []
first_item = True

for line in tree_lines:
    if not line.strip():
        processed_tree.append("")
        continue
    
    # Completely skip DISCLAIMER
    if "DISCLAIMER" in line.upper():
        continue
    
    match = re.match(r'([├└│─\s]+)(.+)', line)
    if match:
        prefix = match.group(1)
        name_full = match.group(2).strip()
        
        # Detect leaf (original line ends with .md)
        is_leaf = name_full.endswith('.md')
        display_name = re.sub(r'\.md$', '', name_full)
        
        # Calculate depth (standard tree output = 4 chars per level)
        depth = len(prefix) // 4
        
        # Maintain folder path stack (only folders are pushed)
        while len(path_stack) >= depth:
            path_stack.pop()
        
        # Build relative folder path for this item
        relative_path = "/".join(path_stack)
        if relative_path:
            relative_path += "/"
        
        # Widen prefix for visual spacing (your original look)
        wide_prefix = widen_prefix(prefix)
        white_line = f"$\\color{{white}}{{\\text{{{wide_prefix}}}}}$"
        
        # Build name part
        if is_leaf:
            # IMPORTANT FIX: URL-encode the filename (spaces → %20)
            encoded_filename = quote(name_full)
            github_url = f"{REPO_URL_BASE}{relative_path}{encoded_filename}"
            
            # Leaf → clickable GitHub link (white text stays white)
            name_display = f'[<span style="color:white">{display_name}</span>]({github_url})'
        else:
            # Folder/category → keep your original white LaTeX style
            name_display = f"$\\color{{white}}{{\\text{{{display_name}}}}}$"
            # Push folder to stack for its children
            path_stack.append(display_name)
        
        processed_tree.append(white_line)
        processed_tree.append(name_display)
        processed_tree.append("")  # empty line between each pair
        
        # Extra blank line AFTER the root "."
        if first_item and display_name == ".":
            processed_tree.append("")
            first_item = False
    else:
        # Fallback for any non-tree lines
        processed_tree.append(line)
        if line.strip() == ".":
            processed_tree.append("")

tree_output = "\n".join(processed_tree)

# Safe replacement in README.md
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

print("✅ Tree fully updated — spaces in filenames (ISO 27001.md, PCI DSS.md, etc.) are now properly encoded as %20!")

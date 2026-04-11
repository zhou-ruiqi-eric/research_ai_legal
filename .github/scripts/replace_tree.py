#!/usr/bin/env python3
import re

# Read files
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

with open("TREE.md", "r", encoding="utf-8") as f:
    tree_lines = f.read().strip().splitlines()

# Function to color a name based on category + depth
def color_name(name: str, prefix: str) -> str:
    name = name.strip()
    if not name:
        return name
    
    # Knowledge_Base
    if "Knowledge_Base" in name:
        return f"$${{\\color{{green}}{{{name}}}}}"
    
    # Individual (people)
    if "Individual" in name:
        return f"$${{\\color{{violet}}{{{name}}}}}"
    
    # AI Industry top-level
    if name.startswith("AI-"):
        return f"$${{\\color{{teal}}{{{name}}}}}"
    
    # Sub-segments (level 2 inside AI)
    if ("│   " in prefix or "├──" in prefix) and not name.startswith("AI-"):
        return f"$${{\\color{{orange}}{{{name}}}}}"
    
    # Companies (level 3+)
    if "│   │" in prefix or "│   │" in prefix:
        return f"$${{\\color{{blue}}{{{name}}}}}"
    
    return name

# Process each tree line: strip .md + apply color to the name
processed_tree = []
for line in tree_lines:
    # Strip .md extension
    line = re.sub(r'\.md$', '', line)
    
    # Extract prefix + name using regex (tree symbols + name)
    match = re.search(r'([├└│─\s]+)(.+)', line)
    if match:
        prefix = match.group(1)
        name = match.group(2).strip()
        colored = color_name(name, prefix)
        line = prefix + colored
    processed_tree.append(line)

tree_colored = "\n".join(processed_tree)

# New block with explanation + colored tree (NO code block so colors render)
new_block = f"""### 🌳 AI & Legal Knowledge Map

**This is not** the literal output of the `tree` command.  
It is a **curated tree map** designed to organize knowledge in the AI industry, legal/tech research, and people.

**3 Types of folders:**
- **👤 Individual** (violet) → real people names & profiles
- **📚 Knowledge_Base** (green) → concepts, certificates, standards, frameworks (linked via [[wiki]] in other files)
- **🤖 AI Industry** (teal / orange / blue):
  - Top level (teal): major AI domains (AI-Legal, AI-Medicine…)
  - Second level (orange): smaller segments (GRC, RegTech…)
  - Third level (blue): specific companies or websites

---

{tree_colored}
"""

# Replace the old block
content = re.sub(
    r"<!-- AUTO-TREE-START -->.*?<!-- AUTO-TREE-END -->",
    f"<!-- AUTO-TREE-START -->\n{new_block}\n<!-- AUTO-TREE-END -->",
    content,
    flags=re.DOTALL
)

# Write back
with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Colored tree map + explanation successfully updated in README.md")
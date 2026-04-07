
#!/usr/bin/env python3
import re
import sys

# 读取 README.md 和 TREE.md
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

with open("TREE.md", "r", encoding="utf-8") as f:
    tree = f.read().strip()

# 新的 tree 区块
new_block = f"""<!-- AUTO-TREE-START -->
```bash
{tree}
```
<!-- AUTO-TREE-END -->"""

# 替换内容
content = re.sub(
    r"<!-- AUTO-TREE-START -->.*?<!-- AUTO-TREE-END -->",
    new_block,
    content,
    flags=re.DOTALL
)

# 写回 README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Tree successfully replaced in README.md")
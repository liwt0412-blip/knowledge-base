---
tags:
  - 冲突
  - 排错
created: 2026-06-06
---

# Obsidian 文件冲突及解决方案

## 1. 编码冲突：GBK vs UTF-8

**现象**：`.txt` 或 `.md` 文件在 Obsidian 中中文全乱码

**原因**：Windows 上创建的 `.txt` 文件默认 GBK 编码，而 Obsidian 只认 UTF-8

**解决**：
```bash
# 检查编码
od -A x -t x1z -v 文件名 | head -3
# 如果看到 ef bf bd 大量出现 → 文件已损坏，需找原始文件
# 如果看到 b4 d3 bf aa 等字节 → GBK 编码，可转换

# 转换
python -c "raw=open('文件','rb').read(); open('文件','w',encoding='utf-8').write(raw.decode('gbk'))"
```

## 2. 文件损坏：� 替换字符

**现象**：Hex 中大量 `ef bf bd`（Unicode 替换字符 U+FFFD）

**原因**：GBK 文件被错误地以 UTF-8 解析后重新保存，原始中文永久丢失

**解决**：找回原始 GBK 文件重新转码，已损坏文件无法恢复

## 3. 图片无法显示

**现象**：Obsidian 中 `!(path)` 语法的图片不渲染、不连线

**解决**：将 `![alt](path/image.png)` 改为 `![[path/image.png]]`

```python
import re
new = re.sub(r'!\[([^\]]*)\]\(([^)]*)\)', lambda m: f'![[{m.group(2)}]]', content)
```

## 4. 关系图谱孤岛

**现象**：文件在关系图谱中无连线、散落为孤点

**原因**：
- 文件之间没有 `[[wikilink]]` 互相链接
- 图片用了 `!(path)` 而非 `![[wikilink]]`

**解决**：创建 MOC（内容地图）笔记，用 `[[wikilink]]` 关联所有文件

## 5. MOC 死链

**现象**：MOC 中链接打不开，文件重命名/删除后未更新 MOC

**解决**：
```bash
# 查找含死链的 MOC
for f in *.md; do
  # 检查 MOC 中每个链接对应的文件是否存在
done
```

重命名文件后必须同步更新所有 MOC 中的链接。

## 相关笔记

- [[📋 技术速查/技术速查总览|📋 技术速查总览]]

- [[MOC-工具运维]]

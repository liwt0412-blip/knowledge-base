# AGENTS.md - 小帅的知识库

## 每次会话开始时

### 孤儿文件链接（由 scan-orphans hook 自动触发）
会话启动时若看到 `ORPHAN FILES DETECTED` 标记，说明有新文件缺少 wikilink。
对每个孤儿文件执行：

1. 读取完整内容，提取关键主题词
2. 用 Grep 在 vault 中搜索这些关键词，找到内容相关的笔记
3. 在孤儿文件中添加/更新 "## 相关笔记" 区域：
   - MOC 回溯链接（必须）
   - 语义相关的笔记链接（至少 1-2 个）
4. 在目标笔记中也添加双向链接（如果目标有相关笔记区域）
5. 全部链接完成后，将孤儿文件路径写入 `.Codex/hooks/vocab-queue.txt`
6. 写入后运行 `python ".Codex/hooks/extract-vocab.py"` 触发词汇提取

### 词汇提取（由 extract-vocab hook 自动触发）
会话启动时若看到 `VOCAB EXTRACTION REQUIRED` 标记，说明有新文件排队等待词汇提取。
按以下规则将候选词写入 `🔤 英语/英语词汇大全.md`：

1. 从候选词中去重（已存在于词汇大全中的跳过）
2. 对每个新词汇提供：IPA 音标、词根拆解、中文含义、来源文件（`[[原文件路径]]`）
3. 格式沿用英语词汇大全现有风格（表格格式，含拆解/含义项目）
4. 根据词汇所属领域放入对应主题区（AI区、Spring区、数据库区、Git区等）
5. 写入完成后清空 `.Codex/hooks/vocab-queue.txt`

### 文件处理
- 新增的 `.txt` 文件先转 GBK → UTF-8，再改 `.md` 扩展名
- 新增的 `.md` 文件检查编码，GBK 的转 UTF-8
- `!(path)` 图片语法转为 `![[path]]`

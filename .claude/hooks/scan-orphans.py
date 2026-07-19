"""轻量检测孤儿 Markdown，并按模块分批提示 Claude 处理。"""

import io
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

VAULT = r"D:\KnowledgeBase\小帅的知识库"
EXCLUDE = {".obsidian", ".git", ".claude", ".agents", ".trash"}
BATCH_SIZE = 10

# 按最长路径优先匹配，把候选笔记路由到当前有效的模块入口。
FOLDER_ENTRY_MAP = [
    ("💼 面试/本人面试准备", "💼 面试/00-面试模块入口.md"),
    ("💼 面试", "💼 面试/00-面试模块入口.md"),
    ("🖥 项目笔记/天机学堂", "🖥 项目笔记/天机学堂/00-天机学堂MOC.md"),
    ("🖥 项目笔记", "🖥 项目笔记/00-项目模块入口.md"),
    ("☕ Java笔记", "☕ Java笔记/00-Java开发与工程实践入口.md"),
    ("🤖 AI Agent", "🤖 AI Agent/00-上下文与记忆入口.md"),
    ("AI大模型开发基础", "AI大模型开发基础/AI大模型开发基础总览.md"),
    ("AI大模型开发", "AI大模型开发/AI大模型开发总览.md"),
    ("SpringAI+AIGC应用", "SpringAI+AIGC应用/SpringAI+AIGC应用总览.md"),
    ("python", "python/Python笔记总览.md"),
    ("常用指令", "常用指令/常用指令总览.md"),
    ("📋 技术速查", "📋 技术速查/技术速查总览.md"),
    ("📖 中州养老课程文档", "📖 中州养老课程文档/中州养老课程总览.md"),
    ("🎬 Remotion旁白文案", "🎬 Remotion旁白文案/00-Remotion旁白文案MOC.md"),
    ("📥 原始资料（待处理）", "📥 原始资料（待处理）/00-原始资料说明.md"),
    ("笔记文档", "笔记文档/笔记文档总览.md"),
    ("GEO项目", "00-知识库地图.md"),
    ("提示词", "MOC-日常学习.md"),
    ("🔤 英语", "MOC-日常学习.md"),
]

ENTRY_FILES = {
    "00-入口.md",
    "00-我的长期上下文.md",
    "00-当前主线.md",
    "00-知识库地图.md",
    "00-Agent启动提示词.md",
    "AGENTS.md",
    "CLAUDE.md",
    "☕ Java笔记/00-Java开发与工程实践入口.md",
    "💼 面试/00-面试模块入口.md",
    "🖥 项目笔记/00-项目模块入口.md",
    "🤖 AI Agent/00-上下文与记忆入口.md",
}


def send_notification(title, message):
    """发送桌面提示；失败不影响扫描结果。"""
    ps = f'''
Add-Type -AssemblyName System.Windows.Forms
$balloon = New-Object System.Windows.Forms.NotifyIcon
$balloon.Icon = [System.Drawing.SystemIcons]::Information
$balloon.BalloonTipTitle = "{title}"
$balloon.BalloonTipText = "{message}"
$balloon.Visible = $true
$balloon.ShowBalloonTip(5000)
Start-Sleep -Seconds 6
$balloon.Dispose()
'''
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            timeout=10,
            capture_output=True,
        )
    except Exception:
        pass


def find_files():
    """获取知识内容文件，排除工具配置与版本库目录。"""
    files = set()
    for root, dirs, filenames in os.walk(VAULT):
        dirs[:] = [directory for directory in dirs if directory not in EXCLUDE]
        for filename in filenames:
            if filename.endswith(".md"):
                path = os.path.join(root, filename)
                files.add(os.path.relpath(path, VAULT).replace("\\", "/"))
    return files


def extract_wikilinks(content):
    """忽略代码块后提取 Wikilink，避免把示例语法当成真实导航。"""
    content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    content = re.sub(r"`[^`\r\n]*`", "", content)
    return set(re.findall(r"\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]", content))


def is_exempt(filepath):
    """控制文件与历史归档允许不参与普通知识网络。"""
    if filepath in ENTRY_FILES:
        return True
    parts = filepath.split("/")
    return (
        "归档" in filepath
        or "记忆备份" in filepath
        or filepath.startswith("🤖 AI Agent/Hermes Agent技能库/")
        or "模板" in parts[-1]
        or parts[-1].upper() == "README.MD"
    )


def find_orphans():
    """查找既没有有效出链、也没有按文件名匹配入链的普通笔记。"""
    all_files = find_files()
    outgoing = {}
    incoming_names = set()

    for relative_path in all_files:
        path = os.path.join(VAULT, relative_path)
        try:
            with open(path, "r", encoding="utf-8") as file:
                targets = extract_wikilinks(file.read())
        except OSError:
            targets = set()
        outgoing[relative_path] = targets
        for target in targets:
            target_name = os.path.splitext(os.path.basename(target.rstrip("/")))[0]
            if target_name:
                incoming_names.add(target_name.lower())

    orphans = []
    for relative_path in sorted(all_files):
        if is_exempt(relative_path):
            continue
        filename = os.path.splitext(os.path.basename(relative_path))[0].lower()
        if not outgoing.get(relative_path) and filename not in incoming_names:
            orphans.append(relative_path)
    return orphans


def match_entry(filepath):
    """根据目录返回最具体的模块入口。"""
    for prefix, entry in FOLDER_ENTRY_MAP:
        if filepath == prefix or filepath.startswith(prefix + "/"):
            return entry
    return "00-入口.md"


def extract_title(filepath):
    """只读取到首个一级标题，不加载整篇正文。"""
    path = os.path.join(VAULT, filepath)
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                stripped = line.strip()
                if stripped.startswith("# "):
                    return stripped[2:].strip()
    except OSError:
        pass
    return "(no title)"


def build_prompt(orphans):
    """每次仅披露一个小批次，避免会话启动时污染上下文。"""
    batch = orphans[:BATCH_SIZE]
    lines = [
        "=" * 50,
        "ORPHAN FILES DETECTED",
        f"共 {len(orphans)} 个候选；本次仅展示前 {len(batch)} 个。",
        "先按当前任务选择需要处理的文件，不要一次性读取全部正文。",
        "=" * 50,
    ]

    for index, relative_path in enumerate(batch, 1):
        lines.append(f"[{index}] {relative_path}")
        lines.append(f"    Title: {extract_title(relative_path)}")
        lines.append(f"    Suggested entry: {match_entry(relative_path)}")

    if len(orphans) > len(batch):
        lines.append(f"其余 {len(orphans) - len(batch)} 个将在后续批次展示。")

    lines.extend(
        [
            "--- Instructions ---",
            "1. 优先处理当前任务所属模块；无关候选可留到后续会话。",
            "2. 选中某篇后再读取完整正文并核验归属。",
            "3. 补充模块入口和 1～2 个语义相关链接。",
            "4. 完成本批后再写入 .claude/hooks/vocab-queue.txt。",
            "=" * 50,
        ]
    )
    return "\n".join(lines)


def main():
    orphans = find_orphans()
    if not orphans:
        print("[scan-orphans] No orphan files found.")
        send_notification("知识库扫描完成", "无孤儿文件")
        return

    print(build_prompt(orphans))
    send_notification("发现孤儿文件", f"{len(orphans)} 个候选，已展示首批 {min(len(orphans), BATCH_SIZE)} 个")


if __name__ == "__main__":
    main()

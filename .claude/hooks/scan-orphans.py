"""Detect orphan .md files and prompt Claude for intelligent semantic linking."""
import os, re, sys, subprocess, io
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

VAULT = r'D:\KnowledgeBase\小帅的知识库'
EXCLUDE = {'.obsidian', '.git', '.claude', '.agents', '.trash'}

FOLDER_MOC_MAP = [
    ('SpringAI+AIGC应用', 'SpringAI+AIGC应用/SpringAI+AIGC应用总览.md'),
    ('中州养老阶段老师的总结/文档', '中州养老阶段老师的总结/中州养老课程总览.md'),
    ('中州养老阶段老师的总结', '中州养老阶段老师的总结/中州养老课程总览.md'),
    ('03.Java笔记已整理', 'MOC-Java基础.md'),
    ('python', 'MOC-日常学习.md'),
    ('常用指令/claude技能指令', 'MOC-工具运维.md'),
    ('常用指令/codex指令', 'MOC-工具运维.md'),
    ('常用指令', 'MOC-工具运维.md'),
    ('提示词', 'MOC-日常学习.md'),
    ('💼 面试/23种设计模式', '💼 面试/23种设计模式/README.md'),
    ('💼 面试', 'MOC-面试题.md'),
    ('🖥 项目笔记/CRM', 'MOC-项目实战.md'),
    ('🖥 项目笔记/中州养老', 'MOC-项目实战.md'),
    ('🖥 项目笔记', 'MOC-项目实战.md'),
    ('笔记文档/框架与老子', 'MOC-思想与灵感.md'),
    ('笔记文档/编程里的结构', 'MOC-思想与灵感.md'),
    ('笔记文档', 'MOC-思想与灵感.md'),
]

ROOT_MOC = '00-入口.md'

MOC_FILES = {
    '00-入口.md', 'MOC-面试题.md', 'MOC-编程相关.md', 'MOC-日常学习.md',
    'MOC-思想与灵感.md', 'MOC-Java基础.md', 'MOC-Spring框架.md',
    'MOC-数据库.md', 'MOC-工具运维.md', 'MOC-项目实战.md',
    '中州养老阶段老师的总结/中州养老课程总览.md',
    'SpringAI+AIGC应用/SpringAI+AIGC应用总览.md',
}

PREVIEW_LINES = 150


def send_notification(title, message):
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
            ['powershell', '-NoProfile', '-Command', ps],
            timeout=10, capture_output=True
        )
    except:
        pass


def find_files():
    files = set()
    for root, dirs, filenames in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for fn in filenames:
            if fn.endswith('.md'):
                rel = os.path.relpath(os.path.join(root, fn), VAULT).replace('\\', '/')
                files.add(rel)
    return files


def extract_wikilinks(content):
    return set(re.findall(r'\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]', content))


def find_orphans():
    all_files = find_files()
    outgoing = {}
    incoming = {}

    for rel in all_files:
        path = os.path.join(VAULT, rel)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        targets = extract_wikilinks(content)
        outgoing[rel] = targets
        for t in targets:
            incoming.setdefault(t, set()).add(rel)

    orphans = []
    for rel in sorted(all_files):
        if rel in MOC_FILES:
            continue
        has_out = bool(outgoing.get(rel))
        fname = os.path.splitext(os.path.basename(rel))[0]
        has_in = False
        for target, sources in incoming.items():
            target_fname = os.path.splitext(os.path.basename(target))[0]
            if target_fname == fname:
                has_in = True
                break
        if not has_out and not has_in:
            orphans.append(rel)
    return orphans


def match_moc(filepath):
    for prefix, moc in FOLDER_MOC_MAP:
        if filepath.startswith(prefix + '/') or filepath.startswith(prefix + '\\'):
            return moc
    if '/' not in filepath and '\\' not in filepath:
        return ROOT_MOC
    return None


def extract_title(filepath):
    """Extract the first # heading from a file."""
    path = os.path.join(VAULT, filepath)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# ') and not line.startswith('## '):
                    return line[2:].strip()
    except:
        pass
    return None


def read_preview(filepath):
    """Read first N lines of a file."""
    path = os.path.join(VAULT, filepath)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = []
            for i, line in enumerate(f):
                if i >= PREVIEW_LINES:
                    lines.append('... (truncated)')
                    break
                lines.append(line.rstrip('\n'))
            return '\n'.join(lines)
    except:
        return '(cannot read file)'


def build_prompt(orphans):
    lines = []
    lines.append('=' * 50)
    lines.append('ORPHAN FILES DETECTED')
    lines.append(f'{len(orphans)} file(s) need semantic linking:')
    lines.append('=' * 50)

    for idx, rel in enumerate(orphans, 1):
        title = extract_title(rel) or '(no title)'
        moc = match_moc(rel) or '(no match)'
        preview = read_preview(rel)

        lines.append(f'\n[{idx}] {rel}')
        lines.append(f'    Title: {title}')
        lines.append(f'    Suggested MOC: {moc}')
        lines.append(f'    --- Content preview (first {PREVIEW_LINES} lines) ---')
        lines.append(preview)
        lines.append('    --- End preview ---')

    lines.append('\n--- Instructions ---')
    lines.append('对每个孤儿文件执行语义链接：')
    lines.append('1. 读取完整内容，提取关键主题词')
    lines.append('2. 用 Grep 在 vault 中搜索这些关键词，找到内容相关的笔记')
    lines.append('3. 在孤儿文件中添加 "## 相关笔记" 区域，包含：')
    lines.append('   - MOC 回溯链接（必须）')
    lines.append('   - 语义相关的笔记链接（至少 1-2 个）')
    lines.append('4. 在目标笔记中也添加双向链接（如果目标有相关笔记区域）')
    lines.append('5. 全部链接完成后，将孤儿文件路径写入 .claude/hooks/vocab-queue.txt')
    lines.append('6. 写入后运行 `python extract-vocab.py` 触发词汇提取')
    lines.append('=' * 50)
    return '\n'.join(lines)


def main():
    orphans = find_orphans()
    if not orphans:
        print('[scan-orphans] No orphan files found.')
        send_notification('知识库扫描完成', '无孤儿文件')
        return

    print(build_prompt(orphans))
    send_notification(
        '发现孤儿文件',
        f'{len(orphans)} 个文件需要语义链接'
    )


if __name__ == '__main__':
    main()

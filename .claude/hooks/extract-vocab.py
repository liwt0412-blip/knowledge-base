"""Check vocab-queue.txt and output extraction prompt for Claude."""
import os, sys, re, io
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

VAULT = r'D:\KnowledgeBase\小帅的知识库'
QUEUE_FILE = os.path.join(VAULT, '.claude', 'hooks', 'vocab-queue.txt')
VOCAB_FILE = os.path.join(VAULT, r'🔤 英语\英语词汇大全.md')

STOP_WORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall',
    'should', 'may', 'might', 'must', 'can', 'could', 'i', 'you', 'he',
    'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my',
    'your', 'his', 'its', 'our', 'their', 'this', 'that', 'these', 'those',
    'and', 'but', 'or', 'not', 'no', 'yes', 'so', 'if', 'else', 'for',
    'while', 'do', 'in', 'on', 'at', 'to', 'of', 'by', 'from', 'with',
    'as', 'all', 'each', 'every', 'both', 'few', 'many', 'most', 'some',
    'any', 'one', 'two', 'first', 'then', 'now', 'here', 'there', 'just',
    'also', 'very', 'too', 'only', 'class', 'public', 'private', 'static',
    'void', 'int', 'string', 'return', 'new', 'null', 'true', 'false',
    'import', 'package', 'extends', 'implements', 'throws', 'try', 'catch',
    'final', 'abstract', 'default', 'super', 'this', 'interface', 'enum',
}


def read_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    return [l.strip() for l in lines if l.strip()]


def read_file_content(rel_path):
    full = os.path.join(VAULT, rel_path)
    if not os.path.exists(full):
        return None
    try:
        with open(full, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(full, 'r', encoding='gbk') as f:
                return f.read()
        except:
            return None


def extract_candidates(content):
    """Extract candidate English technical terms from content."""
    candidates = set()

    # 1. CamelCase (two+ uppercase letters in a word, like FilterChain, JwtUtils)
    for m in re.finditer(r'\b([A-Z][a-z]+){2,}\b', content):
        candidates.add(m.group())

    # 2. UPPER_CASE acronyms (2+ uppercase letters, like JWT, API, IOC, AMQP)
    for m in re.finditer(r'\b[A-Z]{2,}\b', content):
        word = m.group()
        if word not in STOP_WORDS:
            candidates.add(word)

    # 3. snake_case identifiers (like git_add, pre_handle)
    for m in re.finditer(r'\b[a-z]+_[a-z]+(?:_[a-z]+)*\b', content):
        candidates.add(m.group())

    # 4. Standalone English words (alphabetic, 4+ chars, not in stop words)
    #    Look for English words surrounded by Chinese or whitespace
    for m in re.finditer(r'(?<=[\s一-鿿])[a-zA-Z]{3,}(?=[\s一-鿿.,;:!?\)\]])', content):
        word = m.group().lower()
        if word not in STOP_WORDS and len(word) >= 3:
            candidates.add(word)

    # 5. English command-line tools / commands in backticks or code fences
    for m in re.finditer(r'`([a-zA-Z][a-zA-Z_ -]+)`', content):
        word = m.group(1).strip()
        if ' ' not in word and len(word) >= 3:
            w = word.lower()
            if w not in STOP_WORDS:
                candidates.add(word)

    return sorted(candidates, key=str.lower)


def build_prompt(files_info):
    lines = []
    lines.append('=' * 50)
    lines.append('VOCAB EXTRACTION REQUIRED')
    lines.append(f'{len(files_info)} file(s) in queue:')
    lines.append('=' * 50)

    for idx, (rel_path, content, candidates) in enumerate(files_info, 1):
        fname = os.path.basename(rel_path)
        lines.append(f'\n[{idx}] {rel_path}')
        lines.append(f'\n--- File content ({fname}) ---')
        # Limit content to 200 lines to avoid flooding
        content_lines = content.split('\n')
        if len(content_lines) > 200:
            content_lines = content_lines[:200]
            content_lines.append('... (truncated)')
        lines.append('\n'.join(content_lines))

        lines.append(f'\n--- Candidate terms ({len(candidates)}) ---')
        lines.append(', '.join(candidates))

    lines.append(f'\n--- Instructions ---')
    lines.append(f'1. 对候选词去重（检查 {VOCAB_FILE} 中已存在的词汇）')
    lines.append('2. 为每个新词汇补充：IPA 音标、词根拆解、中文含义')
    lines.append('3. 归类到正确的主题区（如 Git 区、Spring 区等）')
    lines.append(f'4. 来源文件：[[{files_info[0][0]}]]')
    lines.append('5. 格式沿用英语词汇大全现有风格（表格 + 拆解/含义项目）')
    lines.append(f'6. 写入完毕后清空 {QUEUE_FILE}')
    lines.append('=' * 50)
    return '\n'.join(lines)


def main():
    queued = read_queue()
    if not queued:
        return  # Silent - nothing to do

    files_info = []
    for rel_path in queued:
        content = read_file_content(rel_path)
        if content is None:
            print(f'[extract-vocab] WARNING: Cannot read {rel_path}', file=sys.stderr)
            continue
        candidates = extract_candidates(content)
        files_info.append((rel_path, content, candidates))

    if not files_info:
        return

    print(build_prompt(files_info))


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""简历精修：时间右对齐 + 项目分隔 + 标题与下段同页"""
import re
from docx import Document
from docx.shared import Twips, RGBColor
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PATH = r"D:\KnowledgeBase\小帅的知识库\💼 面试\本人面试准备\简历-李文韬-AI智能应用开发方向.docx"

doc = Document(PATH)

CONTENT_WIDTH = 11906 - 1134 - 1134  # A4 - 左右页边距 = 9638 twips
SECTION_TITLES = {"专业技能", "工作经历", "项目经历"}
LABEL_RE = re.compile(r"^(技术架构：|项目介绍：|个人职责：)")
MODULE_RE = re.compile(r"^\d、.*：$")
SKILL_GROUP_RE = re.compile(r"^[一二三四五六]、")
TIME_RE = re.compile(r"^　　\d{4}\.\d{2} - ")


def set_bottom_border(paragraph, color="BFBFBF", size="6", space="4"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = pPr.find(qn("w:pBdr"))
    if pBdr is None:
        pBdr = OxmlElement("w:pBdr")
        pPr.append(pBdr)
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:space"), space)
    bottom.set(qn("w:color"), color)
    pBdr.append(bottom)


stats = {"time_right": 0, "keepnext": 0, "divider": 0}

for p in doc.paragraphs:
    text = p.text.strip()
    pf = p.paragraph_format

    # 1) 项目标题：时间右对齐（替换全角空格为右制表位）+ 细分隔线 + 与下段同页
    if any(r.text.startswith("　　") and TIME_RE.match(r.text) for r in p.runs):
        for r in p.runs:
            if r.text.startswith("　　") and TIME_RE.match(r.text):
                r.text = "\t" + r.text.lstrip("　")
                stats["time_right"] += 1
        pf.tab_stops.add_tab_stop(Twips(CONTENT_WIDTH), WD_TAB_ALIGNMENT.RIGHT)
        pf.keep_with_next = True
        set_bottom_border(p, color="D9D9D9", size="4", space="3")
        stats["divider"] += 1
        continue

    # 2) 章节标题 / 标签行 / 模块标题 / 技能组标题：与下段同页
    if text in SECTION_TITLES or LABEL_RE.match(text) or MODULE_RE.match(text) or SKILL_GROUP_RE.match(text):
        pf.keep_with_next = True
        stats["keepnext"] += 1
        continue

    # 3) 工作经历公司行：与下段同页（保险）
    if text.startswith("地坤商务服务有限公司"):
        pf.keep_with_next = True
        stats["keepnext"] += 1

doc.save(PATH)
print("done:", stats)

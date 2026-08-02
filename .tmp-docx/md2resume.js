import fs from "node:fs";
import path from "node:path";
import {
  AlignmentType, BorderStyle, Document, Packer, Paragraph, TabStopType, TextRun, ImageRun,
  convertInchesToTwip,
} from "docx";

const outputPath = process.argv[2];
if (!outputPath) throw new Error("Usage: node md2resume.js /absolute/path/output.docx");

const MD_PATH = "D:/KnowledgeBase/小帅的知识库/.tmp-docx/优化版.md";
const PHOTO_PATH = "D:/KnowledgeBase/小帅的知识库/.tmp-docx/photo.png";

const FONT = { ascii: "Calibri", hAnsi: "Calibri", cs: "Calibri", eastAsia: "Microsoft YaHei" };
const CODE_FONT = { ascii: "Consolas", hAnsi: "Consolas", cs: "Consolas", eastAsia: "Microsoft YaHei" };
const ACCENT = "1F3864";
const GRAY = "595959";

const run = (text, options = {}) => new TextRun({ text, font: FONT, size: 21, ...options });
const para = (children, options = {}) => new Paragraph({
  spacing: { after: 60 },
  ...options,
  children: Array.isArray(children) ? children : [children],
});

// ---- inline markdown: **bold** 和 `code` ----
function inlineRuns(text, base = {}) {
  const runs = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0, m;
  const push = (t, opts) => { if (t) runs.push(run(t, { ...base, ...opts })); };
  while ((m = re.exec(text)) !== null) {
    push(text.slice(last, m.index), {});
    const tok = m[0];
    if (tok.startsWith("**")) push(tok.slice(2, -2), { bold: true });
    else push(tok.slice(1, -1), { font: CODE_FONT, size: 20 });
    last = m.index + tok.length;
  }
  push(text.slice(last), {});
  return runs;
}

const CONTENT_WIDTH = 11906 - 1134 - 1134;

const sectionTitle = (text) => para(run(text, { bold: true, size: 26, color: ACCENT }), {
  spacing: { before: 240, after: 120 },
  keepNext: true,
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ACCENT, space: 4 } },
});

const projectTitle = (title, time) => para([
  run(title, { bold: true, size: 23 }),
  run(`\t${time || ""}`, { bold: true, size: 21, color: GRAY }),
], {
  spacing: { before: 200, after: 80 },
  keepNext: true,
  tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_WIDTH }],
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "D9D9D9", space: 3 } },
});

const labelPara = (text) => para(run(text, { bold: true }), { spacing: { before: 60, after: 50 }, keepNext: true });
const groupHead = (text) => para(run(text, { bold: true }), { spacing: { before: 140, after: 60 }, keepNext: true });
const moduleHead = (text) => para(run(text, { bold: true }), { spacing: { before: 90, after: 50 }, keepNext: true });
const skillItem = (text) => para(inlineRuns(text), { indent: { left: convertInchesToTwip(0.15) }, spacing: { after: 50 } });
const bullet = (text) => para([run("• ", {}), ...inlineRuns(text)], { indent: { left: convertInchesToTwip(0.2) }, spacing: { after: 40 } });
const bodyPara = (text, opts = {}) => para(inlineRuns(text), { spacing: { after: 80 }, ...opts });

const md = fs.readFileSync(MD_PATH, "utf8");
const lines = md.split(/\r?\n/);

const children = [];

// 证件照（右上角）+ 姓名信息
if (fs.existsSync(PHOTO_PATH)) {
  children.push(para(new ImageRun({
    type: "png",
    data: fs.readFileSync(PHOTO_PATH),
    transformation: { width: 105, height: 141 },
  }), { alignment: AlignmentType.RIGHT, spacing: { after: 0 } }));
}

const LABELS = new Set(["技术架构：", "项目介绍：", "个人职责：", "量化成果总览：", "量化成果："]);

for (const raw of lines) {
  const line = raw.trim();
  if (!line || line === "---") continue;

  if (line.startsWith("# ")) {
    children.push(para(run(line.slice(2), { bold: true, size: 44 }), { alignment: AlignmentType.CENTER, spacing: { after: 60 } }));
  } else if (line.startsWith("📞")) {
    children.push(para(run(line, { size: 20, color: GRAY }), { alignment: AlignmentType.CENTER, spacing: { after: 40 } }));
  } else if (line.startsWith("📅")) {
    children.push(para(run(line, { size: 20, color: GRAY }), { alignment: AlignmentType.CENTER, spacing: { after: 120 } }));
  } else if (line.startsWith("## ")) {
    children.push(sectionTitle(line.slice(3)));
  } else if (line.startsWith("### ")) {
    const parts = line.slice(4).split(/\s{2,}/);
    children.push(projectTitle(parts[0], parts[1] || ""));
  } else if (/^\*\*[一二三四五六]、.+\*\*$/.test(line)) {
    children.push(groupHead(line.slice(2, -2)));
  } else if (/^\*\*\d、.+\*\*$/.test(line)) {
    children.push(moduleHead(line.slice(2, -2)));
  } else if (/^\*\*.+\*\*$/.test(line) && LABELS.has(line.slice(2, -2))) {
    children.push(labelPara(line.slice(2, -2)));
  } else if (line.includes("｜") && line.startsWith("**")) {
    // 工作经历公司行
    children.push(para(inlineRuns(line), { spacing: { before: 60, after: 60 }, keepNext: true }));
  } else if (/^\d+\.\s/.test(line)) {
    children.push(skillItem(line));
  } else if (line.startsWith("- ")) {
    children.push(bullet(line.slice(2)));
  } else {
    children.push(bodyPara(line));
  }
}

const doc = new Document({
  features: { updateFields: false },
  styles: { default: { document: { run: { font: FONT, size: 21 } } } },
  sections: [{
    properties: { page: { margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 } } },
    children,
  }],
});

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, await Packer.toBuffer(doc));
console.log("written:", outputPath);

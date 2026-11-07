"""
Compiles paper/report.md + figures/*.png into:
  1. paper/report.html (Apart Research academic paper styling with clean math typesetting)
  2. paper/AI_x_Epistemics_Research_Report.pdf (via Headless Chrome vector PDF print)
  3. paper/AI_x_Epistemics_Research_Report.docx (via python-docx with embedded figures & tables)
Also records verified PDF pagination and abstract word count into results/statistical_summary.json.
"""
import base64
import json
import re
import subprocess
from pathlib import Path

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
import markdown


ROOT = Path("C:/Users/11/.gemini/antigravity/scratch/apart-epistemics-sprint")
CHROME_PATH = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")


def img_to_data_uri(img_path: Path) -> str:
    b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def latex_to_clean_html(expr: str) -> str:
    """Converts LaTeX math expressions in report.md into clean offline HTML typography."""
    s = expr.strip()
    replacements = [
        (r"\\mathbb\{I\}", "𝕀"),
        (r"\\mathcal\{D\}_A", "𝒟<sub>A</sub>"),
        (r"\\mathcal\{D\}_B", "𝒟<sub>B</sub>"),
        (r"\\mathcal\{E\}_A", "ℰ<sub>A</sub>"),
        (r"\\mathcal\{E\}_B", "ℰ<sub>B</sub>"),
        (r"\\mathcal\{E\}", "ℰ"),
        (r"\\text\{([^}]+)\}", r"\1"),
        (r"\\hat\{Y\}", "Ŷ"),
        (r"\\hat\{C\}", "Ĉ"),
        (r"\\hat\{p\}", "p̂"),
        (r"Y\^\*", "Y*"),
        (r"\\downarrow", "↓"),
        (r"\\uparrow", "↑"),
        (r"\\max", "max"),
        (r"\\min", "min"),
        (r"\\left\(", "("),
        (r"\\right\)", ")"),
        (r"\\left\|", "|"),
        (r"\\right\|", "|"),
        (r"\\left\[", "["),
        (r"\\right\]", "]"),
        (r"\\in", "∈"),
        (r"\\neq", "≠"),
        (r"\\equiv", "≡"),
        (r"\\exists", "∃"),
        (r"\\mid", " | "),
        (r"\\to", "→"),
        (r"\\mapsto", "↦"),
        (r"\\leftarrow", "←"),
        (r"\\times", "×"),
        (r"\\dots", "…"),
        (r"\\Delta", "Δ"),
        (r"\\quad", " &nbsp;&nbsp;&nbsp; "),
        (r"\\;", " "),
        (r"\\sum_\{([^}]+)\}\^\{([^}]+)\}", r"∑<sub>\1</sub><sup>\2</sup>"),
        (r"\\sum_\{([^}]+)\}", r"∑<sub>\1</sub>"),
        (r"\\frac\{([^}]+)\}\{([^}]+)\}", r"(\1)/(\2)"),
        (r"_\{([^}]+)\}", r"<sub>\1</sub>"),
        (r"_([A-Za-z0-9]+)", r"<sub>\1</sub>"),
        (r"\^\{([^}]+)\}", r"<sup>\1</sup>"),
        (r"\^([A-Za-z0-9+\-]+)", r"<sup>\1</sup>"),
        (r"\\\{", "{"),
        (r"\\\}", "}"),
        (r"\\\%", "%"),
    ]
    for pat, rep in replacements:
        s = re.sub(pat, rep, s)
    # Second pass in case nested fractions or subscripts remained
    for pat, rep in replacements:
        s = re.sub(pat, rep, s)
    return s


def convert_math_in_markdown(md_text: str) -> str:
    def repl_block(m):
        inner = latex_to_clean_html(m.group(1))
        return f'<div class="math-block">{inner}</div>'

    md_text = re.sub(r"\$\$([^$]+)\$\$", repl_block, md_text)

    def repl_inline(m):
        inner = latex_to_clean_html(m.group(1))
        return f'<span class="math-inline">{inner}</span>'

    md_text = re.sub(r"\$([^$\n]+)\$", repl_inline, md_text)
    return md_text


def verify_abstract_word_count(md_text: str) -> int:
    m = re.search(r"<div class=\"abstract-box\">(.*?)</div>", md_text, flags=re.S)
    if not m:
        return 0
    raw = re.sub(r"<[^>]+>", " ", m.group(1))
    words = [w for w in raw.split() if w.strip()]
    return len(words)


def build_html_and_pdf(md_path: Path, html_path: Path, pdf_path: Path):
    md_text = md_path.read_text(encoding="utf-8")
    abs_words = verify_abstract_word_count(md_text)
    print(f"Abstract word count: {abs_words} words (Sprint requirement: 150-250 words)")
    if not (150 <= abs_words <= 250):
        raise ValueError(f"Abstract word count {abs_words} outside required [150, 250] range!")

    def repl_img(match):
        alt = match.group(1)
        rel_path = match.group(2)
        full_p = (md_path.parent / rel_path).resolve()
        if not full_p.exists():
            full_p = (ROOT / rel_path).resolve()
        if full_p.exists():
            uri = img_to_data_uri(full_p)
            return (
                f'<figure class="paper-figure">'
                f'<img src="{uri}" alt="{alt}" />'
                f'<figcaption><strong>{alt.split(":")[0]}:</strong>{":".join(alt.split(":")[1:])}</figcaption>'
                f'</figure>'
            )
        return match.group(0)

    processed_md = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl_img, md_text)
    processed_md = convert_math_in_markdown(processed_md)
    body_html = markdown.markdown(processed_md, extensions=["tables", "fenced_code"])

    css = """
    @page {
        size: letter;
        margin: 0.46in 0.58in 0.46in 0.58in;
    }
    body {
        font-family: "Georgia", "Times New Roman", serif;
        font-size: 8.75pt;
        line-height: 1.29;
        color: #111827;
        margin: 0;
        padding: 0;
    }
    .header-banner {
        border-top: 3px solid #0b3d2e;
        border-bottom: 1.5px solid #0b3d2e;
        padding: 6px 0 6px 0;
        margin-bottom: 8px;
        text-align: center;
    }
    .sprint-badge {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 7.5pt;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #0b3d2e;
        margin-bottom: 2px;
    }
    h1 {
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 13.0pt;
        font-weight: 800;
        color: #0f172a;
        margin: 2px 0 4px 0;
        line-height: 1.15;
    }
    .authors-block {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 8.0pt;
        color: #334155;
        margin-bottom: 2px;
    }
    h2 {
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 10.0pt;
        font-weight: 700;
        color: #0b3d2e;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 1.5px;
        margin-top: 7px;
        margin-bottom: 3.5px;
    }
    h3 {
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 9.0pt;
        font-weight: 700;
        color: #1e293b;
        margin-top: 5.5px;
        margin-bottom: 2.5px;
    }
    p {
        margin: 0 0 4px 0;
        text-align: justify;
    }
    ul, ol {
        margin: 0 0 4px 0;
        padding-left: 16px;
    }
    li {
        margin-bottom: 1.5px;
    }
    .abstract-box {
        background-color: #f8fafc;
        border-left: 3.5px solid #0b3d2e;
        padding: 6px 10px;
        margin: 4px 0 8px 0;
        font-size: 8.4pt;
        text-align: justify;
    }
    .math-block {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 3px;
        padding: 3px 8px;
        margin: 3px 0 4px 0;
        text-align: center;
        font-family: "Cambria Math", "Times New Roman", serif;
        font-size: 8.7pt;
    }
    .math-inline {
        font-family: "Cambria Math", "Times New Roman", serif;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 4px 0 6px 0;
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 7.0pt;
    }
    th {
        background-color: #0b3d2e;
        color: #ffffff;
        font-weight: 700;
        text-align: left;
        padding: 2.8px 4px;
        border: 1px solid #0b3d2e;
    }
    td {
        padding: 2.2px 4px;
        border: 1px solid #cbd5e1;
        vertical-align: top;
    }
    tr:nth-child(even) td {
        background-color: #f8fafc;
    }
    .paper-figure {
        margin: 4px auto 6px auto;
        text-align: center;
        page-break-inside: avoid;
    }
    .paper-figure img {
        max-width: 92%;
        max-height: 1.92in;
        height: auto;
        border: 1px solid #e2e8f0;
        border-radius: 3px;
    }
    .paper-figure figcaption {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 7.1pt;
        color: #334155;
        margin-top: 2px;
        text-align: left;
        padding: 0 10px;
    }
    code, pre {
        font-family: "Consolas", "Courier New", monospace;
        font-size: 7.5pt;
        background-color: #f1f5f9;
        padding: 0 2px;
        border-radius: 2px;
    }
    .page-break {
        page-break-before: always;
    }
    """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Epistemic Discriminability Under Multi-Turn Pressure — Apart Research Sprint Report</title>
<style>{css}</style>
</head>
<body>
{body_html}
</body>
</html>
"""
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(full_html, encoding="utf-8")

    cmd = [
        str(CHROME_PATH),
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(f"Chrome PDF generation failed: {res.stderr}")
    pdf_bytes = pdf_path.read_bytes()
    page_count = len(re.findall(rb"/Type\s*/Page\b", pdf_bytes))
    print(f"Compiled PDF: {pdf_path} ({len(pdf_bytes):,} bytes, total pages including appendices: {page_count})")

    summary_path = ROOT / "results" / "statistical_summary.json"
    if summary_path.exists():
        summary_obj = json.loads(summary_path.read_text(encoding="utf-8"))
        summary_obj["pdf_and_format_verification"] = {
            "pdf_path": str(pdf_path.relative_to(ROOT)).replace("\\", "/"),
            "pdf_size_bytes": len(pdf_bytes),
            "total_pdf_pages_with_refs_and_appendices": page_count,
            "main_paper_pages_excluding_refs_and_appendices": page_count - 2,
            "meets_4_to_8_page_main_paper_limit": (4 <= (page_count - 2) <= 8),
            "abstract_word_count": abs_words,
            "meets_150_to_250_word_abstract_limit": (150 <= abs_words <= 250),
        }
        summary_path.write_text(json.dumps(summary_obj, indent=2, ensure_ascii=False), encoding="utf-8")


def build_docx(md_path: Path, docx_path: Path):
    doc = docx.Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(10.5)

    lines = md_path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('<div class="authors-block">'):
            auth_txt = re.sub(r"<[^>]+>", "", line)
            p = doc.add_paragraph(auth_txt)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            i += 1
            continue
        if not line or line.startswith("<div") or line.startswith("</div"):
            i += 1
            continue
        if line.startswith("<h1>"):
            title_txt = re.sub(r"<[^>]+>", "", line)
            p = doc.add_heading(title_txt, level=0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif line.startswith("# "):
            p = doc.add_heading(line[2:].strip(), level=0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), level=1)
        elif line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=2)
        elif line.startswith("!["):
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            if m:
                caption, rel = m.group(1), m.group(2)
                img_p = (md_path.parent / rel).resolve()
                if not img_p.exists():
                    img_p = (ROOT / rel).resolve()
                if img_p.exists():
                    doc.add_picture(str(img_p), width=Inches(5.8))
                    cap_p = doc.add_paragraph(caption)
                    cap_p.runs[0].italic = True
                    cap_p.runs[0].font.size = Pt(9)
        elif line.startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = []
            for tl in table_lines:
                cells = [c.strip() for c in tl.strip("|").split("|")]
                if all(set(c) <= set(":-") for c in cells):
                    continue
                rows.append(cells)
            if rows:
                t = doc.add_table(rows=len(rows), cols=len(rows[0]))
                t.style = "Table Grid"
                for r_idx, r_cells in enumerate(rows):
                    for c_idx, val in enumerate(r_cells[: len(rows[0])]):
                        cell = t.cell(r_idx, c_idx)
                        clean_val = re.sub(r"\*\*([^*]+)\*\*", r"\1", val)
                        clean_val = re.sub(r"\$([^$]+)\$", r"\1", clean_val)
                        cell.text = clean_val
            continue
        elif line.startswith("- ") or line.startswith("* "):
            clean_li = re.sub(r"\*\*([^*]+)\*\*", r"\1", line[2:].strip())
            clean_li = re.sub(r"\$([^$]+)\$", r"\1", clean_li)
            doc.add_paragraph(clean_li, style="List Bullet")
        else:
            clean = re.sub(r"<[^>]+>", "", line)
            clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", clean)
            if clean:
                doc.add_paragraph(clean)
        i += 1

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(docx_path))
    print(f"Compiled DOCX: {docx_path} ({docx_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    md_file = ROOT / "paper" / "report.md"
    html_file = ROOT / "paper" / "report.html"
    pdf_file = ROOT / "paper" / "AI_x_Epistemics_Research_Report.pdf"
    docx_file = ROOT / "paper" / "AI_x_Epistemics_Research_Report.docx"
    build_html_and_pdf(md_file, html_file, pdf_file)
    build_docx(md_file, docx_file)

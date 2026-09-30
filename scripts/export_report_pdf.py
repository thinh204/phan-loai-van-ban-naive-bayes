"""Export the Vietnamese report to PDF (optional dependency: reportlab)."""
from __future__ import annotations

import re
from html import escape
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]


def inline(value: str) -> str:
    value = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', value)
    value = escape(value)
    value = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', value)
    value = re.sub(r'`([^`]+)`', r'\1', value)
    return value


def build_report(font_dir: Path = Path('C:/Windows/Fonts')) -> Path:
    for family, filename in [('ReportFont', 'arial.ttf'), ('ReportBold', 'arialbd.ttf')]:
        pdfmetrics.registerFont(TTFont(family, str(font_dir / filename)))
    pdfmetrics.registerFontFamily('ReportFont', normal='ReportFont', bold='ReportBold', italic='ReportFont', boldItalic='ReportBold')
    styles = getSampleStyleSheet()
    for s in styles.byName.values():
        s.fontName = 'ReportFont'
    body = ParagraphStyle('ReportBody', fontName='ReportFont', fontSize=10.5, leading=16, spaceAfter=7)
    heading = ParagraphStyle('ReportHeading', parent=body, fontName='ReportBold', fontSize=15, leading=21, spaceBefore=13, spaceAfter=9, keepWithNext=True)
    subheading = ParagraphStyle('ReportSubheading', parent=heading, fontSize=12, leading=18)
    cover = ParagraphStyle('ReportCover', parent=heading, fontSize=20, leading=29, alignment=1)
    centered = ParagraphStyle('ReportCentered', parent=body, alignment=1)
    cell = ParagraphStyle('ReportCell', parent=body, fontSize=9, leading=13, spaceAfter=0)
    target = ROOT / 'docs/bao-cao-do-an.pdf'
    document = SimpleDocTemplate(str(target), pagesize=A4, rightMargin=50, leftMargin=50, topMargin=48, bottomMargin=48, title='Đồ án Trí tuệ nhân tạo — Phân loại văn bản', author='Nhóm D23VHCN01-N')
    text = (ROOT / 'docs/bao-cao.md').read_text(encoding='utf-8')
    front = text.split('## Mục lục')[0]
    members = [line.strip('| ').split('|') for line in front.splitlines() if line.startswith('| ') and 'Thành viên' not in line and '---' not in line]
    instructor = next(line for line in front.splitlines() if line.startswith('Giảng viên:'))
    story = [Spacer(1, 40), Paragraph('HỌC VIỆN CÔNG NGHỆ<br/>BƯU CHÍNH VIỄN THÔNG', cover), Spacer(1, 35), Paragraph('ĐỒ ÁN MÔN TRÍ TUỆ NHÂN TẠO', cover), Spacer(1, 20), Paragraph('Nghiên cứu và trình bày phương pháp<br/>phân loại văn bản bằng<br/>Multinomial Naive Bayes', cover), Spacer(1, 34), Paragraph('Lớp: <b>D23VHCN01-N</b>', centered)]
    for member in members:
        story.append(Paragraph(inline(' — '.join(item.strip() for item in member)), centered))
    story += [Spacer(1, 20), Paragraph(inline(instructor), centered), Spacer(1, 20), Paragraph('Ngày hoàn thiện: 01/10/2026', centered), PageBreak(), Paragraph('Mục lục', heading)]
    content = text[text.index('## 1. Bài toán'):]
    for line in content.splitlines():
        if line.startswith('## '):
            story.append(Paragraph(inline(line[3:]), body))
    story.append(PageBreak())
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                current = lines[i].strip()
                if not re.match(r'^\|[\s:|\-]+\|$', current):
                    cells = re.split(r'\|(?=(?:[^`]*`[^`]*`)*[^`]*$)', current.strip('|'))
                    rows.append([Paragraph(inline(c.strip()), cell) for c in cells])
                i += 1
            table = Table(rows, colWidths=[(A4[0] - 100) / len(rows[0])] * len(rows[0]), repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EAF0F5')), ('GRID', (0, 0), (-1, -1), .4, colors.HexColor('#ADB8C4')), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
            story.append(KeepTogether([table, Spacer(1, 10)]))
            continue
        if line.startswith('## '):
            story.append(Paragraph(inline(line[3:]), heading))
        elif line.startswith('### '):
            story.append(Paragraph(inline(line[4:]), subheading))
        else:
            story.append(Paragraph(inline(line), body))
            if re.match(r'^\[\d+\]', line):
                for url in re.findall(r'\]\((https://[^)]+)\)', line):
                    story.append(Paragraph(f'<link href="{escape(url, quote=True)}" color="#165A8A">{escape(url)}</link>', cell))
        i += 1

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('ReportFont', 8)
        canvas.setFillColor(colors.HexColor('#536171'))
        canvas.drawString(50, 26, 'Trí tuệ nhân tạo — Phân loại văn bản bằng Naive Bayes')
        canvas.drawRightString(A4[0] - 50, 26, str(doc.page))
        canvas.restoreState()
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    return target


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--font-dir', type=Path, default=Path('C:/Windows/Fonts'), help='Directory containing arial.ttf and arialbd.ttf')
    args = parser.parse_args()
    print(build_report(args.font_dir))

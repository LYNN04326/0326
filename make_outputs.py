# -*- coding: utf-8 -*-
"""把「年資_年」插入原檔 C、D 欄之間，並補回被匯出程式吃掉的中文欄位標題。
同時輸出 CSV 與 Excel（欄寬已調好，日期不會顯示成 ######）。"""
import csv, datetime, re
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font, Alignment

SRC = "/root/.claude/uploads/b50c582f-c718-5e95-96c3-aa756b3b5f25/4f245814-7608_________________Sheet1_1.csv"
YEARS = "/home/user/0326/年資整理結果.csv"          # 取其中的「年資_年」
CSV_OUT = "/home/user/0326/原檔_含年資欄.csv"
XLSX_OUT = "/home/user/0326/原檔_含年資欄.xlsx"
BIG5_OUT = "/home/user/0326/原檔_含年資欄_Big5.csv"   # 繁中版 Excel 直接開不會亂碼
FIXED_OUT = "/home/user/0326/原檔_含年資欄_已修正順序.xlsx"  # 起迄填反的自動對調並標黃

# 沿用原檔標題，只在第 3、4 欄之間插入「年資_年」
_src = list(csv.reader(open(SRC, encoding="utf-8-sig")))
SRC_HEADER, SRC_ROWS = _src[0], _src[1:]
HEADER = SRC_HEADER[:3] + ["年資_年"] + SRC_HEADER[3:]

DATE_RE = re.compile(r"^(\d{4})/(\d{1,2})/(\d{1,2})")

years = [r[5] for r in list(csv.reader(open(YEARS, encoding="utf-8-sig")))[1:]]
rows = SRC_ROWS
assert len(years) == len(rows), (len(years), len(rows))

# ---- CSV（保留原始儲存格文字，只插欄＋換標題） ----
with open(CSV_OUT, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    for y, r in zip(years, rows):
        w.writerow(r[:3] + [y] + r[3:])

# ---- Big5 版（Windows 繁中 Excel 雙擊即開） ----
with open(CSV_OUT, encoding="utf-8-sig") as f, open(BIG5_OUT, "w", encoding="big5", newline="") as g:
    g.write(f.read())

# ---- Excel（日期轉成真正的日期值，欄寬與格式都設好） ----
wb = Workbook(write_only=True)
ws = wb.create_sheet("年資")
ws.freeze_panes = "E2"
widths = {"A": 11, "B": 38, "C": 12, "D": 10}
for i in range(40):
    widths[chr(ord("E") + i) if i < 22 else "A" + chr(ord("A") + i - 22)] = 13
for col, wd in widths.items():
    ws.column_dimensions[col].width = wd

hdr = []
for h in HEADER:
    c = WriteOnlyCell(ws, value=h)
    c.font = Font(bold=True)
    c.alignment = Alignment(horizontal="center")
    hdr.append(c)
ws.append(hdr)

for y, r in zip(years, rows):
    line = [r[0], r[1], int(r[2]) if r[2].strip().lstrip("-").isdigit() else r[2], float(y)]
    for v in r[3:]:
        v = v.strip()
        m = DATE_RE.match(v)
        if m:
            c = WriteOnlyCell(ws, value=datetime.date(*map(int, m.groups())))
            c.number_format = "yyyy/m/d"
            line.append(c)
        else:
            line.append(v)
    ws.append(line)
wb.save(XLSX_OUT)


# ---- 已修正順序版：起迄填反者自動對調，並把對調過的格子標黃 ----
from openpyxl.styles import PatternFill
MIN_VALID = datetime.date(1940, 1, 1)
YELLOW = PatternFill("solid", fgColor="FFE58F")

def to_date(v):
    m = DATE_RE.match(v.strip())
    return datetime.date(*map(int, m.groups())) if m else None

wb2 = Workbook(write_only=True)
ws2 = wb2.create_sheet("年資")
ws2.freeze_panes = "E2"
for col, wd in widths.items():
    ws2.column_dimensions[col].width = wd
ws2.column_dimensions["AS"].width = 34

hdr2 = []
for h in HEADER + ["順序修正註記"]:
    c = WriteOnlyCell(ws2, value=h)
    c.font = Font(bold=True); c.alignment = Alignment(horizontal="center")
    hdr2.append(c)
ws2.append(hdr2)

fixed_pairs = 0
fixed_rows = 0
for y, r in zip(years, rows):
    cells = list(r[3:])
    notes = []
    for i in range(0, len(cells) - 1, 2):
        s_, e_ = to_date(cells[i]), to_date(cells[i + 1])
        if s_ and e_ and s_ >= MIN_VALID and e_ >= MIN_VALID and e_ < s_:
            cells[i], cells[i + 1] = cells[i + 1], cells[i]
            notes.append(SRC_HEADER[3 + i] + "／" + SRC_HEADER[4 + i])
            fixed_pairs += 1
    if notes:
        fixed_rows += 1
    swapped = set()
    for name in notes:
        j = SRC_HEADER.index(name.split("／")[0]) - 3
        swapped.update({j, j + 1})

    line = [r[0], r[1], int(r[2]) if r[2].strip().lstrip("-").isdigit() else r[2], float(y)]
    for idx, v in enumerate(cells):
        v = v.strip()
        m = DATE_RE.match(v)
        if m:
            c = WriteOnlyCell(ws2, value=datetime.date(*map(int, m.groups())))
            c.number_format = "yyyy/m/d"
        else:
            c = WriteOnlyCell(ws2, value=v)
        if idx in swapped:
            c.fill = YELLOW
        line.append(c)
    line.append("、".join(notes) + " 已對調" if notes else "")
    ws2.append(line)
wb2.save(FIXED_OUT)

print("完成：", CSV_OUT, "/", XLSX_OUT)
print(f"已修正順序版：{FIXED_OUT}（對調 {fixed_pairs} 組，分布在 {fixed_rows} 列）")

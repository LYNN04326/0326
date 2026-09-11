# -*- coding: utf-8 -*-
"""把「年資_年」插入原檔 C、D 欄之間，並補回被匯出程式吃掉的中文欄位標題。
同時輸出 CSV 與 Excel（欄寬已調好，日期不會顯示成 ######）。"""
import csv, datetime, re
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Font, Alignment

SRC = "/root/.claude/uploads/b50c582f-c718-5e95-96c3-aa756b3b5f25/8e33dd6b-7608_________________Sheet1.csv"
YEARS = "/home/user/0326/年資整理結果.csv"          # 取其中的「年資_年」
CSV_OUT = "/home/user/0326/原檔_含年資欄.csv"
XLSX_OUT = "/home/user/0326/原檔_含年資欄.xlsx"

# 原始標題的中文在匯出時已變成 "?"，這裡補回可讀名稱
HEADER = ["talentNo", "resumeGuid", "experience", "年資_年"]
for i in range(1, 21):
    HEADER += [f"工作{i}起日", f"工作{i}迄日"]

DATE_RE = re.compile(r"^(\d{4})/(\d{1,2})/(\d{1,2})")

years = [r[5] for r in list(csv.reader(open(YEARS, encoding="utf-8-sig")))[1:]]
rows = list(csv.reader(open(SRC, encoding="utf-8", errors="replace")))[1:]
assert len(years) == len(rows), (len(years), len(rows))

# ---- CSV（保留原始儲存格文字，只插欄＋換標題） ----
with open(CSV_OUT, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    for y, r in zip(years, rows):
        w.writerow(r[:3] + [y] + r[3:])

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
print("完成：", CSV_OUT, "/", XLSX_OUT)

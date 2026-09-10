#!/usr/bin/env python3
"""Token-efficient TCode export inspector. Prints the MINIMUM needed.

Usage:
  tcode.py sheets  <file>                 sheet names + row count + ChangeType counts
  tcode.py header  <file> <sheet>         header row only (letter:idx:name)
  tcode.py changes <file> <sheet>         rows where ChangeType != UnChange  (ct  no  nameA)
  tcode.py find    <file> <sheet> <code…> full field dump for given CodeNo(s)
  tcode.py cats    <file> <sheet> <ct>    items of ChangeType <ct> grouped by 中類(F)
  tcode.py grep    <file> <sheet> <term…> rows whose CodeNameA/B contains a term

Conventions: A=ChangeType(1) D=CodeNo(4) E=CodeNameA(5) F=CodeNameB(6)
G=CodeNameC(7) H=CodeType(8). Compare ChangeType case-insensitively.
"""
import sys, openpyxl
from collections import Counter, defaultdict

def norm(s): return "" if s is None else str(s).strip()
def asint(v):
    try: return int(float(v))
    except: return None

def load(path, ro=True):
    return openpyxl.load_workbook(path, data_only=True, read_only=ro)

def hdr_map(ws):
    return {norm(ws.cell(1, c).value): c for c in range(1, ws.max_column + 1) if norm(ws.cell(1, c).value)}

def cmd_sheets(path):
    wb = load(path)
    for sh in wb.sheetnames:
        ws = wb[sh]
        cnt = Counter(norm(ws.cell(r, 1).value).lower() for r in range(2, ws.max_row + 1))
        nonu = {k: v for k, v in cnt.items() if k and k != "unchange"}
        tag = f"  changes={nonu}" if nonu else ""
        print(f"{sh}: rows={ws.max_row - 1}{tag}")

def cmd_header(path, sheet):
    ws = load(path)[sheet]
    for c in range(1, ws.max_column + 1):
        v = ws.cell(1, c).value
        if v is not None:
            print(f"{openpyxl.utils.get_column_letter(c)}({c}): {v!r}")

def cmd_changes(path, sheet):
    ws = load(path)[sheet]
    h = hdr_map(ws); no_c = h.get("CodeNo", 4); na_c = h.get("CodeNameA", 5)
    n = 0
    for r in range(2, ws.max_row + 1):
        ct = norm(ws.cell(r, 1).value)
        if ct and ct.lower() != "unchange":
            print(f"{ct}\t{asint(ws.cell(r, no_c).value)}\t{norm(ws.cell(r, na_c).value)}")
            n += 1
    print(f"-- {n} changed rows --")

def cmd_find(path, sheet, codes):
    codes = {int(c) for c in codes}
    ws = load(path, ro=False)[sheet]
    h = hdr_map(ws); inv = {v: k for k, v in h.items()}; no_c = h.get("CodeNo", 4)
    for r in range(2, ws.max_row + 1):
        no = asint(ws.cell(r, no_c).value)
        if no in codes:
            print(f"== {no} ==")
            for c in range(1, ws.max_column + 1):
                v = ws.cell(r, c).value
                if v is not None and norm(v) != "":
                    print(f"  {inv.get(c, openpyxl.utils.get_column_letter(c))}: {norm(v)!r}")

def cmd_cats(path, sheet, ct):
    ws = load(path)[sheet]
    h = hdr_map(ws); no_c = h.get("CodeNo", 4); na_c = h.get("CodeNameA", 5)
    nb_c = h.get("CodeNameB", 6); ht_c = h.get("CodeType", 8)
    newcats = []; groups = defaultdict(list)
    for r in range(2, ws.max_row + 1):
        if norm(ws.cell(r, 1).value).lower() == ct.lower():
            A = norm(ws.cell(r, na_c).value); B = norm(ws.cell(r, nb_c).value)
            T = ws.cell(r, ht_c).value if ht_c else None
            (newcats if T == 2 else groups[B or "(無分類)"]).append(A)
    if newcats: print(f"[新分類 {len(newcats)}] " + "、".join(newcats))
    for cat, names in groups.items():
        print(f"〔{cat}〕({len(names)}) " + "、".join(names))

def cmd_grep(path, sheet, terms):
    ws = load(path)[sheet]
    h = hdr_map(ws); no_c = h.get("CodeNo", 4); na_c = h.get("CodeNameA", 5); nb_c = h.get("CodeNameB", 6)
    for r in range(2, ws.max_row + 1):
        A = norm(ws.cell(r, na_c).value); B = norm(ws.cell(r, nb_c).value)
        if any(t.lower() in A.lower() or t.lower() in B.lower() for t in terms):
            print(f"{asint(ws.cell(r, no_c).value)}\t{A!r}\t中類={B!r}")

def main():
    a = sys.argv
    if len(a) < 3: print(__doc__); sys.exit(1)
    cmd, path = a[1], a[2]
    if cmd == "sheets": cmd_sheets(path)
    elif cmd == "header": cmd_header(path, a[3])
    elif cmd == "changes": cmd_changes(path, a[3])
    elif cmd == "find": cmd_find(path, a[3], a[4:])
    elif cmd == "cats": cmd_cats(path, a[3], a[4])
    elif cmd == "grep": cmd_grep(path, a[3], a[4:])
    else: print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()

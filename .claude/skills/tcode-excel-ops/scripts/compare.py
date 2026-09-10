#!/usr/bin/env python3
"""TCode 檔案對照 / version diff.

Usage:
  compare.py edits   <old> <new> <sheet> <code…>   per-code diff of name+4lang fields
  compare.py collide <export> <sheet> <code…>      list new CodeNo already occupied
  compare.py reuse   <export> <sheet>              detect code-reuse (add CodeNo == delete/move CodeNo)

`edits` confirms a rename/edit actually landed (exports reset ChangeType to
UnChange, so you must diff against the prior file). `collide` is the pre-insert
coupling check. `reuse` flags high-risk recycled CodeNos.
"""
import sys, openpyxl
from collections import defaultdict

def norm(s): return "" if s is None else str(s).strip()
def asint(v):
    try: return int(float(v))
    except: return None

def index(path, sheet):
    wb = openpyxl.load_workbook(path, data_only=True)
    if sheet not in wb.sheetnames: return {}, {}
    ws = wb[sheet]
    h = {norm(ws.cell(1, c).value): c for c in range(1, ws.max_column + 1) if norm(ws.cell(1, c).value)}
    no_c = h.get("CodeNo", 4)
    idx = {}
    for r in range(2, ws.max_row + 1):
        no = asint(ws.cell(r, no_c).value)
        if no is None: continue
        idx[no] = {k: norm(ws.cell(r, c).value) for k, c in h.items()}
    return idx, h

KEYS = ["CodeNameA", "CodeNameB", "CodeNameC", "CodeNameA_EN",
        "CodeNameA_VI", "CodeNameA_TH", "CodeNameA_ID"]

def cmd_edits(old, new, sheet, codes):
    oi, _ = index(old, sheet); ni, _ = index(new, sheet)
    for code in (int(c) for c in codes):
        o = oi.get(code, {}); n = ni.get(code, {})
        if not n: print(f"❌ {code}: 新檔無此碼"); continue
        diffs = [(k, o.get(k, ""), n.get(k, "")) for k in KEYS if o.get(k, "") != n.get(k, "")]
        if diffs:
            print(f"✏️ {code} {n.get('CodeNameA','')!r}")
            for k, ov, nv in diffs:
                print(f"   [{k}] 舊:{ov!r} → 新:{nv!r}")
        else:
            print(f"✅ {code} {n.get('CodeNameA','')!r} 一致")

def cmd_collide(export, sheet, codes):
    idx, _ = index(export, sheet)
    hit = [(c, idx[c]["CodeNameA"]) for c in (int(x) for x in codes) if c in idx]
    print(f"衝突 {len(hit)} / {len(codes)}")
    for c, nm in hit: print(f"  ⚠ {c} 已被佔用: {nm!r}")
    if not hit: print("  ✅ 無衝突，可直接插入")

def cmd_reuse(export, sheet):
    wb = openpyxl.load_workbook(export, data_only=True); ws = wb[sheet]
    h = {norm(ws.cell(1, c).value): c for c in range(1, ws.max_column + 1) if norm(ws.cell(1, c).value)}
    no_c = h.get("CodeNo", 4); na_c = h.get("CodeNameA", 5)
    old_owner = {}; new_owner = {}
    for r in range(2, ws.max_row + 1):
        ct = norm(ws.cell(r, 1).value).lower(); no = asint(ws.cell(r, no_c).value)
        b = asint(ws.cell(r, 2).value); name = norm(ws.cell(r, na_c).value)
        if ct in ("move", "move_edit") and b is not None: old_owner[b] = name
        elif ct == "delete" and no is not None: old_owner[no] = name
        elif ct == "add" and no is not None: new_owner[no] = name
    n = 0
    for code, newn in sorted(new_owner.items()):
        if code in old_owner:
            print(f"  {code}: 原={old_owner[code]!r} → 重用為={newn!r}"); n += 1
    print(f"-- {n} 代碼重用 (上線前舊資料須先遷移) --")

def main():
    a = sys.argv
    if len(a) < 4: print(__doc__); sys.exit(1)
    if a[1] == "edits": cmd_edits(a[2], a[3], a[4], a[5:])
    elif a[1] == "collide": cmd_collide(a[2], a[3], a[4:])
    elif a[1] == "reuse": cmd_reuse(a[2], a[3])
    else: print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""重算履歷年資（experience），規則比照公司系統實際行為。

由三批「求職者代碼查詢」結果反推並驗證：
  1. 工作1開始為空 -> 無工作經驗（代號 1），後面段落不看
  2. 每段月數 = (結束年月 - 開始年月) + 1     ← 含頭含尾
  3. 結束日未填（1911/1/1、1905/3/27、1900/1/1、1959/6/1、顛倒…）
     -> 系統顯示「未填寫」，該段不計入年資
     （若該段其實是「在職中」，系統會算到該履歷的上線日；
       但匯出檔沒有「是否在職」欄位，故另開一欄提供對照值）
  4. 累計年資 = 各段月數直接相加（不合併重疊）
  5. 代號 = 累計年數 + 2，上限 32；無任何有效段落 -> 1

驗證通過的案例：
  阮天心 47223292  -> 59 個月  = 4~5年    （系統顯示 4~5年）
  幸攽   53533406  -> 181 個月 = 15年1個月（系統顯示 共15年1個月 / 15~16年）
  古文卿 1183362   -> 8 個月              （系統顯示 共0年8個月）
  陳佑羽 52465267  -> 4 個月              （系統顯示 共0年4個月）
  黃家振 3820758   -> 無工作經驗          （系統顯示 無工作經驗）
  高士民 34862370  -> 無工作經驗          （系統顯示 無工作經驗）
"""
import csv, datetime, re, sys, collections

SRC = sys.argv[1] if len(sys.argv) > 1 else \
    "/root/.claude/uploads/b50c582f-c718-5e95-96c3-aa756b3b5f25/4f245814-7608_________________Sheet1_1.csv"
DST = sys.argv[2] if len(sys.argv) > 2 else "/home/user/0326/年資整理結果.csv"
BASE_DATE = datetime.date(2026, 9, 11)   # 「視為在職中」時算到這天
MIN_VALID = datetime.date(1940, 1, 1)    # 早於此日期一律視為未填寫
# 系統寫入的「空值」日期（由資料分布與系統顯示「未填寫」反推）
SENTINELS = {datetime.date(1911, 1, 1), datetime.date(1905, 3, 27), datetime.date(1900, 1, 1),
             datetime.date(1959, 6, 1), datetime.date(1944, 9, 1), datetime.date(1944, 6, 1)}

EXPERIENCE = ["1_無工作經驗"] + [f"{i+2}_{i}~{i+1}年工作經驗" for i in range(30)] + ["32_30年以上工作經驗"]
DATE_RE = re.compile(r"^(\d{4})/(\d{1,2})/(\d{1,2})")


def parse(v):
    m = DATE_RE.match((v or "").strip())
    if not m:
        return None
    try:
        return datetime.date(*map(int, m.groups()))
    except ValueError:
        return None


def month_span(s, e):
    """系統的算法：含頭含尾，例如 2005/03~2020/03 = 181 個月 = 15年1個月。"""
    return (e.year - s.year) * 12 + (e.month - s.month) + 1


def code_of(months, has_any):
    if not has_any:
        return 1
    return min(months // 12 + 2, 32)


def analyse(row):
    """回傳 (比照系統的月數, 把未填視為在職中的月數, 有效段數, 未填段數, 註記)"""
    segs = [(parse(row[3 + i]), parse(row[4 + i])) for i in range(0, 40, 2)
            if row[3 + i].strip() != "NULL" or row[4 + i].strip() != "NULL"]
    notes = []
    if not segs:
        return 0, 0, 0, 0, []
    first = segs[0][0]
    if first is None or first < MIN_VALID or first in SENTINELS:
        notes.append("工作1開始為空 → 無工作經驗")
        return 0, 0, 0, 0, notes

    sys_mo = alt_mo = 0
    ok = unfilled = 0
    for n, (s, e) in enumerate(segs, 1):
        if s is None or s < MIN_VALID or s in SENTINELS:
            notes.append(f"第{n}段缺開始日，略過")
            continue
        if s > BASE_DATE:
            notes.append(f"第{n}段開始日晚於基準日")
            continue
        bad_end = e is None or e < MIN_VALID or e in SENTINELS or e < s
        if bad_end:
            unfilled += 1
            notes.append(f"第{n}段結束日未填（{row[4 + (n-1)*2].strip()}）")
            alt_mo += month_span(s, BASE_DATE)      # 若視為在職中
            continue
        if e > BASE_DATE:
            e = BASE_DATE
            notes.append(f"第{n}段結束日晚於基準日，截至基準日")
        m = month_span(s, e)
        sys_mo += m
        alt_mo += m
        ok += 1
    return sys_mo, alt_mo, ok, unfilled, notes


def main():
    rows = list(csv.reader(open(SRC, encoding="utf-8-sig")))
    header, data = rows[0], rows[1:]

    out = [["talentNo", "resumeGuid", "experience_原值", "experience_新值", "experience_新值說明",
            "年資_年", "年資_月", "有效工作段數", "結束日未填段數",
            "年資_年_若未填視為在職中", "experience_若未填視為在職中", "資料狀況"]]
    stat = collections.Counter()
    dist = collections.Counter()
    years_by_row = []

    for r in data:
        sys_mo, alt_mo, ok, unfilled, notes = analyse(r)
        code = code_of(sys_mo, ok > 0)
        alt_code = code_of(alt_mo, ok > 0 or unfilled > 0)
        old = r[2].strip()

        stat["總筆數"] += 1
        if code == 1:
            stat["無工作經驗"] += 1
        if unfilled:
            stat["含未填結束日"] += 1
        if old.isdigit() and int(old) != code:
            stat["年資有更正"] += 1
        if code != alt_code:
            stat["兩種認定會不同"] += 1
        dist[code] += 1

        years_by_row.append(round(sys_mo / 12, 2))
        out.append([r[0], r[1], old, code, EXPERIENCE[code - 1],
                    round(sys_mo / 12, 2), sys_mo, ok, unfilled,
                    round(alt_mo / 12, 2), alt_code, "；".join(notes)])

    with open(DST, "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows(out)

    print("== 統計 ==")
    for k, v in stat.items():
        print(f"  {k}: {v:,}")
    print("\n== 新年資分布（前後各 5 級）==")
    ks = sorted(dist)
    for c in ks[:5] + ["…"] + ks[-5:]:
        print("  …" if c == "…" else f"  {EXPERIENCE[c-1]}: {dist[c]:,}")
    return years_by_row


if __name__ == "__main__":
    main()

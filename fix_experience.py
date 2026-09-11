# -*- coding: utf-8 -*-
"""重新計算履歷年資 (experience) 的工具。

規則：
  1. 第 1 段起日 (D 欄) 為哨兵日期  -> 無工作經驗
  2. 迄日為哨兵日期                 -> 在職中，以基準日計算
  3. 起日為哨兵日期 (非 D 欄)       -> 該段無效，略過
  4. 迄日 < 起日 (兩者皆為有效日期) -> 視為填反，對調並標記
  5. 日期超過基準日                 -> 截到基準日
  6. 多段工作期間重疊               -> 合併聯集，避免重複計算
"""
import csv, datetime, re, sys, collections

SRC = sys.argv[1] if len(sys.argv) > 1 else \
    "/root/.claude/uploads/b50c582f-c718-5e95-96c3-aa756b3b5f25/8e33dd6b-7608_________________Sheet1.csv"
DST = sys.argv[2] if len(sys.argv) > 2 else "/home/user/0326/年資整理結果.csv"
BASE_DATE = datetime.date(2026, 9, 11)          # 資料基準日（在職中算到這天）
MIN_VALID = datetime.date(1940, 1, 1)           # 早於此日期一律視為哨兵／無效值

EXPERIENCE = ["1_無工作經驗", "2_0~1年工作經驗", "3_1~2年工作經驗", "4_2~3年工作經驗",
    "5_3~4年工作經驗", "6_4~5年工作經驗", "7_5~6年工作經驗", "8_6~7年工作經驗",
    "9_7~8年工作經驗", "10_8~9年工作經驗", "11_9~10年工作經驗", "12_10~11年工作經驗",
    "13_11~12年工作經驗", "14_12~13年工作經驗", "15_13~14年工作經驗", "16_14~15年工作經驗",
    "17_15~16年工作經驗", "18_16~17年工作經驗", "19_17~18年工作經驗", "20_18~19年工作經驗",
    "21_19~20年工作經驗", "22_20~21年工作經驗", "23_21~22年工作經驗", "24_22~23年工作經驗",
    "25_23~24年工作經驗", "26_24~25年工作經驗", "27_25~26年工作經驗", "28_26~27年工作經驗",
    "29_27~28年工作經驗", "30_28~29年工作經驗", "31_29~30年工作經驗", "32_30年以上工作經驗"]

DATE_RE = re.compile(r"^(\d{4})/(\d{1,2})/(\d{1,2})")


def parse(v):
    v = (v or "").strip()
    if v in ("NULL", ""):
        return None
    m = DATE_RE.match(v)
    if not m:
        return None
    try:
        return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def is_sentinel(d):
    """哨兵／不可能的日期：1911/1/1、1900/1/1、1905/3/27 … 一律視為未填寫。"""
    return d is None or d < MIN_VALID


def experience_code(days, has_period):
    if not has_period:
        return 1
    years = days / 365.2425
    return min(int(years) + 2, 32)


def write_with_years(src, dst, years_by_row, header):
    """把「年資_年」欄插入原始檔案的 C、D 欄之間，其餘欄位原封不動。"""
    with open(src, encoding="utf-8", errors="replace", newline="") as f, \
         open(dst, "w", encoding="utf-8-sig", newline="") as g:
        r = csv.reader(f); w = csv.writer(g)
        head = next(r)
        w.writerow(head[:3] + ["年資_年"] + head[3:])
        for i, row in enumerate(r):
            w.writerow(row[:3] + [years_by_row[i]] + row[3:])


def main():
    with open(SRC, encoding="utf-8", errors="replace", newline="") as f:
        rows = list(csv.reader(f))
    header, data = rows[0], rows[1:]

    out = [["talentNo", "resumeGuid", "experience_原值", "experience_新值", "experience_新值說明",
            "年資_年", "年資_月", "是否在職中", "有效工作段數", "最早到職日", "最後離職日",
            "年資_未合併重疊_年", "資料異常註記"]]
    stat = collections.Counter()
    years_by_row = []
    code_dist = collections.Counter()
    issue_rows = []

    for r in data:
        cells = [parse(c) for c in r[3:43]]
        notes, periods, working = [], [], False
        raw_days = 0

        for i in range(0, 40, 2):
            s, e = cells[i], cells[i + 1]
            n = i // 2 + 1
            if s is None and e is None:
                continue
            if is_sentinel(s):
                if not is_sentinel(e):
                    notes.append(f"第{n}段缺起日")
                continue
            if s > BASE_DATE:
                notes.append(f"第{n}段起日晚於基準日")
                s = BASE_DATE
            if is_sentinel(e):                    # 迄日空白 -> 在職中
                e = BASE_DATE
                working = True
            elif e < s:                           # 起迄顛倒 -> 對調
                notes.append(f"第{n}段起迄顛倒已對調")
                s, e = e, s
            if e > BASE_DATE:
                notes.append(f"第{n}段迄日晚於基準日")
                e = BASE_DATE
            periods.append((s, e))
            raw_days += (e - s).days

        # 合併重疊區間
        merged, days = [], 0
        for s, e in sorted(periods):
            if merged and s <= merged[-1][1]:
                if e > merged[-1][1]:
                    merged[-1] = (merged[-1][0], e)
            else:
                merged.append((s, e))
        for s, e in merged:
            days += (e - s).days
        if days < raw_days:
            notes.append("工作期間有重疊已合併")

        code = experience_code(days, bool(periods))
        old = r[2].strip()
        if not old.isdigit() or not (1 <= int(old) <= 32):
            notes.append(f"原 experience 值不合法({old})")
        if periods and code == 1:
            notes.append("有工作期間但年資為 0")

        stat["總筆數"] += 1
        if not periods:
            stat["無工作經驗"] += 1
        if working:
            stat["在職中"] += 1
        if old.isdigit() and int(old) != code:
            stat["年資有更正"] += 1
        if notes:
            stat["有異常註記"] += 1
        code_dist[code] += 1

        row = [r[0], r[1], old, code, EXPERIENCE[code - 1],
               round(days / 365.2425, 2), round(days / 30.4369, 1),
               "Y" if working else "N", len(periods),
               merged[0][0].strftime("%Y/%m/%d") if merged else "",
               "在職中" if working else (merged[-1][1].strftime("%Y/%m/%d") if merged else ""),
               round(raw_days / 365.2425, 2), "；".join(notes)]
        years_by_row.append(round(days / 365.2425, 2))
        out.append(row)
        if notes:
            issue_rows.append(row)

    with open(DST, "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f).writerows(out)
    with open(DST.replace(".csv", "_需人工確認.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow(out[0]); w.writerows(issue_rows)

    write_with_years(SRC, "/home/user/0326/原檔_含年資欄.csv", years_by_row, header)

    print("== 統計 ==")
    for k, v in stat.items():
        print(f"  {k}: {v}")
    print("\n== 新年資分布 ==")
    for c in sorted(code_dist):
        print(f"  {EXPERIENCE[c-1]}: {code_dist[c]}")


if __name__ == "__main__":
    main()

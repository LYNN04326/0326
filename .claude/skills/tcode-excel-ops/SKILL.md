---
name: tcode-excel-ops
description: >-
  Operate on 1111人力銀行 TCode 代碼表 Excel exports (tCodeCertify, tCodeWorkAbility,
  tCodeCompSkill, tCodeDutyNM, tCodeDutyPT, tCodeBenefit, etc.). Use this skill
  whenever the user works with a TCode_Export file or 代碼表/職務代碼/證照/工作技能/職能
  spreadsheets and wants to: inspect/analyze the sheets, compare two export
  versions (檔案對照), apply 新增/改名/合併 requirements with translations, verify a
  code's ChangeType/edits got applied, detect CodeNo collisions or 代碼耦合,
  build a multi-sheet 異動清單 xlsx, write a Markdown 異動 table, or draft a
  系統公告. Trigger even if the user only says "更新 export"、"列出異動項目"、"發公告"、
  "比對舊新檔"、"分析這個代碼表" without naming the schema explicitly. Analyze Excel
  the token-efficient way described here rather than dumping whole sheets.
---

# TCode 代碼表 Excel 作業

Operations on 1111 TCode export spreadsheets. Read `references/export-schema.md`
first when touching column data; it is the single source of truth for column
positions, CodeType, and translation columns.

## Token-efficient Excel analysis (核心原則)

NEVER dump whole sheets into context. openpyxl in `read_only=True` + targeted
prints only. All TCode sheets share a stable layout (verify via header once):
`A=ChangeType, B=Old_CodeNo, C=New_CodeNo, D=CodeNo, E=CodeNameA(項目),
F=CodeNameB(中類), G=CodeNameC(大類), H=CodeType(1大類/2中類/3項目)`, then
4-language blocks (see schema). CompSkill differs: `G=CodeNameB? ` — always
confirm with the header print before trusting positions on CompSkill/DutyNM.

Use `scripts/tcode.py` — one tool, sub-commands, each prints the minimum:

```
python scripts/tcode.py sheets   <file>                 # sheet names + rows + ChangeType counts
python scripts/tcode.py header   <file> <sheet>         # header row only (col letter:index:name)
python scripts/tcode.py changes  <file> <sheet>         # rows where ChangeType != UnChange (ct,no,nameA)
python scripts/tcode.py find     <file> <sheet> <code…> # full field dump for specific CodeNo(s)
python scripts/tcode.py cats     <file> <sheet> <ct>    # items of a ChangeType grouped by 中類(F)
python scripts/tcode.py grep     <file> <sheet> <term…> # CodeNameA/B containing term (E,F cols)
```

Survey workflow: `sheets` → (if a sheet has changes) `cats`/`changes` → `find`
only the rows you must read in detail. This is how the analysis stayed cheap
across the whole project; do not regress to printing every row.

## Common tasks

### 1. 檔案對照 / version diff (檔案對照成果)
Exports reset every ChangeType to `UnChange` once applied — UnChange means
"已套用完成", not "no change". So you cannot read what changed from the new file
alone; you must map it against the requirement code list (or the prior file).

- Verify edits applied: `python scripts/compare.py edits <old> <new> <sheet> <code…>`
  prints per-code whether CodeNameA/B/C + 4-lang fields differ. Used to confirm
  改名/edit landed (e.g. 職訓局→勞動部勞動力發展署技能檢定中心, ISO renames).
- New-code collision / 代碼耦合 check before inserting:
  `python scripts/compare.py collide <export> <sheet> <code…>` → lists any new
  CodeNo already occupied (different CodeNameA) in production.
- 合併/重複 coupling: a merge SOURCE code's existing references must migrate to
  the TARGET before the source is removed. Count merge/dup codes; if <10 it is
  low-coupling and safe to proceed. See `references/changetype-rules.md`.

### 2. Apply 新增/改名 requirements + translations
Read `references/export-schema.md` (translation rules) and
`references/changetype-rules.md` (ChangeType semantics) before building. Key
rules that bit us repeatedly:
- **Certify**: CodeNameA 直接填入原文到 EN/VI/TH/ID（證照名不翻譯）；descriptions
  translate only. BUT Certify items that are Chinese phrases (TQC/ITE/環保/TIPCI/
  ICDL series) DO need real EN/VI/TH/ID translation — copy-as-is only for already-
  English proper-noun cert names.
- **WorkAbility**: translate ALL CodeNameA into EN/VI/TH/ID.
- **中類/大類 translations**: reuse from an existing sibling row in the same 中類
  (CodeNameB) / 大類 (CodeNameC); don't re-translate.
- New 中類 introduced by new items needs a CodeType=2 header row created too.
- Verify after writing: zero duplicate CodeNo, ascending sort, expected fill counts.

### 3. move / move_edit / delete for duplicate pairs
Requirement tables use delete/move/move_edit, NOT merge. For a duplicate pair:
later (larger) CodeNo → `delete`; earlier (smaller) CodeNo → `move` (kept as-is)
or `move_edit` (kept but renamed). On the survivor row:
`Old_CodeNo = 消失(被刪)的代碼`, `New_CodeNo = 目標(自身保留)代碼`. Mark changed rows
orange. Full rules + the worked 5-pair example in `references/changetype-rules.md`.

### 4. 列出異動項目 → Markdown table (撰寫markdown成果)
Format and a full real example in `references/markdown-output.md`. Defaults:
one table per sheet, columns `異動方式 | CodeNo | CodeNameA`, **RENAME is shown as
EDIT**, ADD before EDIT. If the user says "code snippet" / "in markdown", wrap the
WHOLE thing in one ```markdown fenced block so they can copy it.

### 5. 發公告 / write 系統公告 (發公告成果)
Format + a full real announcement in `references/announcement-template.md`.
Structure: one section per affected 表 (證照/工作技能/電腦技能/職務/兼職職務…),
with 🆕新增分類 / 🆕新增項目 / ✏️更新項目 / 🗑️刪除項目 sub-blocks, items grouped by
中類 in a `類別 | 項目` table. End with a 合計 line. Build the grouping with
`scripts/tcode.py cats`; condense long category lists ("…等共 N 項") for readability.

### 6. Build multi-sheet 異動清單 xlsx (deliverable)
Read `/mnt/skills/public/xlsx/SKILL.md` first. One sheet per TCode table, columns
`異動方式 | CodeNo | CodeNameA`, separator row per ChangeType, fills:
ADD=green `E2EFDA`, EDIT=blue `DEEAF1`, RENAME→treat as EDIT. CodeNameA pulled
from the newest export. `scripts/build_report.py` does this from a JSON spec; or
adapt inline. Save to `/mnt/user-data/outputs/`, then `present_files`.

## Gotchas (learned the hard way)
- web_fetch on Google Sheets returns ~100 rows truncated and reorders; CSV-export
  and `pub?output=csv` URLs are blocked by robots/allowlist. Ask the user to
  upload the .xlsx instead of fighting this.
- ChangeType values appear in mixed case (`Add`/`add`, `Edit`/`edit`/`rename`).
  Always compare case-insensitively and fold `rename`→`edit` for output.
- A job/duty "不合理" judgment is too strict if the 職缺名稱 already contains the
  category keyword (e.g. 行政會計人員 → 行政人員 is fine). When re-judging
  reasonableness, a category slot is justified if its keyword appears in the name.
- CodeType is unreliable on a few CompSkill rows (blank); fall back to the CodeNo
  prefix / 中類 to classify.
- After str_replace/edits, re-verify counts; don't trust an earlier in-context dump.

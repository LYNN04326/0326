# TCode Export 欄位結構 (single source of truth)

All `TCode_Export_*.xlsx` sheets (tCodeCertify, tCodeWorkAbility, tCodeBenefit,
tCodeDutyPT, …) share this 25-column layout. **Always confirm with a header print
once per file** (`tcode.py header`), because tCodeCompSkill and tCodeDutyNM have
extra/shifted columns.

## Standard layout (Certify / WorkAbility / Benefit / DutyPT)

| Col | Idx | Field | Notes |
|---|---|---|---|
| A | 1 | ChangeType | UnChange / add / edit / rename / move / move_edit / delete (mixed case) |
| B | 2 | Old_CodeNo | for move/move_edit = 消失(被刪)的代碼 |
| C | 3 | New_CodeNo | for move/move_edit = 目標(保留)代碼 |
| D | 4 | **CodeNo** | the key |
| E | 5 | **CodeNameA** | 項目名稱 (leaf, CodeType=3) |
| F | 6 | **CodeNameB** | 中類 (CodeType=2) |
| G | 7 | **CodeNameC** | 大類 (CodeType=1) |
| H | 8 | **CodeType** | 1=大類, 2=中類, 3=項目 |
| I | 9 | keywords | usually blank |
| J | 10 | CodeNameA_EN | EN block |
| K | 11 | CodeNameB_EN | (中類譯, reuse from sibling) |
| L | 12 | CodeNameC_EN | (大類譯, reuse from sibling) |
| M | 13 | CodeDescript_EN | |
| N | 14 | CodeNameA_VI | VI block |
| O | 15 | CodeNameB_VI | |
| P | 16 | CodeNameC_VI | |
| Q | 17 | CodeDescript_VI | |
| R | 18 | CodeNameA_TH | TH block |
| S | 19 | CodeNameB_TH | |
| T | 20 | CodeNameC_TH | |
| U | 21 | CodeDescript_TH | |
| V | 22 | CodeNameA_ID | ID block |
| W | 23 | CodeNameB_ID | |
| X | 24 | CodeNameC_ID | |
| Y | 25 | CodeDescript_ID | |

Per language the four columns are always: NameA, NameB, NameC, Descript.

## tCodeCompSkill (differs)
`A=ChangeType, D=CodeNo, E=CodeNameA, F=CodeNameB(中類), G=CodeDescript,
H=CodeType, I=CodeNoNew, J=CodeNameA_EN …`. There is no CodeNameC. Confirm header.

## tCodeDutyNM / DutyPT (job duties, wide)
Has many extra source columns (CodeDescript, CodeCore, CodeAlike, CodeMajor,
CodeDefinition, chsNameA/Description/JobContent, Holland, …) before the EN/VI/TH/ID
blocks. Header indices for the duty edit we did:
ChangeType1, CodeNo4, CodeNameA5, CodeNameB6, CodeNameC7, CodeType8, CodeDescript9,
CodeCore10, CodeAlike11, CodeMajor14, CodeDefinition15, chsNameA16, chsDescription17,
chsJobContent18, chsAlike20, Holland21, CodeNameEN26, CodeNameCHS27,
CodeNameA_EN28, B29, C30, Descript31, VI 32-35, TH 36-39, ID 40-43. Always re-confirm.

## CodeType meaning
- 1 = 大類 (top): row's E=F=G = the 大類 name.
- 2 = 中類 (header): E=F = 中類 name, G = 大類 name. New items under a brand-new
  中類 require creating this header row.
- 3 = 項目 (leaf): the actual selectable item.

## Translation rules (which cells to fill for new/renamed rows)
- **CodeNameA (J/N/R/V)**:
  - WorkAbility & Chinese-phrase Certify (TQC/ITE/EEC/TIPCI/ICDL/環保 series) →
    real translate to EN/VI/TH/ID.
  - Already-English proper-noun cert names (Microsoft/AWS/Google/Cisco…) → 直接填入
    原文 (copy as-is to all four).
- **CodeNameB (K/O/S/W)** = 中類: reuse the existing translation of that 中類 from
  any sibling row; only translate if the 中類 itself is new.
- **CodeNameC (L/P/T/X)** = 大類: reuse from an existing row of that 大類.
- **CodeDescript (M/Q/U/Y)**: translate if a source description exists; Certify
  rows usually have none → leave blank.
- House style examples: 熟悉X = "Be familiar with X" / "Quen thuộc với" /
  "คุ้นเคยกับ" / "Familiar dengan"; 保險=insurance/bảo hiểm/ประกันภัย/asuransi;
  keep technical English (ML, NLP, LLM, RAG, CI/CD, BI) intact across all langs.

## Post-write verification (always)
- zero duplicate CodeNo per sheet
- CodeNo ascending
- new/edited rows have all four CodeNameA langs filled
- red/orange fills land on exactly the intended rows

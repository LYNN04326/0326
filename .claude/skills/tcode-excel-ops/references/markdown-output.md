# 異動清單 Markdown 輸出格式 (撰寫markdown成果)

## Rules
- One table per TCode sheet, header order: `異動方式 | CodeNo | CodeNameA`.
- **RENAME → display as EDIT.** ADD block before EDIT block. Sort by CodeNo.
- Pull CodeNameA from the **newest** export.
- If user says "code snippet" / "table in markdown" → wrap the ENTIRE output in a
  single ```markdown fenced block (so they copy raw markdown, not rendered).
- If user wants only 異動方式 + CodeNo + CodeNameA (no translations), keep just those.

## Skeleton
```
### <sheetName>

| 異動方式 | CodeNo | CodeNameA |
|---|---|---|
| ADD | <no> | <nameA> |
| …    |      |         |
| EDIT | <no> | <nameA> |
```

## Real example (2026/06/17 異動, condensed)
```
### tCodeCertify

| 異動方式 | CodeNo | CodeNameA |
|---|---|---|
| ADD | 180547 | Microsoft Certified: Power Platform Fundamentals |
| ADD | 186000 | TIPCI 臺灣國際專業認證學會 |
| ADD | 187002 | ICDL-文書處理 |
| ADD | 189001 | Certified Kubernetes Administrator (CKA) |
| ADD | 230147 | 淨零碳規劃管理師-初級能力鑑定 |
| EDIT | 183800 | 勞動部勞動力發展署技能檢定中心 |
| EDIT | 230135 | ISO 14064-1 組織溫室氣體盤查內部查證員 |

### tCodeWorkAbility

| 異動方式 | CodeNo | CodeNameA |
|---|---|---|
| ADD | 110700 | 金融行政業務 |
| ADD | 140217 | 檢索增強生成（RAG）系統建置與優化 |
| ADD | 230122 | 熟悉人身保險規範 |

### tCodeCompSkill

| 異動方式 | CodeNo | CodeNameA |
|---|---|---|
| EDIT | 1225 | LotusScript |

### tCodeDutyNM

| 異動方式 | CodeNo | CodeNameA |
|---|---|---|
| EDIT | 250510 | 英語教師 |
| EDIT | 250514 | 華語教師 |

### tCodeDutyPT

| 異動方式 | CodeNo | CodeNameA |
|---|---|---|
| ADD | 250510 | 英語教師 |
| ADD | 250514 | 華語教師 |
```

## 本批 ADD CodeNo 區段對照（產生清單時可直接展開 range）
Certify ADD: 180547-180549, 180704-180722, 181013, 181116, 182614-182615,
183197-183199, 183755-183759, 184317-184321, 184422-184427, 184808-184814,
185613-185618, 186000-186032, 187000-187024, 188000-188003, 189000-189002,
230141-230164.
Certify EDIT: 140401, 140429, 140436, 183800-183809, 230135-230136.
WorkAbility ADD: 100209-100210, 100414-100416, 110120-110125, 110213,
110311-110316, 110700-110711, 130114-130118, 130207-130208, 140212-140228,
140414-140417, 230122-230133, 260115-260116, 290209-290212.
CompSkill EDIT: 1225. DutyNM EDIT: 190222, 250510-250514. DutyPT ADD: 250510-250514.
(These are the requirement code lists used to map against UnChange'd exports.)

# 系統公告格式 (發公告成果)

## Structure
- Title: `# 代碼表異動公告（YYYY/MM/DD）`
- One `## 一、二、三…` section per affected 表, titled `表中文名（EnglishSheet）`,
  e.g. 證照（Certify）、工作技能（WorkAbility）、電腦技能（CompSkill）、
  職務小類（DutyNM）、兼職職務（DutyPT）、福利制度（Benefit）.
- Within a section, the relevant sub-blocks (omit empty ones):
  - `### 🆕 新增分類（N 個）` — a one-cell table listing brand-new 中類.
  - `### 🆕 新增項目（N 項）` — `類別 | 新增項目` table, items grouped by 中類(F),
    joined with 、 . Condense long lists: "…等共 N 項".
  - `### ✏️ 更新項目（N 項）` — same `類別 | 更新項目` shape; note 分類更名 explicitly.
  - `### 🗑️ 刪除項目（N 項）` — same shape.
- End: `**本次異動合計**：新增分類 X 個、新增項目 Y 項、更新項目 Z 項。`
- Build grouping with `tcode.py cats <file> <sheet> add` / `edit`. RENAME→EDIT.

## Real example (2026/06/17, condensed — full categories abbreviated with 等共N項)

```
# 代碼表異動公告（2026/06/17）

## 一、證照（Certify）

### 🆕 新增分類（4 個）
| 新增分類 |
|---|
| TIPCI 臺灣國際專業認證學會、ICDL Foundation／財團法人電腦技能基金會（CSF）、HashiCorp、CNCF |

### 🆕 新增項目（143 項）
| 類別 | 新增項目 |
|---|---|
| MICROSOFT | Power Platform Fundamentals、Security Compliance and Identity Fundamentals、Azure Data Scientist Associate |
| Microsoft (Certiport) | ITS 系列（網路管理、網路安全、資料庫、Python、人工智慧…）、Apple Swift、IC3、ESB 等共 19 項 |
| TQC / ITE / TQC+ / EEC | 會計 IFRS、電子商務、AutoCAD 製圖、雲端服務規劃、AI 應用 等 |
| Google / AWS | Google Cloud 認證、Gemini、AWS Certified AI/Data/ML 等共 13 項 |
| TIPCI（新分類） | 人工智慧應用、程式設計、雲端、資安、大數據 等共 32 項 |
| ICDL（新分類） | 文書處理、試算表、資安、數位行銷、AI、區塊鏈 等共 24 項 |
| HashiCorp / CNCF（新分類） | Infrastructure/Security/Networking Automation、CKA、CKS |
| 環保相關 | ISO 14064/14067/14068/14001、淨零碳、ESG、SDGs 等共 24 項 |

### ✏️ 更新項目（14 項，含 1 個分類更名）
| 類別 | 更新項目 |
|---|---|
| 分類更名 | 職訓局 → 勞動部勞動力發展署技能檢定中心 |
| 勞動部勞動力發展署技能檢定中心 | 各級電腦軟體/硬體/網路技術士（共 9 項隨分類更名） |
| 護理相關 | 照顧服務員單一級(丙)技術士、結業證書、居家服務督導員職前訓練結業證明書 |
| 環保相關 | ISO 14064-1 組織溫室氣體盤查內部查證員、ISO 14067 產品碳足跡主任查證員 |

## 二、工作技能（WorkAbility）

### 🆕 新增分類（1 個）
| 新增分類 |
|---|
| 金融行政業務 |

### 🆕 新增項目（75 項）
| 類別 | 新增項目 |
|---|---|
| 金融行政業務（新分類） | 收租/呆帳催款、客訴控管、貸款流程、洗錢防制 等共 11 項 |
| 程式設計 | 機器學習、深度學習、LLM、RAG、Prompt Engineering、生成式 AI 等共 17 項 |
| 法律諮詢 | 熟悉人身保險/股務/交通/航海/鐵路…相關法規 共 12 項 |
| 保險規劃 / 金融理財 / 產品行銷 / 禮儀輔導 … | （依中類分組列出） |

## 三、電腦技能（CompSkill）
### ✏️ 更新項目（1 項）
| 類別 | 更新項目 |
|---|---|
| 程式設計 | LotusScript |

## 四、職務小類（DutyNM）
### ✏️ 更新項目（6 項）
| 類別 | 更新項目 |
|---|---|
| 營造施作 | 建築物清潔人員 |
| 教育師資 | 英語/日語/韓語/其他語系/華語教師（補各語系教師說明與多語翻譯） |

## 五、兼職職務（DutyPT）
### 🆕 新增項目（5 項）
| 類別 | 新增項目 |
|---|---|
| 教育師資 | 英語/日語/韓語/其他語系/華語教師 |

**本次異動合計**：新增分類 5 個、新增項目 223 項、更新項目 21 項。
```

## Earlier example with 🗑️刪除 block (CompSkill batch)
CompSkill announcements also had a `### 🗑️ 刪除項目` block (e.g. Internet Explorer,
Windows 98/XP/Vista/7, BCB/Clipper/Cold Fusion/Delphi/Fortran/Pascal, Flash,
FrontPage…) grouped by 類別. Include that block whenever delete rows exist.

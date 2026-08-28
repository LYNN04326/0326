# component-doc-figma — Figma 元件 → Markdown 文件

> 原始碼：[`.claude/skills/component-doc-figma/SKILL.md`](../component-doc-figma/SKILL.md)　·　舊名：`generate-component-doc-figma`

## 一句話

針對單一 component／component set 產出完整文件頁：overview、anatomy 圖層樹、design tokens、
variants／states 矩陣、typography、無障礙、內容準則，以及選配的 design-code parity 與 YAML frontmatter。

## 觸發時機

「幫這個元件寫文件」「產出 component docs / spec」「寫一下 anatomy 跟 variants」「component handoff doc」。

## 運作方式（兩段式，不可自由發揮）

```
Figma 檔案
   │  scripts/collect-component-data.js   ← 透過 use_figma 執行（Figma Plugin 環境）
   ▼
結構化 JSON（anatomy／colors＋token id／typography／spacing／component props）
   │  node scripts/generate-doc.mjs       ← 在終端機跑 Node
   ▼
Markdown 文件（同樣的 JSON 永遠產出一模一樣的 Markdown）
```

**不可以憑印象手寫這份文件**——轉換器是決定性的，版面規則寫在
[`references/doc-template.md`](../component-doc-figma/references/doc-template.md)，
轉換器已完整實作，那份是規格不是檢查表。跑不了 Node 就直說做不出來，不要硬寫。

## 檔案

| 檔案 | 角色 |
| :--- | :--- |
| `SKILL.md` | 工作流程與邊界 |
| `scripts/collect-component-data.js` | 資料蒐集，跑在 Figma Plugin 環境（top-level await，用 Node CJS 檢查會報錯屬正常） |
| `scripts/generate-doc.mjs` | JSON → Markdown 決定性轉換器（Node，語法檢查通過） |
| `references/doc-template.md` | Markdown 版面規格＋`cleanVariantName` 規則 |

## 依賴

Figma Desktop app（Plugin API）＋終端機能跑 Node。

## 相關 skill

* `figma-use` — 呼叫 `use_figma` 前必讀，由 Figma MCP 提供（`skill://figma/figma-use/SKILL.md`），不需另裝。
* `annotations-figma` — 把 annotation 當獨立規格輸出時用（未安裝）。
* `export-tokens-figma` — 匯出整套 token 系統（而非單一元件）時用（未安裝）。

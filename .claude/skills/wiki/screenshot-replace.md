# screenshot-replace — 截圖換內容（舊版工作流程）

> 原始碼：[`.claude/skills/screenshot-replace/SKILL.md`](../screenshot-replace/SKILL.md)　·　舊名：`png`（曾短暫叫過 `shot-burn`）

## 一句話

用 Pillow 把 badge／覆蓋文字**燒進**截圖像素。**非預設**，只在 [screenshot-add](screenshot-add.md) 辦不到時使用。

## 什麼時候才用

1. 需要**蓋掉截圖裡的舊文字、寫上新文字**（先畫白底矩形蓋掉，再 `ImageDraw.text` 重寫）。
2. 維護沿用「規格書 UI 截圖標號慣例」的**既有**舊規格書。
3. 需要把整段流程輸出成**單一張 PNG**——但**排版方式不是 Pillow**，見下。

其餘一律用 screenshot-add。

## ⚠️ 最重要的一條：版面用 HTML 組，Pillow 只做像素級處理

這條來自真實事故：同一份文件前半用 HTML 版面品質很好，後半改用 `PIL.ImageDraw` 手工排版，
被使用者直接指出「為什麼後來退步了」。三個疊在一起的根因：

| # | 根因 | 實測 |
| :-- | :--- | :--- |
| 1 | 用 1x 光柵化（等同 `dsf=1`） | 820px vs 1568px，字的解析度差一倍 |
| 2 | 為了塞進畫布把來源圖縮小 | 原圖只剩 **70%** 像素，細節永久損失 |
| 3 | 版面退化成單欄置中＋圖下小字 | 卡片分組、步驟標題列、圖左說明右全丟失 |

鐵律：**`ImageDraw.text()` 只允許用在單張截圖的像素級處理**（蓋白重寫、畫紅框、裁切、量 bbox）。
任何標題、說明、箭頭、卡片、表格**都不准用 Pillow 畫**，一律 HTML 組版面 → Playwright 截圖。
版面標準直接沿用 screenshot-add 規則二，**不因為「這次輸出成 PNG」就降級**。

## 內容地圖

| 章節 | 重點 |
| :--- | :--- |
| 整段內容輸出成單一 PNG | 事故記錄＋7 條鐵律＋Python/JS 參考骨架 |
| 規格書 UI 截圖標號慣例 | 截圖標號 **== 章節編號**（`N` ↔ `## N`、`N.M` ↔ `### N.M`）、徽章樣式（`#FF5F57` 紅底白字圓角、Inter 700 / 20px）、套用步驟 |
| 以 Pillow 標注／覆蓋文字 | 抓圖、改字、落差黃框標注、R2 入庫、裁切與 badge 打在留白處、限制 |
| 與 screenshot-add 的分工 | 四行對照表 |

## 依賴

Pillow、Playwright、boto3；中文字型後備 `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`（已存在）。

## 已知缺口

引用了未安裝的 `spec-doc-1111`（截圖標注／覆蓋一節、`初始化` 不編號）。主要重點已內聯在本 skill 內，
缺這支不影響標號流程。

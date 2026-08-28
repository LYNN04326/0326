# shot-overlay — 截圖疊圖標註（預設做法）

> 原始碼：[`.claude/skills/shot-overlay/SKILL.md`](../shot-overlay/SKILL.md)　·　舊名：`photo`

## 一句話

紅框、編號 badge、說明 callout 全部用 HTML 絕對定位**疊在** `<img>` 上方，
**原始截圖像素不動**。

## 為什麼是預設

| 好處 | 說明 |
| :--- | :--- |
| 標註可事後改 | 改百分比座標即可，不用重新產圖 |
| 深色模式可讀 | 文字由瀏覽器渲染，不是燒死的像素 |
| diff 看得出改了什麼 | 標註是文字，不是二進位圖片 |

做不到的只有一件事：**換掉圖片裡原本的文字**（HTML 只能疊在上面）。那種情況才轉 [shot-burn](shot-burn.md)。

## 觸發時機

「截圖標一下」「框起來加編號」「做成點擊流程圖」「這段貼到 HackMD」。

## 內容地圖

| 章節 | 重點 |
| :--- | :--- |
| 規則一　圖片入庫與引用 | 上傳 Cloudflare R2、boto3 流程、5 個環境變數、key 命名、備案條件 |
| 規則二　版面規則 | 白底容器／步驟標題列／圖左說明右 flex／`15px #222 1.65` callout／紅框＋圓形 badge／badge 與 callout 數字呼應／百分比定位＋`aspect-ratio`／純圖片也要外層 `div` 扛 `max-width` |
| └ 輸出成 PNG 的補充 | `deviceScaleFactor≥2`、`CSS 寬 × dsf ≥ 原生寬`、截容器不截 `fullPage` |
| 座標怎麼抓 | 第 0 點：Figma `get_metadata`／`get_design_context` 精確 bounding box 優先；像素掃描是退場方案 |
| PATCH 前跟同文件既有段落並排比對 | 6 項並排比對檢查清單 |
| 多圖點擊流程 | 一步一卡片、只標當步的框、三處同號、箭頭用 CSS |
| 深色模式可讀性 | 卡片明確給白底、callout 顏色不要寫死在無底色區塊上 |

## 依賴

Playwright（僅在需要輸出 PNG 時）、boto3（R2 上傳）、R2 環境變數。詳見 [Home](Home.md#執行環境依賴)。

## 注意

本頁對應的 `SKILL.md` 是安裝時**依 shot-burn 的交叉引用重建**的（原始壓縮檔沒附這支）。
R2 的 5 個環境變數名稱是依慣例訂的，若團隊原本用別的名字要改規則一那張表。

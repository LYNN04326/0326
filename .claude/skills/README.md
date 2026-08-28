# 本專案已安裝的 Skills

| Skill | 用途 | 狀態 |
| :--- | :--- | :--- |
| [`photo`](photo/SKILL.md) | 截圖標註**預設做法**：紅框／badge／說明用 HTML 絕對定位疊在圖片上，不改像素 | 依 `png` 的交叉引用補寫 |
| [`png`](png/SKILL.md) | 舊版做法：Pillow 把 badge／覆蓋文字燒進截圖像素；僅在需要改寫圖內文字或維護舊格式規格書時使用 | 隨壓縮檔安裝 |
| [`generate-component-doc-figma`](generate-component-doc-figma/SKILL.md) | 從 Figma 元件產出完整 Markdown 文件（anatomy／token／variants／a11y） | 隨壓縮檔安裝 |

## 執行環境依賴

`photo` / `png` 用到的套件在這個容器裡**預設沒有裝**，第一次使用前先安裝：

```bash
pip install pillow boto3          # png 的像素處理；R2 上傳
pip install playwright            # 或 npm i -D playwright
```

已具備、不需處理的部分：

* Chromium 已預裝於 `/opt/pw-browsers`，`PLAYWRIGHT_BROWSERS_PATH` 已設好，**不要**執行
  `playwright install`。若版本對不上，改用 `executablePath: '/opt/pw-browsers/chromium'`。
* 中文字型 `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc` 已存在（Pillow 後備字型），
  另有 Noto CJK 可用。

`photo` 規則一的 R2 圖床需要 `R2_ACCOUNT_ID`、`R2_ACCESS_KEY_ID`、`R2_SECRET_ACCESS_KEY`、
`R2_BUCKET`、`R2_PUBLIC_BASE_URL`，**目前環境未設定**；未設定時走備案（圖片 commit 進 repo）。

`generate-component-doc-figma` 需要 Figma Desktop app（Plugin API）＋在終端機執行 Node。

## 尚未安裝的交叉引用

以下 skill 被引用但不在本 repo，用到相關段落時要另外補：

| 被引用的 skill | 引用處 | 說明 |
| :--- | :--- | :--- |
| `spec-doc-1111` | `png/SKILL.md`（截圖標注／覆蓋、`初始化` 不編號） | 求才系統規格書撰寫慣例；`png` 已內聯主要重點，缺這支不影響標號流程 |
| `figma-use` | `generate-component-doc-figma/SKILL.md` | 由 Figma MCP／plugin 提供（`skill://figma/figma-use/SKILL.md`），不需另裝 |
| `annotations-figma` | 同上 | 只在「把 annotation 當獨立規格輸出」時需要 |
| `export-tokens-figma` | 同上 | 只在「匯出整套 token 系統」時需要 |

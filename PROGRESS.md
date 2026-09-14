# 專案進度筆記

> 這份筆記的用途：把每次工作做到哪裡記下來。開新對話時 Claude 會自動讀到，
> 不用再重講一遍上下文。收工前更新最下面的「目前進度」即可。

## 專案是什麼

一批單一自含的 HTML 頁面（CSS/JS 內嵌、不依賴外部 CDN、介面文字用繁體中文），
主要是表單驗證、聯絡資料列、時程分類等 UI 片段，以及外掛安裝指令頁。

## 檔案地圖

| 檔案 | 內容 |
|---|---|
| `claude-plugins.html` | Claude Code 外掛安裝指令頁，含可運作的整段複製按鈕 |
| `verify-phone*.html` / `verify-email-33.html` | 手機／信箱驗證碼流程的各種版本 |
| `verify-popup-*.html` / `verify-code-popup.html` | 驗證碼彈窗的版本 |
| `contact-phone*.html` / `contact-email-row.html` | 聯絡資料的欄位列排版 |
| `schedule-category.html` | 時程清單的分類標題 |
| `final-all.html` | 整合版 |
| `.claude/hooks/session-start.sh` | 開場 hook，安裝 pypdf 等文件處理套件 |

## 工作慣例

- 要程式碼時，完整 HTML 原始碼要直接貼在回覆訊息裡，不能只寫檔案（見 `CLAUDE.md`）
- 回覆一律繁體中文
- 開發分支：`claude/new-session-m9lyzj`

## 環境限制（重要，避免重複踩）

- 這個對話跑在 Claude Code **網頁版**（雲端暫時容器），不是本機電腦
- 網頁版**沒有** `/plugin` 指令，本機外掛裝不了
- 公司電腦有 IT 管理，**無法下載安裝 Claude Code 桌面版**
- 因此：需要 `/plugin install` 的外掛一律不可行；
  改用 (a) claude.ai 帳號層級的雲端外掛，或 (b) 把 skill 檔案放進本專案 `.claude/skills/`

## 目前進度

**最後更新：2026-09-14**

- [x] 建立 `claude-plugins.html`，修好原截圖中失效的複製按鈕
- [x] 釐清外掛安裝的環境限制（見上）
- [x] 建立本進度筆記
- [ ] 評估「48 個外掛」清單中，哪些 skill 可以直接放進本專案使用

### 下一步

測試 `git clone` 型的 skill 能否裝進 `.claude/skills/`，可行的話挑選需要的項目安裝。

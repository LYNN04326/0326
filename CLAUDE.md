# 專案慣例

## 回覆格式

- 使用者要程式碼時，**一定要在回覆訊息中附上完整的純 HTML 原始碼文字**（放在 ```html 程式碼區塊中），
  而不是只把檔案寫到磁碟或只描述改了什麼。即使同時有建立檔案，也要把完整內容貼出來。
- 回覆使用繁體中文。

## 程式碼風格

- HTML 頁面以單一自含檔案為主：CSS 與 JS 內嵌，不依賴外部 CDN。
- 介面文字使用繁體中文。

## Skill 安裝

- 安裝任何 skill 時，**同時**要更新 `.claude/skills/wiki/`：新增該 skill 的詳頁，
  並把它加進 [`wiki/Home.md`](.claude/skills/wiki/Home.md) 的索引表。沒進索引等於沒安裝。
- 名稱不好記就改名，改名要更新所有交叉引用並記進 wiki 的〈改名對照〉。
- wiki 就放在 repo 的 `.claude/skills/wiki/`，不使用 GitHub 的 Wiki 分頁（那是要人工鏡像的獨立
  repo，session 推不上去也容易跟 repo 內容不同步）。
- 完整流程見 `.claude/skills/wiki/Home.md`〈安裝新 skill 的流程〉。

# Skills Wiki

本 repo 已安裝的 Claude Code skills 索引。**每支 skill 的 `SKILL.md` 才是唯一事實來源**，
本 wiki 只做索引與導航；安裝／移除／改名 skill 時要同步更新本頁。

## 索引

| Skill | 一句話 | 什麼時候會被叫起來 | 詳頁 |
| :--- | :--- | :--- | :--- |
| **screenshot-add** | **加**標註上去：紅框／badge／說明用 HTML 疊在圖上，原圖不動，之後還能改 | 「截圖標一下」「框起來加編號」「做成點擊流程圖」「貼到 HackMD」 | [→](screenshot-add.md) |
| **screenshot-replace** | 把新內容**放進**圖裡：用 Pillow 改像素，換掉圖中原本的文字（舊版做法） | 「蓋掉圖裡的字重寫」「舊版標號慣例」「整段輸出成單一 PNG」 | [→](screenshot-replace.md) |
| **component-doc-figma** | Figma 元件 → 完整 Markdown 規格文件 | 「幫這個元件寫文件」「產出 component handoff spec」 | [→](component-doc-figma.md) |

## 選哪一支？

截圖標註類的兩支是同一件事的兩種做法，判斷只有一個問題：

```
要標註截圖
   │
   ├─ 需要「換掉圖片裡原本的文字」？ ── 是 ──→ screenshot-replace（只有改像素做得到）
   │
   ├─ 要維護舊格式「規格書 UI 截圖標號慣例」的存量文件？ ── 是 ──→ screenshot-replace
   │
   └─ 其他全部（紅框、編號、流程圖、存檔） ─────────────→ screenshot-add ★ 預設
```

名字本身就是判斷依據：

* **add** ＝ 在圖上**加**東西（紅框、編號、說明），加完還能改位置，原圖一個像素都沒動。
* **replace** ＝ 把新內容**放進**圖裡，換掉原本就在圖上的東西（最典型：蓋掉舊文字重寫）。

要「加」就用 `screenshot-add`；非得「換掉圖裡原有的東西」才用 `screenshot-replace`。
`screenshot-replace` 產出「整段內容單一 PNG」時，**版面仍沿用 `screenshot-add` 規則二**，
只是最後用 Playwright 截圖成 PNG——不可以退回 Pillow 手工排版。

## 執行環境依賴

截圖兩支用到的套件在容器裡**預設沒有裝**，第一次使用前先安裝：

```bash
pip install pillow boto3          # screenshot-replace 的像素處理；R2 上傳
pip install playwright            # 或 npm i -D playwright
```

已具備、不需處理：

* Chromium 已預裝於 `/opt/pw-browsers`，`PLAYWRIGHT_BROWSERS_PATH` 已設好，**不要**跑
  `playwright install`。版本對不上時改用 `executablePath: '/opt/pw-browsers/chromium'`。
* 中文字型 `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc` 已存在（Pillow 後備字型），另有 Noto CJK。

尚未設定：R2 圖床的 `R2_ACCOUNT_ID`、`R2_ACCESS_KEY_ID`、`R2_SECRET_ACCESS_KEY`、
`R2_BUCKET`、`R2_PUBLIC_BASE_URL`。未設定時走備案（圖片 commit 進 repo）。

`component-doc-figma` 需要 Figma Desktop app（Plugin API）＋終端機能跑 Node。

## 尚未安裝的交叉引用

以下 skill 被引用但不在本 repo，用到相關段落時要另外補：

| 被引用的 skill | 引用處 | 影響 |
| :--- | :--- | :--- |
| `spec-doc-1111` | screenshot-replace（截圖標注／覆蓋、`初始化` 不編號） | screenshot-replace 已內聯主要重點，缺這支不影響標號流程 |
| `figma-use` | component-doc-figma | 由 Figma MCP 提供（`skill://figma/figma-use/SKILL.md`），不需另裝 |
| `annotations-figma` | component-doc-figma | 只在「把 annotation 當獨立規格輸出」時需要 |
| `export-tokens-figma` | component-doc-figma | 只在「匯出整套 token 系統」時需要 |

## 改名對照

安裝時把原始壓縮檔的名稱改成更好記的名字，舊文件若出現舊名，對照如下。
（截圖兩支中途曾短暫叫過 `shot-overlay`／`shot-burn`，那組名字看不懂，已廢棄。）

| 舊名 | 新名 | 為什麼改 |
| :--- | :--- | :--- |
| `photo` | `screenshot-add` | 「photo」看不出是標註工具，也看不出跟 `png` 差在哪；`add` 直接說出它做什麼 |
| `png` | `screenshot-replace` | 「png」是檔案格式不是工作流程；`replace` 點出它唯一不可取代的能力——換掉圖裡原有的內容 |
| `generate-component-doc-figma` | `component-doc-figma` | 去掉冗贅的 `generate-`，並對齊 `*-figma` 家族命名 |

## 安裝新 skill 的流程

1. 解壓到 `.claude/skills/<name>/`，`SKILL.md` 的 frontmatter `name` 必須等於資料夾名。
2. 檢查腳本有無對外網路請求／`child_process`，並跑語法檢查。
3. 名稱不好記就改名，**同時更新所有交叉引用**（`grep -rn` 舊名確認無殘留）。
4. **在本 wiki 加一頁詳頁、並把它加進上方索引表**，改名的話補進〈改名對照〉。
5. 確認交叉引用到的其他 skill 是否存在，缺的列進〈尚未安裝的交叉引用〉。
6. commit ＋ push；在本機跑 `bash .claude/skills/wiki/sync-to-github-wiki.sh` 同步到 GitHub Wiki。

## 同步到 GitHub Wiki

本目錄是**唯一事實來源**，GitHub Wiki（<https://github.com/LYNN04326/0326/wiki>）是它的鏡像。
改完這裡之後，在**本機**跑：

```bash
bash .claude/skills/wiki/sync-to-github-wiki.sh
```

腳本會 clone wiki repo、把連結轉成 GitHub Wiki 格式（內頁連結去掉 `.md`、指回原始碼的相對路徑
改成絕對 blob 網址）、commit 並推送。

> ⚠️ **不能在 Claude Code session 裡跑這支腳本**：session 的 git proxy 只對授權清單內的 repo
> 注入憑證，而 `*.wiki.git` 不是 GitHub API 認得的 repo，加不進清單，push 一定回 403。
> 讀取（clone）沒問題，只有 push 不行。所以 wiki 同步是**人工在本機執行**的步驟。
>
> ⚠️ 不要直接在 GitHub 網頁上編輯 wiki——下次同步會被覆蓋。

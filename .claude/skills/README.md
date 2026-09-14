# 專案技能（Skills）索引

本資料夾的技能會隨專案版控，在每個 Claude Code session 自動載入。
全部為手動安裝（下載上游 `SKILL.md`），原因見文末「環境限制」。

| 技能 | 用途 | 上游來源 |
|---|---|---|
| `find-skills` | 你問「有沒有能做 X 的技能」時，去開放技能生態搜尋並推薦安裝 | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| `web-design-guidelines` | 依 190 條 Web Interface Guidelines 檢查 UI 程式碼（無障礙、表單、焦點狀態、觸控、i18n…） | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) |
| `frontend-design` | 設計新頁面時的視覺方向指引（配色、字體、版面，避免樣板感） | [anthropics/skills](https://github.com/anthropics/skills) |

## 各技能備註

### web-design-guidelines

上游的 `SKILL.md` 每次檢查時會即時抓取規則檔。本專案另外存了一份快照：

```
references/web-interface-guidelines.md
```

用途是**離線備援** —— 若 `raw.githubusercontent.com` 連不上，可直接讀這份。
快照可能落後上游，正常情況仍以即時抓取的版本為準。

### frontend-design

附上游 `LICENSE.txt`，請保留。

## 更新方式

```bash
cd .claude/skills

curl -sS https://raw.githubusercontent.com/vercel-labs/skills/main/skills/find-skills/SKILL.md \
  -o find-skills/SKILL.md

curl -sS https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/web-design-guidelines/SKILL.md \
  -o web-design-guidelines/SKILL.md
curl -sS https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md \
  -o web-design-guidelines/references/web-interface-guidelines.md

curl -sS https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md \
  -o frontend-design/SKILL.md
```

在**本機**則可用官方 CLI：

```bash
npx skills add https://github.com/vercel-labs/skills --skill find-skills
npx skills add vercel-labs/agent-skills --skill web-design-guidelines
```

## ⚠️ 環境限制（為何手動安裝）

在 **Claude Code 網頁版**的雲端容器中實測：

| 項目 | 狀態 |
|---|---|
| 執行 `npx skills ...` | ❌ 被權限機制擋下（Code from External） |
| 連線 `skills.sh` | ❌ 被網路 egress proxy 擋下（403） |
| 連線 `raw.githubusercontent.com` | ✅ 通 |
| 連線 `registry.npmjs.org` | ✅ 通 |

因此官方 CLI 安裝流程在網頁版走不通，改以 `curl` 取檔並納入版控。

影響範圍：
- `find-skills` 的 CLI 搜尋功能在網頁版失效（改用一般網路搜尋代替），本機環境正常。
- `web-design-guidelines`、`frontend-design` **不受影響**，兩者在網頁版與本機都能完整運作。

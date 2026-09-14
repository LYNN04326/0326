# find-skills（技能來源說明）

- **來源**：[vercel-labs/skills](https://github.com/vercel-labs/skills) → `skills/find-skills/SKILL.md`
- **抓取日期**：2026-09-14
- **用途**：讓 Claude 在你問「有沒有能做 X 的技能」時，主動去開放技能生態搜尋並推薦安裝。

## 更新方式

```bash
curl -sS https://raw.githubusercontent.com/vercel-labs/skills/main/skills/find-skills/SKILL.md \
  -o .claude/skills/find-skills/SKILL.md
```

或在本機用官方 CLI 重裝：

```bash
npx skills add https://github.com/vercel-labs/skills --skill find-skills
```

## ⚠️ 環境限制

在 **Claude Code 網頁版**的雲端容器中，這個技能的核心功能會失效：

| 項目 | 狀態 |
|---|---|
| 執行 `npx skills ...` | ❌ 被權限機制擋下（Code from External） |
| 連線 `skills.sh` | ❌ 被網路 egress proxy 擋下（403） |

**在本機的 Claude Code CLI / 桌面版開啟本專案時，功能才完整。**
在網頁版 session 中，請改用 Claude 內建的一般網路搜尋來找技能，效果相近。

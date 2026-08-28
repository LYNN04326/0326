#!/usr/bin/env bash
# 把 .claude/skills/wiki/ 同步到 GitHub Wiki（https://github.com/LYNN04326/0326/wiki）
#
# 為什麼要有這支：Claude Code 的 git proxy 不接受 *.wiki.git（GitHub API 不把 wiki 當 repo，
# 無法加進 session 的授權清單），所以 wiki 只能從本機推。
#
# 用法：  bash .claude/skills/wiki/sync-to-github-wiki.sh [要在連結中使用的分支名]
set -euo pipefail

REPO_SLUG="LYNN04326/0326"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRANCH="${1:-$(git -C "$SRC" rev-parse --abbrev-ref HEAD)}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "→ clone wiki"
git clone -q "https://github.com/${REPO_SLUG}.wiki.git" "$WORK/wiki"

echo "→ 轉換連結（分支：${BRANCH}）"
SRC="$SRC" DST="$WORK/wiki" BLOB="https://github.com/${REPO_SLUG}/blob/${BRANCH}/.claude/skills/" python3 - <<'PY'
import re, os
SRC, DST, BLOB = os.environ['SRC'], os.environ['DST'], os.environ['BLOB']
pages = {f[:-3] for f in os.listdir(SRC) if f.endswith('.md')}

def fix(m):
    link = m.group(1)
    if link.startswith('../'):                      # 指回 repo 檔案 → 絕對 blob 網址
        return '](' + BLOB + link[3:] + ')'
    base, _, anchor = link.partition('#')            # wiki 內頁 → 去掉 .md
    if base.endswith('.md') and base[:-3] in pages:
        return '](' + base[:-3] + ('#' + anchor if anchor else '') + ')'
    return m.group(0)

for fn in sorted(os.listdir(SRC)):
    if not fn.endswith('.md'):
        continue
    t = re.sub(r'\]\(([^)]+)\)', fix, open(os.path.join(SRC, fn)).read())
    if fn == 'Home.md':
        t = t.rstrip() + (
            '\n\n---\n\n> 本 wiki 由 repo 的 `.claude/skills/wiki/` 同步而來，'
            '**請改那邊再跑 `sync-to-github-wiki.sh`**，不要直接在網頁上編輯（下次同步會被覆蓋）。\n')
    open(os.path.join(DST, fn), 'w').write(t)
    print('  ', fn)
PY

cd "$WORK/wiki"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
  echo "→ 內容沒有變化，不推送"
  exit 0
fi
git add -A
git commit -q -m "Sync skills wiki from .claude/skills/wiki/"
git push -q origin HEAD
echo "→ 完成：https://github.com/${REPO_SLUG}/wiki"

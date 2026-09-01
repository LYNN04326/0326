#!/bin/bash
# SessionStart hook — 安裝 Claude 文件處理 Skill（docx / xlsx / pptx / pdf）所需的依賴。
#
# 背景：Claude Code on the web 的容器預設沒有這些套件，導致 xlsx 的 recalc.py、
# pdf 的轉圖、pptx 的 thumbnail 等腳本無法執行。此 hook 在 session 啟動時補齊。
#
# 本專案（純靜態 HTML）本身沒有建置、測試或 lint 步驟，故此處不做專案依賴安裝。
set -uo pipefail

# 僅在遠端（Claude Code on the web）執行；本機開發不動使用者環境。
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# 依賴安裝失敗不應擋住 session 啟動 —— 本專案的 HTML 工作不需要它們。
# 因此各步驟失敗只警告，最後一律 exit 0。
warn() { echo "[session-start] 警告：$*" >&2; }
info() { echo "[session-start] $*"; }

export DEBIAN_FRONTEND=noninteractive

# ── 1. 系統套件 ────────────────────────────────────────────────
# libreoffice-core 已預裝，但缺 calc/writer/impress，導致 soffice 無法載入任何
# 檔案（Error: source file could not be loaded），xlsx 的公式重算會逾時失敗。
APT_PKGS=()
dpkg -s libreoffice-calc    >/dev/null 2>&1 || APT_PKGS+=(libreoffice-calc)
dpkg -s libreoffice-writer  >/dev/null 2>&1 || APT_PKGS+=(libreoffice-writer)
dpkg -s libreoffice-impress >/dev/null 2>&1 || APT_PKGS+=(libreoffice-impress)
command -v pdftoppm >/dev/null 2>&1          || APT_PKGS+=(poppler-utils)

if [ ${#APT_PKGS[@]} -gt 0 ]; then
  info "安裝系統套件：${APT_PKGS[*]}"
  apt-get update -qq >/dev/null 2>&1 || warn "apt-get update 失敗，改用既有索引"
  apt-get install -y -qq "${APT_PKGS[@]}" >/dev/null 2>&1 || warn "apt 安裝失敗：${APT_PKGS[*]}"
else
  info "系統套件已齊全，略過"
fi

# ── 2. Python 套件 ─────────────────────────────────────────────
# 格式為「import 名稱:pip 套件名」，兩者不一定相同。
PY_SPECS=(
  "openpyxl:openpyxl"
  "pandas:pandas"
  "docx:python-docx"
  "pptx:python-pptx"
  "pypdf:pypdf"
  "pdfplumber:pdfplumber"
  "pdf2image:pdf2image"
  "PIL:pillow"
  "reportlab:reportlab"
  "markitdown:markitdown"
  "lxml:lxml"
  "defusedxml:defusedxml"
)
PIP_MISSING=()
for spec in "${PY_SPECS[@]}"; do
  mod="${spec%%:*}"
  pkg="${spec##*:}"
  python3 -c "import ${mod}" >/dev/null 2>&1 || PIP_MISSING+=("${pkg}")
done

if [ ${#PIP_MISSING[@]} -gt 0 ]; then
  info "安裝 Python 套件：${PIP_MISSING[*]}"
  python3 -m pip install --quiet "${PIP_MISSING[@]}" >/dev/null 2>&1 \
    || warn "pip 安裝失敗：${PIP_MISSING[*]}"
else
  info "Python 套件已齊全，略過"
fi

# ── 3. Node 套件 ───────────────────────────────────────────────
# pptx 的 SKILL.md 宣稱 pptxgenjs 已預裝，實際沒有。
NPM_ROOT="$(npm root -g 2>/dev/null || true)"
if [ -n "${NPM_ROOT}" ] && [ ! -d "${NPM_ROOT}/pptxgenjs" ]; then
  info "安裝 pptxgenjs"
  npm install -g --silent pptxgenjs >/dev/null 2>&1 || warn "pptxgenjs 安裝失敗"
fi

# 全域安裝的模組需要 NODE_PATH 才 require 得到。
if [ -n "${NPM_ROOT}" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export NODE_PATH=\"${NPM_ROOT}\"" >> "${CLAUDE_ENV_FILE}"
fi

info "完成"
exit 0

#!/usr/bin/env bash
# Build the CV from the single source of truth (CV_FILE) into rendercv_output/,
# then assemble a static site/ folder for GitHub Pages.
set -euo pipefail

cd "$(dirname "$0")/.."

CV_FILE="${CV_FILE:-Soheil_Koohi_CV.yaml}"
RENDERCV_VERSION="${RENDERCV_VERSION:-2.8}"
OUT_DIR="rendercv_output"
SITE_DIR="site"

if command -v rendercv >/dev/null 2>&1; then
  RENDERCV=(rendercv)
elif command -v uvx >/dev/null 2>&1; then
  RENDERCV=(uvx --python 3.12 --from "rendercv[full]==${RENDERCV_VERSION}" rendercv)
else
  echo "error: neither 'rendercv' nor 'uvx' found on PATH." >&2
  echo "install one of:" >&2
  echo "  uv tool install --python 3.12 'rendercv[full]==${RENDERCV_VERSION}'" >&2
  echo "  pipx install 'rendercv[full]==${RENDERCV_VERSION}'" >&2
  exit 1
fi

echo ">> rendering ${CV_FILE}"
"${RENDERCV[@]}" render "${CV_FILE}"

BASENAME="$(basename "${CV_FILE%.*}")"
PDF="${OUT_DIR}/${BASENAME}.pdf"
HTML="${OUT_DIR}/${BASENAME}.html"

[ -f "$PDF" ] || { echo "error: expected ${PDF} but it was not produced" >&2; exit 1; }

echo ">> assembling ${SITE_DIR}/"
rm -rf "$SITE_DIR"
mkdir -p "$SITE_DIR"
cp "$PDF" "$SITE_DIR/"
cp "${OUT_DIR}/${BASENAME}.md" "$SITE_DIR/" 2>/dev/null || true

# The landing page is generated from the same YAML, so the site and the PDF can
# never disagree. Needs PyYAML; fall back to uv when the system Python lacks it.
if python3 -c "import yaml" >/dev/null 2>&1; then
  PYTHON=(python3)
elif command -v uv >/dev/null 2>&1; then
  PYTHON=(uv run --quiet --python 3.12 --with pyyaml python)
else
  echo "error: need Python with PyYAML installed, or 'uv' on PATH" >&2
  exit 1
fi
"${PYTHON[@]}" scripts/build_site.py "$CV_FILE"

echo
echo "done:"
echo "  PDF   ${PDF}"
echo "  site  ${SITE_DIR}/index.html"

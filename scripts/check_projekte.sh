#!/usr/bin/env bash
# Build the site and assert the portfolio pages rendered as expected.
set -euo pipefail
cd "$(dirname "$0")/.."

"${HUGO_BIN:-hugo}" --gc --minify --quiet

fail=0
check() {  # check <file> <needle> <description>
  if grep -q -- "$2" "$1" 2>/dev/null; then
    echo "ok   $3"
  else
    echo "FAIL $3  (missing '$2' in $1)"
    fail=1
  fi
}

check public/projekte/index.html 'class=project-grid'          'index renders a card grid'
check public/projekte/index.html 'Vereine & Gemeinwohl'        'index renders the Vereine group heading'
check public/projekte/index.html 'Kinderbasar Biekhofen'       'index lists Kinderbasar'
check public/projekte/kinderbasar/index.html 'project-links'   'detail page renders the link bar'
check public/index.html '>Projekte<'                           'Projekte appears in the main menu'

exit $fail

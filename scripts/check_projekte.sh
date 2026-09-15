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

check public/projekte/index.html 'Vereinswebsite TC Blau-Wei'     'index lists the TCBW website'
check public/projekte/index.html 'Medenspiel-Planner'             'index lists the Medenspiel-Planner'
check public/projekte/index.html 'Getr'                           'index lists the drinks app'
check public/projekte/index.html 'Social-Media-Grafiken'          'index lists the social tools'
check public/projekte/tcbw-website/index.html 'posts/tcbw-website' 'TCBW page links its blog post'

check public/projekte/index.html 'Eigene Produkte'   'index renders the Produkte group heading'
check public/projekte/index.html 'Daten & Zuhause'   'index renders the Daten group heading'
check public/projekte/index.html 'mAI Whisky'        'index lists mAI Tasting'
check public/projekte/index.html 'Doppelkopf'        'index lists doko-stats'

# The doko-stats page must never identify a member of the group.
for name in fabiani niax paumpey ooongbaaak hassan86 flipflop86; do
  if grep -rqi -- "$name" public/projekte/ 2>/dev/null; then
    echo "FAIL privacy: player name '$name' leaked into the portfolio"
    fail=1
  else
    echo "ok   privacy: '$name' absent"
  fi
done

exit $fail

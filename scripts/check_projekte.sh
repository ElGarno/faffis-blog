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
check public/projekte/kinderbasar/index.html 'basar.faffi.cloud'   'detail page links basar.faffi.cloud'
check public/index.html '>Projekte<'                           'Projekte appears in the main menu'

check public/projekte/index.html 'Vereinswebsite TC Blau-Wei'     'index lists the TCBW website'
check public/projekte/index.html 'Medenspiel-Planner'             'index lists the Medenspiel-Planner'
check public/projekte/index.html 'Getränkebuchung am iPad'        'index lists the drinks app'
check public/projekte/index.html 'Social-Media-Grafiken'          'index lists the social tools'
check public/projekte/tcbw-website/index.html 'posts/tcbw-website' 'TCBW page links its blog post'

check public/projekte/index.html 'Eigene Produkte'   'index renders the Produkte group heading'
check public/projekte/index.html 'Daten & Zuhause'   'index renders the Daten group heading'
check public/projekte/index.html 'mAI Whisky'        'index lists mAI Tasting'
check public/projekte/index.html 'Doppelkopf'        'index lists doko-stats'

# The doko-stats page must never identify a member of the group. Scoped to
# all of public/, not just public/projekte/: project bodies are also
# emitted verbatim into public/index.xml (and could leak elsewhere too).
for name in fabiani niax paumpey ooongbaaak hassan86 flipflop86; do
  if grep -rqi -- "$name" public/ 2>/dev/null; then
    echo "FAIL privacy: player name '$name' leaked into the portfolio"
    fail=1
  else
    echo "ok   privacy: '$name' absent"
  fi
done

check public/fuer-vereine/index.html 'class=project-grid' 'Vereins-Seite embeds the card grid'
check public/fuer-vereine/index.html 'Kinderbasar'          'Vereins-Seite shows the Basar reference'
check public/index.html '>Für Vereine<'                     'Für Vereine appears in the main menu'

# The page must not read as a commercial offer. Case-insensitive and
# whole-word (-w) so this doesn't fire on unrelated compounds that merely
# contain the word, like "Abrechnung" or "Preisvergleich". Scoped to all of
# public/, not just /fuer-vereine/index.html, since project bodies are also
# emitted verbatim into public/index.xml.
for word in Honorar Rechnung Angebot Leistungen beauftragen; do
  if grep -rqiw -- "$word" public/ 2>/dev/null; then
    echo "FAIL commercial wording: '$word' found in public/"
    fail=1
  else
    echo "ok   no commercial wording: '$word'"
  fi
done

# "Preis" is scoped to the portfolio pages only, unlike the words above: the
# word appears legitimately in the pre-existing /posts/tcbw-getraenkebuchung/
# post (the drink price field on the iPad kiosk) and that old post is not
# part of what this guard is protecting.
if grep -rqiw -- "Preis" public/fuer-vereine/ public/projekte/ 2>/dev/null; then
  echo "FAIL commercial wording: 'Preis' found on the portfolio pages"
  fail=1
else
  echo "ok   no commercial wording: 'Preis' (portfolio pages)"
fi

# Exactly the five club projects, not all eleven.
n=$(grep -o 'class=project-card>' public/fuer-vereine/index.html | wc -l | tr -d ' ')
if [ "$n" = "5" ]; then echo "ok   Vereins-Seite shows 5 cards"; else echo "FAIL expected 5 cards, got $n"; fail=1; fi

check public/projekte/mai-tasting/index.html 'project-gallery' 'mAI Tasting renders the gallery'

exit $fail

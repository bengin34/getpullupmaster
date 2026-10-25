#!/usr/bin/env bash
# Notify Bing / Yandex / Naver (IndexNow) about new or changed pages.
#
#   scripts/indexnow.sh --all                 # every <loc> in sitemap.xml
#   scripts/indexnow.sh --changed [<base>]    # pages whose index.html changed since <base> (default: HEAD~1)
#   scripts/indexnow.sh URL [URL...]          # explicit URLs
#
# The key file lives at the site root (<KEY>.txt) and is public by design.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST="getpullupmaster.app"
KEY="0b41628e52eab36ebf653a9385beffc6"
KEY_LOCATION="https://${HOST}/${KEY}.txt"

urls=()
case "${1:-}" in
  --all)
    while IFS= read -r u; do urls+=("$u"); done < <(grep -o '<loc>[^<]*</loc>' "$ROOT/sitemap.xml" | sed -e 's|<loc>||' -e 's|</loc>||')
    ;;
  --changed)
    base="${2:-HEAD~1}"
    while IFS= read -r f; do
      case "$f" in
        index.html) urls+=("https://${HOST}/") ;;
        */index.html) urls+=("https://${HOST}/${f%index.html}") ;;
      esac
    done < <(git -C "$ROOT" diff --name-only --diff-filter=AM "$base" HEAD -- 'index.html' '*/index.html')
    ;;
  "")
    sed -n '2,8p' "$0"; exit 2 ;;
  *)
    urls=("$@") ;;
esac

if [ "${#urls[@]}" -eq 0 ]; then
  echo "indexnow: nothing to submit"; exit 0
fi

payload=$(printf '%s\n' "${urls[@]}" | python3 -I -c '
import json, sys
urls = [l.strip() for l in sys.stdin if l.strip()]
print(json.dumps({"host": sys.argv[1], "key": sys.argv[2], "keyLocation": sys.argv[3], "urlList": urls}))
' "$HOST" "$KEY" "$KEY_LOCATION")

echo "indexnow: submitting ${#urls[@]} URL(s)"
printf '  %s\n' "${urls[@]}"
for endpoint in "https://www.bing.com/indexnow" "https://api.indexnow.org/indexnow"; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -X POST "$endpoint" \
    -H 'Content-Type: application/json; charset=utf-8' --data-binary "$payload")
  echo "  $endpoint -> HTTP $code"
  case "$code" in 200|202) ;; *) echo "indexnow: $endpoint rejected the request" >&2; exit 1 ;; esac
done

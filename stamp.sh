#!/bin/bash
# Stamps index.html with the current git short SHA + UTC build time.
# Run before pushing/deploying. Idempotent — safe to run repeatedly.
cd "$(dirname "$0")"
SHA=$(git rev-parse --short HEAD 2>/dev/null || echo dev)
DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
python3 - "$SHA" "$DATE" <<'PY'
import re, sys
sha, date = sys.argv[1], sys.argv[2]
p = 'index.html'
s = open(p).read()
s = re.sub(r'const BUILD = \{[^}]*\};',
           'const BUILD = { sha: "%s", date: "%s" };' % (sha, date), s)
open(p, 'w').write(s)
print("Stamped build:", sha, date)
PY

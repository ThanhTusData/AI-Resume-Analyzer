#!/usr/bin/env bash
set -euo pipefail
MON_DIR=${MONITORING_DIR:-monitoring}
OUT_DIR="${MON_DIR}/archive"
mkdir -p "$OUT_DIR"
ts=$(date +%Y%m%d_%H%M%S)
if [ -f "${MON_DIR}/requests.log" ]; then
  mv "${MON_DIR}/requests.log" "${OUT_DIR}/requests_${ts}.log"
  gzip "${OUT_DIR}/requests_${ts}.log"
  echo "Rotated monitoring log to ${OUT_DIR}/requests_${ts}.log.gz"
else
  echo "No monitoring log to rotate"
fi
# optionally remove archives older than 90 days
find "${OUT_DIR}" -type f -mtime +90 -delete

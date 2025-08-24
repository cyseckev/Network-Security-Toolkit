#!/usr/bin/env bash
# Rotating tcpdump capture with optional BPF filter
# Usage: sudo ./capture_rotate.sh eth0 "tcp port 443 or udp port 53"
set -euo pipefail

IFACE="${1:-}"
FILTER="${2:-}"
OUT_DIR="./out/captures"
mkdir -p "${OUT_DIR}"

if [[ -z "${IFACE}" ]]; then
  echo "Usage: sudo $0 <interface> [BPF_FILTER]"
  exit 1
fi

FILE_BASENAME="${OUT_DIR}/capture_$(date +%Y%m%d-%H%M%S).pcap"
# Rotate every 100MB, keep last 20 files
CMD=(tcpdump -i "${IFACE}" -U -w "${FILE_BASENAME}" -C 100 -W 20)
if [[ -n "${FILTER}" ]]; then
  CMD+=(${FILTER})
fi

echo "[*] Starting capture on ${IFACE} (rotate 100MB, keep 20)"
echo "[*] Output prefix: ${FILE_BASENAME}"
exec "${CMD[@]}"

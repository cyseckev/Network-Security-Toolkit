#!/usr/bin/env bash
# Safe network sweep + top-ports scan
# Usage: sudo ./nmap_sweep.sh 192.168.1.0/24 [IFACE]
set -euo pipefail

CIDR="${1:-}"
IFACE="${2:-}"

if [[ -z "${CIDR}" ]]; then
  echo "Usage: sudo $0 <CIDR> [IFACE]"
  exit 1
fi

OUT_DIR="./out/scans"
mkdir -p "${OUT_DIR}"

DATESTR="$(date +%Y%m%d-%H%M%S)"
HOSTS_FILE="${OUT_DIR}/hosts_${DATESTR}.txt"

# Host discovery (no DNS, ARP/ICMP where possible, quiet)
if [[ -n "${IFACE}" ]]; then
  nmap -sn -n -PR -PE --reason --min-rate 1000 -e "${IFACE}" "${CIDR}" -oG - \
    | awk '/Up$/{print $2}' | sort -u > "${HOSTS_FILE}"
else
  nmap -sn -n -PR -PE --reason --min-rate 1000 "${CIDR}" -oG - \
    | awk '/Up$/{print $2}' | sort -u > "${HOSTS_FILE}"
fi

COUNT=$(wc -l < "${HOSTS_FILE}" || echo 0)
echo "[+] Discovered ${COUNT} host(s). Results -> ${HOSTS_FILE}"

if [[ "${COUNT}" -eq 0 ]]; then
  echo "[i] No hosts up. Exiting."
  exit 0
fi

# Top ports scan (safe defaults)
SCAN_OUT="${OUT_DIR}/topports_${DATESTR}.gnmap"
nmap -sS -Pn -n --top-ports 100 --open --min-rate 500 --defeat-rst-ratelimit \
     -iL "${HOSTS_FILE}" -oA "${OUT_DIR}/topports_${DATESTR}"

echo "[+] Port scan done -> ${OUT_DIR}/topports_${DATESTR}.*"

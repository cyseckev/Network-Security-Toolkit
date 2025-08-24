#!/usr/bin/env bash
# Minimal network hardening (iptables + sysctl reload)
set -euo pipefail

echo "[*] Applying baseline iptables policies (INPUT/FORWARD DROP, OUTPUT ACCEPT)"
iptables -F
iptables -X
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH (adjust port via SSH_PORT env)
SSH_PORT="${SSH_PORT:-22}"
iptables -A INPUT -p tcp --dport "${SSH_PORT}" -j ACCEPT

echo "[*] Reloading sysctl (if any custom hardening present)"
sysctl --system || true

echo "[+] Network hardening applied (baseline)."

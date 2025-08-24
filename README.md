# 📡 Network Security Toolkit

A practical toolkit for **traffic capture, scanning, flow extraction, and baseline hardening** on Linux.
Built for blue teams, lab work, and day-to-day defensive ops.

## ✨ Features
- 🔎 Fast host discovery + safe port scans (`nmap_sweep.sh`)
- 🧲 Continuous packet capture with rotation and BPF filters (`capture_rotate.sh`)
- 📊 PCAP → enriched flow CSV using `tshark` (`pcaps_to_flows.py`)
- 🔥 UFW/iptables log analytics (`analyze_firewall_logs.py`)
- 🛡️ Minimal network hardening (`nethardening.sh`)
- 🧠 Starter configs for Suricata & Zeek (local rules, sensible defaults)
- ⏱️ Systemd timer for unattended captures

> Tested on Debian/Ubuntu/Kali. Requires `tcpdump`, `nmap`, `tshark` (Wireshark CLI) for full functionality.

## 🚀 Quick Start

git clone git@github.com:CySecKev/Network-Security-Toolkit.git
cd Network-Security-Toolkit

# Install common deps (optional)
sudo apt update && sudo apt install -y nmap tcpdump tshark

# 1) Safe subnet sweep and top ports
sudo ./toolkit/nmap_sweep.sh 192.168.1.0/24

# 2) Start rotating capture on interface (with BPF filter)
sudo ./toolkit/capture_rotate.sh eth0 "tcp port 443 or udp port 53"

# 3) Convert pcaps to flow CSV
python3 ./toolkit/pcaps_to_flows.py --pcap ./out/captures/*.pcap --out ./out/flows.csv

# 4) Analyze UFW logs
python3 ./toolkit/analyze_firewall_logs.py /var/log/ufw.log --top 15


## 🧰 Suricata/Zeek

- Suricata: drop toolkit/suricata/suricata.yaml & suricata.rules into your setup (or symlink).
- Zeek: include toolkit/zeek/local.zeek in your sensor.

## ⚠️ Safety

- Scripts are defensive & safe defaults.
- Scanning scripts avoid invasive flags.
- Always respect authorization and scope.
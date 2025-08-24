# Usage

## 1) Nmap sweep (safe)
sudo ./toolkit/nmap_sweep.sh 192.168.1.0/24

## 2) Continuous capture with rotation
sudo ./toolkit/capture_rotate.sh eth0 "tcp port 443 or udp port 53"
# Files land in ./out/captures (ignored by git)

## 3) PCAP → flow CSV
python3 ./toolkit/pcaps_to_flows.py --pcap "./out/captures/*.pcap" --out ./out/flows.csv

## 4) UFW/IPTables log analysis
python3 ./toolkit/analyze_firewall_logs.py /var/log/ufw.log --top 20

## 5) Quick baseline hardening
sudo SSH_PORT=22 ./toolkit/nethardening.sh

## 6) Systemd capture timer
sudo cp systemd/nst-capture.* /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now nst-capture.timer
journalctl -u nst-capture.service -f

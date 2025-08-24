# Cheatsheets

## BPF Filters (examples)
- Only TLS: `tcp port 443`
- DNS only: `udp port 53`
- No local subnets: `not net 10.0.0.0/8 and not net 192.168.0.0/16 and not net 172.16.0.0/12`

## Tshark columns (quick)
tshark -r file.pcap -T fields -e _ws.col.Protocol -e ip.src -e tcp.dstport

## Nmap quick
nmap -sn -n 192.168.1.0/24
nmap -sS -Pn -n --top-ports 100 --open -iL hosts.txt

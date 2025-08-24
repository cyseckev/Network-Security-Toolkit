#!/usr/bin/env python3
"""
Convert PCAPs to simple flow CSV using tshark (no Python deps).
Each row: timestamp,src_ip,src_port,dst_ip,dst_port,proto,bytes
"""
import argparse, glob, os, subprocess, sys

FIELDS = [
    "-e", "frame.time_epoch",
    "-e", "ip.src",
    "-e", "tcp.srcport",
    "-e", "udp.srcport",
    "-e", "ip.dst",
    "-e", "tcp.dstport",
    "-e", "udp.dstport",
    "-e", "_ws.col.Protocol",
    "-e", "frame.len",
]

def run_tshark(pcap):
    cmd = ["tshark", "-r", pcap, "-T", "fields"] + FIELDS
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"[!] tshark error on {pcap}: {res.stderr}", file=sys.stderr)
    return res.stdout.splitlines()

def normalize(line):
    parts = line.split("\t")
    # Expected indices based on FIELDS (tshark prints tabs between fields)
    ts   = parts[0] if len(parts) > 0 else ""
    sip  = parts[1] if len(parts) > 1 else ""
    sport= parts[2] or parts[3] if len(parts) > 4 else ""
    dip  = parts[4] if len(parts) > 4 else ""
    dport= parts[5] or parts[6] if len(parts) > 7 else ""
    proto= parts[7] if len(parts) > 7 else ""
    blen = parts[8] if len(parts) > 8 else ""
    return f"{ts},{sip},{sport},{dip},{dport},{proto},{blen}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pcap", nargs="+", required=True, help="PCAP files or globs")
    ap.add_argument("--out", required=True, help="Output CSV path")
    args = ap.parse_args()

    files = []
    for p in args.pcap:
        files.extend(glob.glob(p))
    files = [f for f in files if os.path.exists(f)]
    if not files:
        print("[!] No input pcaps found.", file=sys.stderr)
        sys.exit(1)

    with open(args.out, "w") as f:
        f.write("timestamp,src_ip,src_port,dst_ip,dst_port,proto,bytes\n")
        for p in files:
            for line in run_tshark(p):
                f.write(normalize(line) + "\n")
    print(f"[+] Wrote flows: {args.out}")

if __name__ == "__main__":
    main()

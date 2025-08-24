#!/usr/bin/env python3
"""
Quick stats for UFW/iptables LOG lines.
Usage: python3 analyze_firewall_logs.py /var/log/ufw.log --top 20
"""
import argparse, re, sys
from collections import Counter

def parse_line(line):
    # Works for UFW's default LOG format and many iptables LOG lines
    src = re.search(r"SRC=([0-9\.]+)", line)
    dst = re.search(r"DST=([0-9\.]+)", line)
    dpt = re.search(r"DPT=(\d+)", line)
    proto = re.search(r"PROTO=([A-Z0-9]+)", line)
    return (
        (src.group(1) if src else "?"),
        (dst.group(1) if dst else "?"),
        (dpt.group(1) if dpt else "?"),
        (proto.group(1) if proto else "?")
    )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logfile", help="Path to firewall log (e.g., /var/log/ufw.log)")
    ap.add_argument("--top", type=int, default=10, help="Top N offenders/services")
    args = ap.parse_args()

    src_count = Counter()
    dport_count = Counter()
    proto_count = Counter()

    try:
        with open(args.logfile, "r", errors="ignore") as f:
            for line in f:
                s, d, dpt, pr = parse_line(line)
                if s != "?": src_count[s] += 1
                if dpt != "?": dport_count[dpt] += 1
                if pr != "?": proto_count[pr] += 1
    except FileNotFoundError:
        print(f"[!] Log not found: {args.logfile}", file=sys.stderr)
        sys.exit(1)

    print("=== Top Sources ===")
    for ip, c in src_count.most_common(args.top):
        print(f"{ip:16} {c}")

    print("\n=== Top Destination Ports ===")
    for p, c in dport_count.most_common(args.top):
        print(f"{p:6} {c}")

    print("\n=== Protocols ===")
    for p, c in proto_count.most_common():
        print(f"{p:6} {c}")

if __name__ == "__main__":
    main()

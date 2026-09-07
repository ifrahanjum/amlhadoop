#!/usr/bin/env python3
import sys
import math
from collections import defaultdict

graph = defaultdict(set)
amounts = {}

# 1. Build Graph in Memory
for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) == 3 and parts[0] == "PATH":
        path, amount = parts[1], int(parts[2])
        src, dst = path.split('->')
        graph[src].add(dst)
        amounts[(src, dst)] = amount

print("==========================================================================")
print("        FINANCIAL CRIME DETECTOR: CIRCULAR MONEY LAUNDERING REPORT        ")
print("==========================================================================")
print("[*] ANALYZING DISTRIBUTED TRANSACTION GRAPH FOR CYCLIC FRAUD RINGS...\n")

detected_rings = set()

# 2. Traverse Graph and Calculate Dynamic Confidence
for a in graph:
    for b in graph[a]:
        if b == a: continue
        for c in graph[b]:
            if c == a or c == b: continue
            if a in graph[c]:
                ring = tuple(sorted([a, b, c]))
                if ring not in detected_rings:
                    detected_rings.add(ring)
                    
                    v1 = amounts.get((a, b), 0)
                    v2 = amounts.get((b, c), 0)
                    v3 = amounts.get((c, a), 0)
                    total_vol = v1 + v2 + v3
                    
                    # Heuristic: Coefficient of Variation
                    mean_val = total_vol / 3.0
                    variance = ((v1 - mean_val)**2 + (v2 - mean_val)**2 + (v3 - mean_val)**2) / 3.0
                    std_dev = math.sqrt(variance)
                    
                    # Avoid division by zero
                    cv = std_dev / mean_val if mean_val > 0 else 0
                    
                    # Scale to a confidence percentage (perfect match = 99.9%)
                    confidence = max(50.0, 99.9 - (cv * 60))
                    
                    risk_level = "CRITICAL" if confidence > 90 else "HIGH" if confidence > 75 else "ELEVATED"
                    
                    print(f"  [!] FRAUD RING DETECTED: {a} -> {b} -> {c} -> {a}")
                    print(f"      --> Total Volume Layered: ${total_vol:,} USD")
                    print(f"      --> Risk Rating: {risk_level} ({confidence:.1f}% Confidence Circular Smurfing)\n")

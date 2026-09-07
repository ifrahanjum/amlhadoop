#!/usr/bin/env python3
import sys
from collections import defaultdict

graph = defaultdict(list)

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) == 2:
        sender, target_info = parts[0], parts[1]
        receiver, amount = target_info.split(':')
        graph[sender].append((receiver, int(amount)))

for sender, neighbors in graph.items():
    total_out = sum(amt for _, amt in neighbors)
    targets = ",".join([f"{r}:{a}" for r, a in neighbors])
    print(f"{sender}\tTOTAL_OUT={total_out}\tTARGETS={targets}")

#!/usr/bin/env python3
import sys

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) == 3:
        sender = parts[0]
        # Strip the prefix and split the targets
        targets_str = parts[2].replace("TARGETS=", "")
        targets = targets_str.split(',')
        for t in targets:
            if ':' in t:
                receiver, amount = t.split(':')
                # Emit a 1-hop path: A -> B
                print(f"PATH\t{sender}->{receiver}\t{amount}")

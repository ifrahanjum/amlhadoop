#!/usr/bin/env python3
import sys

for line in sys.stdin:
    parts = line.strip().split(',')
    if len(parts) == 3:
        sender, receiver, amount = parts[0], parts[1], int(parts[2])
        print(f"{sender}\t{receiver}:{amount}")

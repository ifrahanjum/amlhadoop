#!/usr/bin/env python3
import sys

# Format: Sender_Acc, Receiver_Acc, Amount
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    parts = line.split(',')
    if len(parts) >= 3:
        sender = parts[0].strip()
        amount = parts[2].strip()
        # Map sender account as key, transaction amount as value
        print(f"{sender}\t{amount}")

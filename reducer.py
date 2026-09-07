#!/usr/bin/env python3
import sys

current_account = None
total_volume = 0.0
tx_count = 0

# CSV Header for PyTorch ML pipeline
print("Cycle_ID,Total_Volume,Time_Span_Sec,Is_Flagged")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    parts = line.split('\t')
    if len(parts) != 2:
        continue
        
    account, amount_str = parts[0], parts[1]
    try:
        amount = float(amount_str)
    except ValueError:
        continue

    if current_account == account:
        total_volume += amount
        tx_count += 1
    else:
        if current_account:
            # Flag high-volume/high-frequency accounts (>10,000 volume or >3 transactions)
            is_flagged = 1 if (total_volume > 10000 or tx_count > 3) else 0
            print(f"{current_account},{total_volume:.2f},{tx_count},{is_flagged}")
        
        current_account = account
        total_volume = amount
        tx_count = 1

if current_account:
    is_flagged = 1 if (total_volume > 10000 or tx_count > 3) else 0
    print(f"{current_account},{total_volume:.2f},{tx_count},{is_flagged}")

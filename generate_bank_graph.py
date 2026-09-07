import random

normal_accs = [f"ACC_{i:04d}" for i in range(100, 300)]

# Hidden laundering ring accounts
ring1 = ["MULE_801", "MULE_802", "MULE_803"]
ring2 = ["MULE_901", "MULE_902", "MULE_903"]

with open("bank_transactions.csv", "w") as f:
    # 1. Normal transactions
    for _ in range(50000):
        sender = random.choice(normal_accs)
        receiver = random.choice(normal_accs)
        if sender != receiver:
            amount = random.randint(50, 5000)
            f.write(f"{sender},{receiver},{amount}\n")
    
    # 2. Inject Laundering Ring 1 (MULE_801 -> MULE_802 -> MULE_803 -> MULE_801)
    for _ in range(100):
        f.write(f"{ring1[0]},{ring1[1]},50000\n")
        f.write(f"{ring1[1]},{ring1[2]},49500\n")
        f.write(f"{ring1[2]},{ring1[0]},49000\n")

    # 3. Inject Laundering Ring 2 (MULE_901 -> MULE_902 -> MULE_903 -> MULE_901)
    for _ in range(80):
        f.write(f"{ring2[0]},{ring2[1]},75000\n")
        f.write(f"{ring2[1]},{ring2[2]},74000\n")
        f.write(f"{ring2[2]},{ring2[0]},73500\n")
        
print("Dataset generated successfully: bank_transactions.csv")

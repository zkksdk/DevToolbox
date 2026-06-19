#!/usr/bin/env python3
"""Generate airdrop tracking spreadsheet."""
import csv
from datetime import datetime

chains = [
    {
        "chain": "Monad",
        "funding": "$225M",
        "stage": "Testnet",
        "faucet": "https://testnet.monad.xyz/faucet",
        "address": "0x1485c6A111E4A522eF7AA9708643739bFf23bcA2",
        "actions_needed": "Swap on Kuru, bridge, mint NFT, daily tx",
        "potential": "HIGH",
        "estimated_value": "$500-$5000",
    },
    {
        "chain": "Linea",
        "funding": "$725M (ConsenSys)",
        "stage": "Mainnet (LXP tracking)",
        "faucet": "https://www.infura.io/faucet/linea",
        "address": "0x1485c6A111E4A522eF7AA9708643739bFf23bcA2",
        "actions_needed": "Bridge to Linea, use DApps, swap, provide liquidity",
        "potential": "HIGH",
        "estimated_value": "$300-$3000",
    },
    {
        "chain": "Scroll",
        "funding": "$80M",
        "stage": "Mainnet (Marks tracking)",
        "faucet": "https://faucet.quicknode.com/scroll/sepolia",
        "address": "0x1485c6A111E4A522eF7AA9708643739bFf23bcA2",
        "actions_needed": "Bridge, swap, mint, deploy contract",
        "potential": "MEDIUM",
        "estimated_value": "$100-$1000",
    },
    {
        "chain": "Base",
        "funding": "Coinbase",
        "stage": "Mainnet (ongoing rounds)",
        "faucet": "https://www.alchemy.com/faucets/base-sepolia",
        "address": "0x1485c6A111E4A522eF7AA9708643739bFf23bcA2",
        "actions_needed": "Bridge ETH, swap on Aerodrome, mint NFTs",
        "potential": "MEDIUM",
        "estimated_value": "$50-$500",
    },
    {
        "chain": "MegaETH",
        "funding": "$20M+",
        "stage": "Testnet",
        "faucet": "https://carrot.megaeth.com/faucet",
        "address": "0x1485c6A111E4A522eF7AA9708643739bFf23bcA2",
        "actions_needed": "Daily faucet, swap, interact with DApps",
        "potential": "MEDIUM-HIGH",
        "estimated_value": "$100-$2000",
    },
    {
        "chain": "Arbitrum",
        "funding": "$123M",
        "stage": "Mainnet (ongoing ecosystem)",
        "faucet": "https://www.alchemy.com/faucets/arbitrum-sepolia",
        "address": "0x1485c6A111E4A522eF7AA9708643739bFf23bcA2",
        "actions_needed": "Bridge, swap on GMX/Camelot, LP",
        "potential": "LOW-MEDIUM",
        "estimated_value": "$50-$300",
    },
]

# Write CSV
csv_path = "airdrop_tracker.csv"
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Priority", "Chain", "Funding", "Stage", "Potential",
        "Est. Value", "Wallet", "Balance", "Faucet", "Actions Needed",
        "Last Interaction", "Notes"
    ])
    writer.writeheader()
    for i, c in enumerate(chains):
        writer.writerow({
            "Priority": i + 1,
            "Chain": c["chain"],
            "Funding": c["funding"],
            "Stage": c["stage"],
            "Potential": c["potential"],
            "Est. Value": c["estimated_value"],
            "Wallet": c["address"],
            "Balance": "0",
            "Faucet": c["faucet"],
            "Actions Needed": c["actions_needed"],
            "Last Interaction": datetime.now().strftime("%Y-%m-%d"),
            "Notes": "Zero capital strategy",
        })

print(f"[OK] Tracker saved to {csv_path}")
print(f"[OK] {len(chains)} chains tracked")

# Print summary
print()
print("=" * 60)
print("  AIRDROP TRACKING SUMMARY")
print("=" * 60)
print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"  Wallet: 0x1485c6A111E4A522eF7AA9708643739bFf23bcA2")
print()
print(f"  {'#':<4} {'Chain':<12} {'Potential':<14} {'Est. Value':<16} {'Stage'}")
print(f"  {'-'*4} {'-'*12} {'-'*14} {'-'*16} {'-'*10}")
for i, c in enumerate(chains):
    print(f"  {i+1:<4} {c['chain']:<12} {c['potential']:<14} {c['estimated_value']:<16} {c['stage']}")
print()
print(f"  Total potential: $1,150 - $11,800+")
print(f"  Cost: $0")
print("=" * 60)

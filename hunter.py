#!/usr/bin/env python3
"""
Airdrop Hunter - Multi-chain testnet interaction script.
Zero capital required. Interacts with testnets to qualify for airdrops.

Supported chains:
  - Monad Testnet (MON - $225M funding)
  - MegaETH Testnet
  - Linea Sepolia
  - Scroll Sepolia
  - Base Sepolia
  - Arbitrum Sepolia

Usage:
  python hunter.py                    # Check balances on all testnets
  python hunter.py --claim faucet     # Claim from all available faucets
  python hunter.py --chain monad      # Focus on Monad only
  python hunter.py --swap             # Perform swap transactions
  python hunter.py --bridge           # Cross-chain bridge transactions
  python hunter.py --all              # Full interaction: claim + swap + bridge
"""

import json
import os
import time
import random
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from typing import Dict, List, Tuple, Optional

# ============================================================
# CONFIG
# ============================================================

# Load wallet
with open("wallet_config.json", "r") as f:
    WALLET = json.load(f)

PRIMARY_ACCT: LocalAccount = Account.from_key(WALLET["primary"]["private_key"])
PRIMARY_ADDRESS = WALLET["primary"]["address"]

# Testnet RPCs (public endpoints)
CHAINS = {
    "monad": {
        "name": "Monad Testnet",
        "rpc": "https://testnet-rpc.monad.xyz",
        "chain_id": 10143,
        "token": "MON",
        "explorer": "https://testnet.monadexplorer.com",
        "faucets": [
            "https://testnet.monad.xyz/faucet",  # might need browser
        ],
        "funding": "$225M",
        "priority": 1,
    },
    "linea": {
        "name": "Linea Sepolia",
        "rpc": "https://rpc.sepolia.linea.build",
        "chain_id": 59141,
        "token": "ETH",
        "explorer": "https://sepolia.lineascan.build",
        "funding": "$725M (ConsenSys)",
        "priority": 1,
    },
    "scroll": {
        "name": "Scroll Sepolia",
        "rpc": "https://sepolia-rpc.scroll.io",
        "chain_id": 534351,
        "token": "ETH",
        "explorer": "https://sepolia.scrollscan.com",
        "funding": "$80M",
        "priority": 2,
    },
    "base": {
        "name": "Base Sepolia",
        "rpc": "https://sepolia.base.org",
        "chain_id": 84532,
        "token": "ETH",
        "explorer": "https://sepolia.basescan.org",
        "funding": "Coinbase",
        "priority": 2,
    },
    "arbitrum": {
        "name": "Arbitrum Sepolia",
        "rpc": "https://sepolia-rollup.arbitrum.io/rpc",
        "chain_id": 421614,
        "token": "ETH",
        "explorer": "https://sepolia.arbiscan.io",
        "funding": "$123M",
        "priority": 3,
    },
    "megaeth": {
        "name": "MegaETH Testnet",
        "rpc": "https://carrot.megaeth.com/rpc",
        "chain_id": 6342,
        "token": "ETH",
        "explorer": "https://megaexplorer.xyz",
        "funding": "$20M+",
        "priority": 2,
    },
}

# Swap test DEX contracts (testnet addresses)
DEXES = {
    "monad": {
        "router": "0x...",  # placeholder - need actual testnet DEX address
    },
}

# ============================================================
# CORE FUNCTIONS
# ============================================================

def connect_chain(chain_id: str) -> Optional[Web3]:
    """Connect to a chain's RPC."""
    chain = CHAINS.get(chain_id)
    if not chain:
        print(f"  [!] Unknown chain: {chain_id}")
        return None
    
    try:
        w3 = Web3(Web3.HTTPProvider(chain["rpc"], request_kwargs={"timeout": 15}))
        if w3.is_connected():
            return w3
        return None
    except Exception as e:
        print(f"  [!] Connection failed for {chain['name']}: {e}")
        return None


def get_balance(w3: Web3, address: str, chain_name: str) -> float:
    """Get native token balance."""
    try:
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, "ether")
        return float(balance_eth)
    except Exception as e:
        print(f"  [!] Balance check failed on {chain_name}: {e}")
        return 0.0


def check_all_balances():
    """Check balances across all testnets."""
    print("\n" + "=" * 60)
    print("  BALANCE CHECK - ALL TESTNETS")
    print("=" * 60)
    print(f"  Wallet: {PRIMARY_ADDRESS}")
    print()
    
    results = []
    for chain_id, chain in sorted(CHAINS.items(), key=lambda x: x[1]["priority"]):
        w3 = connect_chain(chain_id)
        if w3:
            balance = get_balance(w3, PRIMARY_ADDRESS, chain["name"])
            status = "[OK]" if balance > 0 else "[!!]️ "
            print(f"  {status} {chain['name']:<25} {balance:.6f} {chain['token']}  "
                  f"(Funding: {chain.get('funding', 'N/A')})")
            results.append({
                "chain": chain_id,
                "name": chain["name"],
                "balance": balance,
                "token": chain["token"],
                "rpc_ok": True,
            })
        else:
            print(f"  [!!] {chain['name']:<25} RPC unreachable")
            results.append({
                "chain": chain_id,
                "name": chain["name"],
                "balance": 0,
                "token": chain["token"],
                "rpc_ok": False,
            })
    
    return results


def send_transaction(w3: Web3, chain_id: str, nonce: int = None) -> Optional[str]:
    """Send a self-transfer (0 ETH) to create on-chain activity."""
    chain = CHAINS[chain_id]
    
    if nonce is None:
        nonce = w3.eth.get_transaction_count(PRIMARY_ADDRESS)
    
    tx = {
        "from": PRIMARY_ADDRESS,
        "to": PRIMARY_ADDRESS,  # self-transfer = 0 cost
        "value": 0,
        "nonce": nonce,
        "gas": 21000,
        "gasPrice": w3.eth.gas_price,
        "chainId": chain["chain_id"],
    }
    
    try:
        signed = PRIMARY_ACCT.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        return tx_hash.hex()
    except Exception as e:
        print(f"    [!] TX failed: {e}")
        return None


def do_interaction(chain_id: str, count: int = 3):
    """Perform multiple transactions on a testnet to build activity."""
    chain = CHAINS[chain_id]
    w3 = connect_chain(chain_id)
    
    if not w3:
        print(f"  [!] Cannot connect to {chain['name']}")
        return
    
    balance = get_balance(w3, PRIMARY_ADDRESS, chain["name"])
    if balance == 0:
        print(f"  [!] No {chain['token']} on {chain['name']}. Use faucet first.")
        return
    
    print(f"\n  {'='*50}")
    print(f"  INTERACTING ON: {chain['name']}")
    print(f"  Balance: {balance:.6f} {chain['token']}")
    print(f"  {'='*50}")
    
    for i in range(count):
        nonce = w3.eth.get_transaction_count(PRIMARY_ADDRESS)
        tx_hash = send_transaction(w3, chain_id, nonce)
        if tx_hash:
            print(f"  [{i+1}/{count}] [OK] TX sent: {tx_hash[:16]}...")
            time.sleep(random.uniform(3, 8))  # random delay
        else:
            print(f"  [{i+1}/{count}] [!!] TX failed")
    
    new_balance = get_balance(w3, PRIMARY_ADDRESS, chain["name"])
    print(f"  Final balance: {new_balance:.6f} {chain['token']}")


def do_faucet_claim_script(chain_id: str):
    """Generate faucet claim URL. Most testnet faucets need browser interaction.
    This provides the URLs and instructions for manual claiming."""
    chain = CHAINS[chain_id]
    
    print(f"\n  --- {chain['name']} Faucet ---")
    
    faucet_urls = {
        "monad": [
            "https://testnet.monad.xyz/faucet",
            "https://faucet.quicknode.com/monad/testnet",
        ],
        "linea": [
            "https://www.infura.io/faucet/linea",
            "https://faucet.quicknode.com/linea/sepolia",
        ],
        "scroll": [
            "https://faucet.quicknode.com/scroll/sepolia",
        ],
        "base": [
            "https://www.alchemy.com/faucets/base-sepolia",
            "https://faucet.quicknode.com/base/sepolia",
        ],
        "arbitrum": [
            "https://www.alchemy.com/faucets/arbitrum-sepolia",
            "https://faucet.quicknode.com/arbitrum/sepolia",
        ],
        "megaeth": [
            "https://carrot.megaeth.com/faucet",
        ],
    }
    
    urls = faucet_urls.get(chain_id, [])
    for url in urls:
        print(f"  -> {url}")
    
    print(f"  📋 Wallet address: {PRIMARY_ADDRESS}")
    print(f"  ℹ️  Copy the address above and paste it on the faucet page.")


# ============================================================
# Airdrop Tracking Table
# ============================================================

def generate_tracking_table():
    """Generate an airdrop tracking markdown table."""
    table = """# [*] Airdrop Tracking Table

**Wallet:** `{addr}`  
**Updated:** {date}

## Active Testnet Airdrops

| # | Project | Chain | Funding | Status | Txs | Balance | Notes |
|---|---------|-------|---------|--------|-----|---------|-------|
""".format(addr=PRIMARY_ADDRESS, date=time.strftime("%Y-%m-%d %H:%M"))
    
    for i, (chain_id, chain) in enumerate(sorted(CHAINS.items(), key=lambda x: x[1]["priority"]), 1):
        w3 = connect_chain(chain_id)
        if w3:
            balance = get_balance(w3, PRIMARY_ADDRESS, chain["name"])
            tx_count = w3.eth.get_transaction_count(PRIMARY_ADDRESS)
            status = "🟢 Active" if balance > 0 else "🔴 Need faucet"
            table += f"| {i} | {chain['name']} | {chain_id.title()} | {chain['funding']} | {status} | {tx_count} | {balance:.4f} {chain['token']} | |\n"
        else:
            table += f"| {i} | {chain['name']} | {chain_id.title()} | {chain['funding']} | ⚫ RPC down | - | - | |\n"
    
    table += """
## Interaction Checklist (Weekly)

- [ ] Monad Testnet: 3+ transactions
- [ ] Linea Sepolia: 3+ transactions
- [ ] Scroll Sepolia: 3+ transactions
- [ ] Base Sepolia: 3+ transactions
- [ ] MegaETH Testnet: 3+ transactions
- [ ] Arbitrum Sepolia: 2+ transactions

## Faucet Links

| Chain | Faucet URL |
|-------|-----------|
| Monad | https://testnet.monad.xyz/faucet |
| Linea | https://www.infura.io/faucet/linea |
| Scroll | https://faucet.quicknode.com/scroll/sepolia |
| Base | https://www.alchemy.com/faucets/base-sepolia |
| Arbitrum | https://www.alchemy.com/faucets/arbitrum-sepolia |
| MegaETH | https://carrot.megaeth.com/faucet |

## Strategy

1. **Daily**: Claim faucet tokens on each chain
2. **Weekly**: Perform 3-5 transactions per chain (self-transfers, DApp interactions)
3. **Monthly**: Try cross-chain bridges between testnets
4. **Keep**: Maintain consistent activity across 2-3 months

## Expected Rewards

Based on similar past airdrops:
- Monad: $200-$2000 (high funding, high expectation)
- Linea: $100-$1000  
- Scroll: $50-$500
- Base: $50-$300
- MegaETH: $50-$500
"""
    
    with open("airdrop_tracker.md", "w") as f:
        f.write(table)
    
    print(f"\n  [OK] Airdrop tracker saved to airdrop_tracker.md")


# ============================================================
# MAIN
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="[*] Airdrop Hunter - Zero Capital")
    parser.add_argument("--check", action="store_true", help="Check balances on all chains")
    parser.add_argument("--chain", type=str, help="Focus on specific chain")
    parser.add_argument("--faucet", action="store_true", help="Show faucet URLs")
    parser.add_argument("--interact", type=int, default=0, help="Perform N interactions per chain with balance")
    parser.add_argument("--tracker", action="store_true", help="Generate tracking table")
    parser.add_argument("--all", action="store_true", help="Full run: check + faucet info + tracker")
    
    args = parser.parse_args()
    
    print(f"""
  ╔══════════════════════════════════════════╗
  ║      [*]  AIRDROP HUNTER v0.1             ║
  ║      Zero Capital. Max Returns.          ║
  ║      Wallet: {PRIMARY_ADDRESS[:10]}...{PRIMARY_ADDRESS[-6:]}        ║
  ╚══════════════════════════════════════════╝
""")
    
    if args.all or args.check:
        check_all_balances()
    
    if args.all or args.faucet:
        print("\n" + "=" * 60)
        print("  FAUCET LINKS")
        print("=" * 60)
        if args.chain:
            do_faucet_claim_script(args.chain)
        else:
            for chain_id in sorted(CHAINS.keys(), key=lambda x: CHAINS[x]["priority"]):
                do_faucet_claim_script(chain_id)
    
    if args.interact > 0:
        if args.chain:
            do_interaction(args.chain, args.interact)
        else:
            for chain_id in sorted(CHAINS.keys(), key=lambda x: CHAINS[x]["priority"]):
                do_interaction(chain_id, args.interact)
    
    if args.all or args.tracker:
        generate_tracking_table()
    
    if not any([args.check, args.chain, args.faucet, args.interact, args.tracker, args.all]):
        # Default: check balances only
        check_all_balances()
        print("\n  Usage: python hunter.py --help")


if __name__ == "__main__":
    main()

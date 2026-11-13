"""CLI for agent-p2p-gossip-synchronizer."""
import sys
import argparse
from .gossip import GossipNode

def main():
    parser = argparse.ArgumentParser(description="Agent P2P Gossip Synchronizer CLI")
    parser.add_argument("--demo", action="store_true", help="Run peer-to-peer state synchronization demo")
    args = parser.parse_args()

    if args.demo:
        node_a = GossipNode("agent-us-east")
        node_b = GossipNode("agent-eu-west")
        node_a.set("global_strategy", "depth_first_tree")
        node_b.set("active_workers", 16)
        print("[*] Initial states created on divergent nodes.")
        pushed, pulled = node_a.reconcile_with_peer(node_b)
        print(f"[+] Reconciled: pushed {pushed} keys, pulled {pulled} keys.")
        print(f"[+] Node A strategy: {node_a.get('global_strategy')}, active_workers: {node_a.get('active_workers')}")
        print(f"[+] Node B strategy: {node_b.get('global_strategy')}, active_workers: {node_b.get('active_workers')}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()

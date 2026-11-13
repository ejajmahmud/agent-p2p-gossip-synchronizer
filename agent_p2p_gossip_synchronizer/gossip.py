"""Anti-entropy epidemic gossip protocol implementation."""
import time
from typing import Dict, List, Optional, Tuple, Any

class StateEntry:
    def __init__(self, key: str, value: Any, version: int, origin: str):
        self.key = key
        self.value = value
        self.version = version
        self.origin = origin
        self.updated_at = time.time()

class GossipNode:
    """Decentralized peer node running epidemic anti-entropy synchronization."""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.state: Dict[str, StateEntry] = {}
        self.peers: Set[str] = set()

    def add_peer(self, peer_id: str):
        if peer_id != self.node_id:
            self.peers.add(peer_id)

    def set(self, key: str, value: Any):
        current_ver = self.state[key].version if key in self.state else 0
        self.state[key] = StateEntry(key, value, current_ver + 1, self.node_id)

    def get(self, key: str) -> Optional[Any]:
        entry = self.state.get(key)
        return entry.value if entry else None

    def get_digest(self) -> Dict[str, int]:
        return {k: entry.version for k, entry in self.state.items()}

    def reconcile_with_peer(self, peer: "GossipNode") -> Tuple[int, int]:
        """Performs two-way push-pull anti-entropy reconciliation with a peer."""
        my_digest = self.get_digest()
        peer_digest = peer.get_digest()

        pulled_count = 0
        pushed_count = 0

        # Push items where self has newer version
        for k, peer_ver in peer_digest.items():
            if k not in my_digest or my_digest[k] < peer_ver:
                self.state[k] = peer.state[k]
                pulled_count += 1

        for k, my_ver in my_digest.items():
            if k not in peer_digest or peer_digest[k] < my_ver:
                peer.state[k] = self.state[k]
                pushed_count += 1

        return pushed_count, pulled_count

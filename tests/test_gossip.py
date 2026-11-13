"""Unit tests for agent-p2p-gossip-synchronizer."""
import unittest
from agent_p2p_gossip_synchronizer.gossip import GossipNode

class TestGossipNode(unittest.TestCase):
    def setUp(self):
        self.node1 = GossipNode("node1")
        self.node2 = GossipNode("node2")

    def test_local_crud(self):
        self.node1.set("keyA", "valA")
        self.assertEqual(self.node1.get("keyA"), "valA")
        self.assertEqual(self.node1.state["keyA"].version, 1)

    def test_bidirectional_reconciliation(self):
        self.node1.set("topic", "AI protocols")
        self.node2.set("model", "Gemini 2.5")
        pushed, pulled = self.node1.reconcile_with_peer(self.node2)
        self.assertEqual(self.node1.get("model"), "Gemini 2.5")
        self.assertEqual(self.node2.get("topic"), "AI protocols")

    def test_higher_version_precedence(self):
        self.node1.set("counter", 10)
        self.node1.set("counter", 20)  # version 2
        self.node2.set("counter", 5)   # version 1
        self.node1.reconcile_with_peer(self.node2)
        self.assertEqual(self.node2.get("counter"), 20)

if __name__ == "__main__":
    unittest.main()

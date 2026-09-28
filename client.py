import hashlib
from typing import List, Dict, Any, Tuple

class MerkleTreeStateProofVerifier:
    @staticmethod
    def _sha256(data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @classmethod
    def build_tree(cls, leaves: List[str]) -> Tuple[str, List[List[str]]]:
        if not leaves:
            return "", []
        current_level = [cls._sha256(leaf) for leaf in leaves]
        tree = [current_level]
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                next_level.append(cls._sha256(left + right))
            tree.append(next_level)
            current_level = next_level
        return tree[-1][0], tree

    @classmethod
    def generate_proof(cls, leaves: List[str], leaf_index: int) -> List[Dict[str, str]]:
        _, tree = cls.build_tree(leaves)
        proof = []
        idx = leaf_index
        for level in tree[:-1]:
            is_right = idx % 2 == 1
            sibling_idx = idx - 1 if is_right else idx + 1
            if sibling_idx < len(level):
                proof.append({"position": "left" if is_right else "right", "hash": level[sibling_idx]})
            else:
                proof.append({"position": "right", "hash": level[idx]})
            idx //= 2
        return proof

    @classmethod
    def verify_proof(cls, leaf: str, proof: List[Dict[str, str]], root: str) -> bool:
        curr = cls._sha256(leaf)
        for item in proof:
            sibling = item["hash"]
            if item["position"] == "left":
                curr = cls._sha256(sibling + curr)
            else:
                curr = cls._sha256(curr + sibling)
        return curr == root

    def benchmark_merkle_verification(self) -> Dict[str, Any]:
        tx_leaves = ["agent_tx_001", "agent_tx_002", "agent_tx_003", "agent_tx_004"]
        root, _ = self.build_tree(tx_leaves)
        proof = self.generate_proof(tx_leaves, 2)
        valid = self.verify_proof("agent_tx_003", proof, root)
        return {"root": root, "leaf": "agent_tx_003", "proof_length": len(proof), "verified": valid}

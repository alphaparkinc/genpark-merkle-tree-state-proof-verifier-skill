from client import MerkleTreeStateProofVerifier

def run_example():
    print("=== GenPark Merkle Tree Inclusion Proof Example ===")
    verifier = MerkleTreeStateProofVerifier()
    res = verifier.benchmark_merkle_verification()
    print("Merkle Root:", res["root"])
    print("Proof Verification Status:", res["verified"])

if __name__ == "__main__":
    run_example()
